# Rho estimation options — plain-language guide

**For:** Charles (edit freely; discuss with Alex)  
**Last synced:** 2026-08-17  
**Context:** Paper Directions 21 — fit homophily knob $\rho$ (rho) on **empirical NCAA rosters**, separate from draft maximum likelihood estimation (MLE)  
**Companions:**
- [`../MLE/MLE_basics.md`](../MLE/MLE_basics.md) — Bernoulli draft MLE ($\lambda$, $t$); **no $\rho$** on fixed rosters
- [`../Alex_stuff/PD20_K_draws_and_rho_explainer.md`](../Alex_stuff/PD20_K_draws_and_rho_explainer.md) — why $\rho$ and draft likelihood are different layers
- [`../../transcripts/PD21_notes.md`](../../transcripts/PD21_notes.md) — Alex lock (Aug 14)
- [`../re_entry/HEROs_and_PASSes/Alex_LG_three_step_briefing.md`](../re_entry/HEROs_and_PASSes/Alex_LG_three_step_briefing.md) — Grandchild assignment (LG) formulas

**Locked project choices (Aug 14):**
- **Assignment engine:** Grandchild assignment (LG) only — not Pass B soft assign
- **Data:** empirical NCAA, empirical roster caps, 2011–2021
- **Outputs:** one $\rho^*$ per season + one **longitudinal** $\rho^*$ pooled across seasons
- **Seeds:** 50 simulation runs per $(\rho, \text{season})$ to start (increase later; high-performance computing (HPC) when stable)
- **Success (stronger):** match sorting index ($H_{\mathrm{sort}}$), global within-team sum of squares (global_wss), and team congestion ($L_C$) distribution vs empirical; report vs legacy $\rho = 0.5$

---

## What all four options are trying to do

You have **real NCAA men’s basketball data** for 2011–2021. For each season you know:

| Input | Meaning |
|-------|---------|
| $\hat{A}_i$ | Player ability (performance per minute, z-scored within season — hero panel) |
| Roster caps | How many seats each real team has (stub capacity multiset) |
| Team labels | **Who ended up on which team** (observed assignment) |

You also have a **simulation rule** for building synthetic rosters: **Grandchild assignment (LG)**. It seats players one at a time. The homophily knob **$\rho$** controls how strongly a player prefers teams whose **current** average ability is close to their own.

**The fitting problem:** find the value of **$\rho$** that makes Grandchild assignment (LG) produce rosters that **look like** the real ones — using **team assignment data only**, not draft outcomes.

**Important:** none of the four options below uses “was this player drafted?” That is a **separate** step (Bernoulli softmax draft MLE for $\lambda$, $t$).

---

## Shared vocabulary

| Term | Plain meaning |
|------|----------------|
| **$\rho$ (rho)** | Homophily knob in Grandchild assignment (LG). Higher $\rho$ → players sit with more similar teammates. $\rho = 0$ → nearly random seating among open teams. |
| **Sorting index ($H_{\mathrm{sort}}$)** | After rosters are set: how much do team labels explain ability spread? Near 0 = teams look random; higher = more ability-sorted. Formula: $1 - \frac{\text{within-team sum of squares}}{\text{total sum of squares}}$. |
| **Global within-team sum of squares (global_wss)** | Raw measure of spread around team means. Same information as $H_{\mathrm{sort}}$, but not scaled to 0–1. |
| **Team congestion ($L_C$)** | How crowded a team is with “viable” peers (smooth viability formula). Used in scoring later; also a diagnostic for roster structure. |
| **Stub capacity ($R_j$)** | Open seats on team $j$ during seating. Grandchild weights multiply homophily by remaining seats. |
| **Random seed** | Grandchild assignment (LG) shuffles player order and randomizes team draws. Same $\rho$, different seed → slightly different rosters. |

---

## Panel policy vs roster caps (don’t conflate them)

Two design choices look related but solve **different problems**. Discuss them separately with Alex.

| Choice | What it controls | Tied to minutes filter? |
|--------|------------------|-------------------------|
| **Minutes / ability policy** | Who is on the panel and what $\hat{A}_i$ they carry | **Yes** |
| **Empirical roster caps ($R_j$)** | Real NCAA team sizes (heterogeneous stub capacities) | **No** |

**Empirical caps are not a workaround for filtering.** Teams have different roster sizes whether or not you drop bench players. Grandchild assignment (LG) still needs a capacity multiset that sums to $N$. Moving to fixed roster size $C$ would simplify the engine but **throws away** real NCAA roster-size heterogeneity — a separate modeling choice Alex already locked for PD21.

### Default panel (Aug 14 baseline)

- **Filter:** drop player-seasons with **under 20 minutes** (`min_minutes = 20`).
- **Ability:** PPM z-scored within season on the **filtered** panel.
- **Caps:** recomputed from that filtered panel (smaller $N$, fewer players per team).

**Issue we saw:** on this panel, **6/11 seasons** had per-season $\rho^* = 0$ and longitudinal $\rho^* \approx 0.07$ — very low assortativity. Simulated sorting at $\rho = 0$ was already close to (or above) empirical on the **trimmed** league.

### Alternative panel (Aug 17 — Alex discussion)

- **Keep all roster rows** (no minutes filter).
- **Bench rule:** set **raw PPM = 0** for players with **under 20 minutes**, then z-score within season as usual.
- **Caps:** actual NCAA roster counts on the **full** panel.

**Script flag:** `--ppm-zero-below-minutes 20` in `pd21_rho_hsort_calibrate.py` (default min-20 filter unchanged; outputs use suffix `_ppm0lt20`).

**What this simplifies:** one roster universe for empirical vs simulated assignment — same bodies, same team sizes; bench carries no skill signal instead of being deleted. Fewer moving parts between “who is in emp $H_{\mathrm{sort}}$” and “who is in sim LG.”

**What it does *not* simplify:**

| Layer | Still need empirical caps? | Still need a minutes policy? |
|-------|---------------------------|------------------------------|
| **ASSIGN $\rho$ / $H_{\mathrm{sort}}$** | **Yes** — heterogeneous $R_j$ | Test ppm-zero; may replace filter here |
| **$L_C$ / congestion diagnostics** | **Yes** | Probably align with ASSIGN panel |
| **Hero ventiles / LOO / draft MLE ($\lambda$, $t$)** | Fixed empirical teams (no LG) | **Probably keep min $\geq$ 20** unless Alex says otherwise — draft estimand is about rotation contributors, not walk-ons |

**Score $\neq$ select (binding):** ASSIGN can use full roster + zero bench while SELECT MLE uses a filtered hero panel. That is allowed and may be **correct** — different layers, different estimands.

### If ppm-zero “works” (sensible interior $\rho^*$, not stuck at cap)

The story is likely **panel definition**, not “drop empirical caps”:

> Low homophily was partly because the minutes filter built a **different league** than raw NCAA rosters — sim at $\rho = 0$ was already “sorted enough” on the trimmed panel.

That does **not** imply recalculating **everything** without filtering. Treat it **layer by layer** (see table above).

### Question for Alex (next meeting)

> “For draft MLE, do we keep `min_minutes = 20` on the hero panel even if ASSIGN $\rho$ calibration uses full roster + zero bench?”

**Working guess:** yes for MLE; maybe full roster + zero bench only for LG / $H_{\mathrm{sort}}$ — but Alex decides.

---

## Option (a): Sorting-index calibration — match one statistic by simulation

### Idea in plain language

Grandchild assignment (LG) is **random**. You cannot expect one simulation run to exactly reproduce one real season. Instead:

1. Measure the **real** sorting index ($H_{\mathrm{sort}}$) from observed team labels.
2. For a trial value of **$\rho$**, run Grandchild assignment (LG) many times (50 seeds) with the **same** abilities and roster caps.
3. Average the simulated sorting index over those runs.
4. Pick the **$\rho$** where simulated and empirical sorting indices match.

You are **calibrating** the knob to a **readout**, not writing a full probability formula for the exact roster.

### Tiny numeric example (made-up numbers)

Suppose **2015** has 4,000 players and empirical sorting index $H_{\mathrm{sort}}^{\mathrm{emp}} = 0.12$.

| Trial $\rho$ | 50 simulation runs → mean $H_{\mathrm{sort}}^{\mathrm{sim}}$ |
|--------------|------------------------------------------------------------------|
| 0.3 | ≈ 0.07 (too mixed) |
| 0.8 | ≈ 0.11 (close) |
| 1.5 | ≈ 0.18 (too sorted) |

Pick **$\rho^* \approx 0.8$** for 2015.

Repeat for each season → **$\rho^*_t$ per season**.  
Then pick **$\rho^*_{\mathrm{long}}$** by minimizing the same mismatch **averaged or summed across all seasons**.

### What this is / is not

| Is | Is not |
|----|--------|
| Honest about Grandchild assignment (LG) being stochastic | A literal “probability this exact roster happened” |
| Easy to explain: “we match realized sorting” | Using draft data |
| Fast to implement (extends existing rho sweep script) | Matching global_wss or $L_C$ unless you add them (→ option d) |

### Per-season vs longitudinal

- **Per season ($\rho^*_t$):** each year gets its own knob — “what homophily matches 2015 NCAA seating?”
- **Longitudinal ($\rho^*_{\mathrm{long}}$):** one knob for 2011–2021 — “one $\rho$ for the whole panel”

Both are natural. They can differ if sorting strength varied by era.

---

## Option (b): Pseudo-likelihood on observed team labels

### Idea in plain language

Grandchild assignment (LG) is **sequential** (players arrive one at a time; team centroids update). Real NCAA data gives only the **final** teams — **not** the seating order.

**Pseudo-likelihood** means: pretend each player’s team choice was a **simple independent decision** based on how close they are to each team’s talent, and ask: *“Under this simplified rule, how plausible are the teams we actually saw?”*

You **do not** re-run the simulator. You look directly at observed rosters.

### The simplified rule (conceptual)

For player $i$, team $j$, with leave-one-out team mean $\bar{A}_{j,-i}$ (team $j$’s average ability **excluding** player $i$):

$$
P(\text{player } i \text{ on team } j) \propto \exp\bigl(-\rho \cdot |\hat{A}_i - \bar{A}_{j,-i}|\bigr)
$$

Multiply (or add log-) these probabilities for **every player’s actual team**. Pick **$\rho$** that makes the **observed** assignment score highest.

### Tiny example: 6 players, 2 teams

Abilities: players 1–3 are high (10, 9, 8); players 4–6 are low (2, 3, 1).

**Observed assignment:**
- Team A: players 1, 2, 4 → team mean ≈ 7.0
- Team B: players 3, 5, 6 → team mean ≈ 4.0

**Question for player 4** (ability = 2, actually on Team A):

- Leave-one-out mean of Team A (without player 4): $(10+9)/2 = 9.5$
- Leave-one-out mean of Team B (without player 4): $(8+3+1)/3 = 4.0$

Player 4 is **closer** to Team B’s mean. Under **high** $\rho$, the simplified model says Team A is **surprising** for player 4.

- **Low $\rho$:** both teams look plausible → observed assignment not very surprising.
- **High $\rho$:** observed assignment looks **less** plausible unless $\rho$ is tuned so distances work out.

Search for the $\rho$ that makes the **whole season’s** observed labels as plausible as possible under this shortcut.

### Why “pseudo”?

Because it **ignores**:

- Stub capacity dynamics ($R_j$ shrinking as seats fill)
- Random seating order
- Endogenous centroids updating during the process

It is a **Besag-style** approximation (common in network statistics when the true model is too hard).

### When it helps

| Good for | Bad for |
|----------|---------|
| Fast sanity check: “is there a $\rho$ consistent with labels?” | Being the **official** Grandchild assignment (LG) generative story |
| No seeds / no simulation loop | Matching $L_C$ distribution (doesn’t simulate full rosters) |
| Cross-check against option (a) | Alex briefing if he asked for strict configuration-model MLE |

**Recommendation:** run as **secondary audit**, not primary, unless Alex explicitly wants this as the main estimator.

---

## Option (c): Exact sequential likelihood

### Idea in plain language

Replay Grandchild assignment (LG) **exactly** as coded:

1. Shuffle player order (random permutation).
2. For each player in that order, compute weights $R_j \exp(-\rho|\hat{A}_i - \mu_j|)$ over open teams.
3. Normalize to probabilities, draw a team, update centroid $\mu_j$.
4. Multiply the probability of **each step’s choice** along that order.

For **empirical** data, you don’t know which permutation NCAA “used.” So you must either:

- **Average** over many random orders (expensive), or
- **Sum** over all permutations (impossible at NCAA scale).

### Tiny example: 3 players, 2 teams (capacities 2 and 1)

Players: A=10, B=5, C=1. Team 1 has 2 seats, Team 2 has 1 seat.

**One possible order:** B, then C, then A.

- **Step 1 (B=5):** both teams open, centroids at league mean → B lands Team 1 with some probability (e.g. 0.55).
- **Step 2 (C=1):** Team 1 centroid updates → C lands somewhere with some probability.
- **Step 3 (A=10):** only open seats left; often forced or nearly forced.

Likelihood for **this order** = product of the three step probabilities.

**Different order** (A first, then B, then C) → **different** product, because centroids evolve differently.

For empirical fit: average likelihood over many orders, or treat order as random and integrate.

### Tradeoffs

| Pros | Cons |
|------|------|
| Closest to “true” Grandchild assignment (LG) generative model | **Slow** and fiddly |
| Principled if you handle order correctly | At NCAA scale (thousands of players), brutal without serious compute |
| | Still doesn’t uniquely identify order for real data |

**Verdict for v1:** skip unless Alex insists on full generative MLE. Options (a) and (d) capture the same $\rho$ intent with far less pain.

---

## Option (d): Multi-moment simulation matching — “stronger” criterion

### Idea in plain language

Same engine as option (a) — run Grandchild assignment (LG) many times per **$\rho$** — but match **several** empirical summaries at once, not just sorting index ($H_{\mathrm{sort}}$):

1. **Sorting index ($H_{\mathrm{sort}}$)** — how sorted are teams?
2. **Global within-team sum of squares (global_wss)** — raw spread around team means
3. **Team congestion ($L_C$) distribution** — histogram of team-level congestion (see `grandchild_empirical_lc_compare.py`)

Define a **combined loss**, e.g.:

$$
\text{loss}(\rho) = w_1 \cdot |H_{\mathrm{sort}}^{\mathrm{sim}} - H_{\mathrm{sort}}^{\mathrm{emp}}| + w_2 \cdot |\mathrm{global\_wss}^{\mathrm{sim}} - \mathrm{global\_wss}^{\mathrm{emp}}| + w_3 \cdot \mathrm{distance}(L_C^{\mathrm{sim}}, L_C^{\mathrm{emp}})
$$

(simulated values = mean over 50 seeds)

Pick **$\rho$** that minimizes total loss — **per season** and **longitudinally**.

### Tiny example (made-up)

Empirical 2015 targets:

- $H_{\mathrm{sort}}^{\mathrm{emp}} = 0.12$
- $\mathrm{global\_wss}^{\mathrm{emp}} = 8200$
- $L_C$ distribution: peak near 0.45

At $\rho = 0.5$ (legacy default), 50 sim runs might give:

- $H_{\mathrm{sort}}^{\mathrm{sim}} = 0.09$ → error 0.03
- $\mathrm{global\_wss}^{\mathrm{sim}} = 9100$ → error 900
- $L_C$ peak at 0.38 → histogram distance 0.05

At $\rho = 0.9$:

- $H_{\mathrm{sort}}^{\mathrm{sim}} = 0.12$ → error 0.00
- $\mathrm{global\_wss}^{\mathrm{sim}} = 8500$ → error 300
- $L_C$ peak at 0.43 → distance 0.02

**Combined loss** might favor $\rho \approx 0.9$ even though $\rho = 0.5$ was “close enough” on sorting alone.

### Why this matches the “stronger” success criterion

- Option (a) alone: “get sorting index right.”
- Option (d): “get sorting **and** within-team spread **and** congestion shape right” — stronger claim that Grandchild assignment (LG) reproduces **structure**, not one number.

**Recommended v1 primary**, with option (b) as optional audit.

---

## Side-by-side comparison

| | **(a) Sorting calibration** | **(b) Pseudo-likelihood** | **(c) Exact sequential LL** | **(d) Multi-moment sim match** |
|--|--|--|--|--|
| **Uses simulator?** | Yes, many seeds | No | Yes, many orders | Yes, many seeds |
| **Uses observed team labels directly?** | Only for target stats | Yes, in formula | Yes, in path | Only for target stats |
| **Handles randomness?** | Average over seeds | N/A | Average over orders | Average over seeds |
| **Matches $H_{\mathrm{sort}}$?** | Yes | Indirectly | Yes | Yes |
| **Matches global_wss / $L_C$?** | Not unless added | No | Can in principle | **Yes** |
| **Implementation effort** | Low | Low | High | Medium |
| **Alex story** | “Calibrate $\rho$ to sorting” | “Approximate label likelihood” | “Full generative MLE” | “Calibrate $\rho$ to roster geometry” |

---

## How this connects to implementation choices

| Choice | Meaning |
|--------|---------|
| **50 seeds** | For (a) and (d), each $(\rho, \text{season})$ runs Grandchild assignment (LG) 50 times; report mean ± spread |
| **One $\rho$ per season + longitudinal $\rho$** | Grid search inside each season; then one pooled objective across 2011–2021 |
| **$\rho = 0.5$ reference** | Always report the same three metrics at legacy default |
| **HPC / Rivanna** | Not required to **build** the script; parallelize $(\text{season}, \rho, \text{seed})$ when seeds or grid fineness increase |

Planned outputs (when coded): `HEROs_and_PASSes/pd21_rho/` — script, JSON, plots.

---

## Suggested path forward

| Role | Option |
|------|--------|
| **Primary** | **(d)** — multi-moment simulation matching |
| **Audit** | **(b)** — pseudo-likelihood, reported alongside |

**One-liner for Alex:**

> “We calibrate Grandchild assignment’s $\rho$ so simulated rosters match empirical sorting, within-team spread, and $L_C$ shape — per season and pooled — not from draft likelihood. Draft MLE for $\lambda$ and $t$ stays on fixed empirical teams.”

---

*Charles runs PDF when ready:*

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/Alex_notes/rho_est_options_for_dummies.md
```
