# MBB — park homophily, replay draft selection on real rosters

**Last synced:** 2026-08-28

**Audience:** Charles (slow read / print). Summary of Aug 28 conversation with Alex after PD28 porch + calibration work.

**Standalone:** On men’s college basketball (MBB), we treat homophily as ~0, keep real players on real teams, fit score knobs on that frozen world, simulate who gets drafted, and compare the resulting HERO plot to empirical data.

---

## In plain language first

We spent a lot of time on **homophily** — the idea that similar players end up on the same teams. On MBB, the data keep saying: **there isn’t much of that.** Empirical $\rho$ is about **zero**. So does **found assortativity** ($H_{\mathrm{sort}}$): only about **6%** of ability variance is explained by which team you’re on. Alex’s reaction: *maybe homophily needs a rethink someday* — but **not this week.**

The productive move for MBB is narrower and honest:

1. **Take the real world as given** — real players, real teams, real season abilities ($\hat{A}_i$ from PPM, etc.).
2. **Do not** build a fake league and try to re-assign people with $\rho$.
3. **Fit** how drafting *scores* people: $\gamma^*$, $\lambda^*$, and temperature (how sharp the ranking is).
4. **Simulate** who gets drafted using those fitted knobs.
5. **Plot** the same HERO readout we already use empirically — draft rate vs leave-one-out (LOO) teammate quality — and ask: **does the model shape look like the data?**

That is **score → select** on a **fixed roster**. It is not “we rebuilt college basketball from scratch.” It is: *given this locker room, does our draft mechanism produce the right kind of crowding story?*

---

## Baby examples

### Example A — The restaurant brigade (fixed ASSIGN)

Imagine a kitchen with **fixed stations** (teams). Everyone’s already placed. You are **not** asking “should the sauté cook swap stations?” ($\rho$, homophily). You’re asking: “Given who is already on the line, **who gets promoted to head chef**?” (draft / advancement).

- **ASSIGN** = who works which station → **frozen** (empirical rosters).
- **SCORE** = how valuable each cook looks given their peers → fit $\lambda$, $\gamma$, $t$.
- **SELECT** = who actually gets promoted → simulate draftees.
- **HERO** = graph: “As local talent around you goes up, does promotion rate go up forever, peak and fall, or something else?”

On MBB with PPM, the empirical HERO is often **flat or monotone** — not a dramatic inverted-U. The **generative** model *can* show an inverted-U at some $(\lambda, t)$. The replay test is whether **calibrated** sim draftees land in the same **shape family** as data.

### Example B — Why $\rho \approx 0$ is a parking ticket, not a failure

Suppose team assignment were random. Then $H_{\mathrm{sort}} \approx 0$. Our bracket says $\rho^* \approx 0$. That is **consistent**: “don’t simulate strong homophily on this domain.”

Trying to **force** $\rho$ to move when $H_{\mathrm{sort}}$ is flat is like tuning a volume knob that isn’t wired to the speaker. You can turn it; nothing useful happens. **Park it.**

### Example C — What “generate draftees” means here

**Not:** invent 5,000 new players and assign them to Duke and Kansas.

**Yes:** for each **real** 2009–2021 player-season on a **real** roster, compute a draft probability or run a selection rule, draw **simulated** draft flags $Y^{\mathrm{sim}}_i$, then bin by LOO pool quality exactly like Pass A.

Compare:

- Empirical: $\hat{P}(Y{=}1 \mid \mathrm{LOO\ bin})$
- Simulated: $\hat{P}(Y^{\mathrm{sim}}{=}1 \mid \mathrm{LOO\ bin})$

Same bins. Same aperture. Side by side.

---

## What Alex proposed (one paragraph)

Park homophily for MBB. Instead of generating a league from an $A_i$ distribution and using $\rho$ for assignment, **use empirical data and empirical teams**, fit $\lambda^*$, $\gamma^*$, and temperature $^*$, plug those into the model, **generate draftees**, and inspect the **HERO plot**. Does that make sense? **Yes** — and it aligns with what PD21 MLE already started (fit on fixed rosters). The missing piece is a clean **generative SELECT → HERO** replay, not another $\rho$ bracket.

---

## Why this is the right move for MBB

| Old wind-tunnel habit | Problem on MBB |
|----------------------|----------------|
| Draw synthetic $A_i$, LG-assign with $\rho$, match $H_{\mathrm{sort}}$ | $\rho^* \approx 0$; bracket has **no slope** |
| Full synthetic league | ASSIGN layer adds noise, not identifiable signal |

| Alex proposal | What it buys |
|-------------|--------------|
| **Empirical rosters + empirical $\hat{A}_i$** | No fake homophily; no $\rho$ algebra |
| Fit **$\lambda^*$, $\gamma^*$, $t^*$** on that panel | SCORE layer still has bite |
| **Generate draftees** → HERO | Tests **SELECT** vs empirical Pass A |

**Army** can keep the full ASSIGN → SCORE → SELECT ladder later. **MBB** becomes: *empirical environment, generative selection.*

---

## What we already have (not starting from zero)

Reigning hero sandbox, 2009–2021, min20, mg10, PPM z:

| Piece | Status | Where |
|-------|--------|-------|
| $\rho^* \approx 0$ (H_sort bracket) | Done | `sports_sandbox/reigning_hero/calibration/rho/` |
| $\gamma^* \approx 19.57$, $\lambda^* \approx 1.30$, $t^* \approx 1.07$ | Done | `.../calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json` |
| Gibbs SELECT temperature sweep | Done | `.../calibration/temperature/` |
| Empirical HERO (last-ps, LOO, EW16) | Done | porch + reigning hero lock in `reigning_hero/README.md` |
| **Sim HERO replay (Gibbs v1)** | **Done (Aug 28)** | `reigning_hero/sim_hero/` · `reigning_hero_sim_hero.py` |
| **Gap** | **Sensitivity + axis alignment** | LOO in SCORE? multi-seed $\beta_2$ bands? F-HERO dual readout |

PD28 notes: `transcripts/PD28_notes.md`  
Campaign compare: `sports_sandbox/reigning_hero/calibration/CAMPAIGN_COMPARE.md`

---

## Binding rules (still apply)

From project binding docs — short version:

1. **Environment** ($L_{\mathrm{net}} = B - D$) $\neq$ **advancement**.
2. **Score** ($S_i = A_i - \lambda L_C$, etc.) $\neq$ **select** (who actually gets drafted).
3. **Hero** = outcomes; do not merge into “one model” in prose.

Alex’s plan respects this: fit **score** knobs on fixed rosters; **then** run **select**; **then** read **hero** (HERO plot). Three steps, named separately.

---

## Deep dive — softmax, Bernoulli, Gibbs, and the two “temperatures”

**Charles, read this slowly.** This is the piece that confused the “open question” wording. Short answer: **you already decided a lot.** Bernoulli and softmax are **not** two competing draft models. Gibbs is **not** a replacement for Bernoulli. They live at **different steps** in the pipeline. You use **both**, for **different jobs**.

### The pipeline in one breath (frozen MBB rosters)

Think of four steps on **real** teams:

```
ASSIGN (frozen)  →  SCORE  →  turn scores into chances  →  SELECT  →  HERO plot
empirical teams     S_i, λ, γ      softmax + maybe t*          who drafts?     draft rate vs LOO
```

- **ASSIGN:** Parked for MBB ($\rho \approx 0$). Rosters are **given**.
- **SCORE:** How good is each player **relative to local context**? $S_i = A_i/t - \lambda L^C$ (PD21 board form).
- **Softmax:** Turn scores into **probabilities** $p_i$ that sum to 1 within each draft season.
- **Bernoulli (fitting only):** How we **learn** $\lambda$, $\gamma$, $t$ by comparing $p_i$ to actual draft outcomes $Y_i$.
- **SELECT (generative replay):** How we **simulate** new draftees for the HERO plot — top-$K$, Bernoulli draws, or **Gibbs** $K$ draws.
- **Gibbs $t$:** Temperature on the **SELECT** step only — how noisy the draft lottery is **after** scores are fixed.

### Formula sheet (copy-paste reference)

**Indices:** player $i$, draft season $s$, team $j(i)$. Draft indicator $Y_i \in \{0,1\}$.

#### Step 0 — Frozen ASSIGN (MBB reigning)

Teams and teammates are **observed**. No grandchild (LG) sim. Homophily $\rho \approx 0$ parked.

#### Step 1 — Ability and local context

| Symbol | Meaning (reigning lock) |
|--------|-------------------------|
| $A_i$ | PPM z-score (winsorized LOO panel) |
| $L^C_i$ | Local crowding / pool context (**MLE uses** `pool_c_smooth_team`; **HERO x-axis uses** `poolq_loo`) |
| $\gamma$ | Viability sharpness — enters **construction** of $L^C$, not inside the softmax line |

#### Step 2 — SCORE (Alex board, PD21 **fitting**)

PD21 **board logits** (per player-season):

$$
\eta_i \;=\; \frac{A_i}{t_{\mathrm{MLE}}} \;-\; \lambda\, L^C_i
$$

**Important:** this is **not** $(A_i - \lambda L^C_i)/t_{\mathrm{MLE}}$. Ability is scaled by $t$ **before** subtracting congestion. (Grandchild SELECT sweeps use the other order — see below.)

Conceptual Alex score (binding doc):

$$
S_i \;=\; A_i \;-\; \lambda\, L^C_i
$$

Think of $\eta_i$ as “$S_i$ with an extra $1/t_{\mathrm{MLE}}$ on talent only.”

#### Step 3 — SOFTMAX (within each draft season $s$)

For all players $i$ in season $s$:

$$
p_i \;=\; \frac{\exp(\eta_i)}{\sum_{k \in s} \exp(\eta_k)}
\qquad\Rightarrow\qquad
\sum_{i \in s} p_i = 1
$$

So $p_i$ are **relative draft weights** in that season, not independent Bernoulli probabilities yet.

#### Step 4 — BERNOULLI likelihood (how we **fit** $\lambda, \gamma, t_{\mathrm{MLE}}$)

Treat each $Y_i$ as an independent Bernoulli trial with “success” probability $p_i$:

$$
\ell(\lambda, \gamma, t_{\mathrm{MLE}})
\;=\;
\sum_i \Big[ Y_i \log p_i + (1-Y_i)\log(1-p_i) \Big]
$$

We maximize $\ell$ over $(\lambda, \gamma, t_{\mathrm{MLE}})$. **Reigning fit:**

$$
\gamma^* \approx 19.57,\quad \lambda^* \approx 1.30,\quad t^*_{\mathrm{MLE}} \approx 1.07
$$

**Softmax + Bernoulli are partners:** softmax builds $p_i$; Bernoulli scores them against real $Y_i$.

#### Step 5 — SELECT (generative replay — **three options**)

After parameters are fixed, simulate draft flags $Y^{\mathrm{sim}}_i$. Let $K_s$ = number of actual draftees in season $s$.

**A. Deterministic top-$K$**

$$
Y^{\mathrm{sim}}_i = 1 \quad \text{iff } i \text{ is among the } K_s \text{ largest } p_i \text{ (or } \eta_i\text{) in season } s
$$

**B. Bernoulli replay** (matches fit likelihood literally)

$$
Y^{\mathrm{sim}}_i \sim \mathrm{Bernoulli}(p_i) \quad \text{independently}
$$

Class size $\sum_i Y^{\mathrm{sim}}_i$ is **random** (not fixed at $K_s$).

**C. Gibbs rule D** (PD20 / temperature sweep — **separate** $t$)

First compute Alex score (grandchild convention):

$$
S_i = A_i - \lambda^* L^C_i
$$

Gibbs weights and $K_s$ draws **without replacement**:

$$
w_i \propto \exp\!\left(\frac{S_i}{t_{\mathrm{Gibbs}}}\right),
\qquad
\text{draw } K_s \text{ players with } \Pr(i \text{ picked}) \propto w_i
$$

Sweep: $\log_{10} t_{\mathrm{Gibbs}} \in [-3, 3]$ (reigning calibration folder).

#### The two temperatures — side by side

| | **$t_{\mathrm{MLE}}$** (PD21) | **$t_{\mathrm{Gibbs}}$** (PD20 SELECT) |
|---|-------------------------------|----------------------------------------|
| **Where** | Inside $\eta_i = A_i/t - \lambda L^C$ before softmax | Inside $\exp(S_i/t)$ at SELECT |
| **Fitted?** | Yes — $t^* \approx 1.07$ | No — swept on a grid |
| **Effect** | Sharpens **spread of $p_i$** from ability | Adds **lottery noise** after scores exist |

#### Step 6 — HERO readout (not part of fit)

Bin players by leave-one-out pool quality $\mathrm{poolq}^{\mathrm{LOO}}_i$ (EW16), plot draft rate vs bin. Compare empirical $Y_i$ to sim $Y^{\mathrm{sim}}_i$. **Score and select do not appear in the HERO formula** — HERO is an outcome diagnostic.

$$
\text{HERO bin } b:\quad
\hat{r}_b = \frac{\sum_{i \in b} Y_i}{\lvert b \rvert}
$$

### What are “board logits”? (plain language)

It might sound like jargon, but the idea is simple.

**Logits** = the **raw scores** you feed into softmax **before** they become probabilities. They can be any real numbers (positive, negative, large, small). Softmax turns them into $p_i$ that sum to 1 within each draft season.

**Board logits** = Alex’s name for those raw scores on the **draft board** — the within-season table of “who gets how much draft mass this year.” **“Board”** is whiteboard language from PD21 (`pd21_draft_bernoulli_mle.py`), not a separate math object.

#### The one formula (same as Step 2)

For player $i$ in draft season $s$:

$$
\eta_i \;=\; \frac{A_i}{t_{\mathrm{MLE}}} \;-\; \lambda\, L^C_i
$$

We write $\eta_i$ or $\mathrm{logits}_i$ interchangeably. Code: `board_logits(ability, lc, lam=lam, t=t)` returns $A/t - \lambda L^C$.

| Piece | Meaning |
|-------|---------|
| $\eta_i$ | Board logit for player $i$ |
| $A_i$ | Ability (PPM z) |
| $L^C_i$ | Local crowding (`pool_c_smooth_team` in the MLE) |
| $\lambda$ | Congestion weight in the ranking |
| $t_{\mathrm{MLE}}$ | MLE temperature on ability only |

**Higher $\eta_i$** → player looks better on the board → **higher** $p_i$ after softmax.

#### Why “logits” and not just “Alex score”?

Conceptual Alex score is $S_i = A_i - \lambda L^C_i$. Board logits are a **reparameterization** for the draft-probability step:

$$
p_i \propto \exp(\eta_i)
= \exp(A_i/t_{\mathrm{MLE}})\cdot \exp(-\lambda L^C_i)
$$

So the board **factorizes** into:

- a **talent** term: $\exp(A_i/t_{\mathrm{MLE}})$
- a **congestion penalty**: $\exp(-\lambda L^C_i)$

“Logits” means: the number **inside** the exponential (up to an additive constant per season). Only **differences** between $\eta_i$ matter for within-season ranking; adding the same constant to everyone does not change $p_i$.

Then softmax makes proper probabilities (Step 3):

$$
p_i = \frac{\exp(\eta_i)}{\sum_{k \in s} \exp(\eta_k)}
$$

Bernoulli fitting (Step 4) asks whether real draft outcomes $Y_i$ match these $p_i$.

#### Baby numeric example (three players, one season)

Fix $\lambda = 1.3$, $t_{\mathrm{MLE}} = 1.07$:

| Player | $A_i$ | $L^C_i$ | $\eta_i = A_i/1.07 - 1.3\,L^C_i$ |
|--------|-------|---------|-----------------------------------|
| Star | 2.0 | 0.5 | $\approx 1.22$ |
| Mid | 0.5 | 0.0 | $\approx 0.47$ |
| Role | $-0.5$ | 1.0 | $\approx -1.77$ |

Softmax → roughly $p \approx (0.62,\, 0.33,\, 0.05)$ (sums to 1).

- **Logits** = $(1.22,\, 0.47,\, -1.77)$ — pre-probability board scores
- **$p_i$** = $(0.62,\, 0.33,\, 0.05)$ — post-softmax draft shares

#### What board logits are **not**

- **Not** probabilities (they do not sum to 1; Role’s logit is negative).
- **Not** the same as Gibbs SELECT weights (those use $S_i = A_i - \lambda L^C$ and a **different** $t_{\mathrm{Gibbs}}$ at SELECT).
- **Not** $(A_i - \lambda L^C_i)/t_{\mathrm{MLE}}$ — PD21 puts $1/t$ on **$A$ only**, not on the whole score.

**One-liner:** *Board logits are the draft-board raw scores $\eta_i = A_i/t_{\mathrm{MLE}} - \lambda L^C_i$ that softmax turns into season draft probabilities $p_i$.*

**See also:** [`_DISPOSABLE_PD25_Alex_board_for_dummies.md`](../../_DISPOSABLE_PD25_Alex_board_for_dummies.md) (standalone PD25 glossary).

### Baby example — graduate admissions (same logic)

**Frozen ASSIGN:** Students are already at specific colleges. We are **not** moving them to new schools.

**SCORE:** Each senior gets a composite $S_i$ from GPA ($A_i$) minus “how crowded your major cohort is” ($\lambda L^C$).

**Softmax (within application year):** Convert scores to **shares** that add to 100%:

- Alice $S=2.0$ → $p_{\mathrm{Alice}} = 8\%$ of “admit weight”
- Bob $S=0.5$ → $p_{\mathrm{Bob}} = 2\%$
- … everyone in the year sums to 100%

Those $p_i$ are **not** literal independent admit probabilities in the real world — they are a **mathematical device** so that better scores get more mass in a **closed** draft season.

**Bernoulli (how we FIT):** PD21 asks: *if each student were independently admitted with probability $p_i$, how well does that explain who actually got in?* We tune $\lambda$, $\gamma$, $t$ until the Bernoulli log-likelihood is happy. **This is calibration, not the generative story Alex tells at the whiteboard.**

**SELECT (how we GENERATE for HERO replay):** When Alex says “generate draftees,” he means **pick winners**. Three flavors:

| Mechanism | What happens | Draft class size |
|-----------|--------------|------------------|
| **Top-$K$** | Take the $K$ highest $S_i$ (or $p_i$) | Exactly $K$ (matches NBA draft count) |
| **Bernoulli replay** | Each player drafted with probability $p_i$ independently | **Random** (might be 58 or 62, not always 60) |
| **Gibbs rule D** | $K$ draws **without replacement**, weight $\propto \exp(S/t)$ | Exactly $K$, with noise |

**Gibbs $t$:** If $t$ is **small**, the highest scores almost always win (like top-$K$). If $t$ is **large**, middling players sometimes slip in — a **noisy lottery** biased toward good scores. PD20 swept $\log_{10} t$ from $10^{-3}$ to $10^{3}$ to see if **inverted-U HERO shapes** survive stochastic select.

### What you already locked (yes, you decided this)

| Decision | What it means | Where |
|----------|---------------|-------|
| **Bernoulli + softmax for FITTING** | Learn $\gamma^*$, $\lambda^*$, $t^*$ on fixed empirical rosters | PD21 Alex board · `pd21_draft_bernoulli_mle.py` |
| **Reigning numbers** | $\gamma^* \approx 19.57$, $\lambda^* \approx 1.30$, $t^* \approx 1.07$ | `reigning_hero/calibration/mle/...json` |
| **Gibbs for SELECT sensitivity** | Stochastic draft after score; sweep temperature | PD20 · `grandchild_temperature_select_sweep.py` |
| **Reigning sweep at $\rho=0$** | Inverted-U-like LOO shapes can appear at some $(\lambda, \mathrm{Gibbs}\ t)$ | `reigning_hero/calibration/temperature/` |

So when the memo said “Bernoulli **vs** Gibbs,” that was **sloppy**. Correct statement:

- **Bernoulli + softmax** = how we **fit** (already done).
- **Gibbs** = one option for how we **select** when generating sim draftees (also already in the codebase for sweeps).

You did **not** fail to choose. You chose **fit with Bernoulli** and **explore select with Gibbs**. The only open piece is: **for the empirical-roster HERO replay v1, which SELECT rule do we wire as default?**

### The two temperatures (both called $t$ — cruel but true)

Same letter, **two different knobs**:

#### Temperature #1 — MLE $t^*$ (in the **score / softmax** fit)

- **Formula (PD21 board):** logits$_i = A_i / t - \lambda L^C$, then $p_i = \mathrm{softmax}(\mathrm{logits})$.
- **Role:** Spreads or sharpens **ability** in the ranking **before** converting to $p_i$.
- **Fitted value (reigning):** $t^* \approx 1.07$.
- **Baby read:** $t$ small → superstar dominates the probability mass; $t$ large → everyone’s $p_i$ looks more equal.

This $t$ was **estimated from data** alongside $\lambda$ and $\gamma$. It is **not** the Gibbs sweep grid.

#### Temperature #2 — Gibbs $t$ (in **SELECT** only)

- **Formula:** draft weight$_i \propto \exp(S_i / t)$; draw $K$ players without replacement.
- **Role:** How **random** the draft is **after** scores exist.
- **Not** jointly re-fit in PD21 MLE. Chosen by **sweep** (PD20 / reigning temperature folder).
- **Baby read:** $t \to 0$ → always take the top $K$ scores; $t$ huge → almost a random draft among plausible players.

**Mnemonic:** **MLE $t$** = “how much does raw talent separate people in the **probability table**?” **Gibbs $t$** = “how much **luck** is in who actually gets the $K$ slots?”

### Softmax vs Bernoulli — not either/or

They stack:

1. Compute logits from $(A_i, L^C_i, \lambda, t)$.
2. **Softmax** → $p_i$ (sum to 1 per season).
3. **Bernoulli log-likelihood** → $\sum_i [ Y_i \log p_i + (1-Y_i)\log(1-p_i) ]$.

Script name says it all: `pd21_draft_bernoulli_mle.py` — **Bernoulli** likelihood on **softmax** probabilities.

We **also** report top-$K$ overlap diagnostics (do the highest $p_i$ match actual draftees?) — that’s a **check**, not the likelihood.

### What is still open (narrowly) for HERO replay v1

Not “softmax vs Bernoulli.” Not “did we pick Gibbs ever.”

**Open:** After fixing $\gamma^*$, $\lambda^*$, MLE $t^*$ on empirical rosters, **which SELECT rule produces $Y^{\mathrm{sim}}_i$ for the sim HERO plot?**

| Option | Pros | Cons |
|--------|------|------|
| **A. Top-$K$ by $p_i$** | Exact draft class size; simple | Zero randomness; not Gibbs |
| **B. Bernoulli draws from $p_i$** | Matches the **fit** likelihood literally | Variable $K$; noisy year-to-year |
| **C. Gibbs $K$-draw with chosen Gibbs $t$** | Matches PD20 generative story; tunable noise | Need one $\log_{10} t$ from sweep (e.g. where inverted-U appeared) |

**Charles lock (Aug 28):** **Gibbs $K$-draw (rule D)** is v1 default for empirical-roster replay. Top-$K$ (rule C) and Bernoulli replay are **sensitivity** runs afterward.

**Gibbs $t$:** pick from reigning temperature sweep (`reigning_hero/calibration/temperature/`); start with $t=1$ ($\log_{10} t = 0$) unless a bin tag says otherwise. Not the same as MLE $t^* \approx 1.07$.

---

## SELECT history — what did we use before?

**Short answer:** For **generative sim** (assign → score → select → HERO), **yes — almost always deterministic top-$K$ (rule C).** Gibbs (rule D) arrived with **PD20** as a deliberate upgrade/sensitivity test. **PD21 fitting** never used SELECT at all.

### Four winner rules in code (`tier1_pool_assignment.py`)

| Rule | Name | Mechanism | When we used it |
|------|------|-----------|-----------------|
| **C** | Top-$K$ | Take the $K$ highest scores $S_i$ | **Default everywhere** — `tier1_sim_config.py` `WINNER_SELECTION = "C"`; Pass A/B; 540 notebook; PD17 λ sweep; most grandchild diagnostics |
| **D** | Gibbs $K$-draw | $w_i \propto \exp(S_i/t)$, draw $K$ without replacement | **PD20+** — temperature sweep, reigning calibration; **new v1 default** for empirical-roster replay |
| **A** | Proportional sample | $K$ draws ∝ positive weights (not Gibbs) | Older 537 experiments; not main path |
| **B** | Bernoulli-ish | Independent coins, expected $\approx K$ | Older 537 experiments; not main path |

**Cold Gibbs nests top-$K$:** at very small $t_{\mathrm{Gibbs}}$, rule D collapses to rule C (see `grandchild_temperature_cold_limit_diagnostic.py`).

### Timeline (MBB modeling)

| Phase | SELECT | Notes |
|-------|--------|-------|
| **Tier1 / 540 / Pass A–B** | Top-$K$ (C) | “Score then pick the $K$ best” — BINDING v1 winner rule |
| **PD17** (`grandchild_lambda_select_sweep`) | Top-$K$ (C) | λ sweep on sim bridge; empirical roster caps |
| **PD20** (`grandchild_temperature_select_sweep`) | Gibbs (D) | **Gate:** does inverted-U survive soft/stochastic select? **Yes** → proceed to MLE |
| **PD21** (`pd21_draft_bernoulli_mle`) | **No SELECT** | Fit uses softmax → Bernoulli on real $Y_i$; top-$K$ overlap is diagnostic only |
| **Reigning calibration** | Gibbs sweep (D) at $\rho=0$ | Same PD20 machinery on 09–21 panel |
| **Empirical-roster replay (next)** | **Gibbs (D)** — Charles lock | Then sensitivity: top-$K$, Bernoulli replay |

So you were not wrong to think “top-$K$ everywhere” — that **was** the generative default for a long time. Gibbs is the intentional next step for replay, building on PD20.

---

## Open questions (remaining)

### 1. SELECT rule for sim HERO — **decided**

**Fitting:** Bernoulli + softmax (PD21) — unchanged.

**Generative replay (v1):** **Gibbs $K$-draw (rule D)** with $K_s$ = empirical draft count per season.

**Sensitivity (after v1):** deterministic top-$K$ (rule C); Bernoulli draws from MLE $p_i$.

**Open sub-choice:** which $t_{\mathrm{Gibbs}}$ from the reigning sweep (default start: $t=1$).

### 2. What is $L^C$ in the fit vs in the HERO readout?

- PD21 MLE on fixed rosters uses **`pool_c_smooth_team`** (smoothed team pool context), not necessarily raw `poolq_loo`.
- Reigning porch HERO uses **`poolq_loo`** on **PPM z** (leave-one-out teammate mean).

**Inconsistency risk:** fit on one local-context definition, plot on another.

**Fix options:** (a) refit MLE with LOO-based $L^C$ for HERO alignment; or (b) build sim HERO using the **same** $L^C$ column the MLE used. Do not mix silently.

### 3. HERO aperture must match exactly

Empirical reigning lock (slide 12):

- Seasons **2009–2021**
- **last-ps** rows for HERO bins
- **ever-$Y$** draft label
- **EW16** equal-width bins on `poolq_loo`
- **ALLT** (no +DFT filter on panel)
- min20 · mg10 · winsor 0.01–0.99 · PPM z

Sim HERO must copy this binning and row filter. Change one filter → you are comparing different objects.

### 4. Does $\gamma^*$ in the generator match the MLE file?

$\gamma$ sharpens viability / $L^C$ in the full grandchild story. Confirm the draft generator reads **reigning** `gamma_hat` from the JSON above — not a stale default in `tier1_sim_config.py`.

### 5. What this path cannot claim

With frozen rosters you **cannot** claim:

- homophily / $\rho$ calibration on MBB,
- “league formation” predictions,
- ASSIGN-layer Pass C $\rho$ ablations.

You **can** claim:

- *Given real MBB rosters, do calibrated score + select reproduce draft-vs-LOO geometry?*

That matches parking homophily.

### 6. Alternate performance metrics (SCOUT ladder)

**Kill criterion (Charles, Aug 28):** A metric is only worth switching to if it **breaks** the naive **monotone increasing** draft-rate vs LOO plot. Higher $H_{\mathrm{sort}}$ alone (BPM, TS%) is **not** enough — it may even make $\hat{A}_i$ vs LOO **more** aligned within teams.

For this replay: **keep PPM** unless SCOUT shows a non-monotone HERO on another metric.

---

## Suggested protocol (v1 — for implementation)

1. **Load** 2009–2021 empirical panel (all-ps for fitting context; last-ps for HERO comparison).
2. **Lock** $\rho = 0$ (documented; no ASSIGN sim).
3. **Lock** $\gamma^*$, $\lambda^*$, MLE $t^*$ from reigning MLE JSON (not 2013–21 campaign defaults).
4. **SELECT (v1):** Gibbs rule D, $K_s$ = empirical count, $S_i = A_i - \lambda^* L^C_i$, $w_i \propto \exp(S_i/t_{\mathrm{Gibbs}})$; sensitivity runs: top-$K$, Bernoulli replay.
5. **Align** $L^C$ definition between fit and HERO axis.
6. **Simulate** $Y^{\mathrm{sim}}_i$ on unchanged team assignments.
7. **Build sim HERO** — same EW16 LOO bins as empirical reigning hero.
8. **Side-by-side** emp vs sim: draft rate vs LOO (+ optional LPM $\beta_2$ for a scalar curvature tag).

**Deliverable name (proposed):** `reigning_hero_sim_hero/` under sandbox, script `reigning_hero_sim_hero.py` — empirical panel in, sim draft flags out, HERO PNG next to empirical.

---

## Numbers to keep on one card

| Quantity | Reigning 09–21 | Notes |
|----------|----------------|-------|
| $\rho^*$ | **0.0** | Bracket floor |
| $H_{\mathrm{sort}}$ (PPM, pooled) | **~0.064** | Weak team sorting |
| $\gamma^*$ | **~19.57** | MLE |
| $\lambda^*$ | **~1.30** | MLE (campaign was ~2.57 on 2013–21) |
| $t^*$ (MLE / softmax) | **~1.07** | Fitted in PD21; sharpens $A_i$ in logits |
| Gibbs SELECT $t$ | **1.0 (v1 lock)** | Mid-$t$ sweep: flat band; cold $t$ excluded from default overlay |
| Sim HERO LPM $\beta_2$ ($t=1$) | **≈ +0.002** | Matches emp flatness |
| Sim ever-drafted (last-ps) | **617** | Emp **615** |
| Empirical HERO LPM $\beta_2$ | **~+0.0017** | Flat / not concave on PPM last-ps |

---

## Aug 28 end-of-day — what we learned (sim replay v1)

**Tone check:** No fireworks. Steady reality — which is what this test was for.

### Headline

**Given frozen 09–21 rosters and reigning MLE score knobs, Gibbs SELECT at $t_{\mathrm{Gibbs}} \approx 1$ reproduces a *flat* empirical LOO-HERO at roughly the right draft count.** That is a **pass on shape family** (flat vs inverted-U), not a proof that temperature cleanly tunes curvature.

### Numbers (reigning lock)

| Readout | Empirical | Sim (Gibbs $t=1$, rule D) |
|---------|-----------|----------------------------|
| Ever-drafted on last-ps | **615** | **617** |
| LPM $\beta_2$ on poolq$_{\mathrm{LOO}}$ | **+0.0017** (flat) | **≈ +0.002** (flat) |
| $K_s$ source | NBA lookup `draft_year == season` | same (not `sum(Y)` on all-ps) |

Artifacts: `reigning_hero/sim_hero/REIGNING_SIM_HERO_gibbs_t1_*` and overlay `REIGNING_SIM_HERO_gibbs_t_sweep_*_last_ps.png`.

### Gibbs $t$ sweep — what it did and did *not* show

- **Cold $t$** ($\lesssim 0.5$): $\beta_2 \approx +0.03$, left-heavy HERO — **top-$K$-like pathology** on score $S$, read out on LOO axis. Documented; excluded from default mid-$t$ overlay.
- **Mid–hot $t$** (0.75–15): all sim curves stay in a **±0.02 band** around empirical flatness; **no monotone “temperature dial”** on $\beta_2$.
- **Interpretation:** reshuffling ~617 discrete picks + **SCORE axis ≠ HERO axis** ($L^C$ from `pool_c_smooth_team` in $S$; HERO bins `poolq_loo`). Wiggling $\beta_2$ with $t$ is mostly **weak identification / bin noise**, not structured physics — except at cold $t$.
- **v1 lock stands:** $t_{\mathrm{Gibbs}} = 1$ (near MLE board temperature; best $\beta_2$ match in sweep). Not uniquely pinned by curvature alone.

### Axis mismatch (open, not a code bug)

| Layer | Object on LOO? | Notes |
|-------|----------------|-------|
| **SCORE** | No — team $L^C$ at $\gamma^*$ | `pool_c_smooth_team` in PD21 MLE |
| **HERO** | Yes — poolq$_{\mathrm{LOO}}$ | reigning slide 12 lock |

BDP porch (Aug 28): $\hat{T}_j$ wide vs LOO tight; $H_{\mathrm{sort}}^{\mathrm{team}} \approx +0.06$ but $H_{\mathrm{sort}}^{\mathrm{LOO}}$ can go **negative** (`frac_var_loo_residual > 1`). Cold Gibbs over-drafts low-LOO “big fish” — **feature of mismatch**, not implementation error.

**Next sensitivity (when ready):** SELECT with `pool_c_smooth_loo` in $S$, same $\lambda^*$; or refit MLE on LOO $L^C$. See `reigning_hero/README.md`.

### SELECT rule comparison (same replay)

| Rule | Verdict |
|------|---------|
| **Gibbs D, $t=1$** | **v1 default** — flat HERO, right $K$ |
| Top-$K$ (C) | $\beta_2 \approx +0.03$ — same cold pathology as low $t$ |
| Bernoulli replay | ~13 sim picks — wrong generative story for fixed $K$ |

### Alex one-liner (Aug 28 evening)

> On real MBB rosters we parked $\rho$, fit score on the frozen panel, and simulated draft with Gibbs SELECT. **Empirical and sim HERO are both flat** at ~617 picks; **$t_{\mathrm{Gibbs}} \approx 1$** is a reasonable lock. Temperature does **not** smoothly tune LOO curvature — score uses team congestion, HERO reads LOO. Cold select looks like top-$K$ and breaks LOO geometry; that's the main structured failure mode.

### What we did *not* get today

- A crisp “sweep $t$ → find inverted-U” story on empirical replay (empirical isn't inverted-U).
- Unique $t^*$ from $\beta_2$ alone.
- Resolution of team vs LOO in $L^C$ without a deliberate sensitivity run.

### What we *did* get

- **Generative replay pipeline** (`reigning_hero_sim_hero.py`) with sweep overlay, career cap, correct $K$.
- **Honest kill on cold-$t$ / top-$K$ as default.**
- **BDP deck** extended ($H_{\mathrm{sort}}$, residuals, T̂$_j$ vs LOO, no-winsor overlay) — explains *why* axis mismatch matters before the sim slide.

---

## SCOUT / perf-metric work (parallel, optional)

Disposable folder: `sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/`

- **H_sort ladder** asks: does another metric show more team sorting?
- **Charles gate:** only promote a metric if **draft vs LOO** is not naive monotone.
- Does **not** block the empirical-roster replay on PPM.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-28 | Alex: park homophily on MBB; fit $\lambda,\gamma,t$ on empirical teams; generate draftees; compare HERO. Document written for print/PDF. |
| 2026-08-28 | Expanded “softmax vs Bernoulli vs Gibbs” deep dive — clarify two temperatures and what is already decided. |
| 2026-08-28 | Added formula sheet ($\eta$, softmax, Bernoulli $\ell$, Gibbs weights, HERO bins). |
| 2026-08-28 | Added plain-language “board logits” glossary (after formula sheet). |
| 2026-08-28 | Charles lock: Gibbs $K$-draw (rule D) v1 for replay; SELECT history section. |
| 2026-08-28 | Implemented `reigning_hero_sim_hero.py` — Gibbs/topk/bernoulli replay in `sim_hero/`. |
| 2026-08-28 (eve) | **Sim replay v1 result:** flat emp + sim HERO; 615 vs 617 picks; $t_{\mathrm{Gibbs}}=1$ lock; $\beta_2$–$t$ oscillation = weak ID + axis mismatch. Section added above. |
| 2026-08-28 (eve) | Gibbs $t$ overlay PNG; cold $t$ pathology; BDP porch slides ($H_{\mathrm{sort}}$, LOO residuals, T̂$_j$ vs LOO no-winsor). |

---

## PDF conversion (Charles)

From repo root:

```bash
./scripts/convert_single_md_to_pdf.sh \
  "3-Master_Plan/re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md"
```

Optional narrow style if you use it elsewhere: add `pdf_styles_narrow.css` per `3-Master_Plan/re_entry/MARKDOWN_FOR_PDF_PLAYWRIGHT.md`.
