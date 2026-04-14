"""
Summaries for BOX vs draft linkage vs the panel subset used in EDA (plot window).

**BOX** = ESPN / sportsdataverse game-level `mbb_df_player_box.csv`.
**Draft** = `nbaplayersdraft` register + `draft_athlete_match` + `athlete_id_draft_lookup`.

The “analysis window” matches `panel_build.filter_panel` (same rows as ventile plots)
unless `CFG.analysis_season_min/max` override it. Reading the full BOX file uses three
columns only but can take ~10s on large extracts.
"""

from __future__ import annotations

from io import StringIO
from typing import Any

import pandas as pd

from sports_pipeline import paths
from sports_pipeline.panel_build import filter_panel


def _season_window_from_use(use: pd.DataFrame, cfg: Any) -> tuple[int, int]:
    lo = getattr(cfg, "analysis_season_min", None)
    hi = getattr(cfg, "analysis_season_max", None)
    if lo is not None and hi is not None:
        return int(lo), int(hi)
    s = use["season"].astype(int)
    return int(s.min()), int(s.max())


def _draft_year_window(s_lo: int, s_hi: int, cfg: Any) -> tuple[int, int]:
    b = int(getattr(cfg, "draft_year_before_season", 1))
    a = int(getattr(cfg, "draft_year_after_season", 5))
    return s_lo - b, s_hi + a


def summarize_data_integrity(panel: pd.DataFrame, cfg: Any) -> str:
    """
    BOX (game-level CSV), draft register, draft→athlete match file, and the same
    `filter_panel` subset used for ventile plots. Large BOX read (3 cols only).
    """
    buf = StringIO()
    w = buf.write

    use = filter_panel(panel, cfg)
    s_lo, s_hi = _season_window_from_use(use, cfg)
    dy_lo, dy_hi = _draft_year_window(s_lo, s_hi, cfg)

    w("=== Data integrity (aligned with ventile-plot sample) ===\n\n")

    w("**Analysis window (collegiate seasons in plot sample `use`)**\n")
    w(f"- Seasons: {s_lo}–{s_hi} (override with CFG.analysis_season_min / max if set)\n")
    w(
        f"- After `dropna(poolq_loo, Y_draft)`"
        + (
            f" and minutes ≥ {getattr(cfg, 'min_minutes', 0)}"
            if float(getattr(cfg, "min_minutes", 0)) > 0
            else ""
        )
        + ":\n"
    )
    w(f"  - Player–season rows: {len(use):,}\n")
    w(f"  - Unique athletes: {use['athlete_id'].nunique():,}\n")
    w(f"  - Unique teams (team_id): {use['team_id'].nunique():,}\n")
    w(f"  - Share of rows with Y_draft=1: {use['Y_draft'].mean():.2%}\n\n")

    w("**BOX (`mbb_df_player_box.csv`, game-level; athlete_id × season × team_id)**\n")
    p_box = paths.player_box_csv()
    if not p_box.is_file():
        w(f"- FILE MISSING: {p_box}\n\n")
    else:
        box = pd.read_csv(
            p_box,
            usecols=["athlete_id", "season", "team_id"],
            low_memory=False,
        )
        w(f"- All seasons in file: {int(box['season'].min())}–{int(box['season'].max())}\n")
        w(f"- Unique athletes (all seasons): {box['athlete_id'].nunique():,}\n")
        w(f"- Unique teams (all seasons): {box['team_id'].nunique():,}\n")
        w(f"- Game-level rows: {len(box):,}\n")
        bw = box[(box["season"] >= s_lo) & (box["season"] <= s_hi)]
        w(
            f"- Within analysis seasons {s_lo}–{s_hi}: "
            f"{bw['athlete_id'].nunique():,} athletes, "
            f"{bw['team_id'].nunique():,} teams, "
            f"{len(bw):,} game rows\n"
        )
        pst = bw.drop_duplicates(["athlete_id", "season", "team_id"])
        w(f"  - Distinct (athlete_id, season, team_id) in window: {len(pst):,}\n\n")

    w("**Draft register (`DO_NOT_ERASE/nbaplayersdraft.csv`)**\n")
    p_reg = paths.nbaplayersdraft_csv()
    if not p_reg.is_file():
        w(f"- FILE MISSING: {p_reg}\n\n")
    else:
        reg = pd.read_csv(p_reg, low_memory=False)
        ycol = "year" if "year" in reg.columns else None
        if ycol:
            w(
                f"- Rows: {len(reg):,}; draft `year` range: "
                f"{int(reg[ycol].min())}–{int(reg[ycol].max())}\n"
            )
        else:
            w(f"- Rows: {len(reg):,} (no `year` column found)\n")
        w("\n")

    w("**Draft→athlete pipeline (`draft_athlete_match.csv`)**\n")
    p_m = paths.draft_athlete_match_csv()
    if not p_m.is_file():
        w(f"- FILE MISSING: {p_m}\n\n")
    else:
        dm = pd.read_csv(p_m, low_memory=False)
        if "year" not in dm.columns:
            w("- No `year` column; skipping draft-year window rates.\n\n")
        else:
            in_win = dm[(dm["year"] >= dy_lo) & (dm["year"] <= dy_hi)]
            n_in = len(in_win)
            w(
                f"- All rows: {len(dm):,}; draft years used for window: "
                f"{dy_lo}–{dy_hi} (season window {s_lo}–{s_hi} minus "
                f"{getattr(cfg, 'draft_year_before_season', 1)} / plus "
                f"{getattr(cfg, 'draft_year_after_season', 5)})\n"
            )
            w(f"- Draft picks in that draft-year band: {n_in:,}\n")
            if n_in > 0:
                has_ath = in_win["athlete_id"].notna()
                w(
                    f"  - With `athlete_id` (player matched to spine): "
                    f"{has_ath.sum():,} ({has_ath.mean():.1%})\n"
                )
                has_team = in_win["team_short_display_name"].notna()
                w(
                    f"  - With ESPN `team_short_display_name` (school mapped): "
                    f"{has_team.sum():,} ({has_team.mean():.1%})\n"
                )
            w("\n")

    w("**Lookup table (`athlete_id_draft_lookup.csv`)**\n")
    p_lu = paths.draft_lookup_csv()
    if not p_lu.is_file():
        w(f"- FILE MISSING: {p_lu}\n\n")
    else:
        lu = pd.read_csv(p_lu, low_memory=False)
        w(f"- Linked athlete rows: {len(lu):,}\n")
        if "draft_year" in lu.columns:
            w(
                f"- draft_year range in lookup: "
                f"{int(lu['draft_year'].min())}–{int(lu['draft_year'].max())}\n"
            )
        w("\n")

    w("**Cached diagnostic summary (if present)**\n")
    p_sum = paths.draft_match_diagnostic_summary_csv()
    if p_sum.is_file():
        sm = pd.read_csv(p_sum)
        def _val(cat, sub, met):
            r = sm[(sm["category"] == cat) & (sm["subcategory"] == sub) & (sm["metric"] == met)]
            return int(r["value"].iloc[0]) if len(r) else None

        dr = _val("total", "all", "draft_rows")
        ma = _val("total", "all", "matched_athlete_id")
        if dr is not None and ma is not None:
            w(f"- From `draft_match_diagnostic_summary.csv`: draft_rows={dr}, matched_athlete_id={ma} ")
            w(f"({ma}/{dr} = {ma/dr:.1%} global pipeline player-match)\n")
    else:
        w("- (no `draft_match_diagnostic_summary.csv`)\n")

    return buf.getvalue()


def summarize_unmatched_schools_draft(cfg: Any) -> str:
    """
    Colleges that appear on the NBA draft register but did not map to your ESPN/school
    linkage (QA table from the draft-match stage).
    """
    buf = StringIO()
    w = buf.write
    p = paths.draft_unmapped_colleges_csv()
    w("**Draft — colleges with no school map**\n")
    if not p.is_file():
        w(
            f"- File missing: `{p}`\n"
            "- If you run a draft-match export that writes `draft_unmapped_colleges.csv`, "
            "those rows list register strings (often JUCO, small colleges, alternate names) "
            "that never linked to `team_short_display_name` / spine.\n\n"
        )
        return buf.getvalue()
    df = pd.read_csv(p, low_memory=False)
    if df.empty:
        w(f"- `{p.name}` exists but is empty.\n\n")
        return buf.getvalue()
    n = len(df)
    col = "college" if "college" in df.columns else None
    if col is None:
        w(f"- `{p.name}` has unexpected columns; expected `college`. Showing head:\n{df.head()}\n\n")
        return buf.getvalue()
    w(f"- Source: `{p}`\n")
    w(f"- **{n:,}** distinct college strings on the draft register without a map\n")
    mx = getattr(cfg, "unmatched_school_report_max_lines", None)
    show = df.sort_values(col).reset_index(drop=True)
    if mx is not None and n > int(mx):
        w(f"- (Printing first {int(mx):,} alphabetically; see CSV for the full list.)\n")
        show = show.head(int(mx))
    for _, row in show.iterrows():
        name = row[col]
        extra = []
        if "n_draft_picks" in df.columns and pd.notna(row.get("n_draft_picks")):
            extra.append(f"n_picks={int(row['n_draft_picks'])}")
        if "years" in df.columns and pd.notna(row.get("years")):
            extra.append(f"years={row['years']}")
        suf = f"  ({'; '.join(extra)})" if extra else ""
        w(f"  - {name}{suf}\n")
    if mx is not None and n > int(mx):
        w(f"  … and {n - int(mx):,} more in `{p.name}`\n")
    w("\n")
    return buf.getvalue()


def summarize_unmatched_schools_sr(cfg: Any) -> str:
    """
    ESPN ``team_id`` / display names where panel rows have no SR BPM merge hit.

    Reflects the **last** ``bpm_merge.run_match`` write to ``bpm_panel_rows_unmatched.csv``
    (player-level QA, aggregated here by school).
    """
    buf = StringIO()
    w = buf.write
    p = paths.bpm_panel_rows_unmatched_csv()
    w("**Sports Reference — ESPN teams with no BPM row match**\n")
    if not p.is_file():
        w(
            f"- File missing: `{p}`\n"
            "- Produced when you run SR refresh / `bpm_merge.run_match`. Until then there is "
            "no row-level QA file to aggregate.\n\n"
        )
        return buf.getvalue()
    df = pd.read_csv(p, low_memory=False)
    if df.empty:
        w(f"- `{p.name}` exists but is empty (all panel rows matched SR raw in the last run).\n\n")
        return buf.getvalue()
    need = {"team_id", "team_short_display_name"}
    if not need.issubset(df.columns):
        w(f"- `{p.name}` missing columns {need - set(df.columns)}; cannot aggregate by school.\n\n")
        return buf.getvalue()
    slug_col = "school_slug" if "school_slug" in df.columns else None
    gcols = ["team_id", "team_short_display_name"] + ([slug_col] if slug_col else [])
    agg = df.groupby(gcols, dropna=False, as_index=False).size().rename(columns={"size": "n_unmatched_rows"})
    agg = agg.sort_values("n_unmatched_rows", ascending=False).reset_index(drop=True)
    n_teams = len(agg)
    n_rows = int(agg["n_unmatched_rows"].sum())
    w(f"- Source: `{p}` (last `run_match` output)\n")
    w(
        f"- **{n_teams:,}** distinct ESPN teams × name (+ slug) with at least one "
        f"unmatched player-season row; **{n_rows:,}** such rows total\n"
    )
    w(
        "- Typical causes: SR slug wrong or missing in crosswalk/aliases, no scrape for that "
        "slug×season, or player name normalization mismatch vs SR roster.\n"
    )
    mx = getattr(cfg, "unmatched_school_report_max_lines", None)
    show = agg
    if mx is not None and n_teams > int(mx):
        w(f"- (Printing top {int(mx):,} teams by unmatched row count; see CSV for full detail.)\n")
        show = show.head(int(mx))
    # Fixed-width-ish columns for copy/paste
    for _, row in show.iterrows():
        tid = row["team_id"]
        tname = row["team_short_display_name"]
        slug = row[slug_col] if slug_col else ""
        cnt = int(row["n_unmatched_rows"])
        slug_s = f"  slug={slug}" if slug_col and pd.notna(slug) and str(slug).strip() else ""
        w(f"  - team_id={tid}  {tname}{slug_s}  (n_unmatched_rows={cnt:,})\n")
    if mx is not None and n_teams > int(mx):
        w(f"  … and {n_teams - int(mx):,} more teams in `{p.name}`\n")
    w("\n")
    return buf.getvalue()


def print_unmatched_school_reports(cfg: Any) -> None:
    """
    Print draft-register colleges without a map + ESPN teams with SR merge gaps.

    Controlled by ``CFG.print_unmatched_school_lists``; line cap via
    ``CFG.unmatched_school_report_max_lines`` (``None`` = no cap).
    """
    print("=== Unmatched schools (draft register vs SR merge QA) ===\n")
    print(summarize_unmatched_schools_draft(cfg))
    print(summarize_unmatched_schools_sr(cfg))


def print_data_integrity(panel: pd.DataFrame, cfg: Any) -> None:
    print(summarize_data_integrity(panel, cfg))
