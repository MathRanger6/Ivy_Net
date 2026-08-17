#!/usr/bin/env python3
"""PD21 — Bernoulli softmax draft MLE (Alex board factorization).

First-pass sketch: fit (λ*, t*) on **fixed empirical rosters** with
season-wise softmax probabilities and independent Bernoulli outcomes.

Board form (PD21 whiteboard):
  p_i ∝ exp(A_i/t) · exp(−λ L^C_{j(i)})
  ⟺ logits_i = A_i/t − λ L^C_i  (within-season softmax)

Likelihood (Alex lock):
  ℓ(λ, t) = Σ_i [ Y_i log p_i + (1 − Y_i) log(1 − p_i) ]
  K is **not** in the formula — sum_i p_i = 1 per season by construction.

Run (repo root):
  python sports/scripts/pd21_draft_bernoulli_mle.py
  python sports/scripts/pd21_draft_bernoulli_mle.py --season 2015
  python sports/scripts/pd21_draft_bernoulli_mle.py --quick   # coarse grid only

Outputs (HEROs_and_PASSes/pd21_mle/):
  PD21_draft_bernoulli_mle_2011_2021.json
  PD21_draft_bernoulli_mle_2011_2021_grid.csv   (--quick or always for audit)
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
    return float(getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0))


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"PD21_draft_bernoulli_mle_{tag}"
    return {
        "json": OUT / f"{stem}.json",
        "grid_csv": OUT / f"{stem}_grid.csv",
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max),
    }


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


def fit_bfgs(
    batches: list[SeasonBatch],
    *,
    lam0: float,
    t0: float,
) -> dict:
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


def main() -> None:
    parser = argparse.ArgumentParser(description="PD21 Bernoulli softmax draft MLE sketch.")
    parser.add_argument("--season-min", type=int, default=FULL_PANEL_SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=FULL_PANEL_SEASON_MAX)
    parser.add_argument("--gamma", type=float, default=None, help="L_C sharpness (default: 539 config)")
    parser.add_argument("--quick", action="store_true", help="Coarse grid only (skip BFGS)")
    parser.add_argument("--lam0", type=float, default=1.5)
    parser.add_argument("--t0", type=float, default=1.0)
    args = parser.parse_args()

    ensure_hero_dirs()
    paths = _output_paths(args.season_min, args.season_max)
    gamma = float(args.gamma if args.gamma is not None else _load_gamma_default())
    seasons = paths["seasons"]

    print(f"Loading empirical panel {seasons} ...")
    panel = gsel._prepare_hero_panel(args.season_min, args.season_max)
    work = attach_player_level_lc(
        panel,
        gamma=gamma,
        season_min=args.season_min,
        season_max=args.season_max,
    )
    batches = season_batches(work)
    n_players = sum(len(b.ability) for b in batches)
    n_drafted = sum(b.k_empirical for b in batches)
    print(
        f"  player-seasons={n_players:,}  drafted={n_drafted:,}  "
        f"seasons={len(batches)}  gamma={gamma:g}"
    )

    # Audit grid (PD20 neighborhood + wide span)
    lam_grid = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    t_grid = np.array([0.01, 0.1, 0.3, 1.0, 3.0, 10.0])
    grid = coarse_grid_search(batches, lam_grid=lam_grid, t_grid=t_grid)
    grid.to_csv(paths["grid_csv"], index=False)
    best_grid = grid.iloc[0].to_dict()
    print(
        f"Grid best: lambda={best_grid['lambda']:.3g} t={best_grid['t']:.3g} "
        f"loglik={best_grid['loglik']:.1f}"
    )

    fit_result: dict | None = None
    if not args.quick:
        print(f"BFGS from lam0={args.lam0:g} t0={args.t0:g} ...")
        fit_result = fit_bfgs(batches, lam0=float(args.lam0), t0=float(args.t0))
        print(
            f"  lambda*={fit_result['lambda_hat']:.4f}  t*={fit_result['t_hat']:.4f}  "
            f"loglik={fit_result['loglik']:.1f}  success={fit_result['success']}"
        )

    meta = {
        "generated": date.today().isoformat(),
        "script": "sports/scripts/pd21_draft_bernoulli_mle.py",
        "season_min": args.season_min,
        "season_max": args.season_max,
        "seasons": seasons,
        "gamma_fixed": gamma,
        "board_form": "p_i ∝ exp(A_i/t) exp(-λ L^C); logits = A/t - λ L^C",
        "likelihood": "Bernoulli product; season-wise softmax; K not in formula",
        "n_player_seasons": n_players,
        "n_drafted": n_drafted,
        "n_seasons": len(batches),
        "grid_best": best_grid,
        "bfgs": fit_result,
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


if __name__ == "__main__":
    main()
