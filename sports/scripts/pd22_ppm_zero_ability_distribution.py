#!/usr/bin/env python3
"""PD22 item 6 — ability distribution under PPM-zero vs drop policy.

Compare post-policy raw PPM and ASSIGN ability (PPM z within season) on:
  - Drop panel (min_minutes = 20, PD21 default)
  - PPM-zero panel (min_minutes = 0, ppm forced to 0 below threshold)

Run (repo root):
  python sports/scripts/pd22_ppm_zero_ability_distribution.py
  python sports/scripts/pd22_ppm_zero_ability_distribution.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_ppm_zero_ability_distribution_2011_2021.csv
  PD22_ppm_zero_ability_distribution_2011_2021.json
  PD22_ppm_zero_ability_distribution_2011_2021.png
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
from pd21_rho_hsort_calibrate import PanelPrepConfig, prepare_calibration_panel

OUT = PD22_MINUTES
SEASON_MIN = 2011
SEASON_MAX = 2021
HERO_LOCK = 20.0
STEM = f"PD22_ppm_zero_ability_distribution_{SEASON_MIN}_{SEASON_MAX}"


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
        panel_season_min=SEASON_MIN,
        panel_season_max=SEASON_MAX,
        analysis_season_min=SEASON_MIN,
        analysis_season_max=SEASON_MAX,
    )


def _load_drop_panel() -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _pipeline_config(min_minutes=HERO_LOCK)
    print(f"Rebuilding drop panel (min_minutes={HERO_LOCK:g}) ...", flush=True)
    raw = conductor.prepare_panel(cfg)
    return panel_build.apply_perf_metric_for_analysis(
        raw,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )


def _load_ppm_zero_panel(*, ppm_zero_below_minutes: float) -> pd.DataFrame:
    cfg = PanelPrepConfig.from_args(min_minutes=0.0, ppm_zero_below_minutes=ppm_zero_below_minutes)
    print(f"Rebuilding PPM-zero panel (threshold={ppm_zero_below_minutes:g} min) ...", flush=True)
    return prepare_calibration_panel(cfg)


def _tag_zeroed(df: pd.DataFrame, *, threshold: float) -> pd.DataFrame:
    out = df.copy()
    out["minutes"] = pd.to_numeric(out["minutes"], errors="coerce")
    out["ppm"] = pd.to_numeric(out["ppm"], errors="coerce")
    out["perf"] = pd.to_numeric(out["perf"], errors="coerce")
    out["zeroed_by_policy"] = out["minutes"].notna() & (out["minutes"] < float(threshold))
    return out


def _summary(drop: pd.DataFrame, ppm_zero: pd.DataFrame, *, ppm_zero_below_minutes: float) -> dict:
    thr = float(ppm_zero_below_minutes)
    drop = _tag_zeroed(drop, threshold=thr)
    ppm_zero = _tag_zeroed(ppm_zero, threshold=thr)

    drop_ppm = drop["ppm"].dropna()
    drop_perf = drop["perf"].dropna()
    pz_ppm = ppm_zero["ppm"].dropna()
    pz_perf = ppm_zero["perf"].dropna()
    pz_zeroed = ppm_zero.loc[ppm_zero["zeroed_by_policy"]]
    pz_rotation = ppm_zero.loc[~ppm_zero["zeroed_by_policy"]]

    n_raw_ppm0 = int((pz_ppm == 0).sum())
    perf_zeroed = pd.to_numeric(pz_zeroed["perf"], errors="coerce").dropna()
    perf_rotation = pd.to_numeric(pz_rotation["perf"], errors="coerce").dropna()

    return {
        "hero_lock_min_minutes": HERO_LOCK,
        "ppm_zero_below_minutes": thr,
        "n_drop_panel": int(len(drop)),
        "n_ppm_zero_panel": int(len(ppm_zero)),
        "n_zeroed_by_policy": int(ppm_zero["zeroed_by_policy"].sum()),
        "pct_zeroed_by_policy": float(ppm_zero["zeroed_by_policy"].mean()),
        "n_raw_ppm_eq_zero_ppm_zero": n_raw_ppm0,
        "drop_raw_ppm_median": float(drop_ppm.median()) if len(drop_ppm) else float("nan"),
        "ppm_zero_raw_ppm_median": float(pz_ppm.median()) if len(pz_ppm) else float("nan"),
        "drop_perf_median": float(drop_perf.median()) if len(drop_perf) else float("nan"),
        "ppm_zero_perf_median": float(pz_perf.median()) if len(pz_perf) else float("nan"),
        "ppm_zero_perf_median_zeroed_cohort": float(perf_zeroed.median()) if len(perf_zeroed) else float("nan"),
        "ppm_zero_perf_median_rotation_cohort": float(perf_rotation.median()) if len(perf_rotation) else float("nan"),
        "n_perf_below_minus1_drop": int((drop_perf < -1).sum()) if len(drop_perf) else 0,
        "n_perf_below_minus1_ppm_zero": int((pz_perf < -1).sum()) if len(pz_perf) else 0,
        "ppm_zero_perf_p01": float(np.percentile(pz_perf, 1)) if len(pz_perf) else float("nan"),
        "ppm_zero_perf_p99": float(np.percentile(pz_perf, 99)) if len(pz_perf) else float("nan"),
    }


def _add_stats_inset(ax, fig, text: str, *, fontsize: int = 8) -> None:
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


def _plot(drop: pd.DataFrame, ppm_zero: pd.DataFrame, summary: dict, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    thr = float(summary["ppm_zero_below_minutes"])

    drop = _tag_zeroed(drop, threshold=thr)
    ppm_zero = _tag_zeroed(ppm_zero, threshold=thr)

    drop_ppm = drop["ppm"].dropna().to_numpy(dtype=float)
    drop_perf = drop["perf"].dropna().to_numpy(dtype=float)
    pz_ppm = ppm_zero["ppm"].dropna().to_numpy(dtype=float)
    pz_perf = ppm_zero["perf"].dropna().to_numpy(dtype=float)
    pz_perf_rot = ppm_zero.loc[~ppm_zero["zeroed_by_policy"], "perf"].dropna().to_numpy(dtype=float)
    pz_perf_zero = ppm_zero.loc[ppm_zero["zeroed_by_policy"], "perf"].dropna().to_numpy(dtype=float)

    fig = plt.figure(figsize=(11.8, 6.2))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.28)

    ax_drop_ppm = fig.add_subplot(gs[0, 0])
    ax_pz_ppm = fig.add_subplot(gs[0, 1])
    ax_drop_perf = fig.add_subplot(gs[1, 0])
    ax_pz_perf = fig.add_subplot(gs[1, 1])

    # Raw PPM — drop
    if len(drop_ppm):
        p99 = float(np.percentile(drop_ppm, 99))
        x_hi = max(1.0, min(p99 * 1.05, float(np.max(drop_ppm))))
        ax_drop_ppm.hist(drop_ppm, bins=np.linspace(0, x_hi, 35), color="steelblue", alpha=0.88, edgecolor="white")
    ax_drop_ppm.set_ylabel("Count")
    ax_drop_ppm.set_title(rf"Drop policy — raw PPM (min $\geq$ {HERO_LOCK:g})")
    ax_drop_ppm.grid(axis="y", alpha=0.25, linewidth=0.5)

    # Raw PPM — PPM-zero (expect spike at 0)
    if len(pz_ppm):
        p99 = float(np.percentile(pz_ppm, 99))
        x_hi = max(1.0, min(p99 * 1.05, float(np.max(pz_ppm))))
        bins = np.linspace(0, x_hi, 35)
        ax_pz_ppm.hist(pz_ppm, bins=bins, color="steelblue", alpha=0.88, edgecolor="white")
    ax_pz_ppm.set_ylabel("Count")
    ax_pz_ppm.set_title(rf"PPM-zero — raw PPM ($n_{{ppm=0}}$ = {summary['n_raw_ppm_eq_zero_ppm_zero']:,})")
    ax_pz_ppm.grid(axis="y", alpha=0.25, linewidth=0.5)
    ppm_stats = (
        f"Zeroed rows: {summary['n_zeroed_by_policy']:,}\n"
        f"({100 * summary['pct_zeroed_by_policy']:.1f}% of panel)\n"
        f"median raw PPM = {summary['ppm_zero_raw_ppm_median']:.3g}"
    )
    _add_stats_inset(ax_pz_ppm, fig, ppm_stats)

    # ASSIGN ability — drop
    if len(drop_perf):
        ax_drop_perf.hist(drop_perf, bins=40, color="darkorange", alpha=0.88, edgecolor="white")
    ax_drop_perf.set_xlabel("ASSIGN ability (PPM z within season)")
    ax_drop_perf.set_ylabel("Count")
    ax_drop_perf.set_title(rf"Drop — standardized ability ($n={summary['n_drop_panel']:,}$)")
    ax_drop_perf.grid(axis="y", alpha=0.25, linewidth=0.5)

    # ASSIGN ability — PPM-zero (rotation vs zeroed cohort)
    perf_bins = np.linspace(-4, 6, 50)
    if len(pz_perf_rot):
        ax_pz_perf.hist(
            pz_perf_rot,
            bins=perf_bins,
            color="darkorange",
            alpha=0.75,
            edgecolor="white",
            label=rf"Rotation (min $\geq$ {HERO_LOCK:g})",
        )
    if len(pz_perf_zero):
        ax_pz_perf.hist(
            pz_perf_zero,
            bins=perf_bins,
            color="0.55",
            alpha=0.85,
            edgecolor="white",
            label=rf"Zeroed (min $<$ {HERO_LOCK:g})",
        )
    ax_pz_perf.set_xlabel("ASSIGN ability (PPM z within season)")
    ax_pz_perf.set_ylabel("Count")
    ax_pz_perf.set_title(rf"PPM-zero — ability by cohort ($n={summary['n_ppm_zero_panel']:,}$)")
    ax_pz_perf.legend(loc="upper right", fontsize=8, framealpha=0.92)
    ax_pz_perf.grid(axis="y", alpha=0.25, linewidth=0.5)
    perf_stats = (
        f"Below $-1$ z: {summary['n_perf_below_minus1_ppm_zero']:,}\n"
        f"(drop panel: {summary['n_perf_below_minus1_drop']:,})\n"
        f"zeroed cohort median = {summary['ppm_zero_perf_median_zeroed_cohort']:.2f}"
    )
    _add_stats_inset(ax_pz_perf, fig, perf_stats)

    fig.suptitle(
        rf"PD22 item 6 — PPM-zero vs drop ability · {seasons} · "
        rf"{summary['n_zeroed_by_policy']:,} bench rows forced to PPM = 0",
        fontsize=11,
        y=0.98,
    )
    fig.subplots_adjust(top=0.90, hspace=0.38, wspace=0.28)
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{STEM}.csv",
        "json": OUT / f"{STEM}.json",
        "png": OUT / f"{STEM}.png",
    }


def run(*, ppm_zero_below_minutes: float) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    drop = _load_drop_panel()
    ppm_zero = _load_ppm_zero_panel(ppm_zero_below_minutes=ppm_zero_below_minutes)
    summary = _summary(drop, ppm_zero, ppm_zero_below_minutes=ppm_zero_below_minutes)
    _plot(drop, ppm_zero, summary, paths["png"])

    rows = []
    for policy, frame in (("drop", drop), ("ppm_zero", ppm_zero)):
        tagged = _tag_zeroed(frame, threshold=ppm_zero_below_minutes)
        chunk = tagged[["minutes", "ppm", "perf", "zeroed_by_policy"]].copy()
        chunk["policy"] = policy
        rows.append(chunk)
    pd.concat(rows, ignore_index=True).to_csv(paths["csv"], index=False, float_format="%.12g")

    meta = {
        "diagnostic": "pd22_ppm_zero_ability_distribution",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "panel_spec": {
            "drop": f"min_minutes={HERO_LOCK:g}; PPM z within season",
            "ppm_zero": f"min_minutes=0 + ppm_zero_below={ppm_zero_below_minutes:g}; PPM z within season",
        },
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nDrop panel: n={summary['n_drop_panel']:,}", flush=True)
    print(
        f"PPM-zero panel: n={summary['n_ppm_zero_panel']:,}; "
        f"zeroed={summary['n_zeroed_by_policy']:,} ({100 * summary['pct_zeroed_by_policy']:.1f}%)",
        flush=True,
    )
    print(f"Raw PPM = 0 under PPM-zero: {summary['n_raw_ppm_eq_zero_ppm_zero']:,}", flush=True)
    print(
        f"ASSIGN perf below -1: drop={summary['n_perf_below_minus1_drop']:,}, "
        f"ppm-zero={summary['n_perf_below_minus1_ppm_zero']:,}",
        flush=True,
    )
    print(f"\nWrote {paths['png']}", flush=True)
    print(f"Wrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only(*, ppm_zero_below_minutes: float) -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    df = pd.read_csv(paths["csv"])
    drop = df.loc[df["policy"] == "drop"].copy()
    ppm_zero = df.loc[df["policy"] == "ppm_zero"].copy()
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    thr = float(meta.get("summary", {}).get("ppm_zero_below_minutes", ppm_zero_below_minutes))
    summary = _summary(drop, ppm_zero, ppm_zero_below_minutes=thr)
    _plot(drop, ppm_zero, summary, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ppm-zero-below-minutes",
        type=float,
        default=HERO_LOCK,
        help=f"Minutes threshold for PPM-zero policy (default: {HERO_LOCK:g})",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV (no panel rebuild)",
    )
    args = parser.parse_args()
    if args.plot_only:
        plot_only(ppm_zero_below_minutes=float(args.ppm_zero_below_minutes))
    else:
        run(ppm_zero_below_minutes=float(args.ppm_zero_below_minutes))


if __name__ == "__main__":
    main()
