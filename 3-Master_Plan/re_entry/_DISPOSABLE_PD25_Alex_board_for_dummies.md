# DISPOSABLE — What Alex asked for (PD25) in plain English

**Purpose:** Sanity check before you interpret the P2b plots.  
**Sources:** PD25 transcript + whiteboard (`transcripts/PD25_notes.md`, `PD25_board.jpeg`).  
**Status (2026-08-21 evening):** **P2b shipped** — primary plot shows Alex’s flat-then-down on +DFT (z [2,3]). Pair with **triptych** for poolq_loo deck.  
**Delete or ignore when done** — not canonical; re_entry scratch only.

---

## 0. The one-sentence version

Alex wants a picture that says: **“Hold individual talent fixed. As team talent rises, draft chance is flat for a while — then drops once the team is so strong that too many teammates are also draft-caliber.”** That drop is **congestion**. **K/N** tells you *where on the X-axis* that story should start and *how many X-bins* you need to see it.

---

## 1. What plot — and what it is NOT

### NOT this

- **Not** the usual hero curve (draft rate vs individual ability, averaging over all teams).
- **Not** “better team → more drafts” without holding the player fixed.
- **Not** poolq_loo on the X-axis (that’s a *different* congestion microscope — P1 / triptych — peers around you excluding self).

### YES this (Alex’s whiteboard)

| Piece | Plain English |
|--------|----------------|
| **Who** | One **fixed talent slice** of players — e.g. “good college players” with PPM z between 2 and 3. Everyone in the plot is roughly the same individual quality. |
| **X-axis** | **Team talent** — mean ability on that roster season. We label it **T̂_j** (team mean PPM z). **Includes the player themselves** in the team average (BINDING-safe caption). |
| **Y-axis** | **Draft rate** — share of those player-seasons that get drafted. Same as our other BDP/CCT “mean Y_draft” plots. |
| **Population (best read)** | **+DFT** — teams that actually produce draft picks in the window. Alex cares about the draft *ecosystem*, not every D-III bench player. |

So: **same fish size, different pond strength on X, draft rate on Y.**

---

## 2. “Flat, then downturn” — what Alex means

Imagine you’re a **solid pro prospect** (fixed Â). You could land on:

- A **mediocre team** — you stand out → scouts notice you.
- A **good team** — still room to stand out → still draftable.
- An **absurdly loaded team** — five other guys look just as good → **you disappear in the crowd**.

Alex’s curve shape:

```
Draft rate
    |     ___________  ← flat “plateau” (congestion not biting yet)
    |                \
    |                 \___  ← downturn (congestion bites)
    +------------------------→  Team talent (T̂_j)
                              ↑ knee / inflection region
```

**Flat:** Moving from weak team to moderately strong team **does not** kill your draft odds (much). Being on a better program might even help visibility — but **within the fixed-Â slice** Alex first expects “roughly flat.”

**Downturn:** Only when team talent gets **high enough** that the roster is crowded with draft-quality peers does **your** draft probability **fall**. The story is **ranking / visibility**, not “bad players on bad teams get drafted.”

**Important:** Alex does **not** require a smooth slide from left to right. He requires a **regime change**: flat-ish left/middle, **lower** right tail. The **last bins** on high T̂_j are the money.

---

## 3. Inflection point — where draft probability “turns down”

**Inflection** here is **not** calculus pedantry. Alex means:

> The **team-talent level** where the curve **stops being flat** and **starts falling** — the **knee**.

On the whiteboard he wrote something like **(K/N − θ) / γ**. Translation:

| Symbol | For dummies |
|--------|-------------|
| **θ (theta)** | Viability cutoff — “how good do you have to be before scouts treat you as a real candidate?” |
| **γ (gamma)** | How **sharp** that cutoff is — soft ramp vs cliff. |
| **K/N** | **Selectivity** — draft **slots** (K) per **roster spot** (N). Tiny in NCAA (~1–2%), bigger in gallery sims (~10%). |

In the **model**, the knee location is **not arbitrary** — it ties to **how selective** the league is (K/N) and **how harsh** the viability gate is (θ, γ).

In **data (P2b)**, we **do not** fit θ and γ yet. We **look empirically**: does draft rate drop in the **high T̂_j tail** after a plateau? **Then** later (MLE / Act III) we ask whether the empirical knee lines up with (K/N − θ)/γ.

**Order Alex gave:** empirical shape **first**, model inflection **second**.

---

## 4. What K/N has to do with it

Think of a roster with **N** scholarship spots and **K** NBA draft picks relevant to that pool (order ~60 per year, but only a slice of college players compete for them — **K is small**).

**K/N** ≈ “how many draft slots per roster seat?”

- **Small K/N (real NCAA):** Very few make it. Congestion means: on an elite team, **many** guys are “good enough to notice” but **K** is tiny → **most** of them lose.
- **Larger K/N (sim default 10%):** Easier to get picked; knee shows up in different places.

Why Alex cares on the **X-axis (team talent)**:

- On a **weak team**, average teammate ability is low → even a fixed-Â player **stands out**.
- As **T̂_j rises**, teammates get better → more peers pass the “viability” zone near θ.
- When **team talent is extreme**, you’re in the “**everyone on this roster is draft-talk**” zone — but **K** hasn’t grown. That’s **congestion**: same individual Â, **lower** P(draft).

So **K/N** is the **selection pressure knob**: it marks **where on team-talent axis** the pond goes from “I’m the guy” to “I’m one of six guys.”

**NCAA twist (Alex):** K is so small that the interesting part of the curve is **far to the right** on T̂_j — “all the action happens **up here**” on the whiteboard. You have to **zoom the high team-talent tail**, not use league-wide marginals.

---

## 5. How K/N helps you pick the **number of X-bins**

Alex’s binning complaint: **blind 16 equal-count ventiles** on T̂_j **smear** the sparse top tail — everyone piles into a few fat bins, you **average away** the downturn, and the plot looks like “draft rate **rises** with team quality” (what our old plot did).

### What he wants instead

1. **Bin the X-axis on purpose** — especially **fine resolution where K/N says congestion should start** (high T̂_j tail).
2. **At least two bins after the downturn** — if the knee is in bin 23, you still need bins 24–25 to **see** the drop, not one merged “elite” bucket.
3. **Back-of-envelope floor ~20 bins** on the relevant X range — below that, Alex said he wouldn’t **expect** to resolve a downturn (use this to **prune** stupid grids, not as gospel).
4. **Tradeoff:** more bins → fewer people per bin → **noisy** cells (we flag n < 30).

### Practical recipe — expanded (Steps A, B, C)

This is the part Alex cares about **operationally**: how do we **cut up the X-axis** so the flat-then-down shape can **appear** in data instead of being averaged away?

---

#### First: why “16 equal-count ventiles” lied to us

**Ventile** = “sort everyone by T̂_j, put ~equal **number of people** in each bin.”

That sounds fair, but it is **wrong for this question** because draft-relevant team talent is **rare**:

- Most player-seasons in a fixed-Â band sit on **ordinary** teams (T̂_j not that high).
- Only a **thin slice** sits on **elite** teams (Kentucky/Duke-level mean talent).

With ventiles, bins 1–12 might span “weak → decent” teams, and bins 13–16 **all cram into the elite tail**. You get **one or two fat bins** at the top where draft rates get **averaged together** — if bin 16 mixes “great team, you stand out” with “insane team, you vanish,” the bar is **middling** and the **downturn disappears**.

Worse: ventiles **stretch** the left side (many bins where nothing interesting happens) and **compress** the right side (where Alex said “all the action happens **up here**”). You spent bin budget on the flat plateau and **ran out of resolution** at the knee.

**Equal-width** on the whole range is better but still wasteful: 20 equal bins from min T̂_j to max T̂_j means ~10 bins on the flat left you don’t need and ~10 on the tail you might still starve.

**Alex’s fix:** spend bins **where the physics is** — coarse left, **microscope on the high-T̂_j tail**.

---

#### Step A — Locate the “congestion zone” on T̂_j

**Question:** On the horizontal axis, *where* should we expect the curve to **start falling**?

**Two ways to answer** (use both; they should rhyme):

**A1. Model intuition (later we fit this; now we use it as a map)**

In the generative story, peers become “draft-viable” around viability cutoff **θ**. Congestion **bites** when so many roster slots are near or above that zone that **K** slots can’t serve everyone. On the whiteboard Alex tied the knee to **(K/N − θ)/γ**:

| Piece | Plain English |
|--------|----------------|
| **K/N** | Slots per seat — NCAA tiny (~1–2% draft rate), Army Gold Star quota same idea |
| **θ** | “Good enough to be in the conversation” |
| **γ** | How sharp that gate is |

Translate to **T̂_j**: the knee lives where **mean team talent** is high enough that **a substantial fraction of the roster** is in the draft-talk zone, but **K hasn’t increased**. That is **far right** on T̂_j for NCAA.

We don’t need the exact numeric knee to **bin** — we need to know **which half of the axis is “maybe flat” vs “where congestion could start.”**

**A2. Empirical shortcut (what P2b v0 actually did)**

Within your **fixed-Â band only** (e.g. PPM z ∈ [2, 3], +DFT, n ≈ 392):

1. Compute **T̂_j** for every row.
2. Find the **median** (50th percentile) of T̂_j in that band.

In our primary run:

- T̂_j ranges roughly **−0.44 to +0.75** (z-scores).
- **Median ≈ +0.12** — half the band sits below that, half above.

**Decision:** treat everything **below median** as “plateau hunting” (coarse bins OK). Treat everything **at/above median** as “congestion hunting” (fine bins required).

That split is **not** claiming the knee is exactly at the median — it is a **practical zoom line**: “left = probably flat; right = where Alex expects the Army/Ranger story.”

You could instead use the 75th percentile for a more aggressive tail-only zoom if the band were larger.

---

#### Step B — Minimum bin count (especially on the tail)

Define:

- **B_left** = bins on the low/mid T̂_j side (plateau region).
- **B_tail** = bins on the **high T̂_j side only** (congestion region).

**Alex’s rules (paraphrased):**

1. **B_tail should be large** — he said he wouldn’t expect to **see** a downturn with **under ~20 bins** on the part of X where the drop should happen. That is a **resolution floor**, not a theorem.
2. After you think you’ve found the knee, you want **≥ 2 bins wholly to the right** of it — otherwise the “drop” is one lonely bar and you can’t tell slope from noise.
3. **B_left can be small** (we used **4**). You’re not trying to measure the plateau with surgical precision; you’re trying to **establish** “roughly flat here” before the tail.

**Our v0 choice: B_left = 4, B_tail = 20 → 24 bins total.**

Why 4 + 20 specifically?

| Region | T̂_j slice (our run) | Width | Bin width | Role |
|--------|----------------------|-------|-----------|------|
| Left 4 bins | about −0.44 → +0.12 | ~0.56 z-units | ~0.14 per bin | “Is it flat over here?” |
| Right 20 bins | about +0.12 → +0.75 | ~0.63 z-units | ~**0.03** per bin | “Where does it break?” |

The tail bins are **~5× narrower** than the left bins. That is the whole trick: **microscope on the Ranger Regiment zone**.

**Picture it on a ruler:**

```
Low T̂_j          median split              High T̂_j (elite teams)
|----|----|----|----|----|----|----|----|----|----|----| ... 20 thin ticks ----|
  bin1  2    3    4    | 5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
  ←── 4 coarse ──→     | ←──────────── 20 fine (equal width) ─────────────────────→
        plateau?       |              congestion / knee / downturn hunt
```

**≥ 2 bins past the knee:** if the downturn starts around bin 20, bins 21–24 still have their **own** draft rates. If we had merged 18–24 into one “elite” bin, we’d only see one height — **no shape**.

---

#### Step C — Power check (will we have enough people per bin?)

Bins are useless if each bar is built from **2 guys**. Alex knows this — finer Â slices and more X bins **fight each other**.

**Back-of-envelope:**

```
average n per bin ≈ (band size) / (total bins)
```

For PPM z [2, 3], +DFT, min10: **392 PS / 24 bins ≈ 16** on average.

But **average lies**:

- **Left coarse bins** often have **more** people (team talent is skewed — many players on mid teams).
- **Right fine bins** often have **fewer** (few player-seasons on truly elite mean-T̂_j teams) → **red “thin cell”** bars (n < 30).

In our primary JSON, many tail bins are thin; bins 2–4 (blue, lower/mid T̂_j) are healthier. **That is expected**, not a bug — you traded **spatial resolution** for **statistical precision** at the extreme tail.

**How to read power without giving up:**

| Signal | Trust level |
|--------|-------------|
| **Plateau region** (several left/mid bins, n ≥ 30) | Compare average draft rate — “~34%-ish flat?” |
| **Tail trend** (last 3–5 orange bins) | Directional — “falling vs plateau?” |
| **Single last bin** (n = 1–5) | **Do not** hang a paper on it — it’s the Ranger anecdote bar |

Alex’s order: **explore empirically first**. Thin tail bins mean “we see the shape in principle; collect more seasons or widen Â band later for precision.”

**If power fails completely:** widen band ([1.5, 2] min20 sensitivity run), reduce B_tail to 12 (worse resolution), or lean on poolq_loo P1 / triptych as peer-congestion evidence while T̂_j stays noisy.

---

#### What “piecewise (4 + 20)” means in one paragraph

1. Restrict to fixed-Â players (+DFT).
2. Split their T̂_j values at the **within-band median**.
3. **Below median:** chop into **4 equal-width** bins (wide buckets — plateau).
4. **At/above median:** chop into **20 equal-width** bins (narrow buckets — knee hunt).
5. For each bin, compute draft rate + Wilson CI + flag thin cells.
6. Plot bars 1–24 left to right; orange = high-T̂_j tail.

That implements Alex’s “bin on purpose” without yet doing the full **K/N → θ, γ → exact cutpoint** memo (still open). The median split is a **stand-in** for “start the microscope where the upper half of team talent lives.”

---

#### What the formal K/N memo will add (not done yet)

Eventually we replace the median shortcut with something like:

1. Pick **K** (NBA picks relevant to this pool) and **N** (roster size ~13–15).
2. Map **K/N** and model **θ, γ** to a **T̂_j cutpoint** on the z-scale: “congestion should begin around here.”
3. Set **B_tail** so bin width × (T̂_j range above cutpoint) gives **≥ 20 bins**, with **≥ 2 bins above** the predicted knee.
4. **Prune** bad grids (e.g. 8 total bins) before running.

Until then, **4 + 20 from median split** is “Alex-aligned engineering v0,” not the final word.

---

## 6. Are we on the same page as Alex? (checklist)

| Alex said | We heard | P2b implementation |
|-----------|----------|---------------------|
| Fix Â_i | Matched PPM z band | ✓ e.g. [2, 3] primary |
| X = team talent | T̂_j (mean perf z, includes self) | ✓ not poolq_loo |
| Y = P(draft) | Mean Y_draft | ✓ |
| Flat then down | Plateau vs high-T̂_j tail | ✓ knee summary in JSON |
| Congestion near K/N | High T̂_j tail zoom | ✓ piecewise 4+20 bins |
| Don’t smear with ventiles | Not 16-quantile on T̂_j | ✓ separate binner |
| Empirical first | P2b before MLE fit | ✓ caption says descriptive |
| +DFT for draft ecosystem | Primary population | ✓ |

**Not the same plot as:** triptych / P1 poolq_loo — **complementary**, both “fix Â,” different X.

---

## 7. How to read **your** P2b plots (**downturn = YES** on primary)

**File:** `basic_data_plots/CCT_draft_rate_fixedAi_Tj_knbins_dft.png`

1. **Ignore the left ⅓ first** — look for a **plateau** (similar bar heights, bins ~2–8 in our run ~30–40% draft rate in +DFT [2,3]).
2. **Look at orange tail bins** (high T̂_j) — do heights **fall** vs the plateau?
3. **Read the box** (plateau % vs tail % vs “Downturn visible: YES/NO”).
4. **Respect red bars** — thin cell; wide error bars; don’t over-interpret one bin.
5. **Last bin** — often n tiny; directional only.

**If downturn = YES:** “Alex’s qualitative shape shows up on T̂_j with tail binning — same fix-Â story as poolq_loo triptych, different axis.”

**If it failed:** revisit bin count, Â band, or +DFT vs full panel — **not** “CCT is dead.”

---

## 8. What we are **not** claiming yet

- Not proof the **generative model** is right.
- Not estimated **θ, γ, K** from this plot alone.
- Not causal “team talent **causes** lower draft rate.”
- Not that **T̂_j** and **poolq_loo** must agree — they measure different congestion lenses.

---

## 9. One paragraph to read aloud (alignment test)

*“Alex wants us to hold individual PPM fixed, put mean team talent on the X-axis, and plot draft rate. He expects a flat stretch while team talent rises, then a drop once the team is so strong that draft slots K are scarce relative to roster size N — congestion. K/N and the viability parameters θ and γ tell us where that knee should live in the model; in the data we bin the high team-talent tail on purpose so we don’t smear the drop. We explore the shape empirically first; fitting the inflection comes later.”*

If that matches your memory of the meeting, you and COMPASS heard the same thing.

---

---

## 10. Print snapshot — what shipped (2026-08-21)

| Artifact | Path | Result |
|----------|------|--------|
| **Alex board (P2b)** | `basic_data_plots/CCT_draft_rate_fixedAi_Tj_knbins_dft.png` | Downturn **YES** — plateau ~34% → tail ~8% |
| **Triptych (poolq_loo)** | `…_min10_ppm_triptych.png` | [2,3] +DFT bin-16 cliff |
| **Campaign plan** | `SCOUT_and_COMPASS/CCT_Campaign_Plan.md` | Act II closed; Act III next |

**Alex (same day):** on track; more progress since summer than prior two years; **after next week** → frame story + paper outline; then 50% writing / 50% code-data.

---

*DISPOSABLE · COMPASS · 2026-08-21 evening · delete when read*
