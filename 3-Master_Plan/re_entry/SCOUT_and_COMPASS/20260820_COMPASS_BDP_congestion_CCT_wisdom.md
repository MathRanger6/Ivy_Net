# COMPASS (+ SCOUT read) — BDP deck wisdom for the congestion story (CCT)

**Date:** 2026-08-20  
**Audience:** Charles (and future SCOUT/COMPASS turns)  
**Print for porch:** **[`20260820_COMPASS_Charles_CCT_porch_reading.md`](20260820_COMPASS_Charles_CCT_porch_reading.md)** — unified narrative (start here). This file = technical supplement.

**Trigger:** Charles finished **`Basics_data_plots_HAND.pptx`** (21 slides + PNG exports).

**Companion memo (SCOUT cross-read, same day):** [`20260820_1726_SCOUT_COMPASS_CCT_big_fish_small_pond_wisdom.md`](20260820_1726_SCOUT_COMPASS_CCT_big_fish_small_pond_wisdom.md) — joint CCT memo with plot menu §5, MLE λ̂, July autopsy, **poolq_loo vs T̂_j** lock, Alex paragraph, ownership table, and **§11 SCOUT addendum** after this cross-read. **Read both.**

**Sources reviewed this session:**  
`slides/Basics_data_plots_HAND/Slide*.png`, all `basic_data_plots/BDP_*.json`, HAND17 Slide 5 (interval overlap), Track C memo, `PD20_22_campaign_big_picture.md`, Phase B λ / L_C characterization logic.

**See also:** Joint SCOUT+COMPASS memo — [`20260820_1726_SCOUT_COMPASS_CCT_big_fish_small_pond_wisdom.md`](20260820_1726_SCOUT_COMPASS_CCT_big_fish_small_pond_wisdom.md). Cross-read addendum at **§10** below.

---

## 0. Plain-English restatement of the mission

You are **not** asking “do good players get drafted?” — everyone knows that.

You are asking: **holding talent fixed**, does **where you sit on the roster ladder** and **how crowded that ladder is** change draft odds? Army data scream this. NCAA data might **whisper**. The BDP deck was step one: **what do the pools look like** when we walk from the full messy league (FP) toward the hero panel (mg10 min20) and toward **draft-history teams** (+DFT orange line)?

That is the right ladder. The deck answers **population geometry**. It does **not yet** answer the **matched-player** Squid-vs-Jackal claim. That is the next zoom.

---

## 1. What the BDP slides already show (empirical facts)

### 1.1 Four base populations (Slide 5) — keep using them

| Spec | Role |
|------|------|
| **FP 11_21** | “Whole messy league” — shows why QC + mg matter (68-player roster freak tails) |
| **mg10 min0** | Real D-I team-seasons, still fat player minutes tail |
| **mg10 min10** | Starts trimming bench clutter |
| **mg10 min20** | **Hero-aligned** — Pass A / ASSIGN panel you defend |

**COMPASS note:** CCT testing should **live on mg10 min20** (and maybe min10 as sensitivity). FP is for “why we filter,” not for mechanism claims.

### 1.2 Marginal distributions — Â_i and T̂_j (Slides 7–18)

**Player ability Â_i (left panel):**

- Full pool: mean ≈ 0, sd ≈ 1 (by construction — within-season z).
- **+DFT orange line:** mean **rises** (~+0.09 PPM, ~+0.12 BPM/OBPM at min20); sd **falls** (PPM +DFT sd ≈ 0.76 vs 1.00 → **24% narrower** at min20).

**Interpretation in plain words:** Players on teams that **ever produce draftees** are not a random slice of the league — they are **better on average** and **less spread out**. That is consistent with “draft talent lives in a tighter band,” but it is **not yet** the Squid-vs-Jackal **within-talent** comparison.

**Team talent T̂_j (right panel):**

- Full pool: T̂_j is **already narrow** (PPM sd ≈ 0.25 at min20 — team means do not wander far in z space).
- **+DFT:** mean shifts **up**; sd **compresses again** (PPM +DFT T̂_j sd ≈ 0.19 → **26% narrower**).

**Interpretation:** “Contender-ish” team-seasons (draft-history teams) cluster in a **higher, tighter** T̂_j band. The Jackals live in a **wider** cloud of team contexts. Your CCT lives in the **overlap region** of those clouds — HAND17 Slide 5 — not in the marginals alone.

### 1.3 Roster size |T_j| (Slides 19–21)

At **mg10 min20**:

- without DFT: **n = 3,842** team-seasons, mean |T_j| ≈ **12.0**, max 19  
- +DFT: **n = 1,494**, mean |T_j| ≈ **11.8**, max 19  

**Important negative finding for a *simple* story:** Contender teams are **not** carrying **fewer** listed players in this panel. Congestion in NCAA is **not** “they have smaller rosters.” It is **more talent packed into similar roster slots** — an **interval / rank** story, not a headcount story.

### 1.4 OBPM vs BPM — what caught your eye (Slide 17 vs 13)

At **mg10 min20**, **T̂_j** sd compression (full → +DFT):

| Metric | sd (without DFT) | sd (+DFT) | % narrower |
|--------|------------------|-----------|------------|
| PPM | 0.251 | 0.186 | **26%** |
| BPM | 0.580 | 0.314 | **46%** |
| OBPM | 0.428 | 0.245 | **43%** |

**Player Â_i** compression at min20:

| Metric | sd (+DFT) / sd (full) |
|--------|------------------------|
| PPM | 0.76 |
| BPM | 0.61 |
| OBPM | 0.64 |

**SCOUT read — why BPM/OBPM “scream” more than PPM:**

1. **BPM family measures role/team context**, not just box-score production. When you restrict to draft-ecosystem teams, **both** individual and team BPM spreads **collapse** — as if “being on those teams” **re-scales** everyone into a tighter impact band.
2. **OBPM vs BPM:** offensive component compresses almost as much as total BPM for T̂_j — the **congestion signal in comprehensive metrics** is not only “defense hid your offense.”
3. **Do not promote BPM/OBPM to canonical hero** (Track C closed that). **Do** use them as **magnifying glasses**: if CCT is subtle in PPM, it may show up **stronger** in metrics that absorb **team role crowding**.

**Caution:** BPM merge drops ~1,150 player-seasons vs PPM — always footnote SR coverage.

---

## 2. HAND17 Slide 5 — why it pairs with BDP

Slide 5 (2015–2019 interval overlap) is the **geometry** your CCT needs:

- **H_sort ≈ 0.105** — teams are not neatly sorted; massive overlap (~**86%** of the talent grid covered by >1 team).
- At the modal talent level, **~3,117 team-seasons** have *some* player there — horizontal crowding.
- **Roster span** median ~**2.85 z** — every team has weak and strong players; width does not shrink as T̂_j rises.
- Each team draws a **talent window** [min Â_i, max Â_i] on the PPM z axis.
- Windows **stack vertically** as **T̂_j rises** — better teams shift intervals up; Jackals host **multiple** players at Squid-star levels *and* higher.

**Connect to Squids vs Jackals in words:**

- Squid star near the **top of a mid window** → locally “big fish.”
- Jackal player at the **same z** might sit **mid-pack** on a window that slid right — same fish, more peers at that level.

**BDP marginals say:** draft teams sit in a **higher, tighter** T̂_j band.  
**Interval slide says:** even there, **windows overlap** — so same-z players on different teams can face **different within-team ranks**.  
**CCT says:** draft odds should track **within-team prominence**, not z alone.

That triangle is the empirical path.

---

## 3. What the **model** already taught us (levers that matter)

Binding stack (do not merge):

| Layer | Knob / object | What it does for CCT |
|-------|----------------|----------------------|
| **Environment** | B − D, L_net | Peers help vs hurt **development** — **not** the draft pick rule |
| **SCORE** | **S_i = A_i − λ L_C** | **Rank** penalized by **team congestion L_C** (viable peers above θ) |
| **SELECT** | top-K, Gibbs T | **Who wins** slots given ranks — separate from score |
| **Hero** | draft rate vs poolq_loo | **Outcome** — mixes score + select + real NBA behavior |

**Phase B (HAND16) discoveries relevant to CCT:**

1. **λ ablation:** With congestion in the **score**, selection curves **bend** vs talent-only (λ=0). That is the **wind-tunnel proof** that your mechanism *can* produce “standing out matters.”
2. **L_C vs ρ (Sketch A):** Team congestion and sorting move together in sim — when teams are more assortative, **L_C** distribution shifts. NCAA ρ* ≈ 0 on hero panel → **low sorting**, high overlap → **exactly** the regime where within-team rank might matter *more* for disambiguating peers at the same z.
3. **θ (viability threshold):** Controls who counts as a “peer” in L_C. Near-threshold players are your Squid/Jackal edge cases.
4. **K/N (selectivity dial):** K winners / N in pool. **Army captain promotion ≈ 35–40%** — high baseline, assembly-line process; Army **screams** via a **robust macro tail drop**, not via tiny K/N. **NCAA draft ≈ 2–2.5%** on the hero panel — scarcer outcome, but CCT still **whispers** in marginals until conditional plots. In Phase B sim, K/N is a **knob** (θ = F⁻¹(1−K/N)); fewer sim slots → congestion in **score** bites harder at the top **in the wind tunnel**, not a claim that Army slots are scarcer than NBA picks.
5. **PD20 Gibbs SELECT:** Stochastic select can smooth sharp top-K edges — sensitivity for “almost drafted” cases.

**What the model does *not* yet do for NCAA:** It does **not** automatically extract matched Squid/Jackal pairs from real rosters. You still need an **empirical conditional plot** designed for that question.

### 3.1 MLE fit (SCOUT add — PPM panel, 2013–2021)

Bernoulli MLE with **γ fixed, then refit λ and t** finds **non-trivial λ̂ ≈ 2.6** and **t̂ ≈ 1.1** — the panel behaves **as if** crowded rosters drag draft log-odds down **after** controlling for A. That supports CCT **in the model layer** even while the **hero ventile** plot looks flat at the elite tail POST-QC.

**Important:** MLE conditions on **A and L^C** jointly. The hero **marginal** curve (draft rate vs poolq_loo bin only) **averages over** A — it can hide “same A, worse pond hurts.” See joint memo §3.2.

### 3.2 Congestion axis lock (from SCOUT joint memo)

| Axis | Use for CCT? | Why |
|------|--------------|-----|
| **poolq_loo** | **Primary** | LOO teammate pond — “crowding **excluding me**”; matches **score** congestion story |
| **T̂_j** | Secondary | Team mean **includes** the player — slightly wrong pond label for prose |
| **L_j^C** | Model-aligned diagnostic | Team viability congestion; plot by T̂_j ventile (joint memo §5.5) |

---

## 4. What **empirical Pass A** already said (and did not say)

**POST-QC hero (mg10 min20, poolq_loo):**

- Draft rate **rises** through middle teammate-quality bins.
- Elite tail **flat**, not inverted-U (July dip = mg0 artifact; Track C: BPM/OBPM **stronger monotonic rise**, not concavity).

**Implication for CCT:** The **hero bins by team pool quality** — not by **within-team rank at fixed A_i**. A flat elite tail **does not falsify** congestion; it may **hide** it because bin 16 mixes Squids and Jackals at different **ranks** inside the bin.

**Track C punchline:** OBPM/BPM **increase** the middle-to-elite gradient (β₂ more positive). If anything, comprehensive metrics say “elite context correlates with **higher** draft rate,” not lower — so CCT must be searched as a **counterfactual within bin**, not as “elite bin dips.”

### 4.1 July hero autopsy (SCOUT add — why the old dip misled)

| View | What it shows | CCT-friendly? |
|------|---------------|---------------|
| **Original HERO (R.I.P.)** n≈62k, min20, **no mg10** | Peak ~bin 12, **dip bin 16** | **Looks** like CCT — contaminated |
| **POST-QC hero (mg10 min20)** | Middle rise, **flat elite tail** | Marginal curve — **does not prove or disprove** |
| **OBPM/BPM Track C** | Stronger monotonic rise | Still marginal; not inverted-U rescue |
| **July mg=0 replay** | Elite dip returns | **Cameo / CPR** artifact — not the subtle NCAA signal |

**Verdict:** Do not reopen marginal ventiles hoping for inverted-U. Zoom **conditional** (joint memo §4–5).

---

## 5. Why BDP alone cannot confirm CCT (honest limit)

Marginal histograms answer:

- “What does the league look like?”
- “What do draft-history teams look like relative to the league?”

They **do not** answer:

- “For **player X at z = +1.5**, does draft probability drop when we move them from a Squid window to a Jackal window?”

That needs **conditioning** — hold A_i (or BPM z) near fixed, vary **team context** and **within-roster rank**.

---

## 6. Populations, filters, and scales that **will** illuminate CCT

**COMPASS recommended “zoom ladder”** (each step is one figure family):

### Step A — Stay on hero panel

- **Panel:** mg10 min20 2011–2021, QC dash-names (same as BDP Slide 9/17).
- **Perf:** PPM primary; BPM/OBPM overlay panels for sensitivity (you already built the culture for this).

### Step B — Define within-team rank (the missing axis)

For each player-season `(i, j, t)`:

- **Roster percentile:** rank of Â_i within team-season (0 = bottom, 1 = top).
- **Headroom:** Â_i − max(teammates) or count of teammates with Â_i within ε (e.g. 0.25 z).
- **L_C empirical proxy:** mean σ(γ(Â_k − θ)) on roster (team smooth from deck) — **same for all on team**, but **interacts** with individual A_i through **relative position**.

### Step C — Core CCT plots (proposed)

1. **Matched-z draft rate vs T̂_j**  
   Bin A_i into narrow bands (e.g. 0.1 z). Within each band, plot draft rate vs T̂_j ventiles.  
   **CCT signature:** flat or falling draft rate at high T̂_j **within** high-A_i band.

2. **Draft rate vs roster percentile, faceted by T̂_j quartile**  
   Four small multiples. **CCT signature:** at high T̂_j, only **top percentile** keeps draft mass; at mid T̂_j, **same z** nearer top of window → higher rate.

3. **Peer count above θ at fixed A_i**  
   For each player, N_peers = #{teammates : Â_k > Â_i − δ}. Plot draft rate vs N_peers stratified by T̂_j.  
   This is the empirical face of **L_C / congestion**.

4. **Interval diagram slice (HAND17 mini, hero panel)**  
   Restrict to players with Â_i in top decile **within team**. Color by drafted Y/N.  
   Visual: drafted players as red dots on interval chart — do they cluster on **leading edge** of window?

5. **Explicit Squid/Jackal matched pairs**  
   Match players across team-seasons on |Â_i − Â_j| < ε and similar minutes. Compare draft indicator; regression with **high T̂_j × high A_i** interaction.

6. **Two-way heatmap** (SCOUT add — joint memo §5.2)  
   Draft rate in cells (**Â_i ventile** × **poolq_loo ventile**). Marginal hero curves are **column averages** — look for lower rate in upper-right (high A, high pond) vs upper-middle (high A, medium pond).

7. **L_j^C vs T̂_j** (SCOUT add — joint memo §5.5)  
   Team congestion by T̂_j ventile; model predicts high T̂_j → higher L^C → lower draft odds at given A if λ > 0.

8. **MLE residual bins** (SCOUT add — joint memo §5.6)  
   Observed − predicted draft rate by poolq_loo at fixed A — shows where softmax still misses.

### Step D — +DFT filter role (from BDP orange line)

Use +DFT **not** as “the answer,” but as **zoom onto draft ecosystem**:

- Repeat Step C on +DFT subsample only → signal may ** sharpen** (your sd compression hints at this).
- Compare **width of T̂_j overlap** at fixed A_i between DFT vs non-DFT teams.

### Step E — Scales / binning choices

| Choice | Recommendation |
|--------|----------------|
| **A_i bins** | Narrow (0.1–0.2 z) for matching; wider for display |
| **T̂_j bins** | Ventiles or quartiles; monotonicity check |
| **Minutes** | Keep min20; sensitivity min10 for “star bench” edge cases |
| **Seasons** | 2011–2021 hero; 2015–2019 replay for HAND17 interval comparability |
| **Perf metric** | PPM headline; BPM/OBPM appendix magnification |

---

## 7. Model ↔ empirics handshake (one paragraph for Alex)

*We see low NCAA sorting (H_sort ≈ 0.1) and heavy interval overlap (HAND17). BDP shows draft-ecosystem teams occupy a tighter, higher T̂_j band with similar roster counts — congestion is about **rank inside the window**, not fewer players. The sim says if ranking penalizes viable-peer density (λ > 0), selection curves bend even when the draft rule is fixed. The empirical test is therefore **conditional**: at fixed talent, does draft probability fall as within-team peer count rises and as team T̂_j rises? Hero ventiles alone average that question away.*

*(Longer Alex-ready paragraph in joint memo §8.)*

---

## 8. What we would **not** do next (SCOUT add)

- More ESPN seasons alone — unlikely to move CCT needle (you and Alex agree).
- Another marginal **poolq_loo** ventile rerun hoping for inverted-U — Track C closed that.
- Promoting OBPM/BPM to canonical hero — sensitivity only.
- Confusing **T̂_j** with **poolq_loo** in Squid/Jackal prose.

---

## 9. Who does what (SCOUT add)

| Plot type | Owner |
|-----------|--------|
| BDP Â/T̂/roster ladders (**done**) | COMPASS + SCOUT scripts |
| Matched A × pond draft-rate (§6C #1–2, heatmap) | **SCOUT** → `basic_data_plots/` |
| Interval overlap conditional | **SCOUT** — extend pd17 overlap |
| L_j^C by T̂_j | **SCOUT** — grandchild/pd17 path |
| Slide wording / ladder order | **COMPASS** |
| HAND deck assembly | **Charles** |

---

## 10. Suggested next SCOUT build (when Charles asks)

**One script, one slide pair:**

`pass_a_congestion_conditional.py` (name TBD)

- Input: hero panel mg10 min20  
- Outputs:  
  - `PASS_A_draft_rate_by_ai_band_and_Tj.png`  
  - `PASS_A_draft_rate_by_roster_percentile_and_Tj.png`  
  - JSON with cell counts (guard sparse bins)

**Do not** block on new scrape. **Do** reuse `pass_a_empirical_bundle` panel path.

---

## 9. Bottom line — COMPASS wisdom

1. **BDP deck = success.** You now have a **shared visual language** for populations (FP → hero) and for **draft-ecosystem vs league** (+DFT). Keep it as Act I of the congestion chapter.

2. **Your instinct on BPM vs OBPM sd compression is real.** It is a clue that **comprehensive team-adjusted metrics** feel crowding more than raw PPM. Use as **sensitivity**, not canon.

3. **CCT is not in the marginals.** It lives in **conditional plots** — fixed A_i, vary rank / T̂_j / peer count — plus the **interval geometry** you already drew on HAND17 Slide 5.

4. **The model already gave you the vocabulary:** L_C, λ, θ, score≠select. The empirical analog is **peers above you on the roster**, not “ worse team mean.”

5. **Flat hero elite tail does not mean congestion is dead.** It may mean the hero **bins the wrong way** for this question — averaging Squids and Jackals at the same z.

6. **Next figure is not another histogram.** It is a **matched-z conditional** or **roster-percentile faceted** plot on mg10 min20.

---

**Files for Charles today:**  
`slides/Basics_data_plots_HAND/` (21 slides) · `basic_data_plots/BDP_*.png` + JSON · **memo pair** in this folder (see joint memo §10 table).

**COMPASS status:** BDP chapter **closed** for deck quality. **Open:** conditional congestion figure family (§6C, joint §5.1–5.8) — recommend before more marginal duplicates.

---

## 10. COMPASS addendum — after reading joint SCOUT memo (20260820)

SCOUT’s joint doc same day. COMPASS adds **framing and guardrails** SCOUT stated well; we fold them here so this file stands alone.

### 10.1 Binding doc + MLE numbers (joint §3)

- Environment **B − D** ≠ advancement; **score** (**S_i**) ≠ **select** — [`BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md).  
- Bernoulli MLE (PPM, 2013–2021, γ fixed): **λ̂ ≈ 2.6**, **t̂ ≈ 1.1** — panel behaves as if congestion in the **score** matters after A.  
- **Residual plot idea (joint §5.6):** observed − predicted draft rate by **poolq_loo** at fixed A — shows where softmax misses and where to zoom.

### 10.2 Congestion axis — poolq_loo vs T̂_j (joint §6)

| Axis | Use for CCT |
|------|-------------|
| **poolq_loo** | **Primary** — LOO teammate pond (excludes self) |
| **T̂_j** | **Secondary** — team mean label; mean **includes** player in average (slightly wrong pond for prose) |

Say “teammates around me” in talk; use **poolq_loo** in plots first.

### 10.3 What we will **not** do (joint §7) — COMPASS endorses

- More ESPN seasons alone for CCT.  
- Another marginal poolq_loo ventile hoping for inverted-U (Track C closed).  
- OBPM/BPM as canonical hero.  
- Conflating T̂_j with pond in Squid/Jackal sentences.

### 10.4 Alex paragraph (joint §8)

COMPASS adopts verbatim the joint one-paragraph brief for advisor talk — conditional Squid/Jackal test, not elite-bin dip.

### 10.5 Agreement statement

**No disagreement** between memos on: BDP = population geometry only; CCT needs **matched Â** + **rank/pond**; mg10 min20 primary panel; BPM/OBPM = magnifier; July tail = QC artifact.

**COMPASS sequencing:** Act I BDP **done** → Act II **one** conditional figure family (§6C + joint §5.1–5.3) before MLE/PD14 reorder debates.

---

*Charles — you asked for elementary verbose fellows. Here we are. The pond is real; the fish are the same size; we need to count how many same-size fish are swimming beside each one.*
