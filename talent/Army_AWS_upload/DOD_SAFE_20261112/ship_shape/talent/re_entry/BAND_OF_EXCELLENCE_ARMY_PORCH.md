# Band of excellence — Army porch & basketball θ (memo)

**Purpose:** Print-friendly anchor for why we drop own Â = 0 on congestion plots, how that relates to basketball **θ**, and which porch panels to trust for the story.

**Date:** 2026-09-24  
**Status:** Design agreed in chat; code prep for Vantage upload (not yet run on Army).

---

## One-sentence claim

**Congestion binds in the band where scarce distinction is actually at stake** — top blocks and promotion among officers senior raters are really sorting — not in the full captain cross-section from Â = 0 upward.

---

## Three filters (do not confuse)

| Filter | What it does | Where it lives |
|--------|----------------|----------------|
| **Missing SNR history** | `tb_ratio_fwd_snr` is **NaN** (no SNR-checked evals) | Already excluded from Panel 2 finite histograms |
| **Own Â = 0** (proposed) | Drop **ratees** with last-snapshot SNR TB ratio **exactly 0** (had SNR evals, never top-blocked) | Plot scripts 7–8–9 only — **no feather rebuild** |
| **Peer Â = 0** (Run 3) | Drop **peers** with tb_ratio = 0 from pool mean/size | Cell 5 / `POOL_EXCLUDE_PEER_TB_ZERO` |

**SNR ratio rule (Cell 4):** numerator = SNR top blocks; denominator = SNR-checked evals only. No SNR box → does not count toward Â (NaN, not zero).

---

## Filter order for panels 7, 8, 9

When the own–Â = 0 toggle is on:

1. **Require any finite OER/pool check column** (rename from mislabeled “zero-OER” filter).
2. **`pool_size_snr_fwd ≥ 3`** at last captain snapshot.
3. **Exclude own `tb_ratio_fwd_snr == 0.0`** (finite zero only).
4. Finite plot variables / dropna as today.

**Pool of six, two ever-TB’d:** All six can pass min-pool if each row has `pool_size ≥ 3`. Only the two with Â > 0 enter the congestion cohort. The pond still “made the cut”; we are not requiring ≥3 ever-TB’d peers in the plot sample.

---

## Basketball θ → Army band

| Basketball (MBB) | Army |
|------------------|------|
| **θ:** viability threshold — “in the draft conversation” (from drafted perf / K/N) | **Â > 0:** at least one SNR top block in career cumulative through last snapshot |
| **Panel 7 CCT:** fixed Â band (e.g. z ∈ [1, 2]), vary pool LOO | Same Act II probe on Army feather |
| **Panel 8 elite pond:** top ~20% Â, upper LOO tail | “Superstar pool” / thick elite pond |
| Congestion read: **upper LOO bins**, not full HERO left tail | Same: **panels 7–8 upper bins**, not Panel 9 lower T̂ bins |

**Interpretive line for Alex:** Senior raters at rating time are disproportionately comparing officers who might receive **scarce top blocks**, not averaging over officers with zero TB history. Ever-TB’d is a coarse empirical gate for “in the game”; CCT/elite gates are the **band of excellence** proper.

---

## θ in the model vs what MLE fits (basketball)

**Two layers — do not collapse them.**

### Model (generative SCORE layer)

Peers count toward team congestion via a **viability map**:

\[
L^C_j = \frac{1}{n_j}\sum_{h\in j}\sigma\big(\gamma(A_h - \theta)\big)
\]

**θ (theta)** = viability cutline — *who counts as a substitutable / draft-viable peer on this roster?* That is the “band of excellence” inside the **model**, not just a plot filter.

### Empirical calibration (PD21 Bernoulli MLE)

`pd21_draft_bernoulli_mle.py` fits a **Bernoulli / logistic-style** draft likelihood (season softmax → \(p_i\), then \(\sum_i [Y_i\log p_i + (1-Y_i)\log(1-p_i)]\)) on **fixed empirical rosters**.

| Parameter | Typical role in fit |
|-----------|---------------------|
| **λ** | Congestion weight in board logits \(A_i/t - \lambda L^C_i\) — **fitted** |
| **γ** | Sharpness of σ around θ — **fitted** (or fixed on grid) |
| **t** | Temperature — **fitted** |
| **θ** | Usually **not** a free MLE parameter — **set per season** from **K/N** (\(F_A^{-1}(1-K/N)\)) or **median perf among drafted** (`viability_theta_drafted_perf`) before building \(L^C\) |

So: **logistic/Bernoulli MLE solves mainly for λ, γ, t**; **θ is calibrated / fixed**, then congestion is built, then advancement is fit.

Open work: `theta_kn_sweep_diagnostic.py` — whether θ should **co-vary with K/N** rather than one fixed rule.

### Army analogue (no PD21 port yet)

| MBB | Army |
|-----|------|
| Draft scarcity **K/N** | Promotion to MAJ + **top-block scarcity** in SNR pool |
| θ = draft-viable perf | **θ_Army** = “in the top-block game” (senior raters sorting for TB) |
| \(L^C\) on **team roster** | Congestion in **senior-rater pool** (future: LOO mean of σ(γ(Â_peer − θ))) |
| Bernoulli draft MLE | **Competing risks** (promote / attrit / censor) — Cox/CIF, different likelihood |

**Near term (porch, discrete θ):**

- **Â > 0** — coarse floor (“ever received a TB”).
- **Panel 7 CCT** — hard band (e.g. z ∈ [1, 2]).
- **Panel 8 elite** — top ~20% Â.

**Medium term:** calibrate θ̂ from promoted officers or ever-TB’d quantiles; optional smooth **L^C** on SNR pools.

**Long term:** Army score → select replay (λ, γ on fixed empirical pools, θ calibrated) — mirror of reigning-hero MLE, **not** a drop-in of PD21 on Cox Cell 12.

**One line:** θ is a **model** viability threshold; MBB MLE **fits λ, γ, t** with θ preset; Army’s near-term θ is the **band-of-excellence gates** above; full Army θ + \(L^C\) is extension work, not current 520 requirement.

---

## Which porch panel for which question

| Panel | Question | Band of excellence? |
|-------|----------|---------------------|
| **2** | Distributions of Â, T̂ (last snapshot) | Full finite sample (before/after filter optional later) |
| **5** | H_sort / pool overlap (assortativity) | Optional same own–Â = 0 filter when testing |
| **7** | CCT: **fixed high Â**, promotion vs pool LOO bins | **Yes — primary congestion test** |
| **8** | Elite pond: top Â × upper LOO | **Yes — thickest elite ponds** |
| **9** | HERO: unconditional promotion vs pool x | **Descriptive full porch**; lower bins may drift if own–Â = 0 dropped — **do not over-read** |

**Lead with 7–8 for mechanism.** Panel 9 stays transparency; conditional story lives where θ logic lives.

---

## Dropping own Â = 0 — tradeoffs

**Pros**

- Focuses on officers **competing on the top-block margin**.
- Aligns Army deck with basketball conditional / θ design.
- Removes a large mass at Â = 0 that is a different estimand (“SNR-rated, never distinguished”).

**Caveats**

- **Lower T̂ / LOO bins on Panel 9** can look odd or “inflated” after exclusion — composition shift, not necessarily new physics.
- A six-officer pool may contribute only one–two officers to 7–8–9 after the filter — report **n excluded** in footers/JSON.
- This is **not** re-computing pools; feather pool metrics unchanged.

---

## Methods one-liner (copy-ready)

*Officers required `pool_size_snr_fwd ≥ 3` at last captain snapshot. Congestion panels further restrict to own SNR TB ratio > 0 (≥1 senior-rater top block in cumulative career through last snapshot). Pool size uses observed pond structure; excluded officers are omitted from promotion-vs-pool plots only. Primary inference: conditional bands (CCT, elite pond), mirroring basketball viability θ and conditional CCT.*

---

## Workflow reminder (Army)

- Code edits on **Mac (Dropbox)**; **no Army data or feathers on Mac** — ever.
- **Runs only on Army systems** (old PDE now, Vantage when live); feedback = **screenshots + error text**, not exported data.
- **Old PDE:** still runnable; **admin blocks uploads** — Mac edits reach it only by **hand transcription** unless urgent.
- **Vantage:** boots from **admin frozen repo snapshot** (not latest Mac); when online, Charles can **upload Mac scrubbed files** to catch up, then run and screenshot.

---

## Planned code (when Vantage is live)

1. Rename HERO “zero-OER” → **`require_any_oer_metric`** (~35–45 lines, 2 files).
2. Add **`EXCLUDE_OWN_TB_ZERO_LAST`** (default **off**) on panels 7–8–9 (~25–35 lines).
3. Later: before/after BDP for Â, T̂, LOO (Panels 2–3); checklist glossary row.

---

## Thread log

| Date | Note |
|------|------|
| 2026-09-24 | Memo from Agent chat: band of excellence, θ parallel, filter order, panel roles |
| 2026-09-24 | Added § θ model vs MLE; PDE/Vantage workflow; VECTOR addendum cross-link |
