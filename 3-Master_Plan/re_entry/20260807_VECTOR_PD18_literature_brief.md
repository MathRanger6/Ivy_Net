# VECTOR brief — PD18 literature search (Aug 7, 2026)

**From:** Charles Levine  
**To:** VECTOR (theory / manuscript / integration)  
**Re:** Assortative **bipartite** network formation with **fixed roster size** — literature scan  
**Time box:** ~weekend; Alex asked for exploration before we commit or revert  
**Meeting source:** `transcripts/20260807_Paper_Directions_18_otter_ai_transcript.docx`  
**Full takeaways:** [`09_PD18_Alex_meeting_takeaways.md`](09_PD18_Alex_meeting_takeaways.md)

---

## 0. Where you left off vs where we are now

You were last deeply involved during the **June 2026 agent rounds** (COMPASS / CODA / SCOUT / PEER / VECTOR markdown mail, Menger companion work, claim-language tables). **Since then (July–Aug 2026)** Charles and COMPASS have been in a **basketball-only re-entry track** — not because Army or tenure were dropped, but because Alex wanted a **clean generative pipeline** and **characterization decks** before Phase C calibration.

**You can skip:** agent mail in `3-Master_Plan/archive/`, the old 14-doc print stack, and notebook `538D` paths unless you want history.

**You should know:** The project still has three domains (Army promotion, MBB draft, tenure), but **this brief is MBB generative ASSIGN only** — the step where synthetic players are seated on teams **before** score and selection.

---

## 1. The dissertation question (one paragraph)

**Empirical stylized fact (Layer A — “hero”):** In real NCAA men’s basketball, draft probability is **not monotone** in individual talent when you bin by **teammate pool quality** — there is an inverted-U / context dependence. Something about **peer environment** matters for **who gets selected**.

**Generative program (Layers B–C):** Build a **transparent fake league** where we control rules, vary one knob at a time (**Phase B characterization**), then **calibrate** knobs to data properties (**Phase C** — not hero-curve sliding).

**Binding pipeline (do not collapse steps):**

```
ASSIGN  →  SCORE  →  SELECT (top K)  →  VISUALIZE (bins / hero readout)
           S_i = A_i − λ·L_C
```

- **Environment** (`L_net = B − D`) ≠ **advancement** (score + select). See [`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md).
- **λ** enters **score**, not the binning scheme alone.
- **ρ** enters **assignment** (who sits with whom), not score.

Plain-English pipeline: [`04_Pass_A_and_Pass_B_in_Plain_English.md`](04_Pass_A_and_Pass_B_in_Plain_English.md).

---

## 2. What we built since June (so the ask makes sense)

### Phase B — fake league characterization (PD15–PD16)

**Deck:** `HEROs_and_PASSes/slides/CHAR_PD16_HAND.pptx` (13 slides after Aug trim)  
**Walkthrough:** [`07_Phase_B_Characterization_Slides_Explained.md`](07_Phase_B_Characterization_Slides_Explained.md)

One-at-a-time knob sweeps on a **synthetic league** (N≈5600, K/N≈10% for gallery default):

| Knob | Layer | What it does |
|------|-------|--------------|
| **ρ** | ASSIGN | Assortativity of soft seating |
| **λ** | SCORE | Congestion weight in **S_i** |
| **θ, γ** | SCORE (L_C kernel) | Viability cutline and sigmoid sharpness |
| **K/N** | SELECT | League selectivity |

**PD16 Alex meeting (Aug 4)** — [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md):

- **L_C** = **team-level** mean σ(γ(A−θ)) on roster (not LOO) — Aug 2026 default.
- **θ** = **F_A⁻¹(1 − K/N)** on ability draw (“naive draft” cutline), not fixed 0.72 preset.
- **ρ** also interpreted as **spread of team L_C** across the league (histogram + T_j vs L_C heatmap).

### Phase PD17 — empirical MBB deck (real rosters)

**Deck:** `HEROs_and_PASSes/slides/CHAR_PD17_HAND.pptx` (7 slides)  
**Cheat sheet:** `HEROs_and_PASSes/slides/README.txt`  
**Regenerate:** `HEROs_and_PASSes/empirical_pd17/REGENERATE.md`

Real panel (2011–2021 MBB, PPM z within season):

1. **Â_i**, **T̂_j** inputs  
2. **Team talent intervals** [min Â, max Â] on each team-season — **overlap** along performance axis  
3. **Team L_C** distribution (γ=0.5 in Charles’s HAND)  
4. **Sketch A:** T̂_j vs L_C  
5. **γ sweep** on empirical L_C  
6. **Slide 7 — ρ calibration capstone:** empirical coverage vs sim soft-assign at varying ρ  

**Slide 7 x-axis (correct readout):** individual **ability** on talent axis; **y** = count of team-seasons (emp) or teams (sim) whose roster interval **covers** that ability level. *Not* team-average T_j on x.

---

## 3. Current assignment mechanism (what we want to simplify)

**Code home:** `sports/tier1_pool_assignment.py` — functions `draw_abilities`, `draw_target_means`, `soft_assign`, `sort_and_chop_assign`.

**Today — soft assign (Pass C / PD17 sim panels):**

1. Draw player abilities **A_i** (e.g. Beta(2,2) on [0,1] for “539 preset”).
2. Draw **one scalar per team** **T_j\*** *before* assignment (i.i.d. Uniform[0,1] in gallery — **synthetic**, not NCAA program talent).
3. Seat each player sequentially: prefer teams whose **T_j\*** is near **A_i**, with sharpness **ρ**.
4. **After** assign: realized **T_j** = mean **A_i** on roster — used descriptively (Sketch A, bins).

**Sort-and-chop benchmark:** sort all **A_i**, chop into equal slices — ignores **T_j\*** entirely; zero between-team overlap; used for γ / λ_crit diagnostics only.

**Alex + Charles (PD18):** **T_j\*** and **ρ** feel **redundant** — both dial how assortative seating looks. Proposal: **drop T_j\* from the assignment rule**; keep **ρ** as the **only** ASSIGN knob; keep **T_j** as **descriptive** post-assignment quantity.

**Critical constraint:** Every team must have the **same roster size** (gallery: 16 × 350 = 5600). Classical network **growth** models often allow unbounded degree — Alex flagged this as the main place the network framing might **break**.

**Fallback:** If no good network/urn model in ~weekend → **revert** to T_j\* + ρ (code **stays** in repo; we do not delete).

---

## 4. What Alex asked us to do (PD18)

> Search for **assortative growth models for bipartite networks**. If thin, start from **unipartite assortative growth**, understand it, and see if there is a natural bipartite extension. **Reframe roster formation** as assortative growth on a **bipartite graph** (players ↔ teams) with **one parameter ρ**.

**Success criterion:** Can we make **“reasonably looking teams”** — especially **realistic interval overlap** along the ability axis (like PD17 slide 3 / 7) — **without** pre-drawn **T_j\***?

**Plan B literature:** **Urn / combinatorial** assortment (balls into bounded bins with sorting weights) — Alex expects this may be math-heavy and **not** from our usual citation-network stack.

**Manuscript upside:** Cleaner assign layer + defensible **networks** vocabulary; later extensions (co-authorship, collaboration graphs, relax strict bipartiteness) without rewriting the whole dissertation frame.

**Menger adjacency:** Your Menger (2024) companion work on assortative matching / tournaments is **conceptually adjacent** (`docs/Menger/`) — PD18 is the **implementation** question for our sim ASSIGN step, not a replacement for those citations.

---

## 5. Literature search — specific asks

### Primary

1. **Bipartite network formation** with **assortative mixing** or **assortative attachment** — edges form so “similar” nodes connect (here: players with similar ability seated into similar roster contexts / teams).
2. Models compatible with **fixed degree on one partition** — each team has exactly **r** slots filled (no unbounded team size).
3. Papers where an **assortativity parameter** (or equivalent) controls overlap / homophily — we will judge rules by **interval coverage curves**, not only degree sequences.

### Secondary (if bipartite is thin)

4. **Unipartite assortative growth** (Holme–Kim, Bianconi–Barabási variants, social signature models, etc.) — note bipartite extensions or finite-size variants.
5. **Configuration-model** or **stub-matching** approaches on bipartite graphs with **prescribed degrees** + **assortative** weighting.

### Plan B

6. **Urn / ball-into-bin** processes with **assortative** or **sorting** constraints and **fixed capacity** per bin.

### Explicitly out of scope for this search

- Fitting the **hero draft curve** directly (that is Phase C / outcome layer).
- **λ, θ, γ** identification (score layer — separate from ASSIGN).
- Army / tenure domains (same math may apply later, but calibrate on MBB first).

---

## 6. Calibration target (why overlap matters)

We are **not** asking for a model that matches raw y-axis counts between empirical (≈6300 team-season peak) and sim (≈1000 team peak) — different counting units.

We **are** asking for a formation rule where:

- **Low ρ** → broad coverage (many teams span each ability level) — like real MBB overlap.  
- **High ρ** → tighter, more disjoint talent windows.  
- **Sort-and-chop** → ~zero overlap (wrong benchmark for NCAA assign).  

**Figure:** `HEROs_and_PASSes/empirical_pd17/EMPIRICAL_rho_coverage_overlay.png`  
**Script:** `sports/scripts/empirical_rho_coverage_overlay.py`

Any proposed assign rule should be evaluable on this **coverage / overlap** readout.

---

## 7. Deliverable shape

**3–5 papers** (more if high quality), each with:

| Field | Content |
|-------|---------|
| **Citation** | Full reference |
| **Formation rule** | Plain English — how edges/nodes arrive |
| **Assortativity knob** | Parameter name and what it controls |
| **Capacity constraint** | Fixed degree? bounded bins? |
| **Bipartite?** | Native bipartite or port from unipartite |
| **Fit to us** | One sentence: players ↔ teams, fixed roster size, ability-labeled player nodes |
| **Risk** | Does bounding break assortativity? (Alex’s main worry) |

Optional: one short paragraph recommending **best candidate** for a weekend prototype or **revert to T_j\***.

---

## 8. Suggested attachments (Charles → VECTOR)

**Minimum (read first):**

| File | Why |
|------|-----|
| **This file** | Self-contained brief |
| [`09_PD18_Alex_meeting_takeaways.md`](09_PD18_Alex_meeting_takeaways.md) | Alex quotes + park/revert rules |
| [`04_Pass_A_and_Pass_B_in_Plain_English.md`](04_Pass_A_and_Pass_B_in_Plain_English.md) | ASSIGN / SCORE / SELECT in sentences |
| [`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md) | Environment ≠ advancement; score ≠ select |

**Context (skim as needed):**

| File | Why |
|------|-----|
| [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md) | Team L_C, θ(K/N), ρ as L_C spread — Aug 4 |
| [`07_Phase_B_Characterization_Slides_Explained.md`](07_Phase_B_Characterization_Slides_Explained.md) | T_j\* glossary (legacy if PD18 wins) |
| `transcripts/PD18_notes.md` | Short working digest |
| `HEROs_and_PASSes/slides/README.txt` | HAND16 vs HAND17 deck map |

**Code (reference — not required to run):**

| File | Why |
|------|-----|
| `sports/tier1_pool_assignment.py` | Current `soft_assign`, `draw_target_means` — **park, do not delete** |
| `sports/scripts/empirical_rho_coverage_overlay.py` | Slide 7 calibration figure |
| `sports/scripts/empirical_team_interval_overlap.py` | Empirical interval overlap (slide 3 logic) |

**Figures (optional PNG attach):**

| File | Why |
|------|-----|
| `HEROs_and_PASSes/empirical_pd17/EMPIRICAL_team_interval_overlap.png` | Real roster overlap |
| `HEROs_and_PASSes/empirical_pd17/EMPIRICAL_rho_coverage_overlay.png` | Slide 7 — emp vs sim ρ |

**Menger (optional — you know this terrain):**

| File | Why |
|------|-----|
| `docs/Menger/Complete_Companion.pdf` or outline summary | Assortative matching bridge already in project voice |

---

## 9. Symbols quick reference

| Symbol | Meaning |
|--------|---------|
| **A_i** | Latent player ability (sim draw or empirical Â_i) |
| **T_j\*** | **PARK (PD18)** — pre-drawn team target for soft assign; synthetic |
| **T_j** | **KEEP** — realized mean A_i on team j after assign (descriptive) |
| **T_jt** | Empirical team-season roster mean of Â_i |
| **ρ** | Assignment assortativity — **candidate sole ASSIGN knob** |
| **λ** | Score congestion weight in S_i = A_i − λ L_C |
| **θ, γ** | Viability cutline and sigmoid sharpness inside L_C |
| **L_C** | Team mean σ(γ(A−θ)) on roster (team smooth, Aug 2026 default) |

---

## 10. Questions back to Charles / COMPASS

If literature is ambiguous, VECTOR may ask:

1. Is **sequential** seating (one player at a time) required, or is **one-shot** stub matching OK?  
2. Must **every** team fill exactly **r** slots, or can we allow empty seats with rejection?  
3. Is **ability-only** assortativity enough, or do we need **latent team “quality”** nodes on the team side of the bipartite graph?

---

*End brief — thank you for picking this up cold.*
