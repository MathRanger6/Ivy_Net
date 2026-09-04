#!/usr/bin/env python3
"""Disposable probe — career cumulative PPM + Option A z + last-PS HERO.

Does not touch canonical pass_a/ or sports_sandbox/hero/ outputs.

Spec (reigning lock):
  2009–2021 · last-ps · ever-Y · mg10 · min20 · poolq_loo · quantile bins

Option A: z-score career PPM using mean/std from last-PS cross-section, applied
to all rows before LOO; LOO on full panel; plot last-PS only.

Run (repo root):
  export PYTHONPATH="sports"
  python3 sports/scripts/pass_a_cum_ppm_hero_probe.py
  python3 sports/scripts/pass_a_cum_ppm_hero_probe.py --n-bins 8 10 16
"""

from __future__ import annotations

import argparse
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
sys.path.insert(0, str(SPORTS))

OUT_DIR = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "sports_sandbox"
    / "_DISPOSABLE_cum_ppm_last_ps"
)

SEASON_MIN = 2009
SEASON_MAX = 2021
MIN_MINUTES = 20.0
MIN_TEAM_SEASON_GAMES = 10
WINSOR = (0.01, 0.99)
DEFAULT_BINS = (8, 10, 16)


def _prepare_panel() -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.y_draft_mode import restrict_to_last_season_rows

    cfg = PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=False,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=WINSOR,
        min_minutes=float(MIN_MINUTES),
        min_team_season_games=int(MIN_TEAM_SEASON_GAMES),
        drop_dash_placeholder_names=True,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=int(SEASON_MIN),
        panel_season_max=int(SEASON_MAX),
        analysis_season_min=int(SEASON_MIN),
        analysis_season_max=int(SEASON_MAX),
    )
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_career_cum_ppm_loo_option_a(panel, poolq_winsor_quantiles=WINSOR)
    use = panel_build.filter_panel(panel, cfg)
    use, audit = restrict_to_last_season_rows(use)
    print(
        f"Career cum PPM · last-ps panel: {audit['n_rows_before']:,} → "
        f"{audit['n_rows_after']:,} rows · {audit['n_athletes']:,} athletes",
        flush=True,
    )
    return use


def _roster_table(df: pd.DataFrame, n_bins: int) -> pd.DataFrame:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = df.dropna(subset=["poolq_loo", "Y_draft"]).copy()
    work["vent"] = assign_poolq_bin_labels(work["poolq_loo"], n_bins, "quantile")
    return (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            poolq_mean=("poolq_loo", "mean"),
        )
        .reset_index()
        .sort_values("vent")
    )


def _quadratic_beta2(df: pd.DataFrame) -> float:
    work = df.dropna(subset=["poolq_loo", "Y_draft"]).copy()
    x = pd.to_numeric(work["poolq_loo"], errors="coerce").to_numpy(dtype=float)
    y = pd.to_numeric(work["Y_draft"], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 10:
        return float("nan")
    x = x[mask]
    y = y[mask]
    x_mat = np.column_stack([np.ones(len(x)), x, x**2])
    beta, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
    return float(beta[2])


def _plot_hero(roster: pd.DataFrame, *, n_bins: int, n_rows: int, beta2: float) -> Path:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Quantile bin ($1$ = lowest poolq$_{\mathrm{LOO}}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        rf"HERO probe — career cum PPM (Option A z) · last-PS · MBB {SEASON_MIN}–{SEASON_MAX}\n"
        rf"Q{n_bins} quantile · mg{MIN_TEAM_SEASON_GAMES} · min {MIN_MINUTES:g} min · N={n_rows:,}",
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    if np.isfinite(beta2):
        sign = "<0, concave" if beta2 < 0 else "not concave"
        ax.text(
            0.02,
            0.96,
            rf"LPM $\beta_2={beta2:+.4g}$ ({sign})",
            transform=ax.transAxes,
            fontsize=8,
            va="top",
        )
    footer = (
        f"DISPOSABLE cum PPM probe · {date.today().isoformat()} · "
        f"career PPM LOO · z ref = last-PS cross-section"
    )
    fig.text(0.01, 0.01, footer, fontsize=7, color="0.45")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    png = OUT_DIR / f"HERO_q{n_bins}_cum_ppm_z_lastps_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def main() -> None:
    parser = argparse.ArgumentParser(description="Career cum PPM HERO probe (disposable)")
    parser.add_argument(
        "--n-bins",
        type=int,
        nargs="+",
        default=list(DEFAULT_BINS),
        help="Quantile bin counts (default: 8 10 16)",
    )
    args = parser.parse_args()

    panel = _prepare_panel()
    n_rows = len(panel)
    n_drafts = int(pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).sum())
    print(f"Resolved panel: N={n_rows:,} · drafts={n_drafts:,}", flush=True)

    for n_bins in args.n_bins:
        roster = _roster_table(panel, int(n_bins))
        beta2 = _quadratic_beta2(panel)
        png = _plot_hero(roster, n_bins=int(n_bins), n_rows=n_rows, beta2=beta2)
        print(f"Wrote {png.relative_to(REPO)} · bins={len(roster)} · β₂={beta2:+.5f}")


if __name__ == "__main__":
    main()
