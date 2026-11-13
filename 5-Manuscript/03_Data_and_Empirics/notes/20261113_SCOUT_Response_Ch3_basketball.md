# Response to FOUNDY — Chapter 3, college basketball / NBA draft (SCOUT)

**SCOUT → Charles / FOUNDY** | 13 November 2026 | **DRAFT** (no new analysis; verified from repo paths read today unless tagged **recalled**)

Answers follow `20261113_Ch3_Questions_for_SCOUT_and_PEER.md` (Parts A + B).

---

## Part A — Shared outline

### A1. Why this system fits the five criteria

| Criterion | How MBB + draft fits | Where it fits only partly |
|-----------|----------------------|---------------------------|
| **1. Observed performance** | Season box-score points and minutes are observed before draft; **points per minute (PPM)** is built from those totals. **verified** — `sports_pipeline/panel_build.py` (`assign_perf_from_metric`, `perf` column). | PPM is one box-score scalar; draft decisions use unobserved scouting. **recalled** — Alex named PPM as the Ch.3 measure in PD52 / executive summary. |
| **2. Non-random groups** | **Team-season** is the group; rosters are institutionally formed, not a random draw. **verified** — group key `(team_id, season)` for LOO in `recompute_teammate_loo_pool_quality`. | No formal test of homophily in Ch.3; empirical ρ ≈ 0 on MBB. **verified** — `MBB_empirical_roster_select_replay.md`. |
| **3. Global selection** | NBA draft fills **league-wide** slots from the college-eligible pool, not a separate contest inside each team. **recalled** — institutional fact + Alex criteria. | Many picks never played college in this panel (international, HS, G League); the college panel is not the full draft universe. **verified** — draft table 780 picks in 2009–2021 vs 615 ever-drafted college rows in HERO (`_provenance.json`). |
| **4. Limited places** | **60 picks per year** (two rounds) cap advancement. **recalled** | Not all 60 map to rows in the college box-score panel; chapter must state college-linked share explicitly (see B9). |
| **5. Mostly closed** | College career is mostly entry → one or more seasons → draft or exit; mid-season NBA entrants from college are rare in design. | **Transfers** and **multi-team seasons** break a pure closed roster; handled as multiple team-season rows. **verified** — one row per player-season-team in spine docs. |

### A2. Search story (narrative)

**recalled** narrative grounded in **verified** file contracts:

We started from a simple observational target: link **who got drafted** to **how good their teammates looked** on the same court, using only public sports data. The first durable choice was to anchor everything on **ESPN-style men's college box scores** accessed through **sportsdataverse / hoopR-style loaders**, because they give repeatable player–team–season identities (`athlete_id`, `team_id`, `season`) suitable for a panel. That spine replaced an older pattern of hopping across several notebooks (`sdv_first`, `sdv_second`, scrape notebooks) without a single conductor.

**NBA draft outcomes** came from a consolidated **`nbaplayersdraft.csv`** register (see B1). Matching draft names and colleges to ESPN athletes was never fully automatic: we built **`athlete_id_draft_lookup.csv`**, **`DO_NOT_ERASE/college_aliases.csv`**, and human feedback templates for misses. That loop cost real time but is what makes Y_draft auditable.

**Sports-Reference (SR) advanced stats** were added as a **second pass** on the same ESPN keys—BPM/OBPM/DBPM and scrape crosswalks—not as a second universe of players. The forward contract is in `sports/documents/SPORTS_DATA_GAMEPLAN.md`: durable inputs live under `datasets/mbb/DO_NOT_ERASE/`; disposable rebuild cache under `datasets/mbb/`.

**Performance measure:** explorations used BPM and alternatives, but the **Chapter 3 / Pass A lock** is **PPM**, z-scored within season for pooling and LOO. **verified** — `HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json` (`perf_metric`: `ppm`).

**When the design settled:** the **530 conductor + `sports_pipeline` modules** (2025–2026) and the **Pass A HERO lock** (2009–2021, min20, mg10, last-ps, ever-Y, q16 on `poolq_loo`) are the run FOUNDY should cite. **verified** — provenance JSON + `pass_a_empirical_bundle.py` header.

**Where datasets came from (recorded):** consolidated register **`5-Manuscript/03_Data_and_Empirics/notes/20261113_MBB_DATA_SOURCES_register.md`** (file-by-file). On disk today the ESPN spine `mbb_df_player_box.csv` spans **2003–2025** game rows (**verified** 13 Nov 2026); Ch.3 HERO still **restricts analysis to 2009–2021**. Draft register in `DO_NOT_ERASE/nbaplayersdraft.csv` spans draft **`year` 1989–2021** (1,922 rows). Exact **download URLs and scrape dates** for the frozen CSVs are **not** in git metadata — register lists **TK** items for Charles (one line each in methods).

**Dead ends (one line each):** treating SR as its own spine without ESPN match (**dropped**); relying on `dedupe` for draft matching (**parked** per gameplan); using full-panel all-seasons HERO without deciding `last-ps` vs `all-ps` estimand (**resolved** in `y_draft_mode.py`).

### A3. Raw sources

| Source | Publisher / host | Row grain | Person ID | Years in file / used | Obtained | Terms |
|--------|------------------|-----------|-----------|----------------------|----------|-------|
| ESPN MBB player box (sportsdataverse) | ESPN via **sportsdataverse** / **hoopR** (`ingest_box.py`, `data_integrity.py`) | Player-game → aggregated to player-season | `athlete_id` | File **2003–2025** on disk; **Ch.3 uses 2009–2021** | Legacy **sdv_first** ingest → frozen `datasets/mbb/mbb_df_player_box.csv`; Stage-1 refresh stub | **Verified** seasons/range; **TK** download date/command — see **MBB_DATA_SOURCES_register** #1 |
| NBA draft register | **`datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv`** | Draft register row (career stats block) | register `id` | **`year` 1989–2021**, 1,922 rows | Static CSV in DO_NOT_ERASE; advisor memos cite **Basketball-Reference**; hoopR/GitHub origin **plausible, not verified** (SCOUT Q&A Aug 2026) | **Verified** counts; **TK** original URL — register #3 |
| Draft ↔ ESPN match | `athlete_id_draft_lookup.csv` | Matched draft row + ESPN athlete | `athlete_id` when matched | Matches through 2021 | Pipeline Stage 2 / `530` | — |
| SR advanced BPM | `DO_NOT_ERASE/bpm_player_season_raw.csv` (when present) | Player-season on SR slug | matched to `athlete_id` post crosswalk | Scrape window per scrape job | Web scrape + slug crosswalk | **recalled** — SR terms of use; rate limits noted in gameplan |

### A4. Linking records

**Draft → ESPN spine**

- **Match keys:** parsed draft name, college string, year; then fuzzy name + **`college_aliases.csv`** school equity. **verified** — `SPORTS_DATA_GAMEPLAN.md` Stage 2a–2c; lookup columns in specstory-exported schema (`match_score`, `match_last_name_score`).
- **Match rate:** **not recorded** in a single canonical markdown table today — **Open item** for Charles. Prior agent notes: **789** rows in lookup file, max draft year 2021 (**recalled** from prior session grep, not re-counted today).
- **Unmatched:** remain in QA exports / feedback templates for human review. **verified** — gameplan pause points.

**ESPN → SR**

- `sr_school_slug_crosswalk.csv`, `sr_school_slug_aliases.csv`, `bpm_player_season_matched.csv`. **verified** — gameplan durable file table.
- Human curation: **yes** for slug aliases and college aliases.

### A5. Cleaning and final sample — flow table

**Order note (verified from code):** build full player-season panel → assign `perf` (PPM) → optional z-score within season → **`recompute_teammate_loo_pool_quality`** (peer measure on **all** rows in that frame) → **`restrict_to_last_season_rows`** when `panel-rows last-ps` → then analysis filters (`dropna` on `poolq_loo`, `Y_draft`, `min_minutes`, `min_team_season_games`, optional team-has-draf tee filter). **verified** — `sports_pipeline/panel_build.py`, `y_draft_mode.py` docstring (apply Y and LOO **before** minute/game floors where noted).

| Step | What it does | Why | Count after |
|------|----------------|-----|-------------|
| Raw box aggregate | Player-season-team rows from ESPN box | Spine | **not recorded** in one saved run log (Charles: pull from last `530` rebuild report if needed) |
| Join draft outcome | `Y_draft` from lookup | Advancement | **not recorded** |
| Assign PPM + z within season | `perf` for LOO | Performance + commensurate peers | **not recorded** |
| LOO teammate mean `poolq_loo` | B2 peer context | HERO x-axis | **not recorded** |
| Last season only (`last-ps`) | One row per athlete at max season | Ch.3 estimand | **not recorded** |
| `dropna(poolq_loo, Y_draft)` | Analysis-ready | **not recorded** |
| `min_minutes >= 20` | Playing-time floor | Stabilize PPM | **not recorded** |
| `min_team_season_games > 10` | Drop thin team-seasons | Exclude fragmentary schedules | **not recorded** |
| Final HERO sample | q16 binning + plot | **verified** | **n = 22,795**, **615** drafted — `HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json` |

### A6. Four concepts

**Performance**

- **Definition:** points per minute for the player-season, then **z-scored within season** before LOO when winsor/z path is active for Pass A lock. **verified** — provenance footer “PPM z”; `apply_perf_metric_for_analysis(..., zscore_perf_within_season)`.
- **Column:** `perf` (underlying), ability ventiles use same `perf` for naïve panel. **verified** — `pass_a_empirical_bundle.py`.

**Group**

- **Definition:** teammates sharing **`team_id`** in **`season`** (team-season roster). **verified** — `recompute_teammate_loo_pool_quality`.
- **Timing:** same season as the focal player-season row (before `last-ps` collapse).

**Peer quality (B1–B4)**

| Code | In MBB code? | Ch.3 canonical figure? |
|------|----------------|----------------------|
| **B1** full-group mean incl. self | Team mean talent constructs exist for diagnostics (`tier1` congestion_quality) | **No** on locked HERO |
| **B2** LOO peer mean | **`poolq_loo`** | **Yes** — HERO x-axis |
| **B3** own minus LOO mean | Can be derived from `perf` and `poolq_loo` | **No** on locked HERO (used elsewhere / CCT) |
| **B4** roster pressure (sigmoid) | **`tier1_mechanism_vars`** weighted crowding experiments | **No** on locked HERO |

- **Groups of one:** LOO undefined when only one valid teammate; row drops at `dropna(poolq_loo)`. **verified** — denominator `(n_teammates - 1)` in `panel_build.py`.

**Advancement**

- **Event:** **`Y_draft = 1`** if athlete ever drafted (lookup), evaluated on **last college player-season row** when `panel-rows last-ps` + `y-draft-mode ever`. **verified** — provenance `y_draft_mode`: `ever`, `panel_rows`: `last-ps`.
- **Not advanced:** `Y_draft = 0` on that final-season row.
- **Unresolved:** players without draft match still have defined `Y_draft` (0/1 from rule); undrafted college players remain in denominator.

### A7. Run of record

| Item | Value | Tag |
|------|--------|-----|
| Script | `sports/scripts/pass_a_empirical_bundle.py` | **verified** |
| Config lock | 2009–2021, q16, min20, mg10, ppm, allt population, last-ps, ever-Y, winsor 0.01–0.99 on LOO | **verified** — `_provenance.json` |
| Figure PNG | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.png` | **verified** (file exists in repo) |
| Provenance | `…/HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json` | **verified** |
| Side binned CSV | `PASS_A_binned_draft_rate_poolq_loo_q16_allt_min20_mg10_9_21_last_ps.csv` | **verified** — provenance `output_files` |
| Panel build entry | `sports/530_sports_pipeline.ipynb` + `sports_pipeline.panel_build` / `panel_rebuild` for refreshed CSV | **verified** — gameplan |

**Why this run:** named in `PEER_INFLUENCE_AXES_MISMATCH.md`, flipbook Act II–III, `MBB_DATA_STORY_plot_highlights.md` “reigning HERO lock.”

### A8. Authoritative vs superseded

| Authoritative | Superseded / exploratory |
|-------------|-------------------------|
| `530_sports_pipeline.ipynb`, `sports_pipeline/*`, `pass_a_empirical_bundle.py` | Retired multi-notebook hop (`obsolete_documents/sports_gameplan_old/`) |
| `datasets/mbb/DO_NOT_ERASE/*` durable inputs | Disposable `datasets/mbb/` cache |
| `pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.*` | Untagged PNGs in `population_sandbox/hero/` with same basename stem (parallel campaign copies) — cite **`pass_a/`** unless Charles picks another |
| `sports/archive/535_sports_tier_1.ipynb` (EDA) | Root `sports/535_sports_tier_1.ipynb` if present as symlink/stub |

### A9. Known quirks

- **PPM vs BPM / OBPM:** canonical HERO does **not** use BPM; sensitivity plots exist under `basic_data_plots/` and hero sandboxes. **verified** — MBB data story.
- **Inverted-U visibility** depends on binning, band, and axis; monotone naïve ability plot coexists (`PASS_A_naive_ability_q16_…_last_ps.png`). **verified** — flipbook `scripts/build_flipbook_figure_deck.py`.
- **Draft register ends 2021** while box ingest may extend further — extending either requires re-match. **verified** — CSV `year` max 2021.
- **Peer axis label vs executive summary:** Ch.3 summary prose matches **B2 LOO**; ensure text does not say “own minus peer” for this figure. **verified** — aligns with `20261109_Ch3_executive_summary_DRAFT.md` basketball paragraph.

### A10. What can be said in print

- No basketball **IRB/subject** row applies to public stats. **recalled**
- Attribute ESPN / sportsdataverse and draft/SR sources in methods; do not republish full player-level tables in print without checking site terms. **recalled** — Charles / IRB not re-checked today.

### A11. Reproducibility

- **Code:** this repo (Dropbox workspace); **`pip install -e .`** at root for `sports_pipeline`. **verified**
- **HPC:** Rivanna copies may exist for Army, not required for MBB lock. **recalled**
- **Expensive to recreate:** `DO_NOT_ERASE/bpm_player_season_raw.csv`, SR scrape merges, hand **`college_aliases.csv`**. **verified** — gameplan
- **Re-build panel from raw:** possible in principle via `530` stages if ESPN extract + draft CSV present; full counts not re-run for this memo.

### A12. Figures (placeholders)

| Role | Path | Axis / notes |
|------|------|----------------|
| **Ch.3 HERO (canonical)** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.png` | **B2** `poolq_loo` (16 Q bins) |
| Naïve own-ability | `…/pass_a/PASS_A_naive_ability_q16_allt_min20_mg10_9_21_last_ps.png` | Own `perf` ventiles |
| Side-by-side talent vs LOO | `…/pass_a/PASS_A_side_by_side_q16_allt_min20_mg10_9_21_last_ps.png` | Left ability / right LOO |
| MBB data story deck | `…/sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png` | Multiple panels (see `MBB_DATA_STORY_plot_highlights.md`) |
| Band-of-excellence / CCT | `…/basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.png` | LOO with **Â band** fixed (sensitivity, not Ch.3 sole figure) |

---

## Part B — Basketball / draft specifics

### B1. Draft list

- **Path:** `datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv`. **verified**
- **Coverage:** years **1989–2021**, **1921** data rows; **780** picks with `year` in **2009–2021**. **verified** (read CSV today)
- **Rounds:** columns include `overall_pick`; **both rounds assumed** for NBA 60-pick era — **recalled** (not verified column-by-column today)
- **Non-college draftees:** remain in draft file but **fail college box match** → excluded from college panel / lower match rate. **recalled**
- **Share in analysis:** **615** ever-drafted players on **22,795** last-ps rows (**2.7%**) — **verified** — provenance; not the same as 615/780 picks (college-linked subset).

### B2. Box scores

- **Divisions / seasons:** D-I MBB box via sportsdataverse ingest; **season window 2009–2021** for canonical HERO. **verified** — provenance
- **Non–D-I opponents:** season totals typically include all scheduled games in box aggregation — **recalled** — exact opponent filter flag not re-read in `panel_rebuild.py` today (**Open item**).

### B3. Draft matching

- See A4. **Match rate not recorded** in provenance JSON.

### B4. Sports-Reference

- **Canonical HERO:** **ESPN PPM only** for `perf` and LOO. **verified** — provenance
- **SR adds:** BPM family for **sensitivity** and tier-1 exploration (`538`, archived `535`), not the locked Pass A figure. **verified** — gameplan Stage 3

### B5. Performance measure

- **Why PPM:** Alex / Ch.3 executive summary example. **recalled** — `20261109_Ch3_executive_summary_DRAFT.md`
- **Alternatives in code:** `PERF_METRIC` switches (`ppm`, `bpm`, `obpm`, `dbpm`, minutes, etc.) — **verified** — `panel_build.py`, `530` config.

### B6. Minutes and games thresholds

- **min20:** `min_minutes >= 20` on player-season row. **verified** — `_provenance.json`, `filter_panel`
- **mg10:** `min_team_season_games = 10` — drop team-season if **distinct `game_id` count ≤ 10**. **verified** — `panel_rebuild.py` docstring / report
- **Order:** LOO recomputed on panel **before** `filter_panel` minutes filter when pipeline order follows `pass_a_empirical_bundle` / y_draft docs; minutes filter **after** LOO. **verified** — `y_draft_mode.py` lines 23–25

### B7. Final season only

- **`last-ps`:** `restrict_to_last_season_rows` keeps `max(season)` per athlete. **verified** — `y_draft_mode.py`
- **Ever-draft:** `Y_draft` from lookup flags whether athlete was **ever** drafted; attached to that final row. **verified** — provenance

### B8. Group / transfers

- **Grain:** player-season-**team**; transfer → **two rows** in different team-seasons; LOO within each. **verified** — gameplan spine grain
- **Two teams same season:** **recalled** — rare; not re-documented in Ch.3 memo today (**Open**).

### B9. Limited places

- State **60 NBA picks/year** league-wide; college panel analyzes **college players** with **615** ever-drafted over window, not “60 × years”. **verified** counts from provenance vs draft CSV totals.

### B10. Who enters late

- **One-and-done / early exit:** appear as **`last-ps`** with single season row. **recalled**
- **Redshirt:** invisible if not in box minutes threshold. **recalled**
- **Draft after final season:** `ever` Y captures draft without requiring draft in same calendar year as final box row — **recalled** — exact year alignment rule in lookup not re-read today.

### B11. What this system cannot give us

- Rich performance (single PPM scalar).
- Full draft universe (international / non-college paths).
- Clean “closed league” rosters (transfers).
- Causal peer effects or model-based selection (Ch.4+).
- Strong inverted-U **by default** on full pond; shape is estimand- and band-dependent. **verified** — MBB empirical replay + COMPASS campaign notes.

---

## Closing boxes

### Open items (Charles / Alex)

- Official **draft match rate** and human-audit counts for methods.
- Whether **non–D-I games** enter season PPM totals (code flag).
- Wording for **limited places** vs international picks.
- Whether Ch.3 shows **naïve ability** figure alongside HERO (flipbook has both).

### Conflicts

- Older docs reference `sports/535_sports_tier_1.ipynb` at repo root; **archive path** is authoritative (`tier_1_roadmap.md` updated 9 Nov).
- Duplicate HERO PNG stems under `population_sandbox/hero/` vs `pass_a/` — cite **pass_a** provenance JSON.

### For other chapters

- **ASSIGN / homophily / ρ** on MBB: parked (`MBB_empirical_roster_select_replay.md`).
- **MLE λ, γ, t** and sim HERO: `sports_sandbox/reigning_hero/`, Ch.4.
- **Band of Excellence / CCT**: env curve near cutoff — not sole Ch.3 headline without Charles pick.

---

*End SCOUT Ch.3 draft. FOUNDY may lift prose into manuscript §; Charles approves before external send.*
