# SCOUT and COMPASS Q&A

I am giving both of you this document. It contains a number of questions
that one or both of you may already have answered, but I would like to
use this document to consolidate those answers so I can make informed
decisions about how to move forward.

## Read-first rule (both agents)

**Before writing anything on your reply line**, read this **entire**
document from top to bottom — the review process, **every question**,
**every existing SCOUT answer**, **every existing COMPASS answer**, and
any sub-questions in Notes. Do not start filling in replies until you
have read the full Q&A once. Round 2 COMPASS in particular must not
answer from memory or from a partial read; read all SCOUT lines first.

Each question has a reply line for **SCOUT** and **COMPASS**.

- If you know the answer, enter it beginning on your reply line and
  include any additional information, caveats, file paths, counts, or
  context that you think is pertinent.
- If a question clearly belongs to the other agent because it concerns
  work you have not yet done or material you have not examined, enter
  **“Not yet my lane.”**
- If a later question makes you realize that an important question is
  missing, add a sub-question immediately below the relevant question
  (for example, **8a**) with new **SCOUT:** and **COMPASS:** reply
  lines. If you know the answer to the new question, answer it on your
  reply line.
- Please distinguish a **verified answer** from an inference,
  recollection, or recommendation. When practical, cite the relevant
  repo file, dataset, script, output, or analysis artifact so we can
  trace the answer later.
- **Do not overwrite or delete the other agent’s response.** Add your
  answer to your own reply line. If you disagree with an existing
  answer, state the disagreement and the evidence for it.

## Document status

| Round | Agent | Status |
|-------|--------|--------|
| **1** | SCOUT | **Complete** (Aug 19 2026) |
| **2** | COMPASS | **Complete** (Aug 19 2026) — Round 2 restored after accidental SCOUT deletion; COMPASS lines unchanged |
| **3** | SCOUT | **Complete** (Aug 19 2026) — see `20260819_1715_SCOUT_Round3_questions_for_Charles.md`; **B5a** added below |
| **3** | COMPASS | **Complete** (Aug 19 2026) — see `20260819_1718_COMPASS_Round3_questions_for_Charles.md`; **B5a** filled; no SCOUT cross-doc needed |
| 4–6 | Both | Pending Charles Round 3 decisions |

------------------------------------------------------------------------

## Review Process

### Round 1 — SCOUT

I will first give this document to SCOUT. SCOUT should take a first pass
at every question. If a question clearly concerns work SCOUT has not
done or material SCOUT has not examined, enter **“Not yet my lane.”**

**Round 1 is done.** SCOUT answers below are frozen unless Charles
asks for a correction or Round 5 reconciliation.

### Round 2 — COMPASS

I will then give COMPASS the updated document containing SCOUT’s
responses. **COMPASS must read the entire document** — all questions
**and** all SCOUT answers — **before writing on any COMPASS line.**

COMPASS should take the same pass at **every** question from COMPASS’s
perspective. COMPASS does **not** re-verify counts SCOUT already marked
**Verified** unless you spot an error; COMPASS adds **sequencing,
priority, and decision framing** for Charles:

- What the SCOUT facts **imply** for the hero campaign, Alex brief, and
  near-term work order.
- What is **blocked** vs **unblocked** (e.g. ρ extension vs draft ventiles).
- Where Charles should **decide** (tradeoffs), vs where the repo already
  constrains the answer.
- If SCOUT’s answer is enough for a decision, say so briefly; if not,
  say what is still missing.

You may add a short **Note to Charles** at the end of a COMPASS reply
when it helps (one sentence). Do **not** edit SCOUT lines.

### Round 3 — Questions Between Agents

After both agents have completed their first pass, I will ask each to
read the fully updated document again. If either agent has questions for
the other agent or for me, create a separate Markdown document in the
same folder using a clear timestamped filename, for example:

`20260819_1425_COMPASS_Qs_for_SCOUT.md`

### Round 4 — Resolve Cross-Agent Questions

We will answer the questions raised in Round 3.

### Rounds 5 and 6 — Final Reconciliation

SCOUT and COMPASS will each receive one final opportunity to review and
complete this Q&A document after the cross-agent questions have been
resolved.

------------------------------------------------------------------------

# Questions

## A. Data Issues

### A1. BPM / OBPM coverage

We now have the ability to merge the existing datasets and, for
**2011-2021**, have BPM/OBPM data available as well. Is that correct?

**SCOUT:** **Verified — partially.** For **2011–2021**, BPM/OBPM/DBPM are available on the hero panel via left-merge of `datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv` onto ESPN keys `(athlete_id, season, team_id)` in `sports/sports_pipeline/panel_rebuild.py` (Stage 3). File on disk: **50,973** matched rows, seasons **2011–2021**; **OBPM** and **BPM** non-null on 100% of matched rows (spot-checked Aug 19 2026). SR **raw** scrape (`DO_NOT_ERASE/bpm_player_season_raw.csv`) extends to **sr_year 2005–2021**, but the **matched** file used by the conductor stops at 2021. ESPN box does **not** contain BPM; PPM/minutes come from box aggregation only.

**COMPASS:** SCOUT’s facts are enough to **unblock a bounded hero exploration**, not to reopen Rung 1. BPM/OBPM on 2011–2021 is **available now** via the existing merge path — no new scrape required. **Sequencing:** (1) keep canonical hero on **PPM + POST-QC** for Alex; (2) run **one** OBPM/BPM sensitivity pass (same 39-spec grid or a short `--quick` slice) and park results in `pass_a/sensitivity/` — parallel filenames, not a new locked hero; (3) only promote BPM to canonical if it changes the **middle-rise** story without estimand cheating (unlikely to restore elite dip given B5–B6). **Not blocked:** SELECT/MLE, PD14, Pass B/C. **Charles decision:** whether OBPM sweep is worth ~1 day before Alex vs appendix-only.

**Note to Charles:** This answers “did we leave a perf metric on the table?” — yes, but it is **exploration**, not a rescue path for the July tail.

### A2. Extending ESPN coverage through 2025

I could re-scrape ESPN for **2022-2025**, retaining the required
columns, concatenate those seasons with the existing data, and then
repeat the matching/merging pipeline. However, we do not yet have
associated **2022-2025 NBA Draft outcome data**. Is that correct?

**SCOUT:** **Verified — half right.** (1) **NBA draft outcomes through 2025:** **Correct** — `datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv` ends at **draft year 2021** (1,922 rows); `athlete_id_draft_lookup.csv` has **789** matched picks, max `draft_year` **2021**. No 2022–2025 draft rows in repo today. (2) **ESPN box 2022–2025:** **Already present** in frozen `datasets/mbb/mbb_df_player_box.csv` — no rescrape required to *use* those seasons (Aug 19 2026 counts: ~9.4k–9.8k minute-positive athletes/season for 2022–2025 via `dataset_coverage.yearly_coverage_detail_table()`). Formal Stage-1 refresh (`sports/sports_pipeline/ingest_box.py`) is still a **stub** (skips if CSV exists). Extending **ρ/H_sort** to 2025 is config-only: `scripts/regenerate_pd21_rho_hsort_13_25.sh`.

**COMPASS:** **Split the extension into two tracks** — SCOUT’s split is the right mental model. **Track A (unblocked):** panel + ρ/H_sort/ESPN diagnostics through **2025** using box already in repo (`regenerate_pd21_rho_hsort_13_25.sh` or season-window flags). No draft outcome needed for ASSIGN calibration or PD22-style panel backup. **Track B (blocked for hero/Y_draft):** any **Pass A hero or draft-rate ventiles** on 2022–2025 need **draft labels first** — SCOUT is correct that lookup stops at 2021. Do **not** rescrape ESPN for forward extension unless QA finds holes (A2a). **Near-term work order:** main line stays **2011–2021 POST-QC**; forward seasons are **ρ extension + optional panel epoch slide**, not hero extension.

**Note to Charles:** You can extend **geometry/calibration** now; you cannot extend **draft-outcome hero** until draft CSV is updated.

### A3. Extending ESPN coverage backward

The **2005 ESPN data** appears usable. What is the status and quality of
the ESPN data for **2005-2010**? If those seasons are similarly usable,
should we scrape the full 2005-2010 period and retain **all available
columns**?

**SCOUT:** **Verified — usable but thinner pre-2014.** SportsDataverse documents ESPN player boxscores from **2002** onward (`load_mbb_player_boxscore`; seasons &lt; 2002 raise `ValueError`). Frozen box file (`mbb_df_player_box.csv`) has game-level rows from **2005** at scale (2003–2004 are junk: 26 and 289 rows). Per-season **player-season** counts (box aggregate, Aug 19 2026):

| Season | Distinct games | Player-seasons (approx.) |
|--------|----------------|-------------------------|
| 2005 | 4,171 | ~4,603 |
| 2008 | 5,386 | ~6,812 |
| 2010 | 5,569 | ~5,569 |
| 2011 | 5,556 | ~5,455 |
| 2014 | 5,932 | ~10,633 |

**2005–2010 is online and in-file**, but roster depth is **~half** the post-2014 level (PD22 ESPN coverage diagnostic: step at **2013→2014**, not 2011). **Draft↔NCAA matching** for picks with college listed is **~94–100%** for draft years **2005–2010** (`draft_athlete_match.csv` vs lookup) — availability cliff for matching is **~2005**, not 2011. **Recommendation (data):** if scraping backward, retain **all 55 ESPN box columns** (same schema as current file); no need to drop to minutes-only. **QC:** expect more fragmentary team-seasons pre-2014; `min_team_season_games=10` will bite harder on low-game schools.

**COMPASS:** **Park unless Charles explicitly wants a pre-2011 era paper.** SCOUT shows 2005–2010 is **in-file and matchable** but **~half the roster depth** of post-2014 — so expect **more CPR-like fragility** under `mg=10`, not a cleaner hero. Backward scrape is **optional hygiene** (retain all 55 columns if done); it is **not** on the critical path for Alex v1 or closed Rung 1. **If pursued:** treat as **robustness appendix** (wider window, same POST-QC rules), run **after** BPM sweep and **after** draft-forward decision — not instead of PD14/SELECT. **Charles decision:** only green-light 2005–2010 if the dissertation needs “long panel” credibility beyond 2011–2021; repo does not require it for the locked campaign.

**Note to Charles:** Thinner pre-2014 ESPN + harder QC ≠ likely inverted-U recovery; same mechanism as July cameos at the low-games margin.

### A4. Existing NBA Draft dataset coverage

The NBA Draft dataset I located appears to end in **2021** and may have
come from a GitHub dataset associated with another project. **What is
the earliest year covered by the draft dataset currently in the repo /
project files, and what is its complete year range?**

**SCOUT:** **Verified** from `datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv` (Aug 19 2026): **1,922 rows**; **`year` (NBA draft year) range 1989–2021** inclusive. Matched subset in `datasets/mbb/athlete_id_draft_lookup.csv`: **789** rows, draft years **2005–2021** (matcher guard excludes earlier picks from auto-link despite register coverage). Provenance string not in repo README (file lives under `DO_NOT_ERASE/`); gameplan references it as **`nbaplayersdraft.csv`** Stage-2 input. Charles’s recollection of a GitHub-sourced table is **plausible** but **not verified** from file metadata here.

**COMPASS:** SCOUT’s counts are enough for planning. **Register:** 1989–2021 picks in `nbaplayersdraft.csv`; **analysis-ready matched:** 2005–2021 only (789 rows). v1 hero, PD14, and Alex brief should cite **2005–2021 or 2011–2021** depending on slide — never imply 1989–2004 is in the matched panel. **No Charles decision needed** on range; **do** keep “matched subset” language in external docs so reviewers do not conflate register vs panel.

**Note to Charles:** Your “ends 2021” memory is correct for **everything that feeds `Y_draft` today**.

### A5. Extending NBA Draft outcome coverage

It should be possible to obtain NBA Draft outcome data covering
additional years. What reliable sources or datasets should we
investigate first, and what year ranges would they add?

**SCOUT:** **Recommendation (not yet implemented).** Investigate in this order: (1) **SportsDataverse / hoopR NBA draft loaders** — same ecosystem as ESPN box; likely adds **2022–2025+** with `player`, `college`, `pick`, `team` fields compatible with existing matcher. (2) **Basketball-Reference draft pages** — canonical; scrape or manual CSV for 2022–2025 (~60 picks/year). (3) **NBA.com/stats historical draft** — official but heavier to wire. After append: re-run legacy matcher (`obsolete_files/sports_gameplan_old/sdv_second_bkup.ipynb` lineage; `draft_match.py` still stub) → refresh `athlete_id_draft_lookup.csv` → rebuild panel. **Year gain:** **2022, 2023, 2024, 2025** (and 2026 when complete). Match **college string schema** to existing `nbaplayersdraft.csv` columns (`year`, `overall_pick`, `player`, `college`, `team`, …).

**COMPASS:** **Agree with SCOUT’s source order.** **Priority for Charles:** append **2022–2025** to `nbaplayersdraft.csv` → re-run matcher → refresh `athlete_id_draft_lookup.csv` → rebuild panel. That unlocks **forward hero** and longer-window PD14 — not required for **2011–2021 main line** already closed. **Sequencing:** (1) finish Alex brief on locked 2011–2021 POST-QC; (2) draft append as **parallel data task** (SCOUT or you, ~half day if hoopR path works); (3) only then re-open Pass A for 2011–2025 or 2013–2025 windows. **Blocker map:** draft append blocks **Y_draft extension** only; it does **not** block ρ to 2025 or SELECT/MLE on current panel.

**Note to Charles:** Treat draft extension as **Rung 3 / horizon**, not a prerequisite to unstick Rung 1 — Rung 1 is already closed on defensible 2011–2021.

------------------------------------------------------------------------

## B. QC Specifics

For this section, define **Cut Player Rows (CPRs)** as player-season
rows removed by the QC rule because they belonged to team-seasons with
**10 or fewer games (`<= 10`)**.

Unless there is evidence that the historical QC implementation used a
different threshold, please use this definition consistently below and
flag any discrepancy between this wording and the code actually used.

### B1. Number of CPRs

How many player-season rows were removed by this QC cut?

**SCOUT:** **Verified** (Aug 19 2026). Definition matches code: `PipelineConfig.min_team_season_games = 10` in `sports/sports_pipeline/config.py`; implemented in `panel_rebuild._apply_box_qc()` — drops all box rows for `(team_id, season)` with **≤ 10** distinct `game_id` values (after dash-name filter). Window **2011–2021**, dash filter on. **CPR player-season rows removed: 45,332** (of **104,615** aggregate player-seasons before QC → **59,283** retained). *Note:* config docstring still mentions “Default 5” in one comment history; **live default is 10** (also used in `pd22_slide_common.py`).

**COMPASS:** Accept SCOUT’s **45,332 CPRs** as the campaign-scale number for slides. **Implication:** mg=10 is a **large row cut** but **not** a draftee cut (see B3) — correct framing for Alex is “we removed fragmentary team-seasons, not NBA talent.” **Repo constrains:** `min_team_season_games=10` is locked with PD22; do not re-litigate mg for hero shape. **No further count work needed** unless Round 5 reconciliation finds a code/doc mismatch on the “Default 5” comment.

**Note to Charles:** Use **45k CPRs / 1 draftee lost** as the QC headline pair in the HAND story.

### B2. Distinct players represented by CPRs

How many **distinct players** are represented among those CPRs?

**SCOUT:** **Verified:** **30,396** distinct `athlete_id` values among CPR player-season rows (same window/definition as B1).

**COMPASS:** **30,396** distinct athletes is the “who got cut” scale — mostly **low-major / fragmentary** careers (consistent with B4’s 2,715 team-seasons). Not actionable for policy change: the cut is **by design**. For Alex: CPRs are **exhibition cameo and D-III fragment** rows, not rotation players on Duke/Kentucky. **No decision.**

**Note to Charles:** This number explains *volume*; B3 explains *draft harm* (negligible).

### B3. Drafted players represented by CPRs

How many **distinct players represented among the CPRs were ever drafted
into the NBA**, according to the draft-outcome data currently available?

Please report the numerator and, if useful, the percentage of distinct
CPR players.

**SCOUT:** **Verified:** **1** distinct ever-drafted athlete among CPR player-seasons: **Derrick White** — `athlete_id` 67845, Colorado Springs **2014** (31 min, 1-game team-season); also has full Colorado 2017 season outside CPR. **1 / 30,396 = 0.003%** of distinct CPR athletes. Matches prior PD22 drafted-minutes audit finding.

**COMPASS:** **This is the decisive QC fact for the hero campaign.** **1 ever-drafted athlete (Derrick White 2014 cameo)** means mg=10 is **defensible for draft-outcome analysis** — you are **not** throwing away the phenomenon to save QC. Combined with B5–B6, the July tail was **composition in bin 16**, not loss of NBA-relevant rows. **Repo constrains:** keep mg=10. **Charles decision:** none on threshold; optional **name White once** in appendix as the literal 1/30,396 edge case.

**Note to Charles:** This single row answers “did QC kill our draft signal?” — **no**.

### B4. Team-seasons represented by CPRs

How many **distinct team-seasons** are represented among the CPRs?

Because PoolQ LOO is team-season-specific, please also confirm whether
this count corresponds one-for-one with the affected team-season PoolQ
LOO environments, or explain any reason that it does not.

**SCOUT:** **Verified:** **2,715** distinct `(team_id, season)` team-seasons among CPRs (equals `team_seasons_dropped_low_games` in box QC report). **PoolQ LOO mapping:** **1:1** — LOO is computed within each `(team_id, season)` roster; dropping a team-season removes **all** player-season rows on that team-season and eliminates that team’s LOO environment entirely. No many-to-one or partial-team effect.

**COMPASS:** **2,715 team-season environments removed** — SCOUT’s 1:1 LOO mapping is the mechanism story for B4/B5/B6. Each dropped team-season is a **whole bogus LOO pool** (exhibition / 1-game TS), not a partial roster trim. That is why bin **16** under mg=0 was **65.8% CPR** (B6): elite LOO ventile was **cameo-inflated**, not “strong teammates hurt draft odds.” **Locked narrative** for Alex + `PD20_22_campaign_big_picture.md` B4. **No decision.**

**Note to Charles:** PoolQ LOO is team-season-local — CPR count = count of eliminated LOO worlds.

### B5. CPR representation above the July Hero peak

The July Hero histogram peaked at **bin 12**. Considering the player
rows in **bins 13-16 combined**, what percentage are CPRs?

Please report both the CPR numerator and the total number of rows in
bins 13-16 used as the denominator.

**SCOUT:** **Verified** (Aug 19 2026). **Method:** hero-lock panel **without** team-season game QC (`min_team_season_games=0`), so CPR rows remain for tagging; then `min_minutes=20`, ppm z-scored, `poolq_loo` winsor `(0.01, 0.99)`, **16 quantile** ventiles, **1-indexed bins** (1 = lowest poolq; matches plot convention in `panel_build.py`). Draft rate peaks at **bin 12** (2.62% mean `Y_draft`); bin counts are equal (~3,886/bin). **Bins 13–16 combined:** **4,808 CPRs / 15,545 rows = 30.93%**.

**COMPASS:** **~31% CPR share in bins 13–16 under July (mg=0) spec** is the smoking gun for **ventile reassignment**, not draftee loss. Peak was bin **12** in that replay; upper bins still **one-third cameo rows** — enough to **flatten or fake** a tail dip when those rows draft at **0%**. POST-QC removes that mass → flat elite tail (canonical hero). **Use in Alex brief:** pair this stat with July replay PNG in `pass_a/sensitivity/`. SCOUT’s method note (mg=0 panel for tagging) is correct for the counterfactual; **do not** treat mg=0 as estimand. **Enough for decision:** mg=10 stays.

**Note to Charles:** **4,808 / 15,545** is the one slide stat that explains why July ≠ canonical.

### B6. CPR representation by bin

What is the CPR representation **separately for each of bins 13, 14, 15,
and 16**?

For each bin, please report:

- total player rows in the bin;
- number of CPRs;
- CPR percentage.

**SCOUT:** **Verified** (same method as B5):

| Bin (1-indexed) | Total rows | CPR rows | CPR % |
|-----------------|------------|----------|-------|
| 13 | 3,887 | 560 | 14.41% |
| 14 | 3,886 | 705 | 18.14% |
| 15 | 3,886 | 986 | 25.37% |
| 16 | 3,886 | 2,557 | **65.80%** |

**COMPASS:** **Bin 16 monotonicity (14% → 18% → 25% → 66% CPR)** is the finest-grained evidence that the **July elite-bin dip was a cameo artifact** — not a one-bin wiggle. Under POST-QC, bin 16 draft rate **stays ~3.2%** (flat tail); under mg=0, bin 16 was **dominated by zero-draft CPR scrubs** with artificially high LOO. **Hero campaign implication:** Rung 1 closed — middle rise real, elite dip not robust. **Optional slide:** small table from B6 next to `PASS_A_sensitivity_loo_mg0_*_july_replay_mg0.png`. **Charles decision:** none on QC; optional whether to add B6 table to HAND deck.

**Note to Charles:** **66.8% in bin 16** is the number that should kill anxiety about “one bin noise” — it was **two-thirds cameo rows**.

### B5a. POST-QC bin 12–16 draft rates (companion to B5/B6)

Under the **canonical** hero spec (mg=10, min=20, 16 quantile poolq_loo, winsor 0.01/0.99, 2011–2021), what are mean `Y_draft` by bin 12–16?

**SCOUT:** **Verified** (Aug 19 2026, same panel as locked hero):

| Bin (1-indexed) | n | Mean draft rate |
|-----------------|---|-----------------|
| 12 | 2,894 | 2.63% |
| 13 | 2,894 | 2.73% |
| 14 | 2,894 | 2.90% |
| 15 | 2,894 | 3.25% |
| 16 | 2,894 | **3.21%** |

Elite tail is **flat / slightly rising** under POST-QC — no dip. Supports COMPASS B5/B6 narrative (July dip was mg=0 CPR composition).

**COMPASS:** **Accept SCOUT’s table as the canonical elite-tail read.** Pair with B5/B6 for Alex: under mg=0, bin **16** draft rate collapsed (~1.16% in July replay) while **66.8%** of bin 16 rows were CPRs; under POST-QC, bins **12→16** rise **2.63% → 3.21%** with **no** elite dip — that is the honest Rung 1 claim. **Optional one-slide contrast:** canonical side-by-side PNG vs July replay PNG (`pass_a/sensitivity/…_july_replay_mg0.png`); B6 table is optional garnish (see Round 3 Charles docs). **No SCOUT re-count needed.**

**Note to Charles:** B5a is the positive half of the July story — use it whenever you show the sensitivity replay.

------------------------------------------------------------------------

## Notes / Additional Questions

Add any newly identified questions here **only if they do not naturally
belong as a sub-question under A1-A5 or B1-B6**.

### A2a. Does forward extension need ESPN rescrape?

**SCOUT:** **Verified:** No — 2022–2025 already in `mbb_df_player_box.csv`. Optional refresh only if QA finds gaps vs live ESPN.

**COMPASS:** **Agree — no rescrape for forward box.** Work order: if extending ρ/H_sort to 2025, use existing `mbb_df_player_box.csv` + config window; QA only if counts look anomalous vs SCOUT’s ~9.4k–9.8k athletes/season. **Blocked:** hero/draft ventiles on 2022–2025 until A5 draft append.

**Note to Charles:** Do not spend scrape time before draft CSV append unless you need live ESPN for a non-draft diagnostic.
