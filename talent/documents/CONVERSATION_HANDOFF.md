# Conversation Handoff (Technical Summary)

Use this doc when starting a new Cursor thread so the next session has context. Research background: add in your first message if needed.

---

## What We Fixed (This Session)

### Run profile and CR plot simplification (config + overrides)
- **Base config:** Added `expand_run_profile(run_scale, run_profile)` so one place sets model vars, standardization, quadratics, interaction config, and automated CR plots. Run profile can include **`cr_plot_defaults`** (e.g. `n_bins`, `bin_method`); these are merged into each automated CR plot so you can change bins for all plots in one swipe. Added **USE_OVERRIDE_CR_PLOTS** (default False); when True, override uses its explicit CR plot list.
- **Overrides (16_1, 16_2, 16_3):** All use RUN_SCALE, RUN_CR_PLOT_DEFAULTS, RUN_PROFILE with `cr_plot_defaults`, `expand_run_profile()`, and USE_OVERRIDE_CR_PLOTS. Default is automated CR plots; optional explicit list with commented example for per-plot override (e.g. `{**RUN_CR_PLOT_DEFAULTS, 'n_bins': 5, 'variable': ..., 'name': ...}`). 16_1 is raw; 16_2/16_3 are z-scale (override plot list uses z_ column names when USE_OVERRIDE_CR_PLOTS is True).
- **Notebook (520):** **Cell 11** — add every column in `model_time_varying_cols` that exists in `df_cox` to `analysis_cols` so interaction/quadratic columns are in `df_analysis` and CR plots find them. **Cell 12.6A** — detect linear+quadratic pair from `final_model_vars` (or optional `COMBINED_EFFECT_BASE_COL`) instead of hardcoding; skip message when no pair found.

### Backward CIF flattening
- **Symptom:** Competing-risks CIF curves for `tb_ratio_bwd_snr` were nearly flat (~0.41–0.46) while forward and legacy showed clear separation.
- **Cause:** Backward paint uses the *next* OER’s eval_thru_dt. For CR plots we use *last snapshot per officer*; in **58.7%** of officers, `eval_thru_dt_bwd` was **after** that last snapshot, so the covariate was future-looking relative to the event → curves flattened.
- **Conclusion:** Backward algorithm is correct; the misalignment is between “last snapshot” and “eval that defines the backward score.” Not a bug in the backward logic itself.

### Time-alignment diagnostic
- Added `eval_thru_dt_bwd` and `snpsht_dt` to the pipeline so we can compute “% where eval_thru_dt_bwd > snpsht_dt” in Cell 11 (`prepare_plot_data`). Debug line: `DEBUG bwd time alignment: missing_eval_thru_dt=..., eval_thru_dt_bwd after snpsht_dt=...`
- **Config:** `pipeline_config.py` — `eval_thru_dt_bwd` in `oer_variables`, `snpsht_dt` in `base_time_varying_cols`.

### Duplicate columns / merge suffixes
- Snapshot table sometimes had prior run’s fwd/bwd columns → merge created `_x`/`_y` and duplicate names → `to_datetime` failed.
- **Fix in `add_cum_oer_metrics_mod_working.py`:** (1) Drop previously-generated columns from `snaps`/`oers` at entry; (2) After merging fwd with bwd, detect duplicate column names and drop duplicates (with a warning). Also guard `_normalize_date_col` when `df[col]` is a DataFrame (duplicate names).

### merge_asof sort order
- Tried sorting by `[pid, date]` for merge_asof; pandas required the *on* key to be sorted, so we reverted to `[snapshot_date_col, pid_col]` (and same for oers) to avoid “MergeAsof only supports left/right keys sorted in ascending order.”

### Terminology
- **Verb for attrition:** “attrit” (not “attrite”).
- **S(u-):** Survival function just *before* time u (left limit); used in CIF formula so the risk set is defined before events at u.

---

## Key Decisions

- **Forward vs backward:** For CR plots (last snapshot), forward painting is time-aligned and gives sensible separation. Backward can stay in the pipeline for Cox (all intervals) or for CR only with a time-alignment guard (`eval_thru_dt_bwd <= snpsht_dt`).
- **Option chosen (user):** Use forward for individual (and optionally forward for pools) for now; user can toggle in `pipeline_config.py` via `TB_ASSIGNMENT_MODE` / `TB_ASSIGNMENT_MODE_SELF` / `TB_ASSIGNMENT_MODE_POOL`.
- **CR vs hazard:** CR/CIF plots show *cumulative* probability (not instantaneous risk). The *instantaneous* quantity is the hazard; Cox and HR plots are the right place for that. See `current_documents/CR_AND_HR_FOR_DUMMIES.md`.

---

## Files Touched

- **`add_cum_oer_metrics_mod_working.py`:** Pre-clean of generated columns; post-merge duplicate column drop; `_normalize_date_col` guard; `debug_bwd` and time-alignment debug prints; optional `eval_thru_dt_bwd`/`snpsht_dt` in downstream data only if included in config.
- **`pipeline_config.py`:** `eval_thru_dt_bwd` in `oer_variables`; `snpsht_dt` in `base_time_varying_cols`; `TB_ASSIGNMENT_MODE` set to `'forward'` at one point (user can switch). **Later:** Run profile system (`RUN_SCALE`, `RUN_PROFILE`, `expand_run_profile()`, `USE_OVERRIDE_CR_PLOTS`); `cr_plot_defaults` merged into automated CR plots; removed `tb_ratio_bwd_snr_legacy` and `eval_thru_dt_bwd` from base `oer_variables`.
- **`520_pipeline_cox_working.ipynb`:** **(Cell 11)** Debug slice, time-alignment line; **and** add `model_time_varying_cols` to `analysis_cols` so interaction/quadratic columns exist in `df_analysis` for CR plots. **(Cell 12.6A)** Combined-effect plot: detect linear+quadratic pair from `final_model_vars` (or `COMBINED_EFFECT_BASE_COL`) instead of hardcoding; skip message when no pair found.
- **`pipeline_config_16_1.py`, `pipeline_config_16_2.py`, `pipeline_config_16_3.py`:** Refactored to use RUN_SCALE, RUN_PROFILE, expand_run_profile(), RUN_CR_PLOT_DEFAULTS, USE_OVERRIDE_CR_PLOTS (16_1 raw; 16_2/16_3 z).
- **`current_documents/CR_AND_HR_FOR_DUMMIES.md`:** Full “for dummies” plus formal formulas (CIF, hazard, Cox, HR, partial effects), worked examples with quadratics and competing risks, numeric example with mini SVG plot, S(u-) note. Use for re-acquainting with CR vs HR.

---

## Pipeline Quick Ref

- **Cell 0:** Reload config (and modules). Override via `pip_config_file` (e.g. `pipeline_config_16_1`).
- **Cell 4:** OER assignment → fwd/bwd cum evals, TB counts, ratios. Output: e.g. `df_pipeline_04a_basic_metrics`.
- **Cell 5:** Pool means, minus-means, sizes (fwd/bwd).
- **Cell 6:** Pool ranks, percentiles, z-scores.
- **Cell 10:** Survival intervals (`start_time`, `stop_time`, `event`); time-varying and static cols from config.
- **Cell 10.5:** Z-scores, interactions, quadratics (if enabled).
- **Cell 11:** CR/CIF plots; collapses to *last snapshot per officer*; uses `prepare_plot_data` → `plot_competing_risks` / `plot_competing_risks_cif_bars`.
- **Cell 12:** Cox fit, HR and partial-effects plots (use *all* intervals).

Override configs (e.g. `pipeline_config_16_1.py`) can use **RUN_SCALE** + **RUN_PROFILE** + `expand_run_profile()` so one place sets model vars, standardization, quadratics, interaction config, and automated CR plots. Optional **RUN_CR_PLOT_DEFAULTS** and **USE_OVERRIDE_CR_PLOTS** control CR plot defaults and per-plot overrides. If an override adds to `oer_variables` (e.g. legacy), it must rebuild `time_varying_cols` at the end.

---

## current_documents/ (all current — none obsolete)

All `.md` files here are **in use**. Use these for reference; do not treat as obsolete.

| File | Purpose |
|------|--------|
| **CONVERSATION_HANDOFF.md** | This file. Technical handoff for new Cursor threads. |
| **CR_AND_HR_FOR_DUMMIES.md** | Plain-English + formulas: CIF vs hazard, Cox, HR, partial effects, quadratics, competing risks, numeric example, mini plot. Primary ref for CR/HR concepts. |
| **520_PIPELINE_COX_OVERVIEW.md** | Main pipeline doc: cells, flow, inputs/outputs, algorithmic detail, forward/backward, checkpoints. |
| **PIPELINE_CONFIG_OVERVIEW.md** | Config layout, overrides, run-specific configs (e.g. 16_1–16_3). |
| **COX_PLOT_HELPERS_OVERVIEW.md** | Plot helpers: CIF curves, CIF bars, Kaplan–Meier, partial effects, filenames. |
| **PROCESS_NOTES_RAW_VS_STANDARDIZED.md** | When to use raw vs z-scores, pool metrics, quadratics, collinearity-aware order, spline vs quadratic. |
| **DECISION_CHART_RAW_VS_ZSCORE.md** | One-page decision flow: raw vs z, rank vs percentile, quadratic rules. |
| **ADD_CUM_OER_METRICS_OVERVIEW.md** | OER assignment and pool metrics: `add_cum_oer_metrics_mod_working.py`, fwd/bwd, pool means/ranks. |
| **JOIN_OER_TO_SNAPSHOTS_OVERVIEW.md** | How OERs are joined to snapshots (merge logic, dates). |
| **METRICS_COLUMNS_OVERVIEW.md** | Column names and roles (TB ratio, pool, rank, etc.). |
| **CELL6_OPTIMIZATION_RECOMMENDATIONS.md** | Cell 6 performance and optimization. |
| **CELL6_SPLIT_GUIDE.md** | How Cell 6 is split (pool means vs ranks). |
| **CELL6_FLOW_AND_OPTIMIZATION_GUIDE.md** | Cell 6 flow and optimization in one place. |
| **PIPELINE_RUN_ORDER.md** | Order to run pipeline steps/cells. |
| **INIT_RAY_CLUSTER_OVERVIEW.md** | Ray cluster setup if used. |
| **add_variable_to_plots_guide.md** | How to add a variable to plotting (config + notebook). |
| **502_DATA_PREP_OVERVIEW.md** | Data prep (502) overview. |
| **COX_METHODS_BRIEF.md** | Short Cox/methods reference. |
| **PDF_CONVERSION_GUIDE.md** | Converting .md to PDF (e.g. `convert_single_md_to_pdf.sh`). |
| **TEMP_STAR_POOL_RUNS.md** | Temporary notes on star/pool runs. |
| **SHOW_ME_INTERPRETATION.md** | Interpretation notes for results. |
| **SHOW_ME_INTERPRETATION_DECK.md** | Deck-style interpretation. |
| **COUNTERINTUITIVE_RESULTS_AND_RUNS.md** | Notes on counterintuitive results and runs. |
| **elementary results.md** | Elementary/foundational results. |
| **DIFFERENT_PLOT_COMPARISONS.md** | Comparing different plot types/settings. |

**Also in current_documents:** `hr_quad_example.svg` — mini plot used inside CR_AND_HR_FOR_DUMMIES.md.

---

## obsolete_documents/ (archived — superseded by current_documents)

**Do not use for current work.** These are older or superseded versions. Refer to `current_documents/` for the active docs.

- **Pipeline/overview:** e.g. `520_PIPELINE_COX_OVERVIEW.md`, `520_PIPELINE_COX_OVERVIEW_root.md`, `PIPELINE_CONFIG_OVERVIEW.md`, `COX_PLOT_HELPERS_OVERVIEW.md`, `METRICS_COLUMNS_OVERVIEW.md`, `ADD_CUM_OER_METRICS_OVERVIEW.md`, `JOIN_OER_TO_SNAPSHOTS_OVERVIEW.md`, `502_DATA_PREP_OVERVIEW.md` (older copies).
- **Cell-specific:** e.g. `CELL6_*`, `CELL10_DIAGNOSTIC_CHANGES.md`, `CELL11_*`, `CELL12_*`, `CELL8_*`, logging/split/optimization guides (superseded by current_documents versions).
- **Other:** `CUMULATIVE_OER_METRICS_OVERVIEW.md`, `512_OER_INTEGRATION_OVERVIEW.md`, `QUICK_USAGE_GUIDE.md`, `PLOT_ENHANCEMENT_EXAMPLES.md`, `FINAL_UPDATES_SUMMARY.md`, `READY_FOR_UPLOAD.md`, `MODULARIZATION_PLAN.md`, `TEMPORAL_SYNCHRONIZATION.md`, `511_cursor_28oct_down_temp.md`, etc.

---

## obsolete_files/ (archived code and data — not for active runs)

**Do not use for current pipeline.** Backup/superseded notebooks, scripts, and data.

- **Notebooks:** e.g. `520_pipeline_cox_working_*.ipynb` (dated backups), `511_cursor*.ipynb`, `510_*.ipynb`, `508_*`, `502_*`, `Test_nb.ipynb`, `Cursor_PDE.ipynb`.
- **Python:** e.g. `add_cum_oer_metrics_mod_working.py` (old), `pipeline_config_*_bkup.py`, `join_oer_to_snapshots*.py`, `temporal_matching_utils.py`, `analysis_promotion.py`, `centrality_analysis.py`, `functionsG*.py`, temp cell snippets.
- **Data/other:** e.g. `officer_*_survival_data.csv`, `advanced_analysis_results.json`.

Active pipeline uses the **root-level** `520_pipeline_cox_working.ipynb`, `add_cum_oer_metrics_mod_working.py`, `pipeline_config.py`, etc., not the copies in `obsolete_files/`.

---

## Open Threads / Next Steps

- If using **forward for individual and backward for pools:** expect individual CR plots to look good; pool CR plots may still flatten unless a time-alignment guard is applied for pool variables.
- Optional: add time-alignment filter in `prepare_plot_data` for _bwd variables (e.g. keep only rows with `eval_thru_dt_bwd <= snpsht_dt`) as an option controlled by config or plot_spec.
- User may remove or reduce debug prints in Cell 11 and `add_cum_oer_metrics_mod_working.py` once satisfied.

---

*End of handoff. Paste this (and optionally a short research context) into the first message of a new conversation.*
