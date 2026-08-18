#!/usr/bin/env python3
"""PD21 — Bernoulli softmax draft MLE (Alex board factorization).

Fit (λ*, γ*, t*) on **fixed empirical rosters** with season-wise softmax
probabilities and independent Bernoulli outcomes.

Board form (PD21 whiteboard):
  p_i ∝ exp(A_i/t) · exp(−λ L^C_{j(i)})
  ⟺ logits_i = A_i/t − λ L^C_i  (within-season softmax)

Likelihood (Alex lock):
  ℓ(λ, t, γ) = Σ_i [ Y_i log p_i + (1 − Y_i) log(1 − p_i) ]
  K is **not** in the formula — sum_i p_i = 1 per season by construction.
  γ enters via L^C (viability sharpness on empirical rosters).

Run (repo root):
  python sports/scripts/pd21_draft_bernoulli_mle.py --season-min 2013
  python sports/scripts/pd21_draft_bernoulli_mle.py --gamma 10   # fix γ; fit λ,t only
  python sports/scripts/pd21_draft_bernoulli_mle.py --quick      # init grid only
  python sports/scripts/pd21_draft_bernoulli_mle.py --profile-gamma --season-min 2013

Default: joint L-BFGS-B on (λ, γ, t). A coarse γ × (λ,t) grid seeds the optimizer.

Outputs (HEROs_and_PASSes/pd21_mle/):
  PD21_draft_bernoulli_mle_{window}.json
  PD21_draft_bernoulli_mle_{window}_grid.csv       (λ×t slice at γ*)
  PD21_draft_bernoulli_mle_{window}_gamma_grid.csv (init audit, one row per γ)
  PD21_draft_bernoulli_mle_{window}_gamma_profile.csv / _gamma_profile.png
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import PD21_MLE, ensure_hero_dirs
from interval_overlap_paths import seasons_label, window_tag

import grandchild_selection_inverted_u_diagnostic as gsel

FULL_PANEL_SEASON_MIN = gsel.FULL_PANEL_SEASON_MIN
FULL_PANEL_SEASON_MAX = gsel.FULL_PANEL_SEASON_MAX
OUT = PD21_MLE

LC_COL = "pool_c_smooth_team"
LOG_EPS = 1e-15
DEFAULT_GAMMA_GRID = (5.0, 10.0, 20.0)
DEFAULT_GAMMA_PROFILE_GRID = (
    5.0, 8.0, 10.0, 15.0, 18.0, 20.0, 30.0, 40.0, 60.0, 80.0, 100.0, 150.0, 200.0
)
DEFAULT_LAM_GRID = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
DEFAULT_T_GRID = np.array([0.01, 0.1, 0.3, 1.0, 3.0, 10.0])


@dataclass(frozen=True)
class SeasonBatch:
    season: int
    ability: np.ndarray
    lc: np.ndarray
    y_draft: np.ndarray
    k_empirical: int


def _load_gamma_default() -> float:
    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return float(getattr(mod, "VIABILITY_SHARPNESS", 18.0))


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"PD21_draft_bernoulli_mle_{tag}"
    return {
        "json": OUT / f"{stem}.json",
        "grid_csv": OUT / f"{stem}_grid.csv",
        "gamma_grid_csv": OUT / f"{stem}_gamma_grid.csv",
        "gamma_profile_csv": OUT / f"{stem}_gamma_profile.csv",
        "gamma_profile_png": OUT / f"{stem}_gamma_profile.png",
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max),
    }


def _parse_gamma_grid(raw: str | None) -> tuple[float, ...]:
    if not raw:
        return DEFAULT_GAMMA_GRID
    vals = tuple(float(x.strip()) for x in raw.split(",") if x.strip())
    if not vals:
        raise ValueError("gamma grid must contain at least one value")
    return vals


def attach_player_level_lc(
    panel: pd.DataFrame,
    *,
    gamma: float,
    season_min: int,
    season_max: int,
) -> pd.DataFrame:
    """Player-season rows with team L_C on empirical rosters (θ per season)."""
    import tier1_pool_assignment as tpa

    parts: list[pd.DataFrame] = []
    for season in range(int(season_min), int(season_max) + 1):
        sub = panel.loc[panel["season"] == int(season)].copy()
        if sub.empty:
            continue
        _, theta, _ = gsel._season_k_theta(panel, int(season))
        use = sub.dropna(subset=["perf", "team_id", "season"]).copy()
        if use.empty:
            continue
        use["pool_id"] = use.groupby(["team_id", "season"], observed=True).ngroup()
        players = use.rename(columns={"perf": "ability"})
        players = tpa.add_team_pool_columns(
            players,
            viability_theta=float(theta),
            viability_sharpness=float(gamma),
        )
        parts.append(players)
    if not parts:
        raise ValueError("No player-season rows after L_C attachment.")
    out = pd.concat(parts, ignore_index=True)
    out = out.dropna(subset=["ability", LC_COL, "Y_draft"])
    return out


def season_batches(work: pd.DataFrame) -> list[SeasonBatch]:
    batches: list[SeasonBatch] = []
    for season, sub in work.groupby("season", observed=True):
        sub = sub.sort_index()
        y = sub["Y_draft"].to_numpy(dtype=float)
        batches.append(
            SeasonBatch(
                season=int(season),
                ability=sub["ability"].to_numpy(dtype=float),
                lc=sub[LC_COL].to_numpy(dtype=float),
                y_draft=y,
                k_empirical=int(y.sum()),
            )
        )
    return batches


def board_logits(ability: np.ndarray, lc: np.ndarray, *, lam: float, t: float) -> np.ndarray:
    """PD21 board: A/t − λ L^C (not (A − λ L^C)/t from sim SCORE)."""
    t_safe = max(float(t), 1e-12)
    return ability / t_safe - float(lam) * lc


def softmax_probs(logits: np.ndarray) -> np.ndarray:
    z = np.asarray(logits, dtype=float)
    z = z - np.max(z)
    ex = np.exp(z)
    s = ex.sum()
    if not np.isfinite(s) or s <= 0.0:
        n = len(z)
        return np.full(n, 1.0 / n if n else np.nan)
    return ex / s


def bernoulli_loglik(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(np.asarray(p, dtype=float), LOG_EPS, 1.0 - LOG_EPS)
    y = np.asarray(y, dtype=float)
    return float(np.sum(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def panel_loglik(batches: list[SeasonBatch], *, lam: float, t: float) -> float:
    total = 0.0
    for batch in batches:
        logits = board_logits(batch.ability, batch.lc, lam=lam, t=t)
        p = softmax_probs(logits)
        total += bernoulli_loglik(batch.y_draft, p)
    return total


def topk_overlap(y: np.ndarray, p: np.ndarray, k: int) -> dict:
    """How well do top-K by p match empirical draft set?"""
    n = len(p)
    k_eff = max(1, min(int(k), n))
    top_idx = np.argsort(-p)[:k_eff]
    pred = np.zeros(n, dtype=bool)
    pred[top_idx] = True
    actual = y.astype(bool)
    tp = int(np.sum(pred & actual))
    return {
        "k": k_eff,
        "overlap": tp,
        "recall": tp / max(int(actual.sum()), 1),
        "precision": tp / k_eff,
    }


def panel_diagnostics(batches: list[SeasonBatch], *, lam: float, t: float) -> dict:
    overlaps: list[int] = []
    recalls: list[float] = []
    sum_p_drafted: list[float] = []
    for batch in batches:
        p = softmax_probs(board_logits(batch.ability, batch.lc, lam=lam, t=t))
        diag = topk_overlap(batch.y_draft, p, batch.k_empirical)
        overlaps.append(diag["overlap"])
        recalls.append(diag["recall"])
        drafted = batch.y_draft.astype(bool)
        sum_p_drafted.append(float(p[drafted].sum()) if drafted.any() else 0.0)
    return {
        "mean_topk_overlap": float(np.mean(overlaps)),
        "mean_topk_recall": float(np.mean(recalls)),
        "mean_sum_p_on_drafted": float(np.mean(sum_p_drafted)),
        "per_season_overlap": overlaps,
    }


def coarse_grid_search(
    batches: list[SeasonBatch],
    *,
    lam_grid: np.ndarray,
    t_grid: np.ndarray,
) -> pd.DataFrame:
    rows: list[dict] = []
    for lam in lam_grid:
        for t in t_grid:
            ll = panel_loglik(batches, lam=float(lam), t=float(t))
            diag = panel_diagnostics(batches, lam=float(lam), t=float(t))
            rows.append(
                {
                    "lambda": float(lam),
                    "t": float(t),
                    "loglik": float(ll),
                    "neg_loglik": float(-ll),
                    **diag,
                }
            )
    return pd.DataFrame(rows).sort_values("loglik", ascending=False)


def fit_at_gamma(
    panel: pd.DataFrame,
    *,
    gamma: float,
    season_min: int,
    season_max: int,
    lam_grid: np.ndarray,
    t_grid: np.ndarray,
    quick: bool,
) -> dict:
    work = attach_player_level_lc(
        panel,
        gamma=gamma,
        season_min=season_min,
        season_max=season_max,
    )
    batches = season_batches(work)
    grid = coarse_grid_search(batches, lam_grid=lam_grid, t_grid=t_grid)
    best_grid = grid.iloc[0].to_dict()
    bfgs: dict | None = None
    if not quick:
        bfgs = fit_bfgs_lt(
            batches,
            lam0=float(best_grid["lambda"]),
            t0=float(best_grid["t"]),
        )
    best_ll = float(bfgs["loglik"]) if bfgs else float(best_grid["loglik"])
    n_players = sum(len(b.ability) for b in batches)
    n_drafted = sum(b.k_empirical for b in batches)
    return {
        "gamma": float(gamma),
        "n_player_seasons": n_players,
        "n_drafted": n_drafted,
        "n_seasons": len(batches),
        "grid_best": best_grid,
        "bfgs": bfgs,
        "loglik_best": best_ll,
        "lambda_best": float(bfgs["lambda_hat"]) if bfgs else float(best_grid["lambda"]),
        "t_best": float(bfgs["t_hat"]) if bfgs else float(best_grid["t"]),
        "grid": grid,
        "batches": batches,
    }


def gamma_outer_search(
    panel: pd.DataFrame,
    *,
    gamma_grid: tuple[float, ...],
    season_min: int,
    season_max: int,
    lam_grid: np.ndarray,
    t_grid: np.ndarray,
    quick: bool,
) -> tuple[list[dict], dict]:
    results: list[dict] = []
    winner: dict | None = None
    for gamma in gamma_grid:
        fit = fit_at_gamma(
            panel,
            gamma=float(gamma),
            season_min=season_min,
            season_max=season_max,
            lam_grid=lam_grid,
            t_grid=t_grid,
            quick=quick,
        )
        summary = {k: v for k, v in fit.items() if k not in {"grid", "batches"}}
        results.append(summary)
        if winner is None or fit["loglik_best"] > winner["loglik_best"]:
            winner = fit
    assert winner is not None
    return results, winner


def panel_loglik_joint(
    panel: pd.DataFrame,
    *,
    season_min: int,
    season_max: int,
    lam: float,
    gamma: float,
    t: float,
) -> tuple[float, list[SeasonBatch]]:
    work = attach_player_level_lc(
        panel,
        gamma=gamma,
        season_min=season_min,
        season_max=season_max,
    )
    batches = season_batches(work)
    return panel_loglik(batches, lam=lam, t=t), batches


def fit_joint_bfgs(
    panel: pd.DataFrame,
    *,
    season_min: int,
    season_max: int,
    lam0: float,
    gamma0: float,
    t0: float,
) -> dict:
    """Joint MLE on (λ, γ, t) via L-BFGS-B in log-parameter space."""
    from scipy.optimize import minimize

    n_eval = 0

    def nll(x: np.ndarray) -> float:
        nonlocal n_eval
        n_eval += 1
        lam = float(np.exp(x[0]))
        gamma = float(np.exp(x[1]))
        t = float(np.exp(x[2]))
        ll, _ = panel_loglik_joint(
            panel,
            season_min=season_min,
            season_max=season_max,
            lam=lam,
            gamma=gamma,
            t=t,
        )
        return -ll

    x0 = np.array(
        [
            np.log(max(lam0, 1e-6)),
            np.log(max(gamma0, 1e-6)),
            np.log(max(t0, 1e-6)),
        ],
        dtype=float,
    )
    res = minimize(nll, x0, method="L-BFGS-B")
    lam_hat = float(np.exp(res.x[0]))
    gamma_hat = float(np.exp(res.x[1]))
    t_hat = float(np.exp(res.x[2]))
    ll_hat, batches = panel_loglik_joint(
        panel,
        season_min=season_min,
        season_max=season_max,
        lam=lam_hat,
        gamma=gamma_hat,
        t=t_hat,
    )
    return {
        "lambda_hat": lam_hat,
        "gamma_hat": gamma_hat,
        "t_hat": t_hat,
        "loglik": float(ll_hat),
        "neg_loglik": float(-ll_hat),
        "success": bool(res.success),
        "message": str(res.message),
        "n_iter": int(getattr(res, "nit", -1)),
        "n_eval": n_eval,
        "start": {"lambda": float(lam0), "gamma": float(gamma0), "t": float(t0)},
        "diagnostics": panel_diagnostics(batches, lam=lam_hat, t=t_hat),
        "batches": batches,
    }


def init_start_from_gamma_grid(
    panel: pd.DataFrame,
    *,
    gamma_grid: tuple[float, ...],
    season_min: int,
    season_max: int,
    lam_grid: np.ndarray,
    t_grid: np.ndarray,
) -> tuple[list[dict], dict]:
    """Coarse γ × (λ,t) grid — seeds joint optimizer; audit only."""
    per_gamma, winner = gamma_outer_search(
        panel,
        gamma_grid=gamma_grid,
        season_min=season_min,
        season_max=season_max,
        lam_grid=lam_grid,
        t_grid=t_grid,
        quick=True,
    )
    return per_gamma, winner


def fit_bfgs_lt(
    batches: list[SeasonBatch],
    *,
    lam0: float,
    t0: float,
) -> dict:
    """Fix γ; optimize (λ, t) only."""
    from scipy.optimize import minimize

    def nll(x: np.ndarray) -> float:
        lam = float(np.exp(x[0]))
        t = float(np.exp(x[1]))
        return -panel_loglik(batches, lam=lam, t=t)

    x0 = np.array([np.log(max(lam0, 1e-6)), np.log(max(t0, 1e-6))], dtype=float)
    res = minimize(nll, x0, method="L-BFGS-B")
    lam_hat = float(np.exp(res.x[0]))
    t_hat = float(np.exp(res.x[1]))
    ll_hat = panel_loglik(batches, lam=lam_hat, t=t_hat)
    return {
        "lambda_hat": lam_hat,
        "t_hat": t_hat,
        "loglik": float(ll_hat),
        "neg_loglik": float(-ll_hat),
        "success": bool(res.success),
        "message": str(res.message),
        "n_iter": int(getattr(res, "nit", -1)),
        "diagnostics": panel_diagnostics(batches, lam=lam_hat, t=t_hat),
    }


def _gamma_summary_rows(per_gamma: list[dict]) -> pd.DataFrame:
    rows: list[dict] = []
    for row in per_gamma:
        bfgs = row.get("bfgs")
        grid_best = row["grid_best"]
        rows.append(
            {
                "gamma": row["gamma"],
                "loglik_best": row["loglik_best"],
                "lambda_best": row["lambda_best"],
                "t_best": row["t_best"],
                "grid_lambda": grid_best["lambda"],
                "grid_t": grid_best["t"],
                "grid_loglik": grid_best["loglik"],
                "bfgs_success": None if bfgs is None else bfgs["success"],
                "mean_topk_recall": (
                    bfgs["diagnostics"]["mean_topk_recall"]
                    if bfgs
                    else grid_best["mean_topk_recall"]
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("loglik_best", ascending=False)


def gamma_profile(
    panel: pd.DataFrame,
    *,
    gamma_values: tuple[float, ...],
    season_min: int,
    season_max: int,
    lam_grid: np.ndarray,
    t_grid: np.ndarray,
) -> pd.DataFrame:
    """Profile loglik(γ) with (λ, t) re-optimized at each γ."""
    rows: list[dict] = []
    for i, gamma in enumerate(gamma_values, start=1):
        print(f"  Profile γ={gamma:g} ({i}/{len(gamma_values)}) ...", flush=True)
        fit = fit_at_gamma(
            panel,
            gamma=float(gamma),
            season_min=season_min,
            season_max=season_max,
            lam_grid=lam_grid,
            t_grid=t_grid,
            quick=False,
        )
        bfgs = fit["bfgs"]
        assert bfgs is not None
        rows.append(
            {
                "gamma": float(gamma),
                "lambda_hat": float(bfgs["lambda_hat"]),
                "t_hat": float(bfgs["t_hat"]),
                "loglik": float(bfgs["loglik"]),
                "neg_loglik": float(bfgs["neg_loglik"]),
                "bfgs_success": bool(bfgs["success"]),
                "mean_topk_recall": float(bfgs["diagnostics"]["mean_topk_recall"]),
            }
        )
        print(
            f"    λ*={bfgs['lambda_hat']:.3g}  t*={bfgs['t_hat']:.3g}  "
            f"loglik={bfgs['loglik']:.2f}",
            flush=True,
        )
    out = pd.DataFrame(rows).sort_values("gamma").reset_index(drop=True)
    out["delta_loglik"] = out["loglik"] - out["loglik"].max()
    return out


def plot_gamma_profile(
    profile: pd.DataFrame,
    *,
    seasons: str,
    out_path: Path,
    gamma_ref: float | None = None,
) -> None:
    import matplotlib.pyplot as plt

    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    gamma = profile["gamma"].to_numpy(dtype=float)
    loglik = profile["loglik"].to_numpy(dtype=float)
    delta = profile["delta_loglik"].to_numpy(dtype=float)
    lam_hat = profile["lambda_hat"].to_numpy(dtype=float)
    t_hat = profile["t_hat"].to_numpy(dtype=float)

    fig, axes = plt.subplots(2, 1, figsize=(8.0, 6.2), sharex=True)

    ax0 = axes[0]
    ax0.plot(gamma, loglik, "o-", color="#1f77b4", lw=2, ms=5)
    ax0.set_ylabel(r"$\ell(\hat\lambda(\gamma), \gamma, \hat t(\gamma))$")
    ax0.grid(True, alpha=0.25)
    ax0.set_title(
        rf"PD21 Bernoulli MLE — $\gamma$ profile ({seasons})",
        fontsize=11,
    )

    ax1 = axes[1]
    ax1.plot(gamma, delta, "o-", color="#d62728", lw=2, ms=5)
    ax1.axhline(0.0, color="0.35", lw=0.8, ls="--")
    ax1.set_ylabel(r"$\Delta\ell$ from best")
    ax1.set_xlabel(r"Viability sharpness $\gamma$ (fixed; re-fit $\lambda, t$)")
    ax1.grid(True, alpha=0.25)

    ax1b = ax1.twinx()
    ax1b.plot(gamma, lam_hat, "s--", color="#2ca02c", lw=1.5, ms=4, alpha=0.9, label=r"$\hat\lambda$")
    ax1b.plot(gamma, t_hat, "^--", color="#9467bd", lw=1.5, ms=4, alpha=0.9, label=r"$\hat t$")
    ax1b.set_ylabel(r"$\hat\lambda$, $\hat t$")

    if gamma_ref is not None:
        for ax in axes:
            ax.axvline(float(gamma_ref), color="#ff7f0e", lw=1.2, ls=":", alpha=0.9)
        axes[0].text(
            float(gamma_ref),
            loglik.max(),
            rf"  $\gamma={gamma_ref:g}$ (sim default)",
            color="#ff7f0e",
            fontsize=8,
            va="top",
        )

    lines_l, labels_l = ax1.get_legend_handles_labels()
    lines_r, labels_r = ax1b.get_legend_handles_labels()
    ax1.legend(lines_l + lines_r, labels_l + labels_r, loc="lower right", fontsize=8, framealpha=0.92)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def run_gamma_profile(args: argparse.Namespace, paths: dict, panel: pd.DataFrame) -> None:
    gamma_values = _parse_gamma_grid(args.profile_gamma_grid)
    seasons = paths["seasons"]
    print(f"γ profile on {seasons}: {', '.join(f'{g:g}' for g in gamma_values)}")
    profile = gamma_profile(
        panel,
        gamma_values=gamma_values,
        season_min=args.season_min,
        season_max=args.season_max,
        lam_grid=DEFAULT_LAM_GRID,
        t_grid=DEFAULT_T_GRID,
    )
    profile.to_csv(paths["gamma_profile_csv"], index=False)
    plot_gamma_profile(
        profile,
        seasons=seasons,
        out_path=paths["gamma_profile_png"],
        gamma_ref=_load_gamma_default(),
    )
    best = profile.loc[profile["loglik"].idxmax()]
    span = float(profile["loglik"].max() - profile["loglik"].min())
    print(
        f"Profile flat span: {span:.3f} nats over γ ∈ "
        f"[{profile['gamma'].min():g}, {profile['gamma'].max():g}]"
    )
    print(
        f"Best on grid: γ={best['gamma']:g}  λ*={best['lambda_hat']:.3g}  "
        f"t*={best['t_hat']:.3g}  loglik={best['loglik']:.2f}"
    )
    print(f"Wrote {paths['gamma_profile_csv']}")
    print(f"Wrote {paths['gamma_profile_png']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PD21 Bernoulli softmax draft MLE sketch.")
    parser.add_argument("--season-min", type=int, default=FULL_PANEL_SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=FULL_PANEL_SEASON_MAX)
    parser.add_argument(
        "--gamma",
        type=float,
        default=None,
        help="Fix γ (fit λ,t only). Default: joint MLE on (λ, γ, t).",
    )
    parser.add_argument(
        "--gamma-grid",
        type=str,
        default=None,
        help=f"Init grid γ values (default: {','.join(str(g) for g in DEFAULT_GAMMA_GRID)}).",
    )
    parser.add_argument("--quick", action="store_true", help="Init grid only (skip BFGS)")
    parser.add_argument(
        "--profile-gamma",
        action="store_true",
        help="Profile loglik vs γ with (λ,t) re-fit at each γ; write CSV + PNG and exit.",
    )
    parser.add_argument(
        "--profile-gamma-grid",
        type=str,
        default=None,
        help=(
            "Comma-separated γ values for --profile-gamma "
            f"(default: {','.join(str(g) for g in DEFAULT_GAMMA_PROFILE_GRID)})."
        ),
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    paths = _output_paths(args.season_min, args.season_max)
    seasons = paths["seasons"]
    gamma_grid = _parse_gamma_grid(args.gamma_grid)

    print(f"Loading empirical panel {seasons} ...")
    panel = gsel._prepare_hero_panel(args.season_min, args.season_max)

    if args.profile_gamma:
        if args.profile_gamma_grid is None:
            args.profile_gamma_grid = ",".join(str(g) for g in DEFAULT_GAMMA_PROFILE_GRID)
        run_gamma_profile(args, paths, panel)
        return

    per_gamma, init = init_start_from_gamma_grid(
        panel,
        gamma_grid=gamma_grid,
        season_min=args.season_min,
        season_max=args.season_max,
        lam_grid=DEFAULT_LAM_GRID,
        t_grid=DEFAULT_T_GRID,
    )
    print(f"  Init γ grid: {', '.join(f'{g:g}' for g in gamma_grid)}")
    for row in per_gamma:
        gb = row["grid_best"]
        print(
            f"  γ={row['gamma']:g}: init λ={gb['lambda']:.3g} "
            f"t={gb['t']:.3g} loglik={gb['loglik']:.1f}"
        )

    lam0 = float(init["lambda_best"])
    gamma0 = float(init["gamma"])
    t0 = float(init["t_best"])
    n_players = init["n_player_seasons"]
    n_drafted = init["n_drafted"]
    n_seasons = init["n_seasons"]

    fit_mode: str
    joint: dict | None = None
    fixed: dict | None = None
    grid_df: pd.DataFrame
    if args.gamma is not None:
        fit_mode = "fixed_gamma_2param"
        fixed = fit_at_gamma(
            panel,
            gamma=float(args.gamma),
            season_min=args.season_min,
            season_max=args.season_max,
            lam_grid=DEFAULT_LAM_GRID,
            t_grid=DEFAULT_T_GRID,
            quick=bool(args.quick),
        )
        gamma_hat = float(args.gamma)
        lam_hat = float(fixed["lambda_best"])
        t_hat = float(fixed["t_best"])
        loglik_hat = float(fixed["loglik_best"])
        batches = fixed["batches"]
        best_grid = fixed["grid_best"]
        grid_df = fixed["grid"]
        fit_result = fixed["bfgs"]
        print(
            f"Fixed γ={gamma_hat:g}: {'grid' if args.quick else 'BFGS'} "
            f"λ*={lam_hat:.4g}  t*={t_hat:.4g}  loglik={loglik_hat:.1f}"
        )
    elif args.quick:
        fit_mode = "grid_init_only"
        gamma_hat = gamma0
        lam_hat = lam0
        t_hat = t0
        loglik_hat = float(init["loglik_best"])
        batches = init["batches"]
        best_grid = init["grid_best"]
        grid_df = init["grid"]
        fit_result = None
        print(
            f"Init only (no BFGS): γ*={gamma_hat:g}  λ*={lam_hat:.4g}  "
            f"t*={t_hat:.4g}  loglik={loglik_hat:.1f}"
        )
    else:
        fit_mode = "joint_3param"
        print(
            f"Joint BFGS from init γ={gamma0:g} λ={lam0:.3g} t={t0:.3g} ..."
        )
        joint = fit_joint_bfgs(
            panel,
            season_min=args.season_min,
            season_max=args.season_max,
            lam0=lam0,
            gamma0=gamma0,
            t0=t0,
        )
        gamma_hat = float(joint["gamma_hat"])
        lam_hat = float(joint["lambda_hat"])
        t_hat = float(joint["t_hat"])
        loglik_hat = float(joint["loglik"])
        batches = joint["batches"]
        fit_result = joint
        work = attach_player_level_lc(
            panel,
            gamma=gamma_hat,
            season_min=args.season_min,
            season_max=args.season_max,
        )
        grid_df = coarse_grid_search(
            season_batches(work),
            lam_grid=DEFAULT_LAM_GRID,
            t_grid=DEFAULT_T_GRID,
        )
        best_grid = grid_df.iloc[0].to_dict()
        print(
            f"Joint MLE: γ*={gamma_hat:.4g}  λ*={lam_hat:.4g}  "
            f"t*={t_hat:.4g}  loglik={loglik_hat:.1f}  "
            f"({joint['n_eval']} evals, success={joint['success']})"
        )

    grid_df.assign(gamma=gamma_hat).to_csv(paths["grid_csv"], index=False)
    _gamma_summary_rows(per_gamma).to_csv(paths["gamma_grid_csv"], index=False)

    meta = {
        "generated": date.today().isoformat(),
        "script": "sports/scripts/pd21_draft_bernoulli_mle.py",
        "season_min": args.season_min,
        "season_max": args.season_max,
        "seasons": seasons,
        "fit_mode": fit_mode,
        "gamma_grid_init": list(gamma_grid),
        "gamma_hat": gamma_hat,
        "lambda_hat": lam_hat,
        "t_hat": t_hat,
        "loglik_hat": loglik_hat,
        "board_form": "p_i ∝ exp(A_i/t) exp(-λ L^C); logits = A/t - λ L^C",
        "likelihood": "Bernoulli product; season-wise softmax; K not in formula",
        "n_player_seasons": n_players,
        "n_drafted": n_drafted,
        "n_seasons": n_seasons,
        "init": {k: v for k, v in init.items() if k not in {"grid", "batches"}},
        "grid_best_at_gamma_hat": best_grid,
        "joint_bfgs": None if joint is None else {k: v for k, v in joint.items() if k != "batches"},
        "fixed_gamma_fit": None if fixed is None else {k: v for k, v in fixed.items() if k not in {"grid", "batches"}},
        "per_gamma_init": per_gamma,
        "pd20_reference_points": [
            {
                "lambda": 1.5,
                "t": 1.0,
                "loglik": panel_loglik(batches, lam=1.5, t=1.0),
                "diagnostics": panel_diagnostics(batches, lam=1.5, t=1.0),
            },
            {
                "lambda": 2.0,
                "t": 1.0,
                "loglik": panel_loglik(batches, lam=2.0, t=1.0),
                "diagnostics": panel_diagnostics(batches, lam=2.0, t=1.0),
            },
        ],
    }
    paths["json"].write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {paths['json']}")
    print(f"Wrote {paths['grid_csv']}")
    print(f"Wrote {paths['gamma_grid_csv']}")


if __name__ == "__main__":
    main()
