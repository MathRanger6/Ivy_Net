# SCOUT → COMPASS: Handoff Report (Basketball / Sports Domain)

> **Rename (2026-06-11):** Formerly `SCOUT_report_to_master_planner.md`; planning agent is **COMPASS**. See [COMPASS_AGENT_IDENTITY.md](COMPASS_AGENT_IDENTITY.md).

**Agent:** **SCOUT** (Cursor agent; NCAA basketball panel, Tier 1 modeling, generative simulation, HPC sweeps)  
**Domain root:** `./sports/` (panel + Tier 1 modules; shared panel CSV at workspace `datasets/mbb/`)  
**Report date:** 2026-06-08  
**Prepared for:** Charles Levine → future **COMPASS** agent (Cursor)  
**Charles’s explicit instruction (2026-06-08):** This report feeds the COMPASS. **Do not** begin drafting the cross-project master plan until Charles **assigns** that agent and asks for planning work. SCOUT/PEER/CODA/VECTOR should only **report status** until then.

**Companion reports (same folder):**
- [`CODA_report_to_COMPASS.md`](CODA_report_to_COMPASS.md) — Army / `talent/`
- [`PEER_report_to_COMPASS.md`](PEER_report_to_COMPASS.md) — Academia / `tenure/`
- **VECTOR report:** Not yet in repo as of this writing — expect manuscript-focused handoff from Scholar GPT workflow or a Cursor session dedicated to `5-Manuscript/`.

---

## 0. What this document is (and is not)

### What it is
- A **ground-truth status snapshot** of the basketball/sports lane as SCOUT understands it after work through **June 2026** (530 inverted-U replicated; 538 empirical Wang ladder; 538D generative CELL 10 congestion score; axis-conditioning finding; documentation pass).
- A **file map** so the COMPASS can navigate without re-deriving context from chat logs, SpecStory exports, or stale May briefs.
- A **list of open questions** where Charles’s intent is not fully locked — SCOUT prefers explicit answers over assumptions.
- Pointers to **CODA**, **PEER**, and **VECTOR** without claiming authority over Army pipelines, tenure scrape, or manuscript prose.

### What it is not
- **Not** the master plan itself.
- **Not** a claim that generative simulation **replicates** the empirical inverted-U on the same conditioning axis as 530 (`poolq_loo` / \(L_Q\) LOO).
- **Not** a substitute for reading **`sports/documents/SPORTS_DATA_GAMEPLAN.md`**, **`tier_1_roadmap.md`**, or **`538_Cell10_Generative_Manual.md`** when implementing or debugging notebooks.

---

## 1. Thesis frame (why SCOUT exists in this repo)

Charles’s dissertation tests **advancement under constrained distinction**: individuals compete in **local talent pools** while advancement is **globally scarce**. Mid-quality peer environments can produce the highest individual advancement rates; elite environments create **congestion / signal compression** that drives rates back down (inverted-U).

| Setting | Agent | Repo home | Outcome | Pool-quality construct |
|--------|-------|-----------|---------|-------------------------|
| 1 — Army | **CODA** | `talent/` | Promotion to Major vs attrition | Senior-rater LOO pool quality; CIF / Cox |
| 2 — Basketball | **SCOUT** | `sports/` | NBA draft (`Y_draft`) | `poolq_loo` (LOO teammate `perf`, usually PPM z) |
| 3 — Academia | **PEER** | `tenure/` | Tenure vs pre-tenure exit | `poolq_loo_mean` (LOO dept assistant pubs) |

**SCOUT’s job:** Build and maintain the **college basketball → NBA draft** empirical stack (530 conductor, panel exports, forensics), the **Alex-ordered Tier 1 modeling ladder** (538 / 538D), and the **modular generative lab** (`tier1_pool_assignment.py`, CELL 10 playground) that stress-tests the **minimal congestion score** without over-claiming mechanism closure.

**Why basketball is “Setting 2” in the cross-domain story:** Global selection (draft) vs local opportunity (minutes, roles, teammate quality) is the cleanest measurement lab for Tier 1 objects (\(A\), \(L_Q\), \(L_C\), \(\Lambda\)). Army is the anchor replication; academia is the third replication (preliminary per PEER report).

**Cross-setting manuscript doc (VECTOR + Charles, June 2026):**  
[`1-Various_PDE_and_Chat_stuff/5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf) — committee-facing whole-project summary. Basketball is §1–§2 empirical anchor; §5–§7 generative framing aligns with SCOUT’s June status.

---

## 2. Current status — basketball / SCOUT (high level)

### Established / working

| Layer | Status | Primary artifacts / location |
|-------|--------|------------------------------|
| Panel conductor | ✅ | `sports/530_sports_pipeline.ipynb` → `datasets/mbb/player_season_panel_530.csv` |
| Empirical inverted-U | ✅ | Binned draft rate vs `poolq_loo`; exports under `datasets/mbb/exports_inverted_u_v0/` (e.g. 2026-06-02 run) |
| Wang empirical ladder | ✅ | `sports/538_alex_tier1_model_and_fit.ipynb` — CELLs 4–6 (bins → LPM → logit, \(L^*\)) |
| Pool forensics (PD11 targets) | ✅ | `530` CELLs 5–9 — overlap, mean×SD, draftee-only variants |
| Tier 1 mechanism columns | ✅ | `sports_pipeline/tier1_mechanism_vars.py` — `congestion_quality`, crowding variants |
| Soft generative assignment | ✅ | `sports/tier1_pool_assignment.py` — τ≈0.65 default, Plot A overlap calibration |
| Congestion selection score | ✅ | \(S_i = A_i - w \cdot L_C\) with `crowding_smooth`; `crowding_l_z_scale` for z-scored ability |
| Generative playground UI | ✅ | `sports/538D_development.ipynb` CELL 10; `tier1_cell10_playground_run.py` |
| 539 score preset (partial DGP) | ✅ | Green button / `SELECTION_539_*` in `tier1_sim_config.py` — score + [0,1] scales, not full 539 assignment/noise/threshold |
| Plot B axis toggle | ✅ | `SHOW_PLOT_B_TEAM_MEAN` — `False` = \(L_Q\) LOO (530); `True` = team_mean (539-style) |
| HPC parameter sweeps | ✅ (infrastructure) | `sports/outputs/simulation_sweeps/` — Rivanna/Mac faithful 538 sweep runbooks |

### Major scientific finding (June 2026 — COMPASS must not garble this)

**Same congestion score, different Plot B x-axis → different curve shape.**

| Plot B conditioning | Typical shape with 539 selection preset | Interpretation |
|--------------------|----------------------------------------|----------------|
| **team_mean** (`SHOW_PLOT_B_TEAM_MEAN=True`) | **Inverted-U** (rise, peak, right-tail dip) | Matches **539 notebook** readout (success vs team quality) |
| **\(L_Q\) LOO** (`SHOW_PLOT_B_TEAM_MEAN=False`) | Mostly **decreasing** | Matches **530 empirical axis** question — standouts in weak peer pools selected most |

**Honest claims for manuscript / briefings:**
- ✅ Empirical inverted-U on **real** college rosters vs LOO `poolq_loo` — **replicated** (stylized fact, not mechanism proof).
- ✅ Minimal score **equation** implemented: advancement score ↑ in own ability, ↓ in local congestion.
- ✅ Generative **proof-of-concept**: inverted-U vs **team_mean** under congestion; **not** bin-for-bin match on \(L_Q\) with same top-\(K\) knobs.
- ❌ Do **not** say “538D decomposes 539” or “generative replicates 530 on the same axis without qualification.”

**Authoritative narrative doc:** [`Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md)

### Three-level Wang sequence (oral + manuscript spine)

| Level | Content | SCOUT status |
|-------|---------|--------------|
| **0 — Equation** | \(S_i = A_i - \lambda L_{C,i}\) | Written + coded |
| **1 — 539 bundled POC** | Sort-chop, score noise ε, 90th percentile threshold, plot vs team_mean | `539_alex_model.ipynb` — reference DGP, not architecture parent |
| **2 — 538D modular lab** | Soft assign τ≈0.65, top-\(K\), no score noise on main path, plot axis swappable | **Active development notebook** |

### Not done / open (sports-specific)

| Item | Notes |
|------|-------|
| Generative match to empirical **LOO pool quality** inverted-U | **Deferred** (Charles Path A) — parallel north-star; may need assignment noise, \(B\) term, or selection-rule work |
| **538** empirical CELL 7+ | Robustness (FE, clustering) — placeholder |
| **535** roadmap TODOs | Cleaner CELL 5 regression block; theory language distinguishing `poolq_loo` vs mechanism columns |
| **CELL 4D heterogeneity** | Wired in 538D (`HETEROGENEITY_TOP_TAIL`); **narrative parked** until scaffolding clearer |
| **537** legacy sim | **Frozen** — sort-and-chop; use only for Thread C promotion-score experiments or benchmark overlay |
| **SR / BPM coverage gaps** | Small colleges, 404 slugs — documented in `Pertinent_Thoughts_Scout.md` |
| **Draft matcher 2c** | Human label loop in gameplan still “planned” |
| **Formal master plan** | Deferred until Charles assigns COMPASS |

---

## 3. Notebook and module architecture (SCOUT conductor map)

```text
530_sports_pipeline.ipynb     — DATA: spine → draft match → panel → ventile EDA / LPM
535_sports_tier_1.ipynb     — MECHANICAL EDA: tier1_mechanism_vars, CELL 4 plots (roadmap contract)
538_alex_tier1_model_and_fit.ipynb — EMPIRICAL WANG LADDER + generative CELL 10–12 (Alex spine)
538D_development.ipynb      — PRIMARY June 2026 generative lab (+ 4D heterogeneity)
537_Sports_Simulation.ipynb — FROZEN legacy (sort-and-chop, old Cell 10)
539_alex_model.ipynb        — Bundled generative POC (one-night); reference only for score preset
```

### Importable Python (generative stack — not in `sports_pipeline/` package)

| File | Role |
|------|------|
| `sports/tier1_pool_assignment.py` | `soft_assign`, selection, `crowding_smooth`, scale helpers |
| `sports/tier1_sim_config.py` | Default constants, `SELECTION_539_*`, `SHOW_PLOT_B_TEAM_MEAN` |
| `sports/tier1_cell10_playground_run.py` | ipywidgets UI |
| `sports/tier1_generative_eda.py` | Plot B bin tables + figures |
| `sports/tier1_cell12_generative_eda.py` | Static replay from `tier1_cell10_playground_state.json` |
| `sports/tier1_heterogeneity_ventiles.py` | CELL 4D exports |
| `sports/tier1_539_reference_settings.json` | Reference λ, θ, γ for 539 preset |

### Package layer (`sports_pipeline/` — empirical panel)

| Module | Role |
|--------|------|
| `panel_build.py` | Panel construction, LOO recompute |
| `tier1_mechanism_vars.py` | `congestion_quality`, crowding columns |
| `paths.py` | `panel_530_csv()` → workspace `datasets/mbb/` |

**Workspace root panel path:** `datasets/mbb/player_season_panel_530.csv` (not under `sports/datasets/`).

---

## 4. Key design decisions (basketball-specific)

1. **Realized pools vs generative rules are separate layers** — 538 §6 measures pools the world formed; CELL 10 simulates assignment rules calibrated to 530 forensics (`Tier1_Presorting_Design_Note.md`).

2. **539 vs 538D is parallel, not parent/child** — 539 is a bundled proof-of-concept DGP; 538D is a modular lab anchored to 530 empirics. The **minimal claim** is the **score equation**, not either notebook.

3. **Plot axis is part of the estimand** — Conditioning success on `poolq_loo` (LOO peer quality) vs `team_mean` is not interchangeable; June 2026 finding is a **feature** for distinguishing mechanism tests.

4. **τ calibration** — Assignment temperature τ≈0.65 targets 530 CELL 8 overlap (peak ≫ 1, median roster SD ~0.8 z). Engineering detail for SCOUT; not centerpiece for VECTOR oral brief.

5. **Ability scale + congestion scale** — When ability is z-scored, `crowding_l_z_scale` (p90−p10 of \(A\)) prevents crowding penalty from being negligible in selection.

6. **537 frozen** — Do not extend sort-and-chop for Thread A; red dashed benchmark overlay in Plot A only.

7. **Document-first split** — `SPORTS_DATA_GAMEPLAN.md` = strategic intent; `tier_1_roadmap.md` = 535 execution contract; `Alex_Tier1_Sequential_Model_Outline.md` = advisor spine (5-Manuscript).

---

## 5. Documentation inventory (SCOUT-authored or SCOUT-maintained, updated June 2026)

### `sports/documents/` — primary SCOUT contracts

| Document | Role | Last refreshed |
|----------|------|----------------|
| [`SPORTS_DATA_GAMEPLAN.md`](../sports/documents/SPORTS_DATA_GAMEPLAN.md) | Forward-looking pipeline contract; fast-path ✅; Stage 5 Tier 1/generative | 2026-06-08 |
| [`tier_1_roadmap.md`](../sports/documents/tier_1_roadmap.md) | 535 `df` contract, CELL 0, 538/538D generative block | 2026-06-08 |
| [`Tier1_Presorting_Design_Note.md`](../sports/documents/Tier1_Presorting_Design_Note.md) | PD11 threads A/B/C; 530 calibration targets | 2026-06-08 |
| [`538_Cell10_Generative_Manual.md`](../sports/documents/538_Cell10_Generative_Manual.md) | CELL 10 operator manual | 2026-06-08 |
| [`Pertinent_Thoughts_Scout.md`](../sports/documents/Pertinent_Thoughts_Scout.md) | Scratch discoveries + June generative section | 2026-06-08 |
| [`Alex_model_interpreted.md`](../sports/documents/Alex_model_interpreted.md) | PD12 interpretation; viable-peer signals table | 2026-06-08 |
| [`RIVANNA_RUNBOOK.md`](../sports/documents/RIVANNA_RUNBOOK.md) | HPC workflow | (ops; verify before large sweeps) |
| [`Mac_Faithful_538_Sweep_For_Dummies.md`](../sports/documents/Mac_Faithful_538_Sweep_For_Dummies.md) | Local sweep | |
| [`Rivanna_Faithful_538_Sweep_For_Dummies.md`](../sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md) | Rivanna sweep | |
| [`537_Manual.md`](../sports/documents/537_Manual.md) | Legacy sim only | |
| [`One_Page_Advisor_Brief_Template_College_Replication.md`](../sports/documents/One_Page_Advisor_Brief_Template_College_Replication.md) | Fill-in template (not auto-updated) | |

### `1-Various_PDE_and_Chat_stuff/5-Manuscript/` — SCOUT ↔ VECTOR bridge docs

| Document | Role | Notes |
|----------|------|-------|
| [`Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md) | **Canonical June ground truth** for generative + briefing | Lead doc for VECTOR |
| [`Scout_Modeling_Status_for_Vector_Barabasi_Briefing.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Scout_Modeling_Status_for_Vector_Barabasi_Briefing.md) | May brief | Superseded banner → June doc |
| [`Alex_Tier1_Sequential_Model_Outline.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Alex_Tier1_Sequential_Model_Outline.md) | Advisor-ordered spine §6A/§7/§10 | Updated 2026-06-08 |
| [`Vector_to_Scout_Tier1_Modeling_Direction.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Vector_to_Scout_Tier1_Modeling_Direction.md) | VECTOR→SCOUT sync | June addendum in Final Note |
| [`alex_gates_briefing_structure_outline_v4.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/alex_gates_briefing_structure_outline_v4.md) | 5-minute oral structure | §5 generative status June |
| [`important_stuff.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/important_stuff.md) | Charles scratch anchor lines | |
| [`Tier1_Briefing_Outline.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Tier1_Briefing_Outline.md) | Equations + data map | Theory; not execution contract |
| [`Tier1_Narrative_Outline.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/Tier1_Narrative_Outline.md) | Prose / competing forces | |
| [`tier_1_model.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/tier_1_model.md) | Model layer reference | |

### Cross-domain docs SCOUT reads but does not own

| Document | Agent |
|----------|-------|
| [`talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md`](../talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md) | CODA |
| [`talent/documents/Army_to_College_Basketball_Replication_Handoff.md`](../talent/documents/Army_to_College_Basketball_Replication_Handoff.md) | CODA → SCOUT replication design |
| [`tenure/documents/TENURE_DATA_GAMEPLAN.md`](../tenure/documents/TENURE_DATA_GAMEPLAN.md) | PEER |
| [`PEER_Status_Update_for_VECTOR_2026-06-03.md`](../1-Various_PDE_and_Chat_stuff/5-Manuscript/PEER_Status_Update_for_VECTOR_2026-06-03.md) | PEER |

### Stale / low-priority for COMPASS (unless scope expands)

- `sports/documents/sports_mechanisms/advisor_packet*.md` — older replication packets; may predate 538D.
- `sports/documents/<!-- Generated by SpecStory, Markdown v2.md` — chat export artifact; not a contract.
- Multiple `alex_gates_briefing_structure_outline_v[1-3].md` — superseded by v4 for oral flow.

---

## 6. Sister agents — what SCOUT knows (read their reports; don’t merge pipelines)

| Agent | Report | Maturity vs SCOUT | SCOUT dependency |
|-------|--------|-------------------|------------------|
| **CODA** | [`CODA_report_to_COMPASS.md`](CODA_report_to_COMPASS.md) | **Most mature** empirical + survival stack | Inverted-U **origin**; CIF/competing-risks vocabulary |
| **PEER** | [`PEER_report_to_COMPASS.md`](PEER_report_to_COMPASS.md) | **Preliminary** third setting (stage 9 bins) | Parallel LOO pool logic; tenure vs attrition |
| **VECTOR** | *(pending)* | Manuscript / theory | Consumes SCOUT status docs; does not run notebooks |

**SCOUT does not:** merge Army OER snapshots into basketball panel, or tenure Wayback HTML into 530, or write dissertation chapter prose (VECTOR’s lane).

---

## 7. Harmonization notes for COMPASS (language only — not code merge)

| Concept | Army (CODA) | Basketball (SCOUT) | Academia (PEER) |
|---------|-------------|-------------------|-----------------|
| Pool | Senior-rater cohort | Teammates (team-season) | Dept assistant cohort |
| LOO peer quality | Pool mean minus self | `poolq_loo` | `poolq_loo_mean` |
| Outcome | Promotion / separation | `Y_draft` | `tenure_event` / `attrition` |
| Inverted-U evidence | Established CIF panels | Established ventiles | Preliminary 18-bin stage 9 |
| Generative layer | Less central in CODA report | **Active** (538D CELL 10) | Not SCOUT’s scope |
| Competing risks framing | Native (Cell 11) | Draft yes/no (no time-to-event in ventile EDA) | Cox **planned** (Layer B; Cells 10/10.5/12 — not in `540` yet) |

**Shared mechanism phrase (VECTOR/Dakota):** “Advancement under constrained distinction” — developmental benefits vs competitive constraints; finite distinction capacity in local comparison environments.

**Wang ordering (cross-domain):** (1) stylized fact, (2) minimal mechanism, (3) non-obvious predictions. SCOUT is between (2) and (3) on basketball generative axis.

---

## 8. Prior plan-map work (Cursor artifact — not master plan)

Charles and SCOUT previously mapped the doc ecosystem in [`.cursor/plans/tier1_plan_map_c0d22e58.plan.md`](../.cursor/plans/tier1_plan_map_c0d22e58.plan.md). Key conclusion: **no single master plan file existed** as of June 2026; Dakota v03 RTF is the best **committee-facing whole-project narrative**; `Alex_Tier1_Sequential_Model_Outline.md` is the best **modeling spine** for basketball Tier 1.

COMPASS may absorb that map or supersede it — SCOUT does not treat the `.cursor/plans/` file as canonical repo documentation.

---

## 9. Clarifying questions for Charles — COMPASS update (2026-06-11)

**COMPASS assigned.** Charles locked several items; SCOUT still needs answers on open rows.

### A. COMPASS process — resolved

| # | Topic | Status |
|---|--------|--------|
| 1–2 | Single COMPASS agent; near-term = core manuscript | **Done** — `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` |
| 3 | Deadline | **Summer–Fall 2026** draft/submission |
| 4 | VECTOR handoff | COMPASS reads `5-Manuscript/` + agent reports |

### B. Basketball generative priorities

5. **Resolved — manuscript-first (e):** exports + axis table + nesting chain; LOO generative match **deferred**. Detail: `20260611_1626_COMPASS_to_SCOUT_model_coherence_questions.md`.
6. Should COMPASS treat **539** as deprecated, reference-only, or still active for Alex demos?
7. Is **team_mean** vs **\(L_Q\)** axis choice a **manuscript figure requirement** (show both) or internal lab detail?

### C. Empirical basketball
8. Is **`535`** still an active notebook path, or is all Tier 1 empirical work consolidating in **538/538D**?
9. **`PERF_METRIC` lock:** Is PPM+z within-season still the canonical spec for cross-domain comparability, or should BPM/OBPM become primary before master plan freezes?

### D. Cross-agent coordination
10. Should PEER adopt SCOUT’s **generative modular stack** for academia simulation (future), or keep PEER empirical-only until tenure Cox results land?
11. Does CODA’s **competing-risks** framing need a basketball analog (e.g. draft vs undrafted vs early exit) in the master plan, or is ventile draft-rate sufficient for Setting 2?

### E. VECTOR / manuscript
12. Who **owns** updating Dakota RTF when PEER/CODA/SCOUT status shifts — VECTOR, Charles, or implementation agents?
13. Should the master plan index **`advancement_under_constrained_distinction_dakota_feedback_v03.rtf`** as the external-facing spine, with internal gameplans as appendices?

---

## 10. Suggested first tasks for COMPASS

*Several items below are **done** or **in progress** (2026-06-11).*

1. Read four agent reports + Dakota RTF + `Alex_Tier1_Sequential_Model_Outline.md`.
2. Produce a **one-page index** doc in `3-Master_Plan/` linking: gameplans, status updates, primary notebooks, canonical outcomes per setting.
3. Lock **claim language** table (what each setting can say in manuscript v1).
4. Sequence remaining work: SCOUT nesting deliverables (blocking prose) vs PEER Cox (parallel) vs CODA TB-stratify (deferred unless elevated).
5. Assign **single owner** per cross-cutting doc (who refreshes Dakota, Alex spine, gameplans).
6. **Do not** merge `talent_pipeline/`, `sports_pipeline/`, and `tenure_pipeline/` codebases — harmonize at **estimand + narrative** layer only unless Charles explicitly requests shared Python abstractions.

---

## 11. Agent identity note

**SCOUT** in Charles’s naming = Cursor agent focused on `./sports/`, college basketball data, Tier 1 generative modules, and SCOUT-authored status docs in `5-Manuscript/`. SCOUT implements, documents, and stress-tests; **VECTOR** drafts manuscript prose; **Alex Gates** sets sequencing; **Charles** owns scientific claims and committee communication.

If a future Cursor session is labeled “SCOUT,” it should read this report + `Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md` before changing generative defaults or briefing language.

---

*SCOUT handoff report ends. COMPASS active — see `20260611_1626_COMPASS_to_SCOUT_model_coherence_questions.md` and `20260611_1626_COMPASS_to_SCOUT_questions.md`.*
