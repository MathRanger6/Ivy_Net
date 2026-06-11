# Tier 1 pre-sorting design note — pools, overlap, and calibration

**Print date:** 2026-06-08 (rev 2)  
**Purpose:** Take-home reference for Alex / PD11 team-building and the Wang-style empirical ladder.  
**Sources:** Paper Directions 11 transcript (`transcripts/20260515_Paper_Directions_11_otter_ai_transcript.pdf`), `Alex_Tier1_Sequential_Model_Outline.md` §6A, `530_sports_pipeline.ipynb` **CELLs 5–9**.

---

## 1. Two layers (do not merge)

| Layer | Question | Where it lives |
|-------|----------|----------------|
| **Empirical (realized pools)** | Given actual rosters, what is LOO pool quality \(Q\), dispersion, draft rate, \(L^*\)? | **`538_alex_tier1_model_and_fit.ipynb`** — bins → LPM → logit on `(team_id, season)` from the panel. |
| **Generative (assignment rules)** | How *should* we put people in pools so overlap and mean–SD patterns look plausible before we simulate promotion? | **`538` / `538D` CELL 10–12** + `tier1_pool_assignment.py` + `tier1_sim_config.py` (**implemented** June 2026). **`537` stays frozen** as the legacy sort-and-chop + Cell 10 playground lab. |
| **Forensics (what real data look like)** | Do team talent windows overlap? Mean vs within-team SD? | **`530` CELLs 5–9** on basketball panel (PPM, within-season z). |

**538 does not re-sort the panel.** It measures pools the world already formed. The **new approach** is: (1) use 530 to set **targets** for a generative assigner; (2) implement that assigner in **538** (or a small module `sports/tier1_pool_assignment.py` called from 538); (3) keep **537** unchanged for historical comparison.

---

## 2. What the 530 forensics show (basketball, ~82,893 player-seasons)

### 2.1 Team means and roster SD (CELL 5)

- **Per (team_id, season):** ~6,550 intervals; mean roster perf median ≈ **0.01** (z); roster SD median ≈ **0.80** (z).
- **Per team (career average):** ~1,140 teams; mean perf tighter around 0; average SD median ≈ **0.95**.
- **Takeaway:** Typical team-season has within-roster spread of ~**0.8–1.0 z**; not a point mass.

### 2.2 Mean vs heterogeneity (CELL 6 all teams; CELL 7 draftee-only)

- **All teams:** Pearson \(r\) (mean, SD) ≈ **0.26** (positive); OLS slope ≈ **0.38** — higher-mean rosters tend to be *slightly more* dispersed, not more homogeneous.
- **Draftee teams (season filter):** weaker linear link; binned curve often **flat then up** at high mean — do **not** assume “elite team = tight roster.”
- **Takeaway:** Generative model should **not** hard-code “high \(T_j\) ⇒ low within-pool SD.” Calibrate span separately or let it emerge from \(\tau\), roster size, and tails.

### 2.3 Interval overlap (CELL 8 all teams; CELL 9 draftee-only)

- **Coverage** = number of team-seasons whose [min, max] perf interval covers a point on the perf axis.
- **Actual rosters:** peak coverage **thousands** at z ≈ 0 (e.g. ~6,500 all-team; ~677 draftee-only) — massive **overlap**.
- **Disjoint sort-and-chop** (sort all players, equal-count slices): coverage ≈ **1** everywhere — **no overlap** (red dashed line in CELL 8).
- **Takeaway:** The old simulation assignment (537 **Assortative** = sort + chop) matches the **red** curve, not the **blue** curve. Overlap is the empirical fact to reproduce.

---

## 3. What Paper Directions 11 asked for (three threads)

| Thread | Idea | Alex’s coding order |
|--------|------|---------------------|
| **A — Pre-sorting** | Draw team/pool **target mean** \(T_j\); assign players with **soft** probabilities (not hard slices); many pools (\(J \gg\) bins). | **After** quick win on C, unless overlap is the main blocker. |
| **B — Mean × SD in data** | Heatmap: LOO mean \(Q\) × LOO peer SD → draft rate. | **538** CELL 4B/4C (done on **real** pools). |
| **C — Promotion score** | Use **gap to pool mean** \(A_i - \bar A_{\text{pool}}\), not rank-only. | Easiest tweak in **537** widgets (`loo_gap_plus_ability` in Cell 10). |

**Alex:** Question **rules** (assignment, promotion), not endless parameter grids.

---

## 4. Recommended generative assignment (Thread A)

### 4.1 Core algorithm — target means + soft matching

**Step 0 — Abilities**  
Draw \(A_i\) (e.g. clipped normal on [0,1] or z-scored scale). Optional: \(A_i = A_i^{\text{base}} + \varepsilon_i\) with **heavy-tailed** \(\varepsilon\) (Student-\(t\)) for rare superstar / bust draws.

**Step 1 — Team targets**  
For \(j = 1,\ldots,J\) teams, with **\(J \gg\)** number of EDA bins (e.g. 50 teams, 8–20 bins):

- \(T_j \sim \mathrm{Uniform}(a, b)\), or  
- \(T_j \sim \mathcal{N}(\mu_T, \sigma_T^2)\) clipped to \([a,b]\).

**Step 2 — Soft assignment (overlap by construction)**  
\[
\pi_{ij} \propto \exp\left(-\frac{(A_i - T_j)^2}{2\tau^2}\right)
\]
or Cauchy kernel for fatter assignment tails. Sample \(j \sim \pi_{i\cdot}\) once per player (or use deterministic argmax + noise).

- **Small \(\tau\)** → more assortative, still overlapping if many \(T_j\) are close.  
- **Large \(\tau\)** → more mixing, more overlap.

**Why it works:** Teams with nearby \(T_j\) compete for the same \(A_i\); realized [min, max] intervals **cross** on the perf axis → coverage \(\gg 1\).

### 4.2 Rich-get-richer (optional second knob)

Sequential: when placing player \(i\),
\[
\pi_{ij} \propto (n_j + k)^\alpha \cdot \exp\left(-\frac{(A_i - T_j)^2}{2\tau^2}\right)
\]
Anchor on **fixed** \(T_j\), not drifting roster mean, or elite teams absorb everyone.

### 4.3 What **not** to use as the main story

| Mechanism | Problem |
|-----------|---------|
| Global **sort + equal slices** (537 choice B) | Disjoint intervals; coverage ≈ 1. |
| ε on sort signal only | Rearranges order but keeps near-partition structure. |
| Copy **empirical college team means** into \(T_j\) | Alex: bad for cross-domain minimal model (530 OK for **ranges** only). |

### 4.4 ε vs heavy tails

| Use | Role |
|-----|------|
| Heavy tail on **\(A_i\)** draw | Occasional “wrong-level” talent before assignment. |
| Noise in **\(\pi_{ij}\)** or large \(\tau\) | Everyday overlap across teams. |
| Sort + ε + chop | Still mimics **disjoint** benchmark in CELL 8. |

---

## 5. Calibration checklist (match 530 before trusting 538 sim)

Run the same diagnostics on **simulated** rosters as **530 CELLs 5–8**:

1. **Coverage curve** — simulated blue band should sit above 1 in the middle of the perf axis; not flat at 1.  
2. **Max coverage** and **% grid points with coverage > 1**.  
3. **Span histogram** — median roster span ~0.8–1.0 z (if using z-scored perf).  
4. **Mean vs SD scatter** and 12-bin curve — weak positive or flat OK; don’t force negative slope.  
5. **\(J \gg\)** bins used in 538/530 ventiles.

**Tune in `tier1_sim_config.py`:** `ASSIGNMENT_TEMPERATURE`, `TARGET_MEAN_SPREAD`, `N_TEAMS`, `ROSTER_SIZE`, tail df, optional `PREFERENTIAL_ALPHA`.

---

## 6. Promotion score (Thread C) — still relevant after pools fix

Conceptual move from rank-only:
\[
\text{score}_i = w\,(A_i - \bar A_{\text{pool}}) + (1-w)\,A_i
\]
(algebraically related forms in transcript). **537 Cell 10** already exposes `w·(A_i−LOO pool q)+(1-w)·A_i` for experiments on the **old** pool builder. **538** empirical ladder can add \(A\) and interactions in CELL 7+ without changing how pools form.

---

## 7. Notebook & config map (print this page)

```
530  — Forensics on REAL panel (CELL 5–9)
       CELL 5: mean & SD histograms
       CELL 6: mean vs SD scatter / hex / bins / 3D counts
       CELL 7: same, draftee teams only
       CELL 8: interval overlap vs sort-and-chop
       CELL 9: interval overlap, draftee teams only

537  — FROZEN legacy simulation lab
       sim_config.py + Cell 10 widgets (authoritative for 537)
       assign_pool_ids: sort + chop (A/B/C)

538 / 538D — Alex empirical ladder (REAL pools) + generative lab (June 2026)
       CELLs 0–6: perf, LOO Q, bins, LPM, logit, L*
       CELL 4B/4C: mean Q × peer SD (PD11-B); 4D heterogeneity (wired, parked)
       CELL 10–12: soft assign + congestion score A−w·L_C; Plot A overlap + Plot B
       tier1_sim_config.py + 538_Cell10_Generative_Manual.md
       SHOW_PLOT_B_TEAM_MEAN: L_Q (530) vs team_mean (539-style)
```

---

## 8. One-sentence design spec

> Draw **team target means** \(T_j\) from a broad distribution; assign players with **soft probabilities** \(\propto f(A_i - T_j)\); optional mild preferential attachment and heavy-tailed ability draws; **calibrate** \(\tau\), \(J\), and roster size so **interval overlap** and **span / mean–SD** patterns match **530**, not sort-and-chop.

---

## 9. Suggested next steps (ordered) — updated June 2026

1. [x] **538 / 538D:** `tier1_pool_assignment.py` + CELL 10–12 generative playground.  
2. [x] Replay **530-style** coverage (Plot A) on simulated rosters; calibrate τ≈0.65.  
3. [x] Congestion selection score \(A - w L_C\) with `crowding_smooth` + scale fix for z-scored ability.  
4. [ ] **Open:** Match empirical **inverted-U on \(L_Q\)** LOO axis (Plot B with `SHOW_PLOT_B_TEAM_MEAN=False`) — may need assignment noise, threshold rule, or extra terms.  
5. [ ] **538:** finish empirical ladder (CELL 7 inference / robustness) on real pools.  
6. [ ] **4D:** return to top-tail heterogeneity narrative when scaffolding is ready.  
7. [x] Update `Alex_Tier1` §10 table (2026-06-08).

---

## 10. Key file paths

| File | Role |
|------|------|
| `sports/documents/Tier1_Presorting_Design_Note.md` | This document |
| `sports/documents/538_Cell10_Generative_Manual.md` | **CELL 10 widget glossary** (operator manual) |
| `sports/tier1_sim_config.py` | Generative assignment defaults for **538** (not 537) |
| `sports/sim_config.py` | **537 only** — run gates, Cell 10 default snapshot |
| `sports/cell10_knob_catalog.py` | 537 widget labels / sweep titles |
| `1-Various_PDE_and_Chat_stuff/5-Manuscript/Alex_Tier1_Sequential_Model_Outline.md` | Advisor spine + §10 cell map |

---

*End of design note.*
