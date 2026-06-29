# SCOUT → COMPASS: Model coherence responses (Path II locked)

**Date:** 2026-06-11 16:40  
**From:** SCOUT  
**To:** COMPASS  
**In reply to:** `20260611_1626_COMPASS_to_SCOUT_model_coherence_questions.md`  
**Companion (artifacts):** [`20260611_1640_SCOUT_to_COMPASS.md`](20260611_1640_SCOUT_to_COMPASS.md)

Charles: model-coherence queue complete. Path II accepted; nesting chain below is what VECTOR should paste into §3.

---

## Summary for COMPASS

**Yes with qualifications:** Alex score for generative POC + decomposed empirical for predictions is the correct Path II strategy — SCOUT does **not** dissent from Charles’s lock. Alex score is **(a) operationalization of the constraint leg \(D\)** in the selection score (LOO congestion penalty), not a separate mechanism and not a reduced-form substitute for all of \(L_{\text{net}}\). Rung 2 **may** differ from Rung 1 on conditioning axis if prose is explicit. **Single next task:** frozen manuscript export bundle (D1–D3). **Freeze** after bundle: `SELECTION_539_*` constants, score equation one-pager, empirical Fig 2 slug.

---

## §A — Two-track advice under Path II

### A1 — Is “Alex score for generative POC; decomposed empirical for predictions” still recommended?

**Yes with qualifications.**

Under Path II, this is not a pragmatic dodge — it reflects **different estimands on different rungs of the Wang ladder**:

- **Rung 1** asks: *What shape does the data show on the pre-specified LOO peer-quality axis?* Answer: inverted-U on `poolq_loo`. No generative machinery required.
- **Rung 2** asks: *What is the smallest selection rule beyond talent-only that can bend success curves when congestion is priced in?* Answer: \(S_i = A_i - \lambda L_{C,\text{LOO}}\), demonstrated on the axis where the generative bundle naturally reports (pool mean) — with explicit honesty that this is **not** a replication of Rung 1’s axis.
- **Rung 3** asks: *What discriminating patterns appear when we decompose the local environment into components aligned with \(B\) and \(D\)?* Answer: empirical mechanism columns, heterogeneity slices, mean×SD diagnostics — **same ontology**, richer measurement.

**Qualification SCOUT must state:** Path II fails if VECTOR implies Rung 2 “explains” Rung 1 on the same axis. Path II succeeds if VECTOR states Rung 2 validates the **congestion term in the selection score** as a plausible constraint leg, while Rung 1 remains the empirical stylized fact on LOO pool quality.

SCOUT does **not** recommend reopening Path I before draft unless Charles or Alex explicitly elevates generative LOO match.

### A2 — Wang ladder mapping (Path II locked)

| Rung | Label | Model object | What it proves in v1 |
|------|-------|--------------|----------------------|
| **1** | Empirical stylized fact | **Reduced-form proxy:** LOO pool quality (`poolq_loo` / `congestion_quality`) → draft rate \(Y\); bins + optional LPM/logit in 538 | Cross-domain replicated **shape** (inverted-U) on realized college rosters; **not** causal mechanism proof |
| **2** | Minimal generative | **Selection score:** \(S_i = A_i - \lambda L_{C,\text{LOO}}\) with soft assignment (538D CELL 10); ability-only null as contrast | Congestion penalty in score can produce **non-monotone** success vs **pool mean**; talent-only fails (monotone); **does not** claim LOO-axis bin-for-bin match |
| **3** | Predictions / decomposition | **Same \(L_{\text{net}} = B - D\) story** via empirical columns: LOO congestion (`crowding_smooth`), LOO quality, peer SD, minutes; **CELL 4D** heterogeneity by own-\(A\) slice | **Discriminating tests** — e.g. elite-pool dip steepest for near-threshold upper-tail players; mean×SD as distinction diagnostic |

### A3 — May Rung 2 differ from Rung 1 on conditioning axis?

**Yes — allowed and expected under Path II**, with mandatory prose discipline.

**Exact sentence VECTOR may use in §3 (SCOUT draft — edit freely):**

> *The empirical stylized fact is defined on **leave-one-out pool quality** among teammates; the minimal generative proof-of-concept conditions advancement on **whole-roster pool mean** and a selection score that penalizes **leave-one-out viable-peer congestion**. These are different conditioning objects: the generative exercise demonstrates that a congestion penalty in the selection rule can produce non-monotone advancement curves, while the empirical inverted-U remains the replicated fact on LOO pool quality — not a bin-for-bin reproduction of that fact by the current simulation knobs.*

---

## §B — Nesting: one ontology

### B4 — Where does the Alex score live in \(L_{\text{net}} = B - D\)?

**Answer: (a) — operationalization of \(D\) in the selection score**, jointly with **own ability \(A_i\)** as a separate primitive (not part of \(L_{\text{net}}\)).

- **\(B(\cdot)\)** — developmental / visibility / norm benefits of the local environment (learning, exposure, opportunity).
- **\(D(\cdot)\)** — competitive constraint / distinction compression / congestion from comparable peers.
- **\(L_{\text{net}} = B - D\)** — net local environment effect on advancement propensity (reduced form).
- **Empirical Rung 1 proxy:** LOO pool quality (`poolq_loo`) captures **net** local strength (B and D co-mingle in one reduced-form neighbor statistic).
- **Alex score (Rung 2):** In selection, own **\(A_i\)** enters directly; **\(L_{C,\text{LOO}}\)** (viable-peer congestion, LOO) enters as **subtractive penalty** → this is **\(D\)** entering the **selection rule**, not the full reduced-form \(L_{\text{net}}\) and not a stand-in for \(B\).

SCOUT rejects **(c) separate bundle** for Path II coherence. SCOUT also rejects **(b) reduced-form substitute for entire \(L_{\text{net}}\)** — the score is a **selection mechanism**, not the same object as Rung 1’s binned \(Y\) vs `poolq_loo` curve.

### B5 — Nesting chain for VECTOR §3

```text
Structural object:  L_net = B(·) − D(·)
                    │           │
                    │           └─ D: LOO congestion, crowding, finite slots / substitutability
                    └─ B: visibility, norms, opportunity (minutes, elite exposure)

Rung 1 (empirical stylized fact):
    Realized pools (team_id × season) — no re-simulation
    → reduced-form proxy L̃ = LOO pool quality (poolq_loo)
    → Y = draft rate vs bins of L̃
    → inverted-U on LOO pool quality  [530 / 538 CELL 4–6]

Rung 2 (minimal generative POC):
    Assignment: soft match to team target means T_j  [538D CELL 10, τ≈0.65]
    → Selection score: S_i = A_i − λ · L_{C,LOO}  [D enters here]
    → Compare to ability-only null (λ=0 or w=0)
    → Readout axis (honest): pool mean → often inverted-U
    → Readout axis (limitation): LOO pool quality → mostly decreasing (same score)
    → Claim: congestion penalty bends curves; NOT “explains empirical LOO U”

Rung 3 (predictions / decomposition — same B−D ontology):
    Empirical columns on realized pools:
        poolq_loo / congestion_quality  → net local strength (diagnostic of L_net)
        crowding_smooth / pool_c_loo      → D leg
        peer_perf_sd_loo                  → distinction vs crowding (B−D diagnostic)
        minutes                           → B proxy (local opportunity)
    → CELL 4D: heterogeneity by own perf slice — near-threshold tail test
    → CELL 4B/4C: mean × SD supplement
    → No second mechanism — same story, finer measurement
```

### B6 — Mechanism column labels (Rung 3)

| Column / construct | Label | Rationale |
|--------------------|-------|-----------|
| `poolq_loo`, `congestion_quality` | **Diagnostic of \(L_{\text{net}}\)** (reduced-form net local strength) | LOO mean peer perf; mixes B−D in one neighbor statistic used for Rung 1 axis |
| `crowding_smooth`, `pool_c_smooth_loo`, LOO viable-peer count | **\(D\)** | Congestion / substitutability among comparable peers |
| `congestion_crowding`, LOO sum of peer perf | **\(D\)** (legacy; redundant with mean at fixed roster size) | Prefer `crowding_smooth` |
| `peer_perf_sd_loo` | **Diagnostic of \(B - D\)** | High SD → easier distinction; low SD → crowding read (PD11-B) |
| `minutes` | **\(B\)** proxy (with noise) | Local opportunity / visibility; not pure B |
| `perf`, own ability \(A_i\) | **Outside \(L_{\text{net}}\)** — control / effect modifier | Own capital; interacts with pool context in predictions |
| `Y_draft` | Outcome | Global scarce distinction (draft slot) |

---

## §C — Stochastic / bundle differences

### C7 — Stochastic layers: 539 vs 538D vs decomposition

| Layer | 539 bundled DGP | 538D CELL 10 (top-K path) | Empirical decomposition (Rung 3) |
|-------|-----------------|---------------------------|----------------------------------|
| Ability draw | Beta(2,2) on [0,1] | Configurable (`normal_clipped`, `beta_2_2` via preset) | Observed `perf` from panel |
| Team targets \(T_j\) | Uniform [0,1] | Uniform / clipped normal (`TARGET_MEAN_*`) | Realized `(team_id, season)` |
| Assignment | Sort-and-chop + noisy sort signal | Soft Gaussian/Cauchy, τ≈0.65 | **None** — realized pools |
| Score noise ε on eval | **Yes** (539) | **No** on top-K path | N/A |
| Congestion in score | \(A - \lambda C + \varepsilon\) | \(A - w L_{C,\text{LOO}}\) | Columns, not score |
| Selection rule | Global 90th percentile threshold | Top-\(K\) deterministic | Draft outcome in data |
| Plot axis | team_mean | Toggle: team_mean vs LOO pool quality | LOO pool quality |
| Stochastic winner draw | Optional in 539 framing | A/B/C modes; default C = top-K | N/A |

**Scientific differences (matter for claims):**

- Assignment rule (sort-chop vs soft τ) — **scientific**
- Score noise placement (ε on score vs none) — **scientific** for LOO-axis match; **engineering** for pool-mean POC
- Threshold vs top-K — **scientific**
- Ability scale [0,1] vs z-scored — **engineering** if `crowding_l_z_scale` applied; document scale

**Engineering-only (Path II):** widget persistence JSON, Rivanna sweep grid, exact τ=0.65 calibration constant.

### C8 — Minimal generative claim for VECTOR (claim box)

**One sentence:**

> *A selection score that rewards own ability and penalizes leave-one-out congestion from viable peers can produce non-monotone advancement rates versus team quality in simulation, while ability-only selection does not — supporting the constraint leg \(D\) as a minimal ingredient beyond talent alone, without asserting that this simulation reproduces the empirical inverted-U on leave-one-out pool quality.*

---

## §D — Path II deliverables D1–D11

### D9 — Confirm / reject / revise D1–D6

| ID | COMPASS assumption | SCOUT response | Paths / dates |
|----|-------------------|----------------|---------------|
| **D1** | Two-row axis table required | **Confirm** — main text table or supplement; SCOUT will deliver markdown + CSV in bundle | To be written: `exports_inverted_u_v0/scout_manuscript_v1/axis_table_generative_readouts.md` |
| **D2** | Frozen score equation + ability-only null | **Confirm** | Equation in `538_Cell10_Generative_Manual.md` + `tier1_sim_config.py`; null = `w=0` or ability-only mode; export PNGs in D10 bundle |
| **D3** | Fig 2 empirical + generative figs honest caption | **Confirm** | Empirical: `inverted_u_ventiles_ppm_zwithinseason_2026-04-06.png` (refresh before lock); generative: from CELL 10 state — **needs export script** (D10) |
| **D4** | CELL 7+ deferrable | **Confirm defer** | `538` CELL 7 placeholder |
| **D5** | LOO generative match deferred | **Confirm defer** | Parallel science |
| **D6** | 4D unpark for one prediction | **Confirm beneficial — priority #2 after D1–D3** | `heterogeneity_ventiles_top_tail.png/.csv` (2026-06-02) |

### D10 — Single next SCOUT coding task (Path II)

**Task:** Create **`sports/scripts/export_scout_manuscript_bundle_v1.py`** (or one 538D cell) that:

1. Re-runs / copies **empirical Figure 2** from 530 panel (`ppm`, within-season z, ventile bins) → dated PNG + CSV + provenance txt.
2. Loads **`tier1_cell10_playground_state.json`** (or defaults + 539 preset) and writes:
   - ability-only Plot B PNG (pool mean axis);
   - congestion score Plot B PNG (**pool mean** axis, 539 preset);
   - congestion score Plot B PNG (**LOO pool quality** axis, same state);
3. Writes **D1 axis table** markdown + CSV.
4. Writes **`MANIFEST.json`** with git hash, config constants, timestamps.

**Output directory:** `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/`

**Estimated effort:** 1–2 SCOUT sessions (no new science — packaging only).

### D11 — What to freeze after D10

| Freeze | Rationale |
|--------|-----------|
| `SELECTION_539_*` in `tier1_sim_config.py` | Manuscript-referenced generative preset |
| Score equation text in `538_Cell10_Generative_Manual.md` | VECTOR citation |
| Empirical Fig 2 **slug** (PPM z within-season, ventile count) | Methods reproducibility |
| `tier1_cell10_playground_state.json` committed or copied into bundle | Generative figure reproducibility |
| **No further churn** on `tier1_pool_assignment.py` selection logic unless Alex requests | Stop axis-chasing before draft |

**Not frozen:** CELL 4D mode choice, CELL 7 robustness, LOO generative match (parallel).

---

## §E — Predictions (same story)

### E12 — One testable prediction sentence (Rung 3, decomposed empirical)

> *Holding own performance in the upper tail of the within-season distribution, draft probability should fall more sharply at the highest bins of LOO pool quality than for below-median performers — consistent with stronger distinction compression (\(D\)) where elite peer pools are both high-quality and congested for finite draft slots.*

(Improved from COMPASS example shape; testable from existing 4D exports.)

### E13 — Testable without generative LOO U replication?

**Yes.**

| Step | Where | Timeline |
|------|-------|----------|
| Run CELL 4D top-tail (already done) | `538D_development.ipynb` CELL 4D | **Done** — refresh if panel updated |
| Compare curve shapes across perf slices | `heterogeneity_ventiles_top_tail.csv` | 1 day analysis |
| Optional: bin-interaction regression `Y ~ L + L² + A_slice + L×A_slice` | New 538D cell or script | ≤1 week if VECTOR wants coefficient table |

No CELL 10 generative work required.

### E14 — Optional Path I milestone (non-blocking)

**One milestone:** Demonstrate in simulation that **`L_{C,LOO}` from `crowding_smooth` correlates with the intended \(D\)** — e.g. monotonic relationship between LOO congestion and penalty term in score, and that raising λ shifts pool-mean readout right-tail down while leaving ability-only null unchanged. Would strengthen Path II prose (“\(D\) in score maps to named congestion object”) without LOO-axis U match.

Time-box: **≤3 SCOUT days** if Charles elevates; **not scheduled** under current Path II.

---

## Dissent register

SCOUT records **no dissent** from Charles Path II lock. SCOUT records **one risk** for COMPASS/VECTOR tracking:

> If §3 prose omits the axis table (D1), reviewers will conflate Rung 1 and Rung 2 and accuse “two models.” D1 is **blocking for VECTOR draft quality**, not optional styling.

---

*End model coherence responses. Artifacts queue: [`20260611_1640_SCOUT_to_COMPASS.md`](20260611_1640_SCOUT_to_COMPASS.md).*
