# Model Chapter First Draft — consistency review (SELECT / MLE)

**Reviewed:** 2026-10-05 (NVector / repo agent; source: [`Model_Chapter_First_Draft.pdf`](Model_Chapter_First_Draft.pdf))  
**Cross-check:** [`COMPASS_to_VECTOR_MLE_Bernoulli_response.md`](COMPASS_to_VECTOR_MLE_Bernoulli_response.md) · code paths cited there  
**For SVector:** Upload this file (or PDF export) if the agent cannot see the repo; it summarizes draft vs repo without requiring git access.

---

## Overall verdict

| Area | Status |
|------|--------|
| **§4.5.1–4.5.2** (capacity, deterministic top-\(K\)) | **Aligned** with BINDING + code rule C |
| **§4.5.4** (Bernoulli vs exact-\(K\)) | **Strong** — matches PD44 and PD21 scope |
| **§4.4.5** (\(S_i = A_i - \lambda C_{g(i)}\)) | **Aligned** with generative SCORE (`tier1_pool_assignment`) |
| **§4.5.3** (stochastic + temperature) | **Conceptually right**; **equation still placeholder** — insert Gibbs exact-\(K\) rule; label **\(t_{\mathrm{Gibbs}}\)** |
| **§4.8** (MLE / fitting bridge) | **Outline only** — no prose yet for likelihood, softmax, \(\theta\), or saved \((\gamma,\lambda,t)\) |

No draft text yet conflates **MLE board temperature** with **Gibbs SELECT temperature** (good — but §4.8 must introduce both explicitly once written).

---

## What already matches the repo

### Score vs select (§4.5 intro, §4.5.2)

- SELECT converts scores to outcomes; capacity \(K\) is separate from ASSIGN capacity — consistent with [`BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md).
- Deterministic top-\(K\) on \(S_i\), tie-break for reproducibility, distinction from random **ASSIGN** — matches implementation and PD44.

### Bernoulli vs fixed-\(K\) (§4.5.4)

Draft language matches repo decisions:

- Bernoulli calibration → **variant / fitting**, not canonical fixed-capacity SELECT.
- Exact-\(K\) without replacement → **canonical fixed-capacity** stochastic story.
- **Parameters not automatically transferable** — matches PD44, ASSORT 20260927 scope, [`MLE_fit_explainer.md`](../../MLE/MLE_fit_explainer.md).

### SCORE (§4.4.4–4.4.5)

- Logistic contribution \(\sigma(\gamma(A_i-\theta))\), group mean \(C_j\), **\(S_i = A_i - \lambda C_{g(i)}\)** — matches Alex v1 / Pass A–B generative score (team-level congestion, include-all-members mean in code as `pool_c_smooth_team` family).

---

## Gaps and recommended fixes

### 1. §4.5.3 — replace equation placeholder

**Issue:** Placeholder correctly asks for exact-\(K\) without replacement, but draft prose says “selection **probability**” in a way that can be read as **independent** Bernoulli. Repo canonical **generative** stochastic rule is **Gibbs rule D**: weights from **\(S_i\)**, then **one** weighted sample of **\(K\)** indices without replacement ([`tier1_pool_assignment.py`](../../../sports/tier1_pool_assignment.py) `choose_selected`, `"D"`).

**Naming:** Call the knob **\(t_{\mathrm{Gibbs}}\)** (or “selection temperature”), **not** the same symbol as PD21 **\(t_{\mathrm{MLE}}\)** without a sentence separating them.

**Suggested insert (prose + display equation for Word):**

> Under the fixed-capacity stochastic rule implemented in the simulation code (PD20 / rule D), define Gibbs weights from the score vector  
> \(w_i \propto \exp(S_i / t_{\mathrm{Gibbs}})\),  
> with \(S_i = A_i - \lambda C_{g(i)}\) as in §4.4.5. Conditional on scores, draw **exactly \(K\)** distinct individuals **without replacement** with inclusion probabilities proportional to \(w_i\) at each draw (weighted sampling without replacement). As \(t_{\mathrm{Gibbs}} \downarrow 0\), the procedure collapses to deterministic top-\(K\) on \(S_i\).  
>  
> This rule is **not** the same as independent Bernoulli selection with season-normalized probabilities (§4.5.4).

Optional footnote: PD21 fitting uses a **different** temperature, \(t_{\mathrm{MLE}}\), inside board logits \(\eta_i = A_i/t_{\mathrm{MLE}} - \lambda L^C_i\) before softmax — see §4.8.

### 2. §4.8 — MLE bridge still to write

§4.8 is currently **bullet headings only**. For the opening bridge (4.8.1 or a dedicated 4.8.0), repo-accurate content should include:

1. **Fixed rosters** — PD21 does not re-run ASSIGN; fits on observed team structure.
2. **Board logits:** \(\eta_i = A_i/t_{\mathrm{MLE}} - \lambda L^C_i\) — **not** \((A_i - \lambda L^C_i)/t_{\mathrm{MLE}}\).
3. **Within-season softmax:** \(p_i = \exp(\eta_i)/\sum_{k\in s}\exp(\eta_k)\), \(\sum_i p_i = 1\) per season; **\(K\) not in the likelihood constraint**.
4. **Bernoulli log-likelihood:** \(\sum_i [Y_i\log p_i + (1-Y_i)\log(1-p_i)]\); **joint estimation** of \((\lambda,\gamma,t_{\mathrm{MLE}})\) (or fixed \(\gamma\)) — script [`pd21_draft_bernoulli_mle.py`](../../../sports/scripts/pd21_draft_bernoulli_mle.py).
5. **\(\theta\)** preset each season from \(K/N\) quantile when building \(L^C\); **\(\rho\)** not estimated in PD21 (assign layer separate).
6. **Reported fits (state window + file):** e.g. reigning 2009–2021 joint fit \(\gamma^*\approx 19.57\), \(\lambda^*\approx 1.30\), \(t^*_{\mathrm{MLE}}\approx 1.07\) ([`REIGNING_PD21_...json`](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json)); 2013–2021 with \(\gamma=18\) fixed gives \(\lambda^*\approx 2.57\) — **do not merge windows in one table without labeling**.
7. **Bridge sentence:** Fitted \((\lambda,\gamma,t_{\mathrm{MLE}})\) are **inputs or diagnostics** for generative SELECT (top-\(K\) or Gibbs); they are **not** likelihood-optimal under those SELECT rules unless refit (§4.5.4, 4.8.4).

**Suggested opening paragraph (adapt for voice):**

> Empirical calibration in the basketball application follows a deliberate separation between **fitting** and **generative selection**. On fixed NCAA rosters, we estimate congestion and board parameters by maximizing a Bernoulli log-likelihood built from season-wise softmax probabilities. Each player-season receives a draft indicator \(Y_i\); logits combine standardized performance with a team-level congestion term constructed from a viability transform of peer performance, with cutline \(\theta\) tied to the empirical selectivity rate in that season. The optimizer adjusts \((\lambda,\gamma,t_{\mathrm{MLE}})\) while holding assignment fixed; homophily \(\rho\) is not part of this fit. The resulting probabilities sum to one within each draft season and therefore do not, by themselves, define a fixed-\(K\) generative draft; generative replay instead uses the SELECT rules in §4.5.2–4.5.3, and parameters calibrated under the Bernoulli formulation should not be treated as automatically valid under exact-\(K\) selection without further justification.

### 3. Notation consistency (optional clarity)

| Draft | Repo / memos | Note |
|-------|----------------|------|
| \(C_j\), \(C_{g(i)}\) | Often \(L^C\), `pool_c_smooth_team` | Fine in chapter; one sentence that **HERO binned axis** may use leave-one-out **\(L_Q\)** while SCORE uses team \(C_j\) — PD21 vs HERO alignment is **open** ([MBB memo](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md)). |
| Single \(t\) in §4.5.3 | Two temperatures in project | Split before §4.8 goes final. |

### 4. What the draft correctly does **not** claim yet

- No erroneous “softmax vs Bernoulli” as competing draft models in generative text.
- No numeric \(\lambda,\gamma,t\) in chapter body yet (avoids wrong-window citation).
- No statement that Bernoulli-fitted \(p_i\) are literal NBA draft probabilities (ASSORT replay caution).

---

## Section map (draft PDF)

| Section | MLE/SELECT relevance |
|---------|----------------------|
| 4.4.5 | \(S_i\) for SELECT — **done** |
| 4.5.2 | Deterministic SELECT — **done** |
| 4.5.3 | Stochastic SELECT — **placeholder equation** |
| 4.5.4 | Bernoulli vs exact-\(K\) — **done** |
| 4.5.5 | \(K/N\) domain mapping — **done** (2.7% caveat present) |
| 4.8 | Fitting bridge — **to draft** |

---

## SVector vs NVector

| Agent | Can use |
|-------|---------|
| **SVector** (upload-only) | This review + [`COMPASS_to_VECTOR_MLE_Bernoulli_response.md`](COMPASS_to_VECTOR_MLE_Bernoulli_response.md) + draft PDF |
| **NVector** (repo) | Above + live scripts, JSON fits, PD44 outline |

---

*Review complete — no changes made to `Model_Chapter_First_Draft.docx`; paste suggestions are advisory.*
