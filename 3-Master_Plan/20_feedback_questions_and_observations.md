# Feedback, questions, and observations (living doc)

**Canonical name:** `20_feedback_questions_and_observations.md`  
**Purpose:** Capture Charles’s reading-time questions and COMPASS answers. **Append new entries at the top** (newest first). Not part of the must-read print stack — use while working through `#01`–`#14` or inking Word.

**PDF (you run locally — narrow margins):** `./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/20_feedback_questions_and_observations.md "" pdf_styles_narrow.css`  
*(COMPASS will not auto-export; re-run after `.md` edits when you want an updated print copy.)*

**Related:** [`Charles_reading_list.md`](Charles_reading_list.md) · [`01_forward_plan_reading_guide.md`](01_forward_plan_reading_guide.md)

---

## How to add entries

```text
### YYYY-MM-DD — Short title

**Context:** (which doc / section you were reading)

**Question / observation:** …

**COMPASS answer:** …
```

---

---

### 2026-06-11 — Full reading-stack shorthand scrub (all #01–#14)

**Request:** Audit **every document on the print stack**, not just `Charles_reading_list.md` — fix agent-only shorthands; explain **B-lite** origin.

**COMPASS answer:**

| Term | Plain English |
|------|----------------|
| **B-lite** | **COMPASS coinage** (`#14` Q2, 2026-06-15): closure strong enough for Alex **without** full 3-domain identifiability. See `#01` **“B-lite closure”** section. |
| **Path II** | Manuscript-first lock: 3 empirical legs + 1 basketball generative POC + honest axis mismatch. |
| **Rung 1–4** | Paper-argument steps (phenomenon → mechanism → features → predictions → write). **Rung 2.5** = model-guided measurements. |

**Files patched this pass:** `#01`–`#09`, `#13`, `#14`, `#05`, `#10`, `#12` (+ prior `#20` § fixes). **Rule going forward:** first notebook mention = full path; capitalized agents need no gloss; **`§` default = manuscript Word** unless file says otherwise.

---

### 2026-06-11 — `§` symbol confusion + reading-list shorthand audit

**Context:** Cumulative “lost in the sauce” from agent-only shorthands (`§5`, bare `4D`, notebook numbers, etc.) while reading the must-read stack.

**Question / observation:** Does **`§N` always mean the manuscript? What else is hiding in the reading list that wasn’t designed to be forward-facing?

**COMPASS answer:** **Usually yes — but not always.** That ambiguity is a doc bug, not your fault.

| Symbol | Default meaning | Common trap |
|--------|-----------------|-------------|
| **`§N`** | **Word manuscript** section (Dakota v03 / `#10`) | Agent note “§4 predictions” often meant **staging `#12` §4** → manuscript **§7**, while manuscript **§4** is **tenure** |
| **`#NN`** | Numbered reading file (`#07`, `#12`, …) | `#12` §4 ≠ manuscript §4 |
| **`§X` in one file** | Subsection **inside that `.md` only** | `#07` §F ≠ manuscript §F |
| **530 / 537 / 538D / CELL 4D** | Repo notebook labels — need **full path** on first mention | Bare “4D” is not four dimensions; it is **`538D` CELL 4D** |

**Audit done (this session):**

- Added **“Symbol systems”** block to [`01_forward_plan_reading_guide.md`](01_forward_plan_reading_guide.md) — manuscript § map, staging `#12` § map, repo shorthand table.
- Updated [`Charles_reading_list.md`](Charles_reading_list.md) decoder banner + clarified ink order (**manuscript §5 → §1 → §4**; predictions = **§7**).
- Fixed wrong “§4 Predictions” wording in this file (below) → **manuscript §7** / staging **`#12` §4**.

**When stuck:** open `#01` → **Symbol systems**; do not infer from context alone.

---

### 2026-07-01 — Notebook shorthand too bare (“4D” example)

**Observation:** In `#20` §5, the Wang-move hook row says “Near-threshold 4D (#1)” with nothing nearby saying **which notebook**, **which cell**, or **which export file**. With dozens of notebooks, that shorthand is one step too short.

**COMPASS answer:** Fair catch — agents know `538D` / `CELL 4D` from June context; you shouldn’t have to. **Rule:** any notebook/cell cite in `#20` or chat must include **path + cell label + export (if any)** on first mention. Expanded §5 below and `#01` glossary (`CELL 4D`, `538D`).

---

### 2026-07-01 — Shorthand lookup tax

**Observation:** Appreciate extensive shorthand for agent coordination, but ~1 in 7 times I still have to go looking.

**COMPASS answer:** Valid — shorthand is for **multi-agent lock-in**, not for making you decode every reply. **Going forward:** (1) first use of a term in chat gets a brief gloss or `(#01)`; (2) file names when citing guidance, not bare “PD12”; (3) recurring misses get added to [`01_forward_plan_reading_guide.md`](01_forward_plan_reading_guide.md) glossary (hook, PD12 guidance vs #14, POC, axis mismatch, scope discipline, sort-and-chop, overlap — added this session). **Flag any miss** in chat; treat it as a doc bug, not your fault.

---

### 2026-07-01 — Pool mean vs LOO; Wang predictions; Alex vs sorting; overlap; “hook”

**Context:** Reading `#03` and related stack; random comments while working through must-read docs.

---

#### 1. Pool mean vs LOO (Army + tenure) when AWS returns

**Observation:** Temporarily lost Army AWS access. When it returns, considering additional plots using **pool means** instead of LOOs. Same inverted-U on pool mean might save a justification step and simplify things — possibly for tenure too.

**COMPASS answer:** **Worth doing as a supplementary check — not as a replacement for LOO in v1.**

**Why it could help:** Generative POC reads out on **pool mean**; empirical v1 is locked on **LOO pool quality** (`poolq_loo`). That gap is the honest “axis mismatch” sentence in `#05`. If Army (and maybe tenure) also show an inverted-U on a **whole-pool / team-mean** x-axis, you can say: *same qualitative shape on a second conditioning object*, which softens the “we only see it one way” worry.

**Why it doesn’t fully remove the justification step:**

| Issue | LOO pool quality | Pool mean |
|--------|------------------|-----------|
| **Concept** | “My peer environment **excluding me**” | “My team’s average **including me**” |
| **Mechanism fit** | Matches comparative evaluation / congestion story | Mechanically correlated with own ability |
| **Alex / PD12** | Primary empirical object | Secondary at best |
| **Sorting discovery** | About **who is in the pool** (overlap) | Different question — mean vs LOO is **how you summarize** the pool |

**Action when AWS returns:** Run plots; label **supplementary**; compare side-by-side with LOO. If both bend the same way → nice Alex-meeting slide. If only LOO bends → **supports** comparative-evaluation framing. Either outcome is informative.

**Tenure:** `poolq_loo` = quality leg; `pool_size_oa_loo` = **congestion proxy**, not substitute for LOO quality. Pool-mean tenure plot → appendix / robustness, not main Setting 3 fact.

**Do not delay manuscript inking for this.** Tier 3 / post-AWS enrichment.

---

#### 2. Doc `#03`: “Non-obvious predictions distinguishing competing explanations”

**Question:** Is this a Wang reference? Explain, including Wang’s exact example.

**COMPASS answer:** Yes — **Wang-ladder language**. Contribution **#3** in `03_Where_we_are_now.md`: phenomenon → mechanism → **predictions that discriminate** → (deferred) network extensions.

**“Wang move” in this project** (`#13`, `#04`):

> A strong theory paper must **predict something you did not use to find the curve** — not only reproduce the inverted-U.

Inverted-U on `poolq_loo` = **Rung 1**. Wang-style paper also needs **Rung 3**: tests separating your story from cheaper alternatives (e.g. pure quadratic in team quality with **no** congestion channel).

**This project’s two prediction slots:**

| # | Name | What it discriminates |
|---|------|------------------------|
| **#1** | Near-threshold heterogeneity | Congestion hurts **borderline elite**, not superstars or non-contenders (Alex mechanism 3) |
| **#2** | Peak shift with **Λ** | Global slot scarcity moves the peak — finite distinction capacity vs purely local story |

**Wang’s example (Yin et al. 2019 — notes in `5-Manuscript/obsolete/superseded_briefings/wang_paper_model.md`):**

Not about inverted-U pools; the **logic** is what we imported.

- **Competing explanations beaten:** “Winners were always better” (raw early failure counts don’t separate); “Success is random / memoryless” (streaks aren’t memoryless).
- **Non-obvious prediction (k-memory model):** Actors reuse components from past attempts with memory **k**; critical **k\*** below → stagnation, above → systematic improvement (phase transition). They test trajectory / learning patterns a failure-count model would not predict.

**PD12 tie-in:** Near-threshold harm ≈ NIH **“just at the cut line”** — substitutability among similar viable applicants.

**Manuscript placement:** **Manuscript §7** (Predictions; ink from staging **`#12` §4**) — inverted-U alone is not enough; #1 and #2 are **candidate** discriminators (honest language per `#07`).

---

#### 3. Alex “score/selection” vs our “talent/sorting”

**Observation:** Gut feeling that Alex’s minimal model defines **selection / score / signal**, whereas our work defines **talent** and thus **sorting**. What is each model’s basic approach, how do they differ, how open to decomposition?

**COMPASS answer:** They sit at **different layers**; `#05` is the nesting note.

```text
Menger / ecology layer          WHO gets sorted into which comparison pool
         ↓
Charles empirical layer       WHAT pool composition looks like (overlap — not disjoint bins)
         ↓
Alex minimal model layer      HOW evaluators SCORE and SELECT given local structure
         ↓
Reduced form (L_net = B − D)  Net advancement propensity (benefit minus constraint)
```

| | **Alex (minimal model)** | **Charles emphasis (sorting + empirics)** |
|---|--------------------------|-------------------------------------------|
| **Basic question** | Given local peers, how does **evaluation/selection** work under congestion? | Given institutions, **who ends up in which peer pool**, and what does that do to advancement? |
| **Core object** | **Score** \(S_i = A_i - \lambda C_{i,t}\) → pick top *K* | **Pool assignment** + **LOO pool quality** → inverted-U |
| **Congestion** | Viable-peer density in **selection rule** | Also `crowding_smooth`, pool overlap, finite slots (Λ) |
| **Generative POC** | Soft assignment on fixed/simulated rosters; talent-only fails | 538 pool assignment, overlap plots |
| **Decomposition** | Narrow: A vs D in score; six Alex mechanisms | Wider: B vs D in \(L_{\text{net}}\); sorting vs selection vs opportunity suppression |
| **v1 role** | Rung 2 POC + D-leg ontology | Rung 1 phenomenon + **distinctive** sorting/composition evidence |

**One sentence for Alex:** *You supply the operational selection score and the quality-vs-congestion split; I supply cross-domain empirical regularity and evidence that realized pools are overlapping talent ecologies, not neat disjoint tiers.*

Not competing models if nesting chain is explicit. Alex is not explaining Duke’s recruiting pipeline; we are not estimating six separate causal channels in one MBB table (PD12 scope discipline).

---

#### 4. Sorting / pool overlap as top discovery (expanded)

**Observation:** Plots showing talent overlap and range of pools were highly informative — crushed naive model of sorting players 1–N and chopping into disjoint talent intervals as pool proxies.

**COMPASS answer:** This is one of your **strongest original empirical contributions**, separate from “we also see an inverted-U.” It answers a **prior** question that many papers skip: *before we interpret advancement vs local pool quality, what do comparison pools actually look like?*

---

**The naive model (what we used to assume)**

Early generative work — especially the frozen **`537`** “sort-and-chop” lab — treated pools like this:

1. Rank every player on ability (1 → *N*).
2. Cut the continuum into **equal-count slices** (disjoint bins).
3. Call each slice a “pool” or team tier.

That assignment is **clean on paper** but **wrong on the data.** It produces interval “coverage” ≈ **1** everywhere on the performance axis: at any talent level, essentially **one** bin claims that player. No cross-pool sharing of talent levels.

---

**What real pools look like (530 forensics — basketball)**

**`530_sports_pipeline.ipynb` CELLs 5–9** (documented in `sports/documents/Tier1_Presorting_Design_Note.md`) measure **realized** rosters, not simulated ones:

| Finding | Numbers / pattern | Implication |
|---------|-------------------|-------------|
| **Within-roster spread** | Median roster SD ≈ **0.8–1.0** z (PPM within-season) | Elite teams are **not** tight point masses of identical talent |
| **Mean vs dispersion** | Pearson *r* (team mean, roster SD) ≈ **0.26** — higher-mean teams slightly **more** dispersed, not less | Do **not** assume “elite ⇒ homogeneous roster” |
| **Interval overlap (CELL 8)** | **Actual** team-season talent windows: peak coverage **thousands** of pools at z ≈ 0 | Many teams’ [min, max] intervals **cross** on the ability axis |
| **Sort-and-chop benchmark** | Coverage ≈ **1** everywhere (red dashed line in CELL 8) | The old 537 **Assortative** assignment matches **red**, not **blue** |

**Plain English:** A player at a given talent level can plausibly appear on **many** kinds of teams. “Pool” is not a disjoint tier label — it is an **assortative but overlapping** comparison environment.

Same logic extends conceptually to Army units and tenure departments: local peer pools are **matched ecologies**, not non-overlapping bins on a global talent ladder.

---

**Why this matters for the dissertation (beyond a methods footnote)**

1. **Legitimizes LOO pool quality.** If pools were disjoint tiers, `poolq_loo` would collapse to “which bin am I in?” Overlap means LOO quality is a **continuous summary of a crowded peer field** — closer to Alex’s comparative-evaluation story.

2. **Separates sorting from selection.**  
   - **Sorting (your layer):** *Who ends up in which overlapping pool?* (Menger **selective ecology / assortative matching**.)  
   - **Selection (Alex layer):** *Given that local structure, how do evaluators score and pick?* (\(S = A - \lambda C\).)  
   The inverted-U on LOO quality is about **distinction inside** pools; overlap plots show **what those pools are made of**.

3. **Motivates the generative fix (538 / `tier1_pool_assignment.py`).** PD11 Thread A: draw team **target means** \(T_j\), assign players with **soft** probabilities \(\pi_{ij} \propto \exp(-(A_i - T_j)^2 / 2\tau^2)\) — overlap **by construction**. **`538D` CELL 10 Plot A** calibrates simulated overlap against 530 CELL 8; **`537` stays frozen** as the failed benchmark, not the forward path.

4. **Distinct from the inverted-U itself.** Reviewers could say “inverted-U is just curve-fitting.” Overlap forensics are harder to dismiss: they are a **structural fact about pool formation** that your old simulation explicitly got wrong and your new assignment explicitly fixes.

---

**What to say vs not say (claim discipline)**

| Do say | Do not say |
|--------|------------|
| Realized comparison pools show **substantial talent overlap** across units/teams/depts | We have **proven** the soft-assignment generative process is the true DGP everywhere |
| Disjoint sort-and-chop is a **useful null** that **fails** on basketball forensics | Overlap plots **replace** the inverted-U or Alex POC |
| Overlap motivates **assortative matching** language (Menger) and honest LOO conditioning | Every domain has identical overlap statistics (Army forensics pending AWS) |

---

**Manuscript placement (concrete — manuscript § numbers)**

| Manuscript § | Content |
|--------------|---------|
| **§1 or §3 (empirical)** | One **overlap / coverage** figure (`sports/530_sports_pipeline.ipynb` CELL 8 style, or cross-domain analog when Army returns) + paragraph: pools are overlapping, not disjoint tiers |
| **§5 (generative / methods)** | Brief contrast: talent-only fails (SCOUT C1/C2); **sort-and-chop fails overlap**; soft assignment + congestion-in-score is the forward generative story |
| **§6 or §5 discussion** | Menger **selective ecology** — who gets matched into elite local environments |
| **Appendix (optional)** | `sports/537_tier1_benchmark.ipynb` vs `538D` CELL 10 Plot A side-by-side for methods readers |

**Not** a substitute for Alex’s congestion-in-score POC — overlap answers *what we condition on*; Alex answers *how selection works given that conditioning*.

---

**Decomposition chain (keep repeating this)**

```text
Sorting / ecology     →  overlapping pools (530 forensics; Menger Ch 10)
         ↓
Local summary         →  LOO pool quality (poolq_loo) → inverted-U (Rung 1)
         ↓
Selection / signal    →  Alex score, congestion, near-threshold predictions
```

**One sentence for the paper:** *Advancement under constrained distinction requires comparison pools that are assortative but overlapping; treating pools as disjoint talent bins misstates the peer environment and misaligns both our earliest simulations and any purely tier-based reading of the inverted-U.*

**Repo pointers:** `530` CELLs 5–9 · `Tier1_Presorting_Design_Note.md` · `538_Cell10_Generative_Manual.md` (Plot A) · `tier1_pool_assignment.py`

---

#### 5. What does “hook” mean?

**Question:** Keep seeing “hook” — reminder? And what is the **spirit** of the word, not just the examples?

**COMPASS answer:**

---

**Core definition (spirit of the word)**

In this project, **hook** is workshop shorthand for an **attachment point** — a named place where an idea **hooks into** something else so it stays findable, honest, and actionable.

Not “marketing hook” (clickbait). Not “plot hook” (narrative suspense). Closer to:

> **A peg, handle, or anchor** that ties an abstract claim, mechanism, or literature bridge to a **concrete landing zone** — manuscript section, repo file, companion chapter, or prediction name — **before** (or without) that landing zone being fully built or proven.

Three things a hook always does:

1. **Names where something belongs** so you and the agents don’t re-litigate “where does Λ live?” every week.
2. **Admits incompleteness honestly** — a hook is allowed to be **prose-only**, **placeholder**, or **repo-target** until evidence arrives (`#07` guardrails).
3. **Keeps the stack connected** — theory ↔ measurement ↔ code ↔ chapter ↔ **manuscript §7** (predictions) stay linked without pretending the link is finished.

**One-line definition:** *A hook is a designated tether between an idea and where it will (or should) show up — not the proof itself.*

---

**Why we say “hook” instead of “placeholder” or “anchor”**

| Word | Why “hook” fits better here |
|------|-----------------------------|
| **Placeholder** | Sounds empty. A Λ hook still carries **conceptual content** (boards, draft picks, tenure slots) — you’re allowed to write **manuscript §7** sentences about it (from staging `#12` §4.2). |
| **Anchor** | Close, but static. “Hook” implies **connection across layers** (Menger ch → project story → Army prose). |
| **TODO** | Too task-list. Hooks are **structural** — part of the paper’s skeleton, not a stray chore. |
| **Claim** | Too strong. A hook is what you may **point at** before you may **assert** (see `#07`: supported vs preliminary vs defer). |

When docs say “Λ hook prose,” they mean: *write the conceptual paragraph now; don’t claim the sweep figure exists.*

---

**What a hook is not**

| Not a hook | Why |
|------------|-----|
| A finished result | D10 near-threshold export **is** evidence; “near-threshold hook” was the **named slot** before the PNG existed. |
| A vague vibe | “Congestion matters” is a theme. “**Repo hook:** `tier1_pool_assignment.py`” is a hook — you know where to implement. |
| Permission to overclaim | Hooks pair with claim discipline. “Conceptual hook” ≠ “demonstrated in all three domains.” |
| The inverted-U itself | Rung 1 phenomenon is **found**; hooks are mostly **Rung 3+** or **infrastructure** (where predictions / code / lit attach). |

---

**Four usages in project docs (examples)**

| Usage | What it hooks **from** → **to** | Example |
|--------|----------------------------------|---------|
| **Prediction hook** | Mechanism → **manuscript §7** prose (figure optional) | “**Λ hook**” = global slot capacity shifts peak (prediction **#2**); Army-led prose in **§7** — **no** finished Λ-sweep figure in repo yet |
| **Wang-move hook** | Model logic → test beyond discovery curve | Prediction **#1** near-threshold heterogeneity — see **worked example** below (not bare “4D”) |
| **Repo / PD12 hook** | Priority / mechanism → codebase location | “Repo hook: `sports/539_alex_model.ipynb`” in [`20260520_Transcript_12_guidance.md`](20260520_Transcript_12_guidance.md) |
| **Literature hook** | Companion chapter → your empirical story | Menger calibration table “project hook” column (Ch 10 → selective ecology / overlap) |

**Worked example — Prediction #1 (Wang-move hook, was “near-threshold 4D”)**

| What | Where |
|------|--------|
| **Prediction** | Near-threshold heterogeneity — congestion should bite **borderline elite**, not superstars or non-contenders (discriminates congestion from “elite pools are just hard”) |
| **Notebook** | `sports/538D_development.ipynb` |
| **Cell** | **CELL 4D** (fourth sub-block under CELL 4 — letter **D**, not “four dimensions”) |
| **Script** | `sports/tier1_heterogeneity_ventiles.py` |
| **Export (D10)** | `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/heterogeneity_ventiles_top_tail.png` (list in `#08`) |
| **Manuscript** | **Manuscript §7** (Predictions; ink from staging **`#12` §4**) — **candidate** readout per `#07` (exploratory, not fully validated cross-domain) |

**Do not write** “4D” alone in prose meant for you — always **`538D` CELL 4D** or the **export filename** the first time.

---

**How to hear it in conversation**

- “What’s the Λ **hook**?” → *Where in the manuscript and which domain leads the argument?* (Answer: **manuscript §7**, Army prose, boards/slots — not “we simulated Λ in `538D` CELL 10.”)
- “Is there a **repo hook** for near-threshold?” → *Which notebook/file owns that readout?* (`sports/538D_development.ipynb` **CELL 4D** → `heterogeneity_ventiles_top_tail.png` in D10 bundle — `#08`.)
- “Menger **hook** for overlap?” → *Which companion chapter justifies assortative-but-overlapping pools?* (Selective ecology / matching — `#20260617` calibration doc.)

**Mnemonic:** *Hook = where it **hangs**. Proof = what **holds** it up.*

---

---

*End entry 2026-07-01.*
