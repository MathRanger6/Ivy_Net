# 520 Full Rebuild Checklist — Run 17_1

**Purpose:** Printable step-by-step guide to run a **full end-to-end rebuild** of the Army Cox pipeline using **`pipeline_config_17_1`** (Run 1: z-scored TB ratio × pool minus mean).

**Notebook:** `talent/talent_pipeline/520_pipeline_cox_working.ipynb`  
**Also valid path:** `talent_pipeline/520_pipeline_cox_working.ipynb` (repo-root symlink — same files)

**Last updated:** 2026-09-17

---

## Before you start

- [ ] Jupyter **working directory** is **`talent/talent_pipeline/`** (checkpoints save to `./running_vars/` next to the notebook).
- [ ] You have enough disk/RAM for a full run (Cells 4–6 are the heaviest; see `520_PIPELINE_COX_OVERVIEW.md` § Memory).
- [ ] Ground truth code is **`talent/talent_pipeline/`**, not a stale copy under `Army_AWS_download/` unless you just merged from AWS.

---

## The three control knobs (where to edit what)

| What you want | File | Where |
|---------------|------|--------|
| **Pick run recipe (17_1)** | `520_pipeline_cox_working.ipynb` | **Cell 0** → `pip_config_file = 'pipeline_config_17_1'` |
| **Full vs partial rebuild** | `pipeline_config.py` | **§1** → `CELL1` … `CELL12_8` flags (`True` = run) |
| **Run 1 filters / model / plot names** | `pipeline_config_17_1.py` | Usually **leave as-is** for standard Run 1 |

**Not automatic:** Creating `pipeline_config_XX_Y.py` does **not** run it. Only **`pip_config_file` in Cell 0** selects the override.

**Output naming:** Set by **`plot_prefix`** in `17_1`’s `RUN_PROFILE` (default `'run1'` → e.g. `run1_cr_z_tb_ratio_fwd_snr`).

---

## Phase A — Upstream data (if feathers missing or stale)

Run these **before** 520 if `./running_vars/` lacks the inputs.

### A1. Snapshot base — `502_working.ipynb`

- [ ] Open `502_working.ipynb` (same folder as 520).
- [ ] Run through to produce **`df_502_base.feather`** in `./running_vars/`.

### A2. OER enrichment — `512_oer_int_working.ipynb`

- [ ] Open `512_oer_int_working.ipynb`.
- [ ] Run **Cells 0–3** (minimum) to produce **`df_oer_enriched.feather`** in `./running_vars/`.
- [ ] 520 Cell 4 **requires** this file; it will error with instructions if missing.

### A3. Verify inputs exist

- [ ] `./running_vars/df_502_base.feather`
- [ ] `./running_vars/df_oer_enriched.feather`

---

## Phase B — Base config: turn on full rebuild

**File:** `talent/talent_pipeline/pipeline_config.py`  
**Section:** `=== 1. CELL EXECUTION FLAGS ===` (top of file)

Set **every flag below to `True`** for a full rebuild:

### Phase 1 — Load & prep

- [ ] `CELL1 = True`   — Load raw snapshots
- [ ] `CELL2 = True`   — Basic filtering
- [ ] `CELL3 = True`   — Year group (yg)

### Phase 2 — OER & pools

- [ ] `CELL4 = True`   — OER merge + individual fwd/bwd metrics
- [ ] `CELL5_POOL_MEANS = True`   — Pool means / minus-means / sizes
- [ ] `CELL6_POOL_RANKS = True`   — Pool ranks / percentiles / z-scores

### Phase 3 — Variables

- [ ] `CELL7 = True`   — Time-varying variables (incl. div_name when 17_1 enables it)
- [ ] `CELL8 = True`   — Static variables

### Phase 4 — Filter

- [ ] `CELL9 = True`   — Advanced filtering (17_1: division filter on)

### Phase 5 — Cox

- [ ] `CELL10 = True`      — Cox interval prep
- [ ] `CELL10_5 = True`   — Standardize + interactions + quadratics
- [ ] `CELL10_5S = False`  — Splines (leave False unless experimenting)
- [ ] `CELL11 = True`      — CR/CIF plots
- [ ] `CELL12 = True`      — Cox models

### Cell 12 sub-steps

- [ ] `CELL12_1 = True`   — Prepare Cox data
- [ ] `CELL12_2 = True`   — Static model
- [ ] `CELL12_3 = True`   — Full model
- [ ] `CELL12_4 = True`   — Model comparison / signal ratios
- [ ] `CELL12_5 = True`   — Competing risks
- [ ] `CELL12_6 = True`   — Partial effects
- [ ] `CELL12_7 = True`   — Interaction **3D surfaces**
- [ ] `CELL12_8 = True`   — Model-based curves

### Optional pre-run

- [ ] `RUN_503 = False` — Set **`True`** only if you need to rebuild prestige UIC lists (`py_503_hierarchies.py`) before Cell 7.

**Note:** `CELL0` in config is legacy; the notebook Cell 0 block for lookup tables is commented out — ignore for normal runs.

**Save** `pipeline_config.py`.

---

## Phase C — Select Run 17_1 in the notebook

**File:** `520_pipeline_cox_working.ipynb`  
**Cell:** **Cell 0** (imports + config load)

- [ ] Set:
  ```python
  pip_config_file = 'pipeline_config_17_1'
  ```
  (module name only — **no** `.py`)

- [ ] **Run Cell 0.** Confirm printed module name is `pipeline_config_17_1`.

### Cell 1 inline option (same notebook, first data cell)

- [ ] Confirm **`load_from_502 = True`** (recommended — uses `df_502_base.feather`).

---

## Phase D — Execute 520

- [ ] **Restart kernel** (optional but clean for a full rebuild).
- [ ] Run **Cell 0**, then **run all cells** through Cell 12 (or Run All).
- [ ] Watch Cell 4 for OER load success; Cells 5–6 for pool metrics; Cell 9 for filter counts.

### Expected checkpoint files (`./running_vars/`)

- [ ] `df_pipeline_01_raw.feather`
- [ ] `df_pipeline_02_base.feather`
- [ ] `df_pipeline_03_base.feather`
- [ ] `df_pipeline_04a_basic_metrics.feather`
- [ ] `df_pipeline_05_pool_means.feather`
- [ ] `df_pipeline_06_pool_ranks.feather`
- [ ] `df_pipeline_07_time_varying.feather`
- [ ] `df_pipeline_08_combined.feather`
- [ ] `df_pipeline_09_filtered.feather`
- [ ] `df_pipeline_10_cox_ready.feather`
- [ ] `df_pipeline_10_5_cox_zscored.feather`
- [ ] `df_pipeline_11_cox_analysis.feather`
- [ ] `df_pipeline_12_01_prepared.feather`

---

## Phase E — Verify outputs

### Plots

- [ ] **`./cox/cox_plots/`** — CR/CIF figures prefixed with **`run1_`** (e.g. `run1_cr_z_tb_ratio_fwd_snr`, pool minus mean, interaction).

### Model / diagnostics

- [ ] **`./cox/cox_results/`** (or paths under `./cox/` per your config) — coefficients CSV, interaction 3D PNG (`interaction_3d_star_pool_interaction_...`).

### Sanity checks

- [ ] Cell 11 completed without “missing variable” errors for `z_tb_ratio_fwd_snr`, `z_pool_minus_mean_snr_fwd`, `star_pool_interaction`.
- [ ] Cell 12.3 full model fitted; 12.7 saved at least one 3D surface.

---

## Phase F — After successful rebuild (optional)

For **faster iteration** next time (Cox/plots only):

- [ ] In `pipeline_config.py`, set **`CELL1` through `CELL6` = `False`** (reuse feathers through Cell 6).
- [ ] Keep **`CELL7`–`CELL12`** as needed (re-run from 7 if you changed division/filter config in 17_1).

---

## What Run 17_1 does (no edits needed for default Run 1)

**File:** `pipeline_config_17_1.py`

| Setting | Value |
|---------|--------|
| `RUN_SCALE` | `'z'` (z-scored model columns) |
| Model TV vars | TB ratio SNR + pool minus mean SNR |
| Interaction | `star_pool_interaction` |
| `plot_prefix` | `'run1'` |
| Quadratics | Both TB ratio and pool minus mean |
| Division | `DIVISION_CONFIG` on; `div_name` in model; division filter in Cell 9 |
| CR plots | Explicit list (`USE_OVERRIDE_CR_PLOTS = True`) |

Edit **`17_1`** only when you want different filters, variables, or `plot_prefix` — not for “run again from scratch.”

---

## Troubleshooting (quick)

| Symptom | Check |
|---------|--------|
| `df_oer_enriched.feather not found` | Run **512** Cells 0–3 |
| `df_502_base.feather not found` | Run **502**, or set `load_from_502 = False` and use DB path in Cell 1 |
| Wrong run / wrong plots | Cell 0 `pip_config_file`; re-run Cell 0 after change |
| Config edit ignored | Re-run cell that calls `reload_pipeline_config()`, or restart kernel + Cell 0 |
| Cells skipped unexpectedly | `pipeline_config.py` CELL flags — must be `True` for full rebuild |
| Empty interaction plot range | 17_1 `interaction_percentile_range`; winsorize settings in `RUN_PROFILE` |

---

## Related docs (deeper reference)

| Doc | Topic |
|-----|--------|
| `520_PIPELINE_COX_OVERVIEW.md` | Full pipeline architecture |
| `PIPELINE_CONFIG_OVERVIEW.md` | CELL flags + RUN_PROFILE |
| `PIPELINE_RUN_ORDER.md` | Checkpoint chain one-liner |
| `README_Talent_Layout_Symlinks_And_AWS_Export.md` | AWS vs local tree |
| `CR_AND_HR_FOR_DUMMIES.md` | Reading CIF vs HR plots |
| `Presentation_Interpretation_Run1_Slides_5-20.md` | Run 1 figure interpretation |

---

## One-page summary

```
1. 502 → df_502_base.feather     (if needed)
2. 512 → df_oer_enriched.feather (if needed)
3. pipeline_config.py → CELL1…CELL12_8 = True
4. 520 Cell 0 → pip_config_file = 'pipeline_config_17_1'
5. 520 Cell 1 → load_from_502 = True
6. Run All 520
7. Check ./cox/cox_plots/run1_* and ./running_vars/df_pipeline_* checkpoints
8. Later: CELL1–6 = False for Cox-only reruns
```

---

*Print this checklist and check boxes as you go.*
