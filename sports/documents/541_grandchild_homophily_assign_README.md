# 541 Grandchild ASSIGN — method note

**Last synced:** 2026-08-11

## What was added

- **`sports/541_grandchild_homophily_assign.py`** — Grandchild one-shot ASSIGN (endogenous centroids, stub capacity, Quayle exponential homophily).
- **`sports/scripts/541_grandchild_rho_sweep.py`** — ρ sweep on 2015 empirical PPM z panel, C=15.
- **`tier1_pool_assignment.simulate_generative_rosters(..., method="grandchild")`** — ASSIGN hook only.

## What was not changed

- Parent (longitudinal dynamic) model — spec only.
- Child (fixed empirical centroid) — not implemented as separate code path here.
- **`soft_assign`**, **`sort_chop`**, SCORE, SELECT — untouched.

## Empirical test league (default sweep)

| Quantity | Value |
|----------|-------|
| Season | 2015 NCAA MBB |
| N | All filtered player-seasons (~6030) |
| C | 15 |
| J | N / C = 402 |
| A_i | PPM z within season (530/PD17 panel filters) |

## Diagnostics

- **D** — within-team Mean Squared Error (MSE) (not assortativity).
- **H_sort** — realized sorting index on a fixed partition (alias: `sorting_index_h` in code; not generative ρ).
- **centroid SD** — between-team dispersion of final μ_j.

**Slide / Alex brief (plain words for D and H_sort):**  
[`3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md`](../../3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md)

**H_sort glossary AUTO slide:**  
`python sports/scripts/build_grandchild_h_sort_explainer_slide.py` → `slides/auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx`

**L_C distribution (empirical vs Grandchild sim):**
```bash
python sports/scripts/grandchild_empirical_lc_compare.py              # 2011–2021 side-by-side
python sports/scripts/grandchild_empirical_lc_compare.py --rho 0.5 --gamma 0.5
python sports/scripts/build_grandchild_empirical_lc_compare_slide.py   # → slides/auto/CHAR_grandchild_empirical_lc_compare_AUTO.pptx
python sports/scripts/grandchild_league_lc_diagnostic.py --season 2015  # sim only, one year
python sports/scripts/empirical_lc_distributions.py --gamma 0.5         # empirical only
```

**Selection inverted-U (Grandchild → SCORE → SELECT):**
```bash
python sports/scripts/grandchild_selection_inverted_u_diagnostic.py          # 2011–2021 stacked
python sports/scripts/grandchild_selection_inverted_u_diagnostic.py --rho 0.5 --rho-sweep
python sports/scripts/grandchild_selection_inverted_u_diagnostic.py --season 2015  # single year
```
Outputs: `grandchild_assign/GRANDCHILD_selection_inverted_u_2011_2021.{png,meta.json}` (+ empirical NCAA overlay).

**541 core scripts:**
```bash
python sports/541_grandchild_homophily_assign.py          # self-test
python sports/scripts/541_grandchild_rho_sweep.py         # full sweep
python sports/scripts/541_grandchild_rho_sweep.py --quick # smoke
```

## Outputs

`3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/`

Default ρ sweep: **0 to 1** in steps of 0.05 (21 points); 30 realizations each.

**ρ → assortativity slide (Alex ASSIGN validation):**

```bash
/opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_rho_assortativity_slide.py
```

Writes `grandchild_assign/GRANDCHILD_rho_vs_assortativity.png` + `slides/auto/CHAR_grandchild_rho_assortativity_AUTO.pptx`.
Sweep-only: `python sports/scripts/541_grandchild_rho_sweep.py`.

**League analysis slide (HAND17 interval overlap — 2×2):**

```bash
/opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_league_analysis_slide.py --compare-window
```

Optional L_C-only diagnostic: `grandchild_league_lc_diagnostic.py`.

## Spec and slides

| Item | Path |
|------|------|
| Detailed spec | `3-Master_Plan/VECTOR_work/COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md` |
| Grandchild deck | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/VECTOR_ASSIGN_Grandchild_Model.pptx` |
| Parent/Child deck | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/VECTOR_ASSIGN_Dynamic_to_OneShot_Model.pptx` |
| Slide JPGs | sibling folders under `…/slides/` (see `slides/README.txt`) |
