# PD20 open questions — K draws and $\rho^*$ (explainer)

**Last synced:** 2026-08-13  
**Audience:** Charles — print, edit, digest before next Alex touchpoint  
**Context:** PD19 (Gibbs SELECT + MLE ambition); PD20 ( $t$ in denominator; inverted-U sweep before MLE)  
**Related:** [`../transcripts/PD20_notes.md`](../transcripts/PD20_notes.md) · [`../transcripts/PD19_notes.md`](../transcripts/PD19_notes.md) · [`MLE_prob.docx`](MLE_prob.docx) · [`PD19_board.jpeg`](PD19_board.jpeg)

**Status:** Both questions are **still open**. PD20 locked temperature; neither K-draw semantics nor $\rho^*$ estimation path is settled.

---

## 1. The K-draws problem

### What the formula on the board says

\[
P(Y_i=1) \;=\; \frac{\exp(S_i / t)}{\sum_{k=1}^{N} \exp(S_k / t)}
\]

This is a **softmax** over the whole season pool. Critical identity:

\[
\sum_{i=1}^{N} P(Y_i=1) \;=\; 1
\]

If you treat each $P(Y_i=1)$ as a **literal Bernoulli probability** for player $i$, the model says: **expected number drafted ≈ 1 per season**, not **K ≈ 60** (or ~1% of $N$).

That is the tension with MBB: many player-seasons, **few** draft slots.

### Three objects people often merge

| Object | What it is | Sum over pool |
|--------|------------|----------------|
| **Gibbs weight** | $w_i \propto \exp(S_i/t)$ | weights sum to 1 after normalize |
| **Bernoulli $p_i$** | “each $i$ drafted independently with prob $p_i$” | $\sum p_i$ can be anything if you design it |
| **Exactly K winners** | NBA draft: K names per season | always **K**, not 1 |

PD19’s written formula looks like **Bernoulli $p_i$ = softmax**. PD20’s “equivalent to top-K at cold $t$” sounds like **exactly K winners**. Those are **not the same** unless you add an extra step.

### What SELECT rule `"D"` does (planned bridge)

1. Compute **scores** $S_i$ (SCORE — unchanged).
2. Gibbs **weights** $w_i \propto \exp(S_i/t)$.
3. **Draw K players without replacement** using those weights (same skeleton as old rule `"A"` in code).

That gives **exactly K** `Y_selected = 1` per season for **sim plots** — same count as PD17 top-K.

But then **$P(Y_i=1)$ for MLE is not** the simple softmax formula above, unless you define:

- **$P(Y_i=1)$** = **marginal** probability that $i$ is in the K-set under K draws without replacement (Plackett-Luce), or
- you use softmax only as **weights** for drawing, not as the literal likelihood term.

### Why it matters for the inverted-U sweep (PD20 first job)

For the **immediate task** (sweep $t$, replot Hero bins):

- **K draws without replacement** is the right sim readout — comparable to old top-K, same K per season, same binning.
- Alex’s worry (“does the U survive softening the cut?”) is about **replacing the hard rank cut with a stochastic rule that still picks K people** — not about fitting a literal softmax Bernoulli yet.

**No blocker for the $t$ sweep** if we use rule `"D"` = Gibbs weights + **K draws**.

### Why it matters later for MLE

When you write **likelihood** on real $Y_i \in \{0,1\}$:

| Approach | Likelihood | Issue |
|----------|------------|--------|
| **Independent Bernoulli with $p_i$ = softmax** | $\prod_i p_i^{Y_i}(1-p_i)^{1-Y_i}$ | $\sum p_i = 1$ → ~1 draft/season; **wrong scale** for MBB |
| **Bernoulli with $p_i = K \cdot \text{softmax}_i$** (capped at 1) | ad hoc | $\sum p_i \approx K$ but not standard; correlation ignored |
| **One K-set per season (Plackett-Luce)** | proper for “K without replacement” | harder; not the single-line softmax |
| **Logistic on $S_i$**: $P(Y_i=1)=\sigma(\alpha + \beta S_i)$ | classic rare-event | **no** “sum to 1” constraint; not full Gibbs pool |

**Open question for Alex:** For MLE, is the object **(a)** Gibbs weights + K draws (generative sim), or **(b)** literal $P(Y_i=1)$ = softmax (the written formula)? PD20 prioritized **(a)** for plots; PD19 synopsis read like **(b)**.

**One sentence:** Softmax is natural for **relative** chance among players; it is **not** automatically the Bernoulli $p_i$ for **K simultaneous** winners unless you define the multi-draw process.

### Cold / hot $t$ (with $t$ in the denominator)

| $t$ | Effect |
|-----|--------|
| **Small $t$** (cold) | Weights ≈ point mass on high $S_i$ → K draws ≈ **top-K** (PD17 world) |
| **Large $t$** (hot) | Weights ≈ uniform → K draws ≈ **random K** → inverted-U may flatten (Alex’s fear) |

That is what the $t$ sweep is meant to test.

### Glossary — softmax (same math as Gibbs here)

**Softmax** turns scores $S_i$ into **probabilities that sum to 1**:

\[
P_i = \frac{\exp(S_i/t)}{\sum_j \exp(S_j/t)}
\]

Higher $S_i$ → higher $P_i$. Smaller $t$ → sharper (more winner-take-all). Larger $t$ → flatter (more equal).

---

## 2. The $\rho^*$ question

### What $\rho$ actually does

**$\rho$ lives only in ASSIGN** (LG):

\[
\tilde{w}_{ij} = R_j \exp(-\rho|\hat{A}_i - \hat{\mu}_j|)
\]

It controls **who sits with whom** → rosters → team $L_C$ → then $S_i$ → then SELECT.

**$\rho$ does not appear in** $S_i = \hat{A}_i - \lambda L_C$.

### What the PD19 MLE doc asked for

Fit **$\rho^*, \lambda^*, \gamma^*$** by maximum likelihood on draft outcomes $Y_i$.

That sounds like one joint fit. The subtlety is **what is held fixed vs re-simulated**.

### Path A — Empirical NCAA rosters (fixed assignment)

If each row keeps **real** `(team_id, season)`:

- $\hat{A}_i$, teammates, $L_C$, and $S_i$ are **fixed** for given $\lambda, \gamma, \theta$.
- **$\rho$ does not enter at all** — you did not re-run LG assign.
- MLE can estimate **$\lambda^*, \gamma^*, t^*$** (and maybe $\theta$), **not $\rho^*$**, from this likelihood alone.

**$\rho$ on this path** is matched separately — e.g. pick $\rho$ so sim **$H_{\text{sort}}$** matches empirical **$H_{\text{sort}}$** (Alex wants $H_{\text{sort}}$ in the paper). That is **calibration**, not draft MLE.

### Path B — Full generative MLE (re-sim ASSIGN at each $\rho$)

For **$\rho^*$ from draft data**, $\rho$ must **move** the fitted object:

1. Fix $\rho$, run LG assign (seed choice matters).
2. Build $L_C$, $S_i$, SELECT (Gibbs + K draws or Bernoulli).
3. Evaluate likelihood of observed $Y_i$.
4. Optimize over $\rho, \lambda, \gamma, t$.

**Hard parts:**

| Issue | Why it hurts |
|-------|----------------|
| **Stochastic ASSIGN** | Same $\rho$ → different rosters each seed → likelihood **noisy** unless you average over seeds |
| **High dimensional** | Full assign likelihood is not a simple product of softmax terms |
| **Identifiability** | $\rho$ shapes $L_C$ and $H_{\text{sort}}$; $\lambda$ also moves SELECT — **tradeoffs** |
| **Empirical $\hat{A}$ fixed** | LG reshuffles seating only; $\rho^*$ = “best **generative** homophily for draft,” not “estimate NCAA’s true matching process” |

### Path C — Two-step (fits this project so far)

| Step | Estimate / match | Data |
|------|------------------|------|
| **1. ASSIGN** | **$\rho^*$** (or $\rho$ band) via **$H_{\text{sort}}$**, coverage, overlap | Roster geometry — **not** the draft equation |
| **2. SCORE + SELECT** | **$\lambda^*, \gamma^*, t^*$** via MLE (after U gate) | Draft $Y_i$ given rosters (empirical or sim at fixed $\rho$) |

Alex PD15: fit **parameters to statistics of raw data**, not “make sim curve match hero bin-by-bin.” **$H_{\text{sort}}$** is a natural **$\rho$** statistic; draft MLE is natural for **$\lambda, t$** (and maybe $\gamma$).

**$\rho^*$ is still a real goal** — but likely **“$\rho$ that matches sorting diagnostics”**, not **“$\rho$ from the same draft likelihood as $\lambda$”** unless you commit to Path B.

### Diagram (one glance)

```text
  ρ (ASSIGN)  →  rosters → L_C → S_i  (λ, γ, θ)
                              ↓
                    SELECT (t, K draws?)
                              ↓
                         Y_i draft
```

- **$\lambda^*, t^*$:** “Given rosters, how does congestion in **score** + Gibbs **select** relate to draft?”
- **$\rho^*$:** “What assign rule gives **realistic sorting** ($H_{\text{sort}}$, overlap)?” — **different data moment** unless you do full joint generative MLE.

---

## 3. Still-open checklist

| Question | Status | For $t$ sweep now? |
|----------|--------|---------------------|
| K draws vs literal softmax Bernoulli | **Open** for MLE; **K draws OK for sim** | Use K draws; confirm with Alex before MLE |
| **$\rho^*$** from draft likelihood vs **$H_{\text{sort}}$** match | **Open** | Fix $\rho$ at PD17 value (e.g. 0.5); sweep $t$ only |
| **$\theta$** fixed from $F^{-1}(1-K/N)$ vs estimated | Mostly fixed | Keep CDF rule for sweep |
| Joint **$\rho, \lambda, \gamma, t$** MLE | **Parked** after inverted-U gate | After PD20 success criterion |

---

## 4. One-liners for Alex

**K draws:**

> “The softmax formula sums to 1 over the pool; MBB has K winners. For sim we use Gibbs weights and draw K without replacement so we still get K picks and can compare to PD17. For MLE we need to agree whether the likelihood uses that K-draw process or independent Bernoullis from softmax.”

**$\rho^*$:**

> “$\rho$ only moves draft predictions if we re-simulate rosters. On fixed empirical rosters, MLE fits $\lambda$ and $t$, not $\rho$. $\rho^*$ is either joint generative MLE (hard) or matching $H_{\text{sort}}$/overlap first, then fitting SELECT given that assign layer.”

---

*Charles runs PDF when ready:*

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md
```
