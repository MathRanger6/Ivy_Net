# COMPASS → Charles: PD12 reassessment (canonical)

**Canonical name:** `14_PD12_reassessment_memo.md`  
**Original archive:** [`obsolete/original_filenames/20260615_1200_COMPASS_PD12_reassessment.md`](obsolete/original_filenames/20260615_1200_COMPASS_PD12_reassessment.md)

**Date:** 2026-06-15 12:00  
**From:** COMPASS  
**To:** Charles Levine (cc: CODA, SCOUT, PEER, VECTOR)  
**In reply to:** [`obsolete/pd12_reassessment_duplicates/20260615_1155_Charles_to_COMPASS.md`](obsolete/pd12_reassessment_duplicates/20260615_1155_Charles_to_COMPASS.md)  
**Supersedes:** duplicate drafts in [`obsolete/pd12_reassessment_duplicates/`](obsolete/pd12_reassessment_duplicates/)

**Sources reviewed:** [`20260520_Transcript_12_guidance.md`](20260520_Transcript_12_guidance.md), [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md), [`06_Generative_closure_checklist.md`](06_Generative_closure_checklist.md), [`07_Claim_language_guardrails.md`](07_Claim_language_guardrails.md), agent STANDING BY files (in [`obsolete/`](obsolete/)), agent PD12 inputs (`1156` round, in [`obsolete/pd12_reassessment_duplicates/`](obsolete/pd12_reassessment_duplicates/)).

**Constraint honored:** No scope expansion, no new workstreams, Path II and correspondence consensus **not** relitigated — **sequencing and language** adjusted only.

---

## Executive answer

Charles’s PD12 reread is **correct**: recent planning **compressed** Alex’s ladder toward **Phenomenon → Minimal model → Paper**, with **model-guided empirical features** (PD12 Priority 3) **under-labeled** in forward docs.

The fix is **not** to reopen identifiability (PD12 Priority 1), full extreme-event sweeps (Priority 2), or falsification domains (Priority 4). The fix is to **make explicit** what SCOUT already built — **quality vs congestion**, **crowding / viable-peer density**, **near-threshold heterogeneity** — as a **named stage** between minimal model and manuscript, and to **tighten the closure definition** toward Alex’s standard **without adding tasks**.

**Living docs patched:** forward plan, [`04_Project_story_plain_English.md`](04_Project_story_plain_English.md), [`03_Where_we_are_now.md`](03_Where_we_are_now.md), [`06_Generative_closure_checklist.md`](06_Generative_closure_checklist.md) §7.

---

## Question 1 — Does the current plan reflect Alex’s intended scientific progression?

### Verdict: **Mostly yes on substance; modest drift on sequencing emphasis**

| Alex progression (PD12 spirit) | Current plan (June 2026) | Alignment |
|--------------------------------|--------------------------|-----------|
| Phenomenon (inverted-U, three settings) | Locked triad; tenure preliminary | ✅ |
| Minimal model organizes inquiry | Path II; Alex score; soft assignment | ✅ |
| Model suggests **new measurements** | **Implemented in repo** (`crowding_smooth`, viable-peer logic, `sports/538D_development.ipynb` CELL 4D heterogeneity) but **not named as a plan stage** | ⚠️ **Under-labeled** |
| Model generates predictions | #1 near-threshold, #2 K peak-shift locked | ✅ (#2 prose-heavy) |
| Parameter identifiability / 3-domain fit | Explicitly **deferred** | ✅ intentional deferral |
| Falsification / 4th domain | **Deferred** | ✅ intentional deferral |

### Where the plan diverges (wording / emphasis, not science)

1. Forward plan Phases A–B read as: unlock D10 → draft paper. That optimizes **packaging velocity**, not Alex’s **“theory proposes new measurements”** sentence (PD12 Priority 3).

2. [`04_Project_story_plain_English.md`](04_Project_story_plain_English.md) showed `Phenomenon → Minimal model → Prediction → Paper`. PD12’s richer ladder is:

```text
Phenomenon → Minimal model → Model-guided features → Predictions → Paper
```

3. **Congestion** is first-class in SCOUT code and PD12 docs but **second-class in planner prose** — the drift Charles and VECTOR flagged.

### Recommended adjustment (material, not expansion)

Re-label the locked ladder in all planning docs as **five rungs** (Rung 2.5 = model-guided features). **No new cells required for v1** if Rung 2.5 is satisfied by artifacts already on disk or exported in D10.

---

## Question 2 — Is “minimal model closure” consistent with Alex’s guidance?

### Verdict: **Upgrade the definition one notch — do not replace it**

**Name origin:** **B-lite** is a **COMPASS label** (this memo, 2026-06-15), not terminology from Alex. It names the middle option between “too weak” (curve only) and “too strong for v1” (full parametric identifiability — PD12 Priority 1).

| Option | Standard | COMPASS recommendation |
|--------|----------|------------------------|
| **A** | Model reproduces phenomenon | **Too weak** for PD12 |
| **B (full)** | Phenomenon + measurable + prediction + identifiability | **Too strong for v1** — pulls in PD12 Priority 1 |
| **B-lite (adopted)** | Phenomenon + model-motivated empirical quantity exported + ≥1 prediction with empirical readout + honest limitations | **Matches Alex Priority 3 without new work** |

### Recommended closure standard (v1 manuscript)

```text
(1) Phenomenon anchored empirically (LOO inverted-U; honest maturity labels)
(2) Minimal mechanism demonstrated:
      talent-only fails + congestion-in-score bends curves (Path II POC)
(3) At least one model-guided measurable quantity exported or cited:
      e.g. crowding_smooth / viable-peer congestion vs poolq_loo (quality)
(4) At least one prediction-facing readout tied to mechanism:
      e.g. near-threshold heterogeneity (`538D` CELL 4D); K hook prose (#2)
(5) Honest limitation prose (axis mismatch; tenure preliminary; no causal claims)
(6) Frozen export bundle (D10)
```

**Explicitly not required for v1 closure:** parametric recovery in all three domains; fourth-domain falsification; full B(Q)−D(Q) generative decomposition in prose as if estimated.

**Operational stop rule unchanged:** SCOUT D10 → **5 greens** per checklist C1–C7 (optional row **C8**: quality vs congestion exported in bundle).

---

## Question 3 — Explicit “Model-Guided Empirical Features” stage?

### Verdict: **Yes — as a labeled stage, not a new workstream**

### What counts (v1 — export/prose only)

| Domain | Feature(s) | Status | Agent |
|--------|------------|--------|-------|
| **Basketball** | Quality `poolq_loo` vs congestion `crowding_smooth` / \(C_{i,t}\) | Implemented; export in **D10** | SCOUT |
| **Basketball** | Near-threshold heterogeneity (`538D` CELL 4D ventiles) | On disk (`#08`) | SCOUT |
| **Army** | Pool minus mean (quality); pool size / K hook | Empirical | CODA |
| **Tenure** | `poolq_loo_mean` (quality); `pool_size_oa_loo` as congestion proxy | On panel; stage 9 uses quality only | PEER |

### Where it sits

```text
Phenomenon (Rung 1 — done)
    ↓
Minimal model POC (Rung 2 — `sports/538D_development.ipynb` CELL 10; talent-only fail)
    ↓
Model-guided empirical features (Rung 2.5 — EXPORT + label)   ← ADD THIS STAGE NAME
    ↓
Predictions (Rung 3 — near-threshold; K prose)
    ↓
Manuscript (Rung 4)
```

**Relative to forward plan:** D10 must package Tier 2.5 artifacts; staging **`#12` §3** (Methods) introduces measurements before **`#12` §4** (Predictions → manuscript **§7**).

**Optional (Charles only — PD12-C):** PEER supplementary bin read on `pool_size_oa_loo` (~0.5–1 session, existing panel). Strengthens tenure on P3 slide; **not required** for v1.

---

## Question 4 — Shortest path to publishable manuscript (PD12-faithful)

**Scope:** Manuscript only — not dissertation completion.

| Step | Action | Owner | PD12 link |
|------|--------|-------|-----------|
| **1** | Charles **Tier A batch** (unchanged): D10 go, C1–C2, V1–V3 | Charles | Unblocks packaging |
| **2** | **SCOUT D10** — generative contrast, **axis table (quality vs congestion)**, near-threshold heterogeneity (`538D` CELL 4D), score one-pager, refreshed empirical Fig 2 | SCOUT | Priority 3 export |
| **3** | **VECTOR** — Wang spine with **Tier 2.5 subsection**; PD12 one-paragraph sentence (quality vs \(C_{i,t}\)) | VECTOR | Theory → measurements |
| **4** | **Manuscript §7** (from staging `#12` §4) — #1 as empirical test of congestion story; #2 K conceptual (Army prose) | VECTOR | Predictions |
| **5** | **PEER** inference CSV (C1–C2); **manuscript §4** tenure + limitations | PEER | Rung 1 leg honest |
| **6** | **Alex meeting** — present 5-rung ladder; confirm v1 **deferrals** (P1, P4) acceptable for submission draft | Charles + Alex | Manage expectations |

**Explicitly not on this path:** full 3-domain generative fit (P1); NHL / fourth-domain falsification (P4); generative LOO bin-for-bin match.

**Shortest unfaithful path (avoid):** Skip Tier 2.5 labeling → draft as “generative POC + three empirical U’s” without quality vs congestion distinction.

---

## Question 5 — Document revisions

| Document | Status |
|----------|--------|
| [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md) | **Patched** — §3 ladder, Phase B′, D10 spec |
| [`04_Project_story_plain_English.md`](04_Project_story_plain_English.md) | **Patched** — 5-rung diagram, PD12 box |
| [`03_Where_we_are_now.md`](03_Where_we_are_now.md) | **Patched** — PD12 alignment row, Tier 2.5 |
| [`06_Generative_closure_checklist.md`](06_Generative_closure_checklist.md) | **Patched** — §7 B-lite closure |
| Claim table, STANDING BY files, Path II nesting chain | **Unchanged** (still valid) |

---

## Agent read receipts and routing

Charles requested all agents read [`obsolete/pd12_reassessment_duplicates/20260615_1155_Charles_to_COMPASS.md`](obsolete/pd12_reassessment_duplicates/20260615_1155_Charles_to_COMPASS.md).

| Agent | Read receipt | Action after reassessment |
|-------|--------------|---------------------------|
| **COMPASS** | ✅ | This document + living doc patches |
| **SCOUT** | [`obsolete/pd12_reassessment_duplicates/20260615_1156_SCOUT_to_COMPASS_PD12_reassessment_input.md`](obsolete/pd12_reassessment_duplicates/20260615_1156_SCOUT_to_COMPASS_PD12_reassessment_input.md) | D10 manifest lists Tier 2.5 exports (quality vs congestion panel, `538D` CELL 4D heterogeneity); optional C8 row |
| **CODA** | [`obsolete/pd12_reassessment_duplicates/20260615_1156_CODA_read_receipt_PD12_reassessment.md`](obsolete/pd12_reassessment_duplicates/20260615_1156_CODA_read_receipt_PD12_reassessment.md) | Army lane unchanged; axis table gloss for quality leg; K / pool-size for prediction #2 |
| **PEER** | [`obsolete/pd12_reassessment_duplicates/20260615_1156_PEER_read_receipt_Charles_to_COMPASS.md`](obsolete/pd12_reassessment_duplicates/20260615_1156_PEER_read_receipt_Charles_to_COMPASS.md) | C1–C2 path unchanged; optional PD12-C pool_size read on Charles route |
| **VECTOR** | Co-requester via Charles; no separate receipt on disk | Staging `#12` §2–§3 before §4; PD12 quality/congestion paragraph in draft |

**No new correspondence round** unless a conflict appears.

---

## Charles decisions (minimal — Tier 1 unchanged)

| ID | Question | COMPASS rec. |
|----|----------|--------------|
| **PD12-A** | Accept **5-rung ladder** relabel in planning docs? | **Yes** (applied) |
| **PD12-B** | Upgrade closure definition to B-lite? | **Yes** (applied) |
| **PD12-C** | Optional PEER **pool_size** feature read for tenure? | **Your call** — ~0.5–1 session |
| **PD12-D** | Tell Alex P1/P4 deferred explicitly at next meeting? | **Yes** |

Tier 1 execution locks (D10, C1–C2, V1–V3) **unchanged**.

---

## One paragraph for Alex

> We are not walking back Path II or the correspondence consensus. The v1 manuscript will show an empirical inverted-U on LOO peer quality across three settings, a minimal generative proof that talent-only selection fails and congestion in the score can bend curves, **explicit model-guided measurements** (quality vs congestion in basketball; pool structure in Army and tenure where data already exist), and two prediction-facing readouts — near-threshold heterogeneity and a global-capacity K hook. Full parametric identifiability across all three domains and a formal negative fourth setting are **planned next**, not blockers for the first complete draft.

---

*End COMPASS PD12 reassessment (canonical).*
