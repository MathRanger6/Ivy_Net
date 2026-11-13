# MBB data sources register — Chapter 3 (SCOUT)

**Charles / FOUNDY** | 13 November 2026 | **Living doc** — extend as provenance is confirmed; no new scraping in this pass.

**Purpose:** One table of **where files come from**, what the pipeline uses them for, and what is **verified on disk today** vs **needs Charles’s memory or a one-line file header**.

**Canonical wiring:** `sports/sports_pipeline/paths.py`, `sports/documents/SPORTS_DATA_GAMEPLAN.md`, `datasets/mbb/DO_NOT_ERASE/README.txt`.

---

## Pipeline layers (read order)

```text
[1] ESPN college box (game-level)     → mbb_df_player_box.csv (+ team box, schedule)
[2] NBA draft register                → DO_NOT_ERASE/nbaplayersdraft.csv
[3] Draft ↔ ESPN match                → draft_athlete_match.csv → athlete_id_draft_lookup.csv
[4] Optional SR advanced scrape       → DO_NOT_ERASE/bpm_player_season_raw.csv → matched
[5] Panel + LOO + filters             → player_season_panel_530.csv
[6] Pass A HERO (Ch.3 figure)         → pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.*
```

**Chapter 3 locked window:** collegiate seasons **2009–2021** on the panel/HERO run (`HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json`). **Not** the full span on disk for box (see below).

---

## Source register

| # | File (repo path) | One row represents | External source (as documented) | How obtained | Season / years on disk today | Used in Ch.3 lock? | Status |
|---|------------------|--------------------|---------------------------------|----------------|------------------------------|--------------------|--------|
| 1 | `datasets/mbb/mbb_df_player_box.csv` | One **game** appearance (player in a game) | **ESPN** men's college basketball box scores via **sportsdataverse** / **hoopR** ecosystem (`ingest_box.py`, `data_integrity.py`) | Historical: legacy **sdv_first** notebook ingest; frozen CSV on disk. **`ingest_box.py` is a stub** (skip if file exists). | **2003–2025** game rows (**verified** 13 Nov 2026) | **Yes** — aggregated to 2009–2021 for HERO | **Verified** coverage; **TK** exact download command/date |
| 2 | `datasets/mbb/mbb_df_team_box.csv` | Team-game box | Same ESPN / SDV spine | Same lineage as (1) | Present (not re-counted today) | Supporting spine | **Verified** file; **TK** ingest date |
| 3 | `datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv` | Drafted player **career summary** row in register (not one row per pick only) | Advisor memos: **Basketball-Reference** NBA draft; gameplan: static register. **SpecStory (Aug 2026):** may be GitHub/hoopR-style table — **not proven from file metadata** | One-time CSV into `DO_NOT_ERASE/` | **`year` 1989–2021**, 1,922 rows (**verified**) | **Yes** — Y_draft link for college athletes in window | **Verified** counts; **TK** original URL/repo |
| 4 | `datasets/mbb/draft_athlete_match.csv` | Draft row + match diagnostics | **Derived** — matcher output (legacy `sdv_second` / future `draft_match.py`) | Pipeline stage 2 | All matcher attempts | Link stage | **Verified** role; **TK** match-rate table in methods |
| 5 | `datasets/mbb/athlete_id_draft_lookup.csv` | Drafted athlete → `athlete_id` | **Derived** from (3)+(1) + `college_aliases.csv` | Pipeline / notebook | **789** rows, draft years **2005–2021** max (**documented** SCOUT Q&A Aug 2026) | **Yes** — defines `Y_draft` in panel | **Recalled** counts; re-verify before print |
| 6 | `datasets/mbb/DO_NOT_ERASE/college_aliases.csv` | Draft college string → ESPN school display | **Hand-curated** crosswalk | Human QA loops (gameplan Stage 2a) | Living file | **Yes** — match quality | **Verified** role |
| 7 | `datasets/mbb/DO_NOT_ERASE/sr_school_slug_crosswalk.csv` | ESPN `team_id` → SR school slug | **Hand-curated** + heuristics | SR scrape prep | Living | **No** for PPM-only HERO | **Verified** role |
| 8 | `datasets/mbb/DO_NOT_ERASE/bpm_player_season_raw.csv` | Player-season on SR advanced page | **Sports-Reference.com** /cbb (scrape) | Custom scraper (`scrape_bpm.py` lineage) | Multi-season; expensive to refresh | **No** for canonical HERO (PPM) | **Verified** role |
| 9 | `datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv` | SR row on `(athlete_id, season, team_id)` | **Derived** merge | Merge notebook / `bpm_merge` | Living | Sensitivity / `PERF_METRIC` switches | **Verified** role |
| 10 | `datasets/mbb/player_season_panel_530.csv` | Player-season-team analysis row | **Derived** — `panel_rebuild.build_from_box` + draft + optional BPM | `530_sports_pipeline.ipynb` / `panel_rebuild.py` | Depends on rebuild config | Intermediate | **Verified** file exists |
| 11 | `datasets/mbb/DO_NOT_ERASE/basketball/csv/*.csv` | NBA league tables (draft history, combine, etc.) | **NBA**-style exports (`draft_history.csv`, `draft_combine_stats.csv`, …) | Bundled reference / combine bridge | Not fully inventoried today | **No** Ch.3 main text (combine bridge optional) | **Verified** folder; **TK** Charles: which package (nba_api?) |
| 12 | `datasets/mbb/DO_NOT_ERASE/all_seasons.csv` | **NBA** player-season (pro), not college | Likely NBA stats export (columns: `team_abbreviation`, `season` 1996-97, …) | Bundled in `DO_NOT_ERASE` | Pro seasons | **Not** college Ch.3 spine | **Verified** peek; **out of scope** for MBB HERO |

---

## What Chapter 3 prose should cite

| Concept | Cite in print (suggested) |
|---------|---------------------------|
| College performance | ESPN-college box scores accessed via **sportsdataverse** / **hoopR** (add package citations Charles uses). |
| Draft outcome | NBA draft register (`nbaplayersdraft.csv`); methods: match to ESPN athletes by name + college + **hand-audited** aliases. |
| Optional advanced stats | Sports-Reference scrape; **not** the primary Ch.3 performance measure. |

Early advisor memos (`sports/documents/sports_mechanisms/college_basketball_empirical_design.md`) list **Sports-Reference (college)** and **Basketball-Reference (draft)** URLs — align Ch.3 with **actual** pipeline: **ESPN box spine + SR scrape for BPM**, **draft register** for Y.

---

## Gaps to close (Charles / SCOUT, no scraping required)

1. **`nbaplayersdraft.csv`** — one sentence: downloaded from **[URL or R script name]** on **[date]**; confirm Basketball-Reference vs hoopR export.
2. **`mbb_df_player_box.csv`** — last full refresh: **command** (R `load_mbb_player_box()` or Python SDV) and **date**; note file already contains **through 2025** while Ch.3 uses **2009–2021**.
3. **`athlete_id_draft_lookup.csv`** — publish **match rate** and **manual review count** in flow table (A5).
4. **`all_seasons.csv` / `basketball.zip`** — label as **NBA sidecar** or archive; remove from “college sources” unless repurposed.

---

## Related repo docs (not duplicates of this register)

| Doc | Role |
|-----|------|
| `sports/documents/SPORTS_DATA_GAMEPLAN.md` | Forward pipeline contract |
| `talent/documents/Scout_background_CBB_pool_quality_draft_rate.md` | Short source list (pre-Ch.3) |
| `3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md` | Draft register years, box 2022–25 |
| `5-Manuscript/03_Data_and_Empirics/notes/20261113_SCOUT_Response_Ch3_basketball.md` | Full A+B answers (A2/A3 cross-link this register) |
| `5-Manuscript/03_Data_and_Empirics/notes/20261113_Ch3_Questions_for_SCOUT_and_PEER.md` | FOUNDY questionnaire (SCOUT doc list includes register) |

---

## Thread log

- **2026-11-13** — SCOUT created register; box seasons **2003–2025** verified; Ch.3 HERO lock **2009–2021**.
