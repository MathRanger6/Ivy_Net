# The Big Fish and the Small Pond — A Porch Reading for Charles

**Prepared by COMPASS** (with SCOUT’s numbers and cross-read folded in)  
**Date:** August 20, 2026  
**SCOUT review:** Complete (2026-08-21) — see [`20260821_SCOUT_porch_reading_review.md`](20260821_SCOUT_porch_reading_review.md). Three minor clarifications only; **approved** for porch use.  
**Purpose:** One coherent story you can print, bring home, and read quietly on the porch with **Ginger** — mission, contention, what we learned today, and where we go next.  
**For Ginger:** You don’t need the notation. The Squid-and-Jackal story is: *same talent, different team — does standing out on the roster change who gets drafted?* Charles has been chasing that question for years. Tonight’s read is where the data stand.

**Source memos merged:** COMPASS BDP wisdom · SCOUT+COMPASS joint CCT wisdom · SCOUT §11 addendum · Track C robustness note.

*This document replaces reading three separate agent memos. The technical pair stays in the folder for reference.*

---

## A note before you begin

You asked SCOUT and COMPASS to look at your new **Basic Data Plots** deck, connect it to **HAND17 Slide 5** (team talent intervals), and help you find how to **illuminate** a conviction you have carried for a long time: the **big fish / small pond** story.

We read everything — all 21 slide exports, every BDP JSON sidecar, the interval overlap slide, the hero history, the model memos, and the BPM/OBPM robustness work.

**Good news first:** Your Central Contention and Theme (CCT) is **coherent**. It fits the Army evidence, the model structure, the interval geometry, and the new BDP overlays. Nothing we saw today falsifies it.

**Honest news second:** The CCT is **not yet visible** in the charts you have been staring at the longest — the marginal “hero” curve and the new histograms. Those charts answer **different questions**. The Squid-versus-Jackal test needs a **microscope**, not a wider lens.

**SCOUT and COMPASS agree on that.** There are **no disagreements** between us on substance today. Where one of us said something exclusively, you will see **[SCOUT]** or **[COMPASS]** in the margin.

---

## Part 1 — What you told us (in your words)

You said something like this:

> I feel like if we go to a pretty good team — call them the **Squids** — there will be a great player. I feel like if we go to a contender — call them the **Jackals** — there will be **several** players with the **same talent** as that one great Squid player. And I think the Squid star, considering everything, will empirically be **more likely to be drafted** than each of the corresponding players at his level on the Jackals — because of **congestion**.

You are convinced this is true. In Army data it is **extreme**. In NCAA data you suspect it is a **subtle nuance** — something you have to **zoom in** on and find.

You also said:

- You built the **BDP deck** to get into the **nitty gritty** of what happens among **top T̂_j teams** — intervals, congestion, roster sizes — not just the league-wide marginals.
- You remember **HAND17 Slide 5**: teams differ in T̂_j, intervals **move up** as teams get better, and overlap/stacking at a given talent level matters for your story.
- You noticed something in the new slides: **OBPM** and **BPM** DFT populations look **tighter** (smaller standard deviations) than the non-DFT populations — and you wondered if that has implications.
- You want populations, filters, and scales that **bring the CCT to empirical day** — not another cryptic outline, but a **view of the data** that makes the principle visible even if NCAA whispers.

We heard you. This document is our answer.

---

## Part 2 — The Central Contention, in plain English

### The question (this is NOT “do good players get drafted?”)

Everyone knows good players get drafted more often. That is not the dissertation move.

The move is:

**Hold individual talent fixed.** Then ask: does **where you sit on the team** — how **crowded** your pond is with other strong players — change your odds of being drafted?

### The cast

| Name | Who they are | Role in the story |
|------|----------------|-------------------|
| **Squid star** | Best player on a **pretty good** team | “Big fish, small pond” — stands out locally |
| **Jackal peer** | Player of **similar individual talent** on a **contender** | “Small fish, big pond” — same fish, more rivals at that level |
| **Congestion** | Too many viable peers on the roster | Hurts you in the **race for scarce draft attention**, not necessarily in your box score |

### What “congestion” is NOT (binding rule — **[COMPASS]**)

Congestion in your **draft story** is **not** the same thing as “bad teammates hurt my development.”

The dissertation deliberately separates:

1. **Environment** — peers can help you grow (B) or crowd you in development (D). Net environment is **L_net ≈ B − D**.
2. **Score** — how we **rank** candidates: **S_i = talent − λ × L_C** (congestion in the **rank**).
3. **Select** — who **wins** the scarce slots **after** ranking (top-K, Gibbs, etc.).
4. **Hero** — what we **observe** in real data (draft rate vs teammate quality bins).

**Do not merge these.** The hero is an **outcome**. It is not the same object as S_i, and environment is not advancement.

### Army vs NCAA

| | Army | NCAA (your working guess) |
|---|------|---------------------------|
| Signal strength | **Screams** — obvious, robust **tail drop** even at macro level | **Whispers** — middle rise, elite tail flat in marginals |
| Baseline outcome rate | **~35–40%** of Captains promote — high baseline, mostly an **assembly-line** process | **~2–2.5%** drafted on your panel — scarcer binary outcome |
| Why it screams (not K/N) | Peer/environment effects show up **strongly in the aggregate hero**; survival analysis adds **timing** and subtle peer indicators **within** a process where many eventually succeed | Same CCT logic may be present, but **marginals + overlap + rare draft** bury the Squid–Jackal contrast until you **condition** |
| What you need | You already had the macro shape | A **microscope** — matched Â × pond plots |

**Do not confuse “Army screams” with “Army K/N is tiny.”** Captain promotion is **not** a 1%-style lottery. The Army is loud because the **tail drop is real and robust in the display** — not because slots are scarcer than the NBA draft (they are not).

**[SCOUT]:** Do not expect another marginal ventile curve to “dip at the elite bin” on POST-QC NCAA data. If CCT is true in NCAA, it will show up when you **hold Â fixed** and compare ponds — not in a single averaged line.

---

## Part 3 — Where this sits in the bigger dissertation story

You started in the **Army**: promotion and selection in peer environments. You found a pattern — advancement vs peer quality often **rises through the middle** and sometimes **softens at the very top** — a **robust macro-level tail drop** that does not need fancy conditioning to see. Most Captains are on a similar track (~**35–40%** promote); **survival analysis** then teases **when** promotion happens and which subtle peer indicators matter inside that mostly-uniform assembly line. You asked: is that special to the Army?

**Basketball** became the working example because you have rich data, a clear scarce outcome (NBA draft), and one slide that captures the phenomenon — the **hero**.

The **Wang-style ladder** you are climbing:

1. **Phenomenon (Layer A)** — What does the data look like? *(Hero, BDP marginals)*
2. **Mechanism story (Layer B)** — Why might peers help and hurt? Congestion in the **score**, not merged with environment. *(Words first)*
3. **Minimal generative test (Layer C)** — Does the smallest fake league show the mechanism **can** bend selection? *(Phase B sim, λ ablation)*
4. **Predictions / fit (Rung 3+)** — MLE, PD14-style checks, conditional empirics. *(Where CCT lives next)*

**[COMPASS]:** Act I of the congestion chapter is now the **BDP deck** you finished today. Act II is **conditional** draft-rate geometry — not another histogram.

---

## Part 4 — What you just built (BDP deck) and why it matters

You finished **`Basics_data_plots_HAND.pptx`** — 21 slides. Source PNGs live in `basic_data_plots/`. The deck walks four **base populations** (all 2011–2021, QC = dash placeholder names removed):

| Population | Plain English |
|------------|---------------|
| **FP 11_21** | Full panel — no minimum games, no minutes floor. Messy but honest about raw ESPN. |
| **mg10 min0** | Drop fragmentary team-seasons (≤10 games). Still all minute levels. |
| **mg10 min10** | Same, but players need ≥10 minutes that season. |
| **mg10 min20** | Same, but ≥20 minutes — **this is your locked hero / ASSIGN panel.** |

For each population (except roster-only slides), you show:

- **Â_i** and **T̂_j** distributions (PPM, then BPM, then OBPM)
- Blue bars = **without DFT** (full filtered population)
- Orange line = **+DFT** (teams that **ever** had a draftee in the 2011–2021 window)
- Roster size |T_j| at the end

**[COMPASS]:** The deck is **Act I: population geometry**. It answers: *What does the league look like? What do draft-ecosystem teams look like compared to the league?* It does **not** yet answer: *At the same Â, does the Squid beat the Jackal?*

That distinction is the whole pivot of this porch reading.

---

## Part 5 — What the new slides actually show (numbers in plain English)

### 5.1 Players spread wide; team averages spread narrow

On almost every BDP slide:

- **Individual player talent Â_i** has standard deviation ≈ **1.0** (by design — within-season z-scores).
- **Team mean talent T̂_j** has standard deviation ≈ **0.25 to 0.43**, depending on metric and filter.

**Plain English:** Stars and bench players differ a lot. **Average team strength differs much less.** Teams are not identical — but team *means* live in a **tighter band** than players do.

This matches HAND17 Slide 5: every team has a **wide internal window** of talent (~3 z from weakest to strongest player), but when you sort teams by T̂_j, the **whole window marches upward** for contenders.

### 5.2 The orange +DFT line — draft-ecosystem zoom

When you overlay teams and players from programs that **ever produced a draft pick** in the window:

**At mg10 min20 (your hero panel), PPM example:**

- **Players (+DFT):** mean shifts up (~+0.09 z); spread **narrows** (sd 1.00 → 0.76, about **24% tighter**).
- **Teams (+DFT):** mean shifts up (~+0.09 z); spread **narrows** again (T̂_j sd 0.25 → 0.19, about **26% tighter**).
- **Counts:** ~46,000 player-seasons without DFT vs ~17,700 +DFT; ~3,842 team-seasons vs ~1,494 +DFT.

**Plain English:** Draft-history teams are **better on average** and **more alike each other** than the full league. The Jackals (contender-ish teams) exist — they are the **right tail** of T̂_j — but they are **few** and **clustered**. You will not see congestion by staring at a histogram of all teams. You must **condition**: pick a talent level, then compare ponds.

### 5.3 What you noticed — OBPM vs BPM compression **[SCOUT]**

At **mg10 min20**, when you compare full league to +DFT, **team-level** spread shrinks more under BPM-family metrics than PPM:

| Metric | T̂_j sd (all) | T̂_j sd (+DFT) | How much narrower? |
|--------|---------------|----------------|---------------------|
| PPM | 0.251 | 0.186 | **26%** |
| BPM | 0.580 | 0.314 | **46%** |
| OBPM | 0.428 | 0.245 | **43%** |

**[SCOUT]’s read:** BPM and OBPM absorb **team role and context**, not just raw production. When you restrict to draft-ecosystem teams, comprehensive metrics **compress** — as if everyone on those rosters gets **re-scaled into a tighter impact band**. At the **team** level, **OBPM** DFT teams are **more alike** (sd 0.25) than **BPM** DFT teams (sd 0.31) — plausible if defensive/role noise widens total BPM spreads.

**[COMPASS]:** Treat BPM/OBPM as **magnifying glasses**, not a new canonical hero. Track C already showed: OBPM/BPM **do not restore** the July elite-bin dip on POST-QC data; they show a **stronger monotonic rise** in the marginal hero curve. Footnote always: BPM merge drops ~1,150 player-seasons vs PPM (Sports-Reference coverage).

### 5.4 Roster **count** is probably not the story **[SCOUT]**

Team-size slides:

- At **FP** (no minutes floor): draft-history teams average **slightly fewer** players (15.4 vs 16.8) — junk roster inflation lives in non-DFT teams.
- At **mg10 min10** and **min20**: DFT and non-DFT are **virtually the same** (~12 players with real minutes; mean |T_j| ≈ 12.0 vs 11.8 at min20; max 19 both).

**Plain English:** Kentucky and Mid-Major U. do **not** differ much on “how many guys played meaningful minutes.” Congestion in your story is **talent stacked into similar roster slots**, not **fewer names on the sheet**.

### 5.5 Which population to use for CCT **[COMPASS]**

| Use for… | Population |
|----------|------------|
| **Mechanism / CCT claims** | **mg10 min20 11_21** (+ optional high-T̂_j slice on top) |
| **Sensitivity** | mg10 min10 |
| **QC storytelling (“why we filter”)** | FP, mg10 min0 |
| **Avoid for CCT claims** | FP min0 alone — cameo noise |

---

## Part 6 — HAND17 Slide 5 — the geometry Ginger can picture

Slide 5 is titled something like **“NCAA team Â_i interval overlap.”** Think of each team-season as a **horizontal bar** on a talent axis:

- **Left end** = weakest player’s talent on the roster  
- **Right end** = strongest player’s talent  
- **Bar height / position** = how good the team is overall (T̂_j)

Facts from the slide (~2015–2019 window):

- **H_sort ≈ 0.10** — teams are **not** neatly sorted; almost everyone overlaps almost everyone.
- **~86%** of the talent grid is covered by **more than one** team at once.
- At the **most common** talent level, **~3,117 team-seasons** have *some* player there — the pond is **crowded horizontally**.
- **Typical roster span** ≈ **2.85 z** — every team has weak and strong players; width does not collapse as teams get better.
- As **T̂_j rises**, intervals **shift right** — contenders have higher floors **and** higher ceilings.

**The Squid vs Jackal picture:**

- Squid star at **+2 z** might be **near the top** of a mid-level team’s window — locally the big fish.
- Jackal player also at **+2 z** might sit on a team whose window runs to **+2.5 or +3** — same number on the stat sheet, **more peers** at that level.

**What Slide 5 shows:** *where* the fish swim.  
**What it does not show:** *who gets drafted* from each pond.  
**What BDP adds:** draft-ecosystem teams sit in a **higher, tighter** T̂_j band.  
**What CCT needs next:** draft rate **on top of** the interval picture — at **fixed Â**.

---

## Part 7 — What the model already taught us (so the empirics are not fishing)

You are not starting from zero. The **fake league** (Phase B) and the **MLE fit** already encode the Squid/Jackal logic.

### 7.1 The score and the knobs

| Piece | Symbol | Role in CCT |
|-------|--------|-------------|
| Own ability | **A_i** (Â_i in data) | How good is the fish? |
| Teammate pond (leave-one-out) | **poolq_loo** | How good are teammates **excluding me**? — **best empirical congestion axis** |
| Team congestion in score | **L_C** | Viable-peer crowding on roster (viability map) |
| Congestion weight | **λ** | How hard L_C penalizes **ranking** |
| Viability sharpness | **γ**, **θ** | Who counts as a “peer” for congestion |
| Selection rule | top-K, Gibbs | Who wins slots **after** scores |
| Sorting on assignment | **ρ** | Separate from score — do not merge |

**[SCOUT]:** In Squid/Jackal prose, say **“teammates around me.”** In plots, use **poolq_loo** first. **T̂_j** (team mean) **includes the player** in the average — slightly wrong label for “pond” (use as secondary axis only).

### 7.2 Phase B sim (HAND16) — the wind tunnel **[COMPASS]**

Old slider exercises still matter:

- **λ > 0** in the **score** bends who gets picked **even when the winner rule is fixed** — pure mechanism proof that “standing out matters.”
- **γ** changes who counts as congestion-bearing.
- **ρ** (assignment sorting) moves team structure — separate from draft score.
- **θ** marks edge-case Squids and Jackals near the viability threshold.
- **K/N** — fraction of the pool that gets the scarce outcome (K winners / N). **Army captain promotion ≈ 35–40%** (high baseline); **NCAA draft ≈ 2–2.5%** on your panel (scarcer). Army **screams** because the **macro hero tail drop is robust**, not because Army K/N is smaller than NCAA. In the **fake league**, K/N is a **sim dial** (θ = F⁻¹(1−K/N); gallery often ~10%) — separate from either empirical rate.
- **PD20 Gibbs SELECT** — softens sharp top-K edges; sensitivity for near-miss cases.

NCAA **ρ* ≈ 0** on the hero panel → **low sorting, high overlap** → exactly the regime where **within-team rank** might disambiguate same-z players better than league sorting does.

### 7.3 MLE fit — the panel “acts as if” congestion matters **[SCOUT]**

Bernoulli MLE on PPM (2013–2021 panel, γ fixed, refit **λ** and **t**):

- **λ̂ ≈ 2.6**
- **t̂ ≈ 1.1**

**Plain English:** Even while the **marginal hero curve** looks flat at the elite tail, a fitted draft model that includes **congestion in the score** finds **non-trivial λ** — the data behave **as if** crowded rosters drag draft log-odds down **after controlling for ability**.

**Critical nuance:** MLE conditions on **A and L_C jointly**. The hero **marginal** curve (draft rate vs poolq_loo bin **only**) **averages over** ability levels. It can **hide** “same A, worse pond hurts.” That is why your CCT can be **true in the model layer** and **invisible on the old slide**.

---

## Part 8 — The hero chart history (why July looked like you, and why we moved on)

| Chart | What it showed | Does it prove CCT? |
|-------|----------------|---------------------|
| **Original hero (R.I.P.)** ~62k rows, min20, **no mg10** | Middle rise, **dip in elite bin** | **Looked** like CCT — but **contaminated** |
| **POST-QC hero (mg10 min20)** | Middle rise, **flat elite tail** | **Does not prove or disprove** — wrong averaging |
| **OBPM/BPM Track C** | **Stronger rise**, no elite dip | Still marginal; **not** inverted-U rescue |
| **July mg=0 replay** | Elite dip **returns** | **Cameo/QC artifact** — not the subtle signal |

**[SCOUT + COMPASS, joint verdict]:**

- The **July inverted-U tail** was mostly **who got dumped into bin 16** (fragmentary teams, cameo players) — not the congestion whisper you want to defend.
- The **POST-QC flat tail** means: if CCT is true in NCAA, it will **not** show up as “bin 16 dips” on a single marginal curve. You must **hold Â fixed** and compare ponds.

**That matches your instinct:** Army screams; NCAA needs a **microscope**, not more ESPN seasons. **[COMPASS]** You and Alex already agree more coverage alone is unlikely to move the CCT needle.

---

## Part 9 — What we have **not** proven yet (honest fence)

Marginal histograms and ventile hero curves answer:

- “What does the league look like?”
- “What do draft-history teams look like vs the league?”

They **do not** answer:

- “For player X at **z = +1.5**, does draft probability **drop** when we move them from a Squid-like team to a Jackal-like team?”

**No disagreement between SCOUT and COMPASS on this.**

Your conviction remains **plausible and structurally supported**. It is **not yet extracted** from NCAA data in the form you need for the dissertation defense — a **conditional** display where Squid and Jackal are **explicitly compared at the same talent**.

---

## Part 10 — The microscope: what to plot next

**[COMPASS] sequencing:** BDP Act I is **done**. Act II should be **one family** of conditional figures before reopening MLE ordering or PD14 debates.

**[SCOUT]:** We are **not** running these until you pick them for the next HAND deck. This is the menu, in priority order.

### Priority 1 — The direct Squid vs Jackal plot (both agents: **start here**)

**Fix a narrow Â_i band** (e.g. z between 1.5 and 2.0, or top decile of ability). **Within that band only**, plot **draft rate** vs:

- **poolq_loo** ventiles (preferred congestion axis), or  
- **T̂_j** ventiles (secondary)

**Squid proxy:** mid pond / mid T̂_j, same Â band.  
**Jackal proxy:** top pond / top T̂_j, same Â band.

**If CCT holds:** the Jackal bar is **lower** than the Squid bar at **same individual talent**.

**Filters:** mg10 min20 11_21; PPM canonical; OBPM/BPM as robustness panels.

This is your thought experiment **literally in the data**.

### Priority 2 — Two-way heatmap **[SCOUT]**

Draft rate in every cell (**Â_i ventile** × **poolq_loo ventile**). The familiar hero curve is a **column average** — it **smears** the story. Look for lower rates in the **upper-right** (high ability, high pond) vs **upper-middle** (high ability, medium pond).

**[SCOUT]:** Signal may live only in the **top 10–15%** of A × top 10–15% of poolq_loo. Full-population plots **drown** it. Use **wider bins at the top** if cell counts get thin (~1,100 total drafts).

### Priority 3 — Within-team rank **[SCOUT] §11.3, [COMPASS] Step B**

Marginal Â and T̂_j miss the missing axis. For each player-season compute:

| Construct | Meaning | CCT role |
|-----------|---------|----------|
| **Roster percentile** | Where Â_i sits within the team (0 = bottom, 1 = top) | “Am I the big fish on this team?” |
| **Headroom** | Gap to best teammate, or count of peers within ε below | “How many rivals at my level?” |
| **N_peers above θ** | Teammates above a viability threshold near me | Empirical face of **L_C** |

**Plot:** Draft rate vs roster percentile, **faceted by T̂_j quartile** — four small panels. **CCT signature:** at high T̂_j, only the **top of the team** keeps draft mass; at mid T̂_j, same z but higher rank → higher rate.

### Priority 4 — Interval overlap + draft **[SCOUT]**

Redo HAND17 Slide 5 logic on the hero panel: color drafted vs not drafted; top T̂_j quartile only; ask whether drafted players cluster on the **leading edge** of each team’s interval.

### Priority 5 — Model-aligned diagnostics **[SCOUT]**

- **L_j^C vs T̂_j** by ventile — high T̂_j should mean higher team congestion; if λ > 0, lower draft odds at given A.
- **MLE residuals** — observed minus predicted draft rate by poolq_loo at **fixed A** — shows where to zoom.

### +DFT zoom (both agents)

Repeat Priority 1–2 on the **+DFT subsample only**. BDP sd compression hints the signal may **sharpen** inside the draft ecosystem. Use +DFT as **magnification**, not as “the answer.”

### When you green-light: **[SCOUT]** build plan

Script name (locked): **`pass_a_congestion_conditional.py`**  
Panel: hero **mg10 min20 11_21** — reuse existing `pass_a_empirical_bundle` path, **no new scrape**.

Outputs to `basic_data_plots/`:

- `BDP_draft_rate_by_ai_band_and_Tj.png` (or poolq_loo variant)
- `BDP_draft_rate_by_roster_percentile_and_Tj.png`
- `BDP_draft_rate_ai_x_poolq_loo_heatmap.png`
- JSON with **cell counts** (guard sparse bins)

---

## Part 11 — What we will **not** do next (save your porch time)

**[SCOUT] list, [COMPASS] endorses:**

1. **More ESPN seasons alone** — unlikely to reveal CCT; you and Alex agree.
2. **Another marginal poolq_loo ventile run** hoping the elite bin dips — Track C closed that path on POST-QC data.
3. **Promoting OBPM or BPM to canonical hero** — useful appendix magnifier, not the main estimand.
4. **Confusing T̂_j with poolq_loo** in talk or slides — Squid/Jackal is about **teammates around the player**, not the team mean label.
5. **Another full ladder of marginal histograms** — Act I is complete.

---

## Part 12 — One paragraph for Alex (Charles or Ginger can read this aloud on the porch)

**[SCOUT] draft, [COMPASS] adopts verbatim:**

> On cleaned NCAA data the simple hero curve rises through the middle and doesn’t show a robust elite dip — the July tail was mostly bad roster rows. But interval overlap shows elite teams stack several players at the same talent level where a mid-major might have one star. Our fitted draft model already puts weight on congestion (λ). The next empirical step is not more bins on the old chart — it’s holding individual talent fixed and comparing draft rates on crowded versus uncrowded ponds. That’s the Squid versus Jackals test.

---

## Part 13 — Who does what when you pick the next plot

| Job | Owner |
|-----|--------|
| BDP Â / T̂ / roster ladders | **Done** (you + scripts) |
| Matched Â × pond draft-rate plots | **SCOUT** |
| Interval overlap conditional on draft | **SCOUT** |
| L_C vs T̂_j diagnostic | **SCOUT** |
| Slide wording, ladder order, sequencing | **COMPASS** |
| HAND deck assembly, Change Picture | **Charles** |

When you name the first plot for the next HAND deck, tell us the slide title + filter ladder — or lock specs in **[`CCT_Campaign_Plan.md`](CCT_Campaign_Plan.md)** §11 and green-light SCOUT. We are ready.

---

## Part 14 — Bottom line (the great news you waited for)

1. **Your CCT is coherent.** It fits Army, the model (λ, score vs select), HAND17 intervals, and today’s BDP +DFT overlays.

2. **The BDP deck is a success.** You now have a shared visual language: FP → hero panel, three perf metrics, draft-ecosystem zoom. **Act I is closed.**

3. **Your OBPM/BPM compression instinct is real.** Comprehensive metrics **magnify** how alike draft-ecosystem teams look. Use as sensitivity, not canon.

4. **Congestion is not roster headcount** at min20. It is **talent stacked into similar-minute rosters** — rank and interval geometry.

5. **The old hero elite dip is not coming back** on POST-QC marginals — and that is **not** a defeat. CCT was never primarily “bin 16 goes down.”

6. **The way forward is conditional, not marginal:** same **Â**, compare draft odds across **pond thickness** and **within-team rank** — on **mg10 min20**, zoomed to the top of the ability × pond grid.

7. **SCOUT and COMPASS agree completely** on substance today. No fork in the road — one next step: **Priority 1 matched plot**.

---

## Glossary (inline — no scavenger hunt)

| Term | Plain English |
|------|---------------|
| **Â_i** | Empirical player ability (PPM/BPM/OBPM z within season) |
| **T̂_j** | Mean player ability on team j that season |
| **poolq_loo** | Leave-one-out mean teammate quality — “pond excluding me” |
| **L_C** | Team congestion in the **score** (viability-weighted peers) |
| **λ** | Weight on congestion in ranking: S = A − λ L_C |
| **DFT / +DFT** | Team-seasons with ≥1 draftee in 2011–2021; orange **player** histogram = all players on those teams (not drafted-only) |
| **mg10** | Drop team-seasons with ≤10 games |
| **min20** | Players need ≥20 minutes that season |
| **H_sort** | How sorted teams are on talent (~0.1 = heavy overlap) |
| **Hero** | Draft rate vs teammate-quality ventiles (outcome chart) |
| **CCT** | Big fish / small pond vs small fish / big pond at **same talent** |
| **K/N** | Winners / pool size. Army promotion ~35–40%; NCAA draft ~2–2.5%. “Army screams” = macro tail drop, **not** tiny Army K/N |

---

## Where the pieces live (if you want to dig later)

| Artifact | Path |
|----------|------|
| BDP slide exports | `HEROs_and_PASSes/slides/Basics_data_plots_HAND/` |
| BDP source PNGs + JSON | `HEROs_and_PASSes/basic_data_plots/` |
| HAND17 interval slide | `slides/CHAR_PD17_HAND/Slide5.png` |
| Agent memo pair (technical) | `SCOUT_and_COMPASS/20260820_*.md` |
| Track C BPM/OBPM note | `SCOUT_and_COMPASS/20260820_1302_SCOUT_to_COMPASS_track_c_bpm_obpm_robustness.md` |
| Big-picture dissertation arc | `HEROs_and_PASSes/PD20_22_campaign_big_picture.md` |
| **CCT Campaign Plan (Act II checklist)** | `SCOUT_and_COMPASS/CCT_Campaign_Plan.md` |
| Binding score vs select | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` |

---

*Charles — you asked your fellows **SCOUT** and **COMPASS** for a plain-spoken porch read you could share with **Ginger**. Here it is. The pond is real. The fish can be the same size. The question is how many same-size fish swim beside each one — and whether the draft notices. We believe you. When you're ready, we'll build the microscope.*

*(Twenty years married September 11 — congratulations to you and Ginger.)*

— **SCOUT** and **COMPASS**, your fellas
