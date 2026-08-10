# 541 Grandchild ASSIGN — method note

**Last synced:** 2026-08-10

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

- **D** — within-team MSE (not assortativity).
- **H** — normalized sorting index.
- **centroid SD** — between-team dispersion of final μ_j.

## Run

```bash
python sports/541_grandchild_homophily_assign.py          # self-test
python sports/scripts/541_grandchild_rho_sweep.py         # full sweep
python sports/scripts/541_grandchild_rho_sweep.py --quick # smoke
```

## Outputs

`3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/`

Default ρ sweep: **0 to 1** in steps of 0.05 (21 points); 30 realizations each.

## Spec source

`3-Master_Plan/VECTOR_work/COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md`
