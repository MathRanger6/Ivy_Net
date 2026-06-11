# COMPASS Initial Review and Alignment Memo

> **Name note:** Authored by **COMPASS** (agent renamed 2026-06-11; formerly “Master Planner”). See [COMPASS_AGENT_IDENTITY.md](COMPASS_AGENT_IDENTITY.md).

**Date:** 2026-06-11  
**Author:** COMPASS (Cursor agent)  
**Purpose:** Structured situational review after ingesting v6 guidance (VECTOR handoff), three domain agent reports, theory/manuscript corpus, dissertation proposal, Dakota v03 brief, and advisor memos.  
**Status:** Near-term plan **largely locked** after Charles clarifications (2026-06-11). Advisor update: [20260611_Brief_for_Alex_Gates_brief.md](20260611_Brief_for_Alex_Gates_brief.md) / [full](20260611_Brief_for_Alex_Gates_full.md).

---

## 1. Executive synthesis

Charles Levine's dissertation program has **morphed substantially** since the August 2024 proposal (*Deciphering the Talent Mosaic* — prestige networks, unit eigenvector centrality, three Army-only chapters) while retaining core DNA: **Army officer careers as a closed talent system**, **peer and evaluator context matter**, **network-science and survival methods**, and **Barabási-style cross-domain universality ambition**.

The **current scientific center of gravity** (June 2026) is narrower and more defensible:

> **Advancement under constrained distinction** — individuals compete in **local comparison pools** while **global distinction is finite**. Empirically, **advancement probability rises with LOO peer-pool quality through the middle of the distribution, then falls at the elite tier** (inverted-U). This pattern is **established in Army**, **replicated in NCAA basketball → NBA draft**, and **preliminary in R1 CS tenure**.

The project is transitioning from **empirical discovery** to **explanatory modeling** (Wang-style: stylized fact → minimal mechanism → non-obvious predictions). The **immediate convergence risk** is not lack of ideas — it is **parallel expansion** (525/UIC, network extensions, generative axis mismatches, tenure scrape expansion) displacing **minimal model closure**, **prediction list discipline**, and **manuscript draft**.

**VECTOR's handoff** is operationalized through [COMPASS_Initial_Guidance_v6.md](COMPASS_Initial_Guidance_v6.md) plus the theory corpus (`Vector_Master_Theory_and_Modeling_Notes_4.md`, `Tier1_Narrative_Outline.md`, Dakota v03 RTF, Wang model notes). There is no separate `VECTOR_report_to_COMPASS.md`; v6 + 5-Manuscript folder **is** the VECTOR lane per Charles.

---

## 2. Established vs preliminary — findings by domain

| Setting | Agent | Outcome | Pool construct | Inverted-U | Cox / survival | Manuscript-ready? |
|---------|-------|---------|----------------|------------|----------------|-------------------|
| **1 — Army** | CODA | CPT→MAJ promotion vs attrition | Senior-rater LOO pool TB (`pool minus mean`) | **Established** — CIF Q-bins + Cox quadratics | **Yes** — Cell 11 CIF + Cell 12 cause-specific Cox | **Strongest** — figures + HR tables exist; estimand language needs care |
| **2 — Basketball** | SCOUT | NBA draft (`Y_draft`) | LOO teammate `poolq_loo` | **Replicated** — ventile/binned draft rate | **Partial** — Wang ladder (bins→LPM→logit); not time-to-event CR | **Strong empirical**; generative claims must be qualified |
| **3 — Academia** | PEER | Tenure (Asst→Assoc) vs attrition | LOO dept `poolq_loo_mean` | **Preliminary** — stage 9, 18 bins, elite bin dip | **📋 Planned (Layer B)** — `540` ends at Cell 9; port `520` → Cells 10/10.5/12 | **Preliminary figure + honest limitations** only |

### Confidence tags (COMPASS)

- **High confidence:** Army and basketball show the same *qualitative* inverted-U on LOO peer-quality axes (descriptive / binned / CIF layers).
- **Medium confidence:** Cox quadratic + interaction terms in Army support curvature on hazard scale; basketball LPM/logit yields turning point \(L^*\).
- **Low–medium confidence:** Tenure stage-9 pattern (small N per bin, ~58% censoring, noisy OpenAlex linkage, unconditional bins).
- **Not yet supported:** Claim that **one minimal generative score** reproduces empirical inverted-U on **\(L_Q\) LOO axis** in simulation (SCOUT June finding: inverted-U on `team_mean`, mostly decreasing on \(L_Q\)).

---

## 3. Theory / minimal model state (VECTOR framing)

### Working thesis (cross-domain)

From `Vector_Master_Theory_and_Modeling_Notes_4.md` and `Tier1_Narrative_Outline.md`:

> Advancement depends on the interaction between **local peer quality** and **scarce distinction**. Stronger pools improve development/signaling up to a point; at the elite tier, **congestion, signal compression, and finite slots** dominate → inverted-U.

### Tier 1 minimal objects

| Object | Meaning | Empirical proxy (basketball) |
|--------|---------|------------------------------|
| \(Y\) | Global advancement (distinction received) | `Y_draft` |
| \(L_{ijt}\) | Amalgamated local environment | Rolled into \(Q\) first |
| \(Q_{ijt}\) | LOO peer quality | `poolq_loo` |
| \(\Lambda_t\) | Global distinction capacity | Draft slots / promotion boards / tenure lines |
| \(A_{ijt}\) | Own ability (control, not headline) | PPM z |

**Minimal generative score (Alex / SCOUT):**

\[
S_i = A_i - \lambda \cdot L_{C,i}
\]

where \(L_C\) = LOO viable-peer congestion. This is the **domain-agnostic minimal claim** — not the 539 notebook bundle.

### Theory vs model discipline (Alex, Apr 30 2026)

`2026_0430_Paper7_feedback.md` and `2026_0507_Alex_Gates_Post_Meeting_Simulation_Memo.md` sharpen:

- **Theory** may include development, evaluator compression, sorting, prestige, networks.
- **Minimal model** should formalize the **smallest** set that reproduces the nonlinear pattern.
- **Quadratic in \(Q\)** is an **empirical diagnostic**, not the generative first principle.
- **Assortative pool formation + local comparison** is the generative story Alex emphasized (PD10–PD12).

### Gaps vs empirical evidence

| Gap | Severity | Notes |
|-----|----------|-------|
| Generative inverted-U on **same axis** as 530 (`poolq_loo`) | **High** | Same score, different Plot B axis → different shape (June 2026) |
| PEER Layer B Cox not archived | **Medium for draft / High for submission** | **Soft gate:** CELL 9 + limitations OK for VECTOR draft now; basic Cell 12 before submission; not urgent during draft phase (Charles 2026-06-11) |
| Mechanism decomposition (B vs D) not separately identified | **Medium** | Tier 1 intentionally rolled-up; predictions list underdeveloped |
| Evans structural misclassification integrated in theory, not in minimal sim | **Medium** | Manuscript optional for v1 |
| Network-science extensions (exposure vs comparison nets) | **Low for v1** | Dakota §8 + Barabási brief — explicitly defer |

---

## 4. Cross-agent tensions and over-claim risks

### 4.1 Estimand conflation (highest manuscript risk)

| Tension | Agents involved | Planner ruling |
|---------|-----------------|----------------|
| **CIF bar panels vs Cox HRs** | CODA | Keep layers distinct in prose; CIF = binned cumulative incidence; Cox = cause-specific hazards with censoring at competing event |
| **Cell 11 CIF estimator simplicity** | CODA | Do not claim full Aalen–Johansen; last-snapshot bin assignment is implementation fact |
| **Plot B axis: `team_mean` vs \(L_Q\)** | SCOUT / VECTOR | **Not interchangeable**; empirical paper leads with \(L_Q\); generative POC may use team_mean — must say so explicitly |
| **539 vs 538D relationship** | SCOUT | Parallel bundles, not parent/child; minimal claim = **equation**, not notebook |
| **Fine–Gray mentioned in Dakota/PEER** | PEER / VECTOR | Code uses cause-specific Cox + empirical CIF; verify before manuscript claims Fine–Gray |
| **"168 schools" inference-ready** | PEER | 168 `uni_slug` ≠ 168 equal-quality departments; distinguish coverage vs inference sample |

### 4.2 Duplicated effort

| Duplication | Recommendation |
|-------------|----------------|
| Multiple Alex briefing outlines (v1–v4) | **Canonical:** `alex_gates_briefing_structure_outline_v4.md` |
| Multiple Scout status docs | **Canonical:** `Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md` |
| `Vector_to_Scout_Tier1_Modeling_Direction.md` vs Alex spine | **Not sole canonical** per CODA Q11; use Alex spine + June Scout status |
| 535 vs 538 empirical paths | Consolidate on **538/538D** unless Charles revives 535 |
| 537 generative sim | **Frozen** — benchmark only |

### 4.3 Hidden assumptions carrying weight

1. **LOO peer quality as sufficient statistic for local environment** — rolls development + congestion into one proxy (Tier 1 design choice).
2. **Three settings in one manuscript** — Charles confirmed 2026-06-08 (CODA report §10); dissertation bar = all three.
3. **Army proprietary data** — basketball/tenure are public-facing legs; Army figures may be illustrative without micro-data release.
4. **PPM+z as cross-domain performance harmonizer** — SCOUT still flags BPM/OBPM as open.
5. **Transcripts folder** — referenced in v6 but **not present in repo workspace**; advisor signal absorbed via memos (`2026_0507`, `2026_0430`, `Alex_Tier1_Sequential_Model_Outline`, `TENURE_DATA_GAMEPLAN` § advisor).

### 4.4 Sequencing tensions — resolved vs open

| # | Issue | Status (2026-06-11) |
|---|-------|---------------------|
| 1 | **Cell 12 Cox on tenure** before Setting 3 prose | **Resolved — soft gate:** CELL 9 + limitations OK for VECTOR draft now; **Cell 12 not urgent during draft**; basic Cox before submission; Fine–Gray deferred |
| 2 | **SCOUT generative priority** | **Resolved — manuscript-first (Path A / Path II):** honest layering + axis table; LOO generative match **deferred**; nesting prose blocking |
| 3 | **CODA parallel track** (525/TB-stratify vs pool audit vs manuscript) | **Open** — Charles has not ranked; default **defer** per near-term plan |
| 4 | **OpenAlex confidence filter** for tenure inference sample | **Open** — HIGH only vs HIGH+MEDIUM vs MULTI with disclaimer |

---

## 5. Advisor alignment sketch (Alex Gates — preliminary)

Full `MENTAL_MODEL_OF_ALEX.md` deferred to Phase 1 embed in near-term plan; preliminary read:

### What problem Alex believes we are solving

> Show that **nonlinear advancement** emerges when **talent sorts into local pools** and **selection uses local comparison**, not raw ability alone — with a **minimal generative story**, not a quadratic baked in.

### What evidence would convince Alex

- Cross-domain **empirical replication** (done for 2.5/3 settings).
- **Generative check**: ability-only fails; adding congestion/local comparison bends the curve.
- **Honest axis/estimand language** — no over-claim that one notebook "decomposes" another.
- **Wang ladder**: bins → transparent quadratic **as diagnostic** → logit \(L^*\) → generative mechanism.

### What Alex would likely cut

- Network-science extensions before minimal model + predictions.
- Copying observed team means into generative assignment as "the model."
- Presenting quadratic as **the** mechanism.
- Chasing perfect tenure scrape before end-to-end measurement on existing data.

### What Alex would likely prioritize

- **PD11 threads**: (C) promotion score vs local rank tweaks → (A) soft-assignment pool formation → (B) mean × dispersion EDA.
- **End-to-end curves** with sample-loss accounting (PEER delivered this ethos).
- **Non-obvious predictions** (heterogeneity in draft-relevant tail; threshold congestion).

### Risks Alex appears focused on

- Methodological overreach (causal claims, Fine–Gray without implementation).
- Generative/empirical axis mismatch presented as replication.
- Distraction from **paper** by 525 coding or URL scraping.

**Laszlo Barabási** (strategic): empirical replication + minimal mechanism + network-science **future** hooks (`barabasi_briefing_outline_v2.md`). Lead with stylized fact, not closed proof.

---

## 6. Dissertation evolution — original vs current

| Dimension | Aug 2024 proposal | June 2026 program |
|-----------|-------------------|-------------------|
| Title/framing | Talent mosaic, unit prestige, OCN eigenvector centrality | Advancement under constrained distinction |
| Domains | Army only (3 chapters) | Army + basketball + academia |
| Core RQs | Prestige units, peer effects, TB tradeoffs | Inverted-U + minimal mechanism + predictions |
| Methods | OCN/OPN networks, survival | Survival + LOO pool metrics + Tier 1 generative lab |
| Committee | Barabási chair, Gates, Vespignani, Dakota Murray | Same; Dakota received v03 brief |

**Retained:** Army as anchor; Evans misclassification; competing risks; people-analytics audience; Wang/Barabási scientific style.

**Deprioritized for immediate manuscript:** Full OCN prestige validation (H1a–c), 525 UIC consistency as *paper* centerpiece (still valuable for Army depth / dissertation later).

---

## 7. Charles decisions (locked) and remaining open questions

### Locked (COMPASS thread, 2026-06-11)

| # | Topic | Decision |
|---|--------|----------|
| 1 | Hard deadline | **Summer–Fall 2026** core manuscript draft/submission |
| 2 | Tenure Cox gate | **Soft gate** — see §4.4 #1 |
| 3 | SCOUT generative priority | **Manuscript-first** — see §4.4 #2 |
| — | Terminology | **LOO** in any name for quantities excluding self |
| — | Alex comms | Plan update briefs (`*_Brief_for_Alex_Gates_*.md`) — Charles's calls, not a decision questionnaire |

### Still open

4. **CODA parallel track** (§4.4 #3) — TB-stratify on AWS? pool-size audit before manuscript?
5. **Transcripts location** — `transcripts/*_Paper_directions*` not in workspace; memos sufficient?
6. Army data in planning docs — what can be named externally?
7. Stale file flags — any v6 paths superseded beyond agent reports?
8. Who owns Dakota RTF refresh when domain status shifts?
9. `PERF_METRIC` lock (PPM+z) vs BPM for cross-domain comparability?
10. **OpenAlex confidence policy** for tenure (§4.4 #4).

---

## 8. Draft agent question queue

| File | Rationale |
|------|-----------|
| `20260611_0826_COMPASS_to_VECTOR_questions.md` | Minimal model closure criteria; prediction prioritization; manuscript section ownership |
| `20260611_0826_COMPASS_to_SCOUT_questions.md` | Generative \(L_Q\) gap vs manuscript scope; axis figure requirements |
| `20260611_0826_COMPASS_to_PEER_questions.md` | Setting 3 maturity target; Cox timeline; inference sample definition |
| `20260611_0826_COMPASS_to_CODA_questions.md` | Army estimand language for manuscript; deferred TB-stratify / pool audit |

Charles routes these to agents; COMPASS will not assume answers.

---

## 9. Provisional answer — shortest defensible path

> If the objective is to complete the minimal model, generate robust predictions, and produce a publishable manuscript, what is the most scientifically defensible path from today?

**Locked path (Charles, 2026-06-11):**

```text
LOCK CLAIM LANGUAGE (all agents)
    ↓
SCOUT: Manuscript exports + axis table + nesting chain for VECTOR §3
       (defer LOO generative bin-for-bin match; parallel north-star sprint if time)
    ↓
VECTOR: Draft Wang-structure manuscript — empirical triad → minimal model → predictions
    ↓
PEER: Layer B Cell 12 Cox before submission only (not urgent during draft; CELL 9 OK for VECTOR now)
    ↓
CODA: Manuscript figures + estimand-checked captions; 525/TB-stratify deferred
    ↓
PREDICTIONS: Lock 2 testable (heterogeneity + one dispersion/stratification candidate)
    ↓
SUBMIT Summer–Fall 2026; defer networks, Fine–Gray, full LOO generative match
```

Detail: `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` and `20260611_Brief_for_Alex_Gates_full.md`.

---

## 10. Review status

- **§§1–4 situational understanding:** Charles affirmed via clarification thread (2026-06-11).
- **§9 path:** Locked for near-term; open items in §7.4–10 remain.
- **`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`:** Active living doc; revise when agent answers land.
- **Alex:** `20260611_Brief_for_Alex_Gates_brief.md` / `_full.md` — plan update (Charles's calls), not a decision memo.

*End initial review memo.*
