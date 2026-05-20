"""
Bridge NBA combine ``player_id`` (``draft_combine_stats``) to ESPN ``athlete_id`` (college box spine).

**Inputs (under ``datasets/mbb/``):**

- ``DO_NOT_ERASE/basketball/csv/draft_combine_stats.csv``
- ``DO_NOT_ERASE/basketball/csv/draft_history.csv`` — ``person_id`` + draft ``season``
- ``DO_NOT_ERASE/basketball/csv/player.csv`` — optional name backfill for NBA ids
- ``athlete_id_draft_lookup.csv`` / ``draft_athlete_match.csv`` — existing draft↔ESPN matches
- ``mbb_df_player_box.csv`` or ``player_season_panel_530.csv`` — spine name index for undrafted combine

**Outputs:**

- ``combine_player_id_bridge.csv`` — one row per combine row + ``athlete_id`` when found
- ``athlete_id_combine_lookup.csv`` — one row per ``athlete_id`` ever at combine
- ``combine_bridge_diagnostic_summary.csv`` — match-tier counts

**Match tiers (best-first):**

1. ``draft_lookup`` — ``athlete_id`` from ``athlete_id_draft_lookup`` + ``draft_year`` = combine ``season``
2. ``draft_athlete_match`` — ``athlete_id`` from ``draft_athlete_match`` + ``year`` = combine ``season``
3. ``spine_name_year`` — normalized display name on ESPN spine, last college season in
   ``[season - 1, season]`` (combine ``season`` = NBA draft year)
4. ``spine_name_fuzzy`` — same window, ``difflib`` ratio ≥ 0.92 on last name + full name guard

``nba_person_id`` on the bridge is the combine ``player_id`` when it appears in
``draft_history`` for that season, else name-resolved ``person_id`` when unique.
"""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sports_pipeline import paths
from sports_pipeline.bpm_merge import normalize_player_name

# Tiers in priority order (lower = better).
_TIER_RANK = {
    "draft_lookup": 0,
    "draft_athlete_match": 1,
    "spine_name_year": 2,
    "spine_name_fuzzy": 3,
    "unmatched": 99,
}

_FUZZY_MIN_RATIO = 0.92


def _read_csv(p: Path, **kwargs: Any) -> pd.DataFrame:
    if not p.is_file():
        raise FileNotFoundError(p)
    return pd.read_csv(p, low_memory=False, **kwargs)


def load_combine_stats(path: Path | None = None) -> pd.DataFrame:
    p = Path(paths.draft_combine_stats_csv() if path is None else path)
    df = _read_csv(p)
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce")
    df["season"] = pd.to_numeric(df["season"], errors="coerce")
    if "player_name" not in df.columns:
        raise ValueError(f"{p} missing player_name")
    df["name_norm"] = df["player_name"].map(normalize_player_name)
    return df


def load_draft_history_index(path: Path | None = None) -> pd.DataFrame:
    """``(name_norm, season)`` → ``person_id`` when unique; includes direct ``player_id`` hits."""
    p = Path(paths.draft_history_csv() if path is None else path)
    dh = _read_csv(p)
    draft = dh.loc[dh["draft_type"].astype(str).str.strip().eq("Draft")].copy()
    draft["person_id"] = pd.to_numeric(draft["person_id"], errors="coerce")
    draft["season"] = pd.to_numeric(draft["season"], errors="coerce")
    draft["name_norm"] = draft["player_name"].map(normalize_player_name)
    g = (
        draft.dropna(subset=["name_norm", "season"])
        .groupby(["name_norm", "season"], as_index=False)
        .agg(
            person_id=("person_id", "first"),
            n_person_ids=("person_id", "nunique"),
            player_name_dh=("player_name", "first"),
        )
    )
    g["person_id_unique"] = g["n_person_ids"] == 1
    return g


def load_nba_player_names(path: Path | None = None) -> pd.DataFrame:
    p = Path(paths.nba_player_csv() if path is None else path)
    if not p.is_file():
        return pd.DataFrame(columns=["player_id", "nba_full_name", "name_norm"])
    pl = _read_csv(p)
    pl["player_id"] = pd.to_numeric(pl["id"], errors="coerce")
    pl["nba_full_name"] = pl["full_name"].astype(str)
    pl["name_norm"] = pl["nba_full_name"].map(normalize_player_name)
    return pl[["player_id", "nba_full_name", "name_norm"]].dropna(subset=["player_id"])


def build_espn_spine_index(
    cfg: Any | None = None,
    *,
    panel_path: Path | None = None,
    box_path: Path | None = None,
) -> pd.DataFrame:
    """
    One row per ``athlete_id``: display name + min/max college ``season`` on file.

    Prefers ``player_season_panel_530.csv`` when present (fast); else aggregates box CSV.
    """
    panel_p = Path(panel_path or paths.panel_530_csv())
    if panel_p.is_file():
        use = _read_csv(
            panel_p,
            usecols=["athlete_id", "season", "athlete_display_name"],
        )
    else:
        box_p = Path(box_path or paths.player_box_csv())
        if not box_p.is_file():
            raise FileNotFoundError(
                f"Need {panel_p} or {box_p} to build ESPN spine index for combine bridge."
            )
        use = _read_csv(
            box_p,
            usecols=["athlete_id", "season", "athlete_display_name"],
        )
    use["athlete_id"] = pd.to_numeric(use["athlete_id"], errors="coerce")
    use["season"] = pd.to_numeric(use["season"], errors="coerce")
    use = use.dropna(subset=["athlete_id", "season"])
    use["name_norm"] = use["athlete_display_name"].map(normalize_player_name)
    spine = (
        use.groupby("athlete_id", as_index=False)
        .agg(
            athlete_display_name=("athlete_display_name", "last"),
            name_norm=("name_norm", "last"),
            season_min=("season", "min"),
            season_max=("season", "max"),
        )
    )
    spine["athlete_id"] = spine["athlete_id"].astype(int)
    return spine


def _attach_nba_person_id(comb: pd.DataFrame, dh_idx: pd.DataFrame) -> pd.DataFrame:
    out = comb.copy()
    # Direct id match on draft history for this draft year.
    dh_pid = dh_idx.rename(columns={"season": "combine_season", "person_id": "person_id_dh"})
    out = out.merge(
        dh_pid[["name_norm", "combine_season", "person_id_dh", "person_id_unique"]],
        left_on=["name_norm", "season"],
        right_on=["name_norm", "combine_season"],
        how="left",
    )
    out = out.drop(columns=["combine_season"], errors="ignore")
    out["nba_person_id"] = np.where(
        out["player_id"].isin(out["person_id_dh"].dropna()),
        out["player_id"],
        np.where(out["person_id_unique"].fillna(False), out["person_id_dh"], np.nan),
    )
    return out


def _links_from_spine_exact(
    comb: pd.DataFrame,
    spine: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    spine_by_name: dict[str, list[dict[str, Any]]] = {}
    for r in spine.itertuples(index=False):
        nn = r.name_norm
        if not nn:
            continue
        spine_by_name.setdefault(nn, []).append(
            {
                "athlete_id": int(r.athlete_id),
                "season_min": int(r.season_min),
                "season_max": int(r.season_max),
            }
        )
    for row in comb.itertuples(index=False):
        nn = row.name_norm
        if not nn or nn not in spine_by_name:
            continue
        cy = int(row.season)
        for cand in spine_by_name[nn]:
            if cand["season_max"] < cy - 1 or cand["season_max"] > cy:
                continue
            rows.append(
                {
                    "player_id": int(row.player_id),
                    "season": cy,
                    "athlete_id": cand["athlete_id"],
                    "match_tier": "spine_name_year",
                    "match_score": 1.0,
                }
            )
            break
    return pd.DataFrame(rows)


def _last_name(norm: str) -> str:
    parts = norm.split()
    return parts[-1] if parts else ""


def _links_from_spine_fuzzy(
    comb: pd.DataFrame,
    spine: pd.DataFrame,
    *,
    already: set[tuple[int, int]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    spine = spine.copy()
    spine["last_norm"] = spine["name_norm"].map(_last_name)
    by_last: dict[str, list[Any]] = {}
    for r in spine.itertuples(index=False):
        if not r.last_norm:
            continue
        by_last.setdefault(r.last_norm, []).append(r)

    for row in comb.itertuples(index=False):
        key = (int(row.player_id), int(row.season))
        if key in already:
            continue
        nn = row.name_norm
        if not nn:
            continue
        ln = _last_name(nn)
        if not ln or ln not in by_last:
            continue
        cy = int(row.season)
        best_id: int | None = None
        best_score = 0.0
        for cand in by_last[ln]:
            if cand.season_max < cy - 1 or cand.season_max > cy:
                continue
            score = difflib.SequenceMatcher(None, nn, cand.name_norm).ratio()
            if score >= _FUZZY_MIN_RATIO and score > best_score:
                best_score = score
                best_id = int(cand.athlete_id)
        if best_id is not None:
            rows.append(
                {
                    "player_id": int(row.player_id),
                    "season": cy,
                    "athlete_id": best_id,
                    "match_tier": "spine_name_fuzzy",
                    "match_score": round(best_score, 4),
                }
            )
    return pd.DataFrame(rows)


def _collect_draft_lookup_links(base: pd.DataFrame) -> pd.DataFrame:
    p = paths.draft_lookup_csv()
    if not p.is_file():
        return pd.DataFrame(columns=["player_id", "season", "athlete_id", "match_tier", "match_score"])
    lu = _read_csv(p)
    lu["athlete_id"] = pd.to_numeric(lu["athlete_id"], errors="coerce")
    lu["draft_year"] = pd.to_numeric(lu["draft_year"], errors="coerce")
    lu["name_norm"] = lu["player"].map(normalize_player_name)
    lu = lu.dropna(subset=["athlete_id", "draft_year", "name_norm"])
    m = base.merge(
        lu[["name_norm", "draft_year", "athlete_id"]].drop_duplicates(),
        left_on=["name_norm", "season"],
        right_on=["name_norm", "draft_year"],
        how="inner",
    )
    m["match_tier"] = "draft_lookup"
    m["match_score"] = 1.0
    return m[["player_id", "season", "athlete_id", "match_tier", "match_score"]]


def _collect_draft_match_links(base: pd.DataFrame) -> pd.DataFrame:
    p = paths.draft_athlete_match_csv()
    if not p.is_file():
        return pd.DataFrame(columns=["player_id", "season", "athlete_id", "match_tier", "match_score"])
    dm = _read_csv(p)
    dm["athlete_id"] = pd.to_numeric(dm["athlete_id"], errors="coerce")
    dm["season"] = pd.to_numeric(dm["year"], errors="coerce")
    dm["name_norm"] = dm["player"].map(normalize_player_name)
    dm = dm.dropna(subset=["athlete_id", "season", "name_norm"])
    score_col = "match_full_name_score" if "match_full_name_score" in dm.columns else None
    keep = ["name_norm", "season", "athlete_id"] + ([score_col] if score_col else [])
    m = base.merge(dm[keep].drop_duplicates(subset=["name_norm", "season"]), on=["name_norm", "season"], how="inner")
    m["match_tier"] = "draft_athlete_match"
    if score_col:
        m["match_score"] = pd.to_numeric(m[score_col], errors="coerce").fillna(1.0)
        m = m.drop(columns=[score_col], errors="ignore")
    else:
        m["match_score"] = 1.0
    return m[["player_id", "season", "athlete_id", "match_tier", "match_score"]]


def _pick_best_links(link_frames: list[pd.DataFrame]) -> pd.DataFrame:
    if not link_frames:
        return pd.DataFrame(columns=["player_id", "season", "athlete_id", "match_tier", "match_score"])
    all_links = pd.concat(link_frames, ignore_index=True)
    all_links["tier_rank"] = all_links["match_tier"].map(_TIER_RANK)
    return (
        all_links.sort_values(
            ["player_id", "season", "tier_rank", "match_score"],
            ascending=[True, True, True, False],
        )
        .drop_duplicates(subset=["player_id", "season"], keep="first")
        .drop(columns=["tier_rank"], errors="ignore")
    )


def build_combine_bridge(
    cfg: Any | None = None,
    *,
    write: bool = True,
    fuzzy: bool = True,
) -> dict[str, Any]:
    """
    Build bridge tables and optionally write CSVs under ``datasets/mbb/``.

    Returns summary dict with DataFrames in ``tables`` when ``write=False``.
    """
    comb = load_combine_stats()
    dh_idx = load_draft_history_index()
    nba_names = load_nba_player_names()
    spine = build_espn_spine_index(cfg)

    base = _attach_nba_person_id(comb, dh_idx)
    if not nba_names.empty:
        base = base.merge(nba_names, on="player_id", how="left", suffixes=("", "_nba"))
        miss = base["name_norm"].eq("") | base["name_norm"].isna()
        base.loc[miss, "name_norm"] = base.loc[miss, "nba_full_name"].map(normalize_player_name)

    link_frames: list[pd.DataFrame] = []
    m_lu = _collect_draft_lookup_links(base)
    if not m_lu.empty:
        link_frames.append(m_lu)
    m_dm = _collect_draft_match_links(base)
    if not m_dm.empty:
        link_frames.append(m_dm)
    exact = _links_from_spine_exact(base, spine)
    if not exact.empty:
        link_frames.append(exact)

    best_links = _pick_best_links(link_frames)
    assigned = set(
        zip(best_links["player_id"].astype(int), best_links["season"].astype(int))
    ) if not best_links.empty else set()

    if fuzzy:
        fuzz = _links_from_spine_fuzzy(base, spine, already=assigned)
        if not fuzz.empty:
            best_links = _pick_best_links([best_links, fuzz] if not best_links.empty else [fuzz])

    bridge = base.merge(
        best_links,
        on=["player_id", "season"],
        how="left",
    )
    bridge["match_tier"] = bridge["match_tier"].fillna("unmatched")
    bridge["match_score"] = bridge["match_score"].fillna(0.0)
    bridge["athlete_id"] = pd.to_numeric(bridge["athlete_id"], errors="coerce")

    lookup_out = (
        bridge.dropna(subset=["athlete_id"])
        .drop_duplicates(subset=["athlete_id"])
        .assign(Y_combine_meas=1)[
            [
                "athlete_id",
                "player_id",
                "season",
                "player_name",
                "match_tier",
                "match_score",
                "nba_person_id",
            ]
        ]
        .rename(
            columns={
                "player_id": "nba_combine_player_id",
                "season": "combine_season",
                "player_name": "combine_player_name",
            }
        )
    )

    diag_rows = [
        {"metric": "combine_rows", "value": len(comb)},
        {"metric": "bridge_athlete_id_matched", "value": int(bridge["athlete_id"].notna().sum())},
        {"metric": "bridge_match_rate", "value": float(bridge["athlete_id"].notna().mean())},
        {"metric": "unique_athlete_ids", "value": int(lookup_out["athlete_id"].nunique())},
    ]
    for tier, n in bridge["match_tier"].value_counts().items():
        diag_rows.append({"metric": f"tier_{tier}", "value": int(n)})
    diagnostic = pd.DataFrame(diag_rows)

    result: dict[str, Any] = {
        "combine_rows": len(comb),
        "matched_rows": int(bridge["athlete_id"].notna().sum()),
        "match_rate": float(bridge["athlete_id"].notna().mean()),
        "unique_athlete_ids": int(lookup_out["athlete_id"].nunique()),
    }

    if write:
        out_bridge = paths.combine_player_id_bridge_csv()
        out_lookup = paths.athlete_id_combine_lookup_csv()
        out_diag = paths.combine_bridge_diagnostic_csv()
        paths.mbb_dir().mkdir(parents=True, exist_ok=True)
        bridge.to_csv(out_bridge, index=False)
        lookup_out.to_csv(out_lookup, index=False)
        diagnostic.to_csv(out_diag, index=False)
        result["paths"] = {
            "bridge": str(out_bridge),
            "lookup": str(out_lookup),
            "diagnostic": str(out_diag),
        }
    else:
        result["tables"] = {
            "bridge": bridge,
            "lookup": lookup_out,
            "diagnostic": diagnostic,
        }

    return result


def run(cfg: Any | None = None) -> dict[str, Any]:
    """Pipeline stage entry: build combine bridge CSVs."""
    return build_combine_bridge(cfg, write=True)


def attach_combine_to_panel(
    panel: pd.DataFrame,
    lookup_path: Path | None = None,
    *,
    combine_season_offset: int = 1,
) -> pd.DataFrame:
    """
    Add ``Y_combine_meas`` and ``nba_combine_player_id`` to a player-season panel.

    Flags combine attendance in the draft year after the collegiate season by default:
    panel ``season`` + ``combine_season_offset`` == ``combine_season`` on the lookup.
    """
    p = Path(paths.athlete_id_combine_lookup_csv() if lookup_path is None else lookup_path)
    if not p.is_file():
        out = panel.copy()
        out["Y_combine_meas"] = 0
        out["nba_combine_player_id"] = np.nan
        return out
    lu = _read_csv(p)
    lu["athlete_id"] = pd.to_numeric(lu["athlete_id"], errors="coerce")
    lu["combine_season"] = pd.to_numeric(lu["combine_season"], errors="coerce")
    lu = lu.dropna(subset=["athlete_id", "combine_season"]).drop_duplicates(
        subset=["athlete_id", "combine_season"]
    )
    out = panel.copy()
    out["athlete_id"] = pd.to_numeric(out["athlete_id"], errors="coerce")
    out["season"] = pd.to_numeric(out["season"], errors="coerce")
    out["_combine_year"] = out["season"] + int(combine_season_offset)
    lu_join = lu[
        ["athlete_id", "combine_season", "nba_combine_player_id"]
    ].drop_duplicates()
    m = out.merge(
        lu_join,
        left_on=["athlete_id", "_combine_year"],
        right_on=["athlete_id", "combine_season"],
        how="left",
    )
    m["Y_combine_meas"] = m["combine_season"].notna().astype(int)
    return m.drop(columns=["_combine_year", "combine_season"], errors="ignore")


if __name__ == "__main__":
    summary = run(None)
    print("Combine bridge:", summary)
