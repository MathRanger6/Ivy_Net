# COMPASS → VECTOR: MLE, Bernoulli calibration, and SELECT rules

**Filename note:** Requested as `COPMASS_to_SVector_MEL_Bernoulli_response`; stored with standard spelling.

**Generated:** 2026-10-05  
**Audience:** Charles Levine (Chapter 4 drafting); VECTOR / COMPASS handoff  
**Scope:** Repo-verified reconstruction only — canonical stochastic SELECT, PD21 likelihood, fitted parameters, and what remains unresolved.  
**Chapter targets:** §4.5.3 (stochastic selection equation); §4.8 opening (MLE / fitting bridge).

**Live Chapter 4 prose (Charles, 2026-10-05):** [`Model_Chapter_First_Draft.docx`](Model_Chapter_First_Draft.docx) · PDF export: [`Model_Chapter_First_Draft.pdf`](Model_Chapter_First_Draft.pdf) (`new_VECTOR_work/`). **Draft vs repo review (2026-10-05):** [`COMPASS_to_VECTOR_Model_Chapter_First_Draft_review.md`](COMPASS_to_VECTOR_Model_Chapter_First_Draft_review.md) — upload to SVector with this memo if the agent lacks repo access. Outline companion: [`VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md`](VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md).

**Binding reminder:** Score ≠ select; Hero ≠ scoring equation. See [`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md).

---

## Executive summary

There is **no single undifferentiated “the SELECT rule”** in the repo. **Fitting (PD21)**, **generative simulation**, and **recent mechanism experiments** use different objects:

| Layer | Rule |
|-------|------|
| **MLE / calibration** | Season softmax → **independent Bernoulli** on \(Y_i\) (not exact-\(K\) generative SELECT) |
| **Long-run generative v1 (BINDING + most sweeps)** | **Deterministic top-\(K\)** on \(S_i\) (code rule **C**) |
| **Documented stochastic generative upgrade (MBB replay, Aug 28 lock)** | **Gibbs: \(K\) draws without replacement** on \(\exp(S_i/t_{\mathrm{Gibbs}})\) (code rule **D**) |

**Do not** treat Bernoulli-fitted \((\lambda,\gamma,t_{\mathrm{MLE}})\) as automatically valid under Gibbs or top-\(K\) SELECT without refit or an explicit approximation argument ([`VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md`](VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md) §4.5).

---

## 1. Canonical stochastic SELECT “going forward”

### What the repo actually documents

| Layer | Rule | Primary sources |
|-------|------|-----------------|
| **Binding / generative v1** | **Deterministic top-\(K\)** by score (rule **C**) | [`BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md); [`3-Master_Plan/re_entry/LG_model_desk_reference.md`](../../re_entry/LG_model_desk_reference.md) Part VI; [`COMPASS_Dissertation_Core_Deck_Materials_Questionnaire_COMPASS_draft.md`](../COMPASS_Dissertation_Core_Deck_Materials_Questionnaire_COMPASS_draft.md) §7.4 (“v1: top K”; “stochastic select = future step only”) |
| **MBB empirical-roster replay (Charles lock, 2026-08-28)** | **Gibbs \(K\)-draw without replacement** (rule **D**) | [`3-Master_Plan/re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md`](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md); [`sports/tier1_pool_assignment.py`](../../../sports/tier1_pool_assignment.py) `choose_selected` |
| **Fitting (not generative SELECT)** | **Independent Bernoulli** on season softmax \(p_i\) | [`sports/scripts/pd21_draft_bernoulli_mle.py`](../../../sports/scripts/pd21_draft_bernoulli_mle.py) |

Rules **A** (proportional \(K\)-sample) and **B** (Bernoulli-ish independent coins) exist in code as older paths; they are **not** stated generative defaults ([`tier1_pool_assignment.py`](../../../sports/tier1_pool_assignment.py) docstring on `choose_selected`).

### Manuscript guidance (PD44, 2026-09-30)

[`VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md`](VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md) §4.5:

- Teach **deterministic top-\(K\)** and **stochastic** selection separately.
- **Bernoulli calibration** and **exact-\(K\) without replacement** are **different probability models**.
- **Final stochastic equations require implementation verification** before chapter prose treats them as fully settled.

### Drafting verdict for §4.5.3

- **Architecture default:** deterministic top-\(K\) on \(S_i\).
- **Stochastic generative story (Aug 28 memo):** **exact-\(K\) Gibbs (rule D)**, not independent Bernoulli replay.
- **Bernoulli:** **calibration likelihood only**, not the generative SELECT law.

---

## 2. Probability formulas (scores and temperature)

### 2.1 SCORE (generative sim — Alex v1)

Binding score for ranking / SELECT weights in sim:

\[
S_i = A_i - \lambda L^C_i
\]

Code: [`selection_weights`](../../../sports/tier1_pool_assignment.py) with `score_mode="loo_gap_plus_ability"`.

### 2.2 Deterministic SELECT (rule C)

\[
Y_i = \mathbf{1}\{\, S_i \text{ is among the top } K \text{ scores (documented tie rule)} \,\}
\]

Implementation: `choose_selected(..., choice="C")` in [`tier1_pool_assignment.py`](../../../sports/tier1_pool_assignment.py).

PD44 deterministic form (season/pool scope as in each run):

\[
Y_i=\mathbf{1}\{i\text{ is among the }K\text{ highest scores}\},\qquad q=K/N,
\]

with a documented tie rule ([`VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md`](VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md) §4.5).

### 2.3 Stochastic SELECT — Gibbs exact-\(K\) (rule D)

From [`grandchild_temperature_select_sweep.py`](../../../sports/scripts/grandchild_temperature_select_sweep.py) and [`MBB_empirical_roster_select_replay.md`](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md):

\[
S_i = A_i - \lambda L^C_i, \qquad
w_i = \exp(S_i / t_{\mathrm{Gibbs}}),
\]

then draw **exactly \(K\)** distinct players **without replacement** with probabilities proportional to \(w_i\) (weighted sampling; code uses `rng.choice(..., replace=False, p=w/\sum w)`).

Very small \(t_{\mathrm{Gibbs}}\) collapses to top-\(K\) (`GIBBS_T_MIN` in [`tier1_pool_assignment.py`](../../../sports/tier1_pool_assignment.py)).

### 2.4 PD21 board, softmax, Bernoulli likelihood (fit only)

**Board logits (PD21 lock — not \((A-\lambda L^C)/t\)):**

\[
\eta_i = \frac{A_i}{t_{\mathrm{MLE}}} - \lambda L^C_i
\]

**Within-season softmax:**

\[
p_i = \frac{\exp(\eta_i)}{\sum_{k \in \text{season}} \exp(\eta_k)}, \quad \sum_i p_i = 1
\]

**Bernoulli log-likelihood (independent trials):**

\[
\ell(\lambda,\gamma,t_{\mathrm{MLE}}) = \sum_i \Big[ Y_i \log p_i + (1-Y_i)\log(1-p_i) \Big]
\]

**\(K\) is not in \(\ell\)** — see docstring in [`pd21_draft_bernoulli_mle.py`](../../../sports/scripts/pd21_draft_bernoulli_mle.py) (lines 7–13) and saved JSON `likelihood` field.

### 2.5 Two temperatures (do not conflate)

| | **\(t_{\mathrm{MLE}}\)** (PD21) | **\(t_{\mathrm{Gibbs}}\)** (PD20 SELECT) |
|---|--------------------------------|------------------------------------------|
| **Where** | In \(\eta_i = A_i/t - \lambda L^C\) before softmax | In \(\exp(S_i/t)\) at SELECT |
| **Fitted?** | Yes (jointly with \(\lambda,\gamma\) or with fixed \(\gamma\)) | No — swept on a grid |
| **Role** | Sharpens spread of \(p_i\) from ability in the **fit** | Lottery noise **after** scores exist in **sim** |

Source: [`MBB_empirical_roster_select_replay.md`](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md) (“two temperatures” table).

---

## 3. What MLE actually optimized (code-exact)

**Script:** [`sports/scripts/pd21_draft_bernoulli_mle.py`](../../../sports/scripts/pd21_draft_bernoulli_mle.py)

**Setup:**

- **Fixed empirical rosters** — no ASSIGN, no SELECT step inside the fit.
- Player-level \(L^C\) via `attach_player_level_lc` → `tpa.add_team_pool_columns` with:
  - **`viability_sharpness = γ`** (estimated or fixed),
  - **`viability_theta = θ_s`** from [`_season_k_theta`](../../../sports/scripts/grandchild_selection_inverted_u_diagnostic.py) each season: quantile \(1 - K_s/N_s\).

**Optimization (default):** joint L-BFGS-B on **\((\lambda, \gamma, t_{\mathrm{MLE}})\)**. Optional `--gamma` fixes γ and fits **\((\lambda, t)\)** only.

**Panel log-likelihood:** sum over seasons of Bernoulli terms using `board_logits` → `softmax_probs` → `bernoulli_loglik` ([`panel_loglik`](../../../sports/scripts/pd21_draft_bernoulli_mle.py)).

**Not estimated in PD21:**

| Parameter | Treatment |
|-----------|-----------|
| **ρ** | Absent (fixed rosters; no homophily in fit) |
| **θ** | Preset per season from \(K/N\), not a free MLE parameter |
| **\(K\)** | Enters via which rows have \(Y=1\) and via θ construction; **not** in likelihood formula |

**Diagnostic only:** `topk_overlap` — overlap between top-\(K_s\) by \(p_i\) and actual draftees; **not** the likelihood.

Further narrative: [`3-Master_Plan/MLE/MLE_fit_explainer.md`](../../MLE/MLE_fit_explainer.md), [`3-Master_Plan/MLE/MLE_basics.md`](../../MLE/MLE_basics.md).

---

## 4. Saved estimates for \(\gamma\), \(\lambda\), \(t\)

**Window and γ treatment matter** — report the artifact that matches the chapter table.

| Artifact | Window | Fit mode | **γ** | **λ** | **\(t_{\mathrm{MLE}}\)** |
|----------|--------|----------|-------|-------|---------------------------|
| [`REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json`](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json) | 2009–2021 | `joint_3param` | **19.57** | **1.30** | **1.07** |
| [`PD21_draft_bernoulli_mle_2013_2021.json`](../../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json) | 2013–2021 | `fixed_gamma_2param`, γ=18 | **18** (fixed) | **2.57** | **1.07** |

**θ:** per-season preset, not MLE’d in PD21.

**ρ:** separate assign calibration (not in PD21); e.g. reigning ρ bracket artifacts under `sports_sandbox/reigning_hero/calibration/rho/`.

**\(t_{\mathrm{Gibbs}}\):** chosen by PD20 temperature sweep ([`grandchild_temperature_select_sweep.py`](../../../sports/scripts/grandchild_temperature_select_sweep.py)); MBB memo suggests starting **\(t_{\mathrm{Gibbs}} = 1\)** for replay — **not** identified as equal to **\(t^*_{\mathrm{MLE}} \approx 1.07\)**.

---

## 5. Refit under exact-\(K\) selection?

**No completed decision or run** to refit \((\lambda,\gamma,t)\) under a K-draw / Plackett–Luce likelihood matching rule D.

Documented positions:

- [`MLE_fit_explainer.md`](../../MLE/MLE_fit_explainer.md): K-draw likelihood is a **different model — not what we ran**; sim may use K-draw **after** Bernoulli fit with the **same** point estimates — **different rule, not re-optimization**.
- [`MLE_basics.md`](../../MLE/MLE_basics.md) Part 10: K-draw likelihood **proposed**; empirical v1 **Bernoulli only**.
- [`PD20_softmax_K_winners_explainer.md`](../../Alex_stuff/PD20_softmax_K_winners_explainer.md): MLE on K-draw vs Bernoulli-softmax **not** declared equivalent.
- [`ASSORT_20260927_empirical_selection_replay_v1_scope.md`](assort_analysis/docs/decisions/ASSORT_20260927_empirical_selection_replay_v1_scope.md): **transport** \(\gamma^*,\lambda^*,t^*\); **no refit**; deterministic top-\(K\) diagnostic only.
- SCOUT [`ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md`](assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md): do not expand into refit sweeps without new authorization.

**PD44:** do not call calibrated parameters **transferable** until equivalence or an explicitly justified approximation is established.

---

## 6. Three-way split (implemented vs manuscript vs open)

### A. Implemented and fit

| Piece | Status |
|-------|--------|
| **PD21 MLE** | Bernoulli × season softmax on \(\eta_i = A_i/t - \lambda L^C\); joint \((\lambda,\gamma,t)\) or fixed-γ \((\lambda,t)\); θ per season preset |
| **Generative SELECT in code** | Rules A/B/C/D; default **`WINNER_SELECTION = "C"`** (top-\(K\)) per MBB SELECT history memo |
| **PD20** | Rule **D** Gibbs + \(S = A - \lambda L^C\) |
| **PD17 / Pass A–B / most λ sweeps** | Rule **C** |
| **Sep 2026 assort mechanism runs** | Deterministic top-\(K\) on \(S\) at scenario \(\lambda\) (not a new MLE) |

### B. Documented “should be canonical” for manuscript (with tension)

| Claim | Source |
|-------|--------|
| Score ≠ select; Hero ≠ score | BINDING |
| **Replay v1:** Gibbs exact-\(K\) (D) after frozen rosters + transported PD21 knobs | MBB memo 2026-08-28 |
| Chapter: teach deterministic and stochastic; warn Bernoulli vs exact-\(K\); two temperatures | PD44 §4.5 |
| COMPASS questionnaire (Sep): deterministic top-\(K\) as v1 SELECT; stochastic “future” | **Older than Aug 28 MBB lock** — reconcile in prose |

**Practical §4.5.3:** deterministic equation as clean default; stochastic = **Gibbs K-draw** with **\(t_{\mathrm{Gibbs}}\)**; footnote **Bernoulli** as **§4.8 fit**, not generative SELECT.

### C. Unresolved

- Single manuscript-grade **stochastic** equation fully signed off (PD44 explicit gap).
- Transport of Bernoulli-fitted \((\lambda,\gamma,t_{\mathrm{MLE}})\) to **Gibbs SELECT**, **top-\(K\) on \(S\)**, or **top-\(K\) on \(p_i\)** without refit or approximation.
- **K-draw MLE** — discussed, **not run**.
- **\(L^C\) alignment:** `pool_c_smooth_team` (fit) vs `poolq_loo` (HERO axis) — MBB memo §2.
- **Row grain:** PD21 all player-seasons vs HERO last-ps — SCOUT ASSORT 20260927.
- **Global vs season top-\(K\)** in replay diagnostics.

---

## 7. Suggested chapter anchors (copy-ready structure)

### §4.5.3 — Stochastic selection

1. **Deterministic baseline:** top-\(K\) on \(S_i = A_i - \lambda L^C_i\) (BINDING + code C).
2. **Stochastic generative rule (PD20 / Aug 28 lock):** \(w_i \propto \exp(S_i/t_{\mathrm{Gibbs}})\), draw **\(K\)** without replacement.
3. **Explicit non-equivalence:** Bernoulli on softmax \(p_i\) with \(\sum p_i = 1\) per season is the **estimation** model (PD21), not exact-\(K\) generative SELECT (PD44, ASSORT scope).

### §4.8 opening — MLE / fitting bridge

1. We fit **independent Bernoulli** outcomes against **season-wise softmax** probabilities from **\(\eta_i = A_i/t_{\mathrm{MLE}} - \lambda L^C_i\)**.
2. **\(K\)** appears in the data and in θ construction; **\(K\)** is **not** in the likelihood constraint \(\sum_i p_i = 1\).
3. **θ** is fixed from \(K/N\) each season; **ρ** is calibrated separately on assignment, not in PD21.
4. Generative chapters use **different SELECT rules** (top-\(K\) or Gibbs); fitted parameters are **inputs or diagnostics**, not automatically likelihood-optimal under those rules unless refit or approximation is stated.

---

## 8. Primary file index

| Topic | Path |
|-------|------|
| PD21 MLE script | `sports/scripts/pd21_draft_bernoulli_mle.py` |
| SELECT rules A–D | `sports/tier1_pool_assignment.py` |
| PD20 Gibbs sweep | `sports/scripts/grandchild_temperature_select_sweep.py` |
| MBB SELECT / two-\(t\) memo | `3-Master_Plan/re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md` |
| MLE explainer | `3-Master_Plan/MLE/MLE_fit_explainer.md` |
| MLE basics (K-draw alt) | `3-Master_Plan/MLE/MLE_basics.md` |
| Chapter outline §4.5 | `3-Master_Plan/VECTOR_work/new_VECTOR_work/VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md` |
| BINDING | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` |
| Reigning fit JSON | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json` |
| 2013–21 fit JSON | `3-Master_Plan/re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json` |
| ASSORT replay scope | `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260927_empirical_selection_replay_v1_scope.md` |
| PD20 K-draw vs Bernoulli | `3-Master_Plan/Alex_stuff/PD20_softmax_K_winners_explainer.md` |

---

*COMPASS archaeology reply for VECTOR — documentation only; no new fits or runs authorized by this memo.*
