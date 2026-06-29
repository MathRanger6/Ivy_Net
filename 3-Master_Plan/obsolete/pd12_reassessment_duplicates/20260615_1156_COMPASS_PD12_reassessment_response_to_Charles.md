# COMPASS → Charles: PD12 reassessment (Q1–Q5)

**Date:** 2026-06-15 11:56  
**From:** COMPASS  
**To:** Charles Levine (cc: CODA, SCOUT, PEER, VECTOR)  
**In reply to:** [`20260615_1155_Charles_to_COMPASS.md`](20260615_1155_Charles_to_COMPASS.md)

**Materials reviewed:** PD12 transcript guidance ([`sports/documents/20260520_Transcript_12_guidance.md`](../sports/documents/20260520_Transcript_12_guidance.md), [`Alex_model_interpreted.md`](../sports/documents/Alex_model_interpreted.md) § PD12), [`forward_plan_background.md`](forward_plan_background.md), [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md), SCOUT closure [`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md), VECTOR claim table [`1100`](20260615_1100_VECTOR_claim_language_table.md), Rounds 1–5 STANDING BY files.

**Constraint honored:** No scope expansion, no new workstreams, Path II and agent consensus **not** relitigated — **sequencing and language** adjusted only.

---

## Executive answer

Charles’s PD12 reread is **correct**: recent planning **compressed** Alex’s ladder toward **Phenomenon → Minimal model → Paper**, with predictions **named** but **model-guided empirical features** (Priority 3) **under-labeled** in forward docs.

The fix is **not** to reopen identifiability (PD12 Priority 1), extreme-event sweeps beyond talent-only fail (Priority 2), or falsification domains (Priority 4). The fix is to **make explicit** what SCOUT already built — **quality vs congestion**, **crowding / viable-peer density**, **near-threshold heterogeneity** — as a **named stage** between minimal model and manuscript, and to **tighten the closure definition** one notch toward Alex’s standard **without adding tasks**.

---

## Question 1 — Does the current plan reflect Alex’s intended scientific progression?

### Verdict: **Mostly yes on substance; modest drift on sequencing emphasis**

| Alex progression (PD12 spirit) | Current plan (June 2026) | Alignment |
|--------------------------------|--------------------------|-----------|
| Phenomenon (inverted-U, three settings) | Locked triad; tenure preliminary | ✅ |
| Minimal model organizes inquiry | Path II; Alex score; soft assignment | ✅ |
| Model suggests **new measurements** | **Implemented in repo** (`crowding_smooth`, viable-peer logic, 4D heterogeneity) but **not named as a plan stage** | ⚠️ **Under-labeled** |
| Model generates predictions | #1 near-threshold, #2 Λ peak-shift locked | ✅ (#2 prose-heavy) |
| Parameter identifiability / 3-domain fit | Explicitly **deferred** | ✅ intentional deferral |
| Falsification / 4th domain | **Deferred** | ✅ intentional deferral |

### Where the plan diverges (wording / emphasis, not science)

1. **Forward plan Phases A–B** read as: unlock D10 → draft paper. That optimizes **packaging velocity**, not Alex’s **“theory proposes new measurements”** sentence ([`20260520_Transcript_12_guidance.md`](../sports/documents/20260520_Transcript_12_guidance.md) Priority 3).

2. **`forward_plan_background.md` § center of gravity** shows:
   ```text
   Phenomenon → Minimal model → Prediction → Paper
   ```
   PD12’s richer ladder is closer to:
   ```text
   Phenomenon → Minimal model → Model-guided features → Predictions → Paper
   ```

3. **Congestion** is first-class in **SCOUT code and PD12 docs** but **second-class in planner prose** (“manuscript convenience” risk Charles flagged).

### What to adjust (material changes only)

| Change | Type |
|--------|------|
| Rename / insert **Phase B′: Model-guided empirical features (export + prose)** before “full manuscript draft” | **Planning language** |
| Require D10 bundle to include **congestion/crowding readouts** + **4D heterogeneity** artifacts explicitly (not only generative contrast PNGs) | **SCOUT D10 spec** (packaging, not new science) |
| VECTOR §3–§4 must use PD12 **quality vs congestion** paragraph ([`20260520_Transcript_12_guidance.md`](../sports/documents/20260520_Transcript_12_guidance.md) § one-paragraph sentence) | **Prose discipline** |
| Alex meeting agenda: show **progression ladder**, not only “ready to draft” | **Communication** |

**Do not adjust:** Path II, LOO generative deferral, identifiability sweeps, NHL negative case, tenure Layer B timing, Army CR sophistication.

---

## Question 2 — Definition of “minimal model closure”

### Verdict: Adopt **Option B-lite** — do not revert to Option A

| Option | Standard | COMPASS recommendation |
|--------|----------|------------------------|
| **A** | Model reproduces phenomenon | **Too weak** for PD12 — Alex wants inquiry organized, not curve replay |
| **B (full)** | Phenomenon + measurable quantity + prediction + identifiability | **Too strong for v1** — pulls in PD12 Priority 1 |
| **B-lite (recommended)** | Phenomenon **+ model-motivated empirical quantity exported + ≥1 prediction with empirical readout** | **Matches Alex Priority 3 + locked predictions without new work** |

### Recommended closure definition (replace SCOUT §7 one-liner in planning docs only)

> **Minimal model closure (v1, PD12-aligned):** (1) Generative score POC shows **talent-only fails** and **congestion-in-score** produces qualitative peak-and-decline on the documented axis; (2) at least **one model-guided empirical feature** is **exported** for the manuscript (e.g. **team quality** $\bar{a}_t$ vs **viable-peer congestion** $C_{i,t}$ / `crowding_smooth`, with axis table); (3) at least **one prediction** has an **empirical readout on disk** (near-threshold heterogeneity — SCOUT 4D); (4) **honest limitation** that LOO generative bin-for-bin match and full parameter identifiability are **out of scope for v1**.

This is **consistent** with existing SCOUT checklist C1–C7; it **elevates C6** from “yellow partial” to **required narrative link** between model and **measurement**, not only between model and **figure**.

**SCOUT D10 “5 greens”** remains the operational stop rule — no new checklist items.

---

## Question 3 — Explicit “Model-Guided Empirical Features” stage?

### Verdict: **Yes — as a labeled stage, not a new workstream**

### What belongs in this stage (already in repo; export/prose only)

| Feature | PD12 name | Repo / artifact |
|---------|-----------|-----------------|
| LOO pool quality | Team quality $\bar{a}_t$ | `poolq_loo`, ventile Fig 2 |
| Viable-peer congestion | $C_{i,t}$ / crowding | `crowding_smooth`, CELL 10; [`tier1_pool_assignment.py`](../sports/tier1_pool_assignment.py) |
| Near-threshold structure | Competitive threshold / borderline harm | 538D CELL 4D exports |
| Army analog (prose) | Senior-rater pool minus mean; competing risks | CODA CIF + cause-specific Cox (empirical leg) |
| Tenure analog (prose) | Dept LOO pub intensity | PEER stage 9 |

### Where it sits (recommended sequence)

```text
Phenomenon (Tier 1 — done)
    ↓
Minimal model POC (Tier 2 — CELL 10; talent-only fail)
    ↓
Model-guided empirical features (Tier 2.5 — EXPORT + label)   ← ADD THIS STAGE NAME
    ↓
Predictions (Tier 3 — near-threshold as test linking C to downturn; Λ prose)
    ↓
Manuscript (Tier 4)
```

**Relative to current forward plan:**

| Current phase | Revised |
|---------------|---------|
| A2 SCOUT D10 | **A2 D10 must explicitly package Tier 2.5 artifacts** (axis table rows for quality vs congestion; heterogeneity PNG/CSV) |
| B2 VECTOR §3 | §3 = minimal model **+** introduced measurements (quality vs congestion) |
| B3 VECTOR §4 | §4 = predictions **as tests of those measurements** (near-threshold; Λ conceptual) |

**Parallelism:** VECTOR may draft §2/§5 while D10 runs; **§3 ink** should reference exported feature names once manifest exists.

---

## Question 4 — Shortest path to publishable manuscript (PD12-faithful)

**Scope:** Manuscript only — not full dissertation completion.

### Shortest faithful path (5 steps)

| Step | Action | Owner | PD12 link |
|------|--------|-------|-----------|
| **1** | Charles **Tier A batch** (unchanged): D10 go, C1–C2, claim table accepted | Charles | Unblocks packaging |
| **2** | **SCOUT D10** — bundle includes: generative contrast, **axis table (quality vs congestion)**, **4D heterogeneity**, score one-pager, refreshed empirical Fig 2 | SCOUT | Priority 3 export |
| **3** | **VECTOR** — draft Wang spine with **explicit Tier 2.5 subsection**: introduce $\bar{a}_t$ vs $C_{i,t}$; use PD12 one-paragraph sentence; claim table §F | VECTOR | Theory → measurements |
| **4** | **VECTOR §4** — prediction #1 as **empirical test** of congestion story (borderline × elite pool); #2 as Λ **conceptual** (Army prose; TBD figure OK with honesty) | VECTOR | Priority 3 + prediction |
| **5** | **Alex read** — estimand sign-off (Army) + confirm **v1 deferrals** (identifiability, falsification) are acceptable **for submission draft** | Charles + Alex | Manage Priority 1/4 expectations |

### Explicitly **not** on this path (PD12 deferred — say so to Alex)

- Full 3-domain generative parameter fit / identifiability (Priority 1)
- Formal 539 kill-switch parameter sweeps beyond documented talent-only fail (Priority 2 extension)
- NHL / macro / fourth-domain falsification (Priority 4)

### Shortest **unfaithful** path (avoid)

Skip Tier 2.5 labeling → draft paper as “generative POC + three empirical U’s” without **quality vs congestion** distinction → **reads like curve-fitting** to Alex (PD12 risk Charles identified).

---

## Question 5 — Document revisions

### Revise (proposed — COMPASS can patch on your go)

| Document | Revision |
|----------|----------|
| **[`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md)** | Insert **Phase B′ (Model-guided features)**; update §3 locked ladder; add PD12 footnote that D10 exports congestion artifacts |
| **[`forward_plan_background.md`](forward_plan_background.md)** | Replace center-of-gravity diagram (§ bottom) with 5-step ladder; add PD12 Priority 3 row in “what everyone agreed” |
| **[`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`](PROJECT_STATUS_AND_NEAR_TERM_PLAN.md)** | One paragraph under modeling status: **Tier 2.5 = model-guided features (SCOUT export)** |
| **[`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md)** | Replace §7 Alex sentence with **B-lite closure** (§Q2 above); C6 note: near-threshold = prediction **and** feature test |
| **[`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md)** | Add 2–3 rows: **quality vs congestion distinction** = supported; **congestion mediates downturn** = preliminary (4D readout); **full identifiability** = defer |
| **[`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md)** | Add bullet: present **5-step ladder** + v1 deferrals (PD12 Priorities 1, 4) |

### Do **not** revise (unless you request)

- Path II nesting chain (`1640` model coherence) — still valid
- Agent STANDING BY files — still valid; Charles locks unchanged
- `COMPASS_Initial_Guidance_v6.md` — archive; superseded by forward plan
- Tier 1 / 538 Cell internals — **no code changes** required for this reassessment

### New doc (optional)

- **`3-Master_Plan/PD12_progression_ladder.md`** — one-page Alex-facing diagram (Charles + VECTOR draft) — **only if you want a standalone committee slide**

---

## Agent read receipts (Charles requested all agents read `1155`)

| Agent | Read `1155`? | CODA/SCOUT/PEER/VECTOR action |
|-------|--------------|-------------------------------|
| **COMPASS** | ✅ | This document |
| **CODA** | ✅ | [`20260615_1156_CODA_read_receipt_PD12_reassessment.md`](20260615_1156_CODA_read_receipt_PD12_reassessment.md) — Army leg unchanged; attrition panel interpretive note per PD12 |
| **SCOUT** | *Route Charles* | Confirm D10 manifest includes Tier 2.5 exports (no new science) |
| **PEER** | *Route Charles* | Tenure remains empirical leg; stage 9 = phenomenon only for Setting 3 |
| **VECTOR** | *Route Charles* | Owns §3–§4 PD12 prose alignment |

---

## COMPASS recommendation to Charles (one paragraph)

> Keep Path II, the claim table, and the Tier A batch **unchanged**. **Relabel** the plan so **model-guided empirical features** (quality vs congestion, near-threshold readout) are an **explicit stage** between minimal model closure and manuscript — because SCOUT already built them and PD12 treats them as **first-class**, not optional decoration. **Tighten closure wording** to Alex’s **B-lite** standard. **Do not** add identifiability, falsification, or new domains before submission draft. Schedule Alex to validate **deferrals**, not to reopen architecture.

---

## Next step for you

1. **Accept or edit** this reassessment (especially Q2 closure definition and Q3 stage name).
2. Reply **“COMPASS: apply doc revisions”** if you want COMPASS to patch forward plan + background + talking points.
3. Proceed with **unchanged Tier A batch** — D10 go still correct; D10 **content spec** now explicitly includes Tier 2.5 exports.

---

*End COMPASS PD12 reassessment.*
