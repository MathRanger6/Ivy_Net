# Model Nesting Note (v1)

**Date:** 2026-06-24  
**Author:** COMPASS (Charles Tier 1 execution)  
**Audience:** VECTOR §3, Alex read-through, committee  
**Status:** Frozen for v1 manuscript — no new equations

---

## 1. Problem this note solves

The project had **one ontology** and **two readouts** that looked like two models:

- Charles’s decomposable story: \(L_{\text{net}} = B - D\) (development benefit minus competitive constraint)
- Alex’s selection score: \(S_i = A_i - \lambda L_{C,\text{LOO}}\) (ability minus congestion in selection)

This note states how they nest. **Path II is locked:** generative POC on pool mean; empirical stylized fact on LOO pool quality; predictions from decomposed empirical columns — **same object**, different rungs.

---

## 2. Structural object (one model)

```
L_net = B(·) − D(·)
         │         │
         │         └─ D: LOO congestion, crowding, finite slots, substitutability
         └─ B: visibility, norms, opportunity (minutes, elite exposure)
```

| Symbol | Meaning |
|--------|---------|
| \(B(\cdot)\) | Developmental / signaling upside of stronger local peers |
| \(D(\cdot)\) | Competitive constraint / distinction compression from comparable peers |
| \(L_{\text{net}}\) | Net local environment effect on advancement propensity (reduced form) |
| \(A_i\) | Own ability / performance — **outside** \(L_{\text{net}}\), enters selection directly |

**Alex score:** \(S_i = A_i - \lambda L_{C,\text{LOO}}\) is **\(D\) entering the selection rule**, jointly with own \(A_i\). It is **not** the full reduced-form \(L_{\text{net}}\) and **not** a second mechanism.

---

## 3. Wang ladder (five rungs — v1)

```text
Rung 1   Phenomenon
         Realized pools → LOO pool quality (poolq_loo) → draft/promotion/tenure rate
         → inverted-U on LOO peer-quality proxy (Army ✅, MBB ✅, tenure ⚠️ preliminary)

Rung 2   Minimal generative POC (basketball only)
         Soft assignment → S_i = A_i − λ·L_{C,LOO} → top-K selection
         → talent-only fails; congestion bends curves on **pool mean** axis
         → NOT bin-for-bin LOO pool-quality replication

Rung 2.5 Model-guided empirical features (PD12 P3)
         poolq_loo (quality) vs crowding_smooth (congestion C_{i,t})
         → theory proposes measurements, not only fits old curves

Rung 3   Predictions (named candidates — not all proven)
         #1 Near-threshold heterogeneity (MBB 4D export)
         #2 Peak shift with global Λ (Army-led prose hook)

Rung 4   Manuscript
```

---

## 4. Axis discipline (mandatory limitation sentence)

> The empirical stylized fact is defined on **leave-one-out pool quality** among teammates; the minimal generative proof-of-concept conditions advancement on **whole-roster pool mean** and a selection score that penalizes **leave-one-out viable-peer congestion**. These are different conditioning objects: the generative exercise demonstrates that a congestion penalty in the selection rule can produce non-monotone advancement curves, while the empirical inverted-U remains the replicated fact on LOO pool quality — **not** a bin-for-bin reproduction of that fact by the current simulation knobs.

(Source: SCOUT model coherence §A3; frozen in D10 `score_equation_one_pager.md`.)

---

## 5. Mechanism column map (Rung 2.5 / 3)

| Column | Leg | Role in v1 |
|--------|-----|------------|
| `poolq_loo`, `poolq_loo_mean` | Diagnostic of \(L_{\text{net}}\) | Rung 1 axis; mixes B−D in one neighbor statistic |
| `crowding_smooth`, viable-peer counts | **\(D\)** | PD12 congestion measurement |
| `peer_perf_sd_loo` | B−D diagnostic | Distinction vs crowding |
| `minutes` | **\(B\)** proxy (noisy) | Local opportunity |
| `perf`, own \(A_i\) | Outside \(L_{\text{net}}\) | Control / effect modifier |

---

## 6. Cross-domain table (one row per setting)

| Setting | Rung 1 | Rung 2 generative | Rung 2.5 | Rung 3 |
|---------|--------|-------------------|----------|--------|
| **Army** | CIF inverted-U on LOO pool minus mean | None (empirical leg) | Pool size / Λ proxies | Near-threshold; Λ peak-shift |
| **Basketball** | LOO `poolq_loo` inverted-U | Alex score POC (539 preset) | Quality vs `crowding_smooth` | 4D near-threshold |
| **Tenure** | Stage 9 on `poolq_loo_mean` (preliminary) | None | `pool_size_oa_loo` optional | Deferred for v1 |

---

## 7. Explicitly deferred (stop rule)

| Item | Why deferred |
|------|--------------|
| Multiplicative talent production function (Menger/Shockley) | §5 discussion; not v1 mechanism rewrite |
| Full generative \(B(Q) - D(Q)\) decomposition | Not estimated in v1 |
| LOO generative bin-for-bin match | Parallel north star; honest limitation |
| 3-domain parametric identifiability (PD12 P1) | Post-draft |
| Fourth-domain falsification (PD12 P4) | Post-draft |

---

## 8. Intellectual positioning (one paragraph)

**Menger** supplies selective ecology and assortative matching — who gets sorted into elite pools. **Barabási/Wang** supply the ladder from stylized fact to minimal mechanism to new measurements. **Alex (PD10–12)** supplies the operational score and the quality-vs-congestion split. **This project** performs the cross-domain empirical test and names the **development vs competitive constraint** distinction inside elite pools — the inverted-U as a local-competition signature, not a superstar-tail paper.

---

## 9. Artifacts (frozen)

| Artifact | Path |
|----------|------|
| D10 bundle | `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` |
| Axis table | `.../axis_table_generative_readouts.md` |
| Score one-pager | `.../score_equation_one_pager.md` |
| Tenure inference sample | `tenure_pipeline/faculty_panel_inference_v1.csv` |
| Claim discipline | `3-Master_Plan/20260615_1100_VECTOR_claim_language_table.md` |

---

*End Model Nesting Note v1.*
