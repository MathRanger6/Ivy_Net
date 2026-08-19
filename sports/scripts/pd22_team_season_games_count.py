#!/usr/bin/env python3
"""PD22 — distinct games per team-season in box data (raw vs after box QC).

Run (repo root):
  python sports/scripts/pd22_team_season_games_count.py
  python sports/scripts/pd22_team_season_games_count.py --after-qc-only
  python sports/scripts/pd22_team_season_games_count.py --raw-only
  python sports/scripts/pd22_team_season_games_count.py --plot-only --after-qc-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_team_season_games_count_2011_2021.{png,json,csv}           # raw box
  PD22_team_season_games_count_after_qc_2011_2021.{png,json,csv}  # after dash + min-games QC
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

OUT = PD22_MINUTES
from pd22_slide_common import MIN_TEAM_SEASON_GAMES

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)


def _w():
    return current_window()

DEFAULT_MIN_GAMES = MIN_TEAM_SEASON_GAMES
BOX_USECOLS = [
    "game_id",
    "athlete_id",
    "season",
    "team_id",
    "team_short_display_name",
    "athlete_display_name",
]


def _load_box_game_rows() -> pd.DataFrame:
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
    df_g = df_g.loc[(df_g["season"] >= _w().season_min) & (df_g["season"] <= _w().season_max)].copy()
    return df_g, _apply_box_qc


def _games_table(df_g: pd.DataFrame) -> pd.DataFrame:
    games = (
        df_g.groupby(["team_id", "season"], observed=True)["game_id"]
        .nunique()
        .rename("games_n")
        .reset_index()
    )
    if "team_short_display_name" in df_g.columns:
        names = (
            df_g.dropna(subset=["team_short_display_name"])
            .groupby("team_id", observed=True)["team_short_display_name"]
            .last()
        )
        games = games.merge(names, on="team_id", how="left")
    return games.sort_values(["season", "team_id"])


def _summary(values: np.ndarray) -> dict:
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
    for k in (3, 5, 10, 15, 20, 30):
        out[f"n_with_{k}_or_fewer"] = int((v <= k).sum())
    out["n_with_ge_20_games"] = int((v >= 20).sum())
    return out


def _plot(
    games_n: np.ndarray,
    *,
    stats: dict,
    png_path: Path,
    title_suffix: str,
    threshold_line: float | None,
    threshold_label: str | None,
) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(_w().season_min, _w().season_max)
    bins = np.arange(games_n.min() - 0.5, games_n.max() + 1.5, 1.0)

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
        if threshold_line is not None:
            ax.axvline(
                threshold_line,
                color="crimson",
                linestyle="--",
                linewidth=1.8,
                label=threshold_label or f"threshold = {threshold_line:g}",
            )
        ax.axvline(
            stats["games_n_median"],
            color="0.35",
            linestyle=":",
            linewidth=1.5,
            label=f"Median = {stats['games_n_median']:.0f}",
        )
        ax.set_xlabel("Games in box data per team-season")
        ax.set_ylabel("Team-season count" if not log_y else "Share of team-seasons")
        ax.set_title("Counts" if not log_y else "Normalized (log y)")
        if log_y:
            ax.set_yscale("log")
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    fig.suptitle(
        f"PD22 — team-season game counts · {title_suffix} · {seasons} · "
        f"n={stats['n_team_seasons']:,}, median={stats['games_n_median']:.0f}",
        fontsize=11,
        y=1.03,
    )
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _stem(*, after_qc: bool) -> str:
    base = f"PD22_team_season_games_count_{_w().tag}"
    return f"PD22_team_season_games_count_after_qc_{_w().tag}" if after_qc else base


def _artifact_paths(*, after_qc: bool) -> dict[str, Path]:
    stem = _stem(after_qc=after_qc)
    return {
        "png": OUT / f"{stem}.png",
        "json": OUT / f"{stem}.json",
        "csv": OUT / f"{stem}.csv",
    }


def _run_one(*, after_qc: bool, write_csv: bool = True) -> dict:
    from sports_pipeline.config import PipelineConfig

    df_g, apply_qc = _load_box_game_rows()
    qc_report: dict | None = None

    if after_qc:
        cfg = PipelineConfig(
            panel_season_min=_w().season_min,
            panel_season_max=_w().season_max,
            drop_dash_placeholder_names=True,
            min_team_season_games=DEFAULT_MIN_GAMES,
        )
        df_g, qc_report = apply_qc(df_g, cfg)
        title_suffix = f"after box QC (keep $\\geq${DEFAULT_MIN_GAMES + 1} games)"
        threshold_line = float(DEFAULT_MIN_GAMES + 1)
        threshold_label = f"Keep threshold = {DEFAULT_MIN_GAMES + 1} games"
    else:
        title_suffix = "raw box (no QC)"
        threshold_line = 1.0
        threshold_label = f"1 game (n={0})"

    table = _games_table(df_g)
    games_n = table["games_n"].to_numpy(dtype=int)
    stats = _summary(games_n)
    if not after_qc:
        threshold_label = f"1 game (n={stats['n_with_1_game']:,})"

    paths = _artifact_paths(after_qc=after_qc)
    _plot(
        games_n,
        stats=stats,
        png_path=paths["png"],
        title_suffix=title_suffix,
        threshold_line=threshold_line,
        threshold_label=threshold_label,
    )

    if write_csv:
        table.to_csv(paths["csv"], index=False)

    meta = {
        "diagnostic": "pd22_team_season_games_count_after_qc"
        if after_qc
        else "pd22_team_season_games_count_raw",
        "date": date.today().isoformat(),
        "season_min": _w().season_min,
        "season_max": _w().season_max,
        "seasons": seasons_label(_w().season_min, _w().season_max),
        "after_box_qc": after_qc,
        **stats,
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
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    label = "after QC" if after_qc else "raw"
    print(f"\n[{label}] {stats['n_team_seasons']:,} team-seasons", flush=True)
    print(
        f"  games_n min={stats['games_n_min']} max={stats['games_n_max']} "
        f"median={stats['games_n_median']:.0f} mean={stats['games_n_mean']:.1f}",
        flush=True,
    )
    if not after_qc:
        print(f"  with 1 game: {stats['n_with_1_game']:,} ({100 * stats['pct_with_1_game']:.1f}%)", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    return meta


def plot_only(*, after_qc: bool) -> None:
    paths = _artifact_paths(after_qc=after_qc)
    if not paths["json"].is_file() or not paths["csv"].is_file():
        raise SystemExit(f"Missing artifacts — run full diagnostic first: {paths['json']}")
    meta = json.loads(paths["json"].read_text(encoding="utf-8"))
    games_n = pd.read_csv(paths["csv"])["games_n"].to_numpy(dtype=int)
    stats = {k: meta[k] for k in meta if k.startswith("games_n_") or k == "n_team_seasons"}
    stats.update(
        {
            "n_with_1_game": meta.get("n_with_1_game", 0),
            "games_n_median": meta.get("games_n_median", float(np.median(games_n))),
        }
    )
    if after_qc:
        title_suffix = f"after box QC (keep $\\geq${DEFAULT_MIN_GAMES + 1} games)"
        threshold_line = float(DEFAULT_MIN_GAMES + 1)
        threshold_label = f"Keep threshold = {DEFAULT_MIN_GAMES + 1} games"
    else:
        title_suffix = "raw box (no QC)"
        threshold_line = 1.0
        threshold_label = f"1 game (n={int(meta.get('n_with_1_game', 0)):,})"
    _plot(
        games_n,
        stats=stats,
        png_path=paths["png"],
        title_suffix=title_suffix,
        threshold_line=threshold_line,
        threshold_label=threshold_label,
    )
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-only", action="store_true", help="Raw box only")
    parser.add_argument("--after-qc-only", action="store_true", help="After box QC only")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV/JSON")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    ensure_hero_dirs()
    do_raw = not args.after_qc_only
    do_qc = not args.raw_only

    if args.plot_only:
        if do_raw:
            plot_only(after_qc=False)
        if do_qc:
            plot_only(after_qc=True)
        return

    if do_raw:
        _run_one(after_qc=False)
    if do_qc:
        _run_one(after_qc=True)


if __name__ == "__main__":
    main()
