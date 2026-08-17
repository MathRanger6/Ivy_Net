# MLE basics — mechanics for our draft / SELECT model

**For:** Charles (edit freely)  
**Last synced:** 2026-08-14  
**Context:** PD19/PD20 — after Gibbs SELECT + $t$ sweep; before fitting $\lambda^*, t^*, \ldots$  
**Companions:**
- [`PD20_softmax_K_winners_explainer.md`](PD20_softmax_K_winners_explainer.md) — softmax, K draws vs Bernoulli (choices A–F)
- [`PD20_K_draws_and_rho_explainer.md`](PD20_K_draws_and_rho_explainer.md) — K-draws + $\rho^*$ (shorter digest)
- [`../../transcripts/PD21_notes.md`](../../transcripts/PD21_notes.md) — **Alex lock (Aug 14):** Bernoulli MLE OK; two fits; board reparameterization

---

## PD21 update (Alex, Aug 14 — read this first)

**The K vs sum-to-1 “problem” is resolved for MLE** (network-science framing):

- **ASSIGN / $\rho^*$:** configuration-model style fit on **who is on which team** + performance — not the draft mechanism.
- **SELECT / $\lambda^*, t^*, \gamma^*$:** **Bernoulli** outcomes with softmax $p_i$ (sum to 1). Likelihood = $\prod_i p_i^{Y_i}(1-p_i)^{1-Y_i}$.
- **K is not in the formula.** You fit $p_i$ so **high-$p$ players match drafted players** — not “$\sum p_i = K$.”
- **No draft order**, no sequential Plackett–Luce required for Alex’s v1.
- **Draft MLE does not need $\rho$** — empirical rosters fixed; $\rho$ only for assign-layer fit.

**Board fit form** (see `transcripts/PD21_board.jpeg`):

\[
p_i \propto \exp(A_i/t)\,\exp(-\lambda L^C_{j(i)})
\]

Rescale $\lambda$ vs $t$ for numerics (avoid unidentified $\lambda/t$).

**Sim vs MLE:** Hero sim may keep K-draws; if paper needs alignment, adjust sim upstream — Alex expects small difference at MBB $N$.

*Sections below were written pre-PD21; keep for intuition, but PD21 supersedes “must use K-draw likelihood.”*

---

## MLE in one sentence (mechanical)

Pick parameters $\theta$ that **maximize**

\[
L(\theta) = P(\text{all the draft outcomes we actually saw} \mid \theta),
\]

i.e. the probability your model would have generated **this exact dataset** if those parameters were true.

No new experiment. One historical panel. “How plausible are these $\lambda, t, \ldots$ given what happened?”

---

## Step-by-step mechanics (generic)

**Step 1 — Write the generative model.**  
“If $\theta$ were true, how would data get produced?”

**Step 2 — Write the likelihood for one observation.**  
For one player-season with outcome $Y_i \in \{0,1\}$:

\[
P(Y_i \mid \text{stuff about } i, \theta).
\]

**Step 3 — Assume independence (often).**  
Multiply over all player-seasons:

\[
L(\theta) = \prod_i P(Y_i \mid \cdots, \theta).
\]

Log is easier numerically:

\[
\ell(\theta) = \sum_i \log P(Y_i \mid \cdots, \theta).
\]

**Step 4 — Maximize.**  
Adjust $\theta$ until $\ell(\theta)$ is as large as possible (BFGS, grid search, etc.).

**Step 5 — Interpret.**  
$\hat\theta$ = “best explanation” of the data **under that generative story**.

MLE is only as good as Step 1. Wrong generative story → “optimal” parameters for the wrong question.

---

## Our setup: what is one row of data?

One **player-season** $i$:

| Field | Meaning |
|--------|---------|
| $\hat A_i$ | Ability (fixed from data) |
| Team / roster | Fixed (empirical NCAA) |
| $L_{C,i}$ | Team congestion (from roster + $\gamma, \theta$) |
| $S_i$ | Selection score $= \hat A_i - \lambda L_{C,i}$ |
| $Y_i$ | **1 if drafted, 0 if not** (what MLE tries to explain) |

For a first MLE pass you’d typically **fix rosters** (no re-sim ASSIGN), so $\rho$ doesn’t move $L_C$. You’re fitting **SELECT/SCORE** knobs like $\lambda, t$ (and maybe $\gamma, \theta$).

---

## Rule C and MLE (why nobody does plain top-K MLE)

Rule C: $Y_i = 1$ iff $i$ is in top K by $S_i$.

Then for player $i$:

\[
P(Y_i=1 \mid S, \text{Rule C}) \in \{0, 1\}.
\]

Either guaranteed in or guaranteed out. For someone **not** drafted:

\[
P(Y_i=0 \mid \cdots) = 1 \quad\Rightarrow\quad \log P = 0.
\]

For someone drafted:

\[
P(Y_i=1 \mid \cdots) = 1 \quad\Rightarrow\quad \log P = 0.
\]

**Every** observation gets probability 1 under the model that produced them. Likelihood is flat w.r.t. $\lambda, t$ — **no curvature, no identification**. Deterministic SELECT doesn’t give a smooth “how likely was this draft?” surface to optimize.

That’s a big reason PD19 moved to **probabilistic** SELECT for MLE.

---

## Rule D + Bernoulli + softmax (PD19-style) — mechanics

**Generative story:**

1. Compute $S_i(\lambda, \gamma, \ldots)$
2. Softmax: $p_i = \dfrac{e^{S_i/t}}{\sum_j e^{S_j/t}}$ **within that season’s pool**
3. **Independent** Bernoulli: $Y_i \sim \mathrm{Bern}(p_i)$

**One player’s likelihood factor:**

\[
P(Y_i \mid p_i) = p_i^{Y_i}(1-p_i)^{1-Y_i}.
\]

Drafted ($Y_i=1$): contribute $\log p_i$  
Not drafted ($Y_i=0$): contribute $\log(1-p_i)$

**Full log-likelihood (one season, pool size N):**

\[
\ell = \sum_{i: Y_i=1} \log p_i + \sum_{i: Y_i=0} \log(1-p_i).
\]

**What the optimizer does:**  
Raise $\lambda, t$ so drafted players get higher $p_i$ and non-drafted lower $p_i$.

---

## Where Bernoulli + softmax breaks (mechanical, not philosophical)

### Breakdown 1 — Expected draft count

Within a season, $\sum_i p_i = 1$.

If Bernoullis are independent:

\[
\mathbb{E}\Big[\sum_i Y_i\Big] = \sum_i p_i = 1.
\]

Real MBB: $\sum_i Y_i = K \approx 125$.

So the model is built for **~1 draft per season on average**, while the data have **K**. MLE will fight the wrong constraint — it can’t simultaneously make all $p_i$ small enough for undrafted mass **and** match K winners without something else (scaling, correlation, exact-K constraint).

### Breakdown 2 — Ignores “exactly K” structure

Real data: **exactly K** ones per season (roughly), strong **negative correlation** (if he’s drafted, someone else’s slot is gone in a soft sense; in hard K-set, it’s structural).

Independent Bernoullis: draft count **varies**; no “these K share one pool of slots” constraint.

MLE treats each $Y_i$ as its own coin flip → **misses joint structure** of the K-set.

### Breakdown 3 — Pool normalization fights rare events

$p_i$ are **relative shares of 1** within the season. A typical player’s $p_i \sim 1/N$. Draft rate $\sim K/N \sim 2\%$.

MLE pushes drafted players’ $p_i$ up and others down, but each $p_i$ is tied to **everyone else** in the softmax denominator. The math is optimizing **shares of a single pie**, not **K pies**.

You can still run the optimizer — it returns numbers. They’re “best” for **that** wrong model.

### Breakdown 4 — Season boundary

Softmax sums to 1 **per season pool**. You must compute $p_i$ within season $t$, not over all 62k rows at once. Code must loop seasons. Conceptually fine; easy to get wrong in implementation.

---

## Rule D + K draws w/o replacement — MLE mechanics

**Generative story (matches sim):**

1. $w_i \propto e^{S_i/t}$
2. Draw **exactly K** distinct players with probabilities $\propto w_i$

**Likelihood object is not per-player Bernoulli with $p_i = \mathrm{softmax}_i$.**

It’s the probability of the **observed draft set** (or the full 0/1 vector) under K-draw.

### Sequential (Plackett–Luce style) picture

Order K picks without replacement:

- Pick 1: $P(i_1) = w_{i_1}/\sum_j w_j$
- Pick 2: remove $i_1$, renormalize over remaining
- … K times

Probability of a **particular ordered** K-tuple:

\[
P(i_1,\ldots,i_K) = \prod_{r=1}^{K} \frac{w_{i_r}}{\sum_{j \notin \{i_1,\ldots,i_{r-1}\}} w_j}.
\]

Real draft has **unordered** K winners. Likelihood = sum over orderings (or use unordered Plackett–Luce formula).

### Unordered K-set (what you want)

Let $D$ = set of drafted player indices, $|D|=K$:

\[
P(D) \propto \sum_{\text{orderings of } D} \prod_{r=1}^{K} \frac{w_{i_r}}{\text{remaining weight}}.
\]

**Log-likelihood for one season:**

\[
\ell_{\mathrm{season}} = \log P(D \mid w(S,\lambda,t)).
\]

Sum over seasons.

**What the optimizer does:**  
Change $\lambda, t$ so the **actual drafted group** had high probability under weighted K-sampling — not so each drafted player had high independent $p_i$.

### Marginal per-player form (alternative view)

You can define **marginal** inclusion probability under K-draw:

\[
q_i = P(Y_i=1 \mid w, K) \quad\text{(not equal to }\mathrm{softmax}_i\text{)}.
\]

Then likelihood can be written with $q_i$, but $q_i$ come from the **K-draw process**, not softmax alone. Computing all $q_i$ is heavier than Bernoulli.

---

## Side-by-side: one drafted player, one season

**Bernoulli-softmax:**

\[
\text{contribution} = \log p_i = \log \frac{e^{S_i/t}}{\sum_j e^{S_j/t}}.
\]

Only depends on $S_i$ **and everyone else’s scores** in the pool.

**K-draw (conceptual):**

\[
\text{contribution} = \log q_i,
\]

where $q_i$ = probability $i$ is **in the K-set**, which depends on $S_i$, K, and the whole weight vector — **not** $p_i = \mathrm{softmax}_i$.

For high $S_i$, both go up when $i$ is drafted. But **magnitude and gradients** differ because K-draw enforces “K total winners.”

---

## Where MLE “breaks down” in our pipeline — map

```text
ASSIGN (ρ) → rosters → L_C → SCORE (λ, γ, θ) → S_i
                                      ↓
                               SELECT generative law
                                      ↓
                    ┌─────────────────┴─────────────────┐
                    │                                   │
            Bernoulli(softmax)                    K-draw(softmax weights)
            Σ p_i = 1, E[#draft]≈1                 exactly K winners
                    │                                   │
                    ↓                                   ↓
            Simple ∏ p_i^{Y_i}                  log P(K-set | w)
            WRONG draft count                     RIGHT count, harder math
                    │                                   │
                    └─────────── MLE maximize ──────────┘
```

**Breakdown is at the arrow into SELECT**, not in SCORE or Hero bins.

- **Sim (Hero):** K-draw — fine.
- **MLE with Bernoulli-softmax:** wrong SELECT law for MBB.
- **MLE with K-draw:** aligned with sim; implementation cost.

---

## What you’d actually code (first MLE v0)

**Data:** empirical panel, fixed rosters, observed $Y_i$ draft indicator.

**Parameters:** start with $\lambda, t$ only (fix $\gamma, \theta$ from PD17).

**For each season:**

1. Build $S_i(\lambda)$ for all players in season.
2. Build weights $w_i = \exp(S_i/t)$.
3. **If Bernoulli path:** $p_i = w_i/\sum w_j$; add $\sum_i [Y_i\log p_i + (1-Y_i)\log(1-p_i)]$.
4. **If K-draw path:** let $D$ = drafted IDs; add $\log P(D \mid w, K)$ from Plackett–Luce / sequential formula.

**Optimize** $\ell(\lambda, t)$ with scipy or similar.

**Sanity checks:**

- Bernoulli-softmax: fitted “draft rate” per season will behave oddly vs K.
- K-draw: at cold $t$, should resemble top-K ranking; $\hat t$ should be interpretable.

---

## Bayesian vs MLE (one line)

Same likelihood $L(\theta)$; MLE takes $\hat\theta = \arg\max L(\theta)$. Bayes multiplies by prior: $P(\theta \mid \mathrm{data}) \propto L(\theta)\,P(\theta)$. **The SELECT breakdown is identical** — wrong likelihood hurts both.

---

## What to ask Alex (MLE-specific)

> “For MLE we need $P(\text{observed draft outcomes} \mid \lambda, t)$. Should that be **(A)** independent Bernoullis with $p_i = \mathrm{softmax}(S_i/t)$, or **(B)** probability of the **K drafted players** under **K weighted draws without replacement** from the same weights? Sim uses (B); the board formula looks like (A).”

Until that’s locked, you can prototype **both** on one season and compare $\ell$ and $\hat\lambda, \hat t$ — that makes the breakdown concrete.

---

## Bottom line

MLE mechanically = multiply (or sum logs of) **model probabilities of each observed outcome**. Rule C gives 0/1 probabilities → useless for fitting. Bernoulli-softmax gives easy per-player factors → **wrong expected K and wrong correlation structure**. K-draw gives the right generative law → **harder** $P(D \mid w,K)$, but matches what we simulate and what the draft institution looks like.

---

## Edit notes (Charles)

<!-- Add your edits below or inline. Park open questions here. -->

- [ ] Lock SELECT law with Alex: Bernoulli softmax vs K-draw likelihood
- [ ] First fit: $\lambda, t$ only on empirical rosters?
- [ ] $\rho$ via $H_{\mathrm{sort}}$ separately (Path C)?

---

*Charles runs PDF when ready:*

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/Alex_stuff/MLE_basics.md
```
