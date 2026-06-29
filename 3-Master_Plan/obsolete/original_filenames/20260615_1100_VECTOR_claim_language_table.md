# VECTOR Claim Language Table

**Date:** 2026-06-15 11:00  
**From:** VECTOR  
**To:** COMPASS, Charles, CODA, SCOUT, PEER  
**Purpose:** Unified manuscript claim-status table and Round 3 VECTOR sign-off.

---

## Status Labels

- **Supported** — evidence currently supports manuscript use with normal caveats.
- **Preliminary** — usable in draft with explicit maturity / limitation language.
- **Unsupported** — do not claim.
- **Defer** — potentially valuable, but not required for v1 manuscript.
- **Out of scope** — not part of the current manuscript architecture.

---

## A. Cross-Cutting Claims

| Claim | Setting | Status | Evidence / caveat |
|---|---|---|---|
| Across multiple domains, advancement outcomes show a nonlinear relationship with leave-one-out peer-pool quality. | Cross-domain | **Supported / Preliminary** | Supported in Army and basketball; preliminary in tenure. Phrase as “observed across Army and basketball, with preliminary evidence in tenure.” |
| The empirical stylized fact is an inverted-U on LOO peer-quality proxies. | Cross-domain | **Supported / Preliminary** | Army and basketball are the mature empirical legs; tenure remains Setting 3 preliminary. |
| The project establishes causal effects of local peer quality on advancement. | Cross-domain | **Unsupported** | Observational analyses; manuscript should avoid causal language. Use “associated with,” “consistent with,” and “suggests.” |
| A talent-only generative baseline is insufficient to reproduce the observed nonlinear story. | Mechanism | **Supported** | SCOUT closure: talent-only / ability-only baseline fails qualitatively relative to the inverted-U stylized fact. |
| A congestion-in-score mechanism can bend advancement curves beyond talent-only selection. | Mechanism | **Supported with caveat** | Supported as a Path II generative proof-of-concept on pool-mean axis, not as bin-for-bin replication of empirical LOO axis. |
| The generative model reproduces the empirical LOO-pool-quality inverted-U bin-for-bin. | Mechanism | **Unsupported** | Explicitly do not claim. Current generative readout differs by conditioning axis. |
| The minimal model is complete enough for v1 manuscript §3 under Path II. | Mechanism | **Supported with caveat** | Complete enough once D10 export bundle freezes axis table, score equation, talent-only contrast, and congestion POC. Not complete as a full LOO-axis generative explanation. |
| The manuscript should follow Wang-style structure: empirical phenomenon → minimal mechanism → predictions. | Manuscript | **Supported** | This is the correct organizing structure for v1. Scaling laws and phase-transition formalism are aspirational, not required. |
| Network science extensions are required for v1 submission. | Manuscript | **Defer** | Exposure/comparison networks, prestige, and talent centers of gravity should be preserved for later, not manuscript-critical now. |

---

## B. Setting 1 — Army / CODA

| Claim | Setting | Status | Evidence / caveat |
|---|---|---|---|
| LOO senior-rater pool quality (“pool minus mean” on TB) and promotion show a non-monotone pattern with elite-tier dip. | Army | **Supported** | Cell 11 CIF bar panels; multiple bin counts tested. |
| Army provides the strongest empirical anchor for the cross-domain story. | Army | **Supported** | Mature descriptive CIF and cause-specific Cox stack. |
| Cause-specific Cox models with quadratic terms and interactions support non-monotone curvature on the hazard scale. | Army | **Supported with run-specific caveat** | Cell 12 results; wording should remain tied to documented run profiles. |
| Cell 11 CIF bars are Cox-predicted curves. | Army | **Unsupported** | They are within-bin empirical summaries, not Cox-predicted curves. |
| Fine–Gray subdistribution hazard regression has been estimated for the Army results. | Army | **Unsupported** | Current stack uses empirical CIF displays + cause-specific Cox. |
| Pool quality has a causal effect on promotion. | Army | **Unsupported** | Observational setting; use associational language. |
| Army pool-size variables literally equal OER board headcount. | Army | **Unsupported until audit** | Pool-size definition requires pre-publication audit. |
| Army requires a generative simulation matching its LOO pool axis for v1. | Army | **Out of scope** | Army is the empirical anchor under Path II; basketball supplies minimal generative POC. |
| Promotion and attrition should be described as simultaneous career processes. | Army | **Supported** | Competing-risks framing is core to the Army layer. |

---

## C. Setting 2 — Basketball / SCOUT

| Claim | Setting | Status | Evidence / caveat |
|---|---|---|---|
| LOO teammate pool quality (`poolq_loo`) and NBA draft rate show an inverted-U with elite-tier dip. | Basketball | **Supported** | 530 / 538 empirical ladder and ventile exports. |
| Basketball provides the cleanest empirical replication of the Army stylized fact. | Basketball | **Supported** | Draft outcome and team-season pool quality provide a strong Setting 2 replication. |
| Talent-only generative selection fails to reproduce the nonlinear pattern. | Basketball / Mechanism | **Supported** | 538D CELL 10; export pending D10. |
| Congestion-in-score generates peak-and-decline behavior on whole-roster pool mean. | Basketball / Mechanism | **Supported with caveat** | Path II POC; must state axis difference. |
| The generative POC reproduces the empirical `poolq_loo` inverted-U. | Basketball / Mechanism | **Unsupported** | Do not claim. Current LOO-axis generative readout is not the manuscript claim. |
| Near-threshold heterogeneity is a primary prediction candidate. | Basketball / Prediction | **Supported** | CELL 4D exports; best current prediction-facing basketball artifact. |
| Peak shift with global Λ is already demonstrated in basketball generative simulations. | Basketball / Prediction | **Unsupported / Defer** | Treat Λ as cross-domain / Army-led hook unless new SCOUT export is built. |
| Basketball time-to-draft Cox modeling is required for v1. | Basketball | **Out of scope** | V1 uses binned draft rates and Wang ladder, not survival modeling. |
| Mean × dispersion interactions are required for v1. | Basketball / Prediction | **Defer** | Potential supplement / later mechanism diagnostic, not primary prediction. |

---

## D. Setting 3 — Tenure / PEER

| Claim | Setting | Status | Evidence / caveat |
|---|---|---|---|
| LOO department peer quality (`poolq_loo_mean`) and tenure show a non-monotone pattern with elite-tier dip. | Tenure | **Preliminary** | Stage 9 binned results; unconditional, noisy, and not yet Cox-validated. |
| Tenure provides a mature third empirical replication equal to Army and basketball. | Tenure | **Unsupported** | Must be described as preliminary Setting 3. |
| Tenure provides a plausible third empirical setting that stress-tests generality. | Tenure | **Supported with caveat** | Use as preliminary third panel with limitations. |
| 168 R1 CS departments are in the panel roster. | Tenure | **Supported** | PEER reports roster coverage. |
| All 168 departments are inference-ready. | Tenure | **Unsupported** | Inference-ready subset is much smaller because LOO pool computation and linkage are limiting. |
| Formal Cox hazard-ratio evidence exists for tenure pool-quality curvature. | Tenure | **Unsupported until Layer B run** | 540 currently ends at Cell 9; Layer B planned before submission. |
| Fine–Gray tenure models are required for the draft. | Tenure | **Defer** | Cause-specific / basic Cox before submission is enough unless elevated. |
| Attrition cleanly distinguishes leaving academia from lateral moves. | Tenure | **Unsupported** | Single-institution panel limitation; lateral moves may appear as attrition. |
| Tenure requires its own generative simulation for v1 model closure. | Tenure | **Out of scope** | Tenure is an empirical leg under Path II, not a generative leg. |

---

## E. Predictions

| Claim | Setting | Status | Evidence / caveat |
|---|---|---|---|
| Prediction #1: elite-pool dip should be strongest for near-threshold / borderline performers. | Cross-domain | **Supported as primary v1 prediction** | Strongest current prediction; SCOUT has basketball artifact, Army may support analogous test. |
| Near-threshold heterogeneity is already fully validated across all three settings. | Cross-domain | **Unsupported** | Treat as testable prediction / partially supported, not fully validated triad result. |
| Prediction #2: peak location should shift with global distinction capacity Λ. | Cross-domain | **Supported as conceptual primary prediction** | Strong manuscript idea; current empirical anchoring is more conceptual / Army-led than fully exported. |
| Peak shift with Λ is already empirically demonstrated across settings. | Cross-domain | **Unsupported** | Do not claim until specific analyses exist. |
| Mean × dispersion interactions are a primary v1 prediction. | Basketball / Cross-domain | **Defer** | Potentially useful later; not primary for current manuscript. |
| Prediction story is required for Wang-style manuscript strength. | Manuscript | **Supported** | Should be present even if one prediction is currently framed as test-ready rather than fully validated. |

---

## F. Required Manuscript Claim Discipline

| Do Say | Do Not Say |
|---|---|
| “We observe a replicated nonlinear association between LOO peer-pool quality and advancement in Army and basketball, with preliminary evidence in tenure.” | “We prove peer quality causes advancement outcomes.” |
| “A congestion penalty in the selection score can produce non-monotone advancement curves on a pool-mean readout.” | “The generative model reproduces the empirical LOO-pool-quality inverted-U.” |
| “The minimal generative model supports the constraint leg of the theory.” | “538D implements the full B(Q)−D(Q) decomposition.” |
| “Tenure is a preliminary third setting with honest limitations.” | “Tenure is equally mature evidence.” |
| “Near-threshold heterogeneity and Λ peak-shift are the primary prediction directions.” | “All predictions are already fully validated across all settings.” |

---

## G. Mutual Understanding Sign-Off

| # | Question | VECTOR Answer |
|---|---|---|
| **M1** | Accept SCOUT Tier 2 closure rule? | **Yes, with caveat:** Tier 2 is complete enough for v1 once D10 freezes exports; it is not a full LOO-axis generative explanation. |
| **M2** | Accept Path II architecture? | **Yes.** Basketball generative POC; Army and tenure empirical legs. |
| **M3** | Accept SCOUT §6 ink rules? | **Yes.** Ready / caveat / do-not-ink distinctions are correct. |
| **M4** | Any unresolved scientific disagreement with CODA, PEER, or SCOUT? | **No.** I see no scientific conflict; remaining issues are claim discipline, exports, and Charles locks. |
| **M5** | After filing this table, is VECTOR waiting on Charles? | **Yes.** VECTOR is waiting on Charles / COMPASS routing for next manuscript artifact, plus SCOUT D10 bundle when Charles gives go. |

---

## H. VECTOR Bottom Line

VECTOR accepts the current consensus.

The manuscript should proceed under Path II:

1. Empirical triad as Rung 1.
2. Basketball generative POC as Rung 2.
3. Near-threshold heterogeneity + Λ peak shift as Rung 3 prediction story.
4. Strong limitations language around axis mismatch, tenure maturity, and causal inference.

The central task now is not to reopen the model architecture. The central task is to turn this consensus into manuscript prose.
