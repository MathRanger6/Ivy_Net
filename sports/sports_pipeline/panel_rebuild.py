"""
Rebuild the 530 **player–season–team** panel from data on disk (no legacy 530 notebook).

**Flow (gameplan-aligned):**

1. Read ``mbb_df_player_box.csv`` (game-level; **not** rewritten on disk).
2. **Box QC** (configurable): drop ESPN ``"-"`` placeholder names; drop ``(team_id, season)``
   with too few distinct games in box.
3. Aggregate → one row per ``(athlete_id, season, team_id)`` with ``minutes``, ``points``,
   ``ppm``, ``games``, display names.
4. Attach **ever-draft** ``Y_draft`` from ``athlete_id_draft_lookup.csv``.
5. Left-merge **SR advanced** columns from ``DO_NOT_ERASE/bpm_player_season_matched.csv`` when
   that file exists (same keys as legacy Cell 7).

Downstream, ``panel_build.apply_perf_metric_for_analysis`` sets ``perf`` and recomputes
``poolq_loo`` / ``poolq_sq`` for ventiles + LPM (PPM, minutes, BPM, OBPM, DBPM).

See also ``bpm_merge`` for crosswalk / scrape jobs / raw→matched refresh.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sports_pipeline import paths

# Populated by the most recent ``build_from_box`` call (for integrity / provenance reports).
last_box_qc_report: dict[str, Any] | None = None


def box_qc_provenance_lines(cfg: Any, report: dict[str, Any] | None = None) -> list[str]:
    """Human-readable provenance lines for ventile exports and integrity reports."""
    rep = report if report is not None else last_box_qc_report
    drop_dash = bool(getattr(cfg, "drop_dash_placeholder_names", True))
    min_g = int(getattr(cfg, "min_team_season_games", 10))
    lines = [
        "Box QC (panel_rebuild.build_from_box; raw mbb_df_player_box.csv untouched on disk):",
        f"  drop_dash_placeholder_names={drop_dash}",
        f"  min_team_season_games={min_g} (drop team-season if distinct game_id count <= this; 0=off)",
    ]
    if rep:
        if drop_dash:
            lines.append(
                f"  dash placeholder rows dropped: {int(rep.get('dash_rows_dropped', 0)):,}"
            )
        if min_g > 0:
            lines.append(
                f"  team-seasons dropped (low games): {int(rep.get('team_seasons_dropped_low_games', 0)):,}; "
                f"game rows removed: {int(rep.get('box_rows_dropped_low_games', 0)):,}"
            )
        lines.append(
            f"  box game rows after QC: {int(rep.get('box_rows_after_qc', 0)):,} "
            f"(read {int(rep.get('box_rows_read', 0)):,})"
        )
    return lines


def _apply_box_qc(df_g: pd.DataFrame, cfg: Any) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Game-level filters before player-season aggregation."""
    report: dict[str, Any] = {
        "box_rows_read": int(len(df_g)),
        "drop_dash_placeholder_names": bool(getattr(cfg, "drop_dash_placeholder_names", True)),
        "min_team_season_games": int(getattr(cfg, "min_team_season_games", 5)),
        "dash_rows_dropped": 0,
        "team_seasons_dropped_low_games": 0,
        "box_rows_dropped_low_games": 0,
    }

    if report["drop_dash_placeholder_names"]:
        dash = df_g["athlete_display_name"].astype(str).str.strip() == "-"
        report["dash_rows_dropped"] = int(dash.sum())
        df_g = df_g.loc[~dash].copy()

    min_g = int(report["min_team_season_games"])
    if min_g > 0:
        if "game_id" not in df_g.columns:
            raise ValueError("min_team_season_games requires game_id in box read columns")
        ts_games = df_g.groupby(["team_id", "season"], observed=True)["game_id"].nunique()
        keep_ts = ts_games[ts_games > min_g]
        dropped_ts = ts_games[ts_games <= min_g]
        report["team_seasons_dropped_low_games"] = int(len(dropped_ts))
        before = len(df_g)
        keep_df = keep_ts.reset_index(name="_games_n")
        df_g = df_g.merge(keep_df[["team_id", "season"]], on=["team_id", "season"], how="inner")
        report["box_rows_dropped_low_games"] = int(before - len(df_g))

    report["box_rows_after_qc"] = int(len(df_g))
    return df_g, report


def merge_sr_matched_into_panel(df: pd.DataFrame, matched_path: Any = None) -> pd.DataFrame:
    """
    Left-merge ``bpm_player_season_matched.csv`` on ``(athlete_id, season, team_id)``.

    Drops overlapping stat columns from ``df`` before merge so refreshed SR values win.
    """
    p = Path(paths.bpm_matched_csv() if matched_path is None else matched_path)
    if not p.is_file():
        return df
    mb = pd.read_csv(p, low_memory=False)
    key = ["athlete_id", "season", "team_id"]
    for c in key:
        if c not in df.columns or c not in mb.columns:
            return df
    for col in key:
        df = df.copy()
        mb = mb.copy()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        mb[col] = pd.to_numeric(mb[col], errors="coerce")
    mb = mb.drop_duplicates(subset=key)
    extra = [c for c in mb.columns if c not in key and c in df.columns]
    out = df.drop(columns=extra, errors="ignore")
    stat_cols = [c for c in mb.columns if c not in key]
    out = out.merge(mb[key + stat_cols], on=key, how="left")
    return out


def build_from_box(cfg: Any) -> pd.DataFrame:
    """
    Build panel from ESPN box + draft lookup + optional SR matched file.

    Does **not** set ``perf`` / ``poolq_loo`` — run ``panel_build.apply_perf_metric_for_analysis``
    next.
    """
    global last_box_qc_report

    box_path = paths.player_box_csv()
    if not box_path.is_file():
        raise FileNotFoundError(f"Missing player box: {box_path}")

    usecols = [
        "game_id",
        "athlete_id",
        "season",
        "team_id",
        "team_short_display_name",
        "athlete_display_name",
        "minutes",
        "points",
    ]
    df_g = pd.read_csv(box_path, usecols=usecols, low_memory=False)
    for c in ["athlete_id", "season", "team_id", "minutes", "points"]:
        df_g[c] = pd.to_numeric(df_g[c], errors="coerce")
    df_g = df_g.dropna(subset=["athlete_id", "season", "team_id"])
    df_g["season"] = df_g["season"].astype(int)

    lo = getattr(cfg, "panel_season_min", None)
    hi = getattr(cfg, "panel_season_max", None)
    if lo is not None:
        df_g = df_g.loc[df_g["season"] >= int(lo)]
    if hi is not None:
        df_g = df_g.loc[df_g["season"] <= int(hi)]

    df_g, qc_report = _apply_box_qc(df_g, cfg)
    last_box_qc_report = qc_report

    df_g = df_g.copy()
    df_g["_played"] = pd.to_numeric(df_g["minutes"], errors="coerce").fillna(0.0) > 0.0

    agg = (
        df_g.groupby(["athlete_id", "season", "team_id"], as_index=False)
        .agg(
            minutes=("minutes", "sum"),
            points=("points", "sum"),
            team_short_display_name=("team_short_display_name", "last"),
            athlete_display_name=("athlete_display_name", "last"),
            games_rostered=("game_id", "count"),
            games_played=("_played", "sum"),
        )
    )
    agg["games"] = agg["games_rostered"]  # legacy alias
    agg["apgms"] = np.where(
        agg["games_played"] > 0,
        agg["minutes"] / agg["games_played"],
        np.nan,
    )
    agg["argms"] = np.where(
        agg["games_rostered"] > 0,
        agg["minutes"] / agg["games_rostered"],
        np.nan,
    )
    agg["ppm"] = np.where(agg["minutes"] > 0, agg["points"] / agg["minutes"], np.nan)

    mm = float(getattr(cfg, "min_minutes", 0.0))
    if mm > 0:
        agg = agg.loc[agg["minutes"] >= mm].copy()

    lu_path = paths.draft_lookup_csv()
    if not lu_path.is_file():
        raise FileNotFoundError(
            f"Missing draft lookup {lu_path}. Build it from your draft-match stage before panel rebuild."
        )
    lu = pd.read_csv(lu_path, low_memory=False)
    if "athlete_id" not in lu.columns:
        raise ValueError(f"Draft lookup must have athlete_id: {lu_path}")
    drafted = set(pd.to_numeric(lu["athlete_id"], errors="coerce").dropna().astype(int))
    agg["athlete_id"] = pd.to_numeric(agg["athlete_id"], errors="coerce")
    agg = agg.dropna(subset=["athlete_id"])
    agg["athlete_id"] = agg["athlete_id"].astype(int)
    agg["Y_draft"] = agg["athlete_id"].isin(drafted).astype(int)

    agg = merge_sr_matched_into_panel(agg)
    qc_report["player_season_rows"] = int(len(agg))
    last_box_qc_report = qc_report
    return agg
