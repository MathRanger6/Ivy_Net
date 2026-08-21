#!/usr/bin/env python3
"""PD22 items 3–4 — PPM distributions (filtered-out vs hero ASSIGN input).

Item 3: raw points-per-minute (PPM) for player-seasons below the minutes floor.
Item 4: raw PPM vs standardized ASSIGN ability (PPM z within season) on min-20 panel.

Run (repo root):
  python sports/scripts/pd22_ppm_distribution.py
  python sports/scripts/pd22_ppm_distribution.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_ppm_distribution_2011_2021.csv
  PD22_ppm_distribution_2011_2021.json
  PD22_ppm_distribution_2011_2021.png
  PD22_ppm_full_vs_filtered_2011_2021.png   # overlay: full panel vs sub-floor PPM
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
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


STEM_PREFIX = "PD22_ppm_distribution"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

OUT = PD22_MINUTES
HERO_LOCK = 20.0


def _overlay_stem() -> str:
    return f"PD22_ppm_full_vs_filtered_{_w().tag}"


def _pipeline_config(*, min_minutes: float) -> object:
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=float(min_minutes),
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=_w().season_min,
        panel_season_max=_w().season_max,
        analysis_season_min=_w().season_min,
        analysis_season_max=_w().season_max,
    )


def _load_panel(*, min_minutes: float) -> pd.DataFrame:
    from sports_pipeline import conductor

    print(f"Rebuilding panel from box (min_minutes={min_minutes:g}) ...", flush=True)
    return conductor.prepare_panel(_pipeline_config(min_minutes=min_minutes))


def _hero_perf_panel(panel_raw: pd.DataFrame) -> pd.DataFrame:
    from sports_pipeline import panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _pipeline_config(min_minutes=HERO_LOCK)
    return panel_build.apply_perf_metric_for_analysis(
        panel_raw,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )


def _summary(
    filtered_out: pd.DataFrame,
    hero_raw: pd.DataFrame,
    hero_perf: pd.DataFrame,
) -> dict:
    fo = filtered_out.copy()
    fo["minutes"] = pd.to_numeric(fo["minutes"], errors="coerce")
    fo["ppm"] = pd.to_numeric(fo["ppm"], errors="coerce")
    positive = fo.loc[fo["minutes"] > 0].copy()
    ppm_pos = positive["ppm"].dropna()
    ppm_all = fo["ppm"].dropna()

    hero_ppm = pd.to_numeric(hero_raw["ppm"], errors="coerce").dropna()
    perf = pd.to_numeric(hero_perf["perf"], errors="coerce").dropna()

    def _tail(arr: pd.Series, thr: float) -> int:
        return int((arr > thr).sum()) if len(arr) else 0

    return {
        "hero_lock_min_minutes": HERO_LOCK,
        "n_filtered_out_total": int(len(fo)),
        "n_filtered_out_zero_minutes": int((fo["minutes"] == 0).sum()),
        "n_filtered_out_positive_minutes": int(len(positive)),
        "n_filtered_out_with_ppm": int(len(ppm_all)),
        "filtered_out_ppm_max": float(ppm_all.max()) if len(ppm_all) else float("nan"),
        "filtered_out_ppm_p99": float(np.percentile(ppm_all, 99)) if len(ppm_all) else float("nan"),
        "filtered_out_ppm_median_positive_min": float(ppm_pos.median()) if len(ppm_pos) else float("nan"),
        "n_filtered_out_ppm_gt_1": _tail(ppm_pos, 1.0),
        "n_filtered_out_ppm_gt_2": _tail(ppm_pos, 2.0),
        "n_hero_panel": int(len(hero_raw)),
        "hero_raw_ppm_median": float(hero_ppm.median()) if len(hero_ppm) else float("nan"),
        "hero_raw_ppm_p99": float(np.percentile(hero_ppm, 99)) if len(hero_ppm) else float("nan"),
        "hero_perf_median": float(perf.median()) if len(perf) else float("nan"),
        "hero_perf_p01": float(np.percentile(perf, 1)) if len(perf) else float("nan"),
        "hero_perf_p99": float(np.percentile(perf, 99)) if len(perf) else float("nan"),
    }


def _add_stats_inset_under_legend(ax, fig, text: str, *, fontsize: int = 8) -> None:
    """Light-blue stats box stacked under ax legend (upper-right anchor)."""
    leg = ax.get_legend()
    if leg is not None:
        fig.draw_without_rendering()
        leg_bbox = leg.get_window_extent().transformed(ax.transAxes.inverted())
        anchor = (leg_bbox.x1, leg_bbox.y0 - 0.012)
    else:
        anchor = (1.0, 0.95)
    inset = AnchoredText(
        text,
        loc="upper right",
        bbox_to_anchor=anchor,
        bbox_transform=ax.transAxes,
        prop={"size": fontsize, "family": "sans-serif"},
        frameon=True,
        borderpad=0.45,
    )
    inset.patch.set_facecolor((0.88, 0.94, 1.0, 0.92))
    inset.patch.set_edgecolor("#9eb8d9")
    inset.patch.set_linewidth(0.8)
    inset.set_zorder(5)
    ax.add_artist(inset)


def _plot_ppm(
    filtered_out: pd.DataFrame,
    hero_raw: pd.DataFrame,
    hero_perf: pd.DataFrame,
    summary: dict,
    png_path: Path,
    *,
    logy_left: bool = True,
) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(_w().season_min, _w().season_max)

    fo = filtered_out.copy()
    fo["minutes"] = pd.to_numeric(fo["minutes"], errors="coerce")
    fo["ppm"] = pd.to_numeric(fo["ppm"], errors="coerce")
    ppm_filtered = fo.loc[fo["minutes"] > 0, "ppm"].dropna().to_numpy(dtype=float)

    hero_ppm = pd.to_numeric(hero_raw["ppm"], errors="coerce").dropna().to_numpy(dtype=float)
    perf = pd.to_numeric(hero_perf["perf"], errors="coerce").dropna().to_numpy(dtype=float)

    fig = plt.figure(figsize=(11.5, 5.4))
    gs_outer = gridspec.GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[2, 1],
        width_ratios=[1, 1],
        hspace=0.36,
        wspace=0.28,
    )
    ax_left = fig.add_subplot(gs_outer[0, 0])
    gs_right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs_outer[:, 1], hspace=0.32)
    ax_raw = fig.add_subplot(gs_right[0, 0])
    ax_perf = fig.add_subplot(gs_right[1, 0])

    # Item 3 — filtered-out raw PPM (positive minutes only; zeros counted in title)
    if len(ppm_filtered):
        p99_f = float(np.percentile(ppm_filtered, 99))
        x_hi_f = max(1.5, min(p99_f * 1.1, float(np.max(ppm_filtered))))
        bins_f = np.linspace(0.0, x_hi_f, 40)
        ax_left.hist(
            ppm_filtered,
            bins=bins_f,
            color="steelblue",
            alpha=0.88,
            edgecolor="white",
            label=rf"Sub-{HERO_LOCK:g} min tail ($> 0$ min)",
        )
    ax_left.set_xlabel("Raw PPM")
    if logy_left:
        ax_left.set_yscale("log")
        ax_left.set_ylabel("Player-season count (log scale)")
        ax_left.set_ylim(bottom=1.0)
    else:
        ax_left.set_ylabel("Player-season count")
    ax_left.set_title(
        f"Filtered out (minutes < {HERO_LOCK:g}, > 0 min) · "
        f"n={summary['n_filtered_out_positive_minutes']:,}"
    )
    ax_left.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax_left.legend(loc="upper right", framealpha=0.92, fontsize=8)

    # Item 4 top — hero panel raw PPM
    if len(hero_ppm):
        p99_h = float(np.percentile(hero_ppm, 99))
        x_hi_h = max(1.0, min(p99_h * 1.05, float(np.max(hero_ppm))))
        bins_h = np.linspace(0.0, x_hi_h, 35)
        ax_raw.hist(hero_ppm, bins=bins_h, color="steelblue", alpha=0.88, edgecolor="white")
    ax_raw.set_ylabel("Count")
    ax_raw.set_title(rf"Hero panel (min $\geq$ {HERO_LOCK:g}) — raw PPM")
    ax_raw.grid(axis="y", alpha=0.25, linewidth=0.5)

    # Item 4 bottom — ASSIGN ability (PPM z within season)
    if len(perf):
        ax_perf.hist(perf, bins=40, color="darkorange", alpha=0.88, edgecolor="white")
    ax_perf.set_xlabel("ASSIGN ability (PPM z within season)")
    ax_perf.set_ylabel("Count")
    ax_perf.set_title("Hero panel — standardized ability input to ASSIGN")
    ax_perf.grid(axis="y", alpha=0.25, linewidth=0.5)

    fig.suptitle(
        f"PD22 items 3–4 — PPM tails · {seasons} · "
        f"{summary['n_filtered_out_ppm_gt_1']:,} sub-{HERO_LOCK:g}-min rows with PPM > 1",
        fontsize=11,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))

    stats = (
        f"0-min rows excluded: {summary['n_filtered_out_zero_minutes']:,}\n"
        f"PPM > 1.0: {summary['n_filtered_out_ppm_gt_1']:,}\n"
        f"max PPM: {summary['filtered_out_ppm_max']:.2g}"
    )
    _add_stats_inset_under_legend(ax_left, fig, stats)

    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _positive_ppm_arrays(panel: pd.DataFrame) -> np.ndarray:
    frame = panel.copy()
    frame["minutes"] = pd.to_numeric(frame["minutes"], errors="coerce")
    frame["ppm"] = pd.to_numeric(frame.get("ppm"), errors="coerce")
    return frame.loc[frame["minutes"] > 0, "ppm"].dropna().to_numpy(dtype=float)


def _shared_ppm_bins(*arrays: np.ndarray, n_bins: int = 45) -> np.ndarray:
    combined = np.concatenate([a for a in arrays if len(a)])
    if len(combined) == 0:
        return np.linspace(0.0, 1.5, n_bins)
    p99 = float(np.percentile(combined, 99))
    x_hi = max(1.5, min(p99 * 1.08, float(np.max(combined))))
    return np.linspace(0.0, x_hi, n_bins)


def _plot_ppm_overlay(
    full_ppm: np.ndarray,
    filtered_ppm: np.ndarray,
    summary: dict,
    png_path: Path,
    *,
    logy: bool = True,
) -> None:
    """Single large figure: full-panel raw PPM vs sub-floor (filtered-out) overlay."""
    configure_matplotlib_mathtext()
    seasons = seasons_label(_w().season_min, _w().season_max)
    bins = _shared_ppm_bins(full_ppm, filtered_ppm)

    fig, ax = plt.subplots(figsize=(10.5, 6.2))

    if len(full_ppm):
        ax.hist(
            full_ppm,
            bins=bins,
            color="0.72",
            alpha=0.55,
            edgecolor="white",
            linewidth=0.4,
            label=f"Full panel (> 0 min, n={len(full_ppm):,})",
            zorder=1,
        )
    if len(filtered_ppm):
        ax.hist(
            filtered_ppm,
            bins=bins,
            color="steelblue",
            alpha=0.82,
            edgecolor="white",
            linewidth=0.4,
            label=(
                f"Sub-{HERO_LOCK:g} min filtered out (> 0 min, "
                f"n={summary['n_filtered_out_positive_minutes']:,})"
            ),
            zorder=2,
        )

    ax.set_xlabel("Raw PPM")
    if logy:
        ax.set_yscale("log")
        ax.set_ylabel("Player-season count (log scale)")
        ax.set_ylim(bottom=1.0)
    else:
        ax.set_ylabel("Player-season count")
    ax.set_title(
        rf"PD22 — raw PPM overlay · full panel vs sub-{HERO_LOCK:g}-min tail · {seasons}",
        fontsize=12,
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=9)

    stats = (
        f"0-min excluded (no PPM): {summary['n_filtered_out_zero_minutes']:,} sub-{HERO_LOCK:g}\n"
        f"Sub-{HERO_LOCK:g} with PPM > 1.0: {summary['n_filtered_out_ppm_gt_1']:,}\n"
        f"Max PPM (sub-{HERO_LOCK:g}): {summary['filtered_out_ppm_max']:.2g}"
    )
    fig.tight_layout()
    _add_stats_inset_under_legend(ax, fig, stats)

    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{_stem()}.csv",
        "json": OUT / f"{_stem()}.json",
        "png": OUT / f"{_stem()}.png",
        "overlay_png": OUT / f"{_overlay_stem()}.png",
    }


def run_ppm(*, write_csv: bool = True, logy_left: bool = True) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    panel0 = _load_panel(min_minutes=0.0)
    panel20 = _load_panel(min_minutes=HERO_LOCK)
    hero_perf = _hero_perf_panel(panel20)

    panel0 = panel0.copy()
    panel0["minutes"] = pd.to_numeric(panel0["minutes"], errors="coerce")
    panel0["ppm"] = pd.to_numeric(panel0.get("ppm"), errors="coerce")
    filtered_out = panel0.loc[panel0["minutes"] < HERO_LOCK].copy()

    summary = _summary(filtered_out, panel20, hero_perf)
    full_ppm = _positive_ppm_arrays(panel0)
    filtered_ppm = _positive_ppm_arrays(filtered_out)
    _plot_ppm(filtered_out, panel20, hero_perf, summary, paths["png"], logy_left=logy_left)
    _plot_ppm_overlay(
        full_ppm,
        filtered_ppm,
        summary,
        paths["overlay_png"],
        logy=logy_left,
    )

    if write_csv:
        fo_out = filtered_out[["minutes", "ppm"]].copy()
        fo_out["role"] = "filtered_out"
        hr = panel20[["minutes", "ppm"]].copy()
        hr["role"] = "hero_raw"
        hp = hero_perf[["minutes", "ppm", "perf"]].copy()
        hp["role"] = "hero_assign"
        pd.concat([fo_out, hr, hp], ignore_index=True).to_csv(
            paths["csv"], index=False, float_format="%.12g"
        )

    meta = {
        "diagnostic": "pd22_ppm_distribution",
        "date": date.today().isoformat(),
        "season_min": _w().season_min,
        "season_max": _w().season_max,
        "seasons": seasons_label(_w().season_min, _w().season_max),
        "panel_spec": {
            "filtered_out": "min_minutes=0 rebuild; minutes < hero_lock",
            "hero_panel": f"min_minutes={HERO_LOCK:g} rebuild; raw PPM column",
            "assign_ability": f"hero panel + PPM z within season (PD21 ASSIGN input)",
        },
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nFiltered out (< {HERO_LOCK:g} min): {summary['n_filtered_out_total']:,} rows", flush=True)
    print(
        f"  positive minutes: {summary['n_filtered_out_positive_minutes']:,}; "
        f"PPM > 1: {summary['n_filtered_out_ppm_gt_1']:,}; "
        f"max PPM: {summary['filtered_out_ppm_max']:.3g}",
        flush=True,
    )
    print(f"Hero panel (min >= {HERO_LOCK:g}): {summary['n_hero_panel']:,} rows", flush=True)
    print(f"Full panel (> 0 min): {len(full_ppm):,} rows", flush=True)
    print(f"\nWrote {paths['png']}", flush=True)
    print(f"Wrote {paths['overlay_png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    if write_csv:
        print(f"Wrote {paths['csv']}", flush=True)
    return meta


def plot_only(*, logy_left: bool = True) -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    summary = meta.get("summary") or {}

    df = pd.read_csv(paths["csv"])
    filtered_out = df.loc[df["role"] == "filtered_out"].copy()
    panel20 = df.loc[df["role"] == "hero_raw"].copy()
    hero_perf = df.loc[df["role"] == "hero_assign"].copy()
    if not summary:
        summary = _summary(filtered_out, panel20, hero_perf)
    full_panel = pd.concat([filtered_out, panel20], ignore_index=True)
    full_ppm = _positive_ppm_arrays(full_panel)
    filtered_ppm = _positive_ppm_arrays(filtered_out)
    _plot_ppm(filtered_out, panel20, hero_perf, summary, paths["png"], logy_left=logy_left)
    _plot_ppm_overlay(
        full_ppm,
        filtered_ppm,
        summary,
        paths["overlay_png"],
        logy=logy_left,
    )
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['overlay_png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV (no panel rebuild)",
    )
    parser.add_argument(
        "--linear-y-left",
        action="store_true",
        help="Linear y-axis on PPM histograms (default: log scale)",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    logy_left = not args.linear_y_left

    if args.plot_only:
        plot_only(logy_left=logy_left)
        return

    run_ppm(logy_left=logy_left)


if __name__ == "__main__":
    main()
