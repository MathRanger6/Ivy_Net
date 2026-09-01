#!/usr/bin/env python3
"""BDP — team games and season-minutes exposure (reigning hero / BDP porch).

1. Team-season game counts (PD22 slide-27 style: linear + log-y panels).
2. Player season-minutes vs team-average season-minutes (side-by-side).

Run (repo root):
  python sports/scripts/bdp_reigning_exposure_plots.py --spec "mg10 min20 09_21"
  python sports/scripts/bdp_reigning_exposure_plots.py --spec "mg10 min20 09_21" --only team_games
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

from bdp_ai_tj_distributions import (  # noqa: E402
    DFT_OVERLAY_COLOR,
    BdpSpec,
    parse_bdp_spec,
    subtitle_lines,
)
from bdp_team_size_distributions import _prepare_roster_panel  # noqa: E402
from gallery_mathtext import configure_matplotlib_mathtext  # noqa: E402
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs  # noqa: E402

BOX_USECOLS = [
    "game_id",
    "athlete_id",
    "season",
    "team_id",
    "team_short_display_name",
    "athlete_display_name",
]


def _games_summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=int)
    if len(v) == 0:
        return {"n_team_seasons": 0}
    out = {
        "n_team_seasons": int(v.size),
        "games_n_min": int(v.min()),
        "games_n_max": int(v.max()),
        "games_n_median": float(np.median(v)),
        "games_n_mean": float(v.mean()),
        "n_with_1_game": int((v == 1).sum()),
        "pct_with_1_game": float((v == 1).mean()),
    }
    mg = 10
    out[f"n_with_{mg}_or_fewer"] = int((v <= mg).sum())
    out["n_with_ge_20_games"] = int((v >= 20).sum())
    return out


def _minutes_summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return {"n": 0}
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
        "median": float(np.median(v)),
        "p25": float(np.percentile(v, 25)),
        "p75": float(np.percentile(v, 75)),
        "p90": float(np.percentile(v, 90)),
    }


def _load_box_rows(spec: BdpSpec) -> tuple[pd.DataFrame, object]:
    sys.path.insert(0, str(REPO / "sports"))
    from sports_pipeline import paths
    from sports_pipeline.panel_rebuild import _apply_box_qc

    box_path = paths.player_box_csv()
    if not box_path.is_file():
        raise FileNotFoundError(f"Missing player box: {box_path}")

    df_g = pd.read_csv(box_path, usecols=BOX_USECOLS, low_memory=False)
    for c in ["athlete_id", "season", "team_id"]:
        df_g[c] = pd.to_numeric(df_g[c], errors="coerce")
    df_g = df_g.dropna(subset=["athlete_id", "season", "team_id"])
    df_g["season"] = df_g["season"].astype(int)
    df_g = df_g.loc[
        (df_g["season"] >= spec.season_min) & (df_g["season"] <= spec.season_max)
    ].copy()
    return df_g, _apply_box_qc


def _games_table(df_g: pd.DataFrame) -> pd.DataFrame:
    return (
        df_g.groupby(["team_id", "season"], observed=True)["game_id"]
        .nunique()
        .rename("games_n")
        .reset_index()
        .sort_values(["season", "team_id"])
    )


def _plot_team_games(
    games_n: np.ndarray,
    *,
    stats: dict,
    spec: BdpSpec,
    png_path: Path,
    after_qc: bool,
) -> None:
    configure_matplotlib_mathtext()
    bins = np.arange(games_n.min() - 0.5, games_n.max() + 1.5, 1.0)
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    qc_note = (
        f"after box QC (keep $\\geq${spec.min_team_season_games + 1} games)"
        if after_qc
        else "raw box (no QC)"
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
    for ax, log_y in zip(axes, (False, True)):
        weights = None if not log_y else np.ones_like(games_n, dtype=float) / games_n.size
        ax.hist(
            games_n,
            bins=bins,
            color="steelblue",
            alpha=0.82,
            edgecolor="white",
            linewidth=0.4,
            weights=weights,
        )
        if after_qc and spec.min_team_season_games > 0:
            thr = float(spec.min_team_season_games + 1)
            ax.axvline(
                thr,
                color="crimson",
                linestyle="--",
                linewidth=1.8,
                label=rf"Keep $\geq${thr:.0f} games",
            )
        elif not after_qc and stats.get("n_with_1_game", 0):
            ax.axvline(
                1.0,
                color="crimson",
                linestyle="--",
                linewidth=1.8,
                label=rf"1 game (n={int(stats['n_with_1_game']):,})",
            )
        ax.axvline(
            stats["games_n_median"],
            color="0.35",
            linestyle=":",
            linewidth=1.5,
            label=rf"Median = {stats['games_n_median']:.0f}",
        )
        ax.set_xlabel("Games per team-season (distinct game_id)")
        ax.set_ylabel("Team-season count" if not log_y else "Share of team-seasons")
        ax.set_title("Counts" if not log_y else "Normalized (log y)")
        if log_y:
            ax.set_yscale("log")
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    fig.suptitle(
        rf"Team-season game counts · {qc_note} · "
        rf"$n={stats['n_team_seasons']:,}$, median={stats['games_n_median']:.0f}",
        fontsize=11,
        y=1.03,
    )
    fig.text(0.5, 0.01, f"{line1}\n{line2}", ha="center", va="bottom", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_team_games(
    spec: BdpSpec,
    *,
    out_png: Path,
    out_meta_dir: Path,
    prefix: str = "REIGNING",
    raw_box: bool = False,
) -> Path:
    """Game counts per team-season — PD22 slide-27 style (default: after box QC)."""
    from sports_pipeline.config import PipelineConfig

    df_g, apply_qc = _load_box_rows(spec)
    qc_report: dict | None = None
    after_qc = not raw_box

    if after_qc:
        cfg = PipelineConfig(
            panel_season_min=spec.season_min,
            panel_season_max=spec.season_max,
            drop_dash_placeholder_names=True,
            min_team_season_games=spec.min_team_season_games,
        )
        df_g, qc_report = apply_qc(df_g, cfg)

    table = _games_table(df_g)
    games_n = table["games_n"].to_numpy(dtype=int)
    stats = _games_summary(games_n)

    stem = f"{prefix}_BDP_team_games_{spec.slug}"
    if raw_box:
        stem += "_raw"
    out_png = out_png.parent / f"{stem}.png"
    out_csv = out_meta_dir / f"{stem}_team_season.csv"
    out_meta = out_meta_dir / f"{stem}.json"

    out_meta_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_csv, index=False)
    _plot_team_games(games_n, stats=stats, spec=spec, png_path=out_png, after_qc=after_qc)

    meta = {
        "diagnostic": "bdp_team_season_games",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "seasons": f"{spec.season_min}-{spec.season_max}",
        "after_box_qc": after_qc,
        "panel_rows": "team-season (box)",
        "hand_analog": "PD22 memo slide 27",
        **stats,
        "outputs": {"png": out_png.name, "team_csv": out_csv.name},
    }
    if qc_report:
        meta["box_qc_report"] = {
            k: qc_report[k]
            for k in (
                "dash_rows_dropped",
                "team_seasons_dropped_low_games",
                "box_rows_dropped_low_games",
                "box_rows_after_qc",
            )
            if k in qc_report
        }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def _team_mean_minutes(panel: pd.DataFrame) -> np.ndarray:
    work = panel.copy()
    work["minutes"] = pd.to_numeric(work["minutes"], errors="coerce")
    work = work.dropna(subset=["minutes", "team_id", "season"])
    team = (
        work.groupby(["team_id", "season"], observed=True)["minutes"]
        .mean()
        .reset_index(name="team_mean_minutes")
    )
    return team["team_mean_minutes"].to_numpy(dtype=float)


def _plot_ecdf(ax, values: np.ndarray, *, color: str = "steelblue", lw: float = 1.8, label: str | None = None) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=lw, label=label)


def _plot_dft_count_line(
    ax,
    values_dft: np.ndarray,
    bins: np.ndarray,
    *,
    label: str,
) -> None:
    counts_dft, _ = np.histogram(values_dft, bins=bins)
    centers = 0.5 * (bins[:-1] + bins[1:])
    ax.plot(
        centers,
        counts_dft,
        color=DFT_OVERLAY_COLOR,
        linewidth=2.0,
        marker="o",
        markersize=2.5,
        label=label,
    )


def _stats_column_lines(stats: dict, title: str, *, col_w: int = 11) -> list[str]:
    return [
        title.rjust(col_w),
        f"n={stats['n']:,}".rjust(col_w),
        f"med={stats['median']:.0f}".rjust(col_w),
        f"μ={stats['mean']:.0f}".rjust(col_w),
        f"σ={stats['std']:.0f}".rjust(col_w),
    ]


def _minutes_stats_box_text(stats: dict, *, stats_dft: dict | None = None, col_w: int = 11) -> str:
    """Two-column w/o DFT | + DFT layout; each column right-aligned."""
    if stats_dft is None:
        return "\n".join(_stats_column_lines(stats, "", col_w=col_w))
    left = _stats_column_lines(stats, "w/o DFT", col_w=col_w)
    right = _stats_column_lines(stats_dft, "+ DFT", col_w=col_w)
    gap = " " * 3
    return "\n".join(f"{l}{gap}{r}" for l, r in zip(left, right))


def _annotate_minutes_stats(
    ax,
    stats: dict,
    *,
    stats_dft: dict | None = None,
    loc: str = "upper left",
) -> None:
    ha = "left" if "left" in loc else "right"
    x = 0.03 if ha == "left" else 0.97
    ax.text(
        x,
        0.97,
        _minutes_stats_box_text(stats, stats_dft=stats_dft),
        transform=ax.transAxes,
        va="top",
        ha=ha,
        fontsize=8,
        linespacing=1.15,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.92, edgecolor="0.8"),
    )


def _add_log_y_inset(
    ax,
    values: np.ndarray,
    *,
    floor_min: float,
    values_dft: np.ndarray | None = None,
    x_hi: float = 200.0,
) -> None:
    """Zoom inset for the low-minute pile-up (log-y counts)."""
    inset = ax.inset_axes([0.54, 0.44, 0.44, 0.52])
    inset_bins = np.arange(0, x_hi + 5, 5)
    inset.hist(
        values,
        bins=inset_bins,
        color="steelblue",
        alpha=0.9,
        edgecolor="white",
        linewidth=0.3,
    )
    if values_dft is not None and values_dft.size:
        _plot_dft_count_line(
            inset,
            values_dft,
            inset_bins,
            label=rf"+ DFT ($n={values_dft.size:,}$)",
        )
    inset.set_yscale("log")
    inset.set_xlim(0, x_hi)
    inset.set_title(r"log $y$ · minutes $\leq$ 200", fontsize=7, pad=2)
    inset.tick_params(labelsize=6)
    inset.grid(axis="y", alpha=0.3, linewidth=0.4)
    if floor_min > 0:
        inset.axvline(floor_min, color="crimson", linestyle="--", linewidth=1.2)


def _plot_minutes_dual(
    player_min: np.ndarray,
    team_mean_min: np.ndarray,
    *,
    player_stats: dict,
    team_stats: dict,
    spec: BdpSpec,
    png_path: Path,
    player_min_dft: np.ndarray | None = None,
    team_mean_dft: np.ndarray | None = None,
    player_stats_dft: dict | None = None,
    team_stats_dft: dict | None = None,
) -> None:
    configure_matplotlib_mathtext()
    has_overlay = player_min_dft is not None and player_min_dft.size > 0
    line1, line2 = subtitle_lines(spec, has_overlay=has_overlay)
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.2))
    fig.subplots_adjust(hspace=0.42, wspace=0.28, top=0.91, bottom=0.09)

    p99 = float(np.percentile(player_min, 99)) if len(player_min) else 1100.0
    if has_overlay and player_min_dft is not None and player_min_dft.size:
        p99 = max(p99, float(np.percentile(player_min_dft, 99)))
    player_hi = max(p99 + 50, float(player_min.max()) if len(player_min) else 1100.0)
    if has_overlay and player_min_dft is not None and player_min_dft.size:
        player_hi = max(player_hi, float(player_min_dft.max()))
    player_bins = np.arange(0, player_hi + 25, 25)

    team_lo = float(team_mean_min.min()) if len(team_mean_min) else 0.0
    team_hi = float(team_mean_min.max()) if len(team_mean_min) else 900.0
    if has_overlay and team_mean_dft is not None and team_mean_dft.size:
        team_lo = min(team_lo, float(team_mean_dft.min()))
        team_hi = max(team_hi, float(team_mean_dft.max()))
    team_bins = np.linspace(team_lo, team_hi, 28)

    player_hist_label = (
        rf"without DFT ($n={player_stats['n']:,}$)"
        if has_overlay
        else None
    )
    team_hist_label = (
        rf"without DFT ($n={team_stats['n']:,}$)"
        if has_overlay
        else None
    )

    # Top-left: player histogram + log-y inset
    ax = axes[0, 0]
    ax.hist(
        player_min,
        bins=player_bins,
        color="steelblue",
        alpha=0.85,
        edgecolor="white",
        linewidth=0.35,
        label=player_hist_label,
    )
    if has_overlay and player_min_dft is not None:
        _plot_dft_count_line(
            ax,
            player_min_dft,
            player_bins,
            label=rf"+ DFT ($n={player_stats_dft['n']:,}$)",
        )
    if spec.min_minutes > 0:
        ax.axvline(
            spec.min_minutes,
            color="crimson",
            linestyle="--",
            linewidth=1.6,
            label=rf"Playing-time floor = {spec.min_minutes:g} min",
        )
    ax.axvline(
        player_stats["median"],
        color="0.35",
        linestyle=":",
        linewidth=1.5,
        label=rf"Median = {player_stats['median']:.0f} min",
    )
    ax.set_xlim(0, player_hi)
    ax.set_xlabel("Season minutes per player")
    ax.set_ylabel("Player-season count")
    ax.set_title(
        "Player-season minutes (histogram)\n(post min20 filter — each row $\\geq$ 20 min)",
        fontsize=10,
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    _add_log_y_inset(
        ax,
        player_min,
        floor_min=float(spec.min_minutes),
        values_dft=player_min_dft if has_overlay else None,
    )
    ax.legend(
        fontsize=6,
        loc="lower left",
        bbox_to_anchor=(0.11, 0.80),
        framealpha=0.95,
        borderaxespad=0.1,
    )

    # Top-right: team mean histogram
    ax = axes[0, 1]
    ax.hist(
        team_mean_min,
        bins=team_bins,
        color="steelblue",
        alpha=0.85,
        edgecolor="white",
        linewidth=0.35,
        label=team_hist_label,
    )
    if has_overlay and team_mean_dft is not None:
        _plot_dft_count_line(
            ax,
            team_mean_dft,
            team_bins,
            label=rf"+ DFT ($n={team_stats_dft['n']:,}$)",
        )
    ax.axvline(
        team_stats["median"],
        color="0.35",
        linestyle=":",
        linewidth=1.5,
        label=rf"Median = {team_stats['median']:.0f} min",
    )
    ax.set_xlabel(r"Mean player minutes per team-season ($\overline{\mathrm{min}}_{j}$)")
    ax.set_ylabel("Team-season count")
    ax.set_title(
        r"Team-season mean minutes (histogram)"
        "\n(mean of roster player-minutes, same filtered panel)",
        fontsize=10,
    )
    ax.legend(fontsize=6, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    # Bottom-left: player ECDF
    ax = axes[1, 0]
    _plot_ecdf(
        ax,
        player_min,
        label=rf"without DFT ($n={player_stats['n']:,}$)" if has_overlay else None,
    )
    if has_overlay and player_min_dft is not None:
        _plot_ecdf(
            ax,
            player_min_dft,
            color=DFT_OVERLAY_COLOR,
            label=rf"+ DFT ($n={player_stats_dft['n']:,}$)",
        )
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    if spec.min_minutes > 0:
        ax.axvline(
            spec.min_minutes,
            color="crimson",
            linestyle="--",
            linewidth=1.4,
            label=rf"Floor = {spec.min_minutes:g} min",
        )
    ax.axvline(
        player_stats["median"],
        color="0.35",
        linestyle=":",
        linewidth=1.4,
        label=rf"Median = {player_stats['median']:.0f} min",
    )
    ax.set_xlim(0, player_hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Season minutes per player")
    ax.set_ylabel("ECDF  $F(x)$")
    ax.set_title("Player-season minutes (ECDF)", fontsize=10)
    ax.legend(fontsize=7.5, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.25, linewidth=0.5)
    _annotate_minutes_stats(ax, player_stats, stats_dft=player_stats_dft, loc="upper left")

    # Bottom-right: team ECDF
    ax = axes[1, 1]
    _plot_ecdf(
        ax,
        team_mean_min,
        label=rf"without DFT ($n={team_stats['n']:,}$)" if has_overlay else None,
    )
    if has_overlay and team_mean_dft is not None:
        _plot_ecdf(
            ax,
            team_mean_dft,
            color=DFT_OVERLAY_COLOR,
            label=rf"+ DFT ($n={team_stats_dft['n']:,}$)",
        )
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.axvline(
        team_stats["median"],
        color="0.35",
        linestyle=":",
        linewidth=1.4,
        label=rf"Median = {team_stats['median']:.0f} min",
    )
    ax.set_xlim(team_lo, team_hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Mean player minutes per team-season ($\overline{\mathrm{min}}_{j}$)")
    ax.set_ylabel("ECDF  $F(x)$")
    ax.set_title("Team-season mean minutes (ECDF)", fontsize=10)
    ax.legend(fontsize=8, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.25, linewidth=0.5)
    _annotate_minutes_stats(ax, team_stats, stats_dft=team_stats_dft, loc="upper left")

    fig.suptitle(
        rf"Season minutes exposure · MBB {spec.season_min}–{spec.season_max} · all-ps",
        fontsize=11,
    )
    fig.text(0.5, 0.02, f"{line1} · {line2}", ha="center", va="bottom", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_minutes_dual(
    spec: BdpSpec,
    *,
    out_png: Path,
    out_meta_dir: Path,
    prefix: str = "REIGNING",
    overlay_dft: bool = True,
) -> Path:
    """Player-season minutes and team-average minutes (all-ps, reigning filter chain)."""
    panel = _prepare_roster_panel(spec)
    player_min = pd.to_numeric(panel["minutes"], errors="coerce").dropna().to_numpy(dtype=float)
    team_mean = _team_mean_minutes(panel)
    player_stats = _minutes_summary(player_min)
    team_stats = _minutes_summary(team_mean)

    player_min_dft: np.ndarray | None = None
    team_mean_dft: np.ndarray | None = None
    player_stats_dft: dict | None = None
    team_stats_dft: dict | None = None
    if overlay_dft and not spec.dft:
        panel_dft = _prepare_roster_panel(replace(spec, dft=True))
        player_min_dft = (
            pd.to_numeric(panel_dft["minutes"], errors="coerce").dropna().to_numpy(dtype=float)
        )
        team_mean_dft = _team_mean_minutes(panel_dft)
        player_stats_dft = _minutes_summary(player_min_dft)
        team_stats_dft = _minutes_summary(team_mean_dft)

    stem = f"{prefix}_BDP_minutes_player_team_{spec.slug}"
    out_png = out_png.parent / f"{stem}.png"
    out_meta = out_meta_dir / f"{stem}.json"

    _plot_minutes_dual(
        player_min,
        team_mean,
        player_stats=player_stats,
        team_stats=team_stats,
        spec=spec,
        png_path=out_png,
        player_min_dft=player_min_dft,
        team_mean_dft=team_mean_dft,
        player_stats_dft=player_stats_dft,
        team_stats_dft=team_stats_dft,
    )

    meta = {
        "diagnostic": "bdp_minutes_player_team_dual",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "seasons": f"{spec.season_min}-{spec.season_max}",
        "panel_rows": "all-ps",
        "overlay_dft": overlay_dft and not spec.dft,
        "player_season_minutes": player_stats,
        "team_mean_minutes": team_stats,
        "n_player_seasons": int(len(player_min)),
        "n_team_seasons": int(len(team_mean)),
        "outputs": {"png": out_png.name},
    }
    if player_stats_dft is not None:
        meta["player_season_minutes_dft"] = player_stats_dft
        meta["team_mean_minutes_dft"] = team_stats_dft
        meta["n_player_seasons_dft"] = int(len(player_min_dft))
        meta["n_team_seasons_dft"] = int(len(team_mean_dft))
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Team games + minutes exposure BDP plots.")
    parser.add_argument("--spec", default="mg10 min20 09_21")
    parser.add_argument("--prefix", default="BDP")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=("team_games", "minutes", "team_games_raw"),
        help="Subset (default: team_games + minutes).",
    )
    parser.add_argument("--out-dir", type=Path, default=BASIC_DATA_PLOTS)
    parser.add_argument(
        "--raw-games",
        action="store_true",
        help="Also write raw-box team games (slide-27 bimodal; no mg filter).",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    spec = parse_bdp_spec(args.spec)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    keys = args.only or ["team_games", "minutes"]
    if args.raw_games and "team_games_raw" not in keys:
        keys = list(keys) + ["team_games_raw"]

    for key in keys:
        if key == "team_games":
            run_team_games(
                spec,
                out_png=out_dir / "team_games.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
                raw_box=False,
            )
        elif key == "team_games_raw":
            run_team_games(
                spec,
                out_png=out_dir / "team_games_raw.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
                raw_box=True,
            )
        elif key == "minutes":
            run_minutes_dual(
                spec,
                out_png=out_dir / "minutes.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
            )


if __name__ == "__main__":
    main()
