#!/usr/bin/env python3
"""Disposable probe — weighted cumulative PER + Option A z + last-PS HERO.

PER_cum at college year k = 1×PER_1 + 2×PER_2 + … + k×PER_k (running sum).

Does not touch canonical pass_a/ or sports_sandbox/hero/ outputs.

Run (repo root):
  export PYTHONPATH="sports"
  python3 sports/scripts/pass_a_cum_per_hero_probe.py --n-bins 8 10 16
  python3 sports/scripts/pass_a_cum_per_hero_probe.py --normalized --n-bins 8 10 16
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

OUT_DIR_RAW = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "sports_sandbox"
    / "_DISPOSABLE_cum_per_weighted_last_ps"
)
OUT_DIR_NORM = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "sports_sandbox"
    / "_DISPOSABLE_cum_per_weighted_norm_last_ps"
)

SEASON_MIN = 2009
SEASON_MAX = 2021
MIN_MINUTES = 20.0
MIN_TEAM_SEASON_GAMES = 10
WINSOR = (0.01, 0.99)
DEFAULT_BINS = (8, 10, 16)


def _prepare_panel(*, normalized: bool) -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.y_draft_mode import restrict_to_last_season_rows

    cfg = PipelineConfig(
        perf_metric=["per"],
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
    n_per = pd.to_numeric(panel.get("PER"), errors="coerce").notna().sum()
    print(f"Panel rows with PER: {n_per:,} / {len(panel):,}", flush=True)
    panel = panel_build.apply_career_weighted_per_loo_option_a(
        panel,
        poolq_winsor_quantiles=WINSOR,
        normalized=normalized,
    )
    use = panel_build.filter_panel(panel, cfg)
    use, audit = restrict_to_last_season_rows(use)
    n_cum = pd.to_numeric(use.get("perf_cum"), errors="coerce").notna().sum()
    label = "norm weighted PER" if normalized else "weighted PER cum"
    print(
        f"{label} · last-ps: {audit['n_rows_before']:,} → "
        f"{audit['n_rows_after']:,} rows · {audit['n_athletes']:,} athletes · "
        f"with perf_cum={n_cum:,}",
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


def _plot_hero(
    roster: pd.DataFrame,
    *,
    n_bins: int,
    n_rows: int,
    beta2: float,
    out_dir: Path,
    normalized: bool,
) -> Path:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="#7E57C2", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Quantile bin ($1$ = lowest poolq$_{\mathrm{LOO}}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    if normalized:
        title_metric = (
            r"PER$_{\mathrm{cum}}=\frac{\sum_i i\cdot\mathrm{PER}_i}{\sum_i i}$ (norm)"
        )
        slug = "cum_per_wt_norm"
        footer_tag = "weighted PER norm"
    else:
        title_metric = r"PER$_{\mathrm{cum}}=\sum_i i\cdot\mathrm{PER}_i$"
        slug = "cum_per_wt"
        footer_tag = "weighted PER cum"
    ax.set_title(
        rf"HERO probe — {title_metric} · Option A z · last-PS · MBB {SEASON_MIN}–{SEASON_MAX}\n"
        rf"Q{n_bins} · mg{MIN_TEAM_SEASON_GAMES} · N={n_rows:,}",
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
        f"DISPOSABLE {footer_tag} probe · {date.today().isoformat()} · "
        f"z ref = last-PS cross-section"
    )
    fig.text(0.01, 0.01, footer, fontsize=7, color="0.45")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    png = out_dir / f"HERO_q{n_bins}_{slug}_z_lastps_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def main() -> None:
    parser = argparse.ArgumentParser(description="Weighted cum PER HERO probe (disposable)")
    parser.add_argument(
        "--normalized",
        action="store_true",
        help="Divide by sum of weights 1..k (weighted average PER)",
    )
    parser.add_argument(
        "--n-bins",
        type=int,
        nargs="+",
        default=list(DEFAULT_BINS),
        help="Quantile bin counts (default: 8 10 16)",
    )
    args = parser.parse_args()

    out_dir = OUT_DIR_NORM if args.normalized else OUT_DIR_RAW
    panel = _prepare_panel(normalized=args.normalized)
    n_rows = len(panel.dropna(subset=["poolq_loo"]))
    plot_panel = panel.dropna(subset=["poolq_loo", "Y_draft"]).copy()
    n_drafts = int(pd.to_numeric(plot_panel["Y_draft"], errors="coerce").fillna(0).sum())
    print(f"HERO panel (poolq_loo): N={n_rows:,} · drafts={n_drafts:,}", flush=True)

    for n_bins in args.n_bins:
        roster = _roster_table(plot_panel, int(n_bins))
        beta2 = _quadratic_beta2(plot_panel)
        png = _plot_hero(
            roster,
            n_bins=int(n_bins),
            n_rows=n_rows,
            beta2=beta2,
            out_dir=out_dir,
            normalized=args.normalized,
        )
        print(f"Wrote {png.relative_to(REPO)} · bins={len(roster)} · β₂={beta2:+.5f}")


if __name__ == "__main__":
    main()
