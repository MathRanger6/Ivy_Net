# 7. Phase B characterization slides — plain-English walkthrough

**Last synced:** 2026-08-04

**Audience:** Anyone who has **not** been in the weeds — advisor, collaborator, or future-you after time away.

**Deck:** `HEROs_and_PASSes/slides/CHAR_Phase_B_characterization.pptx` (7 slides, hand-edited master).

**What this document is:** A slide-by-slide explanation of **what you are looking at** and **why it matters** for the dissertation story. It does not replace the technical memos; it orients a reader before they open PowerPoint.

**Companion:** [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) (what Charles still owes); [`06_Lambda_threshold_and_KN_memo.md`](06_Lambda_threshold_and_KN_memo.md) (sort-and-chop λ threshold detail).

---

## Intro — what this deck is trying to do

### The big picture (one paragraph)

Real college basketball data show a striking pattern: players on **stronger teammate pools** do not always have the **highest** NBA draft rates — the relationship can **bend** (rise, flatten, even dip at the very top). Charles’s dissertation asks whether a **simple fake league** can reproduce shapes like that when we write down explicit rules: put players on teams, **score** them, **select** the top few, then **look at who got selected** broken down by roster context.

**Phase B** (this deck) is **not** “fit the real hero yet.” It is **characterization**: turn one dial at a time in the fake league and ask, *does this dial matter for the shape of the selection curve?* If yes, the dial is part of the story; if no, we note that and move on.

### Three steps in the fake league (memorize this)

Every generative slide shares the same pipeline:

1. **ASSIGN** — Who plays where? (team matching / sorting; knob **ρ**)
2. **SCORE** — Who looks best on paper? **S_i = A_i − λ·L_C** (knob **λ**; congestion term **L_C**)
3. **SELECT** — Who actually advances? Top **K** players by score (knob **K/N** = selectivity)

Then we **VISUALIZE**: among the **K** selected players, plot the **fraction selected in each bin** of **team pool quality** (x-axis = mean ability on the roster, including self — called **pool mean** here).

So the y-axis is **not** “draft rate in the real NCAA.” It is **“share of selected players in this bin”** in a synthetic league with **N ≈ 5,600** players and default **K/N = 10%** (~560 selected), unless a slide says otherwise.

### How to read the curves

- **X-axis (pool mean bins):** Teams sorted into 16 equal-sized bins from **weakest** average talent (left) to **strongest** (right). Bin 1 = low pool mean; bin 16 = high pool mean.
- **Y-axis:** For each bin, what **fraction of all selected players** landed in teams whose pool mean falls in that bin? High values mean “selection concentrates in this roster environment.”
- **Monotone rising curve:** Elite team environments hog selection — looks like “the best teams produce the picks.”
- **Hump / inverted-U-ish curve:** Selection peaks in **middle** pool-mean bins — “mid-tier pressure” shows up in who gets through.
- **Flat curve:** Assignment or score barely changes **where** selected players sit on the pool-mean ladder.

### Knobs on the slides (mini glossary)

| Symbol | Plain name | What it controls |
|--------|------------|------------------|
| **A_i** | Player ability | Innate talent draw (here: Beta(2,2) on [0,1]) |
| **ρ** | Assignment assortativity | How tightly players are matched to team talent targets |
| **λ** | Congestion weight in **score** | How much peer viability **L_C** penalizes ranking |
| **L_C** | LOO peer viability congestion | Mean over teammates *j ≠ i* of σ(γ(A_j − θ)) |
| **θ** | Viability cutline | Center of the sigmoid — who counts as a “viable” peer |
| **γ** | Sigmoid sharpness | How sharp the viability step is around θ |
| **K/N** | Selectivity | Fraction of the league that gets selected (slots K ÷ players N) |

**One-at-a-time (OAT):** Each slide fixes **everything except one knob** (or one small grid for θ×K/N). Same random seed (42) where possible so differences are from the knob, not a new lottery.

---

## SLIDE 1 — Characterize ρ (assignment): sort-and-chop shown

**Knob varied:** **ρ** — how assortative assignment is (plus a **sort-and-chop** benchmark arm).

**Held fixed:** Score rule **S_i = A_i − 0.55·L_C**, top-**K** selection, same draw of abilities and team targets.

### What the figure shows

Several colored curves on one plot. Each curve is a different **assignment rule** applied to the **same** pool of player talent:

- **Low ρ (e.g. 0.1):** Players mix almost randomly across team talent levels → selected players spread evenly across pool-mean bins → curve stays ** fairly flat**.
- **Moderate / high ρ (1, 8, 32):** Strong players tend to land on strong teams → selection shifts toward high pool-mean bins → curve can develop a **peak** or strong tilt to the right.
- **Sort-and-chop arm:** A **hard** sorting benchmark (perfect rank matching within slices). Included here for comparison — it often produces an extreme **monotone** shape (selection piles into the top bins).

### What we learn

**Who you play with (assignment) matters a lot** once score and selection are fixed. Low mixing → flat readout; high assortativity → peer environments concentrate and the selection-vs-pool-mean curve **bends**.

### What we are *not* claiming

This is a **qualitative** proof-of-concept in a fake league. The x-axis is **pool mean**, not the empirical hero axis **poolq_loo**. We have not yet matched bin-for-bin to real NCAA draft rates.

---

## SLIDE 2 — Characterize ρ (assignment): sort-and-chop suppressed

**Same experiment as Slide 1**, but the **sort-and-chop** curve is **omitted from the plot** so the eye focuses on the **soft ρ ladder** only (ρ ∈ {0.1, 1, 8, 32}).

### Why a second slide

Sort-and-chop is a useful **benchmark** (zero overlap between talent slices), but it can **dominate** the figure visually. Soft ρ arms are closer to “continuous” assortativity and are easier to compare to each other.

### What we learn

Same claim as Slide 1, stated without the hard-sort distraction: **raising ρ** moves the selection readout from **flat** toward **concentrated / humped** shapes on the pool-mean axis.

---

## SLIDE 3 — Characterize λ (congestion in score)

**Knob varied:** **λ** in **S_i = A_i − λ·L_C**.

**Held fixed:** Soft assignment at **ρ = 8**, same rosters and talent draw, same top-**K** rule.

### Arms on the plot

Typically four values:

| λ | Score rule | Plain English |
|---|------------|---------------|
| **0** | S_i = A_i | **Talent only** — congestion ignored in ranking |
| **0.25** | mild penalty | Light peer pressure in score |
| **0.55** | moderate penalty | Default-style weight in many Pass B/C runs |
| **1.0** | strong penalty | Heavy peer viability penalty |

### What the figure shows

- **λ = 0:** Curve tends **monotone** — players on the highest pool-mean teams dominate selection because score ≈ raw ability and strong players sit on strong teams.
- **λ > 0:** Congestion enters the **ranking**. Players in extremely strong peer fields can be **penalized** in score even if they are good → selection can **spread** or **peak** away from the very top bins → curve **bends** (inverted-U-ish readout on pool mean).

### What we learn

**Congestion belongs in the score, not just in the environment story.** If advancement used talent alone (λ = 0), you would not get the same selection shape as when roster pressure enters **S_i**.

### Connection to real data (conceptual only)

The empirical hero bins on **teammate quality** in **outcomes**. This slide bins on **pool mean** in a **simulated selection** step. Same *kind* of question (“does context bend who gets through?”), different measurement and league.

---

## SLIDE 4 — Characterize θ (viability cutline): one-at-a-time at K/N = 10%

**Knob varied:** **θ** — center of the logistic viability function inside **L_C**.

**Held fixed:** ρ = 8, λ = 0.55, γ = 10, **K/N = 10%** (characterization default).

### The equation on the slide (what θ does)

\[
L_C = \mathrm{mean}_{j \neq i}\,\sigma\big(\gamma(A_j - \theta)\big)
\]

For each player *i*, look at teammates *j*, map each teammate’s ability through a **soft step** σ centered at θ, average (leave-one-out). **Higher θ** → fewer teammates count as “viable peers” → **L_C** changes → **S_i** changes → selection shifts.

### Arms

θ ∈ **{0.50, 0.72, 0.90}** — low, default-ish (0.72), high cutline.

### What the figure shows (typical pattern)

- **θ = 0.50:** More peers count as viable → congestion term behaves differently → selection peak often sits in **mid** pool-mean bins (e.g. peak around bin **13**).
- **θ = 0.72 (539 default):** Similar hump, sometimes slightly higher peak rate.
- **θ = 0.90:** Viability is hard to achieve → congestion term shifts → selection can **pile into top bins** (peak at bin **16**) — curve looks more **monotone** at the elite edge.

### What we learn

**θ is not a cosmetic parameter.** Moving the viability cutline changes **who wins** under fixed ρ, λ, and selectivity. Before tying θ to real draft data, we need to see it move the sim curve — it does.

---

## SLIDE 5 — Characterize θ × K/N (selectivity panel)

**Knobs varied together (small grid):** **θ** × **K/N** — on purpose, because PD15 asked whether viability and selectivity **co-move**.

**Held fixed:** ρ = 8, λ = 0.55, γ = 10, N = 5600; only **K** changes with K/N.

### What the figure shows

Usually a **heatmap or table of peak bin** — not full curves. Question: *where* does the selection curve peak on the pool-mean axis (bin 1 = weakest teams, 16 = strongest)?

Example readout (seed 42):

| K/N regime | θ = 0.50 | θ = 0.72 | θ = 0.90 |
|------------|----------|----------|----------|
| **~1%** (MBB-like draft rate) | peak bin **6** | **9** | **12** |
| **~10%** (characterization default) | **13** | **13** | **16** |
| **~40%** (high selectivity) | **16** | **16** | **16** |

### How to read it

- **Low K/N (1%):** Only a tiny slice gets selected. Changing θ **moves** where the peak sits — θ and selectivity **interact**.
- **High K/N (40%):** So many selected that everyone elite is taken — peak **saturates at bin 16** for all θ. Selectivity **swamps** θ.
- **Middle (10%):** θ mainly toggles **hump vs top-saturation** (e.g. bins 13 vs 16).

### What we learn

**Do not pick θ in isolation.** Its effect depends on **how selective** the league is. A θ that matters at MBB-like 1% draft rates may barely matter when 40% of players advance. This slide is **descriptive** — we are **not** yet asserting a formula θ = f(K/N) without advisor sign-off.

---

## SLIDE 6 — Characterize γ (viability sharpness): selection curves

**Knob varied:** **γ** — steepness of σ(γ(A − θ)) inside **L_C**.

**Setting:** **Sort-and-chop** assignment benchmark (same rosters within each γ); several **λ** arms overlaid per γ.

### Arms

- **γ ∈ {5, 10, 20}** — soft, default, sharp viability step
- For each γ, **λ ∈ {0, 0.25, 0.55, 0.75, 1.0}**

### What the figure shows

Each panel or color group asks: *as we turn up congestion weight λ, when does the selection curve stop looking like λ = 0?*

- **Low γ (5):** Viability spreads over ability → congestion builds slowly → need **larger λ** before curves change shape.
- **High γ (20):** Sharp knee → congestion “turns on” quickly → **smaller λ** can reorder selection.

### What we learn

**γ sets how “binary” peer viability feels.** Sharper viability → congestion bites at lower λ. This feeds directly into Slide 7’s **λ_crit ≈ 4/γ** rule of thumb on sort-and-chop.

---

## SLIDE 7 — λ_crit ≈ 4/γ (educational)

**Not a new sweep** — an **explanatory** figure tying γ to a **critical λ** where score ranking first differs from talent-only ranking.

### What the figure shows

- The **sigmoid** σ(γ(A − θ)) along the ability axis for several γ.
- Vertical markers at **λ_crit ≈ 4/γ** (e.g. γ = 10 → crit ≈ **0.4**).

### Plain-English meaning of λ_crit

On sort-and-chop rosters, ability and congestion **line up** within teams. Small λ may **not reorder** who makes top-**K** even though λ > 0 in the formula. **λ_crit** is the first λ where **S_i = A_i − λ L_C** actually changes **who** gets selected vs **S_i = A_i**.

**Important nuance:** The **plot** in 16 bins may still **look** like λ = 0 until λ is **slightly above** λ_crit — coarse bins hide small reorderings. Finer bins or checking rank swaps tell the fuller story (see memo 06).

### Why this slide exists

Alex asked why **λ = 0** and **λ = 0.25** can look **identical** on some diagnostics. This slide answers: *because 0.25 is below the reorder threshold for γ = 10 on sort-and-chop*, not because λ “does nothing” in the math.

---

## How the seven slides fit together

| Slide | Knob | One-line takeaway |
|-------|------|-------------------|
| 1–2 | **ρ** | Sorting / assignment shapes roster environments → changes selection readout |
| 3 | **λ** | Congestion in **score** bends the curve vs talent-only |
| 4 | **θ** | Viability cutline moves the hump at fixed selectivity |
| 5 | **θ × K/N** | Cutline effects depend on how many slots exist |
| 6 | **γ** | Sharpness of viability sets when λ starts to matter |
| 7 | **λ_crit** | Explains “identical” low-λ curves on sort-and-chop |

**Story arc for an outsider:** Real data show context matters in **outcomes**. This deck shows which **rules of a fake league** are powerful enough to bend **who gets selected** — assignment (ρ), congestion in score (λ), viability geometry (θ, γ), and league selectivity (K/N). Phase C (later) asks whether we can **fit** those knobs to data; Phase B asks whether the **model has the right moving parts**.

---

## Practical notes for the reader

- **Hand vs auto decks:** Scripts regenerate disposable `slides/auto/*_AUTO.pptx`; Charles’s formatted master is `slides/CHAR_Phase_B_characterization.pptx`. See `slides/README.txt` for PNG paths if figures are refreshed.
- **Regenerate figures only:** `./scripts/build_characterization_slides.sh` (does not touch the hand deck).
- **Empirical hero lives elsewhere:** Pass A / `So_Far_.pptx` slides 1–3 — real MBB draft rates vs talent and poolq_loo.

---

## Suggested one-sentence opener if you present this deck

“We built a transparent fake league, varied one rule at a time, and asked which rules bend **who gets selected** when we bin by team strength — assignment ρ, congestion λ in the score, viability θ and γ, and selectivity K/N all matter in ways this deck summarizes.”
