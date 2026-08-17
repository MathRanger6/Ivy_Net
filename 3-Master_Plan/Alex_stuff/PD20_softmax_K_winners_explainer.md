# Rule C → Rule D: softmax, K winners, and why there is a choice

**For:** Charles (and Alex, if useful)  
**Context:** PD19/PD20 — Gibbs SELECT, MLE later  
**Companion:** [`PD20_K_draws_and_rho_explainer.md`](PD20_K_draws_and_rho_explainer.md) (shorter print digest)

---

## Glossary (plain speech)

### Softmax

**Softmax** turns a list of **scores** (any numbers, higher = better) into a list of **probabilities that add up to 1**.

For players \(i = 1,\ldots,N\) with selection scores \(S_i\):

\[
P_i = \frac{\exp(S_i / t)}{\sum_{j=1}^{N} \exp(S_j / t)}
\]

Read it like this:

- **Numerator:** \(\exp(S_i/t)\) — bigger score → bigger number.
- **Denominator:** sum over **everyone** in the pool — normalizes so all \(P_i\) together equal **1**.
- **Temperature \(t\):** in the **denominator** (PD20 lock). Small \(t\) → weights concentrate on high \(S_i\); large \(t\) → weights flatten toward equal.

**Important:** Softmax does **not** by itself say “pick K people.” It says “here is how to split **100% of one unit** across the pool.”

### Bernoulli (in this story)

A **Bernoulli trial** is one coin flip: outcome is 0 or 1.

If player \(i\) has probability \(p_i\), a **Bernoulli model** says:

- With probability \(p_i\), \(Y_i = 1\) (drafted / selected).
- With probability \(1 - p_i\), \(Y_i = 0\).

If you run an **independent** Bernoulli for **every** player, the **expected** number of winners is:

\[
\sum_{i=1}^{N} p_i
\]

So whatever you set the \(p_i\) to, the model’s **average** draft count is the **sum** of those probabilities.

### Rule C (top-K) — what you already have

1. **SCORE:** compute \(S_i\) for each player (unchanged).
2. **SELECT:** sort by \(S_i\), take the **top K** exactly.

- **Deterministic** (same scores → same K winners).
- **Always exactly K** winners per season.
- No probabilities needed for the cut — only **rank order**.

### Rule D (Gibbs SELECT) — what PD20 added

1. **SCORE:** same \(S_i\).
2. **SELECT:** build Gibbs **weights** \(w_i \propto \exp(S_i/t)\) (same math as softmax).
3. **Then** (in our sim code): **draw K players without replacement** using those weights.

So in **code**, Rule D is **not** “flip a Bernoulli for each player from softmax.” It is “use softmax-style weights, then run a **K-person draft** from those weights.”

The **tension** is that PD19’s **written** formula looked like step 2 only — softmax **as** the draft probability — without step 3.

---

## 1. Why is there an issue going from C to D?

### What changes when you leave Rule C

| | Rule C | Rule D (as written on board) | Rule D (as coded for sim) |
|---|--------|------------------------------|---------------------------|
| Uses \(S_i\) | Yes | Yes | Yes |
| Uses temperature \(t\) | No | Yes | Yes |
| Winners per season | **Exactly K** | **Expected ~1** if softmax = Bernoulli \(p_i\) | **Exactly K** (K draws) |
| Stochastic? | No | Yes (if Bernoulli or K-draw) | Yes |

You already see the issue:

- **Rule C:** rank → chop at K. Clean.
- **Softmax alone:** gives \(P_i\) that **sum to 1**. If each \(P_i\) is “probability this player is drafted,” independent Bernoullis give **~1 draft per season on average**, not **K ≈ 125**.

MBB has **many** player-seasons and **K** draft slots per season. Softmax is natural for **“who is relatively more likely among peers?”** It is **not** automatically “probability of making the NBA draft” unless you define a **second step** (or a different formula).

### Why PD20 still worked for plots

For the **Hero readout** (draft rate vs pool quality), you need:

- Realistic **K** each season (same as before).
- A **softened** alternative to the hard rank cut (Gibbs + \(t\)).

So the sim uses **K draws without replacement** from Gibbs weights. That preserves “exactly K winners” like Rule C, but adds randomness and temperature.

**The issue is not “C vs D breaks the inverted-U.”** Your sweep showed the U survives.

**The issue is:** when you write **MLE** or a **paper formula**, you must say whether the **model** is:

- softmax probabilities **as** Bernoulli \(p_i\), or  
- Gibbs weights **then** a K-person selection process.

Those are **different generative stories** — same scores, different likelihood.

### Where Bernoulli enters (or does not)

**Bernoulli is not in Rule C at all.**

**Bernoulli enters** when someone writes likelihood like:

\[
\mathcal{L} = \prod_i P(Y_i \mid S_i)^{Y_i} \bigl(1 - P(Y_i \mid S_i)\bigr)^{1-Y_i}
\]

and sets \(P(Y_i=1) = P_i\) from the **softmax**. That is “each player independently drafted with probability \(P_i\).” That is the PD19 synopsis read — **integrating Bernoulli with softmax**.

**Our Rule D code does not do that for sim.** It integrates **K sampling** with softmax **weights**:

1. Weights from softmax math.
2. Sample **K distinct indices** without replacement (like a weighted lottery with K tickets).

Bernoulli and K-draw are **two different ways to go from weights to 0/1 outcomes**.

---

## 2. Possible choices to fix the “sum to 1 vs need K winners” problem

Below are the main options people use in practice. All start from the same scores \(S_i\) (and temperature \(t\)).

---

### Choice A — K draws without replacement (what sim Rule D does)

**Procedure (per season):**

1. Compute weights \(w_i \propto \exp(S_i/t)\).
2. Draw player 1 proportional to \(w\), remove them.
3. Repeat until you have **K** distinct winners (or one shot: `numpy.random.choice(..., size=K, replace=False, p=w/normalized)`).

**Interpretation:** Softmax defines **relative chance** in a **K-winners lottery**. Always **exactly K** ones in `Y_selected`.

**Likelihood for MLE (conceptual):** probability of the **observed set** of K drafted players under this sampling scheme (Plackett–Luce / weighted sampling without replacement — not the single-line softmax Bernoulli).

---

### Choice B — Independent Bernoulli with softmax as \(p_i\)

**Procedure:**

1. Compute \(p_i = \text{softmax}(S/t)\).
2. For each player \(i\), independently: \(Y_i \sim \text{Bernoulli}(p_i)\).

**Interpretation:** Each player has draft probability \(p_i\); **no** constraint that exactly K win.

**Expected drafts per season:** \(\sum_i p_i = 1\). Wrong scale for MBB unless you rescale (Choice C).

**Likelihood:** simple product of Bernoullis — easy on paper.

---

### Choice C — Bernoulli with scaled probabilities

**Procedure:**

1. Compute softmax \(P_i\) as above.
2. Set \(p_i = \min\bigl(1,\; K \cdot P_i\bigr)\) (or other scaling so \(\sum_i p_i \approx K\)).
3. Independent Bernoulli\((p_i)\) for each \(i\).

**Interpretation:** “Stretch” softmax so expected count is about K.

**Likelihood:** still Bernoulli product, but \(p_i\) are ad hoc — not standard Gibbs.

**Note:** Still does not enforce **exactly** K winners each season; variance in total draft count.

---

### Choice D — Keep Rule C for sim; use a different object for MLE

**Procedure:**

- **Sim / Hero plots:** Rule C or Rule D with K draws (phenomenology).
- **MLE:** fit a **separate** rare-event model, e.g. logistic regression  
  \(P(Y_i=1) = \sigma(\alpha + \beta S_i)\)  
  where \(\sum_i p_i\) is **not** forced to 1.

**Interpretation:** Gibbs story for **generative sim**; classic binary choice model for **estimation on real draft labels**.

**Likelihood:** logistic (or probit) — no softmax-over-pool constraint.

---

### Choice E — One K-set likelihood (Plackett–Luce / sequential)

**Procedure:**

- Same sampling as Choice A.
- **Likelihood:** write the probability that the **actual K drafted players** (or the full 0/1 vector) arose from sequential proportional sampling.

**Interpretation:** Statistically coherent match between **sim and estimation** for “K from Gibbs weights.”

**Likelihood:** correct but heavier — correlation across players within a season, not a simple per-player Bernoulli.

---

### Choice F — Expected selection curve (no explicit 0/1 likelihood yet)

**Procedure:**

- Do not fit player-level \(Y_i\) yet.
- Compare **binned expected** draft rate under Gibbs + K draws to empirical bins (method-of-moments / calibration).

**Interpretation:** PD15-style “fit to statistics of data,” not full MLE.

**Likelihood:** none — diagnostic only.

---

## 3. Pros and cons (as I see them for this project)

### Choice A — K draws without replacement (current sim)

| Pros | Cons |
|------|------|
| **Exactly K** winners — matches MBB and Rule C count | MLE likelihood is **not** the one-line softmax formula |
| Same skeleton as old Rule “A” in code (weighted sample) | Player-level \(Y_i\) are **correlated** within a season |
| PD20 sweep: inverted-U survives | Must derive/write Plackett–Luce (or simulate) for MLE |
| Cold \(t\) → top-K (verified) | Alex must bless this as **the** model, not Bernoulli softmax |
| Aligns with “Gibbs + draft slots” story | |

**Best for:** Hero sims, Alex’s “soften the cut but keep K,” PD20 gate.

---

### Choice B — Bernoulli + softmax \(p_i\)

| Pros | Cons |
|------|------|
| Matches PD19 **written** formula literally | \(\sum p_i = 1\) → **~1 draft/season** — wrong for MBB |
| Simple likelihood product | Does not match Rule D **sim** |
| Easy to explain on one slide | Hard to defend without rescaling |

**Best for:** Not recommended alone for MBB draft.

---

### Choice C — Scaled Bernoulli (\(p_i = K \cdot P_i\))

| Pros | Cons |
|------|------|
| Fixes expected count roughly | Cap at 1 is ad hoc |
| Still simple likelihood | Still independent — ignores “exactly K” |
| | Not standard in Gibbs/stat-phys literature |
| | Sim and MLE still **misaligned** unless sim uses same rule |

**Best for:** Quick hack; weak for dissertation unless Alex wants it.

---

### Choice D — Sim Gibbs/K-draw; MLE logistic on \(S_i\)

| Pros | Cons |
|------|------|
| MLE is standard econometrics | **Two models** — sim vs fit |
| No sum-to-1 constraint | Paper must separate “generative sim” from “draft choice model” |
| Fits rare events (low draft rate) | Not a unified Gibbs story |

**Best for:** Pragmatic draft prediction; weaker if you want one generative pipeline.

---

### Choice E — Plackett–Luce / full K-set likelihood

| Pros | Cons |
|------|------|
| **Sim = estimation** story | More math and implementation |
| Coherent with Choice A sim | Season-level correlation — harder optimization |
| Defensible in theory | \(\rho\) still needs Path C unless re-sim ASSIGN |

**Best for:** Serious MLE after Alex locks K-draws as the generative SELECT rule.

---

### Choice F — Moments / bin matching only

| Pros | Cons |
|------|------|
| Fast, aligns with “fit to data moments” | Not MLE — Alex asked for MLE eventually |
| Good for checking U shape | Does not give \(\lambda^*, t^*\) with SEs |

**Best for:** Bridge while waiting on Alex; not final parameter story.

---

## Recommended path for this lab (my read)

1. **Sim (done):** Rule D = Gibbs weights + **K draws** (Choice A).
2. **Ask Alex one line:** “MLE on K draws from Gibbs weights (Choice A/E), not independent Bernoulli softmax (Choice B)?”
3. **If yes:** implement **Choice E** likelihood (or MC approximation) on empirical rosters; \(\rho\) via **\(H_{\text{sort}}\)** separately (see other explainer).
4. **If Alex wants the board formula literally:** discuss **Choice C** or rewriting the board to show **two steps** (softmax weights → K draws).

---

## One paragraph you can say aloud

Rule C ranks everyone and chops exactly K — no probabilities. Gibbs softmax turns scores into numbers that sum to one, which is perfect for **relative** chances but not, by itself, “K draft picks.” If you treat those as independent Bernoulli probabilities, you get about one draft per season, not 125. Our sim fixes that by using softmax as **weights** and then drawing **K without replacement**, like a weighted draft lottery. The open choice is whether MLE uses that same K-draw story or the simpler Bernoulli-softmax formula on the board — they are not the same unless Alex says so.

---

*Charles runs PDF when ready:*

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/Alex_stuff/PD20_softmax_K_winners_explainer.md
```
