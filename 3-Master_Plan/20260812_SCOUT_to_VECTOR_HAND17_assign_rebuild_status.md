# SCOUT → VECTOR: HAND17 / LG ASSIGN rebuild — status handoff

**Date:** 2026-08-12  
**From:** Charles Levine (via COMPASS + SCOUT coding session)  
**To:** VECTOR (theory / manuscript agent)  
**Mission:** Rebuild and validate the **LG (Levine–Gates) ASSIGN phase** for the **HAND17 / PD17** Alex brief — empirical NCAA MBB vs **541 Grandchild** simulation, with honest NCAA–LG input comparability and a clear read on whether LG can reproduce the **Hero inverted-U** on SELECT.

**Charles:** route this to VECTOR as the canonical status since the ASSIGN-rebuild push began (Aug 2026).

---

## Executive summary (three bullets)

1. **ASSIGN layer validated:** ρ moves roster geometry as theory predicts — **global_wss** ↓ and **H_sort** ↑ with ρ; **D** (within-team MSE) ↓ with ρ. These are **partition diagnostics**, not selection outcomes. Homophily alone does **not** produce Hero curvature on SELECT.

2. **Input comparability closed a confound:** Empirical roster caps (exact NCAA roster-size multiset per season), **C** sweep, and **min_minutes** ladder show that fixing league geometry was **necessary for apples-to-apples comparison** but **not sufficient** for inverted-U at baseline **λ ≈ 0.55**.

3. **Hero flip lives in SCORE (λ):** With empirical caps + **K/N** held fixed, LG SELECT is **monotone ↑** for **λ ≤ 1.25** and becomes **inverted-U-like on LOO pool quality** for **λ ≳ 1.5**. Best **peak-bin** match to empirical NCAA (bin **11**) at **λ = 2–3** on 2011–2021 panel. This is the main generative breakthrough of the sprint.

---

## Terminology locks (manuscript / Alex brief)

| Term | Lock |
|------|------|
| **LG** | Alex-facing name for Grandchild sim (repo still `grandchild_*`) |
| **ρ** | Generative ASSIGN homophily knob — not the same as realized sorting |
| **H_sort** | Realized sorting index on a **fixed partition** (diagnostic) |
| **global_wss** | Within-team SS numerator on that partition (monotone mirror of H_sort) |
| **Score ≠ select** | ASSIGN geometry ≠ SELECT curvature; **λ** enters **SCORE** only |
| **S** | **S = A − λ·L_C** (`loo_gap_plus_ability` in code) |
| **K, N, θ** | Per season: **N** = filtered player-seasons; **K** = empirical draft count; top-**K** SELECT league-wide |
| **T_j\*** | Pass B legacy target; **eliminated from LG ASSIGN** — Grandchild uses **endogenous μ_j** (roster mean after ASSIGN). PD17 **T̂_j** remains descriptive on empirical side only. |

Full slide memo: [`re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md`](re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md)

---

## What we built (infrastructure)

### One-command rebuild pipeline

[`sports/scripts/rebuild_hand17_grandchild_diagnostics.sh`](sports/scripts/rebuild_hand17_grandchild_diagnostics.sh) — six diagnostic steps + AUTO slide builders:

| Step | Script | Purpose |
|------|--------|---------|
| 1 | `541_grandchild_rho_sweep.py` | ρ sweep → D, H_sort, global_wss |
| 2 | `grandchild_roster_size_c_sweep.py` | Fixed **C ∈ {10, 11, 15}** SELECT readout |
| 3 | `grandchild_empirical_roster_caps_diagnostic.py` | Exact NCAA roster-size multiset per season |
| 4 | `grandchild_league_interval_diagnostic.py` | Interval overlap (empirical caps, 2011–2021) |
| 5 | `hero_min_minutes_sensitivity_ladder.py` | Empirical **min_minutes** {0, 10, 20} ladder |
| 6 | `grandchild_lambda_select_sweep.py` | **λ sweep on SELECT** (empirical caps held fixed) |

Cheat sheet: [`re_entry/HEROs_and_PASSes/slides/README.txt`](re_entry/HEROs_and_PASSes/slides/README.txt)

### Gallery home (canonical outputs)

All new LG diagnostics write to:

`3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/`

Legacy clutter (`alex_side_by_side_v0`, etc.) removed; Pass A/B exports retargeted to **HEROs_and_PASSes** gallery.

### Bug fixes / rendering

- Matplotlib **`global\_wss`** legend/suptitle escapes fixed in ρ sweep and related builders (use `$\mathrm{global\_wss}$` in math mode).
- λ sweep plot colors: distinct color per λ arm (custom sweeps no longer collapse to one yellow).

---

## Scientific results — by layer

### ASSIGN (ρ, roster geometry)

- **ρ sweep (2015, C=15):** D falls, H_sort rises, global_wss falls — direction correct; D does not → 0 at ρ=1 (expected with C=15 and sequential ASSIGN).
- **Primary Alex validation slide:** **global_wss vs ρ** (not “assortativity = ρ”).
- **Empirical caps:** Matches NCAA **J** (team-season count), roster-size distribution (mean ~9.6, median 11), and **L_C** mean/sd vs fixed **C=15** (~4,140 teams on same **N**).

### Input fixes — negative results (important)

At baseline **λ ≈ 0.55**, SELECT on LOO is **monotone increasing** under:

- Fixed **C = 10, 11, 15**
- Empirical roster caps
- ρ sweep arms (geometry changes, not curvature)

**Manuscript read:** We falsified “LG missed Hero because wrong **C** or wrong team count.” Curvature is not an ASSIGN-only artifact.

Logged for future us: [`sports/documents/Pertinent_Thoughts_Scout.md`](sports/documents/Pertinent_Thoughts_Scout.md) § **LG input fixes vs λ for Hero inverted-U (Aug 2026)**.

### SCORE + SELECT (λ sweep) — **main finding**

Panel: **2011–2021**, **min_minutes=20**, **ρ=0.5**, empirical caps, **K/N** from empirical draft counts.

**Empirical NCAA target (LOO):** inverted-U, peak bin **11**, peak rate **~2.62%**.

**Fine λ grid (Aug 12 run):**

| λ | LOO shape | LOO peak bin | Pool-mean shape |
|---|-----------|--------------|-----------------|
| 1.25 | monotone ↑ | 15 | monotone ↑ |
| **1.5** | **inverted-U** | 13 | monotone ↑ |
| 1.75 | inverted-U | 13 | monotone ↑ |
| **2.0** | **inverted-U** | **11** | monotone ↑ |
| **3.0** | **inverted-U** | **11** | monotone ↑ |
| 4.0 | inverted-U | 12 | monotone ↑ |

**Coarser grid (1, 2, 4, 8, 32):** confirms flip between **λ=1** and **λ=2**; high-λ arms stay inverted-U on LOO; **λ=4** also inverted-U on **pool mean** in that run.

**Mechanism sentence for VECTOR:**

> Low **λ** → SELECT ≈ “draft the best players” → draft rate rises with pool quality. High **λ** → gap penalty **λ·L_C** dominates in elite pools → draft rate falls at the top → **inverted-U on LOO**.

**Caveat:** Pool-mean axis still mostly monotone at λ ≤ 4 in fine grid; empirical NCAA shows inverted-U on **both** axes. Do not over-claim full bivariate Hero match yet.

Meta: `grandchild_assign/GRANDCHILD_lambda_select_sweep_2011_2021_meta.json`  
Figure: `grandchild_assign/GRANDCHILD_lambda_select_sweep_2011_2021.png`

---

## HAND17 deck status

- **Master deck:** `re_entry/HEROs_and_PASSes/slides/CHAR_PD17_HAND.pptx` (expanded to ~22 slides in audit).
- **AUTO companions** in `slides/auto/` — ρ (global_wss + H_sort), empirical caps, C sweep, λ sweep, min_minutes, roster-size distribution.
- **Suggested narrative block for Alex:** empirical Hero → input comparability (caps / roster sizes) → ASSIGN ρ validation → **λ sweep flip** → open items.

**Still open (deck polish, not science blockers):**

- Slide 1 deck map may be stale vs current slide count.
- Some embedded PNGs have mathtext / `\n` title glitches; re-paste from regenerated AUTO slides.
- Paste λ sweep slide into HAND17 after empirical SELECT block (~slide 19).
- Slide 20 subtitle had stray “placeholder” text in audit.

---

## What VECTOR can say now (draft language)

**Conservative (defensible today):**

> On NCAA-comparable inputs (same ability pool, draft counts, and roster-size multiset), the LG simulation reproduces monotone selection at baseline congestion weight but generates an inverted-U on leave-one-out pool quality when the score penalty on local congestion **λ** exceeds ~1.5, with peak-bin alignment near **λ ≈ 2–3**.

**Do not say yet:**

- “We estimated NCAA λ = 2.” (Identification not done.)
- “Homophily ρ creates the Hero.” (Ruled out.)
- “Empirical roster caps create the Hero.” (Ruled out — they enable comparison.)
- “H_sort = ρ.” (Diagnostic vs generative knob.)

**Manuscript nesting suggestion:**

- **§ Empirical (Setting 2):** Hero on LOO locked at min_minutes=20.
- **§ Minimal model:** Three layers ASSIGN → SCORE → SELECT; axis discipline (LOO vs pool mean).
- **§ LG validation:** Input parity → ρ geometry → **λ as curvature knob**; honest gap on pool-mean axis.

---

## Suggested VECTOR next actions

1. **Draft HAND17-facing prose** (1–2 pages) using the table above — especially score≠select and λ threshold.
2. **Update minimal-model / Setting 2 subsection** so ASSIGN claims stop at geometry; Hero claim ties to **λ**.
3. **Flag pool-mean gap** explicitly — either appendix sentence or one targeted λ/axis sentence for Alex.
4. **Cross-check** [`VECTOR_ASSIGN_Grandchild_Model.pptx`](re_entry/HEROs_and_PASSes/slides/VECTOR_ASSIGN_Grandchild_Model.pptx) slides vs endogenous **μ_j** (no **T_j\*** in LG ASSIGN).
5. **Optional:** Request one paragraph from SCOUT on **ρ × λ** interaction if manuscript needs “sorting + congestion” joint story (not run yet).

---

## Key file index

| Item | Path |
|------|------|
| D / H_sort / global_wss memo | `re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md` |
| λ sweep script | `sports/scripts/grandchild_lambda_select_sweep.py` |
| λ meta (fine grid) | `grandchild_assign/GRANDCHILD_lambda_select_sweep_2011_2021_meta.json` |
| λ default sweep archive | `grandchild_assign/GRANDCHILD_lambda_select_sweep_2011_2021_meta_dflt.json` |
| C sweep meta | `grandchild_assign/GRANDCHILD_roster_size_c_sweep_2011_2021_meta.json` |
| Empirical caps meta | `grandchild_assign/GRANDCHILD_empirical_roster_caps_2011_2021_meta.json` |
| ρ sweep | `grandchild_assign/GRANDCHILD_rho_sweep_meta.json` |
| Pertinent Thoughts (λ vs caps) | `sports/documents/Pertinent_Thoughts_Scout.md` |
| HAND17 README | `re_entry/HEROs_and_PASSes/slides/README.txt` |
| Rebuild shell | `sports/scripts/rebuild_hand17_grandchild_diagnostics.sh` |

---

## Still open (science / deck)

- **ρ × λ interaction** — not swept; ρ=0.5 fixed for λ work.
- **Pool-mean Hero match** — may need higher λ or different readout; empirical shows inverted-U on both axes.
- **Levels calibration** — sim top-bin draft rates run high vs NCAA at some λ; shape match ≠ level match.
- **HAND17 final paste + Office Math pass** — Charles-side deck assembly.

---

**Bottom line for VECTOR:** The ASSIGN rebuild succeeded as **validation + confound closure**, not as the Hero mechanism. The stylized inverted-U on LOO is now reproducible in LG via **λ in SCORE**, with a sharp threshold between **1.25 and 1.5** and best bin alignment around **λ = 2–3**. That is the result worth threading into minimal-model prose and the Alex brief.
