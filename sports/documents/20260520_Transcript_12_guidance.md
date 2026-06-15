# Paper Directions 12 — Guidance for Charles

**Date:** 2026-05-20 (meeting) · **Documented:** 2026-06-15  
**Source:** `transcripts/20260520_Paper_Directions_12_otter_ai_transcript.docx` (Otter; ~16 min)  
**Interpretation:** [`Alex_model_interpreted.md`](Alex_model_interpreted.md) § PD12 addendum  
**Related:** PD11 (pool pre-sorting, May 15) — separate meeting; three threads, not four

---

## Context

Near the start of PD12, Alex confirmed his theoretical memo (`Alex_model.md`) was produced in **~45 minutes with AI assistance** from prompts. Treat it as a **structured brief and mechanism checklist**, not finalized paper prose. **PD12 overrides or sharpens** several terms — especially **capability** (own performance / differentiation within peer group, not institutional strength) and **crowding vs. quality**.

Alex separated **four priority workstreams** in the second half of the call. They are **not the same task**.

---

## Priority 1 — Parameter identifiability (simulation + fit)

**Alex’s ask:** Fit the generative model (~5–6 parameters) to **real data in all three domains** currently in scope (MBB, tenure, …).

**Concern:** The model may be **overparameterized** — many parameter combinations may fit similarly.

**Remedies discussed:**

- **Fix** some generative knobs across worlds (e.g. same Beta hyperparameters everywhere — not estimated per dataset).
- **Roll** mechanism-specific terms into a single outcome \(Y\) per domain (“in this dataset we roll \(a,b,c\) into \(Y\); in that one, \(a,b,d\)”).
- **Lower dimensionality** until recovered parameters are **unique and interpretable**, not just curve-fitting inverted-U shapes.

**Distinction:** Identifiability = “Can we estimate the structural parameters of *this* model from *these* tables?”

**Repo hooks:** `539_alex_model.ipynb`; formal fit / identifiability sweeps.

---

## Priority 2 — Extreme events (simulation sensitivity)

**Alex’s ask:** Not “rare draft surprises” in data — **knob-turning in the sim**:

- Set \(\lambda \to 0\), turn congestion off, tighten viability, etc.
- Confirm the inverted-U and mediation patterns **disappear mechanistically** when they should.

**Purpose:** Validate the **internal logic** of `539_alex_model.ipynb` before over-interpreting one empirical ventile plot.

**Repo hooks:** `539_alex_model.ipynb` parameter kill switches; compare to CELL 10 ability-only null (talent-only fails).

---

## Priority 3 — Model-guided empirical features

**Alex’s ask:** The theory should **propose new measurements**, not only fit old ones.

**Flagship example:**

- Explicit **congestion** in MBB — quantify \(C_{i,t}\).
- Test whether congestion **mediates** the downturn in \(\bar{a}_t\).
- Kentucky/Duke mega-recruit years as **quasi-experiments**.

**Charles’s clarification (~12:15):** Ideal congestion measure **indirectly reflects** talent in the system but **does not enter the outcome as raw \(a_i\)** — study “how crowded is this team?” and predict harm to marginal members. In practice \(\theta\) is built from \(a_j\) or prospect signals (\(Y_{\text{draft}}\), combine, recruiting); document transparently.

**Charles’s commit after the call (~8:22):** Focus on adding the **congestion crowding term** in the empirical pipeline (not replacing all of 538, but making \(C_{i,t}\) first-class).

**Key conceptual split (PD12):**

| Quantity | Role |
|----------|------|
| **Team quality** \(\bar{a}_t\) | Mean peer performance — `poolq_loo` / LOO pool quality |
| **Viable-peer congestion** \(C_{i,t}\) | Density of teammates above prospect threshold — `crowding_smooth`, viable-peer counts |

**Repo status (June 2026):**

- `crowding_smooth` / `pool_c_smooth_loo` — **implemented** in `tier1_pool_assignment.py` + 538D CELL 10
- Near-threshold heterogeneity — CELL 4D exports (`heterogeneity_ventiles_top_tail.*`)
- Do **not** treat LOO **sum** as crowding at fixed roster size (redundant with mean)

**Natural experiments Alex named:** Kentucky/Duke mega-recruiting years; transfer portal/NIL; cohort shock / DiD; mobility reversal (easier in tenure than MBB single-season panel).

---

## Priority 4 — Falsification and scope

**Alex’s ask:** The three main systems were **chosen** because they plausibly satisfy the model’s conditions. A strong paper also shows **where it fails**.

**Tasks:**

- Find a **fourth or fifth setting** where the inverted-U **does not** appear (NHL draft mentioned).
- Explain **which assumption breaks** (e.g. different attention structure, evaluation noise, no local peer congestion for slots).
- Explore **new positive domains** if data exist — Charles suggested **macro economics** (GDP, patents, oil production vs. GDP across nations competing for firms). Alex: “really nice level of estimation” at country–company scale.

**Timeline:** “Let seep over weeks” — not immediate.

---

## Critical PD12 clarifications (not the four priorities, but binding)

### Capability vs. substitutability

| Misread | Corrected read (Alex, PD12) |
|---------|------------------------------|
| Organizational/program capability (e.g. “Duke’s institutional strength”) | **Own performance and differentiation within the local peer group** — proxy for latent talent \(a_i\) |

In elite environments everyone is strong but **substitutable**; identifiability collapses even when absolute \(a_i\) is high.

### Army CIF figure (Charles showed)

- **Promotion (top):** Inverted-U with elite-tier dip — cross-domain shape exists.
- **Attrition (bottom):** Not a mirror image by construction; late-bin rebound (“superstar tail”) visible — interpret with care (few people / wide uncertainty in top bins).
- PD12 point: **shape exists across domains**, not that promotion and attrition must move opposite bin-for-bin.

### One-paragraph paper sentence (PD12-aligned)

> We distinguish **team quality** (mean peer performance, \(\bar{a}_t\)) from **viable-peer congestion** (density of teammates above a prospect threshold, \(C_{i,t}\)). Elite environments raise both average talent and **substitutability**; the inverted-U in advancement is predicted to steepen on the right primarily where \(C_{i,t}\) is high, especially for **near-threshold** individuals, while **top latent talent** still clears selection — consistent with the small recovery at the highest ventiles in our NCAA draft data.

---

## Suggested implementation order (from Alex_model_interpreted)

1. **`tier1_mechanism_vars.py` / 530 export:** `peer_viable_count_loo` (and optional smooth \(C_{i,t}\) from 539 logic); keep `poolq_loo` as quality leg.
2. **538 / 538D CELL 10:** `crowding_smooth` mode live; document quality vs pool-mean axis (Plot B toggle).
3. **`539_alex_model.ipynb`:** Cells for Priority 1–2 (fit / identifiability, parameter kill switches).
4. **`panel_rebuild` / `combine_bridge`:** Optional `Y_combine_meas`, `Y_nba_signal` on panel for \(\theta\) robustness.
5. **Writing:** Short PD12 cross-ref in advisor briefs; **do not** claim all six mechanisms are separately identified in MBB v1.

---

## Mapping to v1 manuscript plan (June 2026 agent consensus)

| PD12 priority | v1 manuscript status (Path II) |
|---------------|--------------------------------|
| **1 Identifiability** | **Deferred** — qualitative generative POC; not full 3-domain calibration |
| **2 Extreme events** | **Partial** — talent-only fails (CELL 10); formal 539 kill-switch sweeps not draft-critical |
| **3 Congestion features** | **Primary alignment** — crowding_smooth, CELL 10, 4D heterogeneity; SCOUT D10 bundle next |
| **4 Falsification** | **Deferred** — NHL / 4th domain not in Summer–Fall 2026 scope |

**Tension to manage with Alex:** PD12 is richer than the locked v1 path. Agent correspondence (Rounds 1–5) parked 1 and 4 to enable manuscript draft. Priority 3 is what current SCOUT/VECTOR work delivers.

---

## Open questions left on the table (PD12)

- Exact \(\theta\) for MBB: global PPM quantile vs combine/draft-based \(Y_{\text{nba\_signal}}\) vs smooth logistic viability (539).
- Whether to **mediate** with \(C_{i,t}\) in LPM only or also in Tier 1 generative selection (538).
- NHL (or other) **negative case** data feasibility for Priority 4.

---

*End PD12 guidance.*
