# COMPASS → SCOUT — P2b knee overlay: data aperture after last-ps lock

**Date:** 2026-08-27  
**From:** COMPASS (Charles + Alex debrief)  
**To:** SCOUT  
**Status:** **Action requested** — Charles will discuss options with SCOUT  
**Related:** [`CCT_Campaign_Plan.md`](CCT_Campaign_Plan.md) · [`../_DISPOSABLE_CCT_P2b_workflow_thread.md`](../_DISPOSABLE_CCT_P2b_workflow_thread.md) · `population_sandbox/fhero/`

---

## One sentence

We believe the **congestion conditional (CCT) / F-HERO knee** is real (Army analogue), but **last-ps + 2013–2021** leaves only **424 draftees** — thin bins and misaligned overlay reads are now the bottleneck, not the scientific direction.

---

## What we locked (NEW FIXED population)

| Knob | Value |
|------|--------|
| Seasons | **2013–2021** |
| Panel rows | **last-ps** (one row per athlete, final college season) |
| Y | **ever-draft** |
| Filters | min20 · mg10 · winsor 0.01–0.99 · ALLT |
| F-HERO axis | Fix **Â** band → draft rate vs **T̂_j** (piecewise 4+7 bins) |

**Panel:** n = **16,836** athletes · **K = 424** drafts (≈2.5%).

---

## Why last-ps (and why K dropped)

| Spec | n (panel) | Drafts (K) | Notes |
|------|-----------|------------|--------|
| Old deck: 11–21 · +DFT · **all-ps** | 17,659 PS | **1,133** | Multiple seasons per draftee counted |
| Same window · **last-ps** | 7,864 | **520** | One row per draftee |
| **NEW: 13–21 · last-ps** | 16,836 | **424** | −62% vs old K; mostly **last-ps**, not +DFT vs ALLT |

**+DFT vs ALLT does not change K** on the same row mode (424 = 424). The drop is **last-ps** (correct estimand) + **2013–2021** trim.

Charles and Alex agree: **last-ps is the right move** for “who gets drafted from this talent level.” The cost is **statistical power**.

---

## Scientific read (unchanged)

1. **Fix Â, sweep T̂_j** — correct design for the nuanced congestion read (matches Army conditional).
2. **Shape is visible** on single-band F-HERO (top ~5–7% Â): plateau → downturn in elite T̂_j tail.
3. **Overlay across draft-mass tiers** is the Alex board object — compare knees across three **equal ~30% draft-mass** Â slices.
4. **Problem today:** per-tier **within-band median 4+7 binning** put dots at different T̂_j x positions; Alex asked for **aligned bins**. Even with aligned bins, many cells are **n < 30** (hollow markers, min_bin_n = 1 in mid tiers).

---

## What COMPASS shipped today (engineering)

- **Draft-mass ECDF** → three tier cutpoints (~5% / 13.5% / 32% panel top-%)  
  `bdp_ai_draft_mass_ecdf.py` · `--draft-mass-tiers 30`
- **P2b overlay** with **`--tj-edge-mode shared_panel`** (default): one **panel-wide** 4+7 T̂_j grid; all Â tiers use **same bin centers** on x.  
  `cct_p2b_ai_band_overlay.py` → `FHERO_pw4p7_overlay_lines_*_sharetj_*.png`
- Legacy **`within_band`** median split still available (`--tj-edge-mode within_band`).

---

## Ask for SCOUT

Charles wants to **open the data aperture** and explore options to **raise K and bin counts** without abandoning last-ps. Prior pass (all-ps) showed **similar curves** — the issue then was not “wrong shape,” it was **confusing estimand**. Now estimand is clear; **noise** is the limit.

### Priority questions

| # | Question | Why |
|---|----------|-----|
| **A** | **all-ps + last-ps side-by-side** on same 13–21 lock: K, knee stability, bin n | Quantify power gain vs estimand cost |
| **B** | **Season window:** 2011–2021 last-ps vs 2013–2021 — K and knee | +96 drafts on last-ps (520 vs 424) for 11–21 |
| **C** | **+DFT filter** on 13–21 last-ps: same K, smaller n — worth it for F-HERO story? | n ≈ 6,095 vs 16,836; K still 424 |
| **D** | **Division I / II** filter (your thread) — effect on K and T̂_j variance | Parked in sandbox matrix |
| **E** | **min-minutes** sensitivity (10 vs 20) on last-ps | More PS, possibly more drafts |
| **F** | Any **external draft / roster aperture** (transfer portal era, G-league paths) — out of scope or not? | Charles believes in CCT; wants honest power audit |

### Deliverable shape (when Charles green-lights)

1. Small **power table**: rows = aperture knobs, cols = n, K, min bin n (top tier F-HERO), knee T̂_j visible Y/N.  
2. One **aligned shared-grid overlay PNG** per aperture row (script ready).  
3. **SCOUT_report_to_COMPASS** bullet: recommend one “deck aperture” vs “paper aperture.”

---

## What we are **not** asking

- Re-open **HERO poolq_loo** inverted-U hunt (mg0 artifact; mg10 flat elite — settled).  
- Merge score and select (BINDING).  
- Drop last-ps without Charles/Alex sign-off.

---

## Charles intent

> “I believe in this CCT. I think we are finding it, but I think we're at the boundary of statistical significance with the data we have.”

COMPASS agrees. Next step is **measurement of aperture options**, not a new axis.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-27 | Alex debrief: align T̂_j bins; revisit data aperture; 424 drafts on last-ps lock. COMPASS → SCOUT memo filed. |
