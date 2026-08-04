# Read me first — sim re-entry (540, July 2026)

**Last synced:** 2026-07-30

**OPORD:** [`../3-Master_Plan/re_entry/model_OPORD.md`](../3-Master_Plan/re_entry/model_OPORD.md)  
**Your checklist:** [`../3-Master_Plan/re_entry/CHARLES_CHECKLIST.md`](../3-Master_Plan/re_entry/CHARLES_CHECKLIST.md) (PD15 characterization — gallery labels: Pass A empirical, B = λ, C = ρ)

**Before this file’s knockout table:** read [`../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md`](../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md) — full sentences on Pass A/B, empirical vs simulated, assignment, and which scripts to run. This README is the **contract / shorthand** after that.

If you feel lost: read [`../3-Master_Plan/re_entry/00_READ_ME_FIRST.md`](../3-Master_Plan/re_entry/00_READ_ME_FIRST.md) (docs 01–04) before opening sim code.

---

## What to open vs what to ignore

| Use daily (re-entry) | Ignore for daily work |
|----------------------|------------------------|
| This file + `540_three_step_sim.ipynb` | `tier1_cell10_playground_run.py` (**LEGACY** 538 widget UI) |
| `scripts/hero_model_reset_bundle.py` (Pass A) | Archived notebooks under `sports/archive/` |
| `scripts/540_rho_ablation_bundle.py` (Pass B) | `539_alex_model.ipynb` (older Alex lab; not 540 path) |
| `tier1_pool_assignment.py`, `tier1_generative_eda.py`, `tier1_sim_config.py` | Extending CELL 10 widgets |

Engines (`tier1_*`) are **shared libraries**. Bundles are **thin runners**. Playground = old UI around the same engines.

---
## Revolution vs evolution

| Do | Don't |
|----|-------|
| Import `tier1_pool_assignment.py`, `tier1_generative_eda.py`, `tier1_sim_config.py` | Extend archived notebooks (`538D`, `538`, `537`, `535`) |
| Thin scripts / `540_*` notebook | Copy-paste 538D cells |
| Answer Alex-sized questions (knockouts, ablations) | Rivanna sweeps, bin-for-bin hero match as v1 gate |

Archived notebooks in `sports/archive/` are **SCOUT-era lab reference** — read only, do not edit.

---

## Charles's three-step pipeline

1. **Assign** — build rosters (ρ or sort-and-chop)  
2. **Score** — **S_i = A_i − λ·L_C** (Alex v1: **(B−D)=−L_C** **in the score**; **λ** lives here)  
3. **Select** — winner rule: top **K** by **S_i** (later: soft / stochastic draw)

## Knockouts (shorthand — only after doc 04)

Full sentences: [`../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md`](../3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md).

| Pass | What toggles | Status |
|------|--------------|--------|
| **A** | λ=0 vs congestion in **S_i** (winner rule fixed) | Re-run → `HEROs_and_PASSes/pass_a/PASS_A_*` |
| **B** | ρ low / ρ high / sort-and-chop; **fixed score + select** | Re-run → `HEROs_and_PASSes/pass_c_rho/PASS_C_*` |
---

## Three-step assignment (step 1 only)

0. Draw latent abilities **A_i**  
1. Draw team targets **T_j** (e.g. Uniform on [−0.5, 0.5])  
2. Sequential soft match with roster caps:

\[
\pi_{ij} \propto \exp\left(-\rho \cdot \frac{(A_i - T_j)^2}{2\sigma^2}\right) \times (n_j + k)^\alpha
\]

Optional preferential attachment: **`USE_PREFERENTIAL_ATTACHMENT = True`** → **α > 0**; default **False**.

| ρ | Meaning |
|---|---------|
| **ρ = 0** | Uniform among teams with roster room (max **mixing**) |
| **ρ = 1** | Moderate assortativity (≡ legacy **τ = σ ≈ 0.65**) |
| **ρ high** | Sharper match to nearest **T_j** |
| **sort-and-chop** | Separate code path — 537-style global sort + equal slices; **max assortativity benchmark**, not ρ→∞ |

**σ** (`ASSIGNMENT_SIGMA`, default **0.65**) is a fixed scale — not the user-facing knob.

Legacy docs use **τ (temperature)** with **opposite** intuition (small τ = assortative). **540+ uses ρ only** in prose and exports.

---

## Hero estimand lock

| Field | Value |
|-------|-------|
| Outcome | `Y_draft`, mean draft rate per bin |
| X (hero) | `poolq_loo` |
| Bins | 16 quantile |
| Winsor | (0.01, 0.99) |
| min_minutes | 20 |
| Seasons | 2011–2021 |

Slug: `empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011`

---

## Active files

| Role | Path |
|------|------|
| Empirical | `530_sports_pipeline.ipynb`, `sports_pipeline/` |
| Sim engines | `tier1_pool_assignment.py`, `tier1_generative_eda.py`, `tier1_sim_config.py` |
| Pass A bundle | `scripts/pass_a_empirical_bundle.py` → `re_entry/HEROs_and_PASSes/pass_a/PASS_A_*` |
| Pass B bundle | `scripts/pass_b_generative_knockout_bundle.py` → `re_entry/HEROs_and_PASSes/pass_b/PASS_B_*` |
| Pass C bundle | `scripts/pass_c_rho_ablation_bundle.py` → `re_entry/HEROs_and_PASSes/pass_c_rho/PASS_C_*` |
| Notebook | `540_three_step_sim.ipynb` |
| Binding | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` |
| Slide | `3-Master_Plan/re_entry/Model.pdf` |

---

## Export naming

```
3-Master_Plan/re_entry/HEROs_and_PASSes/
  README.txt                     # subfolder index
  pass_a/                        # PASS_A_*, HERO_*
  pass_b/                        # PASS_B_* (λ knockout / ablation)
  pass_c_rho/                    # PASS_C_* (ρ ablation)
  sort_chop_lambda/              # λ threshold diagnostics
  theta/                         # θ sweeps
  slides/                        # PASS_ABC, CHAR_*, So_Far_.pptx
```

---

## Anti-patterns

- Opening `archive/` notebooks as the daily workspace  
- Merging **L_net** and **S_i** in comments or claims  
- Saying ρ ablation **proves** hero bin-for-bin match  
- Using τ in new user-facing text (archive reference only)

---

## When stuck

| Question | Read |
|----------|------|
| What are we proving? | `re_entry/02`, `Model.pdf` |
| Assignment math (legacy τ) | `documents/Tier1_Presorting_Design_Note.md` |
| Widget-era manual | `documents/538_Cell10_Generative_Manual.md` (archive context) |
| Implementation | `tier1_pool_assignment.py` — `soft_assign`, `simulate_generative_rosters` |
