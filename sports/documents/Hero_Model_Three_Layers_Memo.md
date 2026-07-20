# Hero inverted-U — three model layers (v1)

**Date:** 2026-07-20  
**Audience:** Charles + Alex read-through  
**Canonical hero folder:** `sports/datasets/mbb/exports_inverted_u_v0/alex_side_by_side_v0/`  
**Related:** [`05_Model_Nesting_Note_v1.md`](../../5-Manuscript/05_Model_Nesting_Note_v1.md), [`30_Alex_Gates_inform_status_outline.md`](../../3-Master_Plan/30_Alex_Gates_inform_status_outline.md)

---

## 1. Locked hero estimand (fixed target for all tests)

All Layer A/C comparisons use **this** empirical spec unless explicitly noted as robustness.

| Field | Value |
|-------|--------|
| **Outcome** | `Y_draft` (ever drafted), mean rate per bin |
| **X-axis** | `poolq_loo` (LOO mean teammate `perf`) |
| **perf** | ESPN box **ppm**, **z-scored within collegiate season** |
| **Bins** | **16 quantile** (`poolq_binning='quantile'`) |
| **Winsor** | `poolq_loo` at **(0.01, 0.99)** before binning |
| **min_minutes** | **20** (applied before LOO when rebuilding from box) |
| **Panel source** | `use_prebuilt_panel_csv=False` for canonical rebuild path |
| **Draftee filter** | **Off** (`restrict_teams_by_draftees=False`) |
| **Seasons** | **2011–2021** |
| **Sample (Jul 2026 lock)** | **62,180** player-seasons; **1,134** drafted |

**File naming slug:** `empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011`

**Shape (qualitative):** rise through middle ventiles → plateau bins 12–15 (~2.3–2.6%) → **dip at bin 16 only** (~1.2%).

---

## 2. Three layers — do not merge into one “model”

| Layer | Object | Repo anchor | What a “pass” proves | What it does **not** prove |
|-------|--------|-------------|----------------------|----------------------------|
| **A. Phenomenological** | `Y ~ β₀ + β₁·poolq_loo + β₂·poolq_loo²` | `530` / `panel_build.draft_poolq_quadratic_coeffs` | Inverted curvature in the **real panel** on the hero estimand | Mechanism; that NBA uses this score |
| **B. Structural (theory)** | `L_net = B(·) − D(·)`; Alex `S_i = A_i − λ·L_C` in selection | Nesting note §2–3 | Why help and hurt can coexist; **D enters selection** | Separate estimation of B(Q) and D(Q) in v1 |
| **C. Generative (sim)** | Soft assign → score → top-K | `538D` CELL 10–12, `tier1_generative_eda.py` | **Congestion in the score** changes selection curves; **talent-only fails** | Bin-for-bin reproduction of empirical `poolq_loo` ventiles |

**Alex side-by-side (v1):** Layer **A hero PNG** + Layer **C sim PNG** on **same Y** (advancement rate), **honest X** (empirical LOO quality vs sim LOO bins), plus limitation sentence below.

---

## 3. How each layer is tested

### Layer A — regression on real rows

- Filter panel to hero estimand → OLS `Y_draft ~ 1 + poolq_loo + poolq_sq`.
- **Pass:** `β₂ < 0` (concave); optional overlay tracks ventile bin means.
- **Not required:** R², causal interpretation, or match to sim.

### Layer B — prose + ingredient knockouts

- No single estimated formula in v1.
- **Pass:** Narrative consistency + sim shows λ=0 (ability-only) **fails** the generative congestion story.

### Layer C — simulation

- Draw synthetic league → assign rosters → rank by score → select top **K** → bin by **`poolq_loo`** (16 quantile).
- **Knockout A (talent-only):** `score_mode='ability'` → **monotone** selection rate on `poolq_loo` (bin 1 ~0.7% → bin 16 ~28%); no elite dip.
- **Knockout B (congestion):** `score_mode='loo_gap_plus_ability'`, `loo_pool_l_mode='crowding_smooth'`, `w=0.5` → elite-tail **compression** (bin 16 ~16% vs ~28% talent-only); not pointwise hero match.
- **Script:** `sports/scripts/hero_model_reset_bundle.py` writes CSV + side-by-side PNG.

---

## 4. Simplification strategies (both are valid)

| Strategy | Use for | Procedure |
|----------|---------|-----------|
| **Bottom-up** | Layer A | Start quadratic → decompose Q only at Rung 2.5 (`poolq_loo` vs `crowding_smooth` in CELL 5d) |
| **Top-down** | Layer C | Full generative stack → zero λ / ability-only / drop assignment knobs → record what breaks |

Use **bottom-up first** for the hero; **top-down** for 538D mechanism strip-down.

---

## 5. Simulation plumbing vs core claim

| Knob | Role | v1 gate? |
|------|------|----------|
| **λ / w on L_C in score** | Core mechanism | **Yes** |
| **Top-K selection** | Scarcity | **Yes (conceptual)** |
| **Soft assignment (τ, T_j)** | Realistic pools | Helpful, not theorem |
| **Assortative sort-and-chop overlay** | Diagnostic (Plot A) | No |
| **Faithful-538 empirical team sweeps** | Realism stretch | **No — see §6** |
| **Bin-for-bin LOO match to hero** | North-star R&D | **No — see §6** |

**Path II (locked):** Generative figure may bend on **LOO `poolq_loo` bins** (CELL 12 default) while empirical hero is the **replicated fact** on the same conditioning object — still **not** claiming pointwise match without a dedicated calibration pass.

---

## 6. Explicitly deferred (stretch, not v1 success criteria)

Do **not** block Alex draft or side-by-side on:

1. **Bin-for-bin replication** of hero ventile draft rates from sim on `poolq_loo`.
2. **Rivanna / faithful_538** full sweeps (`outputs/simulation_sweeps/faithful_538_sweep*`) until minimal λ + K story is documented.
3. **Separate B(Q) and D(Q) estimation** on one axis.
4. **Assortativity grids**, empirical team cloning, HS binning, multiplicative rewrite.

These remain **parallel R&D** after the minimal POC bundle is frozen.

---

## 7. Limitation sentence (Alex slide / manuscript §5)

> The empirical stylized fact is defined on **leave-one-out pool quality** among teammates; the minimal generative proof-of-concept selects on a **score that penalizes leave-one-out viable-peer congestion** and plots binned **selection rates on the same LOO quality axis**. We do **not** claim bin-for-bin reproduction of the empirical ventile draft rates in v1; we claim that **talent-only selection is insufficient** and that **congestion in the score** can bend advancement curves in a disciplined artificial league.

(Source: nesting note §4; shortened for slides.)

---

## 8. Keepers vs reorder (Jul 2026 reset)

**Keep:** `530` pipeline, hero triplet, nesting note, 538D CELL 10–12, Pertinent Thoughts sensitivities, `alex_side_by_side_v0/` exports.

**Reorder claims:** Phenomenon first (hero) → minimal sim ingredient (λ) → theory prose — not “one formula does everything.”

**Deliverables from this reset:** this memo, `lpm_hero_coefficients.txt`, generative knockout CSVs, `inverted_u_side_by_side_empirical_vs_generative.png` in `alex_side_by_side_v0/`.
