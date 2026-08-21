# Paper Directions 21 — my read (Aug 14, 2026)

**Source:** `transcripts/20260814_Paper_Directions_21_otter_ai_transcript.docx` (~14 min)  
**Whiteboard:** `transcripts/PD21_board.jpeg`  
**Context:** PD20 $t$ sweep done; Charles raised K-draw vs Bernoulli / sum-to-1 vs K  
**Prior:** [`PD20_notes.md`](PD20_notes.md) · [`../3-Master_Plan/MLE/MLE_basics.md`](../3-Master_Plan/MLE/MLE_basics.md)

---

## Headline

Alex **resolves the K vs softmax tension for MLE** in network-science terms: use **Bernoulli success model** with softmax probabilities (sum to 1); **K is not in the likelihood** — you fit the **distribution** so the **highest-$p$ players match the drafted set**. **Two fits:** $\rho^*$ from **configuration-model** ASSIGN; $\lambda^*, \gamma^*, t^*$ from **selection** on fixed empirical rosters (**$\rho$ not needed** for draft MLE).

---

## Network-science framing (Alex)

| Layer | Model type | Parameters | Data |
|-------|------------|------------|------|
| **ASSIGN** | **Configuration model** (network) | $\rho^*$ | Who is on which team + player performance |
| **SELECT** | **Success / Bernoulli** (binary outcomes) | $\lambda^*, \gamma^*, t^*$ | Draft $Y_i$ given rosters already fixed |

Use **stochastic block model** spirit as inspiration — not a literal SBM fit, but the **split**: structure/assignment vs binary success on nodes.

> “$\rho$ is not in the selection probability — it’s baked into assignment.”

---

## K-draw vs Bernoulli — Alex’s lock

Charles raised: softmax sums to 1, not K; sim uses K draws w/o replacement.

**Alex:** “That’s fine. That’s not an issue.”

Mechanical read:

- You are **not** fitting “exactly K sequential picks” or draft order.
- You **are** estimating **parameters of the success distribution** $p_i \propto \exp(\cdots)$ such that:
  - **Drafted players** tend to have **high** $p_i$
  - **Non-drafted** tend to have **low** $p_i$
- Likelihood = **product of Bernoulli factors** over all player-seasons:
  \[
  \prod_i p_i^{Y_i}(1-p_i)^{1-Y_i}
  \]
- **K is implicit:** if the model is good, the top-$p$ set aligns with the ~K drafted — you’re not enforcing $\sum p_i = K$.

Charles paraphrase Alex confirmed: maximize correlation between **top-$p$ players** and **observed draft class**.

**Sim alignment:** If sim (K draws) and MLE (Bernoulli) still feel mismatched for publication, **modify upstream sim** to align with the simple MLE — exchangeability + large $N$ → “shouldn’t be that big a difference.”

---

## Whiteboard formula (PD21_board.jpeg)

Three equivalent **writing** steps (green marker):

1. $p(S_i) \sim \exp\!\bigl(\frac{1}{t}(A_i - \lambda L^C)\bigr)$
2. $\sim \exp(A_i/t - \lambda L^C)$  ← **reparameterization for fitting**
3. $\sim \exp(A_i/t)\cdot\exp(-\lambda L^C)$

**Index:** $L^C$ on team $j(i)$ — Alex wrote $L^C_j$ / team congestion.

**Numerics trick (transcript):** Avoid fitting $\lambda/t$ as an unidentified ratio. **Rescale** so $\lambda$ and $t$ are not both free in a sloppy product — bake scale into $\lambda$ during fit; can factor back out later. “Just the scale — once you fix one, the other is adjustable.”

**Note for code:** PD20 sim uses $S_i/t = (A_i - \lambda L_C)/t$. Board line 2–3 separates **ability/temperature** from **congestion penalty** — check algebra when implementing MLE vs sim.

---

## Two (or four) estimation steps

| Step | Fit | Needs $\rho$? | Data |
|------|-----|---------------|------|
| **1** | $\rho^*$ | yes | Empirical rosters + $\hat A_i$ — configuration / LG assignment likelihood |
| **2** | $\lambda^*, t^*$ (+ $\gamma$ if free) | **no** | Draft $Y_i$ on **fixed** empirical teams |

Alex (end of call): for **selection MLE**, **you don’t need $\rho$** — “selection already happened; once people are on a team it doesn’t matter.” $\rho$ is for **artificial team creation** in sim / assign calibration.

Charles: still mimicking empirical post-filter team sizes in sim — Alex: “Central limit theorem; I’m not worried.”

---

## What this is NOT

- **Not** individual player prediction (fantasy football).
- **Not** draft order / sequential picks.
- **Not** requiring freshman/sophomore identity — player-season performance only.
- **Goal:** show inverted-U is **real**, model **reproduces** it; then population-level predictions — “statistics of how things interact, not who exactly the player is.”

---

## Open / Charles homework

- [x] Re-read Alex’s “sample K from distribution” line against [`MLE_basics.md`](../3-Master_Plan/MLE/MLE_basics.md) — PD21 lock documented Aug 2026
- [ ] Decide if sim Rule D stays K-draw for Hero or shifts toward Bernoulli for paper alignment
- [ ] Implement configuration-model MLE for $\rho^*$ (separate from draft likelihood)
- [ ] Implement Bernoulli-softmax MLE for $\lambda, t$ (board factorization)

---

## One-liners for Alex follow-up

**K vs 1:** “We fit $p_i$ with softmax; Bernoulli product over all $Y_i$; K enters only through which players have $Y_i=1$, not through $\sum p_i = K$.”

**$\rho$ vs draft:** “$\rho^*$ from assign/configuration fit on rosters; draft MLE for $\lambda, t$ on fixed teams — no $\rho$ in selection likelihood.”

---

## Artifacts

| Item | Path |
|------|------|
| Transcript | `transcripts/20260814_Paper_Directions_21_otter_ai_transcript.docx` |
| Whiteboard | `transcripts/PD21_board.jpeg` |

Optional mirror: `3-Master_Plan/re_entry/11_PD21_Alex_meeting_takeaways.md` when stable.
