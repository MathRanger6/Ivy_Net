# Alex Gates — inform status outline (next meeting)

**Date:** 2026-07-16  
**From:** Charles Levine (COMPASS-assisted skeleton — **you** add detail iteratively)  
**Purpose:** **Inform only** — map the full path in minimal bullets. **Not** the decision questionnaire.  
**Questions / tabled items:** [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md)  
**Deep plan (if he asks):** [`03_Where_we_are_now.md`](03_Where_we_are_now.md) · [`04_Project_story_plain_English.md`](04_Project_story_plain_English.md)

---

## 1. One sentence

Cross-domain paper: **inverted-U on leave-one-out peer-pool quality** (Army → basketball → tenure preliminary) → **minimal generative mechanism** (honest claims) → **two predictions** → **Wang-style manuscript** — target **Summer–Fall 2026**.

---

## 2. Where we are (snapshot)

| Leg | Status | One line |
|-----|--------|----------|
| **Army** | ✅ Anchor | CIF + Cox stack mature; AWS is canonical run environment |
| **Basketball** | ✅ Replication | Inverted-U on `poolq_loo`; D10 export bundle on disk |
| **Tenure** | ⚠️ Preliminary | Stage 9 binned plot OK for draft; 796 persons / 52 depts inference-ready |
| **Generative model** | ⚠️ Path II | Talent-only fails; congestion-in-score POC on **pool mean** (axis mismatch stated honestly) |
| **Manuscript** | 🔲 Next | Staging prose written; **inking Word** is current focus |

---

## 3. The path (whole arc — briefing outline)

**How to read:** Top-to-bottom = time order. **Done** = already in hand. **Now** = current focus. **Parallel** = runs alongside draft; does not block first Word pass. **Before submit** = needs to land before we send the paper out. **Later** = explicitly parked unless you or Alex elevate.

---

### Phase A — Empirical pattern across three settings **(DONE)**

**What we proved descriptively:** In each domain, advancement (promotion, draft, tenure) rises with peer-pool quality through the middle range, then dips in the most elite pools — an **inverted-U**, not “better peers always help.”

| Setting | What we measured | Status |
|---------|------------------|--------|
| **Army** | Leave-one-out senior-rater pool quality vs promotion (competing risks with attrition) | **Established** — strongest anchor |
| **Basketball** | Leave-one-out teammate pool quality (`poolq_loo`) vs NBA draft | **Established** — clean replication |
| **Tenure** | Leave-one-out department peer quality vs tenure event | **Preliminary** — binned plot only; smaller inference sample (796 people / 52 departments) |

**One line for Alex:** The **cross-domain stylized fact** is real in Army and basketball; tenure is an honest third panel, not a fourth anchor yet.

---

### Phase B — Close the minimal model **(NOW)**

**Goal:** Freeze enough mechanism language that the manuscript can describe *what the model is*, *what the data columns mean*, and *what we are **not** claiming* — without waiting for a perfect simulation.

| Step | Plain English | Status |
|------|---------------|--------|
| **B1. Score equation** | Advancement score = ability minus congestion penalty (`S = A − λ·congestion`). This is the **constraint-leg** proof-of-concept Alex asked for — who gets selected when pools are crowded. | **Locked** (Tier 1) |
| **B2. Talent-only null** | Simulation with ability only (no congestion) **fails** to reproduce the inverted-U — congestion term is necessary for the generative story. | **Done** (`538D` CELL 10) |
| **B3. Congestion proof-of-concept** | Simulation **with** congestion bends curves on **whole-roster pool average** — not yet point-for-point on the same axis as empirical `poolq_loo`. | **Done** — **axis mismatch stated honestly** |
| **B4. Axis table** | Written table: each model quantity → data column → which axis the plot uses → allowed claim for version 1. Stops prose from over-claiming generative replication. | **On disk** (D10 export bundle) |
| **B5. Claim guardrails** | Master list: every manuscript claim tagged Supported / Preliminary / Unsupported / Defer (`#07`). | **Written** — VECTOR and Charles check prose against it |

**One line for Alex:** Minimal model = **honest Path II** — generative POC on pool-mean axis + explicit limitations; **not** bin-for-bin match to empirical leave-one-out quality before draft.

---

### Phase C — Draft the manuscript **(NOW)**

**Structure (Wang-style):** short opening frame (§0) → empirical phenomenon (§1) → theory (§2–§3) → minimal mechanism (§5) → predictions (§7). **Not** a front-loaded lit review; fuller literature map in Discussion (`#12` §5.2).

| Manuscript section (Word outline) | What goes there | Ink status |
|-----------------------------------|-----------------|------------|
| **§0 Opening framing** | Problem, gap, contribution preview, roadmap (½–1 page) | Staging §1 ready — ink on **polish pass** after §5→§1→§4 |
| **§1 Empirical observation** | Three-setting triad + figures (Army CIF, basketball ventile, tenure preliminary) | Staging prose ready; Army figures pending AWS canon |
| **§2–3 Theory** | Why finite distinction / local comparison pools matter; **L_net = B − D** framing | Staging + nesting note ready |
| **§4 Tenure setting** | Preliminary third leg + limitations | Staging ready; Cell 9 plot OK for draft |
| **§5 Minimal generative model** | Talent-only fails vs congestion-in-score; axis table; limitation paragraph | Staging + D10 figures ready |
| **§7 Predictions** | Two primary prediction **directions** (see below) | Staging ready; one basketball figure on disk |

**Ink order (your current plan):** write **§5** (generative) first → then **§1** (empirical triad) → then **§4** (tenure) → then **§0** (opening frame, ½–1 page polish) — so mechanism language is settled before empirical claims reference it.

**Lit review (v1):** §0 + §2–§3 + Discussion — **not** a separate chapter before §1.

**Two primary predictions (locked for version 1):**

1. **Near-threshold heterogeneity** — the elite-pool dip should hit hardest for **borderline** performers (good but not stars), not the very best or the clearly below-average. One exploratory basketball figure exists; not a full tri-domain proof yet.
2. **Peak shift with global capacity (K)** — when an organization has more scarce advancement slots (bigger boards, more picks, more tenure lines), the **top** of the inverted-U should move. **Conceptual / prose hook** for now — not a finished cross-domain figure.

**One line for Alex:** **Draft is unblocked** — empirical triad is the spine; generative is a disciplined supplement, not a gate.

---

### Phase D — Parallel work while drafting **(does not block Word)**

| Workstream | What it is | When it matters |
|------------|------------|-----------------|
| **Tenure Cox models** (`540` Cell 12) | Inferential hazard models beyond the descriptive binned plot — hazard-ratio tables for tenure curvature | **Before submission**, not before first draft. Cell 9 plot is legitimate for draft prose. |
| **Army figure canon** | You name canonical cell, run profile, and filenames after **AWS sync** (Cursor repo is a digital twin) | Before Alex-facing Army figure is final |
| **Estimand sentences** | Three to five approved sentences: Army **descriptive** binned cumulative-incidence bars (Cell 11) vs **inferential** Cox models (Cell 12) — not the same object | Alex sign-off before final Army methods wording |
| **Manuscript inking** | Paste staging prose into `Manuscript_working_outline_v1.docx` per ink map | **Now** |

---

### Phase E — Advisor read and submission **(TARGET: Summer–Fall 2026)**

1. Charles completes first full Word draft (empirical + generative + predictions + limitations).
2. Alex read — revise **claim language** against guardrails, not reopen Path II unless he asks.
3. Close soft gates: tenure Cox table, Army estimand wording, pool-size audit (pre-publication).
4. Submit interdisciplinary science-of-science target (venue TBD).

**Opportunity-cost rule:** If a task does not improve draft quality, claim honesty, or submission readiness → it stays in the parked queue.

---

### Phase F — Parked queue **(LATER — mention only if he asks)**

| Item | Plain English |
|------|---------------|
| **525 / UIC deep dives** | Extra Army work on prestigious units and senior-rater consistency — mechanism meat if the paper needs it |
| **Network extensions** | Talent center-of-gravity, talent paradox, exposure networks — dissertation / manuscript §8 future work |
| **Full leave-one-out generative match** | Make simulation reproduce empirical `poolq_loo` curve point-for-point — north-star, parallel to draft |
| **Separate B and D estimation (PD12 P1)** | Identify benefit and congestion legs parametrically in all three domains — beyond version 1 |
| **Fourth domain (PD12 P4)** | Add another empirical setting to stress-test generality |

Elevate any parked item only if **Charles or Alex** says so.

---

## 4. What to tell him (talk track — expand as needed)

- **Bottleneck shifted:** discovery → **convergence** (model language + manuscript).
- **Paper-first:** empirical triad is the contribution; generative is **minimal POC**, not full LOO replication.
- **Tenure:** third leg is **preliminary** — honest limitations, not equal maturity to Army/MBB.
- **Not blocked on:** generative bin-for-bin LOO match, Fine–Gray, 525/UIC, network §, tenure Cox for *draft*.
- **Phase A done (June):** Tier 1 locks filed; D10 bundle; faculty inference export; staging prose.

---

## 5. Parked (mention only if he asks — not seeking decisions today)

| Item | One line |
|------|----------|
| 525 / UIC | Prestige-org Army depth — revisit if manuscript needs more mechanism meat |
| Networks | Talent COG, talent paradox — dissertation / later § |
| LOO generative match | North-star parallel; Path II accepts axis mismatch for v1 |
| Pool-size audit | Pre-publication, not pre-draft |

---

## 6. If he wants more detail — point, don’t recite

| Topic | Doc |
|-------|-----|
| Full status + dependencies | `#03` |
| Plain-English story | `#04` |
| Equations / variables | `#21` |
| What we can claim | `#07` |
| Alex score vs. **L_net** (say aloud) | **Appendix** (this doc) |
| TB-stratify, estimand, Fine–Gray | Talking points doc |

---

## 7. Meeting notes (Charles — add after)

<!-- Iterative: decisions, redirects, items elevated from parked queue -->

- 
- 
- 

---

## Appendix — Alex score vs. L_net = B − D (say aloud)

**Purpose:** Practice language for “two equations, one project — not the same object.”  
**Canonical nesting:** [`5-Manuscript/05_Model_Nesting_Note_v1.md`](../../../5-Manuscript/05_Model_Nesting_Note_v1.md) · formula decoder [`21_Formulas_and_variables.md`](21_Formulas_and_variables.md) §1–§2.

---

### A.1 The two equations (say them first)

**Your framing (net environment):**


```text
L_net = B(·) - D(·)
```


**Alex’s framing (selection score):**


```text
S_i = A_i - λ L_C,LOO,i
```


Same project. **Not the same object.**

---

### A.2 One sentence each

| Equation | Say this |
|----------|----------|
| **L_net** | “How does the **local peer environment** net out for advancement — upside from strong peers **minus** downside from crowding them out?” |
| **S_i** | “How does the **selector rank** people — own ability **minus** a penalty for viable-peer congestion?” |

---

### A.3 The significant differences (what to stress aloud)

#### 1. Reduced form vs. selection rule

| | **L_net = B − D** | **S_i = A_i − λ·L_C** |
|--|-------------------------------|----------------------------------|
| **Asks** | Why does peer context help *and* hurt? | Who gets picked when pools are crowded? |
| **Level** | Environment → advancement propensity | Individual → ranking score → selection |
| **Role in paper** | Conceptual spine + empirical story | Minimal **generative** proof-of-concept |

**Say:** “Mine is the **why** — benefit and constraint in the environment. Alex’s is the **who gets selected** rule that puts congestion into the score.”

#### 2. Two legs vs. one leg in the equation

**L_net** has **both**:

- **B** — visibility, norms, minutes, development upside from elite peers  
- **D** — congestion, substitutability, finite slots  

**Alex’s score** has **only the D-leg in the formula** (plus own ability):

- Congestion **L_C** is subtracted from **A_i**  
- **B** is not a term in **S_i** — no “minutes bonus” or “development benefit” in the score equation  

**Say:** “Alex’s equation is **not** **B − D**. It’s **ability minus congestion** — the constraint leg **entering selection**. The benefit leg lives in my broader frame and in **separate empirical columns** (`poolq_loo` vs `crowding_smooth`), not inside his score.”

**Nesting line:** Alex score = **D entering the selection rule**; not the full **L_net** and not a second model.

#### 3. Own ability: outside vs. inside

- In **L_net**, own ability **A_i** is **outside** the decomposition — environment is about **peers**, not you.  
- In **S_i**, own ability is **inside** the score — ranking is explicitly **you vs. congestion**.

**Say:** “**L_net** is about **the pool around you**. **S_i** is about **how evaluators score you** given that pool.”

#### 4. What you measure empirically vs. what the sim uses

| Construct | Empirical world | Alex generative world |
|-----------|-----------------|------------------------|
| Pool “quality” | `poolq_loo` (LOO teammate quality) — **mixes B and D** | Often **pool mean** on roster; LOO quality is a different knob |
| Congestion | `crowding_smooth` — **D proxy** | \(L_{C,\text{LOO}}\) — viable-peer density, LOO |
| Outcome curve | Inverted-U on **LOO quality** | Inverted-U on **pool mean** when **λ > 0** |

**Say:** “Empirically we plot advancement vs **leave-one-out pool quality**. The generative sim shows congestion **in the score** can bend curves on **whole-roster pool mean**. Same story at the mechanism level, **different conditioning object** — and we say that honestly.”

#### 5. What each equation is *for* in v1

- **L_net:** Explains the **inverted-U** (both legs), guides **Rung 2.5** (quality vs. congestion columns), frames **predictions**. **Not separately estimated** as **B(Q)−D(Q)** in v1.  
- **S_i:** Shows **talent-only fails** (**λ = 0**) and **congestion-in-score bends curves** — minimal Path II POC. **Not** bin-for-bin replication of empirical `poolq_loo`.

**Say:** “I’m not claiming we’ve estimated full **B** and **D** as functions of pool quality. Alex’s score isn’t claiming to be the whole **L_net** either. It’s the **minimal generative piece** that makes congestion matter for **who gets selected**.”

---

### A.4 Thirty-second script (practice this)

> “We use **one ontology, two readouts**.  
> **L_net = B − D** is my reduced form: strong peers can **help** through development and visibility and **hurt** through congestion and substitutability — that’s the inverted-U story.  
> **Alex’s score** is narrower: **ability minus viable-peer congestion** in the **selection rule**. That operationalizes the **constraint leg** — who stands out when everyone around you is also viable — not the full benefit-minus-constraint decomposition.  
> Empirically we see the curve on **leave-one-out pool quality**; the simulation shows congestion in the score can produce non-monotone curves on a **different axis**, with the limitation stated explicitly. Same model family, different rung.”

---

### A.5 What **not** to say (Alex will push back)

| Avoid | Say instead |
|-------|-------------|
| “Alex’s equation **is** my model.” | “Alex’s score **nests inside** my frame as the D-leg in selection.” |
| “We estimated **B − D**.” | “We **decompose conceptually**; v1 has quality vs. congestion **columns**, not full **B(Q)−D(Q)**.” |
| “The sim reproduces `poolq_loo`.” | “The sim shows congestion **in the score** matters; empirical U is on **LOO quality**.” |
| “S_i includes development benefits.” | “B shows up in theory and in proxies like minutes; not in S_i.” |

---

### A.6 If he asks: “So are they the same or different?”

**Short answer:**

> “**Same project, different job.**  
> **L_net** is the **environment story** — why elite pools can help on average but hurt at the top.  
> **S_i** is the **selection story** — how congestion enters **ranking** when slots are scarce.  
> The score is the **minimal generative implementation** of the constraint side, sitting under the broader **B − D** frame — not a competing model.”

**Path II in one breath:** not two models fighting — **one ladder** (phenomenon → minimal score POC → quality-vs-congestion measurements → predictions).

---

### A.7 Quick reference — S vs L vs L_net (not the same symbol)

| Symbol | Level | Plain English | In data / code |
|--------|-------|---------------|----------------|
| **S_i** | **Individual** | Ranking score: ability minus congestion penalty | **Latent** in generative sim (`538D` CELL 10); not observed in Army/MBB/tenure panels |
| L_C / λ·L_C | **Individual-in-pool** | Congestion channel — **D leg inside S** | `crowding_smooth` (empirical D proxy) |
| `poolq_loo` / L_Q | **Individual-in-pool** | LOO **teammate quality** — **mixes B and D** | Empirical **x-axis** (Rung 1); often **decreasing** on sim Plot B when `SHOW_PLOT_B_TEAM_MEAN=False` |
| **Pool mean / `team_mean`** | **Pool** | Whole-roster average ability | Generative Plot B **x-axis** when `SHOW_PLOT_B_TEAM_MEAN=True` (539-style) |
| **L_net = B − D** | **Theory** | Why environment helps **and** hurts | Conceptual spine — **not** a column you regress directly in v1 |

**Mnemonic:** **S = who** (rank). **L = where** (pool context on the plot). **L_net** = why (help minus hurt).

**Critical:** **`poolq_loo` is not ≈ λ·**L_C**.** Congestion is one ingredient in selection; pool quality is a **mixed** environment readout.

---

### A.8 Bridging the two plots (same Y, different X — how the formulas connect)

**Your question:** Alex side feels like score → draft; your side is pool quality → draft. How do we link them?

#### What Alex's equation is for — simulation vs. explanation (read this twice)

**Your insight is correct.** Alex's score is primarily a **simulation rule**, not a claim that this one equation **fully explains** your empirical inverted-U on `poolq_loo`.

| Layer | Object | Job in v1 | What we claim |
|-------|--------|-----------|---------------|
| **Empirical (Rung 1)** | Inverted-U on **`poolq_loo`** | **The phenomenon** — established Army + MBB; preliminary tenure | Pattern is **real** and **replicated** (honest tenure caveat) |
| **Theory (spine)** | **`L_net = B − D`** | **Why** help and hurt can coexist in the same peer environment | Conceptual decomposition — **not** separately estimated as B(Q)−D(Q) in v1 |
| **Generative (Rung 2)** | **`S = A − λ·L_C`** → top K | **Minimal POC engine** — run a disciplined simulation | Congestion **in the score** matters; **talent-only fails** (λ = 0) |

**What the sim proves (and does not):**

| Alex sim **does** | Alex sim **does not** |
|-------------------|----------------------|
| Show that **ability-only selection** cannot produce the generative story you need | Claim to **reproduce** your empirical curve on **`poolq_loo`** bin-for-bin |
| Show that adding **congestion to the score** can **bend** aggregate selection curves (on **pool mean** in v1 POC) | Replace **`L_net`** as the explanation for why elite pools help on average but hurt at the top |
| Operationalize the **D-leg inside selection** — who stands out when peers are viable substitutes | Put the **B-leg** (development, visibility, minutes) **inside** the score equation |
| Earn its place as a **Wang-style minimal mechanism** supplement | Serve as the **only** model of the empirical inverted-U |

**One sentence:** Alex's equation **runs** the generative world; **`L_net`** **frames** the empirical world. The sim asks: *"Is congestion in selection plausibly necessary?"* — not *"Does this score equal your observed U on LOO quality?"*

**Path II honesty (say aloud):** "We do **not** claim the simulation **is** the inverted-U. We claim the simulation shows a **minimal ingredient** — congestion in ranking — without which the generative story fails, while the **empirical** inverted-U lives on a **different conditioning axis** (`poolq_loo` vs pool mean), stated explicitly."

---

Both plots share one **Y**:

| | **Y-axis** |
|--|------------|
| **Empirical (you)** | P(drafted) or mean draft rate in bin |
| **Generative (Alex POC)** | P(selected) or mean selection rate in bin |

Same object: **advancement probability**.

#### Different conditioning (X) — and a common confusion

| Plot | **Typical X-axis** | What X means |
|------|-------------------|--------------|
| **Your empirical readout** | **`poolq_loo`** (LOO pool quality) | Observable local environment — **B and D still bundled** |
| **Alex generative readout (Plot B)** | **`team_mean`** (pool mean) — Path II default | Pool-level ability after soft assignment; **not** individual **S_i** on the axis |
| **Alex (alternate Plot B)** | `poolq_loo` / L_Q | LOO quality axis — closer to yours, but sim often **does not** reproduce empirical U with same knobs |

**Important correction:** The main generative **figure** is usually **not** “score vs draft probability.” **S_i** works **inside** the sim (rank everyone, take top **K**). The **published** generative plot is **“selection rate vs pool feature”** — same *kind* of figure as yours (environment on X, outcome on Y), but a **different pool statistic** on X (pool mean vs LOO quality).

At the **individual** level (behind the plot):

```text
Higher S_i  →  higher chance i is in top-K  →  higher P(Y_i = 1)
```

At the **aggregated** level (what you actually draw):

```text
Bin by pool environment L  →  plot mean P(Y) in each bin
```

#### The bridge formula (conceptual)

Think in two steps:

**Step 1 — Micro (Alex selection rule):**


```text
S_i = A_i - λ·L_C,i  =>  Y_i = 1 if S_i in top K
```


**Step 2 — Macro (your empirical stylized fact):**


```text
E[Y | L_Q] = mean draft rate in pools with LOO quality L_Q
```


**Link:**


```text
E[Y | L_Q] ≈ E[1{S in top K} | L_Q]
```


The **left** is your curve (phenomenon). The **right** is what the sim **aggregates** after running the score rule inside each pool. **L_net = B − D** explains **why** the left-hand curve can rise then fall: mid-quality pools net-help; top pools net-hurt once **D** dominates **B**. **λ·L_C** in **S** is only the **congestion channel** in the ranking step — not the full mixed **L** on your x-axis.

#### Side-by-side (print this)

| | **Empirical (Rung 1)** | **Generative (Rung 2)** | **Theory (spine)** |
|--|------------------------|-------------------------|-------------------|
| **Question** | How does draft rate vary with **peer pool quality**? | Can **congestion in the score** bend selection curves? | Why help **and** hurt? |
| **X** | `poolq_loo` | `team_mean` (v1 POC axis) | — |
| **Y** | P(drafted) | P(selected) | — |
| **Mechanism in prose** | **L_net(L_Q) = B − D** | **S = A − λ·L_C** → top **K** | B leg + D leg |
| **What we claim** | Inverted-U **replicated** (Army, MBB) | Congestion **matters**; talent-only fails | Decomposition + limitations |

#### One paragraph to say aloud (plot bridge)

> "Both figures plot **advancement probability on Y**. Mine puts **leave-one-out pool quality** on X — that's the **empirical inverted-U** we're trying to explain. Alex's score doesn't go on the x-axis. It **runs inside** the simulation: rank everyone with **S**, take top K, then plot **selection rate against pool mean**. So at the micro level **S** governs who wins slots; at the macro level **L** on my x-axis is the pool environment I condition on.
>
> Here's the key distinction: **`L_net = B − D`** is my **why** — benefit and constraint in the environment. **Alex's score** is a **minimal simulation rule** — ability minus congestion in **ranking**. It shows congestion **matters** for selection (talent-only fails). It does **not** claim to be the full explanation of my empirical U on LOO quality, and it doesn't put the B-leg inside the score. The sim is a **proof-of-concept engine**; the inverted-U on `poolq_loo` is the **phenomenon**; **`L_net`** is the **conceptual bridge** between them."

#### What would make them line up more (deferred — say honestly)

Full alignment would require the sim to reproduce **`poolq_loo`** bin-for-bin (LOO generative match — **parked**). v1 instead states the **axis mismatch** explicitly: same mechanism family, **different conditioning object** on X.

---

### A.9 Thought experiment — same axis (`poolq_loo`), both show inverted-U

**Bracket axis mismatch for a minute.** Suppose Army is re-run on LOO pool quality and the inverted-U holds. Suppose the generative sim is also read on **`poolq_loo`** (or LOO-quality bins) and — with congestion in the score — also bends down at the top. **How do we explain that?**

#### Step 0 — What you're looking at (same picture twice)

Both sides plot the **same kind of object**:

```text
X = LOO pool quality (poolq_loo)
Y = P(advance) or mean advancement rate in bin
Shape = rise through mid tiers, fall in elite tier
```

Empirical = **observed** officers / players / faculty. Generative = **simulated** agents after running the score rule. Same axes, same qualitative shape.

#### Step 1 — What the empirical curve is saying

**Plain English:** As the quality of your **local peer pool** (excluding yourself) goes up, advancement first goes up, then goes down.

**What `poolq_loo` captures:** A **mixed** readout of the peer environment — better teammates/colleagues on average, but also denser clusters of strong substitutes. You see the **net** curve; you do not yet see B and D separately on that axis.

**`L_net = B − D` reading of the shape:**

| Region of X | Story (conceptual) |
|-------------|-------------------|
| **Low → mid** pool quality | Net environment **helps** — visibility, norms, development upside from stronger peers (**B** dominates net) |
| **Mid → elite** pool quality | Net environment **hurts at the margin** — too many similarly strong, substitutable peers competing for scarce slots (**D** dominates net) |

The inverted-U is the **signature** that both forces exist in the same local comparison pool.

#### Step 2 — What Alex's score does inside the aligned sim

**Micro rule (unchanged):**

```text
S_i = A_i − λ·L_C,i     (ability minus viable-peer congestion)
Rank by S_i → top K get Y_i = 1
```

**Why congestion alone can bend the curve on poolq_loo:**

- In **higher** LOO-quality pools, more agents are **viable substitutes** (high A, above threshold).
- Congestion **L_C** is high → **S** is compressed for many people — especially **near-threshold** types who are good but not dominant.
- Even with strong own ability, harder to land in top **K** when everyone around you is also viable.
- **Aggregate** selection rate in the top pool-quality bins can **fall** even though the pool is "better."

**Talent-only null (λ = 0):** Score ≈ ability only → selection tracks talent → curve tends **monotone** (better pool → more high-A people → no elite-tier dip). **Fails** to match inverted-U. That is the generative falsification.

**With λ > 0:** Congestion enters ranking → non-monotone **selection vs pool quality** becomes **plausible on the same X** as the data.

#### Step 3 — How sim and data connect when axes match

| Layer | Question | Answer when aligned |
|-------|----------|---------------------|
| **Data** | Does advancement bend on LOO pool quality? | **Yes** — stylized fact (Army, MBB; tenure preliminary) |
| **Sim** | Can congestion-in-score produce that bend on the **same** X? | **Yes** — minimal mechanism POC (if knobs reproduce shape) |
| **Theory** | Why would both be true in one framework? | **`L_net`** — same ontology; sim operationalizes **D in selection**; environment story explains rise **and** fall |

**Bridge (aligned case):**

```text
E[Y | poolq_loo]  ≈  E[1{S in top K} | poolq_loo]     (same X, same Y kind)
```

Left = empirical inverted-U. Right = what the sim **aggregates** after running **S** inside each pool-quality bin.

#### Step 4 — What Alex's equation explains vs what `L_net` still adds

Even with perfect axis alignment, the jobs **do not collapse**:

| | **Alex score `S`** | **`L_net = B − D`** |
|--|-------------------|---------------------|
| **Explains downturn?** | **Yes, via D in ranking** — congestion at the top | **Yes, via net constraint** — D dominates B in elite pools |
| **Explains upturn?** | **Only indirectly** — better pools may have more dispersion; not a B term in **S** | **Explicitly** — B leg (development, visibility, upside) |
| **What's on the x-axis?** | Same `poolq_loo` — still **bundles** B and D | Decomposition **concept** — not two separate estimated curves in v1 |
| **Generative role** | **Simulation engine** — shows D-in-selection is **necessary** for the shape | **Narrative spine** — why the bundled x-axis **should** bend |

**Crisp sentence:** Aligned axes mean sim and data tell the **same qualitative story on the same plot**. Alex's score explains **how congestion in ranking can generate the downturn**. `L_net` explains **why the whole environment curve rises then falls** (help and hurt in one frame) — including the part of the rise that is **not** inside the score equation.

#### Step 5 — What you would still **not** claim (even if aligned)

- That you **estimated** separate B(Q) and D(Q) functions
- That **S** includes development benefits (B-leg) — it does not
- **Parametric identity** — same shape ≠ same coefficients / same bins
- **Causation** — associational language throughout
- That one basketball generative preset **proves** Army and tenure

**v1 claim (aligned version):** Cross-domain **phenomenon** on LOO pool quality + **minimal generative ingredient** (congestion in score necessary; talent-only fails) on the **same conditioning axis** + **`L_net`** as the conceptual decomposition + honest limitations on tenure and estimation.

#### Thirty-second script (aligned-axis version)

> "Imagine both plots use leave-one-out pool quality on X and advancement rate on Y, and both show the inverted-U. The data curve says: elite peer pools stop helping at the top. The simulation runs Alex's score inside each pool — ability minus congestion, top K selected — and can reproduce that downturn when congestion is on. Talent-only can't. So the sim shows congestion in **selection** is a **minimal necessary ingredient** for the shape. My `L_net` frame still adds the **why** in two legs: peers can help through development and visibility and hurt through substitutability and finite slots — the score puts only the constraint leg into ranking, not the full benefit-minus-constraint story."

---

*Print:* `./scripts/convert_multiple_md_to_pdf.sh 30`  
*Print (dense):* `./scripts/convert_multiple_md_to_pdf.sh --narrow 30`
