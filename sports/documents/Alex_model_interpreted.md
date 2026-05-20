# Alex Gates — Viable Peer Congestion Model (interpreted)

Structured notes with LaTeX. **Verbatim source:** `Alex_model.md`.  
**Live discussion addendum:** [Paper Directions 12 (PD12)](#addendum-paper-directions-12-pd12--may-20-2026) — May 20, 2026 transcript; clarifies capability, crowding vs. quality, and empirical priorities.

**Alexander Gates** — Assistant Professor, School of Data Science, University of Virginia  
[https://www.alexandergates.net/](https://www.alexandergates.net/)

---

## Main idea

Systems that concentrate high-performing individuals generate **endogenous congestion** in evaluative comparisons, producing **diminishing and eventually negative marginal returns** to elite affiliation.

Congestion is **not** “more good people nearby.” It must alter how **evaluation** and **organizational selection** operate.

---

## Core simulation (proof of concept)

Latent ability → assortative teams → **viability** (smooth threshold) → **peer congestion** (density of viable peers, LOO) → **evaluation score** → global selection (top decile).

Key objects:

| Symbol | Meaning |
|--------|---------|
| $a_i$ | Own ability |
| $\bar{a}_t$ | Team mean ability |
| $v_i$ | Individual viability, e.g. $\sigma\big(\gamma(a_i - \theta_v)\big)$ |
| $C_{i,t}$ | Peer congestion (mean viable-peer density on team, excluding self) |
| $S_i$ | Evaluation score: $a_i - \lambda C_{i,t} + \varepsilon_i$ |

**Implementation:** `sports/539_alex_model.ipynb` — function `simulate_viable_peer_congestion()`.

---

## Mechanisms (not mutually exclusive)

### 1. Comparative evaluation

Evaluators compare candidates to **local reference groups**. In elite environments, “good” becomes normal; **exceptional performances appear less stand-out** (PD12 wording: not “less exceptional,” but harder to distinguish from strong peers).

$$
\text{signal}_i = a_i - f(\text{local peer quality}) + \epsilon_i
$$

—not $a_i$ alone. (NCAA: 15 PPG on a mid-tier team vs. the same player on a stacked roster.)

**Prediction:** congestion affects **signal distinctiveness**.

### 2. Attribution dilution

On strong teams, success is harder to assign individually (system? teammates? suppressed stats?). Plausible in academia, sports, firms, entertainment.

### 3. Finite attention

Bounded evaluator capacity. Elite teams contain **too many** plausible candidates → triage on stars/heuristics → harms **marginally excellent** candidates.

**Prediction:** congestion penalty strongest for **near-threshold** individuals (superstars survive; weak never competed; borderline elite are substitutable).

### 4. Organizational risk minimization

Many viable candidates → conservative selection; marginal benefit of any one hire declines; reliance on prototypes, fame, age heuristics. **Substitutability** rises.

### 5. Opportunity suppression (recursive)

Elite teams allocate minutes, touches, visibility, recommendations unevenly:

$$
\text{viable peers} \rightarrow \text{fewer opportunities} \rightarrow \text{less distinct signals} \rightarrow \text{more congestion}.
$$

### 6. Queueing and timing

Few advancement slots; many qualified people queue → delay, exit, invisibility — **temporal** congestion.

### Framing

> Elite environments increase both **capability** and **substitutability**.

| Environment | Capability | Substitutability |
|-------------|------------|----------------|
| Weak | Low | Low |
| Moderate | High | Manageable |
| Elite | Very high | Extreme |

**PD12 clarification on “capability”:** In the May 20 conversation this was **not** organizational/program capability (e.g. “Duke’s institutional strength”). Alex revised it to **own performance and differentiation within the local peer group** — effectively a **proxy for latent talent** $a_i$: in moderate environments top players still **stand out**; in elite environments everyone is strong but **substitutable**, so identifiability collapses even when absolute $a_i$ is high. See the **PD12 addendum** below for full discussion.

Organizations reward quality imperfectly under uncertainty, finite attention, and **comparative** evaluation. Many highly viable candidates → compressed margins, noisier/heuristic selection.

---

## NCAA basketball operationalization

Observable **viable peer** structure. Three constructs:

1. **Own ability** $a_i$ — e.g. points per minute; better: NBA predictive composite (BPM, WS/40, recruiting, etc.). PPM acceptable for proof of concept.

2. **Team quality**
   $$
   \bar{a}_t = \frac{1}{n_t}\sum_j a_j.
   $$

3. **Viable-peer congestion** — density of teammates who **compete for the same scarce advancement**, not merely “good teammates.”

**Simple congestion:**
$$
C_{i,t} = \frac{1}{n_t - 1} \sum_{j \neq i} \mathbf{1}(a_j > \theta),
$$
with $\theta$ from top prospect share, draft probability, McDonald’s All-American, future pro, combine invite, etc.

**Role-specific (stronger):**
$$
C_{i,t}^{\text{role}} = \frac{1}{n_t - 1} \sum_{j \neq i} w_{ij}\,\mathbf{1}(a_j > \theta),
$$
$w_{ij}$ = positional / playstyle similarity.

**Empirical draft model:**
$$
P(\text{draft}_i) = f(a_i,\, \bar{a}_t,\, C_{i,t}).
$$

Predictions: $\partial a_i > 0$; $\bar{a}_t$ initially positive; $\partial C_{i,t} < 0$.

**Inverted U:** raw team quality may show downturn; **viable-peer congestion** should explain it.

- Baseline: $\text{Draft}_i \sim a_i + \bar{a}_t + \bar{a}_t^2$
- Mechanism: $\text{Draft}_i \sim a_i + \bar{a}_t + C_{i,t}$ — quadratic weakens

**Heterogeneity:** downturn strongest for **middle-high** prospects (not top 1%, not non-prospects).

**Quasi-experiments:** mega-recruit years, portal shocks, one-and-done, NIL concentration — e.g. after several elite guards arrive, incumbent guards’ draft odds fall **conditional on performance**.

---

## Secondary empirical tests (beyond curve-fitting)

Core test: downturn **mediated** by viable-peer density.

### 1. Mediation

Baseline:
$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2.
$$

Mechanism:
$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + C_{i,t},
\quad
C_{i,t} = \frac{1}{n_t - 1}\sum_{j \neq i} \mathbf{1}(a_j > \theta)
$$
(or smooth viability version). Expect $C_{i,t} < 0$ and **shrinkage** of the negative quadratic / top-end team-quality penalty.

### 2. Congestion concentration

Bin teams by $C_{i,t}$. High-congestion bins → steepest right-side decline; low-congestion → monotone or saturating returns to $\bar{a}_t$.

### 3. Assortativity interaction

$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + A_s \cdot \bar{a}_t^2,
$$
$A_s$ = system assortativity. Negative interaction: stronger sorting → stronger top-end penalty.

### Further predictions

| Prediction | Test sketch |
|------------|-------------|
| Mediation | Add $C_{i,t}$; quadratic on $\bar{a}_t$ weakens |
| Near-threshold harm | $Y_i \sim a_i + \bar{a}_t + C_{i,t} + a_i \times C_{i,t}$; penalty largest just above viability margin |
| External benchmarks | Penalty smaller for standardized metrics; larger for committees / prestige narratives |
| Fixed opportunity capacity | Penalty stronger when few slots per team/lab |
| Delay, not only failure | Survival $h_i(t) = h_0(t)\exp(\beta_1 a_i + \beta_2 \bar{a}_t + \beta_3 C_{i,t})$, $\beta_3 < 0$ for high $a_i$ |
| Cohort shock | DiD: existing near-threshold members crowded when strong cohort enters |
| Mobility reversal | Leaving congested elite for strong-but-less-congested teams raises success odds |

**Paper framing:**

> Beyond reproducing an inverted-U between team quality and individual advancement, the model predicts the downturn is explained by **viable-peer density**, concentrated among **near-threshold** candidates, amplified in **assortative** systems, and partially **reversed** by moves to less congested environments.

---

## Link to this repo (538 / 530)

| Alex construct | Current PDE stack |
|----------------|-------------------|
| $a_i$ | `perf` / synthetic `ability` |
| $\bar{a}_t$ | `team_mean` / pool mean |
| Viable peer $C_{i,t}$ | Not raw LOO sum of all $A_j$; use $\sum_{j \neq i} \mathbf{1}(a_j > \theta)$ or smooth viability density |
| LOO mean $L_Q$ | `poolq_loo` / `congestion_quality` |
| Raw LOO sum $L_C$ | `pool_c_loo` — scales with roster size; near redundant with $L_Q$ at fixed $n$ |

**Next modeling step:** replace or supplement `pool_c_loo` with **viable-peer congestion** as in the simulation notebook.

---

## Addendum: Paper Directions 12 (PD12) — May 20, 2026

**Source:** `transcripts/20260520_Paper_Directions_12_otter_ai_transcript.docx` (Otter; ~16 min).  
**Participants:** Alex Gates, Charles Levine.  
**Purpose of this section:** Record what was **agreed, corrected, and prioritized** in the live discussion so implementation and writing stay aligned with Alex’s intent—not only with the AI-generated text in `Alex_model.md`.

---

### Provenance of `Alex_model.md`

Near the start of PD12, Charles noted that Alex had not literally written every sentence of the memo by hand. Alex confirmed the document was produced in **~45 minutes with AI assistance** from prompts (“we have the tools, let’s use them”). Treat `Alex_model.md` as a **structured theoretical brief** and mechanism checklist, not a finalized paper. **PD12 overrides or sharpens** several terms (especially **capability** and **crowding vs. quality**) where the conversation went deeper than the draft text.

---

### Mechanism-by-mechanism notes from PD12

The six mechanism classes in `Alex_model.md` were walked through in order. Below: what resonated, what to stress empirically, and what **not** to over-build in v1.

#### 1. Comparative evaluation

- Charles reframed the second bullet: the punchline is that **exceptional performances appear less stand-out** in elite reference groups—not that they become “less exceptional” in absolute terms.
- Alex endorsed that wording.
- **Empirical tie-in:** This is **signal distinctiveness** (evaluator sees $a_i - f(\text{local peers})$), not raw production. Pool **mean** quality ($\bar{a}_t$, `poolq_loo`) is related but not sufficient for congestion.

#### 2. Attribution dilution

- Uncontroversial; aligns with prior VECTOR thinking (lab effect, system player, brand halo).
- No PD12 change; include in narrative, optional as separate test later.

#### 3. Finite attention

- Strong alignment with Charles’s **earlier model** (some variables already mirrored this)—good convergence check.
- **Substitutability** of **borderline elite** candidates is the money phrase.
- Charles linked borderline substitutables to the **NIH / Wang** “just at the cut line” population: the inverted-U harm is not for obvious superstars or non-contenders, but for **near-threshold** types who look interchangeable when many similar peers exist.

#### 4. Organizational risk minimization

- Charles: “that’s **Moneyball**.”
- NBA gloss: when several teammates look promising, scouts fall back on **heuristics** (physically prototypical, younger, already famous)—Charles jokingly added “or white” as a cynical example of voodoo selection; keep that out of formal write-ups unless explicitly studying bias.
- **Modeling:** This supports **noisier, less meritocratic selection** when $C_{i,t}$ is high, not only lower $P(\text{draft})$.

#### 5. Opportunity suppression (recursive)

- Charles strongly endorsed Alex’s word **“recursive”**: viable peers → fewer touches/minutes/visibility → weaker observable stats → even less distinction → more congestion.
- This bridges **production** and **evaluation**; important for NCAA where $a_i$ is endogenous to role allocation.

#### 6. Queueing and timing

- Charles asked if this is just **selection scarcity**; Alex: **yes**, but scarcity can arise in **multiple ways**—time (queue), comparison (local rank), finite slots (attention).
- **Scope discipline:** Alex cautioned **not to go too deep on every facet** in the first empirical pass. The six mechanisms are **reasons the theory matters**; the paper should **address some, not all**, and use them to guide measurement—not prove six separate causal channels in one MBB table.

---

### Capability vs. substitutability (critical PD12 fix)

The three-row table in `Alex_model.md` is easy to misread.

| Misread (Charles, first pass) | Corrected read (Alex, PD12) |
|------------------------------|-----------------------------|
| “Capability” = organizational strength of the program | “Capability” ≈ **level and clarity of individual talent** in the environment—**how differentiated** the person is from peers |
| Weak schools = low org quality | Weak environments = low **absolute** talent and low substitutability |
| Elite schools = high org quality only | Elite environments = **very high** talent but **extreme substitutability**—top individuals are excellent but hard to tell apart |

Charles and Alex converged: in implementation, **capability ≈ latent $a_i$** (own performance, NBA composite, BPM, etc.), while **substitutability** is the new organizational object captured by **viable-peer congestion** $C_{i,t}$.

**Implication for LOO constructs:**

- **Congestion quality** (LOO **mean** of teammate `perf`, `poolq_loo`) ≈ $\bar{a}_t$ / local peer caliber → can track the **rising** leg of an inverted-U (exposure, development, credibility).
- **Congestion crowding** (LOO **count** of teammates above viability threshold $\theta$) ≈ $C_{i,t}$ → should track the **downturn** (marginal candidates crowded out).
- At **fixed roster size**, LOO **sum** and LOO **mean** are almost the same information ($\sum \approx (n-1)\times \text{mean}$); PD12 + Alex sim imply **do not treat sum as “crowding”**—use **threshold counts** (or smooth viability density as in `539_alex_model.ipynb`).

Alex on operationalizing crowding (~7:20): *“How many people are above the threshold—that’s an easy calculation.”* Then subtract a **small fraction** of that count from innate signal $a_i$ in the evaluation equation (simulation); empirically, enter $C_{i,t}$ in $P(\text{draft})$ or promotion hazard.

---

### Empirical hook discussed on the call: superstar tail of the draft curve

Charles connected the **small uptick at the very highest team-quality / pool-quality ventiles** in the 530 draft-rate plots to Alex’s theoretical prediction that **elite superstars still get drafted** even when borderline players suffer from congestion.

- Alex had not yet mapped that plot to the theory; on PD12 he agreed: **“They still get up there in the very best teams.”**
- **Use in writing:** The inverted-U is **not** “elite teams hurt everyone”—it is **heterogeneous**: top-$a_i$ individuals clear the market; **middle-high** near-threshold players bear the congestion penalty. Heterogeneity tests in `Alex_model.md` are not optional flourishes—they are **the** discriminating prediction.

### Army evidence shown to Alex (same meeting): 100-bin CIF, equal width

Charles showed Alex a **two-panel** figure from the Army pipeline (**“100 BINS, CA, EQUAL WIDTH”**) to argue the downturn is **robust across systems**, not an NCAA-only curve-fit:

| Panel | Outcome | Chart type |
|-------|---------|------------|
| **Top** | **Promotion** (competing risks) | Final CIF by pool-quality bin (Q1–Q99) |
| **Bottom** | **Attrition** | Final CIF on the **same** binning / covariate axis |

**How to read the pair together:**

- **Promotion (top):** Inverted-U–style pattern—gains from better pools up to a point, then a **downturn** in the highest bins (congestion / substitutability story for marginal promotable officers).
- **Attrition (bottom):** On the identical 100-bin axis, attrition is **not** a mirror image by construction (competing risks vs. separate cause-specific CIF). The **late-bin rebound** Charles called the **superstar tail** on this figure is visible on the **attrition** panel (CIF rises again toward Q70–Q99). Interpret with care: document whether top bins are **fewer people / wider uncertainty** before over-claiming; the intended PD12 point was **cross-domain shape exists**, not that promotion and attrition must move in opposite directions bin-for-bin.

**Why Alex cared:** One domain (MBB draft ventiles) can look like a house of cards; **Army promotion + attrition on the same pool construct** shows the broader VECTOR phenomenon is already in the tenure/Cox stack. That motivated confidence before investing in **congestion crowding** in MBB.

*Figure file (workspace): user-provided Army CIF screenshot, May 2026 — promotion top, attrition bottom.*

---

### Priority workstreams (Alex’s agenda, second half of PD12)

Alex separated four threads. They are **not** the same task.

#### Priority 1 — Parameter **identifiability** (simulation + fit)

- Fit the generative model (~5–6 parameters) to **real data in all three domains** currently in scope (MBB, tenure, …).
- Alex suspects the model is **overparameterized**: many parameter combinations may fit similarly.
- **Remedies discussed:**
  - **Fix** some generative knobs across worlds (e.g. same Beta hyperparameters everywhere—not estimated per dataset).
  - **Roll** mechanism-specific terms into a single outcome $Y$ per domain (“in this dataset we roll $a,b,c$ into $Y$; in that one, $a,b,d$”).
  - **Lower dimensionality** until recovered parameters are **unique and interpretable**, not just curve-fitting inverted-U shapes.

**Distinction:** Identifiability = “Can we estimate the structural parameters of *this* model from *these* tables?”

#### Priority 2 — **Extreme events** (simulation sensitivity)

- Not “rare draft surprises” in data—**knob-turning in the sim**: set $\lambda \to 0$, turn congestion off, tighten viability, etc.
- Confirm the inverted-U and mediation patterns **disappear mechanistically** when they should.
- Charles asked for clarification; Alex: validate the **internal logic** of `539_alex_model.ipynb` before over-interpreting one empirical ventile plot.

#### Priority 3 — **Model-guided empirical features** (different from Priority 1)

- The theory should **propose new measurements**, not only fit old ones.
- **Flagship example:** explicit **congestion** in MBB—quantify $C_{i,t}$, test whether it **mediates** the downturn in $\bar{a}_t$, Kentucky/Duke mega-recruit years as **quasi-experiments**.
- Charles (~12:15): ideal congestion measure **indirectly reflects** talent in the system but **does not enter the outcome as raw $a_i$**—so one can study “how crowded is this team?” and predict harm to marginal members. In practice $\theta$ is built from $a_j$ or prospect signals ($Y_{\text{draft}}$, combine, recruiting); document that transparently.

**Charles’s immediate commit after the call (~8:22):** focus on adding the **congestion crowding** term in the empirical pipeline (not replacing all of 538, but making $C_{i,t}$ first-class).

#### Priority 4 — **Falsification and scope** (let seep over weeks)

- The three main systems were **chosen** because they plausibly satisfy the model’s conditions; a strong paper also shows **where it fails**.
- **Task:** Find a **fourth or fifth** setting where the inverted-U **does not** appear (NHL draft mentioned), and explain **which assumption breaks** (e.g. different attention structure, evaluation noise, no local peer congestion for slots).
- Also: **new positive domains** if data exist—Charles suggested **macro economics** (GDP, patents, oil production vs. GDP across nations competing for firms). Alex: “really nice level of estimation” at country–company scale.

---

### Viable-peer signals in MBB data (connects PD12 to repo work)

`Alex_model.md` lists example thresholds for $\mathbb{1}(a_j > \theta)$: top PPM share, draft probability, McDonald’s All-American, future pro, **combine invitation**.

| Signal | Role in $C_{i,t}$ | Repo status (May 2026) |
|--------|-------------------|-------------------------|
| `perf` / BPM / WS/40 | Continuous $a_j$ for $\theta$ or smooth $v_j$ | `perf` on 530 panel; SR merge |
| LOO mean `poolq_loo` | $\bar{a}_t$-like **quality**, not crowding | 530, 538 CELL 10 |
| LOO sum `pool_c_loo` | Near-redundant with mean at fixed $n$ | 538 crowding mode |
| $Y_{\text{draft}}$ | Outcome + possible $\theta$ component | `athlete_id_draft_lookup` |
| Combine | Prospect visibility / $\theta$ | `combine_bridge.py` → `athlete_id_combine_lookup.csv`; **measurement row**, not full invite list |
| Labeled union $Y_{\text{nba\_signal}}$ | “Serious NBA-facing peer” for **thicker** $\theta$ | Design discussed; not in panel export yet |

**PD12 did not discuss combine–draft union**; separate design memo: union helps **peer identification**, not draft **outcome**; see bridge diagnostics (~58% of combine rows linked to `athlete_id`).

---

### Natural experiments Alex named (empirical Priority 3)

- **Kentucky / Duke mega-recruiting years** — exogenous shocks to $C_{i,t}$ on a fixed roster.
- **Transfer portal / NIL** — later waves of concentration (if timed in data).
- **Cohort shock / DiD** — when a school adds several elite same-position players, **incumbent** near-threshold players’ draft odds should fall **conditional on own $a_i$**.
- **Mobility reversal** — leaving a congested elite program for a strong but less crowded team should **raise** advancement odds (harder in MBB single-season panel, easier in tenure).

---

### Suggested implementation order (repo)

1. **`tier1_mechanism_vars.py` / 530 export:** `peer_viable_count_loo` (and optional smooth $C_{i,t}$ from `539` logic); keep `poolq_loo` as quality leg.
2. **538 CELL 10:** Third playground mode or replace “crowding = LOO sum” with **viable-peer count**; label UI clearly (quality vs. crowding).
3. **`539_alex_model.ipynb`:** Cells for Priority 1–2 (fit / identifiability, parameter kill switches).
4. **`panel_rebuild` / `combine_bridge`:** Optional `Y_combine_meas`, `Y_nba_signal` on `player_season_panel_530.csv` for $\theta$ robustness.
5. **Writing:** Short PD12 cross-ref in advisor briefs; do **not** claim all six mechanisms are separately identified in MBB v1.

---

### One-paragraph paper sentence (PD12-aligned)

> We distinguish **team quality** (mean peer performance, $\bar{a}_t$) from **viable-peer congestion** (density of teammates above a prospect threshold, $C_{i,t}$). Elite environments raise both average talent and **substitutability**; the inverted-U in advancement is predicted to steepen on the right primarily where $C_{i,t}$ is high, especially for **near-threshold** individuals, while **top latent talent** still clears selection—consistent with the small recovery at the highest ventiles in our NCAA draft data.

---

### Open questions left on the table

- Exact $\theta$ for MBB: global PPM quantile vs. combine/draft-based $Y_{\text{nba\_signal}}$ vs. smooth logistic viability (539).
- Whether to **mediate** with $C_{i,t}$ in LPM only or also in Tier 1 generative selection (538).
- NHL (or other) **negative case** data feasibility for Priority 4.
- Country-level economics as fourth **positive** domain vs. falsification case.

*Addendum last updated to reflect PD12 transcript and repo state as of May 2026.*
