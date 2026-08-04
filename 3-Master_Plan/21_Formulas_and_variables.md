# Formulas and variables — reader’s companion

**Canonical name:** `21_Formulas_and_variables.md`  
**Purpose:** One place to decode formulas and symbols while reading **`#03`** (and the rest of the stack) **before** **`#05`**. Restates each equation in plain English, defines variables, and notes where it lives in the repo.  
**Not a substitute for:** [`05_Model_Nesting_Note_v1.md`](../5-Manuscript/05_Model_Nesting_Note_v1.md) (canonical theory) · [`01_forward_plan_reading_guide.md`](01_forward_plan_reading_guide.md) (shorthand glossary).  
**Living Q&A:** append misses to [`20_feedback_questions_and_observations.md`](20_feedback_questions_and_observations.md).  
**PDF (you run locally):** `./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/21_Formulas_and_variables.md "" pdf_styles_narrow.css`  
**Compiled:** 2026-06-16 from `#03`–`#07`, `#05`, `#12`, `Alex_model_interpreted.md`, `538_Cell10_Generative_Manual.md`, D10 export templates.

**Quick index:** \(L_{\text{net}}\), B/D → §1 · \(S_i\) score → §2 · `poolq_loo`, congestion → §3 · bins/LPM/logit/\(L^*\) → §4 · Alex regressions → §5 · **`538D`/`538` CELL 10** → §6 · Cox/CIF → §7 · predictions → §8 · axis mismatch → §9 · deferred → §10

**Notation lock (Aug 2026):** **K** = number selected (top-K slots); code `n_selected`. **λ** = congestion weight in **score** only. **K/N** = selectivity rate (characterization default **10%**). Retired: capital **Λ** for slots (old memos).

| If you see… | Start here |
|-------------|------------|
| \(L_{\text{net}}\), B-leg, D-leg | §1 Ontology |
| \(S_i = A_i - \lambda L_C\) | §2 Selection score |
| `poolq_loo`, `crowding_smooth`, LOO | §3 Pool quality & congestion |
| bins → LPM → logit → \(L^*\) | §4 Empirical ladder |
| Draft regressions, mediation | §5 Alex empirical models |
| CELL 10, soft assign, τ, \(T_j\) | §6 Generative simulation (`538D` / `538`) |
| CIF, Cox, tenure hazard | §7 Survival & time-to-event |
| K, near-threshold, predictions | §8 Prediction hooks |
| “axis mismatch” | §9 Axis discipline |

---

## Cross-domain column map (symbols → CSV columns)

| Theory symbol | Plain English | Basketball column | Army column | Tenure column |
|---------------|---------------|-------------------|-------------|---------------|
| \(a_i\), \(A_i\) | Own ability / performance | `perf` (often PPM z within season) | Own talent bucket (TB) / controls | Own publication rate / controls |
| \(\bar{a}_t\) | Team / pool mean quality | `team_mean` (generative); empirical proxy = `poolq_loo` | Pool minus mean construct | Dept context (implicit in LOO) |
| \(L_Q\) | LOO **mean** teammate quality | `poolq_loo` | LOO pool minus mean (`pool_minus_mean` family) | `poolq_loo_mean` |
| \(C_{i,t}\), \(L_{C,\text{LOO}}\) | Viable-peer **congestion** | `crowding_smooth` | Pool size / K (prose hook) | `pool_size_oa_loo` (optional) |
| \(S_i\) | Selection / evaluation score | Generative + score modes in CELL 10 | — (empirical only v1) | — |
| \(Y\) | Advancement outcome | `Y_draft` / draft indicator | Promotion / attrition (competing risks) | `tenure_event` |
| \(K\) | Global slot / board capacity | Draft class size (secondary) | Board size, promotion slots | Tenure lines (prose) |

---

## §1 — Ontology (one model, two readouts)

**1.1 Net local environment — \(L_{\text{net}} = B(\cdot) - D(\cdot)\)**  
**Context:** Master decomposition in VECTOR / COMPASS framing. **Not** the same object as the Alex selection score alone — the score is the **D-leg entering selection**.

\[
L_{\text{net}} = B(\cdot) - D(\cdot)
\]

| Symbol | Meaning |
|--------|---------|
| \(L_{\text{net}}\) | Net effect of the **local peer environment** on advancement propensity (reduced form) |
| \(B(\cdot)\) | **Benefit leg** — visibility, norms, elite exposure, opportunity (e.g. minutes, development upside) |
| \(D(\cdot)\) | **Constraint leg** — competitive congestion, substitutability, finite slots |

**Plain English:** Being around strong peers can **help** (B) and **hurt** (D). The inverted-U is the empirical signature that both operate.  
**Sources:** `#05` §2 · `#03` modeling status · `#04` §2.  
**v1 status:** Conceptual spine — **not** separately estimated as \(B(Q) - D(Q)\) in v1 (deferred).

---

## §2 — Selection score (Alex / Tier 1 generative)

**2.1 Canonical Alex score — \(S_i = A_i - \lambda L_{C,\text{LOO},i}\)**  
**Context:** Minimal **generative** selection rule (`538D` CELL 10). Operationalizes **congestion in who gets picked**, not full \(L_{\text{net}}\).

\[
S_i = A_i - \lambda\, L_{C,\text{LOO},i}
\]

| Symbol | Meaning |
|--------|---------|
| \(S_i\) | Selection / evaluation score for individual \(i\) |
| \(A_i\) | Own latent ability (generative draw; maps to `perf` / `ability` in sim) |
| \(L_{C,\text{LOO},i}\) | Leave-one-out **viable-peer congestion** on \(i\)’s pool |
| \(\lambda\) | Weight on congestion penalty (frozen preset ≈ 0.55 in 539 bundle) |

**Plain English:** Advancement ranking = **how good you are** minus **how crowded your viable peers are**.  
**Repo:** `sports/538D_development.ipynb` CELL 10 · `tier1_cell10_playground_state.json` · D10 `score_equation_one_pager.md`.  
**v1 status:** **Required** generative POC (with ability-only null at \(\lambda=0\)).

**2.2 Congestion score mode (CELL 10) — \(S_i = A_i - w\, L_C\)**  
**Context:** Widget label in CELL 10 when `score_mode = crowding_smooth`. Same idea as §2.1; \(w\) is the UI slider for \(\lambda\).

\[
S_i = A_i - w\, L_C
\]

| Symbol | Meaning |
|--------|---------|
| \(w\) | Congestion weight slider (`loo_gap_weight` in state JSON) |
| \(L_C\) | `crowding_smooth` — LOO mean of smooth viability (see §3.4) |

**Sources:** `538_Cell10_Generative_Manual.md` · `#03` (generative row).

**2.3 LOO-gap blend mode — \(S_i = w(A_i - L_Q) + (1-w)A_i\)**  
**Context:** Alternate CELL 10 score — mixes **gap below pool mean** with raw ability.

\[
S_i = w\,(A_i - L_Q) + (1-w)\, A_i
\]

| Symbol | Meaning |
|--------|---------|
| \(L_Q\) | LOO pool **quality** (mean teammate ability on roster, excluding self) |
| \(w\) | Blend weight toward LOO gap vs pure ability |

**Plain English:** Penalize being **below** your teammates’ average, weighted by \(w\).  
**Repo:** CELL 10 dropdown `loo_gap_plus_ability`.

**2.4 Comparative evaluation (theory prose)**  
**Context:** Alex mechanism #1 — evaluators see you **relative to local peers**.

\[
\text{signal}_i = a_i - f(\text{local peer quality}) + \epsilon_i
\]

| Symbol | Meaning |
|--------|---------|
| \(a_i\) | True ability |
| \(f(\cdot)\) | How much local peer caliber shifts perceived signal |
| \(\epsilon_i\) | Noise |

**Plain English:** Draft odds depend on **standing out**, not raw stats alone.  
**Sources:** `Alex_model_interpreted.md` · PD12 comparative-evaluation notes.

---

## §3 — Pool quality & congestion (measurement)

**3.1 Team mean ability — \(\bar{a}_t = \frac{1}{n_t}\sum_j a_j\)**  
**Context:** Pool **quality** construct; generative readout axis (**pool mean**).

\[
\bar{a}_t = \frac{1}{n_t}\sum_{j=1}^{n_t} a_j
\]

| Symbol | Meaning |
|--------|---------|
| \(\bar{a}_t\) | Mean ability on team / pool \(t\) |
| \(n_t\) | Roster or pool size |
| \(a_j\) | Ability of member \(j\) |

**Empirical proxy (basketball):** `poolq_loo` on LOO axis — **not** identical to \(\bar{a}_t\) (excludes self; different conditioning).  
**Sources:** `Alex_model_interpreted.md` · `#04` §2.5.

**3.2 LOO pool quality — \(L_Q\) → `poolq_loo`**  
**Context:** **Rung 1 empirical x-axis** for basketball (and tenure analog).  
**Definition (basketball):** For player \(i\) on team-season \(t\),

\[
L_{Q,i} = \frac{1}{n_t - 1} \sum_{j \neq i} \text{perf}_j
\]

| Symbol | Meaning |
|--------|---------|
| \(L_{Q,i}\) | Leave-one-out mean teammate performance |
| `perf` | Chosen performance metric (often PPM z within season) |

**Army analog:** LOO senior-rater **pool minus mean** on talent bucket — column family `pool_minus_mean` / `z_pool_minus_mean_snr_fwd`.  
**Tenure analog:** `poolq_loo_mean` — LOO mean dept peer publication intensity.  
**Plain English:** “How good are my **teammates** (without counting me)?”  
**Sources:** `#01` glossary · `#07` claim table · `530` / `538` empirical ladder.

**3.3 Viable-peer congestion (count) — \(C_{i,t}\)**  
**Context:** Alex **crowding** — teammates who **compete for the same scarce slot**, not merely “good teammates.”

\[
C_{i,t} = \frac{1}{n_t - 1} \sum_{j \neq i} \mathbf{1}(a_j > \theta)
\]

| Symbol | Meaning |
|--------|---------|
| \(C_{i,t}\) | Share/count of teammates above viability threshold \(\theta\) |
| \(\theta\) | Prospect threshold (PPM quantile, draft signal, combine, etc.) |
| \(\mathbf{1}(\cdot)\) | Indicator — 1 if viable peer, else 0 |

**Role-specific variant:** \(C_{i,t}^{\text{role}} = \frac{1}{n_t-1}\sum_{j\neq i} w_{ij}\,\mathbf{1}(a_j > \theta)\) with position weights \(w_{ij}\).  
**Sources:** `Alex_model_interpreted.md` §NCAA operationalization.

**3.4 Smooth viability & `crowding_smooth`**  
**Context:** Implemented congestion in CELL 10 / 530 export (539 preset).

\[
v_j = \sigma\bigl(\gamma\,(a_j - \theta)\bigr), \qquad
L_{C,\text{LOO},i} = \frac{1}{n_t - 1} \sum_{j \neq i} v_j
\]

| Symbol | Meaning |
|--------|---------|
| \(v_j\) | Smooth viability of teammate \(j\) |
| \(\sigma(\cdot)\) | Logistic sigmoid |
| \(\gamma\) | Sharpness (preset ≈ 10) |
| \(\theta\) | Viability midpoint (preset ≈ 0.72 on [0,1] scale) |
| \(L_{C,\text{LOO},i}\) | LOO mean viability → column **`crowding_smooth`** |

**Plain English:** Congestion = **how many plausible rivals** sit on your roster, smoothed so counts aren’t brittle.  
**Repo:** `tier1_pool_assignment.py` · `SELECTION_539_*` in `tier1_sim_config.py`.  
**Do not confuse:** `pool_c_loo` (raw LOO **sum**) ≈ \((n-1)\times\) mean at fixed \(n\) — legacy; prefer `crowding_smooth`.

**3.5 Quality vs congestion (Rung 2.5)**  
**Context:** PD12 Priority 3 — theory proposes **two measurements**, not one blended neighbor stat.

| Construct | Symbol / column | Leg | Question it answers |
|-----------|-----------------|-----|---------------------|
| Team quality | `poolq_loo`, \(\bar{a}_t\) | B−D mixed (diagnostic) | “How strong is my peer group?” |
| Congestion | `crowding_smooth`, \(C_{i,t}\) | **D** | “How many rivals for the same slot?” |

**Sources:** `#04` §2.5 · `#05` §5 · `#12` §2.4.

---

## §4 — Empirical inverted-U ladder (basketball / tenure sign-checks)

**4.1 Ventile bins (descriptive)**  
**Context:** **Rung 1** — see the curve before parametric fit.  
**Procedure:** Sort individuals by `poolq_loo` into ventiles (or equal-width bins); plot **mean** draft (or tenure) rate vs bin midpoint.

| Object | Meaning |
|--------|---------|
| Bin midpoint | Mean `poolq_loo` in bin |
| Bin outcome | Mean `Y_draft` or share drafted |

**Repo:** `530_sports_pipeline.ipynb` · `538` CELL 4–6 · `#08` figure list.

**4.2 Linear probability model (LPM)**  
**Context:** **Shape diagnostic** — quadratic curvature for inverted-U.

\[
Y_i = \beta_0 + \beta_1\, L_{Q,i} + \beta_2\, L_{Q,i}^2 + \text{(controls)} + \varepsilon_i
\]

| Symbol | Meaning |
|--------|---------|
| \(Y_i\) | Binary outcome (drafted, tenured, promoted) |
| \(L_{Q,i}\) | `poolq_loo` (or domain analog) |
| \(\beta_2 < 0\) | Concave — inverted-U **if** \(\beta_1 > 0\) at interior |

**Plain English:** OLS on 0/1 — coefficients ≈ **percentage-point** changes; use for **shape**, not final inference.  
**Sources:** `#01` LPM glossary · `#03` empirical ladder row · `538` CELL 5.

**4.3 Logit (proper binary link)**  
**Context:** Same predictors as LPM, logistic link for probabilities in \((0,1)\).

\[
\Pr(Y_i=1) = \text{logit}^{-1}\bigl(\beta_0 + \beta_1 L_{Q,i} + \beta_2 L_{Q,i}^2 + \cdots\bigr)
\]

**Repo:** `538` empirical ladder step after LPM.

**4.4 Peak location — \(L^*\) (L-star)**  
**Context:** Where the **quadratic LPM** predicts maximum expected outcome.

\[
L^* = -\frac{\beta_1}{2\beta_2} \quad (\beta_2 \neq 0)
\]

| Symbol | Meaning |
|--------|---------|
| \(L^*\) | Pool-quality level at predicted peak of inverted-U |

**Plain English:** “At what teammate-quality level does draft probability top out?”  
**Sources:** `#01` · `#03` · `538` CELL 5 (Alex §6 step 2).  
**v1 status:** Beneficial to report all three settings; not all exported yet.

---

## §5 — Alex empirical draft models (mediation & heterogeneity)

**5.1 Baseline draft hazard — quadratic in team quality**

\[
P(\text{draft}_i) = f\bigl(a_i,\, \bar{a}_t,\, \bar{a}_t^2\bigr)
\]

**Predictions:** \(\partial P / \partial a_i > 0\); team quality initially positive; quadratic term captures downturn at elite \(\bar{a}_t\).  
**Sources:** `Alex_model_interpreted.md`.

**5.2 Mechanism regression — add congestion**

\[
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + C_{i,t}
\]

**Plain English:** If \(C_{i,t}\) is negative and **shrinks** the negative quadratic, congestion **mediates** the elite-pool dip.

**5.3 Near-threshold interaction (Prediction #1)**

\[
Y_i \sim a_i + \bar{a}_t + C_{i,t} + a_i \times C_{i,t}
\]

**Plain English:** Congestion hurts most for **borderline** talents (high \(a_i\) but not superstar), not the very best or weak.  
**Repo:** `538D` CELL 4D → `heterogeneity_ventiles_top_tail.png` (`#08`).

**5.4 Assortativity interaction (exploratory)**

\[
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + A_s \cdot \bar{a}_t^2
\]

| Symbol | Meaning |
|--------|---------|
| \(A_s\) | System assortativity (how strongly talent sorts into elite pools) |

**Plain English:** Stronger sorting → stronger right-tail penalty in team quality.

**5.5 Mean × SD peer dispersion (538D 4B/4C — exploratory)**  
**Context:** Downturn may depend on **spread** of talent within pool, not mean alone.  
**Idea:** Interact or joint-model `poolq_loo` with `peer_perf_sd_loo` (LOO SD of teammate `perf`).  
**v1 status:** Exploratory EDA — supplement tier, not closure blocker.

---

## §6 — Generative simulation (CELL 10)

**Repo (this section):** **`sports/538D_development.ipynb` CELL 10** — primary generative lab for v1 closure. Same CELL 10 playground also lives in **`sports/538_alex_tier1_model_and_fit.ipynb`** (empirical + generative in one notebook). Operator manual: `sports/documents/538_Cell10_Generative_Manual.md`. Code: `sports/tier1_cell10_playground_run.py` (widget UI), `sports/tier1_pool_assignment.py` (soft assign), `sports/tier1_generative_eda.py` (Plot B). State file: `sports/tier1_cell10_playground_state.json`. Sort-and-chop null benchmark: **`sports/537_tier1_benchmark.ipynb`** (537 B overlay).

**6.1 Soft assignment kernel**  
**Context:** Realistic **overlapping** pools (not sort-and-chop). Player \(i\) joins team \(j\) with weight:

\[
\tilde{\pi}_{ij} = f(A_i - T_j)\cdot (n_j + k)^\alpha
\]

| Symbol | Meaning |
|--------|---------|
| \(T_j\) | **Fixed** target mean for team \(j\) (drawn once) |
| \(\tau\) | Temperature — scales \((A_i - T_j)\) in kernel |
| \(f\) | Gaussian \(\exp(-(A_i-T_j)^2/(2\tau^2))\) or Cauchy \(1/(1+((A_i-T_j)/\tau)^2)\) |
| \(\alpha\) | Preferential attachment — rich teams attract more players |
| \(n_j\) | Current roster count during sequential placement |

**Plain English:** Players land on teams whose **target level** matches their ability, with noise and overlap.  
**Repo:** `sports/tier1_pool_assignment.py` · `sports/537_tier1_benchmark.ipynb` falsifies disjoint sort-and-chop.

**6.2 Selection rule — top-\(K\)**  
**Context:** After assignment, highest \(S_i\) get `Y_selected = 1` (draft/promotion slots).

| Symbol | Meaning |
|--------|---------|
| \(K\) | `N_SELECTED` — number of advancement slots |
| \(N\) | Total synthetic players (\(J \times\) roster size) |

**Plot B readout:** Mean selection rate vs bins of **x-axis** (see §9).

**6.3 Ability-only null**

\[
S_i = A_i \quad (w = 0,\; \lambda = 0)
\]

**Context:** **Fails** to produce inverted-U alone — required closure check (SCOUT C1).

---

## §7 — Survival & time-to-event (Army, tenure)

**7.1 Cox proportional hazards (generic)**

\[
h_i(t) = h_0(t)\,\exp\bigl(\beta_1 x_{i1} + \beta_2 x_{i2} + \cdots\bigr)
\]

**Context:** Army cause-specific Cox; tenure Layer B (pre-submission).

| Symbol | Meaning |
|--------|---------|
| \(h_i(t)\) | Hazard of event at time \(t\) for person \(i\) |
| \(h_0(t)\) | Baseline hazard |
| \(x_{ik}\) | Covariates (often includes LOO pool quality + **quadratic**) |

**7.2 Alex delay / queueing prediction**

\[
h_i(t) = h_0(t)\exp\bigl(\beta_1 a_i + \beta_2 \bar{a}_t + \beta_3 C_{i,t}\bigr), \quad \beta_3 < 0 \text{ for high } a_i
\]

**Plain English:** Congestion delays advancement, not only binary failure.  
**Army v1:** CIF bar panels on LOO pool-minus-mean bins + cause-specific Cox with quadratics — **not** Fine–Gray in current stack (`#07`).

**7.3 Tenure Cox covariates (planned Layer B)**  
**Typical specification (from PEER correspondence):**

\[
\text{tenure\_hazard} \sim z\_\text{pool\_minus\_mean\_snr\_fwd} + z\_\text{pool\_minus\_mean\_snr\_fwd\_sq} + \text{controls}
\]

| Column | Meaning |
|--------|---------|
| `z_pool_minus_mean_snr_fwd` | Z-scored LOO dept peer quality |
| `..._sq` | Quadratic — inverted-U test |

**v1 status:** Stage 9 **binned** plot on `poolq_loo_mean` is preliminary; Cox not archived for draft.

**7.4 CIF (cumulative incidence)**  
**Context:** Army Cell 11 **descriptive** bar panels — empirical within-bin cumulative incidence, **not** Cox-predicted curves (`#07` guardrail).  
**Plain English:** “Of people in this pool-quality bin, what fraction eventually promoted / attrited?”

---

## §8 — Prediction hooks (variables only)

| Prediction | Formula hook | Key variables |
|------------|--------------|---------------|
| **#1 Near-threshold** | §5.3 interaction | \(a_i \times C_{i,t}\) or ventile slices by own perf |
| **#2 Peak shift with K** | Move \(L^*\) or peak bin with global slots | \(K\) = board size, draft class size, tenure lines |
| Mean × SD dispersion | §5.5 | `peer_perf_sd_loo` × `poolq_loo` |
| Own-TB stratified U (Army) | Stratify CIF/Cox by own talent bucket | Own TB × pool quality |
| Assortativity for U | §6.1 soft assign vs §6.3 null | Overlap + congestion required |

**Sources:** `#03` Predictions section · `#04` §3.

---

## §9 — Axis discipline (mandatory honesty)

**Context:** The #1 source of over-claiming in v1.

| Readout | Typical x-axis | Claim level |
|---------|----------------|-------------|
| Empirical inverted-U (Rung 1) | **LOO pool quality** (`poolq_loo`, `pool_minus_mean`, `poolq_loo_mean`) | Supported / preliminary by domain |
| Generative POC (Rung 2) | **Pool mean** (`team_mean`) | Qualitative peak-and-decline only |
| Same generative score on LOO axis | `poolq_loo` bins | Mostly decreasing — **limitation row** |

**Frozen sentence (paste into manuscript):** see `#05` §4 and `#12` §3.  
**Artifact:** D10 `axis_table_generative_readouts.md` — explicit row-per-quantity table (`#03` “explicit axis table”).

---

## §10 — Explicitly deferred (named so you don’t hunt)

| Formula / object | Why deferred |
|------------------|--------------|
| Full \(B(Q) - D(Q)\) generative decomposition | Not estimated v1 |
| LOO generative bin-for-bin match | Path A — parallel north star only |
| Multiplicative talent production (Menger/Shockley) | Manuscript discussion, not v1 mechanism |
| Fine–Gray subdistribution hazards | Army — revisit pre-publication |
| 3-domain parametric identifiability | Post-draft (PD12 P1) |
| Evans et al. full sim embed | Theory reference only |

**Sources:** `#05` §7 · `#03` Part III defer rows.

---

## Source index (where formulas were gleaned)

| Document | Role |
|----------|------|
| [`03_Where_we_are_now.md`](03_Where_we_are_now.md) | Status + equation-level claim \(S_i\) |
| [`04_Project_story_plain_English.md`](04_Project_story_plain_English.md) | Plain construct map |
| [`05_Model_Nesting_Note_v1.md`](../5-Manuscript/05_Model_Nesting_Note_v1.md) | **Canonical** ontology + column map |
| [`06_Generative_closure_checklist.md`](06_Generative_closure_checklist.md) | What must be true for closure |
| [`07_Claim_language_guardrails.md`](07_Claim_language_guardrails.md) | What you may say per formula readout |
| [`12_Manuscript_staging_prose.md`](../5-Manuscript/12_Manuscript_staging_prose.md) | Ink-ready generative sentence |
| [`Alex_model_interpreted.md`](../sports/documents/Alex_model_interpreted.md) | Full Alex mechanism formulas |
| [`538_Cell10_Generative_Manual.md`](../sports/documents/538_Cell10_Generative_Manual.md) | CELL 10 symbols + score modes |
| `sports/scripts/export_scout_manuscript_bundle_v1.py` | D10 axis table + score one-pager template |

*When you finish `#05`, treat this file as the **fast index**; `#05` remains the frozen nesting authority for manuscript §5.*
