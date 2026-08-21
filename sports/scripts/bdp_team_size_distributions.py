#!/usr/bin/env python3
"""BDP — Team roster size $|T_j|$ distribution (empirical only).

Histogram of players per team-season after each BDP filter chain.

Run (repo root):
  python sports/scripts/bdp_team_size_distributions.py
  python sports/scripts/bdp_team_size_distributions.py --spec "mg10 min20 11_21"

Outputs: ``HEROs_and_PASSes/basic_data_plots/BDP_team_size_<spec>.png`` (+ JSON).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from bdp_ai_tj_distributions import (
    DEFAULT_SPECS,
    DFT_OVERLAY_COLOR,
    Y_HEADROOM,
    BdpSpec,
    _apply_dft,
    _drafted_team_ids,
    _pipeline_config,
    draw_stats_box,
    parse_bdp_spec,
    subtitle_lines,
)
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs

BAR_COLOR = "steelblue"
BAR_ALPHA = 0.85


def _prepare_roster_panel(spec: BdpSpec) -> pd.DataFrame:
    """Player-season rows after BDP filters — no perf / BPM requirement."""
    sys.path.insert(0, str(REPO / "sports"))
    from sports_pipeline import conductor

    drafted_teams: set | None = None
    if spec.dft:
        cfg0 = _pipeline_config(spec, "ppm", min_minutes=0.0)
        raw = conductor.prepare_panel(cfg0)
        drafted_teams = _drafted_team_ids(raw.dropna(subset=["team_id", "season"]))

    build_min = 0.0 if spec.dft else None
    cfg = _pipeline_config(spec, "ppm", min_minutes=build_min)
    panel = conductor.prepare_panel(cfg)
    if spec.dft and drafted_teams is not None:
        panel = _apply_dft(panel, drafted_teams)
    use = panel.dropna(subset=["team_id", "season"]).copy()
    mm = float(spec.min_minutes)
    if mm > 0 and "minutes" in use.columns:
        use = use.loc[pd.to_numeric(use["minutes"], errors="coerce") >= mm]
    return use


def _roster_sizes(panel: pd.DataFrame) -> np.ndarray:
    roster = (
        panel.groupby(["team_id", "season"], observed=True)
        .agg(roster_n=("athlete_id", "size"))
        .reset_index()
    )
    return roster["roster_n"].to_numpy(dtype=int)


def _summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=int)
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": int(v.min()),
        "max": int(v.max()),
        "median": float(np.median(v)),
        "n_ge_60": int((v >= 60).sum()),
    }


def _histogram_bins(*arrays: np.ndarray) -> np.ndarray:
    pooled = np.concatenate([np.asarray(a, dtype=int) for a in arrays])
    lo, hi = int(pooled.min()), int(pooled.max())
    return np.arange(lo - 0.5, hi + 1.5, 1.0)


def _min_filter_label(spec: BdpSpec) -> str:
    if spec.min_minutes > 0:
        return rf"$\geq {spec.min_minutes:g}$ min"
    return "no min filter"


def build_figure(
    spec: BdpSpec,
    sizes: np.ndarray,
    png: Path,
    *,
    sizes_dft: np.ndarray | None = None,
    figsize: tuple[float, float] = (6.8, 6.5),
) -> dict:
    stats = _summary(sizes)
    bins = _histogram_bins(sizes) if sizes_dft is None else _histogram_bins(sizes, sizes_dft)
    centers = 0.5 * (bins[:-1] + bins[1:])
    bin_width = bins[1] - bins[0]

    fig, ax = plt.subplots(figsize=figsize)
    counts, _ = np.histogram(sizes, bins=bins)
    ax.bar(
        centers,
        counts,
        width=bin_width * 0.98,
        align="center",
        color=BAR_COLOR,
        alpha=BAR_ALPHA,
        edgecolor="white",
        linewidth=0.4,
        label=rf"without DFT ($n={stats['n']:,}$)",
    )

    counts_dft: np.ndarray | None = None
    stats_dft: dict | None = None
    if sizes_dft is not None:
        counts_dft, _ = np.histogram(sizes_dft, bins=bins)
        stats_dft = _summary(sizes_dft)
        ax.plot(
            centers,
            counts_dft,
            color=DFT_OVERLAY_COLOR,
            linewidth=2.0,
            marker="o",
            markersize=3,
            label=rf"+ DFT ($n={stats_dft['n']:,}$)",
        )

    peak = int(counts.max())
    if counts_dft is not None:
        peak = max(peak, int(counts_dft.max()))
    ax.set_ylim(0, peak * Y_HEADROOM)

    ax.set_xlabel(rf"Players per team-season ($|T_j|$, {_min_filter_label(spec)})")
    ax.set_ylabel("Team-season count")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    draw_stats_box(ax, stats, stats_dft, decimals=1, include_max=True)

    has_overlay = sizes_dft is not None
    if has_overlay:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.02),
            ncol=2,
            fontsize=8,
            framealpha=0.95,
        )
        bottom = 0.10
    else:
        ax.legend(loc="upper right", fontsize=9)
        bottom = 0.06

    fig.suptitle(
        rf"BDP $|T_j|$ roster sizes",
        fontsize=12,
        y=0.995,
    )
    sub1, sub2 = subtitle_lines(spec, has_overlay=has_overlay)
    fig.text(0.5, 0.962, sub1, ha="center", va="top", fontsize=9, color="0.25")
    fig.text(0.5, 0.947, sub2, ha="center", va="top", fontsize=9, color="0.25")

    fig.tight_layout(rect=(0, bottom, 1, 0.925))
    fig.savefig(png, dpi=150)
    plt.close(fig)
    print(f"Wrote {png.relative_to(REPO)}")
    out = {"without_dft": stats}
    if stats_dft is not None:
        out["dft_overlay"] = stats_dft
    return out


def run_spec(
    spec: BdpSpec,
    *,
    overlay_dft: bool = True,
    figsize: tuple[float, float] = (6.8, 6.5),
    out_png: Path | None = None,
) -> Path:
    ensure_hero_dirs()
    stem = f"BDP_team_size_{spec.slug}"
    out_png = out_png or (BASIC_DATA_PLOTS / f"{stem}.png")
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"

    panel = _prepare_roster_panel(spec)
    sizes = _roster_sizes(panel)

    sizes_dft: np.ndarray | None = None
    dft_panel_n: int | None = None
    if overlay_dft and not spec.dft:
        panel_dft = _prepare_roster_panel(replace(spec, dft=True))
        sizes_dft = _roster_sizes(panel_dft)
        dft_panel_n = int(len(panel_dft))

    fig_stats = build_figure(
        spec, sizes, out_png, sizes_dft=sizes_dft, figsize=figsize
    )

    meta = {
        "diagnostic": "bdp_team_size_distributions",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "seasons": f"{spec.season_min}-{spec.season_max}",
        "qc": "drop_dash_placeholder_names=True",
        "min_team_season_games": spec.min_team_season_games,
        "min_minutes": spec.min_minutes,
        "dft": spec.dft,
        "overlay_dft": overlay_dft and not spec.dft,
        "team_season_summary": fig_stats["without_dft"],
        "player_seasons": int(sizes.sum()),
        "png": out_png.name,
    }
    if "dft_overlay" in fig_stats:
        meta["dft_overlay"] = {
            "team_season_summary": fig_stats["dft_overlay"],
            "player_seasons": int(sizes_dft.sum()) if sizes_dft is not None else None,
            "n_player_season_rows": dft_panel_n,
        }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    s = fig_stats["without_dft"]
    msg = (
        f"  {spec.label}: team_seasons={s['n']:,} mean={s['mean']:.2f} "
        f"median={s['median']:.0f} max={s['max']}"
    )
    if "dft_overlay" in fig_stats:
        sd = fig_stats["dft_overlay"]
        msg += f"  |  +DFT team_seasons={sd['n']:,} max={sd['max']}"
    print(msg)
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="BDP team roster size |T_j| histograms.")
    parser.add_argument(
        "--overlay-dft",
        action="store_true",
        default=True,
        help="Overlay orange +DFT line on blue bars (default: on).",
    )
    parser.add_argument(
        "--no-overlay-dft",
        action="store_false",
        dest="overlay_dft",
        help="Disable +DFT orange overlay.",
    )
    parser.add_argument(
        "--spec",
        action="append",
        dest="specs",
        help=f"BDP filter chain (default: {DEFAULT_SPECS}).",
    )
    parser.add_argument(
        "--fig-height",
        type=float,
        default=6.5,
        help="Figure height in inches (default: 6.5).",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output PNG filename under basic_data_plots/ (e.g. test_team_size.png).",
    )
    args = parser.parse_args()
    specs = [parse_bdp_spec(s) for s in (args.specs or DEFAULT_SPECS)]
    figsize = (6.8, args.fig_height)
    out_png = (BASIC_DATA_PLOTS / args.out) if args.out else None
    for spec in specs:
        print(f"\n=== {spec.label} ===")
        run_spec(
            spec,
            overlay_dft=args.overlay_dft,
            figsize=figsize,
            out_png=out_png if (out_png and len(specs) == 1) else None,
        )
    print("\nDone.")


if __name__ == "__main__":
    main()
