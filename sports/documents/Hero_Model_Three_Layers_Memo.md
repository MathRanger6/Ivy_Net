# Hero inverted-U — three model layers (v1)

**Last synced:** 2026-07-30

**Audience:** Charles + Alex read-through  
**Canonical hero / Pass gallery:** `3-Master_Plan/re_entry/HEROs_and_PASSes/`  
**Related:** [`05_Model_Nesting_Note_v1.md`](../../5-Manuscript/05_Model_Nesting_Note_v1.md), [`30_Alex_Gates_inform_status_outline.md`](../../3-Master_Plan/30_Alex_Gates_inform_status_outline.md), [`BINDING_Selection_is_its_own_step.md`](../../3-Master_Plan/BINDING_Selection_is_its_own_step.md), [`re_entry/02_Three_Kinds_of_Model.md`](../../3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md)

---

## 0. BINDING — environment ≠ advancement; score ≠ select

**Do not merge** “describe the peer environment” with “who wins the scarce slot.” Inside advancement, **do not call the score “selection.”**

| Mechanism | Object | Question |
|-----------|--------|----------|
| **Environment** | `L_net = B(·) − D(·)` | How do peers help vs hurt (development, visibility, crowding around you)? |
| **Scoring** | Alex `S_i = A_i − λ·L_C` | How do we **rank** candidates? (**λ** lives here.) |
| **Selection** | Winner rule (v1: **top K**) | Given ranks, **who wins** the scarce slot? |

**Unified nest:** `S_i = A_i + λ(B − D) = A_i − λ·L_C` when `(B − D) = −L_C` for the ranking channel. Knockout: `λ = 0` ⇒ `S_i = A_i`.

- **Hero (Layer A):** outcome only — draft rate vs pool quality. Does **not** identify environment vs advancement channel.
- **540 / Pass A (Layer C):** makes **score → select** explicit — rank by score → top **K**; knockout = talent-only score vs congestion-in-score.

*The hero describes outcomes; `L_net` is the peer environment; advancement = score then select; the sim tests congestion in the score under a fixed winner rule.*

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
| **B. Structural (theory)** | **Three parts:** (1) `L_net = B − D` environment; (2) Alex `S_i` **scoring**; (3) winner rule **select** | Nesting note §2–3; BINDING | Environment help/hurt **and** **D may enter the score**; select is separate | Separate estimation of B(Q) and D(Q) in v1; hero ≠ scoring equation |
| **C. Generative (sim)** | **Assign (`ρ`) → score (`λ`) → select (top K)** | `540_READ_ME_SIM.md`, `540_three_step_sim.ipynb`, `tier1_*.py` | **Congestion in the score** changes who gets selected; **talent-only score fails** | Bin-for-bin reproduction of empirical `poolq_loo` ventiles |

**Alex side-by-side (v1):** Layer **A hero PNG** + Layer **C sim PNG** on **same Y** (advancement rate), **honest X** (empirical LOO quality vs sim LOO bins), plus limitation sentence below.

---

## 3. How each layer is tested

### Layer A — regression on real rows

- Filter panel to hero estimand → OLS `Y_draft ~ 1 + poolq_loo + poolq_sq` (**LPM** = linear probability model, not linear programming).
- **Pass:** `β₂ < 0` (fitted curve **concave down** / inverted-U tendency); optional overlay tracks ventile bin means.
- **What the quadratic buys you:** a signed curvature claim (`β₂`) plus one turning point `Q* = −β₁/(2β₂)` (local max if `β₂ < 0`). **Not** inflection points (need richer than quadratic). Claims are about the **fitted** curve; hero **bins** stay the stylized fact. Not mechanism.
- **Not required:** R², causal interpretation, or match to sim.

### Layer B — prose + ingredient knockouts

- No single estimated formula in v1.
- **Part 1:** B − D frames the **environment** (help vs hurt among peers).
- **Part 2:** Alex score frames **ranking** — congestion enters the **score**, not “the whole model.”
- **Part 3:** Top K (or later stochastic draw) is the **winner rule**.
- **Pass:** Narrative consistency + sim shows λ=0 (ability-only **score**, same top-K) **fails** the generative congestion story.

### Layer C — simulation

- Draw synthetic league → **assign** rosters (`ρ`) → **score** → **select** top **K** → bin by **`poolq_loo`** (16 quantile).
- **Pass A (talent-only score):** `score_mode='ability'` / `λ = 0` → **monotone** selection rate on `poolq_loo` (bin 1 ~0.7% → bin 16 ~28%); no elite dip.
- **Pass A (congestion in score):** `score_mode='loo_gap_plus_ability'`, `loo_pool_l_mode='crowding_smooth'`, `w=0.5` → elite-tail **compression** (bin 16 ~16% vs ~28% talent-only); not pointwise hero match.
- **Pass B (`ρ` ablation):** low / moderate / high assortativity + sort-and-chop diagnostic → `HEROs_and_PASSes/PASS_B_*` (assignment plumbing, not the headline theorem).
- **Scripts:** `sports/scripts/hero_model_reset_bundle.py` (Pass A); `sports/scripts/540_rho_ablation_bundle.py` (Pass B).
- **Archived labs:** 538D etc. under `sports/archive/` — historical source; daily workspace is **540**.

---

## 4. Simplification strategies (both are valid)

| Strategy | Use for | Procedure |
|----------|---------|-----------|
| **Bottom-up** | Layer A | Start quadratic → decompose Q only at Rung 2.5 (`poolq_loo` vs `crowding_smooth` in CELL 5d) |
| **Top-down** | Layer C | Full generative stack → zero λ / ability-only score / change `ρ` → record what breaks |

Use **bottom-up first** for the hero; **top-down** for 540 mechanism strip-down.

---

## 5. Simulation plumbing vs core claim

| Knob | Role | v1 gate? |
|------|------|----------|
| **λ / w on L_C in score** | Core mechanism | **Yes** (Pass A done) |
| **Top-K selection** | Scarcity (winner rule) | **Yes (conceptual)** |
| **Soft assignment (`ρ`, T_j)** | Realistic pools | Helpful, not theorem (Pass B diagnostic) |
| **Sort-and-chop overlay** | Hard assortative diagnostic | No — not `ρ → ∞` |
| **Preferential attachment** | Boolean, default off | No — stretch |
| **Faithful historical team sweeps** | Realism stretch | **No — see §6** |
| **Bin-for-bin LOO match to hero** | North-star R&D | **No — see §6** |

**Notation:** User-facing assignment knob is **`ρ`**. Legacy **`τ`** (temperature) appears only in archived docs. Soft crowding inside `L_C` ≠ assignment softness ≠ selection noise.

**Path II (locked):** Generative figure may bend on **LOO `poolq_loo` bins** while empirical hero is the **replicated fact** on the same conditioning object — still **not** claiming pointwise match without a dedicated calibration pass.

---

## 6. Explicitly deferred (stretch, not v1 success criteria)

Do **not** block Alex draft or side-by-side on:

1. **Bin-for-bin replication** of hero ventile draft rates from sim on `poolq_loo`.
2. **Rivanna / faithful** full sweeps until minimal score→select story stays locked.
3. **Separate B(Q) and D(Q) estimation** on one axis.
4. **Dense assortativity grids**, preferential attachment on, empirical team cloning, HS binning, multiplicative rewrite.

These remain **parallel R&D** after the minimal POC bundle is frozen.

---

## 7. Limitation sentence (Alex slide / manuscript §5)

> The empirical stylized fact is defined on **leave-one-out pool quality** among teammates; the minimal generative proof-of-concept **scores** with a term that penalizes leave-one-out viable-peer congestion, **selects** top K, and plots binned **selection rates on the same LOO quality axis**. We do **not** claim bin-for-bin reproduction of the empirical ventile draft rates in v1; we claim that **talent-only scoring is insufficient** and that **congestion in the score** can bend advancement curves in a disciplined artificial league.

(Source: nesting note §4; shortened for slides.)

---

## 8. Keepers vs reorder (Jul 2026 reset · sync Jul 28)

**Keep:** `530` pipeline, hero triplet, nesting note, BINDING, re_entry 00–03, **540** three-step sim, Pass A/B gallery (`HEROs_and_PASSes/`), Pertinent Thoughts sensitivities.

**Reorder claims:** Phenomenon first (hero) → minimal score ingredient (λ) → theory prose — not “one formula does everything.” Keep **score ≠ select** in every write-up.

**Deliverables from this reset:** this memo; gallery `3-Master_Plan/re_entry/HEROs_and_PASSes/` (`PASS_A_*` LPM / knockout CSVs / side-by-side PNG; `PASS_B_*` ρ ablation).
