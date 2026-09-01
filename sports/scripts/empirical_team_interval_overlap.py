#!/usr/bin/env python3
"""PD17 — Empirical MBB: team \\hat{A}_i interval overlap (530 CELL 8 port).

For each team-season, [min, max] of player PPM z on the roster defines a talent
window. Coverage counts how many windows cover each point on the perf axis.

Run (repo root):
  python sports/scripts/empirical_team_interval_overlap.py
  python sports/scripts/empirical_team_interval_overlap.py --season-min 2015 --season-max 2019

Outputs (HEROs_and_PASSes/empirical_pd17/):
  Full panel: EMPIRICAL_team_interval_overlap.{png,meta.json,...}
  Window:     EMPIRICAL_team_interval_overlap_2015_2019.{png,meta.json,...}
"""

from __future__ import annotations

import argparse
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

from hero_gallery_paths import ensure_hero_dirs
from interval_overlap_paths import empirical_overlap_paths

TEAM_MIN_PLAYERS = 2
N_INTERVAL_SAMPLE = 80
COVERAGE_GRID_POINTS = 400
SPAN_BINS = 40
BAR_COLOR = "steelblue"


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
        "median": float(np.median(v)),
    }


def _team_intervals(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work = work.dropna(subset=["perf", "team_id", "season"])

    iv = (
        work.groupby(["team_id", "season"], observed=True)["perf"]
        .agg(
            A_hat_min="min",
            A_hat_max="max",
            T_j_hat="mean",
            roster_n="count",
        )
        .reset_index()
    )
    iv = iv.loc[iv["roster_n"] >= TEAM_MIN_PLAYERS].copy()
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]
    return iv, work


def _coverage_curve(lo: np.ndarray, hi: np.ndarray, grid: np.ndarray) -> np.ndarray:
    cover = np.zeros(grid.size, dtype=int)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    return cover


def _disjoint_benchmark(work: pd.DataFrame, n_slices: int, grid: np.ndarray) -> np.ndarray:
    perf_sorted = np.sort(work["perf"].to_numpy(dtype=float))
    cuts = np.array_split(perf_sorted, n_slices)
    disjoint_lo = np.array([c.min() for c in cuts if len(c)])
    disjoint_hi = np.array([c.max() for c in cuts if len(c)])
    return _coverage_curve(disjoint_lo, disjoint_hi, grid)


def _coverage_stats(cover: np.ndarray, n_units: int) -> dict:
    cov_max = int(cover.max())
    return {
        "coverage_max": cov_max,
        "coverage_max_normalized": float(cov_max / n_units) if n_units else None,
        "coverage_mean": float(cover.mean()),
        "coverage_frac_gt_1": float((cover > 1).mean()),
    }


def build_figure(
    iv: pd.DataFrame,
    work: pd.DataFrame,
    *,
    png_path: Path,
    seasons: str,
    h_sort: float | None = None,
    suptitle: str | None = None,
    xlab: str | None = None,
) -> dict:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    grid = np.linspace(iv["A_hat_min"].min(), iv["A_hat_max"].max(), COVERAGE_GRID_POINTS)
    lo = iv["A_hat_min"].to_numpy(dtype=float)
    hi = iv["A_hat_max"].to_numpy(dtype=float)
    cover = _coverage_curve(lo, hi, grid)
    cover_disjoint = _disjoint_benchmark(work, len(iv), grid)
    cov_stats = _coverage_stats(cover, len(iv))

    iv_plot = iv.sort_values("T_j_hat").reset_index(drop=True)
    step = max(1, len(iv_plot) // N_INTERVAL_SAMPLE)
    sample = iv_plot.iloc[::step].head(N_INTERVAL_SAMPLE).copy()

    xlab = xlab or r"Player $\hat{A}_i$ (PPM $z$ within season)"
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ax.fill_between(grid, cover, step="mid", alpha=0.35, color=BAR_COLOR, label="Actual rosters")
    ax.plot(
        grid,
        cover_disjoint,
        color="crimson",
        lw=1.5,
        ls="--",
        label="Disjoint sort-and-chop (equal-$n$ slices)",
    )
    ax.axhline(1, color="gray", ls=":", lw=1, label="No overlap (coverage = 1)")
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel("Team-seasons covering this level", fontsize=10)
    ax.set_title("Interval overlap along talent spectrum", fontsize=11, pad=8)
    ax.text(
        0.02,
        0.98,
        rf"max coverage = {cov_stats['coverage_max']:,}  |  "
        rf"{cov_stats['coverage_frac_gt_1']:.1%} of grid with $>$1 team",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    ax.legend(fontsize=7, loc="lower right")

    ax = axes[0, 1]
    ax.hist(iv["perf_span"], bins=SPAN_BINS, color=BAR_COLOR, edgecolor="white", alpha=0.85)
    ax.set_xlabel(r"Roster span ($\max \hat{A}_i - \min \hat{A}_i$)", fontsize=10)
    ax.set_ylabel("Team-seasons", fontsize=10)
    ax.set_title("Width of each team's talent window", fontsize=11, pad=8)
    span_stats = _summary("perf_span", iv["perf_span"].to_numpy(dtype=float))
    ax.text(
        0.98,
        0.98,
        rf"mean={span_stats['mean']:.2f}, median={span_stats['median']:.2f}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )

    ax = axes[1, 0]
    y0 = np.arange(len(sample))
    ax.hlines(y0, sample["A_hat_min"], sample["A_hat_max"], colors=BAR_COLOR, lw=2, alpha=0.85)
    ax.scatter(sample["T_j_hat"], y0, color="crimson", s=28, zorder=3, label=r"$\hat{T}_j$")
    ax.set_yticks(y0[:: max(1, len(y0) // 8)])
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel(f"Sample of {len(sample)} team-seasons (sorted by $\\hat{{T}}_j$)", fontsize=9)
    ax.set_title(r"Roster $[\min, \max]$ intervals (sample)", fontsize=11, pad=8)
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[1, 1]
    y_all = np.arange(len(iv_plot))
    ax.hlines(
        y_all,
        iv_plot["A_hat_min"],
        iv_plot["A_hat_max"],
        colors=BAR_COLOR,
        alpha=0.15,
        linewidth=0.6,
    )
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel("All team-seasons (sorted by $\\hat{T}_j$)", fontsize=9)
    ax.set_title(
        f"All {len(iv_plot):,} intervals (faint) — overlap = vertical stacking",
        fontsize=11,
        pad=8,
    )

    default_title = (
        rf"Empirical NCAA — team talent window overlap (MBB {seasons})"
        + (
            rf"\nRealized sorting $H_{{sort}}={h_sort:.3f}$ on this partition"
            if h_sort is not None and np.isfinite(h_sort)
            else ""
        )
    )
    fig.suptitle(suptitle or default_title, fontsize=12, y=0.98)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.08, hspace=0.38, wspace=0.28)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png_path}")

    return {
        **cov_stats,
        "coverage_disjoint_max": int(cover_disjoint.max()),
        "coverage_disjoint_mean": float(cover_disjoint.mean()),
        "n_team_seasons": int(len(iv)),
        "n_player_seasons": int(len(work)),
        "H_sort": float(h_sort) if h_sort is not None else None,
        "perf_span": span_stats,
        "T_j_hat": _summary(r"\hat{T}_j", iv["T_j_hat"].to_numpy(dtype=float)),
    }


def _compute_H_sort(work: pd.DataFrame) -> float:
    sys.path.insert(0, str(SPORTS))
    import importlib

    gc = importlib.import_module("541_grandchild_homophily_assign")
    use = work.dropna(subset=["perf"]).copy()
    use["pool_id"] = use.groupby(["team_id", "season"], observed=True).ngroup()
    return float(
        gc.realized_sorting_index_H_sort(
            use["perf"].to_numpy(dtype=float),
            use["pool_id"].to_numpy(dtype=np.int64),
        )
    )


def run_diagnostic(*, season_min: int | None = None, season_max: int | None = None) -> dict:
    paths = empirical_overlap_paths(season_min=season_min, season_max=season_max)
    panel = _prepare_panel()
    if season_min is not None and season_max is not None:
        panel = panel.loc[
            (panel["season"] >= season_min) & (panel["season"] <= season_max)
        ].copy()

    iv, work = _team_intervals(panel)
    paths["csv"].parent.mkdir(parents=True, exist_ok=True)
    iv.to_csv(paths["csv"], index=False)
    print(f"Wrote {paths['csv']}")

    h_sort = _compute_H_sort(work)
    stats = build_figure(
        iv,
        work,
        png_path=paths["png"],
        seasons=paths["seasons"],
        h_sort=h_sort,
    )

    meta = {
        "diagnostic": "empirical_team_interval_overlap",
        "date": date.today().isoformat(),
        "source": "MBB player-season panel (530 pipeline / hero filters)",
        "seasons": paths["seasons"],
        "season_min": season_min,
        "season_max": season_max,
        "compare_window": season_min is not None,
        "perf": "PPM z within season",
        "team_min_players": TEAM_MIN_PLAYERS,
        "coverage_grid_points": COVERAGE_GRID_POINTS,
        "n_interval_sample": N_INTERVAL_SAMPLE,
        "530_analog": "530_sports_pipeline.ipynb CELL 8",
        **stats,
        "outputs": {
            "png": paths["png"].name,
            "team_csv": paths["csv"].name,
        },
    }
    paths["meta"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {paths['meta']}")
    print(
        f"Seasons {paths['seasons']}  |  team-seasons: {stats['n_team_seasons']:,}  |  "
        f"max coverage: {stats['coverage_max']:,}  |  "
        f"norm: {stats.get('coverage_max_normalized', 0):.3f}  |  "
        f"H_sort: {h_sort:.3f}"
    )
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    args = parser.parse_args()

    if (args.season_min is None) ^ (args.season_max is None):
        parser.error("--season-min and --season-max must be supplied together")

    ensure_hero_dirs()
    run_diagnostic(season_min=args.season_min, season_max=args.season_max)
    print("Done.")


if __name__ == "__main__":
    main()
