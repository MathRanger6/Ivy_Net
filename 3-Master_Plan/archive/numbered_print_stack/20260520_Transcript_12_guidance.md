# Paper Directions 12 — Transcript guidance (May 20, 2026)

**Filename:** `20260520_Transcript_12_guidance.md`  
**Source:** `transcripts/20260520_Paper_Directions_12_otter_ai_transcript.docx` (Otter; ~16 min)  
**Participants:** Alex Gates, Charles Levine  
**Interpreted in:** [`sports/documents/Alex_model_interpreted.md`](../../../sports/documents/Alex_model_interpreted.md) (PD12 addendum)

**Purpose:** Standalone summary of what Alex prioritized in PD12 — especially the **four workstreams** — without reading the full transcript or interpreted memo.

---

## Provenance note

- `Alex_model.md` was produced in **~45 minutes with AI assistance** from prompts — a **structured theoretical brief**, not finalized paper prose.
- **PD12 overrides or sharpens** several terms (especially **capability** vs **crowding/quality**) where the live discussion went deeper than the draft text.

---

## Critical conceptual fix (read before the four priorities)

### Capability ≠ organizational strength

| Misread | Corrected read (Alex, PD12) |
|---------|-------------------------------|
| “Capability” = program/institutional strength (e.g. Duke’s brand) | “Capability” ≈ **individual talent and how differentiated** the person is from peers |
| Elite school = high org quality only | Elite environment = **very high talent** but **extreme substitutability** — excellent people, hard to tell apart |

**Implementation mapping:**

| Construct | Empirical proxy (MBB) | Role |
|-----------|----------------------|------|
| **Quality** \(\bar{a}_t\) | LOO mean teammate performance (`poolq_loo`) | Rising leg of inverted-U |
| **Congestion** \(C_{i,t}\) | Viable-peer count / `crowding_smooth` above threshold \(\theta\) | Downturn leg — **do not use LOO sum** (≈ mean at fixed roster size) |

> *“How many people are above the threshold—that’s an easy calculation.”* — Alex (~7:20)

Charles committed on the call (~8:22) to make **congestion crowding** first-class in the empirical pipeline.

---

## Alex’s four priorities (second half of PD12)

Alex separated **four threads**. They are **not the same task.**

### Priority 1 — Parameter **identifiability** (simulation + fit)

**Task:** Fit the generative model (~5–6 parameters) to **real data in all three domains** in scope (MBB, tenure, …).

**Alex’s concern:** The model may be **overparameterized** — many parameter combinations fit similarly (curve-fitting inverted-U shapes without unique structural meaning).

**Remedies discussed:**

- **Fix** some generative knobs across worlds (e.g. same Beta hyperparameters everywhere — not estimated per dataset).
- **Roll** mechanism-specific terms into a single outcome \(Y\) per domain (“in this dataset we roll \(a,b,c\) into \(Y\)”).
- **Lower dimensionality** until recovered parameters are **unique and interpretable**.

**Distinction:** Identifiability = *“Can we estimate the structural parameters of this model from these tables?”*

**Repo hook:** `539_alex_model.ipynb` — fit / identifiability sweeps.

---

### Priority 2 — **Extreme events** (simulation sensitivity)

**Task:** **Knob-turning in the sim**, not rare draft surprises in real data.

Examples:

- Set \(\lambda \to 0\)
- Turn congestion off
- Tighten viability thresholds

**Goal:** Confirm inverted-U and mediation patterns **disappear mechanistically** when they should.

**Distinction:** Validate **internal logic** of the generative model before over-interpreting one empirical ventile plot.

**Repo hook:** `539_alex_model.ipynb` — parameter kill switches; 538D CELL 10 ability-only null (talent-only fails).

---

### Priority 3 — **Model-guided empirical features**

**Task:** Theory should **propose new measurements**, not only fit old ones.

**Flagship example (MBB):**

- Quantify explicit **congestion** \(C_{i,t}\)
- Test whether \(C_{i,t}\) **mediates** downturn in \(\bar{a}_t\)
- Natural experiments: **Kentucky / Duke mega-recruit years**, transfer shocks, mobility reversal (leave congested program → odds rise)

**Charles’s design constraint (~12:15):** Ideal congestion measure **reflects talent in the system indirectly** but **does not enter the outcome as raw \(a_i\)** — study “how crowded is this team?” and predict harm to **marginal** members.

**Near-threshold population:** Inverted-U harm is strongest for **borderline** performers (NIH/Wang “just at the cut line”), not obvious superstars or non-contenders. **Superstars still get drafted** in elite teams — heterogeneous effect, not “elite hurts everyone.”

**Repo hook (June 2026):** `crowding_smooth` in `tier1_pool_assignment.py` + 538D CELL 10; CELL 4D heterogeneity exports; `tier1_mechanism_vars.py` / 530 export for viable-peer counts.

---

### Priority 4 — **Falsification and scope**

**Task:** Strong paper shows **where the model fails**, not only where it works.

**Alex’s agenda:**

- Find a **4th or 5th setting** where inverted-U **does not** appear (NHL draft mentioned) → explain **which assumption breaks** (attention structure, evaluation noise, no local peer congestion for slots, etc.).
- Explore **new positive domains** if data exist (Charles suggested macro: GDP, patents, oil production vs. national firm competition; Alex noted “really nice level of estimation”).

**Pace:** “Let seep over weeks” — not blocking immediate MBB congestion work.

---

## Six mechanisms — scope discipline

`Alex_model.md` lists six mechanism classes. PD12 walkthrough: they are **reasons the theory matters**, not six separate causal channels to prove in one MBB table.

| # | Mechanism | PD12 emphasis |
|---|-----------|---------------|
| 1 | Comparative evaluation | Signal distinctiveness in elite groups |
| 2 | Attribution dilution | Include in narrative; optional test later |
| 3 | Finite attention | **Substitutability** of borderline elite; near-threshold |
| 4 | Organizational risk minimization | “Moneyball” heuristics when \(C_{i,t}\) high |
| 5 | Opportunity suppression | **Recursive** — peers → fewer touches → weaker stats |
| 6 | Queueing / timing | Selection scarcity; don’t over-build all facets in v1 |

**Writing rule:** Address **some**, not all; use mechanisms to **guide measurement**.

---

## Army evidence shown (same meeting)

Charles showed Alex **100-bin equal-width CIF** (promotion top, attrition bottom) on LOO pool quality.

**PD12 point:** Cross-domain shape exists — not NCAA-only curve-fit. Motivated investing in MBB congestion crowding.

**Careful read:** Promotion and attrition panels are **not** required to mirror bin-for-bin; late-bin attrition rebound ≠ superstar story without checking bin N and uncertainty.

---

## Suggested implementation order (from interpreted memo)

1. **530 export:** `peer_viable_count_loo` (+ optional smooth \(C_{i,t}\)); keep `poolq_loo` as quality leg.
2. **538 / 538D CELL 10:** `crowding_smooth` live; document Plot B axis (pool mean vs LOO pool quality).
3. **539:** Priorities 1–2 (identifiability, kill switches).
4. **combine_bridge / panel:** Optional `Y_nba_signal` for \(\theta\) robustness.
5. **Writing:** PD12 cross-ref in advisor briefs; **do not** claim all six mechanisms separately identified in MBB v1.

---

## PD12-aligned one-paragraph paper sentence

> We distinguish **team quality** (mean peer performance, \(\bar{a}_t\)) from **viable-peer congestion** (density of teammates above a prospect threshold, \(C_{i,t}\)). Elite environments raise both average talent and **substitutability**; the inverted-U in advancement is predicted to steepen on the right primarily where \(C_{i,t}\) is high, especially for **near-threshold** individuals, while **top latent talent** still clears selection—consistent with the small recovery at the highest ventiles in our NCAA draft data.

---

## How PD12 maps to current v1 forward plan (June 2026)

| PD12 priority | v1 manuscript status (agent consensus) |
|---------------|----------------------------------------|
| **1 Identifiability** | **Deferred** — Path II qualitative generative POC; not 3-domain parameter fit |
| **2 Extreme events** | **Partial** — talent-only fails (CELL 10); full kill-switch sweeps post-draft |
| **3 Congestion features** | **Active** — aligns with D10 bundle, near-threshold prediction #1, crowding in score |
| **4 Falsification** | **Deferred** — NHL / 4th domain post–Summer–Fall 2026 |

PD12 is **richer** than the locked v1 path. The correspondence experiment **consciously parked** 1 and 4 to enable **writing now**; Priority 3 is what SCOUT D10 delivers.

---

## Open questions left on the table (PD12)

- Exact \(\theta\) for MBB: global PPM quantile vs combine/draft-based \(Y_{\text{nba\_signal}}\) vs smooth logistic viability (539).
- Mediate with \(C_{i,t}\) in LPM only vs also in Tier 1 generative selection (538).
- NHL (or other) **negative case** data feasibility for Priority 4.

---

## Related files

| File | Role |
|------|------|
| [`Alex_model_interpreted.md`](../../../sports/documents/Alex_model_interpreted.md) | Full PD12 addendum + mechanism notes |
| [`Alex_model.md`](../../../sports/documents/Alex_model.md) | AI-assisted theoretical brief (pre-PD12 corrections) |
| [`Tier1_Presorting_Design_Note.md`](../../../sports/documents/Tier1_Presorting_Design_Note.md) | PD11 (earlier meeting — pool pre-sorting; separate from PD12 four priorities) |
| [`forward_plan_background.md`](forward_plan_background.md) | Bring-up-to-speed after agent experiment |
| [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md) | Ordered next steps + Charles locks |

---

*End PD12 guidance summary.*
