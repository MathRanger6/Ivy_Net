"""
Sports-Reference BPM **crosswalk**, **scrape job list**, and **raw → matched** merge.

Ports the durable-file workflow from ``bpm_merge_to_530_bkup.ipynb`` into callable Python so
``530_sports_pipeline.ipynb`` can refresh SR linkage without opening that notebook.

**Typical order (when SR data needs refresh):**

1. ``ensure_crosswalk()`` — maintain ``DO_NOT_ERASE/sr_school_slug_crosswalk.csv``.
2. ``write_scrape_jobs(panel)`` — write ``datasets/mbb/bpm_scrape_jobs.csv``.
3. ``scrape_bpm.run_batch()`` — extend ``bpm_player_season_raw.csv``.
4. ``run_match(panel=...)`` — write ``bpm_player_season_matched.csv`` + unmatched QA CSV.
5. ``panel_rebuild.build_from_box(cfg)`` (or merge) then ``apply_perf_metric_for_analysis``.

**One-shot:** ``run_sr_refresh_stage(cfg, panel)`` runs steps 1–4 in order (each step can be
disabled with ``do_crosswalk=`` … flags) and prints a single summary line.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

from sports_pipeline import paths


def normalize_player_name(name: Any) -> str:
    """Match key: lowercase, strip punctuation, drop Jr/Sr/II (same as legacy merge notebook)."""
    if pd.isna(name) or str(name).strip() == "":
        return ""
    s = str(name).lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+(jr|sr|ii|iii|iv|v)\s*$", "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def suggest_school_slug(team_short_display_name: str) -> str:
    """Heuristic SR slug from ESPN short name; often wrong — edit crosswalk CSV."""
    s = str(team_short_display_name).strip().lower()
    s = s.replace("&", "and")
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def ensure_crosswalk(cfg: Any | None = None) -> pd.DataFrame:
    """
    Load or create ``sr_school_slug_crosswalk.csv`` from ``mbb_df_team_box.csv``.

    Preserves user-edited ``school_slug`` values for known ``team_id``s; fills new teams
    with ``suggest_school_slug``.
    """
    _ = cfg
    team_box = paths.team_box_csv()
    cross_path = paths.sr_crosswalk_csv()
    cross_path.parent.mkdir(parents=True, exist_ok=True)

    usecols = ["team_id", "team_short_display_name"]
    tb = pd.read_csv(team_box, usecols=usecols, low_memory=False)
    tb = tb.dropna(subset=["team_id", "team_short_display_name"]).drop_duplicates(
        subset=["team_id", "team_short_display_name"]
    )

    if cross_path.is_file():
        existing = pd.read_csv(cross_path, low_memory=False)
        if "school_slug" not in existing.columns:
            raise ValueError(f"{cross_path} must contain column school_slug")
        base = tb.merge(
            existing[["team_id", "school_slug"]].drop_duplicates("team_id"),
            on="team_id",
            how="left",
        )
        miss = base["school_slug"].isna()
        if miss.any():
            base.loc[miss, "school_slug"] = base.loc[miss, "team_short_display_name"].map(
                suggest_school_slug
            )
        out = base[["team_id", "team_short_display_name", "school_slug"]].copy()
    else:
        out = tb.copy()
        out["school_slug"] = out["team_short_display_name"].map(suggest_school_slug)

    out = out.drop_duplicates(subset=["team_id"], keep="first")
    out.to_csv(cross_path, index=False)
    print(f"Crosswalk: {len(out)} rows → {cross_path}")
    return out


def write_scrape_jobs(panel: pd.DataFrame, cfg: Any | None = None) -> Path:
    """
    Unique ``(school_slug, sr_year)`` from panel + crosswalk → ``bpm_scrape_jobs.csv``.

    ``sr_year`` equals panel ``season`` (same convention as ``scrape_bpm.sr_year_from_box_season``).
    """
    _ = cfg
    cw_path = paths.sr_crosswalk_csv()
    if not cw_path.is_file():
        raise FileNotFoundError(f"Missing {cw_path}. Run bpm_merge.ensure_crosswalk() first.")
    cw = pd.read_csv(cw_path, low_memory=False)
    p = panel.drop(columns=["school_slug"], errors="ignore")
    need = p.merge(cw[["team_id", "school_slug"]], on="team_id", how="left")
    need = need.assign(sr_year=need["season"].astype(int))
    jobs = (
        need.dropna(subset=["school_slug"])
        .groupby(["school_slug", "sr_year"])
        .size()
        .reset_index(name="n_panel_rows")
        .sort_values(["sr_year", "school_slug"])
    )
    out = paths.bpm_scrape_jobs_csv()
    out.parent.mkdir(parents=True, exist_ok=True)
    jobs.to_csv(out, index=False)
    print(f"Scrape jobs: {len(jobs)} slug×season → {out}")
    return out


def run_match(
    cfg: Any | None = None,
    *,
    panel: pd.DataFrame | None = None,
    raw_path: Path | None = None,
    crosswalk: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Match ``bpm_player_season_raw`` rows onto panel rows; write matched + unmatched CSVs.

    If ``panel`` is ``None``, reads ``player_season_panel_530.csv`` (must include
    ``athlete_display_name``). For a panel built only from box, pass the DataFrame from
    ``panel_rebuild.build_from_box`` instead.
    """
    _ = cfg
    panel_path = paths.panel_530_csv()
    raw_p = raw_path or paths.bpm_raw_csv()
    matched_out = paths.bpm_matched_csv()
    unmatched_out = paths.bpm_panel_rows_unmatched_csv()

    if panel is None:
        if not panel_path.is_file():
            raise FileNotFoundError(
                f"Missing {panel_path}. Pass panel=DataFrame from panel_rebuild.build_from_box, "
                "or export a panel CSV with athlete_display_name."
            )
        panel_df = pd.read_csv(panel_path, low_memory=False)
    else:
        panel_df = panel.copy()

    if "athlete_display_name" not in panel_df.columns:
        raise ValueError("Panel must contain athlete_display_name for name matching.")
    if not raw_p.is_file():
        raise FileNotFoundError(
            f"Missing {raw_p}. Run scrape_bpm.run_batch after bpm_scrape_jobs.csv exists."
        )

    bpm = pd.read_csv(raw_p, low_memory=False)
    req = {"school_slug", "Player", "sr_year", "MP"}
    miss = req - set(bpm.columns)
    if miss:
        raise ValueError(f"bpm_player_season_raw.csv missing columns: {miss}")
    if "BPM" not in bpm.columns:
        bpm["BPM"] = float("nan")

    if crosswalk is None:
        cw_path = paths.sr_crosswalk_csv()
        if not cw_path.is_file():
            raise FileNotFoundError(f"Missing {cw_path}. Run ensure_crosswalk() first.")
        cw = pd.read_csv(cw_path, low_memory=False)
    else:
        cw = crosswalk

    if "school_slug" in panel_df.columns:
        panel_df = panel_df.drop(columns=["school_slug"])
    panel_df = panel_df.merge(cw[["team_id", "school_slug"]], on="team_id", how="left")
    panel_df["player_key"] = panel_df["athlete_display_name"].map(normalize_player_name)
    bpm = bpm.copy()
    bpm["player_key"] = bpm["Player"].map(normalize_player_name)
    bpm["sr_year"] = bpm["sr_year"].astype(int)
    panel_df["season"] = panel_df["season"].astype(int)

    bpm_sort = bpm.sort_values(
        ["school_slug", "sr_year", "player_key", "MP"],
        ascending=[True, True, True, False],
    )
    bpm_dedup = bpm_sort.drop_duplicates(
        subset=["school_slug", "sr_year", "player_key"], keep="first"
    )

    stat_cols = [
        c
        for c in ["PER", "TS%", "WS", "WS/40", "OBPM", "DBPM", "BPM", "MP", "G", "GS"]
        if c in bpm_dedup.columns
    ]
    rename_map = {"MP": "mp_sr", "TS%": "ts_pct_sr"}
    bpm_sub = bpm_dedup[["school_slug", "sr_year", "player_key"] + stat_cols].rename(
        columns=rename_map
    )

    # ``build_from_box`` left-merges the previous ``bpm_player_season_matched.csv`` onto the
    # panel, so ``panel_df`` may already contain BPM/OBPM/... . A second merge with ``bpm_sub``
    # collides on those names: pandas keeps the left column and renames the right to ``*_drop``,
    # and we drop ``*_drop`` below — which discards fresh SR stats and leaves only stale seasons
    # (e.g. 2011–2015) on the left. Drop overlapping SR columns before merging.
    _keep = {"school_slug", "player_key"}
    _overlap = [c for c in bpm_sub.columns if c in panel_df.columns and c not in _keep]
    panel_df = panel_df.drop(columns=_overlap, errors="ignore")

    merged = panel_df.merge(
        bpm_sub,
        left_on=["school_slug", "season", "player_key"],
        right_on=["school_slug", "sr_year", "player_key"],
        how="left",
        suffixes=("", "_drop"),
    )
    merged = merged.drop(columns=[c for c in merged.columns if c.endswith("_drop")], errors="ignore")
    merged = merged.drop(columns=["sr_year"], errors="ignore")

    merged["has_bpm"] = merged["BPM"].notna().astype(int) if "BPM" in merged.columns else 0
    rate = merged["has_bpm"].mean()
    print(f"Rows with BPM matched: {merged['has_bpm'].sum():,} / {len(merged):,} ({rate:.1%})")

    out_cols = [
        "athlete_id",
        "season",
        "team_id",
        "has_bpm",
    ] + [
        c
        for c in ["PER", "ts_pct_sr", "WS", "WS/40", "OBPM", "DBPM", "BPM", "mp_sr", "G", "GS"]
        if c in merged.columns
    ]
    matched_only = merged.loc[merged["has_bpm"] == 1, out_cols].drop_duplicates(
        subset=["athlete_id", "season", "team_id"]
    )
    matched_out.parent.mkdir(parents=True, exist_ok=True)
    matched_only.to_csv(matched_out, index=False)
    print(f"Wrote {matched_out} rows: {len(matched_only):,}")

    deb = [
        c
        for c in [
            "athlete_id",
            "season",
            "team_id",
            "athlete_display_name",
            "team_short_display_name",
            "school_slug",
            "player_key",
            "minutes",
            "ppm",
        ]
        if c in merged.columns
    ]
    unmatched = merged.loc[merged["has_bpm"] == 0, deb].copy()
    unmatched.to_csv(unmatched_out, index=False)
    print(f"Wrote {unmatched_out} rows: {len(unmatched):,} (QA)")

    return {
        "stage": "bpm_merge",
        "matched_path": str(matched_out),
        "unmatched_path": str(unmatched_out),
        "n_matched_rows": int(len(matched_only)),
        "n_unmatched_rows": int(len(unmatched)),
        "match_rate_rows": float(rate),
    }


def run_sr_refresh_stage(
    cfg: Any,
    panel: pd.DataFrame,
    *,
    do_crosswalk: bool = True,
    do_scrape_jobs: bool = True,
    do_scrape: bool = True,
    do_match: bool = True,
) -> dict[str, Any]:
    """
    Run the full SR maintenance chain in order: crosswalk → scrape jobs → network scrape →
    raw→matched. Pass the same ``panel`` you built in **CELL 4** (needs ``team_id``,
    ``season``). After this, re-run ``panel_rebuild.build_from_box(cfg)`` so SR columns
    refresh from ``bpm_player_season_matched.csv``.

    Toggle any step off when you only need part of the chain (e.g. ``do_scrape=False`` if
    raw is already complete). Network scrape requires ``pip install -e '.[scrape]'``.
    """
    out: dict[str, Any] = {"stage": "sr_refresh", "steps": {}}
    summary_bits: list[str] = []

    if do_crosswalk:
        cw = ensure_crosswalk(cfg)
        n_teams = len(cw)
        out["steps"]["crosswalk"] = {"n_teams": n_teams}
        summary_bits.append(f"crosswalk_teams={n_teams}")

    if do_scrape_jobs:
        jobs_path = write_scrape_jobs(panel, cfg)
        jobs = pd.read_csv(jobs_path, low_memory=False)
        n_jobs = len(jobs)
        out["steps"]["scrape_jobs"] = {"path": str(jobs_path), "n_slug_season": n_jobs}
        summary_bits.append(f"scrape_jobs={n_jobs}")

    if do_scrape:
        from sports_pipeline import scrape_bpm

        scrape_out = scrape_bpm.run_batch(pipeline_cfg=cfg)
        out["steps"]["scrape"] = scrape_out
        summary_bits.append(
            f"scrape_ok={scrape_out.get('n_ok', 0)} fail={scrape_out.get('n_fail', 0)}"
        )

    if do_match:
        match_out = run_match(cfg, panel=panel)
        out["steps"]["match"] = match_out
        summary_bits.append(
            f"matched_rows={match_out.get('n_matched_rows', 0)} "
            f"match_rate={match_out.get('match_rate_rows', 0):.1%}"
        )

    print("SR refresh — " + " | ".join(summary_bits) if summary_bits else "SR refresh — (no steps run)")
    return out
