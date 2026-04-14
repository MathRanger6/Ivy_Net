# Army -> College Basketball Replication Handoff (for Coding LLM Agent)

## 0) Purpose of this handoff

This document gives a coding-focused LLM enough context to continue the project without re-discovering prior work.

Assumption:
- The receiving agent already understands the existing college basketball pipeline and current codebase (including `sdv_second.ipynb`).
- Therefore this handoff emphasizes **research direction, mapping decisions, and replication criteria**, not basic implementation onboarding.

Primary objective:
- Replicate the **Army finding** that advancement probability has an **inverted-U** relationship with peer-pool quality (improves at low/mid pool quality, weakens at very high pool quality).

Secondary objective:
- Explore multiple Army->college mappings (not just one), compare results, and preserve flexibility while iterating with the human researcher.

Core question to replicate:
- Do we see the same "upside-down U" in college basketball advancement outcomes under credible pool definitions and controls?

---

## 1) Where the project stands (high-level)

From Army data work:
- The core empirical result is already established in the Army pipeline and summarized in existing docs:
  - `current_documents/Publication_Plan.md`
  - `current_documents/advisor_brief_twofold_status.pdf`
  - `current_documents/sports_mechanisms/advisor_packet_COMPACT_CLEAN.md`
  - `current_documents/sports_mechanisms/sports_replication_strategy_FINAL.md`
  - `current_documents/sports_mechanisms/model_walkthrough_reference.md`
- Stylized finding: an **inverted-U** relationship between advancement and pool quality.
- Mechanism framing used so far:
  - Positive channel: signal quality / credibility in stronger pools.
  - Negative channel: congestion / competition / rank-in-pool compression at very high pool quality.

From sports coding work:
- The college-basketball data infrastructure is actively underway.
- `sdv_second.ipynb` currently focuses on robust matching between draft records and ESPN athlete IDs to create reliable advancement labels.
- Several sports mechanism docs and empirical design docs are already in place under:
  - `current_documents/sports_mechanisms/`

Execution-context note:
- Some Army development used an SWS workflow where code was co-developed and then transcribed/replayed in this workspace.
- Therefore, full local "from-zero rerun" visibility for every historical Army step is not always present here.
- Treat Army docs/configs/saved outputs as authoritative for what was executed and found.

---

## 2) Army work recap: what was done and what was found

### 2.1 Pipeline architecture (Army)

Canonical build path referenced in documentation:
- 502 -> 512 -> 520

Interpretation from project docs:
- `502`: base personnel snapshot panel.
- `512`: OER enrichment / linkage.
- `520`: main analysis pipeline (pool metrics, Cox/competing risks, CIF plots, diagnostics).

Related planning / extension path:
- `current_documents/525_plans.pdf` describes additional mechanism analyses (UIC, division, senior-rater consistency, longevity/path).

### 2.2 Core empirical object

Army model object (conceptual):
- Advancement outcome as function of own performance + pool quality + pool quality squared + controls.
- Pool quality defined from evaluation architecture (senior-rater x time; with optional branch/rank structure in some runs).

Representative notation used across documents:
- `PoolQ_{jt}^{(-i)}` as leave-one-out pool quality.
- Inverted-U test: quadratic term negative (`beta_3 < 0`), turning point `-beta_2 / (2*beta_3)`.

### 2.3 Main finding to carry forward

Across Army artifacts:
- Promotion probability rises with pool quality through low/mid ranges, then diminishes/reverses at high pool quality.
- This is the pattern to replicate in public datasets (sports first).

### 2.4 Interpretation constraints

The project currently treats mechanism as hypothesized and iteratively refined:
- Strong associative pattern with structured evaluation pools.
- Non-experimental setting -> avoid overclaiming causal identification.

---

## 3) Replication target in college basketball

### 3.1 Replication criterion (pass/fail for "same stuff")

A credible replication should show:
1. Pool-quality linear term positive/weakly positive in low/mid region.
2. Pool-quality quadratic term negative and meaningful.
3. Nonparametric bins/plots visually consistent with inverted-U (not purely monotone).
4. Pattern robust to reasonable pool/performance/outcome definitions.

### 3.2 Why college basketball is currently preferred

From existing sports docs:
- Teams provide natural pools (team x season).
- Advancement is scarce and competitive (draft / pro entry).
- Performance is measurable and observable.

**Affordance — team-level “organizational” success:** In basketball we can often observe **team outcomes** (wins, ratings, strength of schedule) as **controls** distinct from **peer talent** (leave-one-out pool quality) and distinct from **how talent is distributed on the roster** (congestion / roster-pressure constructs). In Army replication work, comparable **unit success** indicators may be harder to obtain at scale without sensitive readiness data; unclassified proxies (e.g., administrative flow, maintenance posture, training mix) may be explored in parallel but are **out of scope for the current sports coding path** unless separately sourced. See `obsolete_documents/sports_gameplan_old/College_Replication_Decision_Memo_Baseline_vs_Alternative_bkup.md` (**Advisor alignment**, **(7)** vs **(5)**).

### 3.3 Secondary setting (future)

Also documented:
- NBA longevity/hazard as follow-on replication setting.

---

## 4) Current sports coding status from `sdv_second.ipynb` (context only)

This notebook is important because it builds advancement labeling infrastructure.

### 4.1 What `sdv_second.ipynb` does now

Primary goal in notebook header:
- Match NBA draft picks (`nbaplayersdraft.csv`) to ESPN `athlete_id` in `mbb_df_player_box.csv`.

Core matching pipeline:
1. College string -> team mapping (exact).
2. Alias mapping via `COLLEGE_ALIASES`.
3. Fuzzy college -> ESPN school mapping when confidence thresholds are met.
4. One row per athlete selection from player-season data.
5. Block candidate athletes by school + draft-year window.
6. Fuzzy player-name matching.
7. Second pass with wider window if needed.

Key outputs currently produced:
- `datasets/mbb/draft_athlete_match.csv`
- `datasets/mbb/draft_match_review.csv` (read-only review extract—structured accept/reject for the optional dedupe model go in `draft_match_manual_feedback_template.csv`, not new columns on this file)
- `datasets/mbb/draft_unmapped_colleges.csv`
- `datasets/mbb/draft_unmapped_college_candidates.csv`
- `datasets/mbb/draft_unmapped_athlete_candidates.csv`
- `datasets/mbb/draft_match_manual_feedback_template.csv` (human labels for dedupe training)
- `datasets/mbb/athlete_id_draft_lookup.csv`

Practical implication:
- Advancement labels are already being built in a draft-centric, auditable way.
- Treat this as an existing capability; focus next effort on model-design choices and replication evidence.

---

## 5) Army -> college mapping candidates (run more than one)

The human researcher explicitly wants to explore multiple mappings.

### Mapping A (primary first pass)
- Outcome: draft/pro entry indicator (`Y_i`).
- Unit: player-season.
- Pool: team x season.
- Own performance: BPM (plus alternates like WS/40, usage-adjusted variants).
- Pool quality: leave-one-out teammate mean performance.

### Mapping B (roster pressure explicit)
- Outcome: pro entry.
- Pool quality: teammate quality + explicit congestion measures (e.g., concentration of top performers, usage share inequality, depth at position).

### Mapping C (dynamic panel framing)
- Outcome: conditional probability of pro entry by year window.
- Pools and quality vary over seasons; emphasize trajectory and exposure duration.

### Mapping D (secondary setting)
- NBA longevity/hazard setup with team-season pool exposure.

Implementation instruction:
- Do not hardcode one mapping; structure code so definitions are configurable.

---

## 6) Suggested roadmap for the coding LLM (decision-first)

### Phase 1 - Lock current iteration choices
- Choose and document: outcome definition, pool definition, own-performance metric, and control set for the baseline.
- Choose at least one alternative mapping for falsification/robustness.

### Phase 2 - Build/refresh modeling panel as needed
- Create player-season modeling table with:
  - player identifiers
  - team-season identifiers
  - own performance features
  - leave-one-out pool quality features
  - controls (season FE, position/class proxies if available, team strength)
  - advancement outcome (`Y_i`)

Minimum quality checks:
- No leakage in leave-one-out computations.
- Team-season sample-size constraints (avoid unstable tiny pools).
- Coverage diagnostics by season and school.

### Phase 3 - Baseline replication tests
- Estimate:
  - LPM and/or logit/probit with linear + quadratic pool quality.
- Compute:
  - turning point and confidence interval (delta method or bootstrap).
- Plot:
  - binned nonparametric relationship (deciles/ventiles, plus support checks).

Pass condition:
- Qualitative inverted-U appears and is not driven purely by extreme outliers.

### Phase 4 - Robustness and alternative mappings
- Re-estimate using:
  - alternate performance metrics
  - alternate pool definitions
  - alternate sample filters (minutes thresholds, role thresholds, era subsets)
  - stronger sorting controls where feasible

### Phase 5 - Reporting package
- Produce concise replication brief:
  - what matched Army pattern
  - what did not
  - which mapping appears most credible
  - what additional data would increase confidence

---

## 7) Known risks and how to handle them

1. **Name / school matching error**
- Risk: mislabeling outcomes.
- Mitigation: keep review outputs and confidence tiers; require audit sample before final models.

2. **Sorting into teams**
- Risk: better players select into better teams.
- Mitigation: richer controls, subgroup analyses, and transparent interpretation as associational.

3. **Mechanical correlation**
- Risk: own performance contaminates pool metric.
- Mitigation: leave-one-out pool quality by construction.

4. **Sparse support at tails**
- Risk: fake curvature from limited high-end observations.
- Mitigation: support diagnostics, bins with minimum counts, sensitivity to trimming/winsorization.

5. **Outcome definition sensitivity**
- Risk: draft-only vs broader pro-entry changes conclusions.
- Mitigation: run at least two outcome definitions.

---

## 8) Files to read first (recommended orientation order)

1. `current_documents/sports_mechanisms/advisor_packet_COMPACT_CLEAN.md`
2. `current_documents/sports_mechanisms/sports_replication_strategy_FINAL.md`
3. `current_documents/sports_mechanisms/college_basketball_empirical_design.md`
4. `current_documents/sports_mechanisms/model_walkthrough_reference.md`
5. `current_documents/Publication_Plan.md`
6. `current_documents/advisor_brief_twofold_status.pdf`
7. `current_documents/525_plans.pdf`
8. `sdv_second.ipynb`

Useful data artifacts:
- `datasets/mbb/draft_unmapped_college_candidates.csv`
- `datasets/mbb/draft_unmapped_athlete_candidates.csv`
- `datasets/mbb/draft_athlete_match.csv`
- `datasets/mbb/draft_match_review.csv` (read-only review; labels go in `draft_match_manual_feedback_template.csv`)
- `datasets/mbb/draft_match_manual_feedback_template.csv`
- `datasets/mbb/athlete_id_draft_lookup.csv`

---

## 9) Operational guidance for the coding LLM agent

- Keep all major definition choices parameterized (outcome, pool, performance).
- Track each run with explicit metadata (date, config, sample restrictions, metric choice).
- Always output both:
  - coefficient-based evidence (`beta_2`, `beta_3`, turning point),
  - visual/nonparametric evidence (binned plots with counts/support).
- Prioritize reproducibility and auditable intermediate files over one-shot model output.
- If a design choice is ambiguous, present options and request user selection before locking in.

### 9.1 Priority framing for an already-familiar agent

Given the agent already knows the sports pipeline, prioritize:
1. Correct replication logic over new infrastructure.
2. Side-by-side mapping comparisons over one "best guess" model.
3. Decision-grade outputs Charles can react to quickly (what changed, why, what to run next).

### 9.2 Plot pattern reference (Army signature to compare against)

Use this as the qualitative target when reading college outputs:
- Promotion CIF by bins: low -> mid increase, then high-bin flatten/decline.
- Final promotion CIF bars: hump shape (non-monotone) across bins.
- Attrition side should be interpreted jointly (not necessarily mirror image, but informative for mechanism consistency).

---

## 10) Handoff success criteria

The handoff is successful when the receiving agent can:
1. Explain the Army inverted-U finding in one paragraph.
2. Build and validate a college player-season panel with reliable advancement labels.
3. Run at least one primary and one alternative mapping.
4. Produce evidence for/against inverted-U with diagnostics.
5. Summarize replication status in a decision-ready memo for the human researcher.

---

## 11) Current intent reminder (from human researcher)

- The target pattern is the **upside-down U**.
- More than one Army->college mapping is expected and encouraged.
- The researcher and agent will discuss mapping choices iteratively during coding.
- If uncertain about intent at decision points, pause and request clarification.

