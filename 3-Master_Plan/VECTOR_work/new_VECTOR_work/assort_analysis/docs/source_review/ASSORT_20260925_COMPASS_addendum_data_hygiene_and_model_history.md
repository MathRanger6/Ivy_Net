# COMPASS addendum — basketball data hygiene and model history

**Prepared:** September 25, 2026  
**For:** VECTOR / Charles  
**Companion to:** [`ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md`](ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md)  
**In reply to:** [`ASSORT_20260925_questions_for_SCOUT.md`](ASSORT_20260925_questions_for_SCOUT.md)

**Scope:** Planning chronology, campaign framing, and modeling intellectual history. **Does not** replace SCOUT’s pipeline evidence. Read-only; no code execution.

---

## How this addendum relates to SCOUT’s response

SCOUT owns **what the code did**, **saved counts**, and **artifact paths**. COMPASS owns **why work was sequenced**, **how labels (Pass A / B / C) were used**, and **how modeling choices fit the dissertation ladder**.

Use SCOUT for verification. Use this addendum when VECTOR needs **narrative order** and **decision rationale** that live in planning memos rather than in scripts.

---

## Part A — Campaign chronology (why box QC landed when it did)

### A.1 Timeline in plain order

| When | What happened | Why it mattered |
|------|----------------|-----------------|
| **Jul 2026** | Hero exploration on prebuilt / mixed panels; **minimum games = 0** still allowed one-game team-season cameos | Elite-bin inverted-U **tail dip** visible on leave-one-out pool quality axis |
| **Early Aug 2026** | **Paper Directions 20–21:** Levine–Gates assign engine, homophily (ρ) bracket vs sorting index; Gibbs gate cleared | Assign layer credible before defending empirical panel |
| **17 Aug 2026** | **Paper Directions 22 prep:** roster-size diagnostic finds BYU-style junk rows; **box quality control** coded at panel build | Problem traced to **Stage 1 box extract**, not draft matching |
| **17 Aug 2026 (day)** | Rollout: dash-name filter + **minimum team-season games = 5** (retain **> 5** → **≥ 6** captured games) | First cut on fragmentary opponents |
| **17 Aug 2026 (same day, evening)** | Policy tightened to **minimum team-season games = 10** (retain **> 10** → **≥ 11**); impact table showed **zero** additional drafted hero rows lost vs six-game rule | Low-cost robustness after mg5 left residual partial seasons |
| **18–19 Aug 2026** | Pass A sensitivity pair (July replay **mg0** vs POST-QC **mg10**); SCOUT and COMPASS Q&A rounds B1–B6 | Quantified **cut player-row** contamination of elite ventile |
| **18 Aug 2026** | **Paper Directions 23:** panel story defended; production lock **drop sub-20 minutes**; zero-points-per-minute = **contrast only** | Separated estimand from sensitivity |
| **Sep 2026** | **Reigning hero** lock (2009–2021, last player-season, equal-width 16 bins) | Current reference figure — **different spec** from August sensitivity pair |

**Primary planning sources:** [`3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md`](../../../../../../3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md); [`3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md); [`transcripts/PD23_notes.md`](../../../../../../transcripts/PD23_notes.md).

### A.2 Why six games became eleven (COMPASS read on SCOUT’s gap)

SCOUT correctly marks **no standalone Charles memo** for the same-day six → eleven step. **[Interpretation — planning, not a quoted decision]:**

1. **Six games** was the minimum fix for the **one-game opponent** pathology Charles discovered.
2. **Eleven games** was a **same-day tighten** once mg5 counts showed **23** additional marginal team-seasons removable **with no drafted-player loss** on the hero panel.
3. The choice was **empirical robustness**, not a formal “inspect curve at eleven first” sensitivity sweep documented in git.

If VECTOR needs a **primary quote**, search Aug 17 SpecStory / oral approval in Charles’s notes — not COMPASS prose.

### A.3 What “inverted-U survived cleaning” meant in August

Three statements coexist; they are **not** contradictory if you separate **local tail** from **global curvature** and **figure spec**:

| Claim | Meaning | Figure family |
|-------|---------|---------------|
| “Survived” (Paper Directions 23) | Middle **rise** + defensible panel; main line intact for the book | Narrative / Alex briefing |
| POST-QC sensitivity (Aug 19) | **No elite right-tail dip** on leave-one-out axis; flat bins 12–16 | `PASS_A_sensitivity_loo_mg10_*` |
| Reigning hero (Sep) | Positive quadratic coefficient; **“tail drop” label ≠ concavity** | `HERO_q16_allt_min20_mg10_9_21_last_ps` |

**COMPASS framing for VECTOR:** Cleaning **removed an artifact dip** driven by cut player-rows in bin 16 under **mg0**. It did **not** erase the broader “context matters” middle rise that motivates the mechanism work.

---

## Part B — Commentary on SCOUT’s flagged gaps

| SCOUT gap | COMPASS can add | Still needs SCOUT / Charles |
|-----------|-----------------|------------------------------|
| **No memo for mg5 → mg10** | Same-day policy table + rollout narrative (Part A) | Aug 17 chat transcript if VECTOR wants direct quote |
| **Missing Pass A PNGs in git** | Regen was **planned** in rollout memo §12; HAND decks = Charles Change Picture | Recover PNGs from local/Dropbox export folders |
| **Six two-player 2015 teams** | Pre–box-QC panel era (Aug 11 Grandchild meta) — **not** comparable to post-QC counts without relabeling | Box-level audit per team identifier |
| **Quantitative T̂_j inflation audit** | Mechanism aligns with Charles’s concern (Part C.1); LOO ventile CPR math is the **documented** counterpart | Join game counts to interval-overlap exports |
| **HAND slide re-picture log** | Phase A/B regen order in Aug 17 rollout memo | Charles audit of which slide masters were updated |
| **Otter drop vs zero garble** | PD23 notes + post-call execution record support **drop = production** | Transcript alone is ambiguous |

---

## Part C — Modeling intellectual history (expanded §8)

This section answers VECTOR’s §8 with **reasons and limitations**, not only final settings. The new assortativity investigation **need not copy** these choices; it **should not misrepresent** them.

### C.1 Empirical team mean T̂_j vs leave-one-out pool quality (horizontal axis)

**Historical fact:** Early generative work (538D soft assignment) could produce an inverted-U when the horizontal axis was **team mean ability** (including self). The **empirical Hero** and August-locked work use **leave-one-out mean teammate performance** (`poolq_loo`) so the focal player does not grade himself.

**Why the axis change mattered:** Team mean and leave-one-out answer different questions. Congestion in the **score** uses **team-level** peer pressure (L_C); the **Hero plot** bins on **leave-one-out environment** for comparability across real and simulated rosters.

**Limitation:** Changing the axis is **not** a relabel — curve shape can change materially. See [`3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md`](../../../../../../3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md) §2.

**Charles’s T̂_j concern (fragmentary teams):** On basic data plots, **T̂_j** is the mean within-season points-per-minute z-score on the retained roster. Fragmentary capture can **inflate** that mean for weak schools because only a few rotation players survive the twenty-minute floor on a partial schedule. Hero work **standardized on leave-one-out**, but **T̂_j** diagnostics remain relevant for assign / interval-overlap figures.

### C.2 Soft ordered assignment vs Levine–Gates (Grandchild) assignment

| Era | Mechanism | Centroids | Status |
|-----|-----------|-----------|--------|
| **539 / early 540** | Soft match to **exogenous** team targets T_j* | Fixed or drawn targets | Teaching / gallery; not production assign |
| **Aug 2026 onward** | **Levine–Gates:** sequential seating, **endogenous** centroids updating after each seat | Start at league mean μ₀; update from members | Production assign for ρ calibration |

**Why we moved:** Exogenous targets **pre-load** between-team heterogeneity. The Grandchild question was whether **homophily + capacity + path dependence** could **generate** sorting from identical empty teams — closer to “peers end up together” without baking in empirical team means.

**Desk reference:** [`3-Master_Plan/re_entry/LG_model_desk_reference.md`](../../../../../../3-Master_Plan/re_entry/LG_model_desk_reference.md).

### C.3 Fixed roster size fifteen vs observed NCAA capacities

Early ρ sweeps used **C = 15** for every team (**J = N / 15**). Production comparability runs prefer **empirical roster-size multiset** per season (real team capacities summing to N).

**Why both exist:** Fixed fifteen is clean for mechanism validation; empirical caps match listing structure for apples-to-apples Hero / assign calibration.

**Limitation:** Real panel teams average ~10 rotation players after filters; synthetic fifteen-person leagues **repack** the same abilities — team-season counts differ even when congestion distributions look similar.

### C.4 Noise layers (assignment, score, selection)

Historical 538D playground separated:

- **Assignment noise** — stochastic seating (Levine–Gates is inherently stochastic via random order and team draw).
- **Score noise** — perturbations to ranking input (mostly **not** used in August hero lock).
- **Selection noise** — stochastic draft draw from scores (Paper Directions 20 Gibbs gate; **deterministic top-K** is today’s v1).

**Limitation:** Conflating these layers caused early confusion between **environment**, **score**, and **select**. Binding rule: [`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../../../../../3-Master_Plan/BINDING_Selection_is_its_own_step.md).

### C.5 Congestion scaling, negative scores, selection temperature

**Score (version 1):** S_i = Â_i − λ L_C, with team congestion L_C built from soft peer viability σ(γ(Â_k − θ)).

**Historical knobs** (not all active in August hero lock): automatic scaling so λ·L_C matches ability units; treatment of negative scores; selection temperature in stochastic select.

**Why they existed:** Early cells explored **identifiability** and **gallery behavior** before locking Paper Directions 16 team L_C.

**Limitation for VECTOR:** New deterministic selection design should document which of these are **intentionally retired**, not accidentally “current.”

### C.6 Pass A / Pass B / Pass C labels (campaign map)

Names shifted over months; use **artifact folder** as ground truth when labels conflict.

| Label | What it meant (Aug 2026 lock) | Typical artifacts |
|-------|------------------------------|-------------------|
| **Pass A** | **Empirical** hero + knockouts (λ in score, fixed select); sensitivity grids | `HEROs_and_PASSes/pass_a/` |
| **Pass B** | Often **generative** λ / congestion in sim (context-dependent in older docs) | `pass_b/` (sparse) |
| **Pass C** | **ρ** / assign ablation; conditional ability campaign (CCT) | `pass_c_rho/`, CCT review memo |

**COMPASS caution:** Read [`3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md`](../../../../../../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md) before trusting an old slide label. **540 README** maps Pass B to ρ in shorthand — doc 04 is the full sentence version.

### C.7 Artificial playing-time allocation — rejected

**Decision:** Do **not** simulate minutes or assign zero points-per-minute as **production** policy. Minutes are **observed**; low-minute rows are **dropped** (twenty-minute floor) for the main estimand.

**Why:** Simulating minutes would conflate **assign** (who is on the roster) with **playing-time allocation** (coaching / opportunity), overfitting listing quirks.

**Contrast run only:** `--ppm-zero-below-minutes 20` keeps rows but zeros raw points-per-minute below twenty — **wrong estimand** for hero, useful for ρ/H_sort slides 15–16.

Sources: [`sports/documents/Pertinent_Thoughts_Scout.md`](../../../../../../sports/documents/Pertinent_Thoughts_Scout.md); Paper Directions 23 notes.

### C.8 Points per minute as environment-reflecting measure

**Lock:** Within-season **points-per-minute z-score** is the primary ability input for hero, basic data plots, and Levine–Gates assign calibration.

**Why not switch casually:** September 2026 performance-metric batch (box plus / advanced metrics) **failed to dethrone** points-per-minute on the **leave-one-out shape gate** for the hero campaign.

**Limitation:** Points per minute **mixes** individual production with team context (pace, role). It is a **pragmatic** measure, not a claim that scoring rate is exogenous to environment.

---

## Part D — Correction on 65.80% vs 66.8%

**Canonical:** **65.80%** = 2,557 / 3,886 cut player-row share in bin 16 under mg0 tagging. **[Saved result]** SCOUT Q&A B6 table.

**66.8%** appears in **COMPASS Round 2 prose** (“Note to Charles”) as informal rounding / slip — **not** a second audited ratio. VECTOR and manuscripts should use **65.80%** with the B6 numerator and denominator.

---

## Part E — Recommended reading (COMPASS lane, after SCOUT list)

Read SCOUT §9.4 first. Then, if VECTOR wants **planning + model arc**:

1. [`PD20_22_campaign_big_picture.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md) — wavetops from Army hero to POST-QC panel  
2. [`LG_model_desk_reference.md`](../../../../../../3-Master_Plan/re_entry/LG_model_desk_reference.md) — assign → score → select formulas  
3. [`04_Pass_A_and_Pass_B_in_Plain_English.md`](../../../../../../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md) — empirical vs sim vocabulary  
4. [`COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md`](../../../../../../3-Master_Plan/COMPASS_work/COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md) — why Grandchild was coded  
5. [`20260821_SCOUT_CCT_campaign_review.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/20260821_SCOUT_CCT_campaign_review.md) — do not treat restoring elite dip as success criterion  

---

## Part F — Implications for VECTOR’s 2015 population freeze

**Historical outputs are evidence, not inputs.** When freezing a 2015 population with observed capacities:

- Explicitly choose **minimum team-season games** (eleven captured games = config value ten), **minimum minutes** (drop twenty vs zero-points-per-minute contrast), and **focal row rule** (all player-seasons vs last player-season).
- Do **not** assume the September reigning hero spec equals the August sensitivity pair.
- Treat **mg0 July replay** curves as **contamination illustration**, not the estimand to recover.

COMPASS does **not** authorize execution or population freeze here — only documentary clarity.

---

*COMPASS addendum — read-only companion to SCOUT response. Does not modify question or SCOUT answer files.*
