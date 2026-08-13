#!/usr/bin/env python3
"""Hero estimand sensitivity — min_minutes ladder (empirical poolq_loo ventiles).

Rebuilds panel from box for each floor, bins draft rate on poolq_loo (16 quantile),
compares shape vs hero lock (min=20).

Run (repo root):
  python sports/scripts/hero_min_minutes_sensitivity_ladder.py
  python sports/scripts/hero_min_minutes_sensitivity_ladder.py --minutes 10
  python sports/scripts/hero_min_minutes_sensitivity_ladder.py --minutes 0 10 20

Outputs (HEROs_and_PASSes/grandchild_assign/):
  HERO_min_minutes_sensitivity_compare_2011_2021.png
  HERO_inverted_u_min{M}_2011_2021.png          — one per floor M
  HERO_min_minutes_sensitivity_2011_2021_meta.json
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
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from gallery_knobs import HERO_BINS
from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label

OUT = GRANDCHILD_ASSIGN
SEASON_MIN = 2011
SEASON_MAX = 2021
DEFAULT_MINUTES = (10, 20)
HERO_LOCK = 20
COLORS = {10: "teal", 20: "steelblue", 0: "gray"}


def _pipeline_config(min_minutes: float) -> object:
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=HERO_BINS,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=float(min_minutes),
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=SEASON_MIN,
        panel_season_max=SEASON_MAX,
        analysis_season_min=SEASON_MIN,
        analysis_season_max=SEASON_MAX,
    )


def _prepare_panel(min_minutes: float) -> tuple[object, pd.DataFrame]:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _pipeline_config(min_minutes)
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    use = panel_build.filter_panel(panel, cfg)
    return cfg, use


def _roster_summary(use: pd.DataFrame) -> dict:
    roster = (
        use.dropna(subset=["perf", "team_id", "season"])
        .groupby(["team_id", "season"], observed=True)
        .agg(roster_n=("perf", "size"))
        .reset_index()
    )
    sizes = roster["roster_n"].to_numpy(dtype=int)
    return {
        "n_team_seasons": int(sizes.size),
        "mean_roster_n": float(sizes.mean()),
        "median_roster_n": float(np.median(sizes)),
        "std_roster_n": float(sizes.std()),
        "min_roster_n": int(sizes.min()),
        "max_roster_n": int(sizes.max()),
    }


def _curvature(roster: pd.DataFrame) -> dict:
    y = roster["draft_rate"].to_numpy(dtype=float)
    if len(y) < 3:
        return {"shape": "insufficient_bins", "peak_bin": None}
    peak_idx = int(np.argmax(y))
    peak = float(y[peak_idx])
    left = float(y[0])
    right = float(y[-1])
    if 0 < peak_idx < len(y) - 1 and peak > left and peak > right:
        shape = "inverted_u_like"
    elif peak_idx == len(y) - 1:
        shape = "monotone_increasing"
    elif peak_idx == 0:
        shape = "monotone_decreasing"
    else:
        shape = "other"
    return {
        "shape": shape,
        "peak_bin": peak_idx,
        "peak_rate": peak,
        "left_rate": left,
        "right_rate": right,
        "bin16_rate": float(y[-1]),
        "bin15_rate": float(y[-2]) if len(y) >= 2 else None,
    }


def _lpm_coef(use: pd.DataFrame) -> dict:
    from sports_pipeline import panel_build

    coef = panel_build.draft_poolq_quadratic_coeffs(use)
    return {
        "beta_poolq_loo": float(coef.get("poolq_loo", np.nan)),
        "beta_poolq_sq": float(coef.get("poolq_sq", np.nan)),
        "concave": bool(coef.get("poolq_sq", 0) < 0),
    }


def _run_floor(min_minutes: float) -> dict:
    from sports_pipeline import panel_build

    cfg, use = _prepare_panel(min_minutes)
    roster = panel_build.ventile_table(use, cfg)
    m = int(min_minutes) if float(min_minutes).is_integer() else min_minutes
    csv_path = OUT / f"HERO_binned_draft_rate_min{m}_{SEASON_MIN}_{SEASON_MAX}.csv"
    roster.to_csv(csv_path, index=False)

    n_players = int(len(use))
    n_drafted = int(use["Y_draft"].sum()) if "Y_draft" in use.columns else 0

    return {
        "min_minutes": float(min_minutes),
        "n_player_seasons": n_players,
        "n_drafted": n_drafted,
        "draft_rate_panel": n_drafted / n_players if n_players else float("nan"),
        "roster_summary": _roster_summary(use),
        "ventiles": roster.to_dict(orient="records"),
        "curvature": _curvature(roster),
        "lpm": _lpm_coef(use),
        "csv": csv_path.name,
        "roster_df": roster,
    }


def _plot_single(result: dict) -> Path:
    configure_matplotlib_mathtext()
    mm = result["min_minutes"]
    m_tag = int(mm) if float(mm).is_integer() else mm
    roster = result["roster_df"]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float) * 100.0
    color = COLORS.get(int(mm) if float(mm).is_integer() else -1, "steelblue")
    ax.bar(x, y, color=color, edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Ventile bin ($1$ = lowest poolq_loo)")
    ax.set_ylabel(r"Mean draft rate (\%)")
    curv = result["curvature"]
    ax.set_title(
        rf"Empirical hero — min minutes = {mm:g}  "
        rf"($n={result['n_player_seasons']:,}$, shape={curv['shape']})",
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.text(
        0.97,
        0.97,
        rf"bin 16 = {curv['bin16_rate'] * 100:.2f}\%",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    fig.tight_layout()
    png = OUT / f"HERO_inverted_u_min{m_tag}_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def _plot_compare(results: list[dict]) -> Path:
    configure_matplotlib_mathtext()
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(5.5 * n, 4.5), sharey=True, squeeze=False)
    axes = axes[0]

    ymax = 0.0
    for res, ax in zip(results, axes):
        mm = res["min_minutes"]
        m_int = int(mm) if float(mm).is_integer() else None
        roster = res["roster_df"]
        x = roster["vent"].to_numpy(dtype=float) + 1
        y = roster["draft_rate"].to_numpy(dtype=float) * 100.0
        ymax = max(ymax, float(y.max()) if len(y) else ymax)
        color = COLORS.get(m_int if m_int is not None else -1, "steelblue")
        ax.bar(x, y, color=color, edgecolor="white", alpha=0.9)
        curv = res["curvature"]
        ax.set_xlabel(r"poolq_loo ventile")
        ax.set_title(
            rf"min = {mm:g} min ($n={res['n_player_seasons']:,}$) — "
            rf"{curv['shape']}; bin16={curv['bin16_rate'] * 100:.2f}\%",
            fontsize=9,
        )
        ax.set_xticks(x)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    axes[0].set_ylabel(r"Mean draft rate (\%)")
    for ax in axes:
        ax.set_ylim(0, ymax * 1.12 if ymax > 0 else 3.0)

    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    fig.suptitle(
        rf"Hero sensitivity — min_minutes ladder (MBB {seasons}, 16 quantile, ppm z, winsor 0.01–0.99)",
        fontsize=11,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    png = OUT / f"HERO_min_minutes_sensitivity_compare_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def _plot_overlay(results: list[dict]) -> Path:
    configure_matplotlib_mathtext()
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    for res in results:
        mm = res["min_minutes"]
        m_int = int(mm) if float(mm).is_integer() else None
        roster = res["roster_df"]
        x = roster["vent"].to_numpy(dtype=float) + 1
        y = roster["draft_rate"].to_numpy(dtype=float) * 100.0
        color = COLORS.get(m_int if m_int is not None else -1, "steelblue")
        ax.plot(
            x,
            y,
            "o-",
            color=color,
            lw=2,
            ms=6,
            label=rf"min={mm:g} ($n={res['n_player_seasons']:,}$, {res['curvature']['shape']})",
        )
    ax.set_xlabel(r"poolq_loo ventile bin")
    ax.set_ylabel(r"Mean draft rate (\%)")
    ax.set_title(rf"Hero LOO ventiles — min_minutes overlay (MBB {seasons_label(SEASON_MIN, SEASON_MAX)})")
    ax.set_xticks(range(1, HERO_BINS + 1))
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25, linewidth=0.5)
    fig.tight_layout()
    png = OUT / f"HERO_min_minutes_sensitivity_overlay_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--minutes",
        type=float,
        nargs="+",
        default=list(DEFAULT_MINUTES),
        help=f"Playing-time floors to compare (default: {list(DEFAULT_MINUTES)})",
    )
    args = parser.parse_args()
    floors = sorted(set(float(m) for m in args.minutes))

    ensure_hero_dirs()
    results_with_df: list[dict] = []
    from diagnostic_progress import StepProgress

    sweep = StepProgress("min_minutes ladder", floors)
    sweep.header()
    for mm in floors:
        sweep.begin(f"min_minutes={mm:g}")
        res = _run_floor(mm)
        png = _plot_single(res)
        print(
            f"  n={res['n_player_seasons']:,}  drafted={res['n_drafted']:,}  "
            f"mean roster={res['roster_summary']['mean_roster_n']:.1f}  "
            f"shape={res['curvature']['shape']}  bin16={res['curvature']['bin16_rate'] * 100:.2f}%",
            flush=True,
        )
        print(f"  Wrote {png.name}", flush=True)
        results_with_df.append({**res, "png_single": png.name})
    sweep.finish()

    print("\nWriting compare figures ...", flush=True)
    compare_png = _plot_compare(results_with_df)
    overlay_png = _plot_overlay(results_with_df)

    serializable = [{k: v for k, v in res.items() if k != "roster_df"} for res in results_with_df]

    meta_path = OUT / f"HERO_min_minutes_sensitivity_{SEASON_MIN}_{SEASON_MAX}_meta.json"
    meta = {
        "diagnostic": "hero_min_minutes_sensitivity_ladder",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "hero_lock_min_minutes": HERO_LOCK,
        "floors_run": floors,
        "panel_spec": "ppm z, 16 quantile poolq_loo, winsor (0.01, 0.99), rebuild from box",
        "runs": serializable,
        "outputs": {
            "compare_png": compare_png.name,
            "overlay_png": overlay_png.name,
            "single_png_pattern": f"HERO_inverted_u_min{{M}}_{SEASON_MIN}_{SEASON_MAX}.png",
        },
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nWrote {compare_png}")
    print(f"Wrote {overlay_png}")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
