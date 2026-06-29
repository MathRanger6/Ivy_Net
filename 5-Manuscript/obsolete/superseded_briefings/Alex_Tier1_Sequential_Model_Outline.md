# Alex — Tier 1 sequential model outline

## Role of this document

This note is the **advisor-ordered spine**: each section follows the sequence Alex emphasized (minimal model → assumptions → data → fitting → what we extract). It **does not replace** existing work; it points to it.

**Paper Directions 11 (pool pre-sorting & promotion rules)** is **§6A** — separate from the **538** empirical ladder (§4–§6). Read §6A before treating **538** as addressing “how teams are built.” **Printable design note:** `sports/documents/Tier1_Presorting_Design_Note.md`.

**Stable references (do not fork their content here):**

- `Tier1_Briefing_Outline.md` — full technical detail, equations, and data column map.
- `Tier1_Narrative_Outline.md` — narrative arc and voice.
- `sports/documents/tier_1_roadmap.md` — execution contract for `535` / panel columns.
- **`sports/538_alex_tier1_model_and_fit.ipynb`** — notebook that should **mirror this section order** for code + outputs (`537` stays the simulation lab). **Cell-level map: §10 below** (update when 538 changes).
- **`sports/documents/tier_1_roadmap.md`** — **535 execution contract** (pipeline steps, `df` columns, CELL 0 switches for **`535_sports_tier_1.ipynb`**). Not superseded by 538; 538 reuses the same pipeline modules with a slimmer cell ladder.
- **Wang-style cross-domain template** (same *logical* steps as this outline): `Vector_Questions_and_Modeling_Thoughts.md` §11; mechanics of the Yin–Wang failure/success paper: `wang_paper_model.md`.

---

## 1. Unit of modeling

- State the primary unit \((i,j,t)\) and the empirical row (player–season / player–team–season).
- One sentence: local pool vs global advancement.

*Fill from `Tier1_Briefing_Outline.md` §1; keep only what you will say aloud.*

---

## 2. Minimal model objects (headline only)

- Outcome \(Y\) (global advancement).
- Amalgamated local environment \(L_{ijt}\) (Tier 1 object); first proxy \(Q\).
- Global selection capacity \(\Lambda_t\).
- Role of own performance / ability proxy \(A_{ijt}\) (baseline, not the mechanism headline).

*Detail table: `Tier1_Briefing_Outline.md` §2–§3.*

---

## 3. Minimal assumptions

- Local vs global scarcity framing.
- Leave-self-out for peer-based \(Q\).
- Variable domains (binary \(Y\), standardized \(L\) for fitting, etc.).
- What Tier 1 **defers** (sorting, dynamics, full causal ID). **How pools are *formed*** is the PD11 generative agenda — see **§6A**; §4–§6 **take pools as given** in the data.

*Bullets only here; expand in manuscript later.*

---

## 4. Map model to data

One table: object → meaning → `df` column / construction step (`530` / panel load + Tier 1 cols).

*Canonical table: `Tier1_Briefing_Outline.md` §4.*

**In `538`:** **CELL 1** (`CFG`, panel path) → **CELL 2** (`load_panel`, `apply_perf_metric_for_analysis`, legacy `poolq_loo`) → **CELL 3** (`add_tier1_mechanism_variables`, `ALEX_L_COL` from `PRIMARY_POOL_MODE`).

---

## 5. Primary estimand

- **Main object to report:** turning point \(L^*\) (or \(Q^*\) in raw units), not only linear coefficients.
- One sentence on why (competing margins / inverted-U readout).

*Formulas: `Tier1_Briefing_Outline.md` §7.*

---

## 6. Fitting plan (ordered)

1. Descriptive bins (no model). → **`538` CELL 4** (table), **CELL 4A** (binned line; optional if CELL 5 overlay is enough).
2. Transparent quadratic spec in \(L\) (LPM) + controls as needed. → **`538` CELL 5** (OLS on z-scored \(L\), \(L^2\), \(A\); binned means + fitted curve).
3. Binary response (logit/probit) for the same index structure. → **`538` CELL 6** (logit; same index; \(L^*\) from linear part).
4. Robustness: FE, clustering, alternative \(L\) proxy, one decomposition term at a time. → **`538` CELL 7+** (placeholder).

**Exploratory (not Alex §6 step 1; from Paper Directions 11 meeting):** mean peer \(Q\) × LOO peer perf **SD** vs draft. → **`538` CELL 4B** (hexbin + Q histogram), **CELL 4C** (3D surface; optional). Always uses `congestion_quality` on *x* even when `PRIMARY_POOL_MODE='crowding'`.

*Expand: `Tier1_Briefing_Outline.md` §5–§6.*

---

## 6A. Paper Directions 11 — pool formation, promotion rules, and where they live

**Source:** `transcripts/20260515_Paper_Directions_11_otter_ai_transcript.pdf` (2026-05-15).  
**Do not confuse with §6:** §6 is the **Wang-style empirical ladder** on **realized** pools. PD11 is about **questioning the rules** that put people in pools and that turn pool context into promotion — especially **pre-sorting / team building** in a **generative** layer (**implemented** in **`538` / `538D` CELL 10–12** + `tier1_pool_assignment.py`; **`537` frozen**), not re-running more parameter grids.

### What PD11 is *not* asking for (here)

- Replacing §6 with new bins/LPM/logit specs alone.
- Calibrating the generative model by **copying observed college team means** — Alex: misleading for a **multi-domain** minimal story (forensic checks on overlap/inequality across domains are fine).
- Treating **538** generative as **finished science** — assignment + congestion score are **implemented** (June 2026), but **L_Q-axis inverted-U match to 530** is still open (see **Where each thread lives** and `Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md`).

### Three threads (meeting order of emphasis)

| # | Thread | Question | Priority in code |
|---|--------|----------|------------------|
| **A** | **Pre-sorting / how teams (pools) are built** | How do we **assign** individuals to local pools so pools **overlap** in talent, are not rigidly ordered slices, and **# pools ≫ # quantile bins**? | **`538` / `538D` CELL 10–12** + `tier1_pool_assignment.py` + `tier1_sim_config.py` (**live**). **`537` frozen** (legacy sort-and-chop). Forensics: **`530` CELL 8–9.** |
| **B** | **Pool mean × pool dispersion** | Does advancement depend on LOO **mean** peer ability *and* LOO **SD** of peer ability (crowding vs distinction)? | **`538` CELL 4B, 4C** (exploratory EDA). Columns: `congestion_quality`, `peer_perf_sd_loo` (`tier1_mechanism_vars.py`). |
| **C** | **Promotion score vs local rank** | Should promotion weight **gap to pool mean** (\(A_i - \bar A_{\text{pool}}\)) rather than **rank within pool** (same rank whether peers are tight or spread)? | **`537`** first — e.g. `ADDITIVE_LOCAL_RANK_WEIGHT` / score mode in `sim_config.py`, Cell 10 playground. **Then** revisit **A** if shape does not move. |

**Alex’s implementation order (transcript):** tweak **C** in existing simulation machinery first (easy); if insufficient, rebuild **A**; use **B** in data to see whether dispersion belongs in the story.

### Thread A — pre-sorting (generative pool assignment)

**Problem with the old rule (still in `537` for assortative pools):**

1. Draw abilities for all \(i\).
2. Sort (optionally add Gaussian ε to a **sorting signal**).
3. **Chop** the sorted list into \(J\) equal-sized pools → **hard, ordered** teams with little realistic overlap.

**Critique (PD11):** teams look like **non-overlapping talent intervals**; ε-smearing is **too linear** for **heavy tails** (elite player on weak team occasionally); **# teams must be much larger than # quantile bins** used in EDA.

**Directions discussed (generative — pick one family to prototype in `538`):**

1. **Target means, then soft assignment (preferred framing)**  
   - Draw a **target mean ability** \(T_j\) for each pool \(j\) (e.g. \(J\) draws from Uniform\([0,1]\) or another spread).  
   - Assign \(i\) with ability \(\alpha_i\) to pool \(j\) with probability **↑ as \(\alpha_i\) is close to \(T_j\)** (Gaussian kernel around \(T_j\), or heavier tail).  
   - Yields **overlapping “talent windows”** across pools — some tight, some spread out.

2. **Sequential / preferential assignment**  
   - Start with even assignment probabilities; **update** as pools fill (Barabási-style “rich get richer”) — another way to avoid rigid slices.

3. **Heavy-tailed reassignment noise**  
   - Charles: ε from a **heavy-tailed** distribution so elites occasionally land in weak pools but usually sort high — closer to rare “superstar on weak program” events.

**Assortativity knob:** width of the assignment kernel (or attachment strength) controls how **assortative** mixing is — still need many pools vs few bins.

**Empirical basketball:** pools are **observed** `(team_id, season)` after real sorting (recruiting, transfers, minutes). §4–§6 **measure** LOO \(Q\) and peer SD **within** that realization; they **do not** re-simulate assignment.

### Thread B — mean × SD (empirical diagnostic)

- **x:** LOO mean peer performance → `congestion_quality` (same object as primary \(Q\) / `ALEX_L_COL` when `PRIMARY_POOL_MODE='quality'`).
- **y:** LOO sample SD of teammate `perf` → `peer_perf_sd_loo`.
- **Color / z:** mean `Y_draft` (or promotion rate in other domains).

**Hypothesis (talking point):** low peer SD → **crowding** → stronger inverted-U; high peer SD → easier **distinction** → weaker crowding read. **Ranking alone drops SD information** — motivates B alongside mean-only \(Q\).

**538 note:** 4B/4C fix **x** to `congestion_quality` even when `PRIMARY_POOL_MODE='crowding'` (crowding toggle affects §6 ladder cells, not this PD11 plot).

### Thread C — promotion rule (simulation)

**Old composite (conceptual):** \(w \cdot \text{local\_rank} + (1-w)\cdot A_i\).

**PD11 push:** weight should reflect **how much better than the pool mean**, not “#1 in pool” regardless of spread — e.g. terms involving \(A_i - \bar A_{\text{pool}}\) (discussion: \(w(A_i - \bar A_{\text{pool}}) + (1-w)A_i\) and algebraically related forms). Map to **`537`** score / weight construction before investing in **A**.

**Separate exploratory idea (later):** promotion may depend on **own ability × pool context** (high/mid/low \(A\) strata do not add up to the aggregate U-shape) — not the same as **A**, but related to interaction terms in the outcome model, not pool construction per se.

### Where each thread lives (do not merge notebooks)

| Layer | Pools | PD11 threads |
|-------|--------|----------------|
| **`538` / `538D`** | **Empirical:** fixed panel (`team_id`, `season`). **Generative (June 2026):** soft τ≈0.65 assignment + congestion score \(A - w L_C\); Plot B axis toggle (`SHOW_PLOT_B_TEAM_MEAN`) | **B** (4B/4C) + §6 ladder; **A** (CELL 10–12); **4D** heterogeneity wired, narrative parked |
| **`537`** | **Frozen** legacy sim — sort-and-chop + Cell 10 widgets | **C** (promotion score); compare old assignment only |
| **`530` CELL 5–9** | Real panel forensics | Mean/SD histograms, mean×SD, interval overlap |
| **`535` / `tier_1_roadmap.md`** | Pipeline + heavy EDA on same realized pools | Mechanism columns; not generative reassignment |

**Config files:** `sports/sim_config.py` = **537 only**. `sports/tier1_sim_config.py` = generative defaults for **538**. Design note: `sports/documents/Tier1_Presorting_Design_Note.md`.

**`537` anchors (legacy, do not extend for Thread A):** `assign_pool_ids`, `sorting_signal_for_pools`, `SORTING_NOISE_SD`; Cell 10 (`cell10_playground_run.py`, `cell10_knob_catalog.py`, `sim_config.py`).

### How §6A relates to §7 and §9

- **§6 / `538`:** minimal **reduced form** on **realized** pools (Wang replay) — still required for Alex conversations and cross-domain comparability.
- **§6A / `538` (generative):** new **assignment rules** calibrated via **`530`**; **`537`** unchanged for comparison.
- **§9:** cross-domain program keeps the **same §6 ladder** per domain; **§6A** is the shared **assignment + promotion rulebook** to align Army / academia / sports simulations before claiming universality.

---

## 7. Where simulation fits (`537` vs `538`)

- **`538` (empirical):** §4–§6 ladder on **real** `(team_id, season)` pools — primary Alex deliverable.
- **`538` / `538D` (generative, June 2026):** soft assignment + **congestion-adjusted selection** + Plot A/B; **539 selection** preset imports score + [0,1] scales (not full 539 DGP). Open: inverted-U on **\(L_Q\)** LOO axis vs empirical 530. Knobs: `tier1_sim_config.py`, `538_Cell10_Generative_Manual.md`.
- **`537` (frozen):** legacy sort-and-chop lab + Cell 10 widgets; use only to compare **old** assignment or to try **promotion-score** (Thread C) tweaks via `sim_config.py`.
- **`530` CELL 5–9:** forensic targets for calibrating generative assignment (not simulation).

---

## 8. Deliverables for the next conversation

- This outline filled in at **talking-point** depth (sub-bullets, not dissertation length).
- Matching cells in **`538_alex_tier1_model_and_fit.ipynb`** so figures/tables follow sections 4–6.

---

## 9. Wang-style program — same skeleton, many domains

Alex’s sequence is how you **lock a minimal empirical model** in one domain. The Wang-line aspiration in your notes is: **(i)** a stable empirical shape, **(ii)** a **small** generative story, **(iii)** extra **testable** predictions, **(iv)** replay in other domains.

**Keep constant across domains (the “minimal model that does the trick”):**

| Layer | What stays the same | What changes per domain |
|------|---------------------|-------------------------|
| **Unit** | Individual (or role-holder) embedded in a **local pool** at time \(t\); outcome is **globally** scarce. | Definition of pool (team, unit, department) and calendar. |
| **Objects** | \(Y\), amalgamated \(L\) (peer/rivalry proxy), \(\Lambda_t\), baseline \(A\). | How you **measure** \(L\), \(Y\), \(\Lambda\) from logs. |
| **Estimand** | Turning point \(L^*\) (or equivalent in z-score then mapped back). | Binning / windowing rules; institutional noise. |
| **Fitting ladder** | Bins → quadratic in \(L\) (LPM) → logit/probit → one decomposition at a time. | FE structure (season vs fiscal year vs cohort). |

**How you *find* minimality (not wish it):**

1. **Start with the briefing’s Tier 1 spec** — one \(L\) proxy, \(L + L^2 + A\), report \(L^*\). That *is* the candidate minimal reduced form.
2. **Add complexity only on forensic rules:** e.g. crowding or minutes enters only if (a) theory says the shape should move with that margin *and* (b) the data move that way, or the minimal spec is badly misspecified in a pre-registered sense. Your “one diagnostic at a time” rule is the operational version of minimality.
3. **Use `537` for Wang-style *comparative statics*** without bloating the empirical notebook: e.g. shift effective \(\Lambda\), concentration, or opportunity; check whether \(L^*\) / top-bin behavior moves in the direction `Vector_Questions` lists (shift of peak, stronger top decline under congestion). That ties “simple mechanism” to **extra predictions**, not only the inverted-U picture.
4. **Per new domain:** copy the **same section headings** (this doc §1–§6) into a short domain addendum or notebook; replace §4’s table with that domain’s column mapping; rerun the ladder. The **abstract** story should read almost unchanged; only the measurement bridge changes.

**Honest scope:** “All domains” is **parallel replay of the same checklist**, not one pooled mega-regression on day one. The Wang papers earn universality by showing the **same qualitative mechanism** with domain-specific codings; your Alex outline is the contract for what must match across those codings.

---

## 10. `538` implementation map (keep in sync with notebook)

**Notebook:** `sports/538_alex_tier1_model_and_fit.ipynb`  
**Switchboard:** **CELL 0** (`RUN_CELL*`, `PERF_METRIC`, `PRIMARY_POOL_MODE`, `COMPUTE_WEIGHTED_CROWDING`, …).

| Outline § | Step / object | `538` cells | Notes |
|-----------|---------------|-------------|--------|
| §4 | Data map | **0** → **1** → **2** → **3** | Same pipeline as `535` cells 1–3; no heavy 535 CELL 4 EDA. |
| §6.1 | Descriptive bins | **4**, **4A** | **4** = table; **4A** = binned draft rate vs mean \(L\) in bin. |
| §6A (PD11-B) | Q × peer SD diagnostic | **4B**, **4C** | Associational; see **§6A**. Gated by `RUN_CELL4B`. |
| §6.2 | Quadratic LPM + \(L^*\) | **5** | Overlay: binned means + fitted LPM (\(\tilde A=0\)). |
| §6.3 | Logit + \(L^*\) | **6** | Same z-scores as **5**; needs `statsmodels`. |
| §6.4 | Inference / robustness | **7+** | Not implemented yet. |
| §6A (PD11-A) | Generative pool assignment + selection | **`538` / `538D` CELL 10–12** + `tier1_pool_assignment.py` | Calibrate Plot A to **530** CELL 8–9; congestion score + axis toggle per June Scout update. |
| §6A (PD11-C) | Promotion score experiments | **`537`** Cell 10, `sim_config.py` | Legacy only; optional compare to 538. |
| §7 | Forensics / legacy sim | **530** CELL 5–9; **`537`** frozen | Empirical ladder in **538** §4–§6. |

**When you add or rename a `538` cell:** update this table and the **§6** bullets above.

---

## What this document is *not*

- **Not “PD11 = only the heatmap.”** PD11’s **center of gravity** is **pre-sorting / pool construction** (**§6A thread A**, **CELL 10–12** in **`538` / `538D`**; **`537` frozen**). The **Q × peer SD** block (**4B** / **4C**, **§6A thread B**) is one empirical check; **promotion vs rank** (**§6A thread C**) can still be probed in **537** Cell 10.
- **Not “generative replicates 530 bin-for-bin.”** Empirical §6 uses **realized** pools; generative **CELL 10** produces inverted-U vs **team_mean** (539-style) more readily than vs **\(L_Q\)** LOO — see June Scout status doc.
- **Not the same as `tier_1_roadmap.md`.** That file is the **living checklist for `535`** (pipeline contract, `df` columns, 535 CELL 0). **538** follows *this* outline §4–§6; the roadmap *links* here but still centers **535** for mechanism EDA and exports.
- **Spine for Alex meetings:** §1–§6 + §10 (**538** empirical). **Generative rulebook:** **§6A** + `Tier1_Presorting_Design_Note.md` + `tier1_sim_config.py` (**538**, when coded). **Legacy sim:** **537** only.

---

## Changelog

| Date | Note |
|------|------|
| 2026-05-18 | `Tier1_Presorting_Design_Note.md`; `tier1_sim_config.py`; generative → **538**, **537** frozen; `sim_config` 537-only. |
| 2026-05-18 | **§6A:** PD11 pool formation, promotion rules, 538 vs 537 split; §3/§7/§10/“What this is not” cross-refs. |
| 2026-05-18 | §10: `538` cell map; §4/§6 cross-refs; clarify vs `tier_1_roadmap` and Paper Directions 11. |
| 2026-05-12 | §9: Wang-style cross-domain program — same skeleton, measurement bridge per domain; `537` for comparative statics. |
| 2026-06-08 | §6A/§7/§10: generative **implemented** (CELL 10–12, congestion score, `SHOW_PLOT_B_TEAM_MEAN`); 538D parallel lab; L_Q match still open. |
| 2026-05-12 | Initial skeleton: Alex-sequenced spine; links to existing briefing + new `538` notebook. |
