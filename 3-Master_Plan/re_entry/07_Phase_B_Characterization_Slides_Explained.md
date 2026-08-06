# 7. Phase B characterization slides — plain-English walkthrough

**Last synced:** 2026-08-06 (hand-deck JPEG exports for visual audit)

**Audience:** Anyone who has **not** been in the weeds — advisor, collaborator, or future-you after time away.

**Deck:** `HEROs_and_PASSes/slides/CHAR_Phase_B_characterization_HAND.pptx` (hand-edited master).

**Visual exports (agents):** `HEROs_and_PASSes/slides/HAND_slides_images/Slide1.jpeg` … `Slide16.jpeg` — full-deck JPEG export; re-run after hand edits so COMPASS can see Equation Editor math and layout (not scrapeable from `.pptx`).

**Slide count:** Auto merge = **8** slides (intro + 7 characterization). Charles’s hand deck is **16** slides in the Aug 2026 export; θ×K/N may split into **5heat** + **5line**; γ / λ_crit renumber accordingly.

**What this document is:** A slide-by-slide explanation of **what you are looking at** and **why it matters** for the dissertation story. It does not replace the technical memos; it orients a reader before they open PowerPoint.

**Companion:** `[CHARLES_CHECKLIST.md](CHARLES_CHECKLIST.md)` (what Charles still owes); `[06_Lambda_threshold_and_KN_memo.md](06_Lambda_threshold_and_KN_memo.md)` (sort-and-chop λ threshold detail).

---



## SLIDE 0 — Intro (Phase B framing)

**Type:** Text-only opener — no figure. Build: `python sports/scripts/build_intro_characterization_slide.py` → `slides/auto/CHAR_intro_characterization_AUTO.pptx` (copy layout into hand deck).

**Purpose:** Orient Alex (or future-you) before any curves. Everything on this slide is also spelled out below in the intro sections; the slide is the **at-a-glance** version.

### Left column — knob glossary


| Symbol  | Plain name                     | What it controls                                                                                        |
| ------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **A_i** | Player ability (individual talent) | Innate talent draw (Beta(2,2) on [0,1]); empirical lane uses **Â_i** from data |
| **T_{j*}** | Sim assignment target | Synthetic iid Uniform[0,1] per team — soft-assign attractor; **not** realized roster talent |
| **T_j** | Realized team talent | Mean **A_i** on team *j*’s roster (post-ASSIGN); empirical **T_jt** = team-season roster mean of **Â_i** |
| **ρ**   | Assignment assortativity       | How tightly soft assign matches **A_i** to **T_{j*}** |
| **L_C** | Congestion **measure**         | **Smooth (deck):** LOO mean σ(γ(A_j − θ)). **Hard (code):** LOO share with A_j > θ |
| **λ**   | Congestion **weight** in score | How hard **L_C** penalizes ranking — **not** congestion itself                                          |
| **θ**   | Viability cutline              | Center of the sigmoid                                                                                   |
| **γ**   | Sigmoid sharpness              | Steepness of viability step around θ                                                                    |
| **K/N** | Selectivity                    | Fraction of league selected (K ÷ N)                                                                     |




### Right column — four ideas to carry through the deck

1. **Not curve fitting.** Phase B asks which generative rules **bend** synthetic selection curves. Phase C (later) asks whether we can **calibrate** to the empirical hero.
2. **Three pipeline steps + readout:** ASSIGN (ρ) → SCORE (S_i = A_i − λ·L_C) → SELECT (top-K) → VISUALIZE (pool-mean bins).
3. **One-at-a-time + seed 42:** Each slide moves one knob; benchmarks hold elsewhere. Seed locks **A_i**, **T_{j*}**, and soft-ρ assignment lotteries; score, top-K, and bins are deterministic.
4. **Benchmarks while sweeping:** Fixed values (λ=0.55, θ=0.72, γ=10, ρ=8, K/N=10%) anchor to the **539 reference track** where noted — not re-estimated in Phase B. See tables below.



### Empirical hero vs this deck (one paragraph)

**Layer A (real data):** MBB draft rate vs **poolq_loo** (leave-one-out teammate quality) — a **bend** at the top bins (hero plot; see `So_Far_.pptx` slides 1–3).

**Layer C (this deck):** Fraction **selected** vs **pool mean** in a fake league — same *kind* of question (“does roster context bend who gets through?”), different axis, different league, no claim of bin-for-bin match yet.

Benchmark numbers tie slides to the Alex **539 playground** so characterization stays comparable across figures; they are **reference anchors**, not “we fit λ=0.55 to NCAA.”

---



## Intro — what this deck is trying to do (walkthrough detail)



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


| Symbol  | Plain name                     | What it controls                                                        |
| ------- | ------------------------------ | ----------------------------------------------------------------------- |
| **A_i** | Player ability (individual)  | Innate talent draw (here: Beta(2,2) on [0,1]); empirical **Â_i** from data |
| **T_{j*}** | Sim assignment target         | Synthetic Uniform[0,1] per team — soft-assign attractor; not NCAA data |
| **T_j** | Realized team talent         | Mean **A_i** on roster *j* (post-ASSIGN); Sketch A 2D **y**-axis |
| **ρ**   | Assignment assortativity       | How tightly **A_i** is matched to **T_{j*}**                              |
| **λ**   | Congestion **weight** in score | Multiplier on **L_C** in S_i = A_i - \lambda L_C                        |
| **L_C** | LOO peer viability congestion  | **Smooth (deck):** mean σ(γ(A_j − θ)); **hard (code):** share with A_j > θ |
| **θ**   | Viability cutline              | Center of the sigmoid — who counts as a “viable” peer                   |
| **γ**   | Sigmoid sharpness              | How sharp the viability step is around θ                                |
| **K/N** | Selectivity                    | Fraction of the league that gets selected (slots K ÷ players N)         |


**One-at-a-time (OAT):** Each slide fixes **everything except one knob** (or one small grid for θ×K/N). Same random seed (42) where possible so differences are from the knob, not a new lottery.

### What is random vs deterministic? (seed 42)

**Stochastic (seed matters):**

1. **Draw player abilities** A_i — Beta(2,2) on [0,1] (`draw_abilities`; 539 preset).
2. **Draw sim team targets** T_{j*} — see **Where T_{j*} comes from** below.
3. **Soft assignment (ρ arms only)** — shuffle who is processed first, then weighted random team pick per player (`assign_soft`). Each ρ arm gets its own assignment lottery; OAT slides still reuse the **same** A_i and T_{j*} draw.

**Deterministic given a roster:**

1. **Sort-and-chop assignment** — sort by ability, chop into rosters (no randomness).
2. **Score** — compute L_C from teammates, then S_i = A_i - \lambda L_C (pure arithmetic).
3. **Selection (winner rule** `"C"`**)** — deterministic **top K** by score (ties broken by stable sort). Pass A/B/C and all Phase B characterization scripts use `"C"`.
4. **VISUALIZE** — quantile bins and “fraction selected per bin” (deterministic bookkeeping).

**Not used in this deck:** winner rules `"A"` / `"B"` (stochastic proportional sample / Bernoulli). Those are for later soft-selection experiments.

**Why seed 42:** One league draw (A_i, T_{j*}) per figure family so curve differences trace to the knob, not a new talent lottery. Soft-ρ arms need a second seed offset per arm so assignment differs while abilities stay fixed.

### Where **T_{j*}** (sim assignment targets) comes from

**What T_{j*} is:** One number per team — drawn **before** assignment. Soft assign seats player *i* on teams whose T_{j*} is near A_i (weighted by ρ). This is **not** realized roster talent; after ASSIGN, **T_j** = mean A_i on the roster.

**Where the numbers come from (Phase B / 539 gallery):**


| Piece        | Value                         | Source                                                        |
| ------------ | ----------------------------- | ------------------------------------------------------------- |
| Distribution | **Uniform**, iid across teams | `target_dist: "uniform"` in pass scripts                      |
| Range        | **[0, 1]**                    | `SELECTION_539_TARGET_MEAN_LOW/HIGH` in `tier1_sim_config.py` |
| Function     | `draw_target_means()`         | `sports/tier1_pool_assignment.py`                             |
| Randomness   | Same seed as A_i draw         | `HERO_SEED = 42` in `gallery_knobs.py`                        |


**What we are *not* doing:** We do **not** copy real NCAA team talent into T_{j*}. The draw is **synthetic** — commensurate with A_i on [0,1], not mirroring real programs.

**When T_{j*} matters vs doesn’t:**

- **Soft ρ slides (1–2, 3, 4–5):** T_{j*} enters the assignment kernel \propto \exp(-\rho(A_i - T_{j*})^2 / (2\sigma^2)).
- **Sort-and-chop (γ / λ_crit slides):** T_{j*} is **drawn but unused** — rosters come from sorting A_i and chopping into fixed-size slices (see memo 06).
- **PD16 Sketch A (L_C vs ρ):** 2D heatmap **y**-axis is **realized T_j** (roster mean), not T_{j*}.

**Older 539 full-scale note:** `MATCH_539_FULL` also uses Uniform[0,1] for targets at N=30,000 scale. The generic `TARGET_MEAN_LOW/HIGH = ±0.5` in `tier1_sim_config.py` applies to non-539 presets; **Phase B characterization uses the 539 [0,1] band.**

### Where λ = 0.55 comes from (benchmark, not a new fit)

**0.55 is the 539 reference preset**, not something we re-estimated for Phase B:


| Source                                     | Value                                                         |
| ------------------------------------------ | ------------------------------------------------------------- |
| `sports/tier1_539_reference_settings.json` | `"lambda_": 0.55`                                             |
| `sports/tier1_sim_config.py`               | `SELECTION_539_LOO_GAP_WEIGHT = 0.55`                         |
| Playground default                         | `tier1_cell10_playground_state.json` → `loo_gap_weight: 0.55` |
| Gallery knob name                          | `LAMBDA_MODERATE = 0.55` in `gallery_knobs.py`                |


**How it is used in the deck:**

- **Slides 1–2, 4–5:** **Fixed** at 0.55 while another knob moves — “run at the 539 reference weight.”
- **Slide 3 (Pass B):** **0.55 is one arm** among {0, 0.25, 0.55, 1.0} — the moderate comparison point, same number as the preset.
- **Slides 6–7 (γ / λ_crit):** 0.55 appears again as a **labeled λ arm** on the sweep grid, not a separate calibration.

We have **not** yet argued 0.55 is the “true” NCAA λ; it is the **Alex 539 track default** so characterization stays comparable to the playground and reference JSON.

### Hard vs smooth **L_C** (both in code; deck shows smooth)

The code builds **two** congestion columns in `add_loo_pool_columns()` (`tier1_pool_assignment.py`):

| Mode | Config string | Formula for each teammate *j* | **L_C** for player *i* |
|------|---------------|------------------------------|------------------------|
| **Smooth (Phase B default)** | `crowding_smooth` | σ(γ(A_j − θ)) ∈ (0,1) | Mean over LOO teammates |
| **Hard (available, not in deck)** | `crowding` | 1 if A_j > θ else 0 | Mean = **share** of LOO teammates above θ |

**Every characterization figure** sets `loo_pool_l_mode="crowding_smooth"`. The playground (CELL 10) can switch modes; Phase B does not sweep hard vs smooth.

**Educational figure:** `sort_chop_lambda/VIABILITY_hard_vs_smooth.png` — side-by-side peer weights on a θ-straddle roster. Regenerate: `python sports/scripts/build_viability_hard_vs_smooth_figure.py`.

#### What would change if we used hard **L_C**?

Qualitative story (**λ > 0 bends selection**) would **survive** — congestion in score still matters. Concrete differences:

| Topic | Smooth (what we show) | Hard (counterfactual) |
|-------|----------------------|------------------------|
| **γ knob** | **Matters** — controls sigmoid steepness; γ sweep slides are meaningful | **Irrelevant** — only θ enters; **γ sweep would be pointless** |
| **Peer near θ** | Graded weight (~0.5 at A_j = θ) | **Cliff** — jumps 0 → 1 at θ |
| **L_C values** | Continuous in [0,1] | **Discrete steps** (multiples of 1 / #teammates, e.g. 0, 1/15, 2/15, …) |
| **λ_crit story** | λ_crit ≈ **4/γ** on sort-and-chop (memo 06) | Sharper reorder at roster seams; no 4/γ law — **θ-only** cutline |
| **All-above-θ team** | L_C ≈ 1 (saturated, not exactly 1) | L_C = **1 exactly** |
| **All-below-θ team** | L_C ≈ 0 | L_C = **0 exactly** |
| **Curve shapes** | Similar humps; transitions **spread** around θ | Often **sharper** threshold behavior; small rank changes can flip many peers 0↔1 |

**If Alex asks:** “We use smooth σ because peer viability is graded in the story and γ is a real knob. Hard share is the limit γ → ∞ and is still in code for comparison. Phase B standardizes on smooth so θ and γ slides are coherent.”

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



## SLIDE 3 — Characterize λ (weight on **L_C** in score)

**Knob varied:** **λ** — how heavily the congestion measure **L_C** enters **ranking**: S_i = A_i - \lambda L_C.

**Terminology lock:** **L_C** is computed from teammates (LOO peer viability). **λ** is only the **scalar weight** on that term. Congestion lives in **L_C**; λ says how much it matters for who ranks high.

**Held fixed (benchmarks):**


| Setting    | Value                      | Provenance                                                       |
| ---------- | -------------------------- | ---------------------------------------------------------------- |
| Assignment | Soft **ρ = 8**             | `GALLERY_LAMBDA_FIXED_RHO` — moderate-high mixing for λ/θ slides |
| Roster     | One draw + one soft assign | Same players on same teams for all λ arms                        |
| **θ, γ**   | 0.72, 10                   | 539 reference JSON                                               |
| **K/N**    | 10%                        | Characterization default (`gallery_knobs`)                       |
| Selection  | Top-K by score (`"C"`)     | Deterministic                                                    |
| Seed       | 42                         | Same A_i, T_{j*}, assignment                                       |




### The experiment (what actually changes)

Pass B draws the league **once**, assigns rosters **once** at ρ=8, then re-scores the **same** players with four λ values. Only the **SCORE** step changes; ASSIGN and SELECT rules are identical.

### Arms on the plot


| λ        | Score rule       | Plain English                                    |
| -------- | ---------------- | ------------------------------------------------ |
| **0**    | S_i = A_i        | **Talent only** — L_C ignored in ranking         |
| **0.25** | mild penalty     | Light weight on congestion                       |
| **0.55** | moderate penalty | **539 reference preset** — not re-fit in Phase B |
| **1.0**  | strong penalty   | Full unit weight on L_C in score                 |




### What the figure shows

- **λ = 0:** Curve tends **monotone** — best players sit on the strongest teams (ρ=8), and score ≈ raw ability → elite pool-mean bins dominate selection.
- **λ > 0:** L_C is **subtracted** in score. Players in extremely strong peer fields can rank below slightly weaker players on softer rosters → selection **spreads** or **peaks** away from bin 16 → inverted-U-ish readout on pool mean.



### What we learn

**Congestion must enter through SCORE to bend selection — not through VISUALIZE alone.**

- **Environment / hero (Layer B):** L_net = B - D describes peer effects on development; it does **not** pick sim winners by itself.
- **Score (this slide):** L_C is **calculated** from rosters and **weighted** by λ in S_i → **reorders** the top-K list.
- **VISUALIZE:** Pool-mean bins are **readout** — where selected players sit after score + select.

The knockout contrast: **λ=0 vs λ>0**, same rosters, same top-K — curves diverge because **ranking** changed, not because we changed the binning scheme.

### Connection to empirical data (conceptual)


|                  | Empirical hero                   | This slide                                      |
| ---------------- | -------------------------------- | ----------------------------------------------- |
| **Outcome**      | Drafted (0/1)                    | Selected in fake league (0/1)                   |
| **Context axis** | **poolq_loo** (teammate quality) | **Pool mean** (team talent incl. self)          |
| **Question**     | Does context bend outcomes?      | Does λ in **score** bend **who gets selected**? |


Same *kind* of “context matters” story; Phase B does not claim bin-for-bin match to NCAA rates.

---



## SLIDE 4 — Characterize θ (viability cutline): one-at-a-time at K/N = 10%

**Knob varied:** **θ** — center of the logistic viability function inside **L_C**.

**Held fixed:** ρ = 8, λ = 0.55, γ = 10, **K/N = 10%**. **L_C mode:** `crowding_smooth` (hard `crowding` available in code — not this slide).

### The equation on the slide (what θ does)


L_C = \mathrm{mean}_{j \neq i}\sigma\big(\gamma(A_j - \theta)\big)


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



## SLIDE 5heat — Characterize θ × K/N (heatmap)

**Hand deck:** usually **slide 5**. **PNG:** `theta/THETA_KN_sweep_peak_bin.png`

**Knobs varied together (small grid):** **θ** × **K/N** — on purpose, because PD15 asked whether viability cutline and selectivity **co-move**.

**Held fixed:** ρ = 8, λ = 0.55, γ = 10, N = 5600; only **K** changes with K/N.

### What this figure is

A **3×3 heatmap** of **peak pool-mean bin** (integer 1–16). We do **not** plot full selection curves here — only *where the hump peaks* on the pool-mean ladder for each (θ, K/N) cell.

- **Rows:** K/N presets — MBB-like **1%**, characterization **10%**, high **40%**.
- **Columns:** θ ∈ {0.50, 0.72, 0.90}.
- **Cell color / number:** Peak bin (1 = weakest team environments, 16 = strongest).



### Example readout (seed 42)


| K/N regime                  | θ = 0.50 | θ = 0.72 | θ = 0.90 |
| --------------------------- | -------- | -------- | -------- |
| **~1%** (MBB-like)          | **6**    | **9**    | **12**   |
| **~10%** (default)          | **13**   | **13**   | **16**   |
| **~40%** (high selectivity) | **16**   | **16**   | **16**   |




### How to read the heatmap

- **Yellow / high numbers (→16):** Selection peak sits on **elite** team environments — top-saturated.
- **Green / mid numbers (~6–13):** Peak sits **mid-ladder** — inverted-U-ish readout on pool mean.
- **Scan a row (fixed K/N):** See whether θ moves the peak as you go left → right.
- **Scan a column (fixed θ):** See whether selectivity moves the peak as you go top → bottom.



### When to use this slide

Best when Alex (or you) want **exact bin numbers** at a glance, or when comparing to the table in `theta/THETA_KN_sweep_summary.csv` without estimating from a line chart.

### What we learn (shared with 5line)

**Do not pick θ in isolation.** At **1%** selectivity, raising θ shifts the peak up the pool ladder (6 → 12). At **40%**, everything saturates at bin **16** — selectivity **swamps** θ. At **10%**, θ toggles mid-hump vs top-saturation (13 vs 16). **Descriptive only** — not a fitted law θ = f(K/N).

---



## SLIDE 5line — Characterize θ × K/N (line plot)

**Hand deck:** duplicate of 5heat, usually **slide 6**. **PNG:** `theta/THETA_KN_sweep_peak_bin_lines.png`

**Same experiment as 5heat** — identical 3×3 grid, different graphic.

### What this figure is

**Peak bin vs θ**, with **one line per K/N** preset:

- **Green — MBB-like (K/N ≈ 1%):** Peak rises with θ (≈ 6 → 9 → 12) — θ and selectivity **interact** when few slots exist.
- **Blue — characterization (K/N ≈ 10%):** Mostly flat then jumps to bin 16 at high θ (13, 13, 16).
- **Red — high selectivity (K/N ≈ 40%):** Flat at bin **16** for all θ — everyone elite is already selected.

Markers sit at the **three measured θ** values only; line segments connect those points. **Not** a dense surface or interpolated grid — only the nine diagnostic runs.

### How to read the line plot

- **Steep green line:** θ matters a lot when the league is highly selective (few picks).
- **Flat red line at top:** When many advance, θ barely moves where the peak sits.
- **Subtitle on figure:** “3×3 diagnostic grid — lines join measured θ only” — remind audience we are not claiming smooth θ–K/N physics between grid points.



### When to use this slide

Best for **live presentation** — the co-variation story is visible in one glance. Use **instead of** 5heat in a tight meeting, or keep both and hide one in PowerPoint until you decide.

### What we learn

Same as **5heat**; the claim in your footer applies to both:

> θ and K/N co-vary — at MBB-like selectivity, raising θ shifts peak bin up the pool ladder; at 40% selectivity, curves are top-saturated regardless of θ.

---



## SLIDE 6 — Characterize γ (viability sharpness): selection curves

**Knob varied:** **γ** — steepness of σ(γ(A − θ)) inside **L_C**.

**Setting:** **Sort-and-chop** assignment benchmark (same rosters within each γ); **λ** arms overlaid per γ.

**Figure (readable default):** `sort_chop_lambda/GAMMA_sweep_lambda_curves_key_arms.png` — **λ ∈ {0, 0.55, 1.0}** only, stacked panels (one γ per row). Full five-arm grid: `GAMMA_sweep_lambda_curves.png` (solid = key arms, dashed = intermediate λ).

### Why sort-and-chop here (not soft ρ = 8)

**Your read is basically right:** sort-and-chop is **maximum assignment assortativity** — it **removes ambiguity in roster geometry** so we can characterize **γ** and **λ_crit** cleanly. Precision below.

Slides **1–2** use **soft ρ** because the knob under test is **assignment mixing**. Slides **6–7** use **sort-and-chop** on purpose:

1. **Clean geometry for γ and λ_crit** — sort all players by A_i, chop into equal rosters. **Zero between-team ability overlap** (unlike soft ρ, where ~99% of team pairs overlap). Within each team, ability and peer viability **line up** → one **θ-straddle** roster, clean **seams** at slice boundaries. That is where λ first reorders top-K (memo 06; λ_crit ≈ 4/γ).
2. **Isolate score reordering** — not fighting soft-assignment noise or overlapping talent windows. Question: *given extreme seating, when does λ change who wins?*
3. **Answer Alex’s “λ = 0 vs 0.25 looks identical” puzzle** — sub-threshold λ often **does not swap** global ranks; γ sets how sharp that threshold is.

**What sort-and-chop is *not*:** It is **not** the ρ knob. ρ controls **soft** match to **T_{j*}**. Sort-and-chop **ignores T_{j*}** and is a **hard diagnostic benchmark** — “perfect rank sorting,” not “realistic NCAA mixing.”

**Pairing:** Soft ρ = 8 → **realistic** assignment world (slides 1–5). Sort-and-chop → **controlled testbed** for sigmoid sharpness (γ) and critical λ (slides 6–7). Same score rule; different assignment extreme.

### Arms

- **γ ∈ {5, 10, 20}** — soft, default, sharp viability step
- For each γ, **λ ∈ {0, 0.25, 0.55, 0.75, 1.0}**



### What the figure shows

Each panel or color group asks: *as we turn up congestion weight λ, when does the selection curve stop looking like λ = 0?*

- **Low γ (5):** Viability spreads over ability → congestion builds slowly → need **larger λ** before curves change shape.
- **High γ (20):** Sharp knee → congestion “turns on” quickly → **smaller λ** can reorder selection.



### What we learn

**γ sets how “binary” peer viability feels.** Sharper viability → congestion bites at lower λ. This feeds directly into Slide 7’s **λ_crit ≈ 4/γ** rule of thumb on sort-and-chop (Slide **8** if both θ×K/N variants remain in the hand deck).

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



## How the slides fit together


| Slide | Knob        | One-line takeaway                                                           |
| ----- | ----------- | --------------------------------------------------------------------------- |
| **0** | —           | Phase B = characterization, not fit; glossary + benchmarks + seed           |
| 1–2   | **ρ**       | Sorting / assignment shapes roster environments → changes selection readout |
| 3     | **λ**       | Congestion in **score** bends the curve vs talent-only                      |
| 4     | **θ**       | Viability cutline moves the hump at fixed K/N = 10%                         |
| 5heat | **θ × K/N** | Heatmap — exact peak bins; θ interacts with selectivity                     |
| 5line | **θ × K/N** | Same grid as 5heat — trend lines for presenting                             |
| 6     | **γ**       | Sharpness of viability sets when λ starts to matter                         |
| 7     | **λ_crit**  | Explains “identical” low-λ curves on sort-and-chop                          |


*If both 5heat and 5line stay in the hand deck, γ and λ_crit become slides **7** and **8**.*

**Story arc for an outsider:** Real data show context matters in **outcomes**. This deck shows which **rules of a fake league** are powerful enough to bend **who gets selected** — assignment (ρ), congestion in score (λ), viability geometry (θ, γ), and league selectivity (K/N). Phase C (later) asks whether we can **fit** those knobs to data; Phase B asks whether the **model has the right moving parts**.

---



## Practical notes for the reader

- **Hand vs auto decks:** Scripts regenerate disposable `slides/auto/*_AUTO.pptx`; Charles’s formatted master is `slides/CHAR_Phase_B_characterization_HAND.pptx`. See `slides/README.txt` for PNG paths if figures are refreshed.
- **Hand deck JPEG exports:** `slides/HAND_slides_images/SlideN.jpeg` — export whole deck from PowerPoint after edits; agents use these to audit notation and layout against this walkthrough.
- **Regenerate figures only:** `./scripts/build_characterization_slides.sh` (does not touch the hand deck).
- **Empirical hero lives elsewhere:** Pass A / `So_Far_.pptx` slides 1–3 — real MBB draft rates vs talent and poolq_loo.

---



## Suggested one-sentence opener if you present this deck

“We built a transparent fake league, varied one rule at a time, and asked which rules bend **who gets selected** when we bin by team strength — assignment ρ, congestion λ in the score, viability θ and γ, and selectivity K/N all matter in ways this deck summarizes.”