# Pipeline Config Overview (Revolution Version)

## Cell Flags
- `CELL0`: Library imports / setup
- `CELL1`: Load raw snapshots → `df_pipeline_01_raw`
- `CELL2`: Basic filtering → `df_pipeline_02_base`
- `CELL3`: Add year group → `df_pipeline_03_base`
- `CELL4`: Assign OERs (fwd/bwd) → `df_pipeline_04a_basic_metrics`
- `CELL5_POOL_MEANS`: Pool means/minus-means/sizes → `df_pipeline_05_pool_means`
- `CELL6_POOL_RANKS`: Pool ranks/pct/z‑scores → `df_pipeline_06_pool_ranks`
- `CELL7`: Time‑varying variables → `df_pipeline_07_time_varying`
- `CELL8`: Static variables → `df_pipeline_08_combined`
- `CELL9`: Advanced filtering → `df_pipeline_09_filtered`
- `CELL10`: Cox prep → `df_pipeline_10_cox_ready`
- `CELL11`: Cox analysis → `df_pipeline_11_cox_analysis`
- `CELL12`: Cox models → `df_pipeline_12_01_prepared`

## OER Assignment Settings
- `NEW_OER_TB_VALUE`: TB threshold (default 70)
- `NEW_OER_USE_TQDM`: progress bar toggle
- `CELL6_COLUMN_MAPPING`: column mapping for snapshots/OERs

## Pool Metrics Settings
- `POOL_MIN_SIZE`: minimum pool size
- `POOL_EXCLUDE_SELF`: exclude officer from pool mean
- `POOL_RANK_METHOD`, `POOL_RANK_ASCENDING`, `POOL_Z_EPS`

## Column Config
- `COLUMN_CONFIG['oer_variables']` includes explicit fwd/bwd columns and pool metrics.

## Run Overrides (16_1, 16_2, 16_3)

- Run-specific overrides: `pipeline_config_16_1.py`, `pipeline_config_16_2.py`, `pipeline_config_16_3.py`.
- The notebook sets `pip_config_file` (e.g. `'pipeline_config_16_1'`); Cell 0 reloads the base config then the override.

### Run profile (one place for scale + variables)

Overrides can use **RUN_SCALE** and **RUN_PROFILE** so one place controls raw vs z and which variables the run uses:

- **RUN_SCALE:** `'raw'` or `'z'` — drives model columns, CR plots, interaction plots, and (via `expand_run_profile()`) standardization and quadratics.
- **RUN_PROFILE:** dict with `tv_vars`, `quadratic_bases`, `interaction_name`, `plot_prefix`, optional `var_x_label`/`var_y_label`, and **`cr_plot_defaults`**.
- **expand_run_profile(RUN_SCALE, RUN_PROFILE):** Fills `STANDARDIZE_CONFIG`, `model_time_varying_cols`, `QUADRATIC_CONFIG['terms']`, `INTERACTION_CONFIG`, and automated **PLOT_CONFIG['plots']** (one CR plot per tv_var + interaction). Call in override: `globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))`.
- **RUN_CR_PLOT_DEFAULTS:** Dict of CR plot options (e.g. `n_bins`, `bin_method`). Pass as `'cr_plot_defaults': RUN_CR_PLOT_DEFAULTS` in RUN_PROFILE so all automated CR plots share these settings (change bins etc. in one swipe).
- **USE_OVERRIDE_CR_PLOTS:** If `True`, the override replaces `PLOT_CONFIG['plots']` with an explicit list (so you can edit per-plot). If `False` (default), automated plots from `expand_run_profile()` are used. In the override, a commented example shows how to override bins for one plot: `{**RUN_CR_PLOT_DEFAULTS, 'n_bins': 5, 'variable': ..., 'name': ...}`.
- **USE_Z_FOR_RUN:** Set by `expand_run_profile()` when RUN_SCALE is `'z'`; notebook can use it for plot scale if needed.

All three overrides (16_1, 16_2, 16_3) use this pattern: RUN_SCALE, RUN_CR_PLOT_DEFAULTS, RUN_PROFILE (with `cr_plot_defaults`), `expand_run_profile()`, USE_OVERRIDE_CR_PLOTS, and an optional explicit CR plot list (16_1 raw; 16_2/16_3 z-scale with z_ column names in the override list when USE_OVERRIDE_CR_PLOTS is True).

## Plot Config Additions
- `plot_cif_bars`: enable CIF bar plots for CR plots.
- `cif_bar_legend_outside`: legend placement for CIF bars.
- `show_metadata_cards`: inline metadata cards in Cell 11.
- `include_z_cols`: auto-include z-columns in plots when enabled.
