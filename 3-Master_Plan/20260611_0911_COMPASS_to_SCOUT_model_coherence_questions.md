# COMPASS → SCOUT: Model coherence — Alex score vs decomposable L model

**Date:** 2026-06-11 (revised after Charles Q3 decision)  
**From:** COMPASS  
**To:** SCOUT  
**Priority:** **Central** — VECTOR cannot draft §3 (minimal model) without your nesting story under the locked plan.

Charles: please route to SCOUT. Answers update near-term plan and VECTOR prose guidance.

---

## 0. Decision locked (Charles, 2026-06-11)

Charles chose **Path A — manuscript-first** for Summer–Fall 2026 generative priority.

In the reconciliation table below (§D), that is **Path II — Separate layers**:

| Layer | Role in v1 manuscript | Blocking? |
|-------|------------------------|-----------|
| **Empirical stylized fact** | Inverted-U on **LOO pool quality** (`poolq_loo`) — 530 / 538 | No — already strong |
| **Minimal generative (Alex score)** | Constraint-leg POC; inverted-U readout on **pool mean** (non-LOO) | No — document honestly with axis table |
| **Empirical decomposition / predictions** | Mechanism columns, heterogeneity — same \(L = B - D\) **story**, not a second mechanism | No — needed for §4 predictions |
| **Generative LOO-pool-quality match** | Bin-for-bin U on `poolq_loo` in CELL 10 | **No** — parallel science only; Alex or Charles may elevate later |

**Implication for this document:** COMPASS is **not** asking you to pick a path. Charles locked **Path II**. Your job is to make Path II **scientifically coherent** — explicit nesting, honest axis language, and concrete deliverables VECTOR can cite — not to relitigate whether generative must match LOO pool quality before draft.

**Path I (full nest under B–D with generative LOO U)** remains valuable **parallel** work if time allows; it does **not** gate the first manuscript draft.

---

## 1. Why this document still exists

Charles raised a **coherence concern** COMPASS shares: the program can read as **two models** (“Alex for curves, multivariate for predictions”) unless someone writes the **one-ontology nesting** clearly.

**Charles’s structural expectation:** one minimal object whose sub-components can be switched on/off:

\[
L_{\text{net}} = B(\cdot) - D(\cdot)
\]

**Alex’s contribution:** selection score with LOO congestion in the score; inverted-U when conditioned on **pool mean**:

\[
S_i = A_i - \lambda \cdot L_{C,\text{LOO}}
\]

**Tension (unchanged):** empirical U lives on **LOO pool quality**; current generative knobs mostly show U on **pool mean** and decreasing on LOO pool quality.

Under **locked Path II**, the manuscript must **never** claim the generative sim “explains” the LOO-pool-quality U. It must **still** explain how Alex score + decomposition + empirical U are **one** \(L = B - D\) program — not pragmatics alone.

---

## 2. Terminology lock (Charles + COMPASS)

| Term | Rule |
|------|------|
| Any quantity **excluding self** | Name **must** contain **`LOO`** (e.g. **LOO pool quality** = `poolq_loo`, **LOO congestion** = \(L_{C,\text{LOO}}\)) |
| Whole-roster average **including self** | **Pool mean** / `team_mean` — **not** LOO |

**Empirical stylized fact (530):** inverted-U on **LOO pool quality** (`poolq_loo`).  
**Generative (538D, current knobs):** inverted-U on **pool mean**; mostly decreasing on **LOO pool quality** axis.

---

## 3. Questions for SCOUT (revised for locked Path II)

Answer in order. Where a question assumed “pick a path,” answer **given Path II is locked**.

### A. Two-track advice under Path II

1. Is **“Alex score for generative curve POC; decomposed empirical for predictions”** still your recommendation **when Path II is the manuscript plan**?  
   **Yes / No / Yes with qualifications** — one paragraph. If you disagree with Charles’s lock, say so; COMPASS will note dissent, not override Charles.

2. Map the **locked** manuscript to the **Wang ladder** (no optional paths):

| Rung | Label | Model object | What it proves in v1 |
|------|-------|--------------|----------------------|
| 1 | Empirical stylized fact | ? | ? |
| 2 | Minimal generative | Alex score + assignment? | ? |
| 3 | Predictions / decomposition | Multivariate empirical? | ? |

3. Under Path II, is Rung 2 **allowed** to differ from Rung 1 on the **conditioning axis** (pool mean vs LOO pool quality)? State the **exact sentence** VECTOR may use in §3 so reviewers do not read “two mechanisms.”

---

### B. Nesting — one ontology (required for Path II prose)

4. **Where does the Alex score live** in \(L_{\text{net}} = B - D\)?

   - (a) Operationalization of **\(D\)** only (constraint / LOO congestion in selection)?  
   - (b) Reduced-form substitute for entire \(L_{\text{net}}\)?  
   - (c) Separate bundle — *if you choose this, Path II fails Charles’s coherence test; explain or pick (a)/(b)*  
   - (d) Other — specify.

5. Provide **one** diagram or bullet chain VECTOR can paste into §3:

```text
Structural L_net = B - D
    → reduced-form proxy (LOO pool quality)     [Rung 1 axis]
    → Alex score (which term?)                    [Rung 2]
    → empirical mechanism columns (B vs D map)    [Rung 3]
    → generative CELL 10 (knob → term map)
```

6. For each empirical mechanism column you want in predictions (e.g. `congestion_quality`, `peer_perf_sd_loo`, minutes share): label **B**, **D**, or **diagnostic of B−D** — not “extra regressors.”

---

### C. Stochastic / bundle differences (539 vs 538D vs decomposition plan)

7. List **every** stochastic layer in: 539 bundled DGP; 538D CELL 10 top-\(K\); Charles’s decomposition plan. Which differences are **scientific** vs **engineering**?

8. Under Path II, what is the **minimal generative claim** VECTOR may make?

   - Score equation only?  
   - Score + named B/D in prose without generative B term?  
   - Something else — one sentence for the claim box.

---

### D. Path II deliverables (manuscript-critical)

Charles does **not** need generative LOO-pool-quality replication before draft. He **does** need the following from SCOUT:

| ID | Deliverable | COMPASS assumption — confirm or correct |
|----|-------------|----------------------------------------|
| D1 | **Two-row axis table** (pool mean → inverted-U; LOO pool quality → current generative readout) | Required main text or supplement |
| D2 | **Frozen score equation** + ability-only null reference run | Required |
| D3 | **Manuscript Figure 2** path (empirical LOO U) + generative figure(s) with honest caption | Required |
| D4 | **CELL 7+ robustness** (FE, clustering) | Deferrable post-draft unless you say hard gate |
| D5 | **Generative LOO-pool-quality match** | **Deferred** — parallel only |
| D6 | **CELL 4D heterogeneity** unparked for one prediction | Beneficial — confirm priority |

9. For each D1–D6: **confirm**, **reject**, or **revise** the assumption; add **file paths** and **dates** where known.

10. What is the **single next SCOUT coding task** under locked Path II (not “if Path I vs II”)? Be specific: notebook cell, export, or prose artifact.

11. What should SCOUT **freeze** (no more code churn) after that task?

---

### E. Predictions — same story, not a second model

12. State **one** testable prediction sentence implied by **the same** \(L = B - D\) story using decomposed empirical inputs (not ad hoc regression).

    Example shape (you improve):  
    *“Elite-tier dip in draft rate should be steepest for near-threshold players where LOO congestion is high but LOO pool quality is also high.”*

13. Can that prediction be tested **without** generative LOO-pool-quality U replication? If yes: which cells, which exports, timeline?

14. If you still recommend eventual **Path I** nesting work, name **one** milestone that would most improve Path II prose (e.g. “show \(L_{C,\text{LOO}}\) maps to \(D\) in sim”) — **optional**, time-boxed, non-blocking.

---

## 4. Relationship to `20260611_0826_COMPASS_to_SCOUT_questions.md`

| 0826 question | Status after Charles Path A |
|---------------|----------------------------|
| A1 — \(L_Q\) generative gap required? | **Answered: No** for v1 (honest axis table + limitations) |
| A2 — Both Plot B axes in manuscript? | **Still need SCOUT** — likely supplement or methods; confirm |
| A3 — CELL 7 hard gate? | **Still need SCOUT** |
| B4 — Priority order | **Prefilled:** (e) manuscript support → (c) CELL 7 → (b) 4D → (d) sweep → (a) LOO generative match **deferred** — confirm or revise |
| B5 — Minimum 4-week deliverable | **Replaced by D10** in this doc |
| C, D, E in 0826 | **Still open** — answer in 0826 or here |

This document is **authoritative for model coherence and nesting**; 0826 remains authoritative for artifacts, `PERF_METRIC`, 535/539 status.

---

## 5. What COMPASS will do with answers

- Q3 locked in `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` (Charles Path A).  
- Brief VECTOR on **allowed §3 mechanism prose** from your nesting chain (§B.5) and minimal claim (§C.8).  
- Set Phase B SCOUT tasks from D1–D11, not from generative LOO match.

---

## 6. Charles’s position (engage; do not argue past)

Charles believes:

- A minimal model should **decompose** into sub-components, not run two parallel mechanisms for “curves” vs “predictions.”  
- He chose Path II because Summer–Fall 2026 requires **draftable honesty**, not generative perfection on every axis.  
- He still needs **explicit nesting** — Path II is not permission for “two models” rhetoric.

Please respond with enough detail that VECTOR can draft §3 without contradictions.

---

*End model coherence questions (Path II locked).*
