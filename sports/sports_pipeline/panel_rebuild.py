"""
Rebuild the 530 **player–season–team** panel from data on disk (no legacy 530 notebook).

**Flow (gameplan-aligned):**

1. Aggregate ``mbb_df_player_box.csv`` → one row per ``(athlete_id, season, team_id)`` with
   ``minutes``, ``points``, ``ppm``, ``games``, display names.
2. Attach **ever-draft** ``Y_draft`` from ``athlete_id_draft_lookup.csv``.
3. Left-merge **SR advanced** columns from ``DO_NOT_ERASE/bpm_player_season_matched.csv`` when
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
    box_path = paths.player_box_csv()
    if not box_path.is_file():
        raise FileNotFoundError(f"Missing player box: {box_path}")

    usecols = [
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

    agg = (
        df_g.groupby(["athlete_id", "season", "team_id"], as_index=False)
        .agg(
            minutes=("minutes", "sum"),
            points=("points", "sum"),
            team_short_display_name=("team_short_display_name", "last"),
            athlete_display_name=("athlete_display_name", "last"),
            games=("minutes", "count"),
        )
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
    return agg
