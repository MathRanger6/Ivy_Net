#!/usr/bin/env python3
"""BDP — APGMS / ARGMS / season minutes side-by-side (player + team-mean panels).

**APGMS** — season total minutes / games with minutes > 0.
**ARGMS** — season total minutes / games rostered (incl. DNP).
**season_minutes** — player-season total minutes; team panel = mean player total on roster.

Run (repo root):
  python sports/scripts/bdp_apgms_argms_distributions.py
  python sports/scripts/bdp_apgms_argms_distributions.py --spec "mg10 min1 11_21"
  python sports/scripts/bdp_apgms_argms_distributions.py --metric season_minutes

Use **min1** (not min0 + clip) to drop zero-minute player-seasons — filenames and subtitles stay aligned.
Integer ESPN minutes ⇒ min1 ≡ drop zero-min only.

Outputs:
  ``basic_data_plots/BDP_APGMS_mg10_min1_11_21.png`` (+ JSON)
  ``basic_data_plots/BDP_ARGMS_mg10_min1_11_21.png`` (+ JSON)
  ``basic_data_plots/BDP_season_minutes_mg10_min1_11_21.png`` (+ JSON)
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
    BAR_ALPHA,
    DFT_OVERLAY_COLOR,
    N_BINS,
    Y_HEADROOM,
    BdpSpec,
    _apply_dft,
    _drafted_team_ids,
    _histogram_edges,
    _pipeline_config,
    _summary,
    draw_stats_box,
    parse_bdp_spec,
    subtitle_lines,
)
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs

BAR_COLOR = "steelblue"
PLAYER_BAR_COLOR = "seagreen"
TEAM_BAR_COLOR = "steelblue"
DEFAULT_SPEC = "mg10 min1 11_21"

METRICS = {
    "apgms": {
        "col": "apgms",
        "team_col": "T_apgms",
        "title_short": "APGMS",
        "player_title": r"APGMS — avg minutes per played game ($n={n:,}$)",
        "team_title": r"mean team APGMS — $\overline{{\mathrm{{APGMS}}}}_j$ ($n={n:,}$ team-seasons)",
        "xlabel": "Minutes per played game (season avg)",
    },
    "argms": {
        "col": "argms",
        "team_col": "T_argms",
        "title_short": "ARGMS",
        "player_title": r"ARGMS — avg minutes per rostered game ($n={n:,}$)",
        "team_title": r"mean team ARGMS — $\overline{{\mathrm{{ARGMS}}}}_j$ ($n={n:,}$ team-seasons)",
        "xlabel": "Minutes per rostered game (season avg)",
    },
    "season_minutes": {
        "col": "minutes",
        "team_col": "T_season_minutes",
        "title_short": "season_minutes",
        "player_title": r"Total season minutes — player ($n={n:,}$)",
        "team_title": r"Mean player total season minutes — $\overline{{M}}_j$ ($n={n:,}$ team-seasons)",
        "xlabel": "Total season minutes (player-season)",
    },
}


def _prepare_panel(spec: BdpSpec, *, need_cols: tuple[str, ...] = ("apgms", "argms")) -> pd.DataFrame:
    """Player-season panel; min0 build unless DFT overlay path."""
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
    for c in need_cols:
        if c not in use.columns:
            raise RuntimeError(
                f"Panel missing {c!r} — rebuild after panel_rebuild.py update."
            )
    mm = float(spec.min_minutes)
    if mm > 0 and "minutes" in use.columns:
        use = use.loc[pd.to_numeric(use["minutes"], errors="coerce") >= mm]
    return use


def _attach_team_means(panel: pd.DataFrame) -> pd.DataFrame:
    """Add T_apgms / T_argms (mean player metric within team-season)."""
    out = panel.copy()
    team = (
        out.groupby(["team_id", "season"], observed=True)
        .agg(
            T_apgms=("apgms", "mean"),
            T_argms=("argms", "mean"),
            T_season_minutes=("minutes", "mean"),
        )
        .reset_index()
    )
    return out.merge(team, on=["team_id", "season"], how="left")


def _team_values(panel: pd.DataFrame, team_col: str) -> np.ndarray:
    team_df = (
        panel.groupby(["team_id", "season"], observed=True)
        .agg(val=(team_col, "first"))
        .reset_index()
    )
    return team_df["val"].to_numpy(dtype=float)


def build_figure(
    spec: BdpSpec,
    metric_key: str,
    player: np.ndarray,
    team: np.ndarray,
    png: Path,
    *,
    player_dft: np.ndarray | None = None,
    team_dft: np.ndarray | None = None,
    figsize: tuple[float, float] = (10.5, 6.5),
) -> None:
    meta = METRICS[metric_key]
    pool = [player, team]
    if player_dft is not None and team_dft is not None:
        pool.extend([player_dft, team_dft])
    edges = _histogram_edges(*pool, n_bins=N_BINS)
    centers = 0.5 * (edges[:-1] + edges[1:])
    bin_width = edges[1] - edges[0]

    fig, axes = plt.subplots(1, 2, figsize=figsize, sharex=True)
    bar_colors = (
        (PLAYER_BAR_COLOR, TEAM_BAR_COLOR)
        if metric_key in ("apgms", "argms")
        else (BAR_COLOR, BAR_COLOR)
    )
    panels = [
        (axes[0], player, player_dft, meta["player_title"].format(n=player.size), bar_colors[0]),
        (axes[1], team, team_dft, meta["team_title"].format(n=team.size), bar_colors[1]),
    ]

    legend_handles = legend_labels = None
    for ax, values, values_dft, title, bar_color in panels:
        counts, _ = np.histogram(values, bins=edges)
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=bar_color,
            alpha=BAR_ALPHA,
            edgecolor=bar_color,
            linewidth=0.3,
            label="without DFT",
        )
        counts_dft = None
        if values_dft is not None:
            counts_dft, _ = np.histogram(values_dft, bins=edges)
            ax.plot(
                centers,
                counts_dft,
                color=DFT_OVERLAY_COLOR,
                linewidth=2.0,
                marker="o",
                markersize=3,
                label=rf"+ DFT ($n={values_dft.size:,}$)",
            )
        peak = int(counts.max())
        if counts_dft is not None:
            peak = max(peak, int(counts_dft.max()))
        ax.set_ylim(0, peak * Y_HEADROOM)
        ax.set_xlabel(meta["xlabel"], fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(title, fontsize=11, pad=6)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        if legend_handles is None:
            legend_handles, legend_labels = ax.get_legend_handles_labels()
        draw_stats_box(ax, _summary(values), _summary(values_dft) if values_dft is not None else None)

    has_overlay = player_dft is not None
    if legend_handles and has_overlay:
        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.02),
            ncol=2,
            fontsize=8,
            framealpha=0.95,
        )
        bottom = 0.10
    else:
        axes[0].legend(loc="lower right", fontsize=8, framealpha=0.92)
        bottom = 0.06

    fig.suptitle(
        rf"BDP — {meta['title_short'].replace('_', ' ')} (player + team mean)",
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


def run_spec(
    spec: BdpSpec,
    metric_key: str,
    *,
    overlay_dft: bool = True,
    figsize: tuple[float, float] = (10.5, 6.5),
) -> Path:
    ensure_hero_dirs()
    meta = METRICS[metric_key]
    stem = f"BDP_{meta['title_short']}_{spec.slug}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_json = BASIC_DATA_PLOTS / f"{stem}.json"

    need = ("minutes", "apgms", "argms")
    panel = _attach_team_means(_prepare_panel(spec, need_cols=need))
    col = meta["col"]
    team_col = meta["team_col"]

    player = panel[col].to_numpy(dtype=float)
    player = player[np.isfinite(player)]
    team = _team_values(panel, team_col)
    team = team[np.isfinite(team)]

    player_dft = team_dft = None
    dft_panel_n: int | None = None
    if overlay_dft and not spec.dft:
        panel_dft = _attach_team_means(
            _prepare_panel(replace(spec, dft=True), need_cols=need)
        )
        dft_panel_n = int(len(panel_dft))
        player_dft = panel_dft[col].to_numpy(dtype=float)
        player_dft = player_dft[np.isfinite(player_dft)]
        team_dft = _team_values(panel_dft, team_col)
        team_dft = team_dft[np.isfinite(team_dft)]

    build_figure(
        spec,
        metric_key,
        player,
        team,
        out_png,
        player_dft=player_dft,
        team_dft=team_dft,
        figsize=figsize,
    )

    payload = {
        "diagnostic": f"bdp_{metric_key}_distributions",
        "date": date.today().isoformat(),
        "metric": metric_key,
        "definitions": {
            "apgms": "season minutes / games with minutes > 0",
            "argms": "season minutes / games rostered (incl. DNP)",
            "season_minutes": "player-season cumulative ESPN box minutes",
            "team_mean": "mean of player-season values within (team_id, season)",
        },
        "bdp_spec": spec.label,
        "seasons": f"{spec.season_min}-{spec.season_max}",
        "player": _summary(player),
        "team_mean": _summary(team),
        "overlay_dft": overlay_dft and not spec.dft,
        "png": out_png.name,
    }
    if player_dft is not None:
        payload["dft_overlay"] = {
            "player": _summary(player_dft),
            "team_mean": _summary(team_dft),
            "n_player_season_rows": dft_panel_n,
        }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="BDP APGMS / ARGMS histograms.")
    parser.add_argument("--spec", default=DEFAULT_SPEC, help=f"BDP chain (default: {DEFAULT_SPEC}).")
    parser.add_argument(
        "--metric",
        choices=["apgms", "argms", "season_minutes", "both", "all"],
        default="both",
        help="Which figures: both=APGMS+ARGMS; all=+season_minutes.",
    )
    parser.add_argument(
        "--overlay-dft",
        action="store_true",
        default=True,
        help="Orange +DFT line overlay (default: on).",
    )
    parser.add_argument(
        "--no-overlay-dft",
        action="store_false",
        dest="overlay_dft",
    )
    parser.add_argument("--fig-height", type=float, default=6.5)
    args = parser.parse_args()
    spec = parse_bdp_spec(args.spec)
    figsize = (10.5, args.fig_height)
    if args.metric == "both":
        keys = ["apgms", "argms"]
    elif args.metric == "all":
        keys = ["apgms", "argms", "season_minutes"]
    else:
        keys = [args.metric]
    for key in keys:
        print(f"\n=== {key.upper()} · {spec.label} ===")
        run_spec(
            spec,
            key,
            overlay_dft=args.overlay_dft,
            figsize=figsize,
        )
    print("\nDone.")


if __name__ == "__main__":
    main()
