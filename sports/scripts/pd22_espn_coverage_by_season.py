#!/usr/bin/env python3
"""PD22 — ESPN box coverage by season (2013→2014 roster-depth break diagnostic).

Documents the Aug 2026 finding that raw player-season counts jump in 2014 because
ESPN lists more players per box score (~+2 rows/game/team), not because games doubled.
Box QC + min-20 hero panel stabilizes longitudinal counts for rho / H_sort calibration.

Run (repo root):
  python sports/scripts/pd22_espn_coverage_by_season.py
  python sports/scripts/pd22_espn_coverage_by_season.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_espn_coverage_by_season_2011_2021.png
  PD22_espn_coverage_by_season_2011_2021.json
  PD22_espn_coverage_by_season_2011_2021.csv
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
from pd22_slide_common import MIN_TEAM_SEASON_GAMES

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_espn_coverage_by_season"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

OUT = PD22_MINUTES
HERO_LOCK = 20.0
BOX_USECOLS = [
    "game_id",
    "athlete_id",
    "season",
    "team_id",
    "athlete_display_name",
    "minutes",
]


def _artifact_paths() -> dict[str, Path]:
    return {
        "png": OUT / f"{_stem()}.png",
        "json": OUT / f"{_stem()}.json",
        "csv": OUT / f"{_stem()}.csv",
    }


def _load_box() -> pd.DataFrame:
    from sports_pipeline import paths

    box_path = paths.player_box_csv()
    if not box_path.is_file():
        raise FileNotFoundError(f"Missing player box: {box_path}")
    df = pd.read_csv(box_path, usecols=BOX_USECOLS, low_memory=False)
    for c in ["athlete_id", "season", "team_id", "minutes"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["athlete_id", "season", "team_id"])
    df["season"] = df["season"].astype(int)
    return df.loc[(df["season"] >= _w().season_min) & (df["season"] <= _w().season_max)].copy()


def _player_seasons(g: pd.DataFrame) -> int:
    return int(g.groupby(["athlete_id", "season", "team_id"], observed=True).ngroups)


def _season_row(g: pd.DataFrame) -> dict:
    roster = g.groupby(["team_id", "season"], observed=True)["athlete_id"].nunique()
    rpg = g.groupby(["game_id", "team_id"], observed=True).size()
    return {
        "games": int(g["game_id"].nunique()),
        "teams": int(g["team_id"].nunique()),
        "team_seasons": int(g.groupby(["team_id", "season"], observed=True).ngroups),
        "player_seasons_raw": _player_seasons(g),
        "median_roster_per_ts": float(roster.median()),
        "mean_roster_per_ts": float(roster.mean()),
        "mean_box_rows_per_game_team": float(rpg.mean()) if len(rpg) else float("nan"),
        "dash_rows": int((g["athlete_display_name"].astype(str).str.strip() == "-").sum()),
    }


def _overlap_team_comparison(df: pd.DataFrame) -> dict:
    t2013 = set(df.loc[df["season"] == 2013, "team_id"].unique())
    t2014 = set(df.loc[df["season"] == 2014, "team_id"].unique())
    both = t2013 & t2014
    out = {
        "teams_2013": len(t2013),
        "teams_2014": len(t2014),
        "overlap_teams": len(both),
        "new_in_2014": len(t2014 - t2013),
        "gone_from_2013": len(t2013 - t2014),
    }
    for yr, label in ((2013, "2013"), (2014, "2014")):
        sub = df.loc[(df["season"] == yr) & (df["team_id"].isin(both))]
        out[f"player_seasons_overlap_{label}"] = _player_seasons(sub)
    return out


def _build_table(df: pd.DataFrame) -> pd.DataFrame:
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.panel_rebuild import _apply_box_qc

    cfg_qc = PipelineConfig(
        panel_season_min=_w().season_min,
        panel_season_max=_w().season_max,
        min_team_season_games=MIN_TEAM_SEASON_GAMES,
    )

    rows: list[dict] = []
    for season, g in df.groupby("season", sort=True):
        base = _season_row(g)
        g_qc, qc_rep = _apply_box_qc(g.copy(), cfg_qc)
        base.update(
            {
                "season": int(season),
                "player_seasons_after_qc": _player_seasons(g_qc),
                "teams_after_qc": int(g_qc["team_id"].nunique()),
                "team_seasons_dropped_qc": int(qc_rep.get("team_seasons_dropped_low_games", 0)),
            }
        )
        rows.append(base)

    tab = pd.DataFrame(rows).sort_values("season")

    from sports_pipeline import conductor

    pipe = PipelineConfig(
        min_minutes=HERO_LOCK,
        panel_season_min=_w().season_min,
        panel_season_max=_w().season_max,
        use_prebuilt_panel_csv=False,
    )
    print("Rebuilding min-20 hero panel (box QC on) for per-season counts ...", flush=True)
    panel = conductor.prepare_panel(pipe)
    hero_by_season = panel.groupby("season").size()
    tab["player_seasons_min20"] = tab["season"].map(hero_by_season).fillna(0).astype(int)

    return tab


def _pct_change(a: float, b: float) -> float | None:
    if a == 0:
        return None
    return 100.0 * (b - a) / a


def _2013_2014_summary(tab: pd.DataFrame) -> dict:
    r13 = tab.loc[tab["season"] == 2013].iloc[0]
    r14 = tab.loc[tab["season"] == 2014].iloc[0]
    keys = [
        "games",
        "teams",
        "player_seasons_raw",
        "player_seasons_after_qc",
        "player_seasons_min20",
        "median_roster_per_ts",
        "mean_box_rows_per_game_team",
    ]
    out: dict = {"seasons": "2013→2014"}
    for k in keys:
        a, b = float(r13[k]), float(r14[k])
        out[f"{k}_2013"] = a
        out[f"{k}_2014"] = b
        out[f"{k}_pct_change"] = _pct_change(a, b)
    return out


def _break_x_between(seasons: np.ndarray, y_before: int, y_after: int) -> float | None:
    """Mid-x index between two consecutive seasons (for vertical break markers)."""
    seasons = np.asarray(seasons, dtype=int)
    i_before = np.flatnonzero(seasons == y_before)
    i_after = np.flatnonzero(seasons == y_after)
    if i_before.size and i_after.size:
        return (float(i_before[0]) + float(i_after[0])) / 2.0
    return None


def _plot(tab: pd.DataFrame, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = tab["season"].to_numpy(dtype=int)
    x = np.arange(len(seasons))
    break_x = _break_x_between(seasons, 2013, 2014)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    ax = axes[0]
    ax.plot(x, tab["player_seasons_raw"], "o-", color="0.55", label="Raw aggregate (all box rows)", lw=2)
    ax.plot(
        x,
        tab["player_seasons_after_qc"],
        "s-",
        color="steelblue",
        label=f"After box QC (keep >{MIN_TEAM_SEASON_GAMES} games)",
        lw=2,
    )
    ax.plot(
        x,
        tab["player_seasons_min20"],
        "^-",
        color="darkorange",
        label=f"Hero panel (min $\\geq$ {HERO_LOCK:g} min)",
        lw=2.2,
    )
    if break_x is not None:
        ax.axvline(break_x, color="crimson", ls="--", lw=1.5, alpha=0.85)
        ax.text(break_x + 0.05, ax.get_ylim()[1] * 0.97, "2013→2014", color="crimson", fontsize=8, va="top")
    ax.set_xticks(x)
    ax.set_xticklabels(seasons, rotation=45, ha="right")
    ax.set_xlabel("Season")
    ax.set_ylabel("Player-season rows")
    ax.set_title("Panel size by season")
    ax.legend(loc="upper left", fontsize=7.5)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    ax = axes[1]
    w = 0.35
    ax.bar(x - w / 2, tab["median_roster_per_ts"], width=w, color="steelblue", alpha=0.85, label="Median roster / team-season")
    ax2 = ax.twinx()
    ax2.plot(
        x,
        tab["mean_box_rows_per_game_team"],
        "D-",
        color="darkorange",
        label="Mean box rows / game / team",
        lw=2,
    )
    if break_x is not None:
        ax.axvline(break_x, color="crimson", ls="--", lw=1.5, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(seasons, rotation=45, ha="right")
    ax.set_xlabel("Season")
    ax.set_ylabel("Median players per team-season")
    ax2.set_ylabel("Mean rows per game per team")
    ax.set_title("ESPN box depth (raw)")
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=7.5)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    seasons_label_str = seasons_label(_w().season_min, _w().season_max)
    fig.suptitle(
        f"PD22 — ESPN box coverage by season · {seasons_label_str} · "
        f"2013→2014 raw player-seasons +{tab.loc[tab.season == 2014, 'player_seasons_raw'].iloc[0] - tab.loc[tab.season == 2013, 'player_seasons_raw'].iloc[0]:,} "
        f"(games +{_pct_change(tab.loc[tab.season == 2013, 'games'].iloc[0], tab.loc[tab.season == 2014, 'games'].iloc[0]):.0f}%)",
        fontsize=10.5,
        y=1.03,
    )
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run(*, write_csv: bool = True) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    print("Loading frozen ESPN box CSV ...", flush=True)
    df = _load_box()
    tab = _build_table(df)
    if write_csv:
        tab.to_csv(paths["csv"], index=False)

    jump = _2013_2014_summary(tab)
    overlap = _overlap_team_comparison(df)

    meta = {
        "diagnostic": "pd22_espn_coverage_by_season",
        "date": date.today().isoformat(),
        "season_min": _w().season_min,
        "season_max": _w().season_max,
        "seasons": seasons_label(_w().season_min, _w().season_max),
        "source": "datasets/mbb/mbb_df_player_box.csv (frozen; not rewritten)",
        "hero_lock_min_minutes": HERO_LOCK,
        "min_team_season_games": MIN_TEAM_SEASON_GAMES,
        "jump_2013_2014": jump,
        "overlap_teams_2013_2014": overlap,
        "by_season": tab.to_dict(orient="records"),
        "scout_note": (
            "SCOUT verify: 2014 jump is roster depth (median roster/team-season, rows/game/team), "
            "not game count. Hero min-20 panel should be ~flat across 2013→2014."
        ),
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    _plot(tab, paths["png"])

    print(f"\n2013→2014 raw player-seasons: {jump['player_seasons_raw_2013']:.0f} → {jump['player_seasons_raw_2014']:.0f} "
          f"({jump['player_seasons_raw_pct_change']:+.1f}%)", flush=True)
    print(f"  games: {jump['games_pct_change']:+.1f}%  median roster/ts: {jump['median_roster_per_ts_pct_change']:+.1f}%", flush=True)
    print(f"  min-20 panel: {jump['player_seasons_min20_2013']:.0f} → {jump['player_seasons_min20_2014']:.0f} "
          f"({jump['player_seasons_min20_pct_change']:+.1f}%)", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    tab = pd.read_csv(paths["csv"])
    _plot(tab, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    if args.plot_only:
        plot_only()
        return
    run()


if __name__ == "__main__":
    main()
