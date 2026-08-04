# 2. Three kinds of “model” (why you got lost)

**Last synced:** 2026-07-28

**Audience:** Charles, re-entering  
**Standalone:** definitions are inline; no other files required.  
**Slide summary (same story):** [`Model.pdf`](Model.pdf)

---

## The mistake that feels like failure but is not

You kept hearing “the model” and assumed one equation should do everything: fit the hero, explain NBA psychology, simulate a league, and satisfy Alex — all at once.

This project actually uses **three different objects**. They stack, but they are **not the same thing**. Confusion came from switching layers mid-sentence — not from you being unable to do math.

---

## BINDING insight — environment ≠ advancement; score ≠ select (#1 confusion)

Charles lock (Jul 2026; sharpened Jul 2026). Full binding doc: [`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md).

You were merging mechanisms that must stay separate:

1. **Environment / development** — peers affect you through benefit (B) and congestion (D). The **combined environment object** is **`L_net = B − D`**. This **describes the peer environment**, not who wins the slot.
2. **Advancement** — who gets the scarce slot — itself has **two** pipeline steps:
   - **Scoring** — rank candidates: **`S_i = A_i − λ·L_C`** (**λ** lives here).
   - **Selection (winner rule)** — turn ranks into winners: **top K** in v1 (later: soft / stochastic draw).

| | Environment (`L_net` = B − D) | Scoring (`S_i`) | Selection (winner rule) |
|---|-------------------------------|-----------------|-------------------------|
| **Asks** | How do peers help vs hurt development? | How do we **rank**? | Given ranks, **who wins**? |
| **Knob** | (theory; not estimated in v1) | **λ** | Top K now; noise later |
| **Hero plot** | Does not separate channels | Shows **outcome only** | — |
| **Sim** | Who lands on which roster | Build **`S_i`** | Draft by winner rule |

**Carry this sentence:** *The hero describes outcomes; **`L_net`** is the peer environment; advancement = **score** then **select**; the sim tests whether the **weight λ on L_C in the score** changes who gets selected under a fixed winner rule.*

Layer C is powerful because it **names score and select as steps** — talent-only score vs congestion-in-score, same top-K — instead of hiding advancement inside a giant environment model.

---

## Layer A — describe the curve (phenomenology)

**Job:** Answer *“What does the data look like?”*

**Tools:** Bin the real panel. Optionally fit a simple curve (e.g. draft probability vs pool quality plus its square).

**Basketball example:** The hero plot and a quadratic regression on the same filtered rows.

We fit a **quadratic** (not a line) because the hero bends at the top — it is the simplest way to ask whether draft rate is **concave** in pool quality (negative squared term) and to draw a smooth overlay on the bins. We are **not** claiming NBA teams use that formula; the **binned hero** stays the headline stylized fact.

**Why the quadratic LPM is still useful (brief):** Fit `Y ≈ β₀ + β₁Q + β₂Q²` on the same hero rows (**LPM** = linear probability model = OLS on a 0/1 draft outcome). Then:

- **`β₂ < 0`** ⇒ fitted curve is **concave down** (inverted-U / hill); **`β₂ > 0`** ⇒ **concave up** (U).
- One turning point at `Q* = −β₁/(2β₂)` — a **local max** if `β₂ < 0`, a **local min** if `β₂ > 0`.
- A pure quadratic has **no inflection point** (second derivative is constant). Do not claim inflection from this fit.
- Speak about the **fitted quadratic**, not “the data are definitively a parabola.” Fitted values can leave `[0, 1]` — fine for **shape**, not a full probability model. Mechanism remains Layer B/C.

**What success looks like:** Negative curvature — draft rate bends down at the top bins — on the **locked** hero definition (16 bins, leave-one-out quality, minutes filter, seasons 2011–2021).

**What this does NOT prove:**

- Why the curve exists.
- That NBA teams use our formula.
- That simulation must match bin-by-bin.

**Analogy:** Layer A is a **weather report**. It records the shape of the cloud. It is not a **theory of rain**.

---

## Layer B — explain help vs hurt (mechanism story)

**Job:** Answer *“Why could good peers both help and hurt?”* — and **separate environment from advancement** (and, inside advancement, **score from select**).

**Tools:** Words and symbols — not one estimated equation in v1.

### Part 1 — Environment (B minus D)

Net value from the peer environment splits into two parts that **pull in opposite directions**:

- **B (benefit)** — upside from good peers: development, visibility, playing in a strong context.
- **D (congestion / dilution)** — downside from good peers: harder to stand out, more competition around you.

Write this as **`L_net ≈ B − D`** (net local environment). As pool quality rises, **both** B and D can increase. Early on, benefit may dominate (draft rate rises). At the very top, **congestion can catch up or outweigh benefit** — a story for why the hero tail **might** dip. In v1 we are **not** estimating separate B and D curves from data.

**This part describes the environment — not who gets drafted.**

### Part 2 — Advancement: score, then select

**Advancement is separate from environment.** After rosters exist, someone must decide **who gets the scarce slot**. That happens in **two** steps:

1. **Scoring** — compute a rank for each player.
2. **Selection (winner rule)** — pick winners from those ranks (v1: **top K**; later: soft / stochastic draw).

**Alex’s equation is about scoring**, not the full environment and not the winner rule:

- **`S_i = A_i − λ·L_C`** — own **ability** minus **weight × viable-peer congestion** in the **score** (equivalently **`S_i = A_i + λ(B−D)`** with **(B−D) = −L_C** in the score for Alex v1)
- **`L_C`** — **D-ish** congestion measured **LOO on a roster** after assignment; not full **`L_net`**, not **`L_C = f(B, D, ρ)`** in v1
- **λ** — weight on congestion **in the score only**

That is why the simulation makes advancement explicit: assign → **score** → **select (top K)**. **Knockout** (repo shorthand — say **mechanism contrast** to Alex if you prefer): hold the fake league **and the winner rule** fixed; **remove congestion from the score**. Compare top-**K** on **`S_i = A_i`** only (λ = 0) vs top-**K** on **`S_i = A_i − λ·L_C`**. The **one ingredient toggled** is **`L_C` in the score** — not talent, not top-K, not the whole **`L_net`** environment.

**What success looks like:** The story is coherent; sim shows ability-only **scoring** fails the congestion-in-score story when λ = 0.

**What this does NOT prove in v1:**

- Separate measurement of B(Q) and D(Q) on one axis.
- That real NBA front offices compute Alex’s score literally.
- That the hero curve proves the scoring channel only (hero is outcome; channel is theory + sim).

**In plain terms:** Layer B Part 1 = environment (B − D). Layer B Part 2 = **score (`S_i`) then select (top K)**. Layer C = **run those steps in code**.

### Unified nesting — how the pieces fit (beyond v1)

One way to **nest** the symbols without merging layers:

**General score:** **`S_i = A_i + λ·(B − D)`** (ability plus weighted net local environment **in the ranking**).

| Restriction | Meaning | Score |
|-------------|---------|--------|
| **Knockout** | **λ = 0** — remove all of **(B − D)** from the **score** | **`S_i = A_i`** |
| **Alex v1** | Only congestion enters the **score**: **(B − D) = −L_C** (not “B is zero in the world”) | **`S_i = A_i − λ·L_C`** |
| **Full (later)** | **λ ≠ 0** with both B and D in **(B − D)** | Richer; **not** what v1 runs |

**Full generative pipeline** (Layer C — Charles’s three steps):

```
Draw A_i  →  assign to rosters (ρ)  →  compute LOO poolq_loo, L_C on rosters
       →  score: S_i = A_i + λ(B−D)  [v1: (B−D)=−L_C]
       →  select: top K  [later: stochastic winner rule]  →  bin for plots
```

| Knob | Step | Role |
|------|------|------|
| **ρ (rho)** | **Assignment** (who lands where) | **Assortativity** in soft match to team targets **T_j**; **ρ=0** = max mixing; **ρ↑** = sharper match; **not** inside **`S_i`** |
| **λ** | **Scoring** | Weight on **(B − D)** in **`S_i`**; v1 knocks out via **λ = 0** or sets **(B − D) = −L_C** |
| **Top K / noise** | **Selection (winner rule)** | How ranks become winners; v1 = deterministic top K |
| **B, D** | **Environment (theory)** | **`L_net = B − D`** — help vs hurt among peers; not separately estimated in v1 |
| **`L_C`** | **Computed on rosters** after assignment | **D-ish** operational congestion (LOO viable-peer crowding, e.g. `crowding_smooth`) — **not** the same object as full **`L_net`**, and **not** a clean formula **`L_C = f(B, D, ρ)`** |

**Minimal generative claim (Alex v1):** some **roster step** (so LOO stats exist) **and** **score → select** (congestion in vs out of **`S_i`**, same top-K). **Calibrating ρ** to 530 or matching hero bins is **not** the v1 gate.

**Hero mapping (stay honest):** The hero is **Layer A outcome** — mean draft rate by **`poolq_loo`** on the **real panel**. It **motivates** the story; it does **not** identify **(ρ, λ, B, D)** or prove **`S_i`** is the NBA rule. **`poolq_loo`** is a **pool proxy**, not measured **(B − D)**.

**`L_C` and θ (viability cutline):** On a roster, **`L_C`** = LOO congestion from **viable peers**. **θ** = viability threshold (530 default: **med(perf | ever drafted)**). **Hard:** count teammates with **`A_j > θ`**. **Smooth (default):** LOO mean of **`σ(γ(A_j − θ))`** (`crowding_smooth`). **γ** = sharpness of the sigmoid around θ.

**Optional follow-up (Alex asked Jul 2026):** **ρ** sim ablations — fix **score and winner rule**, vary assignment assortativity — test “is sorting involved?” **Not** required for v1 minimal model; the headline knockout is **λ = 0** vs **(B−D)=−L_C** in **`S_i`** (already run; see doc 03).

---

## Layer C — simulate a fake league (generative proof-of-concept)

**Job:** Answer *“If we write explicit draft rules, does congestion in the score change who gets picked?”*

**Tools:** Thin `540_*` / scripts (archived 538D is reference only): create synthetic players → assign to teams → **score** → **select** (top K) → plot draft rate by bins.

**Headline comparison (knockout on `L_C` in the score; winner rule fixed):**

- **Knockout arm (λ = 0):** **`S_i = A_i`** — congestion **removed** from the **score**.
- **Full rule for this test:** **`S_i = A_i − λ·L_C`** — same league, same top-K, congestion **in** the score.

**What success looks like:** The two **scoring** rules produce **different shapes** under the same winner rule — especially, talent-only scoring fails to show the “congestion story.”

**What this does NOT prove:**

- Point-for-point match to every hero bin.
- That the real draft **is** this simulation.

**Analogy:** Layer C is a **wind-tunnel model**. It shows a mechanism **can** produce bent curves. It is not claiming the wind tunnel **is** the sky.

---

## How the three layers stack (one picture in words)

```
Real NCAA data  →  Layer A  →  "Here is the hero curve (outcome only)"
       ↓
Story in prose  →  Layer B  →  "Environment: L_net (B−D); Score: S_i; Select: top K; nest (B−D)=−L_C in score for v1"
       ↓
Fake league code →  Layer C  →  "Assign (ρ) → score (λ, L_C) → select (top K); knockout λ=0"
       ↓
Alex slide       →  Model.pdf + hero PNG beside sim PNG + limitation sentence
```

You do **Layer A** first (mostly done). You need **Layer C minimal** for the simplified model deadline. **Layer B** has environment (B − D) plus **score then select** — you are not failing if you have not “estimated Layer B” as one formula.

---

## What Alex side-by-side actually means (v1)

Not: “Sim reproduces hero exactly.”

Yes:

- Same **kind** of Y-axis (advancement / draft rate).
- **Honest** X-axis labels (empirical leave-one-out quality vs sim bins on the best matching axis you have).
- One clear **limitation sentence**: we show congestion in the **score** can bend who gets selected under top-K; we do **not** claim bin-for-bin replication yet.

That is enough for the simplified model chapter of work.

---

## Notation landmines (same symbol, different day)

While re-entering, ignore cross-domain notation. For **basketball v1 only**, use this cheat sheet:

| Symbol / term | Meaning **here** | Ignore for now |
|---------------|------------------|----------------|
| **`L_net`** | Net peer environment = **B − D** (help minus hurt among peers) | Any other “L” in old emails |
| **`S_i`** | **Score** (Alex) — ranking for advancement; **not** the winner rule | Hero regression coefficients |
| **Selection** | **Winner rule** — top K now; later stochastic draw from scores | Calling **`S_i`** “selection” |
| **`L_C`** | LOO **viable-peer congestion** on a roster (used in **`S_i`**); D-ish, not full **`L_net`** | Network centrality papers |
| **θ (theta)** | Viability cutline for “substitutable peer” — e.g. **med(A \| drafted)** | Generic threshold in other domains |
| **γ (gamma)** | Sharpness of **`σ(γ(A_j − θ))`** in smooth **`L_C`** | — |
| **ρ (rho)** | Assignment **assortativity** — soft match to team targets **T_j**; **ρ=0** = max mixing; **not** inside **`S_i`** | Legacy **τ (temperature)** in archived docs (opposite intuition) |
| **Knockout** | Same league + same winner rule; **`L_C` removed from the score** (λ = 0) vs Alex score with it **in** | “Mechanism contrast” to Alex |
| **BINDING** | **`L_net`** ≠ advancement; **score ≠ select**; hero ≠ scoring equation | — |
| Pool quality (LOO) | Leave-one-out teammate quality | Army “poolq” without LOO |
| Ability (`A_i`) | Player talent in sim / own perf in data | Tenure “productivity” |
| **λ (lambda)** | **Weight** on **`L_C`** in score: \(S_i = A_i - \lambda L_C\) (**λ** is not L_C itself) | — |
| **K** | **Selection capacity** — count of winners (top-K); code: `n_selected` | Old memos used **Λ** for this — retired |
| **K/N** | Selectivity rate (system feature); characterization default **10%** | MBB draft ~**1%** is a domain point, not the general baseline |
| Hero | Empirical binned draft plot | Any other “hero” in old emails |

When a doc uses shorthand without re-defining, **close it** and come back to this table.

---

## Notation addendum (Aug 2026) — read before Phase B

**Purpose:** One page so **λ**, **K**, and **K/N** stop swapping roles. Full threshold notes: [`06_Lambda_threshold_and_KN_memo.md`](06_Lambda_threshold_and_KN_memo.md).

### Score vs select (BINDING)

| Step | Symbol | Plain English | Code |
|------|--------|---------------|------|
| **Score** | **λ** | **Weight** on congestion in the score — how much **L_C** is subtracted from **A_i** | `loo_gap_weight` |
| | **L_C** | Viable-peer congestion (built with **θ**, **γ**) | `pool_c_smooth_loo` |
| | **S_i** | Ranking number: \(S_i = A_i - \lambda L_C\) | `selection_weight` |
| **Select** | **K** | How many get **Y = 1** (top-K) | `n_selected` |
| | **K/N** | Selectivity rate — **system feature** | `K / (n_teams × roster_size)` |

**λ is not “the congestion.”** Congestion is **L_C**. **λ** is only the **weight** on that term in **S**.

**K is not λ.** **K** counts winners after scoring. Old memos used **Λ** for **K** — retired.

### Characterization defaults (gallery)

| Preset | N | K | K/N | When to use |
|--------|---|---|-----|-------------|
| **`characterization`** (default) | 5600 | 560 | **10%** | Phase B knob sweeps |
| **`mbb_draft`** | 5600 | 56 | **~1%** | Domain calibration (later) |
| **`army_high`** | 5600 | 2240 | **40%** | High-selectivity regime (explore) |

Set via `GALLERY_K_OVER_N` or `GALLERY_N_SELECTED` (see `sports/scripts/gallery_knobs.py`).

### θ — do not set by rule until tested

**θ** = center of σ(γ(A−θ)) when building **L_C** (who counts as a “viable peer”).

- **539 sim default:** θ = 0.72 on [0,1] Beta **A** (Alex reference JSON).
- **530 empirical:** θ ≈ med(perf | ever drafted) on ppm **z** — different scale.

**Open (PD15):** Does θ **co-vary with K/N**? Run **θ × K/N panel** *before* adopting any fixed rule for θ. Script: `sports/scripts/theta_kn_sweep_diagnostic.py`.

### γ, ρ (unchanged)

- **γ** — sharpness of viability sigmoid (not assignment).
- **ρ** — assignment assortativity (not inside **S_i**).

### λ_crit (sort-and-chop benchmark)

**Critical λ** = first λ where **score ranking** (\(S_i = A_i - \lambda L_C\)) differs from **talent-only ranking** — not “when congestion feels big.” Full derivation and the **θ-straddle team** picture: [`06_Lambda_threshold_and_KN_memo.md`](06_Lambda_threshold_and_KN_memo.md) § Critical λ, § The θ-straddle team.

---

## What to tell yourself when reading old memos

If a one-page memo assumes you already know which layer is which, it will feel like gibberish. That is a **format mismatch**, not missing intelligence.

**While lost:** read only re_entry docs 01–03.  
**When steady:** optional short memos become useful again.

**Next:** [03_Three_Day_Basketball_Focus.md](03_Three_Day_Basketball_Focus.md)
