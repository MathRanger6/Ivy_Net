# SCOUT + COMPASS — Wisdom on the Central Contention (CCT)

**Date:** 2026-08-20  
**To:** Charles  
**From:** SCOUT and COMPASS (joint memo)  
**Print for porch:** **[`20260820_COMPASS_Charles_CCT_porch_reading.md`](20260820_COMPASS_Charles_CCT_porch_reading.md)** — unified narrative (start here). This file = technical supplement.

**Trigger:** You finished the first **Basics_data_plots_HAND** deck; you asked us to read the PNG exports, connect them to **HAND17 Slide 5** (interval overlap), and help find how to **illuminate** the big-fish / small-pond story in NCAA data.

**See also:** COMPASS standalone memo (same folder) — [`20260820_COMPASS_BDP_congestion_CCT_wisdom.md`](20260820_COMPASS_BDP_congestion_CCT_wisdom.md). Cross-read addendum at **§11** below.

**Your CCT in one sentence:** A great player on a pretty-good team (Squids) should be **more likely drafted** than a player of the **same individual talent** on a contender (Jackals), because the Jackals roster is **crowded** with other great players — congestion hurts each of them in the race for scarce draft slots.

We believe you. The Army data scream this. NCAA may whisper. This memo says what we see so far, what the **model** already teaches us, and what **populations / filters / scales** might make the whisper louder.

---

## 0. What we read

| Deck | Slides | Role |
|------|--------|------|
| `slides/Basics_data_plots_HAND/` | 1–21 exports | BDP ladder: PPM / BPM / OBPM; FP → mg10 → min10/min20; Â_i, T̂_j, roster size |
| `slides/CHAR_PD17_HAND/Slide5.png` | Interval overlap 2015–2019 | Team talent windows stack as T̂_j rises |
| `basic_data_plots/*.png` + JSON | Source figures behind BDP | Numeric SD means, n’s |
| Prior hero / Track C | `pass_a/`, `pass_a/sensitivity/` | Draft rate vs **poolq_loo** ventiles |

---

## 1. What the BDP deck already shows (empirical facts)

### 1.1 Player talent spreads wide; team mean talent spreads narrow

On almost every BDP slide (PPM, BPM, OBPM):

- **Â_i** (player) has SD ≈ **1.0** (by construction — z within season).
- **T̂_j** (team mean) has SD ≈ **0.25–0.43** depending on metric and filter.

**Plain English:** Individual players differ a lot. **Average team strength differs much less.** That does *not* mean “all teams are the same” — it means team means live in a **tight band**, while stars and bench players live in a **wide band**.

This matches HAND17 Slide 5: roster **intervals** (min–max Â on a team) are ~3 z wide, but when you sort teams by T̂_j the **whole interval marches upward** — contenders have higher floors *and* higher ceilings.

### 1.2 The “+DFT” overlay is a compressed, shifted subset

When we overlay player-seasons / team-seasons that **ever produced a draft pick** (orange line):

| Population (example: **mg10 min20 11_21**) | Â_i DFT | T̂_j DFT |
|--------------------------------------------|---------|---------|
| **OBPM** | mean +0.12, SD **0.64** (vs 1.0 all) | mean +0.13, SD **0.25** (vs 0.43 all) |
| **BPM** | mean +0.12, SD **0.61** | mean +0.12, SD **0.31** (vs 0.58 all) |
| **PPM** | mean +0.09, SD **0.76** | mean +0.09, SD **0.19** (vs 0.25 all) |

**What you noticed (OBPM vs BPM SD):**

- At **player** level, DFT pools are similarly ** tightened** (OBPM 0.64 vs BPM 0.61 at min20).
- At **team** level, **OBPM DFT teams are more compressed** (T̂_j SD **0.25**) than **BPM DFT teams** (T̂_j SD **0.31**). Contender teams look **more alike** on offensive BPM than on total BPM — plausible if defense/extra-role noise widens BPM team spreads.

**Implication for CCT:** The Jackals *exist* in data — they are the right tail of T̂_j — but they are **few** and **clustered**. You will not see congestion in a **histogram of all teams**; you have to **condition** on “high T̂_j” and then compare **players at fixed Â**.

**COMPASS add — full T̂_j SD compression at mg10 min20 (% narrower, full → +DFT):**

| Metric | sd (without) | sd (+DFT) | % narrower |
|--------|--------------|-----------|------------|
| PPM | 0.251 | 0.186 | **26%** |
| BPM | 0.580 | 0.314 | **46%** |
| OBPM | 0.428 | 0.245 | **43%** |

Player Â_i +DFT sd / full sd at min20: PPM **0.76**, BPM **0.61**, OBPM **0.64**. BPM/OBPM are **magnifying glasses**, not canonical hero ([Track C memo](20260820_1302_SCOUT_to_COMPASS_track_c_bpm_obpm_robustness.md)).

### 1.3 Roster **count** is probably not the congestion channel (at min10+)

BDP team-size slides:

- **FP** (no min): DFT teams slightly **smaller** on average (15.4 vs 16.8 players) and much **less variable** — junk roster inflation lives in non-DFT teams (walk-ons, cameos).
- **mg10 min10**: DFT and non-DFT are **virtually identical** (~12.6–12.7 players with ≥10 minutes, SD 1.6).

**Plain English:** Kentucky and Mid-Major U. do **not** differ much on “how many guys played real minutes.” Congestion in your story is **talent stacking**, not **headcount**.

### 1.4 Four base populations (Slide 5) — good ladder

Your four bases (all 11_21):

1. **FP** — QC only (dash names out), no mg, no min  
2. **mg10 min0** — serious team-seasons, all minute levels  
3. **mg10 min10** — rotation-ish  
4. **mg10 min20** — hero-aligned  

**COMPASS read:** For **CCT exposition**, prioritize **mg10 min20** (same estimand as locked hero) *plus* a deliberate **high-T̂_j slice** on top — not FP alone (too much cameo noise) and not min0 unless you are diagnosing QC.

---

## 2. What HAND17 Slide 5 adds (why intervals matter for CCT)

Slide 5 (`PD17 — NCAA team Â_i interval overlap`):

- **H_sort ≈ 0.105** — teams are **not** neatly sorted; massive **overlap** at most talent levels (~86% of the spectrum covered by >1 team).
- **At the modal talent level, ~3,117 team-seasons** have *some* player there — the pond is **crowded horizontally**.
- **Roster span** median ~2.85 z — every team has weak and strong players on the roster.
- **Sorted interval plot:** as T̂_j rises, intervals **shift right** — Jackals have **multiple** players at Squid-star levels *and* higher.

**This is the structural precondition for CCT:**  
Squid star at Â ≈ +2 sits in a band where fewer teammates share that height.  
Jackal player at Â ≈ +2 sits on a team whose **interval** also reaches +2.5 or +3 — same individual tag, **richer teammate field**.

The interval slide shows **where** the fish swim. It does **not** yet show **who gets drafted** from each pond — that needs a **draft-rate** layer on top.

---

## 3. What the **model** already discovered (levers that help)

Remember the binding ladder ([`BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md)):

| Piece | Symbol | What it does for CCT |
|-------|--------|----------------------|
| **Own ability** | **A_i** (Â_i empirically) | “How good is the fish?” |
| **Teammate field (LOO)** | **poolq_loo** | “How good is the pond *excluding me*?” — **direct empirical congestion proxy** |
| **Team congestion (not LOO)** | **L_j^C** | Viability-weighted crowding on roster; used in **score**, not LOO |
| **Scoring** | **S_i = A_i − λ·L^C** | Congestion enters **rank**, not environment B−D |
| **Selection** | top-K / softmax | Who wins slots **after** scores |
| **γ** | viability sharpness | Who counts as a “viable” draft peer on the roster |
| **λ** | congestion weight in score | MLE **λ̂ ≈ 2.6** — congestion **matters** in fitted Bernoulli draft model |
| **t** | talent scale in softmax | MLE **t̂ ≈ 1.1** |

### 3.1 Old widgets (Phase B sim) — still valid intuition

PD16 / grandchild sliders showed:

- **λ > 0** in the **score** bends who gets picked **holding the winner rule fixed** — that is exactly “same talent, worse odds if crowded.”
- **γ** changes **who counts** as congestion-bearing peers.
- **ρ** (ASSIGN) changes sorting — separate from draft **score** (do not merge).

**Model lesson:** CCT is a **selection / scoring** story, not “bad teammates hurt your stats.” The empirical axis that matches **scoring congestion** is **poolq_loo** (or L^C), not raw T̂_j alone.

### 3.3 Phase B sim levers (COMPASS add — HAND16)

Beyond λ and γ sliders:

- **ρ (ASSIGN)** vs **L_C** — Sketch A: sorting and team congestion move together; NCAA ρ* ≈ 0 on hero panel → **low sorting, high overlap** → within-team rank may matter *more* for disambiguating same-z peers.
- **θ** — viability threshold; near-threshold players = Squid/Jackal edge cases.
- **K/N** — winners / pool. Army promotion ~35–40%; NCAA draft ~2–2.5%. Army **screams** (macro tail drop), not because Army K/N is tiny. Sim K/N is a separate dial (θ rule).
- **PD20 Gibbs SELECT** — stochastic select sensitivity for near-cutoff players.

Environment **B − D** is **not** the draft-rank story — do not merge with **S_i = A_i − λ L_C** ([`BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md)).

### 3.2 MLE fit (PPM-based, 2013–2021)

Bernoulli MLE with **γ fixed, then refit λ and t** finds **non-trivial λ** — the panel behaves **as if** crowded rosters drag draft log-odds down, **after** controlling for A. That supports CCT **in the model layer** even while the **hero ventile** plot looks flat at the elite tail POST-QC.

**Important:** MLE conditions on **A and L^C** jointly. The hero **marginal** curve (draft rate vs poolq_loo bin only) **averages over** A — it can hide “same A, worse pond hurts.”

---

## 4. Why the classic hero slide did not “prove” CCT (and what July was)

| View | What it shows | CCT-friendly? |
|------|---------------|---------------|
| **Original HERO (R.I.P., Slide 2)** n≈62k, min20, **no mg10** | Peak ~bin 12, **dip bin 16** | **Looks** like CCT — but contaminated |
| **POST-QC hero (mg10 min20)** | Middle rise, **flat elite tail** | **Does not** show dip — **marginal** curve |
| **OBPM/BPM Track C** | **Stronger monotonic rise**, no dip | **Opposite** of inverted-U; still marginal |
| **July mg=0 replay** | Elite dip returns | **Cameo / CPR** artifact (B5–B6), not OBPM rescue |

**SCOUT + COMPASS honest verdict:**

- The **July inverted-U tail** was mostly **who is in bin 16** (cameo teams), not the subtle congestion signal you want for the dissertation defense.
- The **POST-QC flat tail** means: **if CCT is true in NCAA, it is not visible in a single marginal ventile curve** — it is **too subtle** or **confounded** unless you **hold Â fixed** and compare ponds.

**That matches your instinct:** Army = loud; NCAA = need a **microscope**, not a wider ESPN scrape.

---

## 5. How to “bring CCT to empirical day” — plot ideas we would try next

We are **not** running these until you pick them for **Basics_data_plots_HAND**. This is the menu.

### 5.1 The direct CCT plot (highest priority)

**Matched comparison:** Fix **Â_i bin** (e.g. z ∈ [1.5, 2.0] or top decile of A). Within that band, plot **draft rate vs T̂_j bin** (or vs **poolq_loo** bin).

- **Squid proxy:** mid T̂_j ventile, same A band.  
- **Jackal proxy:** top T̂_j ventile, same A band.  

**If CCT holds:** right bar **lower** than middle bar at **same A**.

**Filters:** **mg10 min20 11_21**; perf = PPM canonical, robustness OBPM/BPM.

**Why this works:** It is the Squid-vs-Jackal thought experiment **literally in the data** — not an average over all abilities.

### 5.2 Two-way heatmap

**Draft rate** in cells (**Â_i ventile** × **poolq_loo ventile**).

- Marginal curves are **column averages** — they smear the diagonal story.
- Look for **lower draft rate upper-right** (high A, high pond) vs **upper-middle** (high A, medium pond).

### 5.3 “Within-team rank” view (PD17 intervals + draft)

On **top T̂_j decile** teams only:

- Rank players by Â within team.
- Compare draft rate for **#1 on team** vs **#2–#3 at similar Â** vs **same Â on mid-T teams**.

Speaks directly to “Jackals have *several* Squid-level players.”

### 5.4 Interval overlap **conditional on draft**

Redo HAND17 Slide 5 **split**:

- Teams with ≥1 draft pick vs without.
- Top T̂_j quartile only — do drafted teams’ intervals **stack more mass** at high Â?

You already see DFT teams shifted right on T̂_j; next step is **overlap at fixed Â**.

### 5.5 Congestion diagnostic L_j^C vs T̂_j

Plot **L_j^C distribution** by T̂_j ventile (not LOO — team-level congestion from viability map).

**Model prediction:** high T̂_j → higher L^C → if λ>0, hurts draft odds **at given A**.

Empirical pd17/grandchild scripts exist; point output to `basic_data_plots/`.

### 5.6 Residual plot from MLE

From fitted Bernoulli model: **observed − predicted** draft rate binned by **poolq_loo** at **fixed A**. Shows where simple softmax still misses — guides where to zoom.

### 5.7 +DFT zoom (COMPASS add — from BDP orange line)

Use +DFT **not** as the answer but as **draft-ecosystem magnification**:

- Repeat §5.1–5.2 on +DFT subsample — signal may **sharpen** (SD compression hints at this).
- Compare overlap at fixed Â between DFT vs non-DFT team-seasons.

### 5.8 First SCOUT script (COMPASS name lock)

When Charles picks a plot: **`pass_a_congestion_conditional.py`** (TBD) on hero panel mg10 min20 →  
`PASS_A_draft_rate_by_ai_band_and_Tj.png`, `PASS_A_draft_rate_by_roster_percentile_and_Tj.png` + JSON cell counts. Reuse `pass_a_empirical_bundle` panel path — no new scrape.

---

## 6. Populations, filters, scales — our recommendation

| Choice | Recommendation | Why |
|--------|----------------|-----|
| **QC baseline** | Dash names out only | Your BDP rule — do not sneak mg10 in |
| **Primary ladder** | **mg10 min20 11_21** | Same as locked hero + draft estimand |
| **Secondary** | **mg10 min10** | Sensitivity — more players, noisier A |
| **Avoid for CCT claims** | **FP min0** | Cameo inflation; good for QC story, bad for congestion |
| **Ability scale** | **PPM** canonical; **OBPM** for offensive “star” read | BPM blends O+D; you saw OBPM compresses DFT teams more |
| **Congestion axis** | **poolq_loo** first, **T̂_j** second | poolq_loo = LOO pond; T̂_j = team mean (includes you in team average — slightly wrong pond for CCT) |
| **Bins** | 8–16 ventiles; consider **wider bins at top** for n | Draft n≈1,100 — thin cells kill signal |
| **Outcome** | **Y_draft ever** on 11_21 | Same as hero |

**Scale zoom:** The signal may live in **top 10–15% of A** × **top 10–15% of poolq_loo** only — full-population plots will **drown** it.

---

## 7. What we would **not** do next (save time)

- More ESPN seasons alone — you and Alex already agree: unlikely to move CCT needle.
- Another marginal **poolq_loo** ventile rerun hoping for inverted-U — Track C closed that.
- Promoting OBPM to canonical hero — useful robustness, not the congestion expositor.
- Confusing **T̂_j** with **poolq_loo** in prose — Squid/Jackal is about **teammates around the player**, not team mean label.

---

## 8. One paragraph you can say to Alex (draft)

*“On cleaned NCAA data the simple hero curve rises through the middle and doesn’t show a robust elite dip — the July tail was mostly bad roster rows. But interval overlap shows elite teams stack several players at the same talent level where a mid-major might have one star. Our fitted draft model already puts weight on congestion (λ). The next empirical step is not more bins on the old chart — it’s holding individual talent fixed and comparing draft rates on crowded versus uncrowded ponds. That’s the Squid versus Jackals test.”*

---

## 9. Who does what when you pick plots

| Plot type | Owner |
|-----------|--------|
| BDP Â/T̂/roster ladders (done) | COMPASS + SCOUT scripts |
| **Matched A × pond draft-rate** (§5.1–5.2) | **SCOUT** — new script, `basic_data_plots/` |
| Interval overlap conditional (§5.4) | **SCOUT** — extend pd17 overlap |
| L_j^C by T̂_j (§5.5) | **SCOUT** — grandchild/pd17 path |
| Slide wording / ladder order | **COMPASS** |
| HAND deck assembly | **Charles** |

---

## 10. Bottom line

**Your CCT is coherent with:**

- Army evidence (loud),
- Model structure (**λ**, poolq_loo, score vs select),
- HAND17 intervals (Jackals **can** host multiple stars),
- BDP DFT overlays (drafted teams are **higher T̂_j**, **tighter** talent bands).

**It is not yet visible in:**

- Marginal POST-QC hero ventiles (flat elite tail),
- BPM/OBPM robustness (monotone rise).

**The way forward is conditional, not marginal:** same **Â**, compare draft odds across **pond** thickness — heatmaps, matched bins, within-team ranks — on **mg10 min20**, zoomed to the top of the A × poolq_loo grid.

When you name the first plot for **Basics_data_plots_HAND**, use the template from COMPASS: slide title + source + filter ladder. We are ready.

**Memo pair (Aug 2026):**

| File | Emphasis |
|------|----------|
| `20260820_COMPASS_BDP_congestion_CCT_wisdom.md` | BDP deck numbers, SD tables, Step A–E ladder |
| `20260820_1726_SCOUT_COMPASS_CCT_big_fish_small_pond_wisdom.md` | CCT story, plot menu, MLE, July autopsy, Alex line |

— **SCOUT** (data / scripts / numbers) + **COMPASS** (sequencing / framing / Alex line)

---

## 11. SCOUT addendum — after reading COMPASS memo (20260820)

COMPASS wrote the sibling doc same day. SCOUT adds **numbers and build detail** COMPASS emphasized; we agree on direction.

### 11.1 BPM/OBPM compression — percent table (mg10 min20)

**T̂_j** sd shrink (full → +DFT):

| Metric | sd (all) | sd (+DFT) | % narrower |
|--------|----------|-----------|------------|
| PPM | 0.251 | 0.186 | **26%** |
| BPM | 0.580 | 0.314 | **46%** |
| OBPM | 0.428 | 0.245 | **43%** |

**SCOUT read:** BPM family **magnifies** “draft-ecosystem teams look alike” more than PPM. Use as **sensitivity magnifier**, not canonical hero (Track C closed promotion).

### 11.2 Roster size at min20 (exact BDP JSON)

- without DFT: **n = 3,842** team-seasons, mean |T_j| ≈ **12.0**, max 19  
- +DFT: **n = 1,494**, mean |T_j| ≈ **11.8**, max 19  

Congestion ≠ fewer bodies on the roster at hero minutes floor.

### 11.3 Missing axis for CCT — **within-team rank** (COMPASS Step B)

Marginal Â and T̂_j are not enough. SCOUT will compute on hero panel:

| Construct | Definition | CCT role |
|-----------|------------|----------|
| **Roster percentile** | rank of Â_i within `(team_id, season)` | “Am I the big fish on this team?” |
| **Headroom** | Â_i − max(teammates) or # teammates within ε below | “How many peers at my level?” |
| **N_peers above θ** | #{teammates : Â_k > Â_i − δ} | empirical face of **L^C / viable-peer density** |

**ρ* ≈ 0**, **H_sort ≈ 0.1** on NCAA → low league sorting, heavy overlap → **within-team rank** may disambiguate same-z Squids vs Jackals better than T̂_j alone.

### 11.4 Phase B knobs COMPASS flagged (SCOUT agrees)

- **θ** (viability): who counts as a congestion peer — edge cases live near threshold.  
- **K/N**: Army promotion ~35–40% (high baseline); NCAA draft ~2–2.5%. Army **screams** at macro level (tail drop); NCAA **whispers** until conditional plots — **not** because Army slots are scarcer.  
- **PD20 Gibbs SELECT**: soften top-K — sensitivity for near-miss draft cases.  
- **λ ablation** (HAND16): already proves mechanism *can* bend curves in sim.

### 11.5 Proposed script (when Charles green-lights)

`pass_a_congestion_conditional.py` (name TBD) — hero panel **mg10 min20 11_21**, outputs to `basic_data_plots/`:

- `BDP_draft_rate_by_ai_band_and_Tj.png`  
- `BDP_draft_rate_by_roster_percentile_and_Tj.png`  
- `BDP_draft_rate_ai_x_poolq_loo_heatmap.png`  
- JSON with **cell n** (guard sparse bins)

Reuse `pass_a_empirical_bundle` panel path; **no new scrape**.

### 11.6 Track C tie-in COMPASS stated clearly

Marginal OBPM/BPM hero curves show **stronger elite rise**, not dip. CCT cannot be “bin 16 dips” on POST-QC; it must be **within-bin counterfactual** (same Â, worse pond/rank).

**Status:** Joint memo + COMPASS memo are **aligned**. BDP deck **closed** for Act I. Next figure = **conditional**, not another marginal histogram.

