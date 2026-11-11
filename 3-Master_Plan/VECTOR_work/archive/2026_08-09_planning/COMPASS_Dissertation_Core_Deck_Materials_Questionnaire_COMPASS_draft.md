# COMPASS draft answers — Dissertation Core Deck Handoff to VECTOR

**Status:** COMPASS prefill (2026-09-15). **Charles locks Sep 16** in § Charles response block + handoff checklist.

**Sep 16 phase note:** This questionnaire is **background for ~1 month out**. **Week-one VECTOR deliverable** = **`STORY_OUTLINE_Charles_Alex.md`** (story beats + have/partial/need tags). See [`handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md`](handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md) — **VECTOR has no repo access**; Charles uploads that folder.

**Blank template:** [`COMPASS_Dissertation_Core_Deck_Materials_Questionnaire.md`](COMPASS_Dissertation_Core_Deck_Materials_Questionnaire.md)  
**Charles checklist:** [`../re_entry/_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md`](../re_entry/_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md)

**Provisional story arc (Alex/COMPASS):**

> Army discovery → cross-domain replication in NCAA men's basketball and R1 academic tenure → simple Wang-style mechanism/model → model characterization → predictions and tests.

Charles confirmed judgment calls Sep 16; narrative **order** deferred to VECTOR proposal for Alex meeting.

---

# 1. Current State

### 1.1 Canonical handoff

**COMPASS:**

1. **Read first:** `3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md` — slide claims Acts 0–VI (authority after Charles red-pen).
2. **Sequencing / gaps:** `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md`
3. **Alex locks:** `transcripts/PD30_notes.md`
4. **Orientation (not deck SSOT):** `3-Master_Plan/re_entry/00_READ_ME_FIRST.md`

### 1.2 Project map

**COMPASS:**

| Doc | Role |
|-----|------|
| `3-Master_Plan/re_entry/01_The_Problem_in_Plain_English.md` | Phenomenon + thesis |
| `3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md` | Layer A/B/C; score ≠ select |
| `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | **BINDING** three separations |
| `3-Master_Plan/plans/20260721_hero_model_reset.plan.md` | Longer working plan |
| `3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md` | POST-QC MBB hero locks + Wang ladder |

### 1.3 Major changes since VECTOR’s last close involvement

**COMPASS:**

- **PD29–PD30:** Paper flipbook is P0 intellectual work; Army = scientific origin, MBB = Common Access Card gap replication, tenure = third leg.
- **Army PNGs (Sep 15):** Extracted from executed AWS notebook → `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/` (G1 sandbox OK; **CAC access restored Sep 16** — AWS refresh unblocked).
- **MBB reigning lock:** last-ps · EW16 · poolq leave-one-out · mg10 · min20 · 2009–2021 (`mbb_reigning_3x3_manifest.json`).
- **Tenure PD29 lock:** decision cohort · dept LOO · career rate · Q16 (`tenure_pd29_3x3_manifest.json`).
- **Folder naming drift:** λ knockout sim outputs live in `HEROs_and_PASSes/pass_b/` (**G2** PNG ✅ Sep 15). ρ ablation in `pass_c_rho/`. Doc 04 “Pass B” = ρ, not λ — see §13.3.

### 1.4 Locked versus provisional

**COMPASS:**

| Status | Items |
|--------|--------|
| **LOCKED** | Environment `L_net = B − D` ≠ advancement; advancement = **score** (`S_i`, λ) then **select** (top K) — `BINDING_Selection_is_its_own_step.md` |
| **LOCKED** | Three-layer model (outcome / mechanism / sim) — `02_Three_Kinds_of_Model.md` |
| **LOCKED** | Army-first narrative anchor (MBB stand-in during CAC gap; **CAC restored Sep 2026**) — flipbook § Charles lock |
| **LOCKED** | **Charles (Sep 16):** Army HERO shape locked; MBB definite tendency (weaker); tenure reliable, improves with N |
| **LOCKED** | MBB reigning spec — `sports_sandbox/data_story/mbb_reigning_3x3_manifest.json` |
| **LOCKED** | Tenure PD29 spec — `tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json` |
| **CURRENT BEST** | Flipbook slide claims Acts 0–VI — drafted, **pending Charles red-pen** |
| **CURRENT BEST** | Army G1 from `army_sandbox/` extract (Sep 15) |
| **CURRENT BEST** | Alex v1 score `S_i = A_i − λ·L_C` — `Model.pptx` / `540_READ_ME_SIM.md` |
| **PROVISIONAL** | Grandchild (LG) assign as canonical vs Parent/Child — `[CHARLES — deck canonical ASSIGN?]` |
| **PROVISIONAL** | Tenure formal Cox parallel (G3) — **Charles: nice-to-have, not defense-blocking** |
| **PROVISIONAL** | Three-domain composite figure (composable, not built) |
| **SUPERSEDED** | 14-doc print stack — `3-Master_Plan/archive/numbered_print_stack/` |
| **SUPERSEDED** | mg=0 HERO as canonical MBB porch — see `sports_sandbox/README.md` |

---

# 2. Army — Discovery and Bedrock Evidence

### 2.1 Origin of the phenomenon

**COMPASS minimum set:**

| Item | Path |
|------|------|
| Pipeline overview (SSOT) | `talent/documents/520_PIPELINE_COX_OVERVIEW.md` |
| Working notebook (repo) | `talent/talent_pipeline/520_pipeline_cox_working.ipynb` |
| Executed notebook (figure source) | `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb` — 29 embedded PNGs, Cell 11+12 run |
| Slide interpretation | `talent/documents/Presentation_Interpretation_Run1_Slides_5-20.md` |
| Cox methods | `talent/documents/COX_METHODS_BRIEF.md`, `CR_AND_HR_FOR_DUMMIES.md` |
| Army→MBB handoff | `talent/documents/Army_to_College_Basketball_Replication_Handoff.md` |

**Key cells:** Cell 11 — CIF bars on `z_pool_minus_mean_snr_fwd` (hero) and `z_tb_ratio_fwd_snr` (own top-block); Cell 12 + 12.6A — Cox quadratic on pool-minus-mean.

`[CHARLES — confirm reigning AWS export: 20260320 vs 20260421 folder]`

### 2.2 Canonical Army figures

**COMPASS:**

| Figure | Path | One sentence | Type | Defense-ready? |
|--------|------|--------------|------|----------------|
| **G1 hero CIF** | `HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png` | Promotion cumulative incidence vs pool-minus-mean (8 bins); inverted-U | Layer A porch | ✅ extracted Sep 15; `[CHARLES confirm]` |
| Own-TB baseline | `…/ARMY_own_tb_ratio_fwd_cif_b8.png` | Own top-block ratio monotone with promotion CIF | Layer A control axis | ✅ |
| Partial effects | `…/ARMY_partial_effects_pool_minus_mean.png` | Cox quadratic curvature check | Formal check | ✅ |
| Extract manifest | `…/army_sandbox/EXTRACT_MANIFEST.txt` | Slot → AWS filename map | Meta | — |
| Regen | `scripts/extract_army_figures_from_520_notebook.py` | Notebook → sandbox | Code | — |

### 2.3 Robustness and identification

**COMPASS:**

**Core deck:** Cell 11 CIF porch; Cell 12 quadratic Cox; flipbook Act I claims 1.2–1.4.

**Backup / appendix:** `Presentation_Interpretation_Run1_Slides_5-20.md` (backward pool-minus-mean sensitivity, Slides 11–17); `talent/documents/COUNTERINTUITIVE_RESULTS_AND_RUNS.md`; optional `army_sandbox/ARMY_cox_competing_risks_analysis_stdz.png`.

**Limitation (LOCKED in flipbook):** own top-block ↔ pool-minus-mean r ≈ 0.93 — CIF porch = headline; Cox = formal curvature check, not reduced-form causal identification.

### 2.4 Canonical Army terminology

**COMPASS:**

| Use | Avoid |
|-----|-------|
| **pool minus mean** / **pool-minus-mean (leave-one-out-style)** | “star pool” without naming axis |
| **senior-rater pool** | vague “unit quality” |
| **top-block (TB) ratio** | undifferentiated “performance” |
| **Layer A hero porch** | calling hero “the model” |
| **promotion CIF** / **competing risk attrition** | draft/NBA language on Army slides |

---

# 3. NCAA Men’s Basketball — Cross-Domain Replication

### 3.1 Canonical dataset/sample

**COMPASS:**

- **Manifest SSOT:** `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json`
- **Talk track:** `…/MBB_DATA_STORY_plot_highlights.md`
- **Sandbox README:** `…/sports_sandbox/README.md` (leave-one-out vs team mean, mg10 QC)
- **Pipeline:** `sports/530_sports_pipeline.ipynb`
- **Empirical bundle:** `sports/scripts/pass_a_empirical_bundle.py`

**Lock:** 2009–2021 · last college season · mg10 · min20 · ALLT · PPM z · poolq leave-one-out · EW16 · ever drafted · N = 22,795 / 615 drafted (~2.7%).

### 3.2 Canonical NCAA finding

**COMPASS:**

- 3×3 deck: `…/sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png`
- Reigning HERO (panel 9): `…/sports_sandbox/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png`
- POST-QC narrative: `HEROs_and_PASSes/PD20_22_campaign_big_picture.md`
- Empirical archive: `HEROs_and_PASSes/pass_a/`

### 3.3 LOO versus team-mean geometry

**COMPASS:**

- `sports_sandbox/README.md` — leave-one-out vs poolq, mg=0 vs mg=10 vs F-HERO
- MBB panel 5 (team interval overlap): manifest path under `reigning_hero/basic_data_plots/REIGNING_team_interval_overlap_mg10_min20_09_21.png`
- MBB panel 2 (Â vs T̂_j): `reigning_hero/basic_data_plots/REIGNING_BDP_Ai_Tj_…png`
- Football pedagogy (optional Act V): `football_sandbox/perf_story/FOOTBALL_usage_Tj_q16_ew16.png` + LOO usage panel

### 3.4 Remaining QC/data issues

**COMPASS:**

- Weaker elite-tail dip vs Army (β₂ ≈ +0.002 — middle rise, softer tail).
- Panel 7 CCT uses 2011–21 +DFT window (not full 09–21).
- Division filter blocked — SCOUT note in sandbox README.

`[CHARLES — any QC issue you want flagged to Alex in deck?]`

### 3.5 Must-show NCAA figures

**COMPASS:**

1. `MBB_DATA_STORY_reigning_3x3.png` — full porch
2. `…/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png` — reigning hero
3. `…/fhero/BDP_Ai_draft_mass_ecdf_mg10_min20_09_21_allt_ppm_last_ps.png` — own Â monotone (panel 4)
4. `…/basic_data_plots/REIGNING_team_interval_overlap_mg10_min20_09_21.png` — leave-one-out motivation (panel 5)
5. [Optional] elite pond twin — `…/_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_…png`

---

# 4. R1 Academic Tenure — Third Domain

### 4.1 Dataset/outcome

**COMPASS:**

- Manifest: `tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json`
- Overview: `tenure/documents/TENURE_PIPELINE_OVERVIEW.md`
- Gameplan: `tenure/documents/TENURE_DATA_GAMEPLAN.md`
- Notebook: `tenure/540_tenure_pipeline.ipynb`
- PD29 notes: `transcripts/PD29_notes.md`

**Lock:** decision year · infHM all resolved · dept LOO whole-dept · Â = pubs per career year · Q16 · N ≈ 391 resolved.

### 4.2 Canonical tenure finding

**COMPASS:**

- 3×3: `tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png`
- Reigning HERO: `tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_slide.png`
- Talk track: `tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md`
- Act II probes (thin n): `tenure_sandbox/act2/`

### 4.3 Cross-domain mapping

**COMPASS:**

- **Best crosswalk today:** flipbook Acts I–III + `PAPER_Campaign_Plan.md` §0 — **no single authoritative three-column table doc**.
- Parallel structure: MBB and tenure 3×3 manifests (9-panel grid).
- Army→MBB explicit: `talent/documents/Army_to_College_Basketball_Replication_Handoff.md`

### 4.4 Domain-specific differences

**COMPASS:**

- **Army:** time-varying Cox, competing risks, largest N, strongest inverted-U.
- **MBB:** draft ever-Y, team-season grain, mg10 QC removed spurious mg=0 dip.
- **Tenure:** sparse N, metric choice moves porch (`TENURE_PERF_METRIC_STORY*.png`).
- **All three:** leave-one-out on peer pond; own-performance axis monotone separately.

### 4.5 Must-show tenure figures

**COMPASS:**

1. `TENURE_DATA_STORY_pd29_3x3.png`
2. `…/hero/HERO_tenure_q16_decision_dept_loo_infHM_slide.png`
3. `TENURE_PERF_METRIC_STORY.png` (+ `TENURE_PERF_METRIC_STORY_p2.png` sensitivity)
4. [Optional] `tenure_sandbox/act2/CCT_tenure_rate_ai_band_dept_loo_pd29_z1_2_q8.png`

---

# 5. Cross-Domain Empirical Phenomenon

### 5.1 Current best statement

**COMPASS:**

> Scarce advancement plus strong peers produces a **repeatable hero-shaped outcome pattern** when binning advancement on **peer pond quality (leave-one-out)**, with own talent on a separate monotone axis. Signal strength: Army > MBB > tenure.

Source: flipbook § One-sentence thesis + `PAPER_Campaign_Plan.md`. **`[CHARLES — approve wording]`**

### 5.2 Common statistical object

**COMPASS:**

| Domain | Operationalization |
|--------|-------------------|
| Cross-domain prose | BINDING Layer A = binned advancement rate vs leave-one-out pool quality |
| Army | `z_pool_minus_mean_snr_fwd` quantile bins → promotion CIF |
| MBB | `poolq_LOO` EW16 bins → draft rate (LPM β₂ in manifest) |
| Tenure | dept LOO career rate Q16 → tenure rate (β₂ ≈ −0.017) |

**No single canonical equation doc** — `sports/documents/Hero_Model_Three_Layers_Memo.md` is shorthand reference (park until doc 02 is easy).

### 5.3 Cross-domain comparison visual

**COMPASS:** **No pre-built three-domain figure.** Composable from Army G1 + MBB panel 9 + tenure panel 9 (flipbook slide 3.3 prose). `build_flipbook_figure_deck.py` builds inventory/talk decks, not a composite.

### 5.4 Alternative explanations

**COMPASS:**

| Alternative | Where addressed |
|-------------|-----------------|
| Own talent confounding | Separate Â / own-TB panels all three domains |
| Team mean includes self | Leave-one-out pedagogy: football twin, MBB panel 5 |
| Sample/QC (mg=0) | `sports_sandbox/README.md`, PD20_22 big picture |
| Metric choice (tenure) | `TENURE_PERF_METRIC_STORY*.png` |
| Causal peer effects | flipbook Act VI — **not claimed** |

---

# 6. Theory and Literature

### 6.1 Core literature

**COMPASS:**

| Bucket | Repo pointers |
|--------|---------------|
| Wang-style methodology | `HEROs_and_PASSes/PD20_22_campaign_big_picture.md` Part 1; flipbook G4 stub |
| Local competition / λ | `3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md` |
| Assortative formation | `VECTOR_work/VECTOR_Bipartite_Assortative_Formation_Model.md` |
| Selection/advancement | `BINDING_Selection_is_its_own_step.md` |
| Alex magnitude (Phase C, parked) | `05_Alex_Magnitude_Spec.md` |

`[CHARLES — exact Wang paper citation for §8.1 if locked outside repo]`

### 6.2 Companion/literature documents

**COMPASS:**

- re_entry `01`–`08` under `3-Master_Plan/re_entry/`
- `Model.pptx` / `Model.pdf`
- `VECTOR_work/VECTOR_Saracco_Bomiriya_ASSIGN_Reading_Guide.md`
- `VECTOR_work/VECTOR_Alex_ASSIGN_Configuration_Model_Response.md`
- `VECTOR_work/Quayle_One_Page_Formula_Concept_Sheet.md` (if present)

### 6.3 Abandoned literature paths

**COMPASS:**

- 14-doc stack: `3-Master_Plan/archive/numbered_print_stack/`
- Big Fish domains: `HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md`
- Archived correspondence: `3-Master_Plan/archive/`, `obsolete/correspondence_rounds/`

---

# 7. Current Canonical Simple Model

### 7.1 Architecture

**COMPASS:**

| Layer | Path |
|-------|------|
| One-slide story | `3-Master_Plan/re_entry/Model.pptx`, `Model.pdf` |
| Plain English | `02_Three_Kinds_of_Model.md` |
| Pass A/B prose | `04_Pass_A_and_Pass_B_in_Plain_English.md` |
| Sim contract | `sports/540_READ_ME_SIM.md` |
| Execution order | `3-Master_Plan/re_entry/model_OPORD.md` |
| Code | `sports/tier1_pool_assignment.py`, `tier1_generative_eda.py`, `tier1_sim_config.py` |

### 7.2 Levine–Gates (LG) ASSIGN

**COMPASS:**

| Item | Path |
|------|------|
| COMPASS brief | `VECTOR_work/COMPASS_BRIEF_ASSIGN_GRANDCHILD.md` |
| Detailed instructions | `VECTOR_work/COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md` |
| VECTOR formation spec | `VECTOR_work/VECTOR_Bipartite_Assortative_Formation_Model.md` |
| One-page homophilic model | `VECTOR_work/VECTOR_One_Page_Homophilic_Initial_League_Model.md` |
| Implementation | `sports/tier1_pool_assignment.py` (Parent/Child/Grandchild modes) |
| ρ calibration | `sports_sandbox/reigning_hero/calibration/README.md`; slides `CHAR_PD21_MLE_fit_13_21_HAND.pptx` |

**Status:** Grandchild = **experimental arm** per COMPASS brief. `[CHARLES — LG vs Parent/Child for defense deck?]`

### 7.3 SCORE

**COMPASS:**

- Equation: **`S_i = A_i − λ·L_C`** (Alex v1; congestion only in score).
- λ threshold: `06_Lambda_threshold_and_KN_memo.md`
- Phase B slides: `07_Phase_B_Characterization_Slides_Explained.md`
- λ knockout: CSVs in `pass_b/`; PNG path `pass_b/PASS_B_generative_lambda_knockout_side_by_side.png` — **file not in repo as of Sep 15; regen via `sports/scripts/pass_b_generative_knockout_bundle.py` (G2)**
- Script: `sports/scripts/pass_b_generative_knockout_bundle.py`

### 7.4 SELECT

**COMPASS:**

- v1: **top K** by score (deterministic).
- Scarcity: K/N in `tier1_sim_config.py`; θ from K/N — PD16 (`08_PD16_Alex_meeting_takeaways.md`).
- BINDING: stochastic select = future step only.

### 7.5 Model behavior already demonstrated

**COMPASS (point to evidence; do not rerun for confirmation):**

| Behavior | Evidence |
|----------|----------|
| λ=0 monotone vs λ>0 elite compression | `pass_b/` CSVs + caption files; PNG G2 |
| λ ablation sweep | `pass_b/PASS_B_lambda_ablation_*.png` (if present) |
| ρ → roster geometry / L_C | `pass_c_rho/LC_distribution_vs_rho_*.png` |
| ρ calibration / MLE | `slides/CHAR_PD21_MLE_fit_13_21_HAND.pptx` |
| Grandchild ρ sweep | `slides/CHAR_grandchild_league_analysis.pptx` |

### 7.6 Known failures/discrepancies

**COMPASS:**

- Sim bins **pool mean**; empirical hero bins **poolq leave-one-out** — qualitative proof-of-concept only (flipbook Act IV 4.2).
- Bar-for-bar hero match **not** v1 gate (`540_READ_ME_SIM.md`).
- Separate B(Q)/D(Q) curves **not** estimated (`BINDING`).
- ρ→530 calibration gap — see `PARKED_FOR_LATER.md`.

---

# 8. Wang-Style Strategy

### 8.1 Exact Wang source

**COMPASS:** Methodological inspiration referenced throughout as “Wang-style arc” (phenomenon → minimal mechanism → prediction). Best in-repo summary: `HEROs_and_PASSes/PD20_22_campaign_big_picture.md` Part 1.

`[CHARLES — paste exact Wang paper citation if locked]`

### 8.2 Modeling logic

**COMPASS:** Confirmed in flipbook + doc 01:

$$\text{Empirical regularity} \rightarrow \text{minimal mechanism} \rightarrow \text{prediction} \rightarrow \text{validation} \rightarrow \text{extension}$$

Pass structure: empirical hero (Layer A) → Pass A λ knockout → Pass B/C ρ (`04_Pass_A_and_Pass_B_in_Plain_English.md`).

### 8.3 Parameter classification

**COMPASS:**

| Parameter | Class |
|-----------|-------|
| **ρ** | Mechanism / assignment behavioral |
| **λ** | Scoring behavioral (congestion weight) |
| **C** (roster cap) | Structural constraint |
| **K/N** | Advancement scarcity / structural |
| **N** (league size) | Simulation choice |

---

# 9. Predictions — Next Scientific Step

### 9.1 Predictions proposed

**COMPASS:** λ knockout comparative statics; ρ → within-team dispersion / L_C; θ(K/N) threshold; Alex Phase C magnitude (parked).

### 9.2 Predictions tested

**COMPASS:**

| Test | Code | Output |
|------|------|--------|
| λ knockout | `sports/scripts/pass_b_generative_knockout_bundle.py` | `pass_b/` CSVs + captions; PNG G2 |
| ρ ablation | `sports/scripts/540_rho_ablation_bundle.py` | `pass_c_rho/` |
| Grandchild ρ sweep | `sports/scripts/grandchild_*.py` | slides + diagnostics |

### 9.3 Phase structure

**COMPASS:** Partial ρ slices in `pass_c_rho/`; λ ablation in `pass_b/`. Full ρ×λ phase map **not complete** — `06_Lambda_threshold_and_KN_memo.md`. Phase B deck: `07_Phase_B_Characterization_Slides_Explained.md` + `slides/CHAR_gamma_characterization.pptx`.

### 9.4 Highest-value next experiments

**COMPASS (agreed plans):**

1. **G1** Army AWS porch refresh (**CAC restored** — Charles priority when ready)
2. **G2** λ knockout slide — **core / must-show** (PNG ✅ Sep 15)
3. **G4** contribution — **6.3 approved**; VECTOR polish + alternate draft
4. Three-domain composite visual (built Sep 15 — flipbook 3.3)
5. **G3** tenure formal Cox — **nice-to-have**

**Charles (Sep 16):** No active backup legs in defense deck — football / Big Fish = placeholders only.

### 9.5 Prospective validation

**COMPASS:**

- Army: refresh Cell 11–12 on AWS (**CAC access restored Sep 2026**)
- Tenure: scrape bolster (`20260901_COMPASS_to_PEER_tenure_scrape_bolster.pdf`)
- MBB: division filter (blocked SCOUT)
- Big Fish: parked

---

# 10. Dissertation Narrative and Defense Deck

### 10.1 Existing outlines

**COMPASS (newest first):**

1. `_DISPOSABLE_paper_flipbook_PD30.md`
2. `PAPER_Campaign_Plan.md`
3. re_entry `01`–`04`
4. `plans/20260721_hero_model_reset.plan.md`
5. `_DISPOSABLE_paper_flipbook_PD30_FIGURE_DECK.pptx` (talk skeleton)
6. `_DISPOSABLE_paper_flipbook_PD30_FIGURE_INVENTORY.pptx` (full catalog)

### 10.2 Candidate narrative

**COMPASS:** Acts 0→VI in flipbook: Frame → Army → MBB → Tenure → Mechanism → leave-one-out pedagogy (optional) → Limits/gaps.

**Charles (Sep 16, §4c):** Defer narrative order — **VECTOR to propose** Acts 0→VI vs alternatives before Charles locks.

### 10.3 Core versus backup

**Charles confirmed §4a (Sep 16):**

| Tier | Content |
|------|---------|
| **Must-show core** | Army G1, MBB panel 9, tenure panel 9, Model.pptx, λ knockout **G2 (core)**, BINDING table |
| **Supporting robustness** | Army Cox partials, MBB panels 5/8, tenure perf story |
| **Technical validation** | pass_c_rho, grandchild slides, Phase B CHAR_* decks |
| **Placeholders only (not active backup)** | Big Fish 3×3s, football composite, legends — other-dataset placeholders, not defense legs |

### 10.4 Dissertation versus paper

**COMPASS:** PD30 plan: **dissertation/defense first**, paper after; flipbook = paper-talk prototype. MBB honest-access narrative (Army origin, basketball stand-in) — flipbook slide 0.4.

**Charles (Sep 16, §4d):** **No** Alex-specific dissertation-vs-paper split — **same story** (paper may be shorter later).

### 10.5 Claims we cannot yet make

**COMPASS:**

- Causal peer effects / development channel separation
- Universal inverted-U magnitudes across domains
- Real leagues literally maximize `S_i`
- Bar-for-bar sim-to-empirical match
- Big Fish as primary legs

**Charles (Sep 16, §4e):** No additional prohibited claims beyond COMPASS list above for now.

---

# 11. Figures, Slides, and Visual Assets

### 11.1 Existing decks

**COMPASS (priority order):**

1. `_DISPOSABLE_paper_flipbook_PD30_FIGURE_DECK.pptx` — **talk skeleton** (Acts 0–VI)
2. `_DISPOSABLE_paper_flipbook_PD30_FIGURE_INVENTORY.pptx` — **superset catalog**
3. `Model.pptx` — mechanism one-slide
4. `HEROs_and_PASSes/slides/CHAR_PD16_HAND.pptx` — Phase B
5. `CHAR_PD20_22_takeaways_memo_HAND.pptx` — POST-QC
6. `CHAR_PD21_MLE_fit_13_21_HAND.pptx` — ρ/MLE
7. `CHAR_grandchild_league_analysis.pptx` — LG diagnostics

Regen flipbook decks: `python scripts/build_flipbook_figure_deck.py`

**Superseded:** `CHAR_PD20_HAND_backup_20260817.pptx`; archived fhero under `sports_sandbox/_archive/`.

### 11.2 Figure inventory

**COMPASS:** Yes — flipbook § Figure inventory + INVENTORY.pptx/HTML. Authoritative dirs:

- Army: `HEROs_and_PASSes/army_sandbox/`
- MBB: `sports_sandbox/data_story/`, `hero/`, `reigning_hero/`
- Tenure: `tenure_sandbox/data_story/`, `hero/`
- Model: `pass_b/`, `pass_c_rho/`, `pass_a/`

JSON manifests: `mbb_reigning_3x3_manifest.json`, `tenure_pd29_3x3_manifest.json`.

### 11.3 Figures needing rebuild

**COMPASS:**

- Army: confirm sandbox PNGs vs latest AWS export `[CHARLES]`
- G2: λ knockout side-by-side PNG missing from git (CSVs exist)
- Pre–POST-QC mg=0 HERO in old decks — avoid

### 11.4 Missing visuals

**COMPASS:**

- Three-domain crosswalk composite
- ASSIGN→SCORE→SELECT schematic (partial via Model.pptx; may need LG refresh)
- ρ×λ phase map
- Phase C prediction diagram (parked)

---

# 12. Code and Reproducibility

### 12.1 Canonical entry points

**COMPASS:**

| Domain | Entry |
|--------|-------|
| Army | `talent/talent_pipeline/520_pipeline_cox_working.ipynb` |
| Army extract | `scripts/extract_army_figures_from_520_notebook.py` |
| MBB | `sports/530_sports_pipeline.ipynb`; `pass_a_empirical_bundle.py` |
| Tenure | `tenure/540_tenure_pipeline.ipynb`; `tenure/scripts/` |
| ASSIGN | `sports/tier1_pool_assignment.py` |
| Sim | `sports/540_three_step_sim.ipynb` |
| λ knockout | `sports/scripts/pass_b_generative_knockout_bundle.py` |
| ρ ablation | `sports/scripts/540_rho_ablation_bundle.py` |
| Flipbook decks | `scripts/build_flipbook_figure_deck.py` |

### 12.2 Superseded code

**COMPASS:** Ignore `sports/archive/` (535–538D notebooks); `539_alex_model.ipynb`; root `talent_pipeline/` duplicate; MCP raw JSON notebook edits.

**Naming trap:** folder `pass_b/` = **λ knockout sim**; folder `pass_a/` = **empirical hero**; folder `pass_c_rho/` = **ρ ablation** (doc 04 “Pass B”).

### 12.3 Reproducibility

**COMPASS:**

| Asset | Regenerable? | Gap |
|-------|--------------|-----|
| MBB 3×3 + HERO | ✅ | Needs local ESPN data |
| Tenure 3×3 | ✅ | Needs tenure panel |
| Army G1 | ⚠️ | AWS/CAC or extract script |
| λ knockout G2 | ✅ | PNG not committed |
| Flipbook PPTX | ✅ | `build_flipbook_figure_deck.py` |

---

# 13. Agent Knowledge and Handoffs

### 13.1 Other agents

**COMPASS:**

| Agent | Lane | Handoff |
|-------|------|---------|
| COMPASS | Sequencing, flipbook | `PAPER_Campaign_Plan.md`, `COMPASS_AGENT_IDENTITY.md` |
| VECTOR | Manuscript, theory | `VECTOR_work/*.md` |
| CODA | Army / talent | `520_PIPELINE_COX_OVERVIEW.md` |
| SCOUT | MBB / sim | `sports_sandbox/README.md`, `540_READ_ME_SIM.md` |
| PEER | Tenure | `TENURE_PIPELINE_OVERVIEW.md`, `20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.pdf` |

### 13.2 Recent handoffs

**COMPASS:** `_DISPOSABLE_paper_flipbook_PD30.md`; `PAPER_Campaign_Plan.md`; `transcripts/PD30_notes.md`; tenure scrape PDFs Sep 2026; `SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md`.

### 13.3 Unresolved disagreements

**COMPASS:**

- 520 notebook reigning copy: `talent/talent_pipeline/` vs AWS export dates
- LG vs Parent/Child for deck canonical ASSIGN
- Pass folder naming vs doc 04 labels — document clearly for VECTOR
- Army-forward story vs figure readiness (MBB/tenure ready now)
- Tenure metric: career rate reigning; annum pubs sensitivity remains

`[CHARLES — any disagreements with Alex/CODA to flag?]`

---

# 14. Prioritized Upload Manifest for VECTOR

### Tier 1 — Read before first slide-placeholder outline

**COMPASS:**

```
3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md
3-Master_Plan/re_entry/PAPER_Campaign_Plan.md
transcripts/PD30_notes.md
3-Master_Plan/BINDING_Selection_is_its_own_step.md
3-Master_Plan/re_entry/01_The_Problem_in_Plain_English.md
3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md
3-Master_Plan/re_entry/Model.pdf
talent/documents/520_PIPELINE_COX_OVERVIEW.md
3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png
3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json
3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png
3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json
3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png
3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30_FIGURE_DECK.pptx
3-Master_Plan/VECTOR_work/COMPASS_Dissertation_Core_Deck_Materials_Questionnaire_COMPASS_draft.md
```

Add `pass_b/PASS_B_generative_lambda_knockout_side_by_side.png` when G2 regen completes.

`[CHARLES — veto or add to Tier 1?]`

### Tier 2 — While fleshing empirical/model sections

**COMPASS:**

```
3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md
sports/540_READ_ME_SIM.md
HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_plot_highlights.md
HEROs_and_PASSes/tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md
talent/documents/Presentation_Interpretation_Run1_Slides_5-20.md
HEROs_and_PASSes/sports_sandbox/README.md
3-Master_Plan/plans/20260721_hero_model_reset.plan.md
3-Master_Plan/VECTOR_work/VECTOR_Bipartite_Assortative_Formation_Model.md
HEROs_and_PASSes/PD20_22_campaign_big_picture.md
_DISPOSABLE_paper_flipbook_PD30_FIGURE_INVENTORY.pptx
tenure/documents/TENURE_DATA_GAMEPLAN.md
```

### Tier 3 — Reference / robustness / backup

**COMPASS:**

```
06_Lambda_threshold_and_KN_memo.md
07_Phase_B_Characterization_Slides_Explained.md
08_PD16_Alex_meeting_takeaways.md
HEROs_and_PASSes/pass_c_rho/
HEROs_and_PASSes/pass_a/sensitivity/
HEROs_and_PASSes/football_sandbox/perf_story/
HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md
talent/documents/Army_to_College_Basketball_Replication_Handoff.md
scripts/build_flipbook_figure_deck.py
scripts/extract_army_figures_from_520_notebook.py
```

### Do not upload unless requested

**COMPASS:**

```
3-Master_Plan/archive/numbered_print_stack/
3-Master_Plan/obsolete/
.specstory/
sports/archive/
talent/Army_AWS_download/ (full tree — use army_sandbox PNGs)
sports_sandbox/_archive/
```

---

# 15. Final Executive Handoff

**COMPASS draft — `[CHARLES APPROVE each bullet]`**

1. **What have we discovered?** In Army officer promotion data, advancement vs **leave-one-out-style pool-minus-mean** in the senior-rater pool shows a **strong inverted-U** (strongest of three domains). Own top-block performance rises monotonically on a separate axis. Evidence: `army_sandbox/ARMY_G1_*.png`, flipbook Act I.

2. **What have we replicated across domains?** The same **qualitative family** — advancement vs peer pond quality (leave-one-out) can rise through mid ponds then soften at the elite tail — appears in **NCAA men's basketball** (draft, weaker tail) and **R1 tenure** (decision cohort, graded signal). Evidence: MBB panel 9, tenure panel 9, manifests.

3. **What mechanism are we proposing?** **Minimal assign → score → select:** homophilic assignment places talent in ponds; **score** `S_i = A_i − λ·L_C` can embed congestion in ranking; **select** top K produces advancement scarcity. Environment `L_net = B − D` is **not** the advancement step. Evidence: `Model.pptx`, `BINDING`, `540_READ_ME_SIM.md`.

4. **What has the simple model already demonstrated?** λ=0 vs λ>0 knockout shows congestion **in the score** can compress elite bins (qualitative POC; CSVs in `pass_b/`). ρ ablations show assignment geometry moves team congestion distribution (`pass_c_rho/`). Not bar-for-bar empirical match.

5. **What predictions are we about to test?** θ(K/N) threshold work open (`06_Lambda_threshold_and_KN_memo.md`); Phase C Alex magnitude parked; **G1 AWS refresh** (CAC restored Sep 2026); tenure formal Cox (G3, nice-to-have); three-domain composite built (flipbook 3.3).

6. **Biggest unresolved threats before defense:** (a) causal identification not claimed — sorting/confounding; (b) Army own-TB ↔ pool-minus-mean correlation; (c) sim bins pool mean vs empirical leave-one-out; (d) tenure N sparse; (e) **G1a** all-branches army hero PNG regen; (f) slide **1.4** Cox pop + HR explainer. **1.1 ✅** — HERO robust across branch slices; deck plan = all-branches anchor + CS+CSS stronger slice. **G4 contribution approved** (6.3).

---

## Charles response block (Sep 16, 2026)

```
FLIPBOOK RED-PEN: mostly OK — 1.1 ✅ (HERO robust across branches; all-branches anchor + CS+CSS stronger slice; G1a regen pending). Open: 1.4 (Cox pop + HR explainer). Act V parked.
FIGURE DECK NOTES: [pending Step 2 skim — spot-check 2.2 naïve, 3.3 composite, 4.2 G2]
6.3 G4: approved — VECTOR may polish wording; also send alternate contribution draft
4a CORE vs BACKUP: Core = Army + MBB + Tenure + Model + Pass A λ slide. No active backup legs — football/legends/Big Fish placeholders only.
4b LOCKED vs PROVISIONAL: Army HERO locked. MBB less convincing but definite tendency. Tenure reliable, improves with more data.
4c NARRATIVE ORDER: defer — want VECTOR's suggestions on Acts 0→VI before locking
4d DISS vs PAPER: NO split — same story (paper shorter later)
4e DO NOT CLAIM: none beyond COMPASS defaults for now
G1–G5 PRIORITIES:
  G1 — CAC restored; refresh AWS porch PNGs when ready; sandbox OK interim
  G2 — core / must-show (model kept, not fully deployed everywhere); PNG regen done Sep 15
  G3 — nice to have
  G4 — 6.3 approved; VECTOR polish + alternate draft
  G5 — CAC access restored; VECTOR may draft deck status wording
ORIGIN STORY: confirmed — Army first; MBB stand-in during CAC gap; tenure portability; CAC back Sep 2026
TIER 1 VETO/ADD: [none yet]
OTHER FOR VECTOR: propose narrative order (4c); gap-slide wording options for 6.2
```
