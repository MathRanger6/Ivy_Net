# SCOUT → COMPASS: ESPN `"-"` placeholder rows in box data

**Date:** 2026-08-17  
**From:** SCOUT  
**To:** COMPASS (for Charles)  
**Re:** `20260817_1606_Charles_to_SCOUT_espn_dash_placeholder_rows.md`

---

## Executive summary

Charles’s BYU 2018 **115-man roster** spike is **not** from draft matching or `college_aliases`. It is **frozen ESPN box junk** in `datasets/mbb/mbb_df_player_box.csv`: 99 rows with `athlete_display_name == "-"` from a single game (`400986852`). I **re-fetched that game from ESPN’s public summary API today (2026-08-17)** — ESPN **still** returns 113 BYU athlete slots, **99** with display name `"-"`. Re-scraping without a filter would reproduce the same rows.

**Recommendation:** **(c) both**, but treat **(a) a permanent dash filter in `panel_rebuild.build_from_box`** as the real fix; **(b) re-scrape** the five games is optional hygiene only (won’t remove ESPN placeholders). For **PD21 ρ / hero panel**, **`min_minutes = 20` is sufficient**; for **PD22 raw roster diagnostics** (`min_minutes=0`), apply the dash filter or add a slide footnote before citing counts to Alex.

---

## Q1 — Root cause: our scrape vs ESPN source?

### 1. Scrape-log / retry evidence

**None found in-repo for these five games.**

- Current Stage 1 entry point: `sports/sports_pipeline/ingest_box.py` — **placeholder only** (checks that `mbb_df_player_box.csv` exists; does **not** re-fetch).
- Legacy ingest lived in **`sdv_first`** (removed from repo root 2026-03-31 per `sports/documents/SPORTS_DATA_GAMEPLAN.md`); salvage is under `obsolete_documents/sports_gameplan_old/` / `obsolete_files/sports_gameplan_old/` (not searched for per-game logs in this pass).
- No scrape-log artifacts under `datasets/mbb/` matching these `game_id`s.

**Conclusion:** We cannot attribute the dash rows to a **transient** timeout/partial-response bug from our side. The frozen CSV matches **live ESPN** (see below).

### 2. Re-fetch game `400986852` (2026-08-17)

**Endpoint:** `https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?event=400986852`

| Team | Live ESPN athletes | Live `"-"` names | Frozen CSV (same game) |
|------|-------------------:|-----------------:|-----------------------:|
| BYU (`team_id=252`) | 113 | **99** | 113 rows, 99 dash |
| Utah Valley (`3084`) | 16 | 0 | 16 rows, 0 dash |

- Live dash `athlete_id`s are the same sequential block as in the frozen file (**4289042–4289141**).
- All dash rows: **0 minutes** in both live API stats and frozen CSV; **0** dash rows globally have `minutes > 0` (2011–2021).

**Verdict:** Placeholders are **present in ESPN’s source today**, not an artifact introduced after ingest.

### 3. One-sided home-team bloat

Pattern holds for **all five dash games** — **only one team per game** carries dash rows; the opponent is normal (~15–21 players):

| game_id | date | team with dash rows | dash | opponent | opponent dash |
|---------|------|---------------------|-----:|----------|--------------:|
| 400986852 | 2017-11-29 | BYU (home) | 99 | Utah Valley | 0 |
| 400830589 | 2015-11-20 | Weber St | 45 | Antelope Valley | 0 |
| 400846817 | 2015-12-31 | Fort Valley St | 24 | Alabama St | 0 |
| 400990127 | 2017-11-19 | Kent State | 4 | Miss Valley St | 0 |
| 400990018 | 2017-11-30 | Delaware St | 3 | Binghamton | 0 |

Live re-fetch confirmed the same one-sided counts for `400830589`, `400846817`, `400990127`, and `400990018`.

This fits an **ESPN-side box-score quirk** (unnamed roster slots on one side of specific games), **not** a draft/alias merge and **not** strong evidence of a **our-side** parser doubling rows across both teams. The sequential fake IDs are consistent with ESPN assigning placeholder athlete records that our ingest faithfully copied.

**Current scrape entry point for Charles:** `sports/sports_pipeline/ingest_box.py` (stub). Full refresh logic is still **TODO** — factor from `sdv_first` per gameplan. Until implemented, box CSV is treated as **frozen Stage 1 truth**.

---

## Q2 — Policy after Q1

**Recommend (c) both, with priorities:**

| Option | SCOUT view |
|--------|------------|
| **(a) Filter `"-"` at panel build** | **Do this.** Zero blast radius on substance: 175 player-season rows (2011–2021), all 0/NaN minutes. BYU 2018: 115 → **16**. Implement in `sports/sports_pipeline/panel_rebuild.py` inside `build_from_box`, **before** the `groupby`, e.g. drop rows where `athlete_display_name.astype(str).str.strip() == "-"`. |
| **(b) Re-scrape / repair five games** | **Low value** for dash rows — live ESPN still serves them. Repair would only help if ESPN fixes the API later. Optional when `ingest_box.run()` is implemented (force-refresh flag per `game_id`). |
| **(c) Both** | **Yes** — filter now for all downstream consumers; note five `game_id`s in ingest TODO / data QC doc for optional refresh. |

**Any reason not to drop `"-"` rows?** **No.** They are not a documented sentinel in our pipeline; they carry no minutes or points; they are not real athletes. I found **no** intentional use of `"-"` as a coding convention in `sports_pipeline/`.

---

## Q3 — Confirm pipeline separation

**Confirmed for Charles:**

> Draft matching + `college_aliases` adjudication **cannot** inflate `(team_id, season)` roster counts — only `Y_draft` and related draft/combine flags — unless box CSVs were hand-edited.

**Evidence:**

1. **`panel_rebuild.build_from_box`** (`sports/sports_pipeline/panel_rebuild.py`):
   - Reads **`team_id` only from `mbb_df_player_box.csv`**, aggregates to `(athlete_id, season, team_id)`.
   - Applies **`min_minutes`** filter on aggregated minutes.
   - Attaches **`Y_draft`** via left join to `athlete_id_draft_lookup.csv` (`isin` on `athlete_id`) — **does not read `college_aliases.csv`**.
   - Optional SR merge adds stat columns on the same keys; **does not reassign team**.

2. **`college_aliases.csv`** is Stage **2a** (draft `college` string → ESPN school for **matching**), per `sports/documents/SPORTS_DATA_GAMEPLAN.md`. It influences **which spine athletes are candidates for a draft row**, not box row `team_id`.

3. **`draft_match.py`** is also a stub that skips when lookup exists; it does not rewrite box.

**Where team assignment can still go wrong (not Charles’s case):**

- **Hand-editing** `mbb_df_player_box.csv` (wrong `team_id` on rows).
- **Upstream ESPN/SDV ingest bug** that assigns wrong `team_id` when flattening box JSON (would affect **both** teams’ rows differently from alias merge — not observed here).
- **Draft match mis-link** could mark the wrong athlete as `Y_draft=1` but would **not** add roster rows or move an athlete to BYU unless the box already had that `(athlete_id, season, team_id)`.

Charles’s checks (no BYU rows in `college_aliases`, single BYU `team_id`, sane `draft_athlete_match.csv`) align with this.

---

## Q4 — Related outliers (no `"-"` name)

**Separate pathology from dash placeholders**, but same **family** of “one game inflates team-season roster count.”

Seven team-seasons with `roster_n > 50` in 2011–2021 (raw panel, `min_minutes=0`):

| season | team_id | school (ESPN short) | roster_n | dash in season? | dominant game | players in that game |
|--------|--------:|---------------------|---------:|-----------------|---------------|---------------------:|
| 2018 | 252 | BYU | 115 | 99 dash rows | 400986852 | 113 |
| 2016 | 2692 | Weber St | 61 | 45 dash (other game) | 400830589 | 61 |
| 2016 | 2299 | Jarvis Chr | 68 | 0 | 400843478 | 62 |
| 2014 | 2691 | Webber Int | 52 | 0 | 400499056 | 52 |
| 2015 | 2299 | Jarvis Chr | 52 | 0 | 400595624 | 52 |
| 2021 | 2721 | Whitworth | 52 | 0 | 401274903 | 52 |
| 2021 | 2235 | Fresno Pacific | 51 | 0 | 401268802 | 46 |

**Non-dash cases (e.g. Jarvis Christian 2016, Webber International 2014):**

- **Real display names**, not `"-"`.
- **One game** accounts for almost all inflation (62/68 and 52/52).
- Many rows have **0 minutes** in that game (Jarvis `400843478`: 49/62 at 0 min; only 13 with minutes > 0).
- **Live ESPN re-fetch today** still returns 62 (Jarvis) and 52 (Webber) athletes — same as frozen CSV.

**Interpretation:** Likely **ESPN listing full nominal rosters** (exhibition, early-season multi-team events, or D-II/NAIA games with loose box hygiene) rather than alias merge or dash placeholders. **Not fixed by the dash filter alone.**

**Suggested box-QC rules (future, not blocking PD21):**

- Per-game cap on distinct `athlete_id` per team (e.g. flag if > 25).
- Optional exhibition / season-type filter when schedule metadata supports it.
- For PD22 slide: footnote that tail includes **ESPN box anomalies**, not model roster size.

---

## Q5 — PD21 / hero panel

| Use case | `min_minutes = 20` enough? |
|----------|----------------------------|
| **PD21 ρ / H_sort / empirical roster caps / hero LPM** | **Yes.** Dash rows have 0/NaN minutes → dropped at `min_minutes=20`. They do not enter `perf`, `poolq_loo`, or draft-rate ventiles. |
| **PD22 raw roster histogram / backup slide (`min_minutes=0`)** | **No — add hygiene or disclaimer.** Max `roster_n=115` is misleading without filtering `"-"` or noting ESPN junk. After dash filter, BYU 2018 lands at **16** ( sensible). |
| **Non-dash >50 outliers** | **Unaffected by `min_minutes=20` or dash filter** if those players accumulate ≥20 season minutes across games. Worth a separate QC pass if Charles cites “typical roster size” beyond the dash issue. |

**For Alex meeting:** Defend **`min_minutes=20`** on **hero-panel** grounds (playing-time floor for PPM/BPM signal). If showing **raw roster-size** figure, either regenerate after dash filter or annotate tail as ESPN box artifacts.

---

## One-line answer to Charles

**`"-"` players are permanent ESPN/scrape junk you should filter at panel build; re-scrape alone won’t fix them (ESPN still serves them). Your draft/school matching did not cause the BYU 115-man roster.**

---

## Investigation artifacts

| Check | Result |
|-------|--------|
| Frozen box dash rows 2011–2021 | 175 rows, 5 games, 5 team-seasons, 0 with minutes > 0 |
| Live ESPN API 2026-08-17 | `400986852`: BYU 99 dash; other four dash games match frozen counts |
| `panel_rebuild.py` | No dash filter today; draft lookup only sets `Y_draft` |
| `ingest_box.py` | Stub — no re-fetch, no logs |

**Primary paths cited:** `datasets/mbb/mbb_df_player_box.csv`, `sports/sports_pipeline/panel_rebuild.py`, `sports/sports_pipeline/ingest_box.py`, `sports/documents/SPORTS_DATA_GAMEPLAN.md`.
