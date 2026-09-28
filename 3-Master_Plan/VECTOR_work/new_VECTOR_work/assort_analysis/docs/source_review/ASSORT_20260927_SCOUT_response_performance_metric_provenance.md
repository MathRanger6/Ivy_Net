# SCOUT response — performance-measure provenance (PPM, BPM, PER)

**Prepared:** September 27, 2026  
**For:** VECTOR / Charles  
**In reply to:** [`ASSORT_20260927_SCOUT_performance_metric_provenance_questions.md`](ASSORT_20260927_SCOUT_performance_metric_provenance_questions.md)  
**Status:** Read-only source review. Join counts re-checked locally against saved CSVs; no scrape, panel rebuild, new sorting indices, or curves.

---

## How to read this document

| Tag | Meaning |
|-----|---------|
| **[Direct repo]** | Code or file verifiable in the repository today |
| **[Saved result]** | Named artifact or memo; not re-run here |
| **[Interpretation]** | Mechanism synthesis — not independently audited row-by-row |
| **[Gap]** | Missing primary provenance record |

---

## 1. Matching lineage and quality

### 1.1 What produced `bpm_player_season_matched.csv`

**[Direct repo]** Pipeline contract is documented in `sports/sports_pipeline/bpm_merge.py` (module docstring, lines 7–16) and implemented in `run_match()` (same file):

1. **Crosswalk:** `datasets/mbb/DO_NOT_ERASE/sr_school_slug_crosswalk.csv` maps ESPN `team_id` → Sports-Reference `school_slug` (`ensure_crosswalk()` reads `mbb_df_team_box.csv`; user-edited slugs preserved).
2. **Raw SR table:** `datasets/mbb/DO_NOT_ERASE/bpm_player_season_raw.csv` — team-season advanced pages scraped by `sports/sports_pipeline/scrape_bpm.py` (BPM/OBPM/DBPM when published, plus PER, WS, TS%, etc.).
3. **Match keys on the panel side:** normalized display name (`normalize_player_name`) + `school_slug` + `season` (= SR `sr_year`).
4. **Match keys on output:** **`(athlete_id, season, team_id)`** — ESPN identifiers from whichever **panel DataFrame** was passed into `run_match`, not from SR directly.
5. **Duplicate SR rows:** same `(school_slug, sr_year, player_key)` → keep row with highest SR minutes (`MP`).
6. **Writes:** `bpm_player_season_matched.csv` (rows with finite BPM at time of older code; see §1.3) and QA `datasets/mbb/bpm_panel_rows_unmatched.csv`.

**[Direct repo]** Downstream consumption: `sports/sports_pipeline/panel_rebuild.merge_sr_matched_into_panel()` left-joins the matched file on `(athlete_id, season, team_id)` when building from box (`panel_rebuild.py`, lines 95–118). `sports/sports_pipeline/perf_metric.py` maps user keys `bpm` / `per` → columns `BPM` / `PER`.

### 1.2 Last documented refresh (not a formal run record)

**[Saved result]** [`3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md`](../../../../re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md) records an **August 27, 2026** SR maintenance chain: backup/trim raw, network rescrape 2009–2021, then **`run_match`** (queued in `sports/scripts/run_sr_rescrape_2009_21.sh`). Agent transcript archives cite post-match sizes on the order of **~60,231** matched rows and **~8,483** unmatched QA rows after engineering that extended SR pass-through beyond BPM-only rows.

**[Direct repo]** On disk today (read September 27, 2026): `bpm_player_season_matched.csv` has **60,231** rows, seasons **2011–2021**, **4,667** rows with `season == 2015`, **zero** duplicate `(athlete_id, season, team_id)` keys in 2015. Columns include `has_bpm`, `has_sr_match`, `BPM`, `PER`, and extended SR rate columns — **broader than** the minimal column list in the current `run_match()` excerpt (which still documents BPM-centric `has_bpm` only). Treat the **saved file** as the authoritative column set for analysis; treat **current** `bpm_merge.py` as the documented algorithm with possible later extensions reflected only in the artifact.

**[Gap]** There is **no** repository `docs/run_records/` (or equivalent) JSON naming the exact panel snapshot, git commit, and checksum fed to the August 2026 `run_match`. Lineage is **reconstructed** from code + SCOUT memo + file stats, not a single auditable “match run record.”

### 1.3 Relation to the accepted ASSORT 2015 audit population

**[Direct repo]** The assort audit players file (`outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz`) was built under ASSORT-specific rules: 2015 only, minutes recovery overlay, canonical team, **≥11 captured games**, **≥20 total minutes**, population PPM and `ability_standardized` computed in that pipeline — **without** requiring SR merge at construction time. See [`docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md`](../decisions/ASSORT_20260925_construction_specification_and_source_audit.md) §2 (explicit that optional SR merge is not part of the authorized experiment construction).

**[Interpretation]** The matched file **predates and differs from** that construction path: it was built from a **hero/panel-style** ESPN aggregation (typically `build_from_box` with box QC, often **mg10** and sometimes **min20**), then name/slug matching to SR. Joining audit players to matched rows by `(athlete_id, season, team_id)` is **legitimate for coverage screening** but does **not** prove SR stats were matched under the same eligibility filters or canonical-team logic as the audit file.

### 1.4 Match-quality diagnostics (existing)

| Mechanism | What it limits | Source |
|-----------|----------------|--------|
| Name normalization | Punctuation, suffixes (Jr/Sr/II) | `bpm_merge.normalize_player_name` |
| School slug | ESPN short name → SR URL segment; manual crosswalk + alias CSV | `ensure_crosswalk`, `scrape_bpm.SR_SCHOOL_SLUG_ALIASES` |
| Transfers / two team-season rows | Match is **per** `(athlete_id, season, team_id)`; wrong team row → wrong or missing SR row | **[Interpretation]** — no ASSORT-specific transfer audit on SR join |
| Name collisions | Same normalized name + school + year → highest SR minutes wins | `run_match` dedup rule |
| Unmatched panel rows | QA export | `datasets/mbb/bpm_panel_rows_unmatched.csv` |

**[Gap]** No saved **match accuracy study** (manual sample, collision list, or transfer reconciliation) scoped to **2015** or to the **4,267** audit IDs. Accuracy bounds are **process description + QA file**, not measured precision/recall.

---

## 2. Coverage on the accepted 2015 population

### 2.1 VECTOR counts — verified

**[Direct repo]** Re-join (September 27, 2026): audit file **4,267** players; `season` imputed **2015** (column absent on audit export). Left join to `bpm_player_season_matched.csv` on `(athlete_id, season, team_id)`:

| Quantity | VECTOR | SCOUT re-check |
|----------|-------:|---------------:|
| Accepted players | 4,267 | 4,267 |
| Three-field key present in matched file | 4,176 | **4,176** (`_merge == both`) |
| Finite BPM | 4,174 | **4,174** |
| Finite PER | 4,163 | **4,163** |
| Finite both | 4,161 | **4,161** |

Coverage rates **~97.8%** (BPM) and **~97.6%** (PER) on this population hold.

### 2.2 Unmatched keys vs matched-but-null measures

**[Direct repo]** Among **93** audit players **without** finite BPM:

| Class | Count | Meaning |
|-------|------:|---------|
| **No row** in matched file for `(athlete_id, 2015, team_id)` | **91** | `left_only` — SR merge never attached an ESPN key for that team-season (name/slug miss, player absent from SR advanced table, panel row not in match input, etc.) |
| **Row present**, BPM not finite | **2** | Key exists; SR side lacked usable BPM for that matched row (2015 matched file has **20** such rows overall: 4,667 keys, 4,647 with `has_bpm == 1`) |

**[Direct repo]** Of the **91** key misses, **91** also appear in **`bpm_panel_rows_unmatched.csv`** for **season 2015** — consistent with “panel row at match time had `has_bpm == 0` / no SR match,” not a join bug in the audit script.

**[Interpretation]** VECTOR’s minutes comparison (median **602** minutes among BPM-missing vs **535.5** among BPM-present) is **descriptive only**; it does **not** explain missingness (many high-minute players can still fail name/slug/SR coverage).

**[Gap]** No pre-written memo classifies the **91** by reason (slug error vs SR gap vs name variant). That would require a **narrow, authorized** read of unmatched QA + crosswalk for those keys — not done in this reply.

---

## 3. Meaning of the measures (saved columns)

### 3.1 Points per minute (PPM) on the audit population

**[Direct repo]** Audit PPM = season sum of verified box **points** ÷ season sum of verified **minutes** after ASSORT source rules and overlays; standardized to `ability_standardized` in the audit pipeline. This is **native** to the 4,267-player file and does **not** use SR.

**[Direct repo]** PPM is **not** a latent talent measure; it mixes scoring with minutes and role. Sorting and interval work on this population used **measured** PPM only ([`ASSORT_20260927_sorting_sensitivity_v1_report.md`](../results/ASSORT_20260927_sorting_sensitivity_v1_report.md), [`ASSORT_20260927_rotation_core_intervals_v2_report.md`](../results/ASSORT_20260927_rotation_core_intervals_v2_report.md)).

### 3.2 BPM and PER in `bpm_player_season_matched.csv`

**[Direct repo]** Values are **scraped** from Sports-Reference **men’s team advanced** pages (`scrape_bpm.py` docstring, lines 4–7). Stored columns are SR field names (`BPM`, `PER`, …) plus ESPN keys from the match step.

**[Saved result]** External definitions (VECTOR memo links): **College BPM 2.0** combines box stats with **team overall performance**; minutes-weighted player BPM is aligned to team efficiency. **PER** is a pace-adjusted per-minute production index normalized to league average (~15). These are **third-party estimators**, not draft outcomes.

**[Interpretation] — team context vs draft:**

| Contamination type | PPM (audit) | BPM (SR) | PER (SR) |
|--------------------|-------------|----------|----------|
| Team scoring environment / pace | Strong (same team shares offensive context) | **Built-in team adjustment** in BPM methodology | Pace normalization in PER |
| Direct use of **NBA draft result** in metric construction | **No** (box counting) | **No** in SR public definitions | **No** in SR public definitions |
| Minutes / role | Via denominator and opportunity | Via regression and minutes weights | Per-minute index |

**[Gap]** We do **not** store SR’s internal formula version per row. The **August 2026 rescrape** likely reflects SR’s **current** published college tables (including BPM 2.0-era pages for historical seasons), but **without** a scrape timestamp column per player-season we cannot prove which SR revision each 2015 cell reflects. Assume **“SR as scraped in 2026”**, not “ESPN-era frozen SR snapshot.”

**[Interpretation]** High **H_sort** on BPM in older ladder work is **not** independent evidence of talent sorting; it can partly reflect **shared team-level adjustment** embedded in BPM.

---

## 4. Comparable existing evidence (same 4,267 audit players)

**[Direct repo]** **No** saved artifact computes **BPM**, **PER**, or **H_sort(BPM/PER)** on the **same** `ASSORT_20260927_rotation_audit_v1_players.csv.gz` roster.

**Same population — PPM only (executed in `assort_analysis/`):**

| Work | What it uses |
|------|----------------|
| Rotation audit, sorting sensitivity, core intervals v1/v2 | `points_per_minute` / `ability_standardized` |
| PPM by position, games played, participation crosscheck | Same accepted player file; PPM unchanged |

**Closest other work — different population or question:**

| Artifact | Population / rule | Metrics |
|----------|-------------------|---------|
| [`H_SORT_LADDER_REPORT.md`](../../../../re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/H_SORT_LADDER_REPORT.md) | **2009–2021**, mg10, min20, last-ps-style panel; pooled **H_sort** | PPM ~0.064, BPM ~0.337, PER ~0.111 — **not** 2015 audit N |
| Hero / LG saved traces (e.g. Aug 19 mg10 2015) | Production panel filters, not ASSORT canonical-team audit | PPM **H_sort** ~0.06 band |
| `loo_shape/LOO_SHAPE_REPORT.md` | Draft-curve shape gate | Different estimand |

**[Interpretation]** Choosing BPM because the ladder shows higher **H_sort** would violate VECTOR’s stop rule. A fair three-metric comparison requires a **new, explicitly authorized** same-population descriptive run (even if only **H_sort** and simple dispersion — not hero/LG).

---

## Remaining decision

**Is existing evidence enough to pick one measure for the next small same-population comparison?**

**Not quite — one provenance check first, then Charles can authorize the comparison.**

| Measure | Verdict on this population |
|---------|----------------------------|
| **PPM** | **Fully defined** on the 4,267 audit file; provenance closed for ASSORT. |
| **BPM / PER** | **~98% joinable** by ESPN keys, but **match lineage is not tied to the audit build**, and **93** players lack finite BPM with **91** true key misses documented in existing QA. |

**Recommended narrow check (read-only, no rescrape):** For the **91** audit `left_only` keys (+ **2** null-BPM keys), produce a **one-page classification** from **`bpm_panel_rows_unmatched.csv`**, crosswalk slug, and displayed names — buckets such as “likely slug,” “likely name variant,” “no SR advanced row,” “unclear.” Stop there unless Charles authorizes rematch or scrape.

**After that check (or if Charles accepts ~2% key miss):** Authorize a **bounded descriptive** same-population comparison (PPM vs BPM vs PER on standardized values **within 2015**, reporting **H_sort** and simple team-interval width **without** selecting the “winner” by magnitude). That step is **not** part of this SCOUT reply per the stop rule.

---

*SCOUT read-only provenance review — no pipeline or analytical artifacts modified.*
