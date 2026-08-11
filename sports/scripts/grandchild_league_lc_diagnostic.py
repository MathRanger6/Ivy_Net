#!/usr/bin/env python3
"""Grandchild sim league — team L_C distribution (HAND17 slide 4 analog).

Draw 2015 empirical PPM z abilities, run one Grandchild ASSIGN realization,
then compute team-smooth L_C on the generated rosters (score-side diagnostic).

Run (repo root):
  python sports/scripts/grandchild_league_lc_diagnostic.py
  python sports/scripts/grandchild_league_lc_diagnostic.py --rho 0.5 --gamma 0.5

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_league_L_C_distribution.png
  GRANDCHILD_league_team.csv
  GRANDCHILD_league_lc_meta.json
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs

OUT = GRANDCHILD_ASSIGN
PNG_1D = OUT / "GRANDCHILD_league_L_C_distribution.png"
TEAM_CSV = OUT / "GRANDCHILD_league_team.csv"
META_JSON = OUT / "GRANDCHILD_league_lc_meta.json"

N_LC_BINS = 48
BAR_COLOR = "darkorange"
BAR_ALPHA = 0.85
LC_TICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
DEFAULT_RHO = 0.5
DEFAULT_GAMMA = 0.5
DEFAULT_SEED = 5412015


def _load_gamma_default() -> float:
    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return float(getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0))


def _summary(name: str, values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    return {
        "label": name,
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
        "median": float(np.median(v)),
    }


def _theta_from_panel(panel: pd.DataFrame) -> tuple[float, float, dict]:
    work = panel.dropna(subset=["perf"]).copy()
    ability = work["perf"].to_numpy(dtype=float)
    if "Y_draft" in work.columns:
        n_drafted = int(work["Y_draft"].sum())
    else:
        n_drafted = 0
    n_total = int(len(work))
    k_over_n = n_drafted / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n)) if n_total else float("nan")
    kn_meta = {
        "n_accepted": n_drafted,
        "n_total": n_total,
        "K_over_N": k_over_n,
        "theta_quantile": 1.0 - k_over_n if n_total else float("nan"),
    }
    return theta, k_over_n, kn_meta


def _interval_stats(team_df: pd.DataFrame) -> dict:
    lo = team_df["A_hat_min"].to_numpy(dtype=float)
    hi = team_df["A_hat_max"].to_numpy(dtype=float)
    grid = np.linspace(lo.min(), hi.max(), 400)
    cover = np.zeros(grid.size, dtype=int)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    span = team_df["perf_span"].to_numpy(dtype=float)
    return {
        "coverage_max": int(cover.max()),
        "coverage_frac_gt1": float((cover > 1).mean()),
        "perf_span": _summary("perf_span", span),
    }


def _teams_from_grandchild(
    ability: np.ndarray,
    pool_id: np.ndarray,
    *,
    theta: float,
    gamma: float,
) -> pd.DataFrame:
    import tier1_pool_assignment as tpa

    lc_col = tpa.POOL_L_CROWDING_SMOOTH_TEAM_COL
    players = pd.DataFrame({"ability": ability, "pool_id": pool_id.astype(np.int64)})
    players = tpa.add_team_pool_columns(
        players,
        viability_theta=float(theta),
        viability_sharpness=float(gamma),
    )
    team_df = (
        players.groupby("pool_id", observed=True)
        .agg(
            T_j_hat=("ability", "mean"),
            A_hat_min=("ability", "min"),
            A_hat_max=("ability", "max"),
            L_C=(lc_col, "first"),
            roster_n=("ability", "size"),
        )
        .reset_index()
        .rename(columns={"pool_id": "team_id"})
    )
    team_df["perf_span"] = team_df["A_hat_max"] - team_df["A_hat_min"]
    return team_df


def build_1d_figure(
    lc: np.ndarray,
    *,
    rho: float,
    theta: float,
    gamma: float,
    k_over_n: float,
    n_teams: int,
    interval_meta: dict,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc_edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (lc_edges[:-1] + lc_edges[1:])
    bin_width = lc_edges[1] - lc_edges[0]
    counts, _ = np.histogram(lc, bins=lc_edges)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.bar(
        centers,
        counts,
        width=bin_width * 0.98,
        align="center",
        color=BAR_COLOR,
        alpha=BAR_ALPHA,
        edgecolor=BAR_COLOR,
        linewidth=0.3,
        label=rf"Grandchild sim ($\rho={rho:g}$)",
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(LC_TICKS)
    ax.set_xlabel(r"$L_C$", fontsize=11)
    ax.set_ylabel("Teams", fontsize=10)
    ax.set_title(
        rf"Team $L_C$ on Grandchild rosters ($n={n_teams:,}$ teams)",
        fontsize=11,
        pad=8,
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
    stats = _summary("", lc)
    span = interval_meta.get("perf_span", {})
    ax.text(
        0.97,
        0.97,
        rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=8,
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            alpha=0.85,
            edgecolor="0.8",
        ),
    )
    ax.text(
        0.97,
        0.86,
        rf"span mean={span.get('mean', float('nan')):.2f} z · "
        rf"max coverage={interval_meta.get('coverage_max', 0):,}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=7,
        color="0.35",
    )
    ax.text(
        0.97,
        0.76,
        rf"$\theta$ = {theta:.3f} z-units; $\gamma={gamma:g}$; $K/N={k_over_n:.4f}$",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=7,
        color="0.35",
    )
    fig.suptitle(
        rf"Grandchild ASSIGN — team smooth $L_C$ (2015 PPM z, $C=15$, $\rho={rho:g}$)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG_1D, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG_1D}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Grandchild sim league L_C diagnostic")
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO, help="Grandchild homophily ρ")
    parser.add_argument(
        "--gamma",
        type=float,
        default=None,
        help=f"Viability sharpness γ (default {DEFAULT_GAMMA} to match HAND17 slide 4)",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--season", type=int, default=2015)
    args = parser.parse_args()

    ensure_hero_dirs()
    gamma_default = _load_gamma_default()
    gamma = float(args.gamma) if args.gamma is not None else DEFAULT_GAMMA
    gamma_source = (
        f"CLI --gamma {gamma:g}"
        if args.gamma is not None
        else f"HAND17 slide-4 default ({DEFAULT_GAMMA:g}); tier1 default is {gamma_default:g}"
    )

    gc = importlib.import_module("541_grandchild_homophily_assign")
    from empirical_team_interval_overlap import _prepare_panel

    panel = _prepare_panel()
    season_panel = panel.loc[panel["season"] == int(args.season)].copy()
    season_panel = season_panel.dropna(subset=["perf"])
    season_panel["perf"] = pd.to_numeric(season_panel["perf"], errors="coerce")
    season_panel = season_panel.dropna(subset=["perf"])

    ability, emp_meta = gc.load_empirical_abilities_season(int(args.season))
    c = int(gc.ROSTER_SIZE_DEFAULT)
    if len(ability) % c != 0:
        raise ValueError(f"N={len(ability)} not divisible by C={c}")

    theta, k_over_n, kn_meta = _theta_from_panel(season_panel)
    rng = np.random.default_rng(int(args.seed))
    res = gc.run_one_realization(ability, c, float(args.rho), rng=rng, seed=int(args.seed))
    team_df = _teams_from_grandchild(
        res.ability, res.pool_id, theta=theta, gamma=gamma
    )
    team_df.to_csv(TEAM_CSV, index=False)
    print(f"Wrote {TEAM_CSV}")

    lc = team_df["L_C"].dropna().to_numpy(dtype=float)
    interval_meta = _interval_stats(team_df)
    build_1d_figure(
        lc,
        rho=float(args.rho),
        theta=theta,
        gamma=gamma,
        k_over_n=k_over_n,
        n_teams=int(team_df.shape[0]),
        interval_meta=interval_meta,
    )

    meta = {
        "diagnostic": "grandchild_league_lc",
        "date": date.today().isoformat(),
        "assignment": {
            "method": "grandchild",
            "rho": float(args.rho),
            "seed": int(args.seed),
            "roster_size": c,
            "n_teams": int(team_df.shape[0]),
            "n_players": int(len(ability)),
            "within_team_mse": float(res.within_team_mse),
            "sorting_index_h": float(res.sorting_index_h),
            "centroid_sd": float(res.centroid_sd),
        },
        "ability_source": emp_meta,
        "lc_mode": "crowding_smooth_team",
        "theta_mode": "season_panel_k_over_n_quantile",
        "theta": theta,
        "gamma": gamma,
        "gamma_source": gamma_source,
        "theta_K_over_N": kn_meta,
        "intervals": interval_meta,
        "L_C": _summary("L_C", lc),
        "T_j_hat": _summary(r"\hat{T}_j", team_df["T_j_hat"].to_numpy(dtype=float)),
        "empirical_hand17_reference": {
            "note": "HAND17 slide 4 (empirical MBB 2011-2021, gamma=0.5)",
            "L_C_mean": 0.254,
            "L_C_sd": 0.039,
        },
        "outputs": {
            "png_1d": PNG_1D.name,
            "team_csv": TEAM_CSV.name,
        },
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print(
        f"rho={args.rho:g}  theta={theta:.4f}  gamma={gamma:g}  "
        f"L_C mean={meta['L_C']['mean']:.3f} sd={meta['L_C']['std']:.3f}  "
        f"span mean={interval_meta['perf_span']['mean']:.2f}"
    )
    print("Done.")


if __name__ == "__main__":
    main()
