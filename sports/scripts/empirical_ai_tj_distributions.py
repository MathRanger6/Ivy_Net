#!/usr/bin/env python3
"""PD17 — Empirical MBB: $\\hat{A}_i$ and $\\hat{T}_j$ distributions (side-by-side).

Mirrors sim layout in sim_league_input_distributions.py / CHAR sim-input slide,
but on the locked hero panel (real rosters, not synthetic draws).

Left:  player-season ability $\\hat{A}_i$ (perf, ppm z within season)
Right: team-season realized talent $\\hat{T}_j$ = mean $\\hat{A}_i$ on roster (not $T_{j^*}$)

Run (repo root):
  python sports/scripts/empirical_ai_tj_distributions.py

Outputs (HEROs_and_PASSes/empirical_pd17/):
  EMPIRICAL_Ai_Tj_distributions.png
  EMPIRICAL_Ai_Tj_team_season.csv   — one row per (team_id, season)
  EMPIRICAL_Ai_Tj_meta.json
"""

from __future__ import annotations

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
PNG = OUT / "EMPIRICAL_Ai_Tj_distributions.png"
TEAM_CSV = OUT / "EMPIRICAL_Ai_Tj_team_season.csv"
META_JSON = OUT / "EMPIRICAL_Ai_Tj_meta.json"

N_BINS = 48
BAR_COLOR = "steelblue"
BAR_ALPHA = 0.85


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


def _histogram_edges(*arrays: np.ndarray, n_bins: int = N_BINS) -> np.ndarray:
    """Shared x-axis across panels — robust range on pooled values."""
    pooled = np.concatenate([np.asarray(a, dtype=float) for a in arrays])
    pooled = pooled[np.isfinite(pooled)]
    lo = float(np.quantile(pooled, 0.005))
    hi = float(np.quantile(pooled, 0.995))
    if hi <= lo:
        lo, hi = float(pooled.min()), float(pooled.max())
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    return np.linspace(lo - pad, hi + pad, n_bins + 1)


def build_figure(ability: np.ndarray, team_talent: np.ndarray) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    edges = _histogram_edges(ability, team_talent)
    centers = 0.5 * (edges[:-1] + edges[1:])
    bin_width = edges[1] - edges[0]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharex=True)

    panels = [
        (
            axes[0],
            ability,
            rf"$\hat{{A}}_i$ — player ability ($n={ability.size:,}$)",
            "Player-seasons (hero filters)",
        ),
        (
            axes[1],
            team_talent,
            rf"$\hat{{T}}_j$ — realized team talent ($n={team_talent.size:,}$ team-seasons)",
            r"Mean $\hat{A}_i$ on roster (not $T_{j^*}$)",
        ),
    ]

    for ax, values, title, subtitle in panels:
        counts, _ = np.histogram(values, bins=edges)
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
        ax.set_xlabel(r"PPM $z$ within season", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(title, fontsize=11, pad=8)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.92)
        stats = _summary("", values)
        ax.text(
            0.03,
            0.97,
            rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8,
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="white",
                alpha=0.85,
                edgecolor="0.8",
            ),
        )
        ax.text(
            0.03,
            0.88,
            subtitle,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=7,
            color="0.35",
        )

    fig.suptitle(
        r"Empirical MBB inputs — $\hat{A}_i$ and $\hat{T}_j$ "
        r"(2011–2021, min 20 min, poolq winsor 0.01–0.99)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


def main() -> None:
    ensure_hero_dirs()
    use = _prepare_panel()
    use = use.dropna(subset=["perf", "team_id", "season"]).copy()

    ability = use["perf"].to_numpy(dtype=float)
    team_df = (
        use.groupby(["team_id", "season"], observed=True)
        .agg(
            T_j_hat=("perf", "mean"),
            roster_n=("perf", "size"),
            draftees=("Y_draft", "sum"),
        )
        .reset_index()
    )
    team_talent = team_df["T_j_hat"].to_numpy(dtype=float)

    team_df.to_csv(TEAM_CSV, index=False)
    print(f"Wrote {TEAM_CSV}")

    build_figure(ability, team_talent)

    n_drafted = int(use["Y_draft"].sum())
    k_over_n = n_drafted / len(use) if len(use) else float("nan")

    meta = {
        "diagnostic": "empirical_ai_tj_distributions",
        "date": date.today().isoformat(),
        "source": "MBB player-season panel (530 pipeline / hero filters)",
        "seasons": "2011-2021",
        "perf": "PPM z within season",
        "outputs": {
            "png": PNG.name,
            "team_csv": TEAM_CSV.name,
        },
        "theta_K_over_N": {
            "description": "PD17: accepted / total in filtered panel",
            "n_accepted": n_drafted,
            "n_total": int(len(use)),
            "K_over_N": k_over_n,
        },
        "A_i_hat": _summary(r"\hat{A}_i", ability),
        "T_j_hat": _summary(r"\hat{T}_j", team_talent),
        "n_team_seasons": int(team_df.shape[0]),
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print(
        f"K/N (theta proxy): {k_over_n:.5f} "
        f"({n_drafted:,} drafted / {len(use):,} player-seasons)"
    )
    print("Done.")


if __name__ == "__main__":
    main()
