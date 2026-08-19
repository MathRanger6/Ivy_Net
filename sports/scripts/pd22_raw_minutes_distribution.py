#!/usr/bin/env python3
"""PD22 item 2 — raw panel season-minutes distribution.

Rebuild panel at min_minutes=0; plot minutes ECDF for all player-seasons with
ever-draft overlay and candidate floor markers (10 / 20 min).

Run (repo root):
  python sports/scripts/pd22_raw_minutes_distribution.py
  python sports/scripts/pd22_raw_minutes_distribution.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_raw_minutes_distribution_2011_2021.csv
  PD22_raw_minutes_distribution_2011_2021.json
  PD22_raw_minutes_distribution_2011_2021.png
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import PD22_MINUTES, ensure_hero_dirs
from interval_overlap_paths import seasons_label

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_raw_minutes_distribution"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

OUT = PD22_MINUTES
HERO_LOCK = 20.0
ALT_FLOOR = 10.0


def _pipeline_config() -> object:
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=0.0,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=_w().season_min,
        panel_season_max=_w().season_max,
        analysis_season_min=_w().season_min,
        analysis_season_max=_w().season_max,
    )


def _load_raw_panel() -> pd.DataFrame:
    from sports_pipeline import conductor

    cfg = _pipeline_config()
    print("Rebuilding panel from box (min_minutes=0) ...", flush=True)
    panel = conductor.prepare_panel(cfg)
    if "minutes" not in panel.columns:
        raise KeyError("Panel missing minutes column.")
    return panel


def _minutes_frame(panel: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(
        {
            "minutes": pd.to_numeric(panel["minutes"], errors="coerce"),
            "Y_draft": pd.to_numeric(panel.get("Y_draft"), errors="coerce").fillna(0).astype(int)
            if "Y_draft" in panel.columns
            else 0,
        }
    )
    return out.dropna(subset=["minutes"]).reset_index(drop=True)


def _summary(frame: pd.DataFrame) -> dict:
    mins = frame["minutes"].to_numpy(dtype=float)
    n = int(len(mins))
    drafted = frame.loc[frame["Y_draft"] == 1, "minutes"].to_numpy(dtype=float)
    pct = lambda thr: float(np.mean(mins < thr) * 100.0) if n else float("nan")

    return {
        "n_player_seasons": n,
        "n_drafted_player_seasons": int((frame["Y_draft"] == 1).sum()),
        "n_zero_minutes": int(np.sum(mins == 0)),
        "pct_zero_minutes": float(np.mean(mins == 0) * 100.0) if n else float("nan"),
        "minutes_median": float(np.median(mins)) if n else float("nan"),
        "minutes_p25": float(np.percentile(mins, 25)) if n else float("nan"),
        "minutes_p75": float(np.percentile(mins, 75)) if n else float("nan"),
        "minutes_p90": float(np.percentile(mins, 90)) if n else float("nan"),
        "minutes_p99": float(np.percentile(mins, 99)) if n else float("nan"),
        "minutes_max": float(np.max(mins)) if n else float("nan"),
        "pct_below_10": pct(ALT_FLOOR),
        "pct_below_15": pct(15.0),
        "pct_below_20": pct(HERO_LOCK),
        "drafted_minutes_median": float(np.median(drafted)) if len(drafted) else float("nan"),
        "drafted_pct_below_20": float(np.mean(drafted < HERO_LOCK) * 100.0) if len(drafted) else float("nan"),
        "hero_lock_min_minutes": HERO_LOCK,
        "alt_floor_min_minutes": ALT_FLOOR,
    }


def _plot_ecdf(ax, values: np.ndarray, *, color: str, label: str, lw: float = 2.0) -> None:
    if len(values) == 0:
        return
    xs = np.sort(values)
    ys = np.arange(1, len(xs) + 1) / len(xs)
    ax.step(xs, ys, where="post", color=color, lw=lw, label=label)


def _plot_distribution(frame: pd.DataFrame, summary: dict, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(_w().season_min, _w().season_max)
    mins_all = frame["minutes"].to_numpy(dtype=float)
    mins_drafted = frame.loc[frame["Y_draft"] == 1, "minutes"].to_numpy(dtype=float)

    fig = plt.figure(figsize=(11.5, 5.4))
    gs = gridspec.GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[2, 1],
        width_ratios=[1, 1],
        hspace=0.14,
        wspace=0.28,
    )
    ax_left = fig.add_subplot(gs[0, 0])
    ax_right = fig.add_subplot(gs[:, 1])

    ax = ax_left
    _plot_ecdf(ax, mins_all, color="steelblue", label=rf"All player-seasons ($n={len(mins_all):,}$)")
    _plot_ecdf(
        ax,
        mins_drafted,
        color="darkorange",
        lw=1.8,
        label=rf"Ever-draft ($Y_{{\mathrm{{draft}}}}=1$, $n={len(mins_drafted):,}$)",
    )
    for thr, color, ls in [(ALT_FLOOR, "teal", "--"), (HERO_LOCK, "crimson", "-")]:
        ax.axvline(thr, color=color, ls=ls, lw=1.5, alpha=0.85)
    x_hi = float(np.percentile(mins_all, 99)) if len(mins_all) else 500.0
    ax.set_xlim(left=0, right=max(x_hi, HERO_LOCK + 5))
    ax.set_xlabel("Season minutes")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title(rf"Full panel — empirical CDF (ECDF) · {seasons}")
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=8, loc="lower right")

    ax = ax_right
    zoom_hi = 150.0
    bins = [0, 5, 10, 15, 20, 30, 45, 60, 90, 120, zoom_hi]
    ax.hist(
        mins_all[mins_all <= zoom_hi],
        bins=bins,
        color="steelblue",
        alpha=0.85,
        edgecolor="white",
        label="All player-seasons",
    )
    drafted_zoom = mins_drafted[mins_drafted <= zoom_hi]
    if len(drafted_zoom):
        ax.hist(
            drafted_zoom,
            bins=bins,
            histtype="step",
            lw=2,
            color="darkorange",
            label="Ever-draft",
        )
    for thr, color in [(ALT_FLOOR, "teal"), (HERO_LOCK, "crimson")]:
        ax.axvline(thr, color=color, ls="--", lw=1.5, alpha=0.85)
    ax.set_xlabel(rf"Season minutes (zoom $0$–${int(zoom_hi)}$)")
    ax.set_ylabel("Player-season count")
    ax.set_title(
        f"Low-minute region · {summary['pct_below_20']:.1f}% all below {HERO_LOCK:g} min"
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=8, loc="upper right")

    fig.suptitle(
        f"PD22 item 2 — raw panel minutes · median = {summary['minutes_median']:.0f} · "
        f"{summary['n_zero_minutes']:,} rows at 0 min ({summary['pct_zero_minutes']:.1f}%)",
        fontsize=11,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{_stem()}.csv",
        "json": OUT / f"{_stem()}.json",
        "png": OUT / f"{_stem()}.png",
    }


def run_distribution(*, write_csv: bool = True) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    panel = _load_raw_panel()
    frame = _minutes_frame(panel)
    summary = _summary(frame)

    if write_csv:
        frame.to_csv(paths["csv"], index=False, float_format="%.12g")

    _plot_distribution(frame, summary, paths["png"])

    meta = {
        "diagnostic": "pd22_raw_minutes_distribution",
        "date": date.today().isoformat(),
        "season_min": _w().season_min,
        "season_max": _w().season_max,
        "seasons": seasons_label(_w().season_min, _w().season_max),
        "panel_spec": "rebuild from box, min_minutes=0, no playing-time filter",
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nPlayer-seasons: {summary['n_player_seasons']:,}", flush=True)
    print(f"Median minutes: {summary['minutes_median']:.1f}", flush=True)
    print(
        f"Below {HERO_LOCK:g} min: {summary['pct_below_20']:.2f}% all · "
        f"{summary['drafted_pct_below_20']:.2f}% ever-draft",
        flush=True,
    )
    print(f"Zero-minute rows: {summary['n_zero_minutes']:,} ({summary['pct_zero_minutes']:.2f}%)", flush=True)
    print(f"\nWrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    frame = pd.read_csv(paths["csv"])
    summary = _summary(frame)
    _plot_distribution(frame, summary, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV (no panel rebuild)",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    if args.plot_only:
        plot_only()
        return

    run_distribution()


if __name__ == "__main__":
    main()
