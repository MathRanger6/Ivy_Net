#!/usr/bin/env python3
"""PD17 — Empirical MBB: team $L_C$ distribution and $\\hat{T}_j$ vs $L_C$ (Sketch A).

Team smooth congestion on real rosters:
  $L_C = mean_j \\sigma(\\gamma(\\hat{A}_j - \\theta))$ over each roster.

$\\theta$ = empirical $\\hat{A}_i$ quantile at $1 - K/N$ (draft rate in panel).
$\\gamma$ = 539 placeholder (10) until PD17 $\\gamma$/$\\lambda$ calibration.

Run (repo root):
  python sports/scripts/empirical_lc_distributions.py
  python sports/scripts/empirical_lc_distributions.py --gamma 3

Outputs (HEROs_and_PASSes/empirical_pd17/):
  EMPIRICAL_L_C_distribution.png       — 1D team-season $L_C$ histogram (slide 2)
  EMPIRICAL_L_C_vs_Tj_2d.png           — 2D heatmap $\\hat{T}_j$ vs $L_C$ (slide 3)
  EMPIRICAL_L_C_team_season.csv
  EMPIRICAL_L_C_meta.json
"""

from __future__ import annotations

import argparse
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
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import EMPIRICAL_PD17, ensure_hero_dirs

OUT = EMPIRICAL_PD17
PNG_1D = OUT / "EMPIRICAL_L_C_distribution.png"
PNG_2D = OUT / "EMPIRICAL_L_C_vs_Tj_2d.png"
TEAM_CSV = OUT / "EMPIRICAL_L_C_team_season.csv"
META_JSON = OUT / "EMPIRICAL_L_C_meta.json"

N_LC_BINS = 48
N_2D_LC_BINS = 20
N_2D_TJ_BINS = 20
BAR_COLOR = "steelblue"
BAR_ALPHA = 0.85
LC_TICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]


def _hero_pipeline_config():
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=20,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=2011,
        panel_season_max=2021,
        analysis_season_min=2011,
        analysis_season_max=2021,
    )


def _prepare_panel() -> pd.DataFrame:
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _hero_pipeline_config()
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    return panel_build.filter_panel(panel, cfg)


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
    }


def _attach_team_lc(panel: pd.DataFrame, *, theta: float, gamma: float) -> pd.DataFrame:
    sys.path.insert(0, str(SPORTS))
    import tier1_pool_assignment as tpa

    lc_col = tpa.POOL_L_CROWDING_SMOOTH_TEAM_COL
    use = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    use["pool_id"] = use.groupby(["team_id", "season"], observed=True).ngroup()
    players = use.rename(columns={"perf": "ability"})
    players = tpa.add_team_pool_columns(
        players,
        viability_theta=float(theta),
        viability_sharpness=float(gamma),
    )

    team_df = (
        players.groupby(["team_id", "season"], observed=True)
        .agg(
            T_j_hat=("ability", "mean"),
            L_C=(lc_col, "first"),
            roster_n=("ability", "size"),
            draftees=("Y_draft", "sum"),
        )
        .reset_index()
    )
    return team_df


def _tj_bin_edges(values: np.ndarray, *, n_bins: int) -> np.ndarray:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    lo = float(np.quantile(v, 0.005))
    hi = float(np.quantile(v, 0.995))
    if hi <= lo:
        lo, hi = float(v.min()), float(v.max())
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    return np.linspace(lo - pad, hi + pad, n_bins + 1)


def build_1d_figure(lc: np.ndarray, *, theta: float, gamma: float, k_over_n: float) -> None:
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
        label="Empirical MBB",
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(LC_TICKS)
    ax.set_xlabel(r"$L_C$", fontsize=11)
    ax.set_ylabel("Team-seasons", fontsize=10)
    ax.set_title(
        rf"Team $L_C$ on real rosters ($n={lc.size:,}$ team-seasons)",
        fontsize=11,
        pad=8,
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
    stats = _summary("", lc)
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
        0.88,
        rf"$\theta$ = $F^{{-1}}_{{\hat{{A}}}}(1-K/N)$ = {theta:.3f} z-units; "
        rf"$\gamma={gamma:g}$ (539 placeholder); $K/N={k_over_n:.4f}$",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=7,
        color="0.35",
    )
    fig.suptitle(
        r"Empirical MBB — team smooth $L_C$ "
        r"(2011–2021, min 20 min, poolq winsor 0.01–0.99)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG_1D, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG_1D}")


def build_2d_figure(team_df: pd.DataFrame, *, theta: float, gamma: float) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc = team_df["L_C"].to_numpy(dtype=float)
    tj = team_df["T_j_hat"].to_numpy(dtype=float)
    mask = np.isfinite(lc) & np.isfinite(tj)

    lc_edges = np.linspace(0.0, 1.0, N_2D_LC_BINS + 1)
    tj_edges = _tj_bin_edges(tj[mask], n_bins=N_2D_TJ_BINS)

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    h, _, _, im = ax.hist2d(
        lc[mask],
        tj[mask],
        bins=[lc_edges, tj_edges],
        cmap="viridis",
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(LC_TICKS)
    ax.set_xlabel(r"$L_C$", fontsize=11)
    ax.set_ylabel(r"$\hat{T}_j$ (PPM $z$ within season)", fontsize=10)
    ax.set_title(
        r"Do stronger rosters face more congestion? (team-season counts)",
        fontsize=11,
        pad=8,
    )
    fig.colorbar(im, ax=ax, label="Teams in bin", shrink=0.88)
    fig.suptitle(
        rf"Empirical Sketch A — $\hat{{T}}_j$ vs $L_C$ "
        rf"($\theta={theta:.3f}$ z-units, $\gamma={gamma:g}$)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG_2D, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG_2D}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PD17 empirical team L_C figures")
    parser.add_argument(
        "--gamma",
        type=float,
        default=None,
        metavar="G",
        help=(
            "Override viability sharpness γ in σ(γ(Â−θ)). "
            "Default: SELECTION_539_VIABILITY_SHARPNESS from tier1_sim_config.py (10)."
        ),
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    gamma_default = _load_gamma_default()
    gamma = float(args.gamma) if args.gamma is not None else gamma_default
    gamma_source = (
        f"CLI --gamma {gamma:g}"
        if args.gamma is not None
        else f"tier1_sim_config SELECTION_539_VIABILITY_SHARPNESS ({gamma_default:g})"
    )

    panel = _prepare_panel()
    panel = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    ability = panel["perf"].to_numpy(dtype=float)
    n_drafted = int(panel["Y_draft"].sum())
    n_total = int(len(panel))
    k_over_n = n_drafted / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n))

    team_df = _attach_team_lc(panel, theta=theta, gamma=gamma)
    team_df.to_csv(TEAM_CSV, index=False)
    print(f"Wrote {TEAM_CSV}")

    lc = team_df["L_C"].dropna().to_numpy(dtype=float)
    build_1d_figure(lc, theta=theta, gamma=gamma, k_over_n=k_over_n)
    build_2d_figure(team_df, theta=theta, gamma=gamma)

    meta = {
        "diagnostic": "empirical_lc_distributions",
        "date": date.today().isoformat(),
        "source": "MBB player-season panel (530 pipeline / hero filters)",
        "seasons": "2011-2021",
        "perf": "PPM z within season",
        "lc_mode": "crowding_smooth_team",
        "theta_mode": "empirical_k_over_n_quantile",
        "theta": theta,
        "gamma": gamma,
        "gamma_source": gamma_source,
        "gamma_note": "539 placeholder until PD17 gamma/lambda calibration",
        "theta_K_over_N": {
            "description": "PD17: accepted / total in filtered panel",
            "n_accepted": n_drafted,
            "n_total": n_total,
            "K_over_N": k_over_n,
            "theta_quantile": 1.0 - k_over_n,
        },
        "L_C": _summary("L_C", lc),
        "T_j_hat": _summary(r"\hat{T}_j", team_df["T_j_hat"].to_numpy(dtype=float)),
        "n_team_seasons": int(team_df.shape[0]),
        "lc_bins_1d": N_LC_BINS,
        "outputs": {
            "png_1d": PNG_1D.name,
            "png_2d": PNG_2D.name,
            "team_csv": TEAM_CSV.name,
        },
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print(f"gamma: {gamma:g} ({gamma_source})")
    print(f"theta (F_A_hat^-1(1-K/N)): {theta:.4f} z-units  K/N: {k_over_n:.5f}")
    print("Done.")


if __name__ == "__main__":
    main()
