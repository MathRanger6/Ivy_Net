# Charles → SCOUT: ESPN `"-"` placeholder rows in box data

**Date:** 2026-08-17  
**From:** Charles (via COMPASS chat)  
**To:** SCOUT  
**Priority:** Medium — blocks a clean roster-size figure for an advisor meeting; does **not** block PD21 ρ work if we keep min-minutes=20 on the hero panel.

---

## How to respond

| Field | Rule |
|-------|------|
| **Location** | `3-Master_Plan/` |
| **Filename** | `YYYYMMDD_HHMM_SCOUT_to_COMPASS_espn_dash_placeholder_rows.md` (use your local date/time) |
| **Format** | Numbered replies matching **Questions** below; cite file paths and (if you re-fetch) scrape logs |

Save the response file in `3-Master_Plan/` and notify Charles when complete. Do **not** edit this question file unless Charles asks.

---

## Background — what Charles was doing (you were not in this thread)

Charles is preparing for an **Alex Gates meeting (17 Aug 2026)**. Before defending **PD21 ρ / H_sort calibration**, Alex asked Charles to justify the **playing-time floor** on the college basketball panel (`min_minutes = 20` drop vs keeping sub-20 players with PPM = 0).

Charles ran a short diagnostic sprint documented as **“PD22”** (Paper Directions 22 — **not** a pipeline stage name in your code; just a meeting-prep folder under `HEROs_and_PASSes/`).

### Where to read Charles’s work

| What | Path (repo root relative) |
|------|---------------------------|
| **Start here — runbook** | [`3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/README.md`](re_entry/HEROs_and_PASSes/pd22_minutes/README.md) |
| **Full todo + figure narratives** | [`3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_minutes_panel_investigation_todo.md`](re_entry/HEROs_and_PASSes/pd22_minutes/PD22_minutes_panel_investigation_todo.md) |
| **Roster-size diagnostic script** | `sports/scripts/pd22_raw_roster_size_distribution.py` |
| **Roster-size figure (PNG)** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_distribution_2011_2021.png` |
| **Roster-size summary JSON** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_distribution_2011_2021.json` |
| **Per team-season counts CSV** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2011_2021_raw.csv` |
| **Backup slide (AUTO)** | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD22_raw_roster_size_distribution_AUTO.pptx` |

Related PD22 scripts (minutes / PPM / draft audit): same `sports/scripts/pd22_*.py` prefix; outputs all under `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/`.

### What the roster diagnostic does

`sports/scripts/pd22_raw_roster_size_distribution.py` calls **`panel_rebuild.build_from_box`** with `min_minutes=0`, then counts **distinct `(athlete_id, season, team_id)` rows per team-season**. That is “how many player-season rows sit on each roster” before the min-20 hero filter.

**Panel entry point you own:** `sports/sports_pipeline/panel_rebuild.py` → aggregates `datasets/mbb/mbb_df_player_box.csv`.

**Draft / alias work you helped Charles build** (`college_aliases.csv`, `draft_athlete_match.csv`, etc.) runs **later** and sets `Y_draft` — it does **not** assign `team_id` on box rows. Charles wants confirmation of that separation.

---

## What triggered this question

The roster-size histogram (`PD22_raw_roster_size_distribution_2011_2021.png`) has a long right tail. **Max roster_n = 115** (not ~120 — x-axis is histogram bin padding).

Forensics on **`datasets/mbb/mbb_df_player_box.csv`** (Aug 17 2026) show the max case is:

| Field | Value |
|-------|--------|
| School | **BYU** (`team_id=252`, ESPN short name `"BYU"`) |
| Season | **2018** |
| roster_n | **115** distinct athletes |
| Normal BYU seasons | ~12–20 athletes (e.g. 2017: 20, 2019: 15) |

**Cause (preliminary):** **99** of the 115 are placeholder rows with **`athlete_display_name == "-"`** (literal dash), **0 / NaN minutes**, all from **one game**:

- `game_id = 400986852`, date **2017-11-29**, BYU vs Utah Valley
- Same game: Utah Valley **16** players, **0** dash rows
- Other BYU 2018 games: median **14** players per game

Charles initially worried his **manual college/draft alias adjudication** had merged another school into BYU. Checks so far say **no**:

- `datasets/mbb/DO_NOT_ERASE/college_aliases.csv` — **no BYU rows**
- Only one ESPN `team_id` with short name `"BYU"` (BYU Hawaii is separate `team_id=2088`)
- `datasets/mbb/draft_athlete_match.csv` — 5 BYU rows, all `college = "BYU"`

So the spike appears to originate in **Stage 1 box data** (before draft match), not in Stage 2 adjudication.

---

## Global scope of `"-"` rows (2011–2021)

| Metric | Value |
|--------|--------|
| Player-season rows with name `"-"` | **175** |
| With minutes > 0 | **0** |
| Team-seasons affected | **5** |
| Distinct bad games | **5** |

**All five games:**

| game_id | date | team (dash rows) | dash count |
|---------|------|------------------|------------|
| 400986852 | 2017-11-29 | BYU | 99 |
| 400830589 | 2015-11-19 | Weber St | 45 |
| 400846817 | 2015-12-30 | Fort Valley St | 24 |
| 400990127 | 2017-11-19 | Kent State | 4 |
| 400990018 | 2017-11-29 | Delaware St | 3 |

Dash `athlete_id`s on BYU 2018 are a tight sequential block (~4289042–4289141).

**Charles’s lean (pending your answer):** drop `athlete_display_name.strip() == "-"` in **`panel_rebuild.build_from_box`** before aggregating to player-season. Blast radius: 175 rows; BYU 2018 would go 115 → **16**.

**Note:** The **min-minutes=20 hero panel** (used in PD21 ρ / empirical caps) already excludes these (NaN minutes). This mainly affects **min=0** raw diagnostics and the backup roster slide.

---

## Questions for SCOUT

### Q1 — Root cause: our scrape vs ESPN source?

Did these `"-"` rows enter `mbb_df_player_box.csv` because of **our Stage 1 ingest/scrape** (timeout, partial JSON, retry with empty slots, sportsdataverse parser bug, etc.), or because **ESPN already returned** unnamed placeholder roster slots for those games?

Please trace **box ingest** for the five `game_id`s above. Specifically:

1. Is there scrape-log / retry / error evidence (timeouts, 429, truncated responses) for those games?
2. Can you **re-fetch game 400986852** today and see whether ESPN still returns ~99 unnamed BYU slots vs a normal ~15-man box?
3. **Only the home team bloats** in that game (BYU 99 dash, Utah Valley 0 in the same box). Does that fit a known **ingest bug** or an **ESPN-side quirk**?

**Relevant code/docs:**

- [`sports/documents/SPORTS_DATA_GAMEPLAN.md`](../sports/documents/SPORTS_DATA_GAMEPLAN.md) — **Stage 1 — Spine from BOX data**
- Legacy ingest may live in obsolete snapshots under `obsolete_documents/sports_gameplan_old/` or the conductor notebook — please point Charles to the **current** scrape entry point if it moved into `sports_pipeline/`

### Q2 — Policy after Q1

Recommend one of:

- **(a)** Permanent filter: drop `athlete_display_name == "-"` at panel build
- **(b)** Re-scrape / repair those five games at source
- **(c)** Both

Any reason **not** to drop `"-"` rows (e.g. intentional sentinel)?

### Q3 — Confirm pipeline separation

Confirm explicitly for Charles:

> Draft matching + `college_aliases` adjudication **cannot** inflate `(team_id, season)` roster counts — only `Y_draft` and related flags — unless box CSVs were hand-edited.

If that’s wrong, say where team assignment can still go wrong.

### Q4 — Related outliers (no `"-"` name)

The PD22 roster CSV also shows **>50** player-seasons for some small schools with **real names** and **zero minutes**, often **one inflated game** (e.g. Jarvis Chr 2016: 68 athletes, 62 in one game; Webber Int 2014: all 52 in one game). Same scrape pathology, or a separate box-QC rule?

See: `PD22_raw_roster_size_by_team_season_2011_2021_raw.csv` — filter `roster_n > 50`.

### Q5 — PD21 / hero panel

Is **`min_minutes = 20`** sufficient hygiene for ρ / empirical roster-cap work, or should box-QC (dash filter, per-game cap, exhibition exclusion) run **before** Charles cites raw roster-size numbers to Alex?

---

## Primary data files (for your investigation)

```
datasets/mbb/mbb_df_player_box.csv          # source box game logs
datasets/mbb/mbb_df_team_box.csv             # team_id ↔ display names
datasets/mbb/DO_NOT_ERASE/college_aliases.csv
datasets/mbb/draft_athlete_match.csv
sports/sports_pipeline/panel_rebuild.py     # aggregation + min_minutes filter
```

---

## One-line ask from Charles

*“I need to know whether `"-"` players are permanent ESPN/scrape junk we should filter at panel build, or a scrape bug we should re-run — and confirmation that my draft/school matching didn’t cause the BYU 115-man roster.”*
