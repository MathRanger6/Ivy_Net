# COMPASS → Charles: PD12 reassessment (answers to `1155`)

**Date:** 2026-06-15 11:56  
**From:** COMPASS  
**To:** Charles (+ CODA, SCOUT, PEER, VECTOR)  
**In reply to:** [`20260615_1155_Charles_to_COMPASS.md`](20260615_1155_Charles_to_COMPASS.md)  
**Sources reviewed:** [`20260520_Transcript_12_guidance.md`](../sports/documents/20260520_Transcript_12_guidance.md) (PD12), [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md), [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md), [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md), agent STANDING BY files, [`forward_plan_background.md`](forward_plan_background.md).

**Constraint honored:** No new workstreams, no scope expansion, no reopening Path II or settled agent consensus.

---

## Executive answer

**The current plan is directionally correct but under-labeled.** Recent forward-plan prose compresses Alex’s ladder to **Phenomenon → Minimal model → Paper**, which makes the work look like “fit a curve and write.” PD12 (May 20) adds an explicit middle rung: **the model should organize inquiry by proposing measurable quantities and testable predictions** — not only reproduce the stylized fact on one axis.

**The fix is framing and sequencing in planning docs, not a new research program.** Most PD12 Priority 3 content is **already in the repo** (crowding/congestion in SCOUT, near-threshold 4D, quality vs congestion split). Priority 1 (three-domain parametric identifiability) and Priority 4 (fourth-domain falsification) remain **correctly deferred** for v1 — but COMPASS should name that deferral explicitly when you talk to Alex so it reads as discipline, not drift.

---

## Question 1 — Does the current plan reflect Alex’s intended scientific progression?

### Verdict: **Mostly yes; one emphasis gap**

| Alex progression (PD12) | Current plan | Alignment |
|------------------------|--------------|-----------|
| Phenomenon (inverted-U on LOO proxy) | Locked triad; tenure preliminary | ✅ |
| Minimal model organizes inquiry | Path II generative POC + axis honesty | ✅ |
| Model suggests **new measurements** | **Under-stated** in forward plan | ⚠️ **Gap** |
| Predictions (Wang move) | #1 near-threshold, #2 Λ | ✅ |
| Parameter identifiability / fit (3 domains) | **Deferred** | ✅ for v1; ⚠️ vs full PD12 P1 |
| Falsification / negative cases | **Deferred** | ✅ for v1 |

### Where it diverges (wording, not science)

1. **Forward plan center of gravity** ([`1045`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md) §3, [`forward_plan_background`](forward_plan_background.md) §154) reads as **execution toward manuscript** immediately after minimal model packaging. Alex’s PD12 adds **model-guided empirical features** as a named step *between* mechanism and “paper done.”

2. **Congestion vs quality** is implemented in basketball (`crowding_smooth`, `poolq_loo` split per PD12 guidance doc §Priority 3) but the **locked consensus paragraph** does not foreground “congestion as first-class construct” the way PD12 does.

3. **Priority 1 (fit 5–6 parameters in all three domains)** is absent from v1 — intentionally parked. That is the **largest** gap versus Alex’s full four-priority list, but expanding it now would **violate** your constraint and the correspondence experiment’s stop rule.

### Recommended adjustment (material, not expansion)

Re-label the locked ladder in all planning docs as:

```text
Phenomenon (Rung 1)
    ↓
Minimal mechanism (Rung 2 — Path II POC)
    ↓
Model-guided empirical features (Rung 2.5 — existing artifacts, explicit in prose)
    ↓
Predictions (Rung 3)
    ↓
Manuscript (Rung 4)
```

**No new cells required for v1** if Rung 2.5 is satisfied by artifacts already on disk or in D10.

---

## Question 2 — Is “minimal model closure” consistent with Alex’s guidance?

### Verdict: **Upgrade the definition one notch — do not replace it**

**Not sufficient for PD12-aligned closure:**

```text
Model reproduces phenomenon (qualitatively on pool-mean axis)
```

**Current SCOUT closure** ([`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md)) is **closer to the right standard** but should be **named explicitly**:

### COMPASS recommended closure standard (v1 manuscript)

```text
(1) Phenomenon anchored empirically (LOO inverted-U; honest maturity labels)
(2) Minimal mechanism demonstrated:
      talent-only fails + congestion-in-score bends curves (Path II POC)
(3) At least one model-guided measurable quantity exported or cited:
      e.g. crowding_smooth / viable-peer congestion vs poolq_loo (quality)
(4) At least one prediction-facing readout tied to mechanism:
      e.g. near-threshold heterogeneity (4D); Λ hook prose (#2)
(5) Honest limitation prose (axis mismatch; tenure preliminary; no causal claims)
```

Items (3)–(4) are **already yellow/green** in SCOUT checklist **C6**; the reassessment is to treat them as **closure criteria**, not “nice supplement.”

**Explicitly not required for v1 closure (PD12 P1 / P4 parked):**

- Parametric recovery of all generative knobs in MBB + tenure + Army  
- Fourth-domain falsification (NHL, etc.)  
- Full B(Q)−D(Q) generative decomposition in prose as if estimated  

---

## Question 3 — Explicit “Model-Guided Empirical Features” stage?

### Verdict: **Yes — as a named stage; mostly **existing work**, not a new phase**

### Where it sits

```text
Minimal model complete enough (D10 bundle + score one-pager)
        ↓
Model-guided empirical features  ← NAME THIS STAGE
        ↓
Predictions (§4 manuscript)
        ↓
Draft / Alex meeting
```

**Parallel with manuscript drafting:** VECTOR can draft §3 mechanism while SCOUT finishes D10; **§4 predictions** should cite model-guided features explicitly.

### What counts as model-guided features (v1 — no new workstreams)

| Domain | Feature(s) | Status | Agent |
|--------|------------|--------|-------|
| **Basketball** | **Quality** `poolq_loo` vs **congestion** `crowding_smooth` / viable-peer density | Implemented; export in **D10** | SCOUT |
| **Basketball** | Near-threshold heterogeneity (4D ventiles) | On disk | SCOUT |
| **Army** | Pool minus mean (quality leg); pool size / slot scarcity as Λ hook | Empirical; Λ prose CODA-led | CODA |
| **Tenure** | `poolq_loo_mean` (quality); **`pool_size_oa_loo`** as congestion proxy | **On panel** — under-used in stage 9 | PEER |

**PEER note (no new scrape):** Stage 9 uses quality only. A **single** supplementary read — tenure rate vs `pool_size_oa_loo` bins or quality×pool-size interaction — would align tenure with PD12 “congestion vs quality” without Layer B Cox. **Optional**; route only if Charles wants tenure on the model-guided features slide for Alex.

### What does **not** belong in this stage for v1

- New OpenAlex bulk pass  
- Tenure generative sim  
- 539 full identifiability sweeps  
- NHL negative case  

---

## Question 4 — Shortest path to publishable manuscript (PD12-faithful)

**Scope:** Manuscript only — not dissertation completion.

### Shortest faithful path (sequenced)

| Step | Action | PD12 alignment | Owner |
|------|--------|----------------|-------|
| **1** | Charles Tier 1 locks (unchanged) | Unblock execution | Charles |
| **2** | SCOUT **D10** bundle: talent-only fail, congestion POC, **axis table** (quality vs congestion rows), score one-pager | P2 partial + **P3 primary** | SCOUT |
| **3** | Name **model-guided features** in VECTOR outline: §3.2–3.3 (MBB); cross-ref Army pool-minus-mean; tenure quality + optional pool-size | **P3 explicit** | VECTOR |
| **4** | §4 predictions: **#1** near-threshold (4D figure); **#2** Λ stub (CODA prose, conceptual) | Wang move | VECTOR |
| **5** | PEER inference CSV (C1–C2); tenure §1 figure + limitations | Rung 1 leg honest | PEER |
| **6** | Draft §2–§5 under claim table §F | Paper | VECTOR |
| **7** | Alex meeting: present **ladder above**; confirm TB-stratify defer + estimand sign-off | Manage P1/P4 deferral explicitly | Charles |

**Critical honesty for Alex:** v1 delivers **Priority 3 (congestion/features) + partial Priority 2 (kill switches via talent-only fail)**. **Priority 1 (3-domain fit)** and **Priority 4 (falsification)** are **post-v1 or dissertation chapters** — say that out loud.

**Do not add** before submission: 539 parametric fit across three domains, tenure Layer B Cox (unless you elevate), NHL hunt.

---

## Question 5 — Document revisions?

### Verdict: **Yes — targeted edits only**

| Document | Revision |
|----------|----------|
| [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md) | Insert **Phase B.0: Model-guided empirical features (Rung 2.5)** between D10 and §4 predictions; add PD12 one-paragraph alignment footnote |
| [`forward_plan_background.md`](forward_plan_background.md) | Update center-of-gravity diagram (§154) to 5-rung ladder; add PD12 “what we deferred vs what we deliver” box |
| [`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`](PROJECT_STATUS_AND_NEAR_TERM_PLAN.md) | Add one row: PD12 alignment — P3 in v1, P1/P4 deferred |
| [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) | **Clarify C6** header: “model-guided measurable + prediction” = closure, not optional |
| [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) | Add 1–2 rows: congestion vs quality distinction **supported with caveat**; 3-domain parametric identifiability **defer** |
| [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md) | Add talking point: v1 = mechanism + **model-suggested features** + predictions; identifiability/falsification timeline |
| **Do not revise** | Path II lock, claim-table core, agent STANDING BY files, `COMPASS_Initial_Guidance_v6` (archive) |

COMPASS will apply the **`1045` + `forward_plan_background` + `PROJECT_STATUS`** edits in a follow-up commit when you say **go** — not preemptively unless you want them now.

---

## Agent inputs incorporated (Round 5 read receipts)

| Agent | File | COMPASS use |
|-------|------|-------------|
| **PEER** | [`20260615_1156_PEER_read_receipt_Charles_to_COMPASS.md`](20260615_1156_PEER_read_receipt_Charles_to_COMPASS.md) | Tenure Rung 2.5: pool_size columns; no new scrape |
| **SCOUT** | *(pending Round 5)* | crowding_smooth + 4D = P3 delivery |
| **CODA** | *(pending Round 5)* | Λ / pool-size as Army feature hooks |
| **VECTOR** | Co-requester via Charles | Manuscript ladder emphasis |

---

## One paragraph for you (Alex prep)

> We are not walking back Path II or the correspondence consensus. The v1 manuscript will show an empirical inverted-U on LOO peer quality across three settings, a minimal generative proof that talent-only selection fails and congestion in the score can bend curves, **explicit model-guided measurements** (quality vs congestion in basketball; pool structure in Army and tenure where data already exist), and two prediction-facing readouts — near-threshold heterogeneity and a global-capacity Λ hook. Full parametric identifiability across all three domains and a formal negative fourth setting are **planned next**, not blockers for the first complete draft.

---

## Charles decisions (minimal — not reopening Tier 1)

| ID | Question | COMPASS rec. |
|----|----------|--------------|
| **PD12-A** | Accept **5-rung ladder** relabel in planning docs? | **Yes** |
| **PD12-B** | Upgrade closure definition to include (3) measurable + (4) prediction? | **Yes** |
| **PD12-C** | Optional PEER **pool_size** feature read for tenure (no new data)? | **Your call** — strengthens P3 slide; ~0.5–1 PEER session |
| **PD12-D** | Tell Alex P1/P4 deferred explicitly at next meeting? | **Yes** |

Tier 1 execution locks (D10, C1–C2, V1–V3) **unchanged**.

---

*End COMPASS PD12 reassessment.*
