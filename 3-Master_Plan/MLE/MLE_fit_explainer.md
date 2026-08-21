# How we fit λ, γ, and temperature — read this first

**For:** Charles — learn the MLE thread from scratch  
**Date:** 2026-08-20  
**Go deeper (derivations):** [`MLE_basics.md`](MLE_basics.md)  
**Slides:** [`../re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD21_MLE_fit_AUTO.pptx`](../re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD21_MLE_fit_AUTO.pptx)  
**Code:** `sports/scripts/pd21_draft_bernoulli_mle.py`

---

## What this document is for

You asked for **instruction**, not a cheat sheet. This page walks through **what we did**, **why**, and **what the numbers mean**, assuming you remember the rest of the pipeline (ASSIGN / SCORE / SELECT, hero, ρ*, etc.) but **not** the statistics of maximum likelihood yet.

Symbols like **λ**, **t**, **γ**, **A**, **L^C** are fine — we use those everywhere. Words like “logit” and “Bernoulli MLE” are **not** assumed; when they appear, they get a one-line meaning, and the full derivation lives in [`MLE_basics.md`](MLE_basics.md).

---

## The question we answered

> Given real NCAA player-seasons (drafted or not), **what values of λ and t** make our **draft-probability story** best match what actually happened?

We held **γ = 18** fixed (same as the generative sim default). We did **not** re-fit ρ — rosters stay as observed.

**Panel (committed run):** 2013–2021, POST-QC, min 20 minutes → **38,123** player-seasons, **882** drafted.

---

## Where this sits in the three-step pipeline

You already know the split:

| Step | Knob(s) | This fit? |
|------|---------|-----------|
| **ASSIGN** | ρ (who lands on which roster) | **No** — ρ* from H_sort bracket separately |
| **SCORE** | λ, γ (ability vs congestion in the ranking formula) | **Partially** — λ yes; γ fixed at 18 |
| **SELECT** | t (how sharply probabilities follow the score) | **Yes** — t̂ from MLE |

**Score ≠ select** still applies: we are fitting the **probability model for draft**, not proving the NBA uses our score equation.

---

## Maximum likelihood in one paragraph (no jargon yet)

For every player-season we see a **yes/no** outcome: drafted (**Y = 1**) or not (**Y = 0**).

We write down a **model** that assigns each player a probability **p** of being drafted, where **p** depends on ability **A**, congestion **L^C**, and the knobs **λ** and **t**.

**Maximum likelihood** means: choose **λ** and **t** so that, if the model were true, the **whole history of yes/no outcomes we actually saw** would be as **likely as possible**.

No new data. No new experiment. One pass over the historical panel: “Which parameters make our story hardest to reject?”

That is standard statistics — not a sim-only trick.

---

## Step 1 — What goes into each row

One **row** = one player in one season.

| Column | Meaning |
|--------|---------|
| **A** | Ability (PPM z-score within that season) |
| **L^C** | Leave-one-out congestion on his roster (depends on γ) |
| **Y** | 1 if ever drafted from college, 0 if not |
| Roster | Fixed from real data (not re-simulated) |

We are **not** moving players between teams in this fit. ρ already did its job when the panel was built.

---

## Step 2 — From ability and congestion to a draft probability

This is the heart of the model. Read slowly; [`MLE_basics.md`](MLE_basics.md) shows the algebra.

### 2a. A “draft appeal” number for each player

Before probabilities, each player *i* in season *s* gets a **single number** that says how attractive he looks **relative to everyone else that season**:

\[
\text{appeal}_i = \frac{A_i}{t} - \lambda L^C_i
\]

Plain English:

- **Higher ability A** → higher appeal (good).
- **Higher congestion L^C** → lower appeal (crowded roster hurts), scaled by **λ**.
- **Temperature t** divides ability: smaller **t** means ability differences matter **more** (sharper ranking); larger **t** flattens everyone toward similar appeal.

**λ** and **t** are what we **estimate**. **A** and **L^C** are **inputs** from the panel (L^C changes when γ changes — that is why we later “profile” γ).

### 2b. Turn appeal numbers into probabilities (within one season)

Draft probabilities must be **between 0 and 1** and **add up to 1** across all players **in that season** (we treat each season as its own pool).

The standard way to do that is the **softmax** (explained step-by-step in MLE_basics):

\[
p_i = \frac{\exp(\text{appeal}_i)}{\sum_{j \text{ in same season}} \exp(\text{appeal}_j)}
\]

So: exponentiate each appeal, then divide by the season total. Highest appeal → highest **p**, but everyone shares one “pie” that sums to 1.

**Important:** Softmax probabilities sum to **1** per season, not K. We get a **ranking**; K enters later in sanity checks and sim ( **Step 5** ), not inside this formula.

---

## Step 3 — Bernoulli likelihood (yes/no trials)

Once each player has a model probability **p_i**, treat draft as a **coin flip** biased toward **p_i**:

- If **Y_i = 1** (drafted): the model contributes a factor **p_i** — “how likely was a yes?”
- If **Y_i = 0** (not drafted): the model contributes **(1 − p_i)** — “how likely was a no?”

For one player:

\[
P(Y_i \mid p_i) = p_i^{Y_i}(1-p_i)^{1-Y_i}
\]

Multiply over **all** player-seasons (we assume independence). Take the **log** (products become sums — easier for the computer):

\[
\ell = \sum_i \Big[ Y_i \log p_i + (1-Y_i)\log(1-p_i) \Big]
\]

**Maximum likelihood** = find **λ** and **t** (and optionally γ) that make **ℓ as large as possible**.

That sum **ℓ** is what the script prints as log-likelihood. Bigger (less negative) = better fit.

---

## Step 4 — How the computer actually finds λ̂ and t̂

1. **Build the panel** — ability, L^C at γ = 18, draft labels.
2. **Coarse grid** — try many (λ, t) pairs on a grid (e.g. λ from 0.5 to 3, t from 0.01 to 10). Keep the pair with the best ℓ.
3. **Refine** — hand that pair to a numerical optimizer (L-BFGS-B: smooth hill-climbing with bounds) that adjusts λ and t until ℓ stops improving.
4. **γ profile (optional diagnostic)** — fix γ at 5, 8, 10, …, 200; at **each** γ, rebuild L^C, repeat grid + refine for (λ, t), record the best ℓ. Plot ℓ vs γ to see whether draft data pin γ down (they mostly do not).

Script: `sports/scripts/pd21_draft_bernoulli_mle.py`  
Outputs: [`../re_entry/HEROs_and_PASSes/pd21_mle/`](../re_entry/HEROs_and_PASSes/pd21_mle/)

---

## Step 5 — Where K fits (two phases — read this)

You are right to ask: **we do not pass a known K into the optimizer.** There is **no** second math step that “finalizes” λ̂ and t̂ using K. The story is two phases:

### Phase A — Fit (what we already did)

- **Input:** every player’s **Y** (drafted or not). Each season has **K_s** drafted players — that is just **how many Y = 1** rows you see (e.g. 89 in one season).  
- **Estimate:** **λ**, **t** by maximizing Bernoulli ℓ.  
- **K is not in the formula.** Softmax makes ∑ **p_i = 1** per season, not K.  
- **Output:** **λ̂ ≈ 2.57**, **t̂ ≈ 1.07**, and a **p_i** for every player. **Done.** Parameters do not get re-fit.

### Phase B — Use known K (after the fit — no new λ, t search)

1. **Sanity check:** For each season, sort by **p_i**, take the top **K_s** (same K_s as counted from data), compare to real draftees. Mean overlap ≈ 12 picks — **check only**, not re-estimation.  
2. **We do not** rescale **p_i** so they sum to K (not in v1).  
3. **Sim / generative SELECT:** Use **λ̂**, **t̂** to build weights, then draw **exactly K** draftees without replacement (K-draw). That is how the wind tunnel picks fake draft classes — **same parameters**, different selection rule than Bernoulli MLE.

**If you wanted K inside the fit from the start:** that would be a **K-draw likelihood** (different model) — not what we ran. See [`MLE_basics.md`](MLE_basics.md) Part 5 and Part 10.

**Hand example:** [`MLE_basics.md`](MLE_basics.md) Part 6 — five players, one season, **K = 2**, compute p and ℓ by hand.

---

## What we found (2013–2021)

| Quantity | Value | Read it as |
|----------|-------|------------|
| **λ̂** | **≈ 2.57** | Congestion in the score **helps** explain who got drafted (λ > 0). Ability-only would miss something. |
| **t̂** | **≈ 1.07** | Moderate sharpness — not “only #1 matters” (t → 0), not “everyone equal” (t → ∞). |
| **γ** | **18 fixed** | Same as sim default. Profile shows ℓ nearly flat from γ ≈ 18 to 100 — draft labels do **not** tightly identify γ. |
| **Best ℓ** | **≈ −6919.1** | Best score under γ = 18 (only meaningful **relative** to other λ, t, γ tries). |

**γ profile takeaway:** ℓ is slightly best around γ = 100 on the grid, but **λ̂ and t̂ barely move**. We report **γ = 18** to stay aligned with the generative sim, not because MLE screams “18.”

**Sanity (not headline):** mean overlap between model top-K and real draftees ≈ 12 picks per season; recall on drafted players ≈ 12%. Soft probabilities ≠ perfect ranker — expected.

---

## Two different uses of “temperature t” (do not mix them up)

### A. PD20 generative sweep (before MLE)

**Question:** In the **simulator**, if SELECT is soft (Gibbs) instead of hard top-K, does the inverted-U in draft rate vs teammate quality **survive**?

**Method:** Grid over t on fake leagues — **not** fitting real draft labels.

**Answer:** Yes, mostly → we were allowed to move on to empirical MLE.

Plot: [`../re_entry/HEROs_and_PASSes/pd20_temperature/GRANDCHILD_temperature_select_sweep_2013_2021.png`](../re_entry/HEROs_and_PASSes/pd20_temperature/GRANDCHILD_temperature_select_sweep_2013_2021.png)

### B. Empirical MLE (this fit)

**Question:** What **t** (and λ) best explain **real** draft yes/no outcomes?

**Answer:** **t̂ ≈ 1.07**.

Use **t̂ from MLE** when you talk about the empirical fit. The PD20 sweep is the **gate** that justified soft SELECT in sim — not a substitute for t̂.

---

## Why Bernoulli here, not “draw exactly K winners”?

The **simulator** often picks **K** draftees without replacement (weighted draws). You could write a likelihood that matches that exactly.

For **empirical** draft MLE we use **independent Bernoulli trials** with softmax **p_i** instead (PD21 lock). Reasons in plain language:

1. **Tractable** — per-player factors multiply cleanly; optimizer is standard.
2. **Alex’s framing** — fit the **distribution of draft probability**, so high-**p** players match drafted players; K is in the **data**, not forced into ∑p_i = K.
3. **Sim can stay on K-draws** for pictures; at NCAA scale the gap is expected to be small.

See [`MLE_basics.md`](MLE_basics.md) for the honest caveats (probabilities sum to 1 per season, not K; independence vs “exactly K picks”).

---

## Hero (Layer A) — separate thread

The **ventile chart** (draft rate vs teammate quality) is **not** this fit.

- POST-QC: middle rise, **flat** elite tail.
- July inverted-U tail = pre-QC sensitivity only.

This document is about **λ, t, γ on draft labels**. Hero shape is documented elsewhere.

---

## Questions that come up while reading

**Is this really maximum likelihood?**  
Yes. We maximize the sum of log Bernoulli probabilities with **p_i(λ, t, γ)** from the softmax story above. JSON: `PD21_draft_bernoulli_mle_2013_2021.json`.

**Why not fit γ in the main run?**  
Draft yes/no does not move γ much once λ and t adjust. We anchor γ = 18 for one line with the sim; joint (λ, γ, t) MLE is in the script if needed later.

**Where is K? Are we fitting with a known K?**  
**No — K is not in the likelihood.** We fit λ and t using every row’s yes/no **Y**. Each season’s **K_s** is implicit (count of yeses). After the fit, we **check** top-**K_s** overlap and use **K-draw** in sim — but we do **not** run a second optimization to “apply K” to finalize λ̂, t̂. See **Step 5** and MLE_basics Part 5–6.

**Where is ρ?**  
Fitted separately on roster sorting (H_sort). Draft MLE uses **fixed** empirical rosters.

---

## Files

| Item | Path |
|------|------|
| This doc (overview) | `3-Master_Plan/MLE/MLE_fit_explainer.md` |
| Derivations & caveats | `3-Master_Plan/MLE/MLE_basics.md` |
| Slide deck | [`../re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD21_MLE_fit_AUTO.pptx`](../re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD21_MLE_fit_AUTO.pptx) |
| Fit JSON | [`../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json`](../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json) |
| γ profile plot | [`../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021_gamma_profile.png`](../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021_gamma_profile.png) |
| Regenerate slides + figure | `python sports/scripts/build_pd21_mle_fit_slides.py --season-min 2013 --season-max 2021 --slides-only --force-figures` |

---

## One-sentence summary

We assigned each player a draft probability from ability and congestion (knobs **λ**, **t**), scored how well those probabilities explain every real drafted / not-drafted outcome, and picked **λ̂ ≈ 2.6**, **t̂ ≈ 1.1** with **γ = 18** fixed — congestion in the score matters; the hero ventile chart is a different, parked thread.
