# Model re-entry — operations order (OPORD)

**Last synced:** 2026-07-30  
**Owner:** Charles + Cursor agent (not a SCOUT handoff)  
**Status:** **Executed** — archive, 540 surface, Pass B exports on disk.

**Charles — personal checkoff:** Do **not** use this OPORD as your to-do list. Use [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) (what **you** run / prove). This file is ops history and agent phases.

---

## Intent

Re-entry sim work mirrors the document re-entry pattern: **park old lab notebooks**, build a **thin `540_*` surface**, reuse **`tier1_*` engines**. Revolution = new problem approach and entry point; evolution = import battle-tested libraries.

**Charles authored** the three-step **pipeline**: **assign → score (`S_i`) → select (top K)**. Alex endorsed it.

**User-facing assignment knob:** **ρ (rho)** = assortativity (0 = max mixing; ρ↑ = sharper match). Legacy **τ (temperature)** in archived docs = inverse mixing; **ρ = 1, σ = 0.65** maps to old **τ ≈ 0.65**.

---

## Phase 0 — Precondit

| # | Step | Owner |
|---|------|--------|
| 0.1 | Proceed in this chat (Charles + Cursor agent) | Charles |
| 0.2 | Notebook burn: cell index 1 unless `skip burn` | Agent |

---

## Phase 1 — Spec on disk (brief before moves)

| # | Step | Deliverable |
|---|------|-------------|
| 1.1 | Write `sports/540_READ_ME_SIM.md` | Re-entry sim contract |
| 1.2 | Pointer in `re_entry/00_READ_ME_FIRST.md` | One paragraph |
| 1.3 | Update `re_entry/02`, `03`: τ → **ρ** for assignment | Short patches |
| 1.4 | Update `PARKED_FOR_LATER.md` | 538D archived; active = `540_*` |

**Gate:** Charles approves `540_READ_ME_SIM.md` before Phase 2.

---

## Phase 2 — Archive

| # | Step | Deliverable |
|---|------|-------------|
| 2.1 | Create `sports/archive/` + `README.md` | Folder + manifest |
| 2.2 | Move into archive | `538D_development.ipynb`, `538_alex_tier1_model_and_fit.ipynb`, `537_Sports_Simulation.ipynb`, `535_sports_tier_1.ipynb`, `538D_widget_render_test.ipynb`, optional `535_*_outputs_backup_*.ipynb` |
| 2.3 | Grep and fix broken doc pointers | Docs we touch only |
| 2.4 | **Do not move** | `530`, `tier1_*.py`, `hero_model_reset_bundle.py`, `sports_pipeline/` |

---

## Phase 3 — COMPASS touch (light)

| # | Step | Deliverable |
|---|------|-------------|
| 3.1 | `3-Master_Plan/20260727_COMPASS_sim_reentry_status.md` | ½-page status + claims guard |
| 3.2 | Mirror plan if `~/.cursor/plans/` edited | `./scripts/mirror_plan.sh` (optional) |

No mandatory COMPASS agent session.

---

## Phase 4 — SCOUT (reference only)

| # | Step | Deliverable |
|---|------|-------------|
| 4.1 | No SCOUT session required this sprint | — |
| 4.2 | Archived notebooks = SCOUT-era lab reference; do not edit | Note in `540_READ_ME_SIM.md` |
| 4.3 | Fresh SCOUT session only if `tier1_*` bug | Uses 540 brief |

---

## Phase 5 — Code (ρ + Pass B)

| # | Step | Deliverable |
|---|------|-------------|
| 5.1 | **ρ** in `tier1_pool_assignment.py` | `exp(-ρ·(A_i-T_j)²/(2σ²))`; ρ=0 → uniform among open rosters |
| 5.2 | `USE_PREFERENTIAL_ATTACHMENT` bool in config | α=0 default |
| 5.3 | `sports/scripts/540_rho_ablation_bundle.py` | Low ρ, high ρ, sort-and-chop; fix **score + winner rule** |
| 5.4 | Export `HEROs_and_PASSes/PASS_B_*` | CSVs, PNG, summary, caption |
| 5.5 | `sports/540_three_step_sim.ipynb` | Thin Jupyter orchestration |
| 5.6 | Dry-run from repo root | Green run |

**Pass A (λ knockout):** already in `HEROs_and_PASSes/PASS_A_*` — do not redo.

**Pass B (ρ ablation):** fix **score** (**S_i** / λ / **L_C**) and **select** (top K); vary assignment only.

---

## Phase 6 — Reconcile Alex bundle

| # | Step | Deliverable |
|---|------|-------------|
| 6.1 | Keep `HEROs_and_PASSes/PASS_A_*` | Pass A |
| 6.2 | `PASS_B_README.txt` | Cross-link to λ knockout |
| 6.3 | Limitation sentence for ρ pass | caption.txt |

---

## Phase 7 — Presentation to Alex (Charles leads)

| # | Step | Deliverable |
|---|------|-------------|
| 7.1 | `Model.pdf` + 2 min addendum | Three-step pipeline; Pass A + Pass B |
| 7.2 | Minimal table | λ knockout vs ρ ablation arms |
| 7.3 | PDFs of updated docs | Charles runs convert scripts locally |
| 7.4 | Email / meeting | Figure paths + limitation sentences |

---

## Phase 8 — Close-out (when Charles asks)

| # | Step |
|---|------|
| 8.1 | Git commit (docs + archive + scripts + tracked exports) |
| 8.2 | Park stretch in `PARKED_FOR_LATER.md` |

---

## Already done (skip)

- Empirical hero + LPM  
- Pass A: λ knockout + `HEROs_and_PASSes/PASS_A_*`  
- Re-entry docs 01–03 + `Model.pdf`  
- BINDING: **`L_net`** ≠ advancement; **score ≠ select**; unified **S_i**, **(B−D)=−L_C**

---

## Execution order

```
1.1 → 1.4  →  2.1 → 2.4  →  3.1  →  5.1 → 5.6  →  6.1 → 6.3  →  7.x  →  8.x (optional)
```

---

## Assignment formulas (540 contract)

**Three-step assignment (generative step 1):**

1. Draw **A_i** (abilities)  
2. Draw **T_j** (team target means)  
3. Soft place: \(\pi_{ij} \propto \exp\bigl(-\rho\,(A_i-T_j)^2/(2\sigma^2)\bigr)\) × optional \((n_j+k)^\alpha\)

| ρ | Meaning |
|---|---------|
| **0** | Uniform among teams with roster room (max mixing) |
| **1** | Moderate (≡ legacy τ=σ≈0.65) |
| **High** | Sharper match to **T_j** (not sort-and-chop) |

**Sort-and-chop:** separate benchmark (`method="sort_chop"`) — max assortativity in 537 sense; not ρ→∞.

**Scoring (step 2):** **S_i = A_i − λ·L_C** (**λ** lives here).  
**Selection (step 3):** winner rule — v1 **top K**; later soft / stochastic. Pass B fixes λ, **L_C**, and K.

---

## Anti-patterns

- Adding cells to archived notebooks  
- Duplicating `tier1_*` logic inside 540  
- Claiming ρ ablation reproduces hero bin-for-bin  
- Renaming ρ back to τ in user-facing prose  

---

*See also: `sports/540_READ_ME_SIM.md`, `3-Master_Plan/re_entry/00_READ_ME_FIRST.md`*
