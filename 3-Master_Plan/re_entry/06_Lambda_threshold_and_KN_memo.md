# 6. Sort-and-chop λ threshold — what we learned (Aug 2026)

**Last synced:** 2026-08-03

**Notation (Aug 2026):** **K** = slots selected (top-K); **λ** = congestion weight in score; **K/N** = selectivity. Retired **Λ** for slots. Characterization default **K/N = 10%** (`gallery_knobs`); MBB draft ~1% is a domain calibration point later.

**Purpose:** Capture findings from the **sort-and-chop λ diagnostic** before moving on to θ, γ, and **K/N** sweeps. Standalone; inline glossary.

**Figures / scripts**

| Artifact | Path |
|----------|------|
| λ sweep (sort-and-chop) | `re_entry/HEROs_and_PASSes/sort_chop_lambda/PASS_C_sort_chop_lambda_sweep.png` |
| γ / λ_crit explainer | `re_entry/HEROs_and_PASSes/sort_chop_lambda/LAMBDA_threshold_gamma_viability.png` |
| Hard vs smooth σ | `re_entry/HEROs_and_PASSes/sort_chop_lambda/VIABILITY_hard_vs_smooth.png` |
| Diagnostic script | `sports/scripts/sort_chop_lambda_diagnostic.py` |
| γ figure script | `sports/scripts/build_lambda_gamma_threshold_figure.py` |
| Gallery knobs (N, K) | `sports/scripts/gallery_knobs.py` — default **350×16 = 5600**, **K = 560** (K/N = 10%) |

**Checklist:** [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) Phase B — θ, γ, **K/N** rows.

**PD15 source:** [`../../transcripts/PD15_notes.md`](../../transcripts/PD15_notes.md) — θ likely tied to **K/N** (hypothesis; **not yet tested**).

---

## Critical λ — definition (BINDING plain language)

**Critical λ** is the **first** λ at which **score ranking** (\(S_i = A_i - \lambda L_C\)) **differs from talent-only ranking** (\(S_i = A_i\)) — i.e. the first **rank swap** at the global top-**K** margin.

> **Critical λ is the first λ where the score reorder beats pure talent reorder — not “when congestion feels big.”**

Below \(\lambda_{\mathrm{crit}}\): bin curves can match λ = 0 exactly (λ = 0.25 often invisible).  
Above \(\lambda_{\mathrm{crit}}\): enough swaps accumulate that **16-bin selection rates** move and the hump appears.

This is a **reorder** statement, not a magnitude statement about how large \(L_C\) is in absolute terms.

---

## The θ-straddle team (sort-and-chop picture)

Under **perfect sort-and-chop**, players are sorted by \(A_i\) and chopped into rosters of 16. **Ability ranges do not overlap between teams:** the weakest player on the upper team still has **strictly higher** \(A_i\) than the strongest player on the team below.

**\(L_C\)** = leave-one-out mean of soft peer viability \(\sigma(\gamma(A_j - \theta))\) over **teammates only** (you excluded from the mean).

**NCAA bookkeeping (real rosters):** max **15** players on a team → each player has at most **14** teammates → **PoolQ** (full-pool mean) uses **15** player-abilities on the roster; **PoolQ LOO** / **L_C** use **14** (everyone else on the team).

**Gallery sim default:** `roster_size = 16` (350×16 = 5600) — teaching scale, not NCAA 15. Then LOO = **15** teammates. Override with `GALLERY_ROSTER_SIZE=15` when you want NCAA headcount; threshold **algebra** (4/γ) is unchanged — only headcounts in prose/examples shift.

### League-wide pattern (typical draw, θ in the interior)

| Team type | Who is in the LOO peer set | Typical \(L_C\) |
|-----------|------------------------------|-----------------|
| **All-above-θ teams** (strong slices) | All LOO peers have \(A_j \gg \theta\) → every \(\sigma \approx 1\) | **Saturated high** (~≈ 1; all “max viable”) |
| **θ-straddle team** (one slice) | Some LOO peers above θ, some below — **only roster that mixes** | **Interior** (only team not near 0 or saturated) |
| **All-below-θ teams** (weak slices) | All LOO peers have \(A_j \ll \theta\) → every \(\sigma \approx 0\) | **Near zero** (~≈ 0; no viable peers) |

**Charles lock (Aug 2026):** In this idealized picture, **every team above the straddle team has all players above θ**; **every team below has all players below θ**; **only the straddle team** has both kinds. Within that team, roster slots follow **global ability order within the block** (weakest-to-strongest along the slice): there is an index \(k\) such that slots \(k+1..R\) are above θ and slots \(1..k\) are below θ, where \(R\) = roster size (15 NCAA, 16 gallery default).

**Code nuance:** We use **smooth** \(\sigma\), not a hard step — so “\(L_C = 0\)” below means **≈ 0**, and “max” above means **≈ saturated**, not literally binary.

### Why this team sets \(\lambda_{\mathrm{crit}}\)

Rank swaps need a **small** \(\Delta A\) and a **large** \(\Delta L\) at a marginal pair. That happens at **slice seams** next to the θ-straddle team:

- **Bottom of an all-above team** vs **top of the straddle team** (or straddle vs all-below): tiny talent gap (consecutive global ranks), big jump in peer viability → large \(\Delta L\).

The steepest “viability per unit ability” is at the **θ knee** of \(\sigma\), where \(\mathrm{d}\sigma/\mathrm{d}A = \gamma/4\), giving \(\lambda_{\mathrm{crit}} \approx 4/\gamma\).

**Carry this sentence:** *Sort-and-chop makes one “mixed” roster; λ first bites at the seams next to it, where a sliver of talent edge meets a wall of congestion change.*

---

## One-line summary

On **sort-and-chop** rosters (between-team overlap = 0), talent-only and moderate λ can look identical until **λ exceeds ≈ 4/γ**; then congestion at the **viability cutline θ** reorders global top-**K** selection and produces the hump. **0.41 is λ (lambda), not A_i and not T_j.**

---

## Setup (what we held fixed)

- **Assignment:** sort-and-chop only (hard slices; **overlap between teams = 0**).
- **Score:** \(S_i = A_i - \lambda L_C\) when λ > 0; \(S_i = A_i\) when λ = 0.
- **L_C:** `crowding_smooth` — LOO mean of \(\sigma(\gamma(A_j - \theta))\).
- **Ability draw:** `beta_2_2` on **[0, 1]** (539 preset — **not** empirical ppm z).
- **θ:** `SELECTION_539_VIABILITY_THETA = 0.72` (Alex 539 reference JSON).
- **γ:** `SELECTION_539_VIABILITY_SHARPNESS = 10`.
- **Select:** global top-**K**, winner `"C"`.
- **Bins:** 16 quantile bins on **pool mean** (visualization only — **does not** set λ threshold).

**T_{j*}** (sim assignment targets) is **not used** by sort-and-chop assignment.

---

## Main findings

### 1. λ = 0 and λ = 0.25 can be identical (on sort-and-chop)

- On disjoint slices, **Spearman(A_i, L_C) = 1** — high talent teams have high crowding.
- For small λ, **16-bin selection rates** can match λ = 0 exactly (max |Δrate| = 0 across bins).
- Individual swaps at the cut line may occur without changing bin-level curves.

### 2. Monotone → hump transition is sharp

| λ range (539, seed 42, N = 15k, K = 1500) | Shape |
|-------------------------------------------|--------|
| 0 – ~0.40 | Same bin curve as talent-only; strictly increasing in pool-mean bin |
| ~0.42 | First bin-rate movement; peak still at highest bin |
| ~0.44–0.46 | Hump forming; peak shifts left |
| 0.55+ | Needle hump (Pass B/C familiar shape) |

At **N = 5600, K = 560** (K/N = 10%): same λ threshold story; top-bin rate depends on **K/N** (saturation), not on the 4/γ algebra itself.

### 3. Critical λ ≈ **4/γ** (not a magic 0.41 constant)

**Definition:** \(\lambda_{\mathrm{crit}}\) = first λ where **score reorder** ≠ **talent-only reorder** (first global rank swap), **not** “when congestion feels big.”

Adjacent sort-and-chop **players** at slice seams (not overlapping teams — disjoint slices) flip when

\[
\lambda < \min_{\text{adjacent teams}} \frac{\Delta A}{\Delta L}.
\]

The tightest pair sits where **L_C** rises fastest vs **A** — at the **θ knee** of \(\sigma(\gamma(A-\theta))\). There, \(\mathrm{d}\sigma/\mathrm{d}A = \gamma/4\), so

\[
\lambda_{\mathrm{crit}} \approx \frac{4}{\gamma}.
\]

| γ | 4/γ | Observed curve break (539, sort-and-chop) |
|---|-----|-------------------------------------------|
| 5 | 0.80 | ~0.80 |
| **10** | **0.40** | **~0.42** |
| 20 | 0.20 | ~0.23 |

Observed break is slightly **above** 4/γ because bin curves move only after reorders affect **global top-K**.

**γ only matters when λ > 0** (crowding in score). Sort-and-chop assignment itself has no γ.

### 4. What does **not** move the core threshold much

| Knob | Effect on λ_crit ≈ 4/γ |
|------|-------------------------|
| **n_bins** (4–64) | None (aggregation only) |
| **roster_size** (5–50, fixed N) | ~None (min ΔA/ΔL stays ≈ 4/γ) |
| **T_{j*}** | None (unused in sort-and-chop) |
| **T_j** | Realized roster mean (post-chop) |

### 5. What moves the **visible** hump (secondary)

| Knob | Effect |
|------|--------|
| **K/N** | Shifts where global cut sits vs θ-crossing teams; changes top-bin saturation |
| **θ** | Moves **where** on the ability axis the bottleneck sits; min ΔA/ΔL still ≈ 4/γ at each θ, but **when** the plot breaks depends on K |

---

## Within-team vs between-team “overlap”

| | Sort-and-chop | Soft ρ (realistic NCAA) |
|--|---------------|------------------------|
| **Within-team** ability SD | ~0.0002–0.0007 (tiny slices) | ~0.16 |
| **Between-team** interval overlap | **0%** of pairs | **~99%** of pairs |

The ~0.0002 figure is **within-roster** spread, not between-team overlap.

---

## Where θ comes from (today — not from K/N)

| Source | Value | Meaning |
|--------|-------|--------|
| **`SELECTION_539_VIABILITY_THETA`** | **0.72** | 539 teaching preset on [0,1] Beta **A** — from `sports/tier1_539_reference_settings.json` |
| **`VIABILITY_THETA`** (530 default) | **≈ 0.755** | `med(perf \| ever drafted)` — ppm **z within season** (CELL 5d) |

**Not implemented:** θ = f(K/N). **PD15 hypothesis:** θ may **co-vary** with selection rate across domains (MBB vs Army); that is a **planned sweep**, not a current rule.

**PD15 also says:** θ is **not** “median of selected players” in the sim.

---

## K/N — empirical ballpark vs current sim

| Domain / setting | K | N (pool) | K/N | Notes |
|------------------|---|----------|-----|-------|
| **Current gallery default** | 560 | 5600 | **~10%** | Phase B characterization baseline |
| **MBB NBA draft (D1 order of magnitude)** | **~60** | **~5,500** | **~1.1%** | Empirical anchor later — not general sim default |
| **Old 539 preset** | 1500 | 15000 | **10%** | Same selectivity as new default; different N |
| **Army (Charles intuition)** | — | — | **~40%?** | High selectivity regime — **sweep, don’t assume** |

**Charles’s point:** At K/N ≈ 1–2% we are in **MBB-like** selectivity only. The model’s behavior at **K/N ~ 10–40%** (Army-like) is largely **unexplored** and may look very different (top-bin saturation, θ placement, hump visibility).

**Recommendation for Phase B:** Treat **K/N** as its own slide — at minimum three regimes, e.g. **~1%** (MBB), **~10%** (539 legacy), **~40%** (Army ballpark). Keep sort-and-chop or move to soft ρ only when testing **overlap**; threshold algebra above is sort-and-chop specific.

---

## Open work (do not forget)

### From PD15 — θ × K/N (Alex)

- [ ] **Sweep θ** (sigmoid center) at fixed γ, λ, ρ — characterize both curves.
- [x] **θ × K/N panel** — `theta_kn_sweep_diagnostic.py`; readout in `HEROs_and_PASSes/theta/THETA_KN_sweep_summary.md`. **Yes:** peak bin shifts with both θ and K/N (see table there).
- [ ] **γ sweep** — links directly to λ_crit = 4/γ.

Suggested minimal panel (sort-and-chop or baseline soft ρ):

- θ ∈ {0.5, 0.72, 0.9} × K/N ∈ {1%, 10%, 40%} (adjust N, K via `GALLERY_N_SELECTED`, `GALLERY_N_TEAMS`, `GALLERY_ROSTER_SIZE`).
- Record: peak bin, top-bin rate, λ at which curve departs from λ = 0.

### Gallery / code hygiene

- Consider setting default **K = 60** (not 100) for tighter MBB match — optional; document whichever you use on slides.
- Sort-and-chop remains a **benchmark** (overlap 0); general NCAA pools need soft **ρ** later.

---

## Glossary (this memo)

| Symbol | Name | Role |
|--------|------|------|
| **λ** | `loo_gap_weight` | **Weight** on **L_C** in **score** (not congestion itself) |
| **L_Q** | `poolq_loo` | LOO mean teammate **A** (hero X-axis analog) — **14** peers NCAA / **15** at gallery default |
| **L_C** | `pool_c_smooth_loo` | LOO mean peer viability σ(γ(A−θ)) — same peer count as **L_Q** |
| **PoolQ** | `pool_mean` | Full-roster mean ability (**15** NCAA including self in denominator, or **16** gallery) — **not** LOO |
| **γ** | `viability_sharpness` | Sharpness of σ(γ(A−θ)) in **L_C** |
| **θ** | `viability_theta` | Viability cutline / sigmoid center |
| **ρ** | `assignment_rho` | Assortativity in **assignment** (not sort-and-chop) |
| **K/N** | `n_selected / n_individuals` | Selection rate — **system feature** |
| **λ_crit** | — | First λ where **score reorder** beats **talent-only reorder** (not “when congestion feels big”) |

**Full story:** § Critical λ — definition; § The θ-straddle team.

---

## Regenerate figures

```bash
python sports/scripts/sort_chop_lambda_diagnostic.py
python sports/scripts/build_lambda_gamma_threshold_figure.py
python sports/scripts/theta_kn_sweep_diagnostic.py
```

Override scale:

```bash
GALLERY_N_TEAMS=350 GALLERY_ROSTER_SIZE=16 GALLERY_N_SELECTED=60 \
  python sports/scripts/sort_chop_lambda_diagnostic.py
```
