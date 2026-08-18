#!/usr/bin/env python3
"""PD22 — team-season roster size (before vs after box QC, min_minutes=0).

Counts player-season rows per (team_id, season) from panel rebuild at min=0,
optionally with legacy raw box (no QC) or default box QC (dash + min games filter).
Compares to min-20 hero panel on the same figure.

Run (repo root):
  python sports/scripts/pd22_raw_roster_size_distribution.py --before-qc-only
  python sports/scripts/pd22_raw_roster_size_distribution.py --after-qc-only
  python sports/scripts/pd22_raw_roster_size_distribution.py
  python sports/scripts/pd22_raw_roster_size_distribution.py --plot-only --before-qc-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_raw_roster_size_distribution_before_qc_2011_2021.{png,json,csv}
  PD22_raw_roster_size_distribution_after_qc_2011_2021.{png,json,csv}
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

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import PD22_MINUTES, ensure_hero_dirs
from interval_overlap_paths import seasons_label
from pd22_slide_common import KEEP_MIN_TEAM_SEASON_GAMES

OUT = PD22_MINUTES
SEASON_MIN = 2011
SEASON_MAX = 2021
HERO_LOCK = 20.0
NCAA_DRESS_CAP = 15


def _stem(*, before_qc: bool) -> str:
    base = f"PD22_raw_roster_size_distribution_{SEASON_MIN}_{SEASON_MAX}"
    return f"{base}_before_qc" if before_qc else f"{base}_after_qc"


def _pipeline_config(*, min_minutes: float, before_qc: bool) -> object:
    from sports_pipeline.config import PipelineConfig

    kw: dict = dict(
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
    if before_qc:
        kw["drop_dash_placeholder_names"] = False
        kw["min_team_season_games"] = 0
    return PipelineConfig(**kw)


def _load_panel(*, min_minutes: float, before_qc: bool) -> pd.DataFrame:
    from sports_pipeline import conductor

    label = "legacy raw box (QC off)" if before_qc else "box QC on"
    print(f"Rebuilding panel from {label}, min_minutes={min_minutes:g} ...", flush=True)
    return conductor.prepare_panel(_pipeline_config(min_minutes=min_minutes, before_qc=before_qc))


def _roster_table(panel: pd.DataFrame) -> pd.DataFrame:
    use = panel.dropna(subset=["team_id", "season"]).copy()
    return (
        use.groupby(["team_id", "season"], observed=True)
        .size()
        .rename("roster_n")
        .reset_index()
        .sort_values(["season", "team_id"])
    )


def _summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=int)
    if len(v) == 0:
        return {"n": 0}
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": int(v.min()),
        "max": int(v.max()),
        "median": float(np.median(v)),
        "p10": float(np.quantile(v, 0.10)),
        "p25": float(np.quantile(v, 0.25)),
        "p75": float(np.quantile(v, 0.75)),
        "p90": float(np.quantile(v, 0.90)),
        "share_eq_15": float((v == NCAA_DRESS_CAP).mean()),
        "share_ge_15": float((v >= NCAA_DRESS_CAP).mean()),
        "share_gt_15": float((v > NCAA_DRESS_CAP).mean()),
    }


def _histogram_bins(*arrays: np.ndarray) -> np.ndarray:
    lo = min(int(a.min()) for a in arrays if len(a))
    hi = max(int(a.max()) for a in arrays if len(a))
    return np.arange(lo - 0.5, hi + 1.5, 1.0)


def _plot(
    raw_sizes: np.ndarray,
    filtered_sizes: np.ndarray | None,
    *,
    raw_stats: dict,
    filtered_stats: dict | None,
    png_path: Path,
    before_qc: bool,
) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    arrays = [raw_sizes] if filtered_sizes is None or len(filtered_sizes) == 0 else [
        raw_sizes,
        filtered_sizes,
    ]
    bins = _histogram_bins(*arrays)

    if before_qc:
        blue_label = f"Raw box panel (min=0, no QC), n={raw_stats['n']:,} team-seasons"
        title_panel = "raw box (no QC)"
    else:
        blue_label = f"Box-QC panel (min=0), n={raw_stats['n']:,} team-seasons"
        title_panel = f"box QC (min=0, keep $\\geq${KEEP_MIN_TEAM_SEASON_GAMES} games)"

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    for ax, weights_norm in zip(axes, (False, True)):
        ax.hist(
            raw_sizes,
            bins=bins,
            color="steelblue",
            alpha=0.82,
            edgecolor="white",
            linewidth=0.4,
            label=blue_label,
            weights=None
            if not weights_norm
            else np.ones_like(raw_sizes, dtype=float) / raw_sizes.size,
        )
        if filtered_sizes is not None and len(filtered_sizes):
            ax.hist(
                filtered_sizes,
                bins=bins,
                color="darkorange",
                alpha=0.55,
                edgecolor="white",
                linewidth=0.4,
                label=(
                    f"Min-{HERO_LOCK:g} drop panel, n={filtered_stats['n']:,} team-seasons"
                    if filtered_stats
                    else "Min-20 drop"
                ),
                weights=None
                if not weights_norm
                else np.ones_like(filtered_sizes, dtype=float) / filtered_sizes.size,
            )
        ax.axvline(
            NCAA_DRESS_CAP,
            color="crimson",
            linestyle="--",
            linewidth=1.8,
            label=f"NCAA dress cap = {NCAA_DRESS_CAP}",
        )
        ax.axvline(
            raw_stats["mean"],
            color="0.35",
            linestyle=":",
            linewidth=1.5,
            label=f"Blue mean = {raw_stats['mean']:.1f}",
        )
        ax.set_xlabel("Players per team-season (box panel row count)")
        ax.set_ylabel("Team-season count" if not weights_norm else "Share of team-seasons")
        ax.set_title("Counts" if not weights_norm else "Normalized")
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    fig.suptitle(
        f"PD22 — roster size: {title_panel} vs min-{HERO_LOCK:g} drop · {seasons} · "
        f"blue median={raw_stats['median']:.0f}, mean={raw_stats['mean']:.1f}, "
        f"{100 * raw_stats['share_eq_15']:.1f}% exactly 15",
        fontsize=11,
        y=1.03,
    )
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths(*, before_qc: bool) -> dict[str, Path]:
    stem = _stem(before_qc=before_qc)
    csv_base = stem.replace("distribution", "by_team_season")
    return {
        "png": OUT / f"{stem}.png",
        "json": OUT / f"{stem}.json",
        "csv": OUT / f"{csv_base}.csv",
    }


def run(*, before_qc: bool, write_csv: bool = True) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths(before_qc=before_qc)

    raw_panel = _load_panel(min_minutes=0.0, before_qc=before_qc)
    filtered_panel = _load_panel(min_minutes=HERO_LOCK, before_qc=before_qc)

    raw_roster = _roster_table(raw_panel)
    filt_roster = _roster_table(filtered_panel)

    raw_sizes = raw_roster["roster_n"].to_numpy(dtype=int)
    filt_sizes = filt_roster["roster_n"].to_numpy(dtype=int)
    raw_stats = _summary(raw_sizes)
    filt_stats = _summary(filt_sizes)

    _plot(
        raw_sizes,
        filt_sizes,
        raw_stats=raw_stats,
        filtered_stats=filt_stats,
        png_path=paths["png"],
        before_qc=before_qc,
    )

    tag = "legacy_raw_min0" if before_qc else "box_qc_min0"
    if write_csv:
        raw_roster.assign(panel=tag).to_csv(
            paths["csv"].with_name(paths["csv"].name.replace(".csv", "_raw.csv")),
            index=False,
        )
        filt_roster.assign(panel=f"min_{int(HERO_LOCK)}_drop").to_csv(
            paths["csv"].with_name(paths["csv"].name.replace(".csv", "_min20.csv")),
            index=False,
        )

    meta = {
        "diagnostic": "pd22_raw_roster_size_distribution_before_qc"
        if before_qc
        else "pd22_raw_roster_size_distribution_after_qc",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "before_box_qc": before_qc,
        "ncaa_dress_cap_reference": NCAA_DRESS_CAP,
        "raw_panel_spec": (
            "panel_rebuild min_minutes=0; QC off (legacy raw box)"
            if before_qc
            else f"panel_rebuild min_minutes=0; box QC on (keep >={KEEP_MIN_TEAM_SEASON_GAMES} games)"
        ),
        "filtered_panel_spec": f"panel_rebuild min_minutes={HERO_LOCK:g}; same QC policy",
        "raw_team_season_summary": raw_stats,
        "filtered_team_season_summary": filt_stats,
        "player_seasons_raw": int(raw_sizes.sum()),
        "player_seasons_filtered": int(filt_sizes.sum()),
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    label = "before QC (legacy raw)" if before_qc else "after box QC"
    print(f"\n[{label}] min=0 panel: {raw_stats['n']:,} team-seasons", flush=True)
    print(
        f"  mean={raw_stats['mean']:.2f} median={raw_stats['median']:.0f} "
        f"min={raw_stats['min']} max={raw_stats['max']}",
        flush=True,
    )
    print(f"\nMin-{HERO_LOCK:g} drop: {filt_stats['n']:,} team-seasons", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only(*, before_qc: bool) -> None:
    paths = _artifact_paths(before_qc=before_qc)
    if not paths["json"].is_file():
        raise SystemExit(f"Missing JSON — run full diagnostic first: {paths['json']}")
    meta = json.loads(paths["json"].read_text(encoding="utf-8"))
    raw_csv = paths["csv"].with_name(paths["csv"].name.replace(".csv", "_raw.csv"))
    filt_csv = paths["csv"].with_name(paths["csv"].name.replace(".csv", "_min20.csv"))
    if not raw_csv.is_file() or not filt_csv.is_file():
        raise SystemExit("Missing roster CSVs — run full diagnostic first.")
    raw_sizes = pd.read_csv(raw_csv)["roster_n"].to_numpy(dtype=int)
    filt_sizes = pd.read_csv(filt_csv)["roster_n"].to_numpy(dtype=int)
    _plot(
        raw_sizes,
        filt_sizes,
        raw_stats=meta["raw_team_season_summary"],
        filtered_stats=meta["filtered_team_season_summary"],
        png_path=paths["png"],
        before_qc=before_qc,
    )
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before-qc-only", action="store_true", help="Legacy raw box only")
    parser.add_argument("--after-qc-only", action="store_true", help="Default box QC only")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV/JSON")
    args = parser.parse_args()

    do_before = args.before_qc_only or (not args.before_qc_only and not args.after_qc_only)
    do_after = args.after_qc_only or (not args.before_qc_only and not args.after_qc_only)

    if args.plot_only:
        if do_before:
            plot_only(before_qc=True)
        if do_after:
            plot_only(before_qc=False)
        return

    if do_before:
        run(before_qc=True)
    if do_after:
        run(before_qc=False)


if __name__ == "__main__":
    main()
