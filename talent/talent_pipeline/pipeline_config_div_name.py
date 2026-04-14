"""
pipeline_config_div_name.py
----------------------------
Run 1 profile with **div_name** in the model and division-aware CR plots.

In **Cell 0** of 520 set:
    pip_config_file = 'pipeline_config_div_name'

Requires: DIVISION_CONFIG merge + re-run CELL 7→9→10 so df_cox carries div_name.
Optional PDE lookup (if you build it in 503): set DIVISION_CONFIG['uic_div_lookup_file']
    to 'df_uic_div_lookup_pde' and ensure that feather exists.
"""

from pipeline_config import *

# RUN 1: Individual TB ratio vs pool minus mean (one place for scale + variables).
# Set RUN_SCALE to 'raw' or 'z' to control model, CR plots, PE plots, and interaction plots.

RUN_SCALE = 'z'

# One-swipe defaults for all CR plots (used by automated plots and by individual plots when USE_OVERRIDE_CR_PLOTS is True)
# Keep default group_by None so only plots that override it use div_name.
RUN_CR_PLOT_DEFAULTS = {
    'group_by': None,
    'plot_type': 'competing_risks',
    'bin_continuous': True,
    'n_bins': 8,
    'cif_bar_hspace': 0.1,
    # Key name must match cox_plot_helpers.plot_competing_risks_cif_bars (cif_bar_show_legend)
    'cif_bar_show_legend': False,  # set True to show legend on CIF bar plots
    'bin_method': 'equal_width',
    'min_group_size': 3,
    'use_time_varying': True,
    'filter_zero_oer': True,
    'filter_nan_variable': True,
    'filter_nan_group_by': True,
    'strict_equal_n': False,
    'x_min_days': None,
    'x_max_days': 4500,
    'bin_group_by': True,
    'group_bins': 3,
    'group_bin_method': 'equal_width',
}

# Quadratics: set in one place here via quadratic_bases. Order of operations (in Cell 10.5): raw → square → then z-score the square if RUN_SCALE is 'z'.
# combined_effect_base: which quadratic gets the 12.6A plot (must be in quadratic_bases); default is quadratic_bases[0].
RUN_PROFILE = {
    'tv_vars': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'quadratic_bases': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'combined_effect_base': POOL_MINUS_MEAN_SNR_COL,  # 12.6A plot: pool minus mean (not TB ratio)
    'interaction_name': 'star_pool_interaction',
    'plot_prefix': 'run1',
    'var_x_label': 'TB ratio',
    'var_y_label': 'Pool minus mean',
    'cr_plot_defaults': RUN_CR_PLOT_DEFAULTS,
    # Optional: one-swipe control (expand_run_profile applies these)
    'winsorize': {'enabled': False},  # turn off for e.g. [90, 100] interaction zoom
    'interaction_percentile_range': [0, 100],  # zoom to high-high corner
    'interaction_log_z': False,  # log scale for hazard ratio (z-axis / color)
    'interaction_log_xy': False,  # log scale x and y axes (only when both axes > 0, e.g. raw)
    # 1D slice: fix x at top (e.g. super top-block ratio); plot HR vs y over tip-top pool range
    'interaction_slice_x_at': None,  # 'max' or e.g. 99 for 99th percentile; None = no slice
    'interaction_slice_y_range': None,  # e.g. [90, 100]
}
globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))

# --- div_name + model columns ---
# Any other time-varying categorical for Cox: append to EXTRA_TIME_VARYING_COLS (or model list), add an entry
# under COLUMN_CONFIG['dummy_variables']['categorical_cols'], and if Cell 10 uses string forward-fill, add the
# name to string_fill_cols in 520 Cell 10 next to div_name. Use extra_survival_tv_cols only for carry-only cols.

# --- Extra time-varying columns (div_name, etc.). For static (e.g. yg) use EXTRA_STATIC_COLS below. ---
# These are carried into df_cox (Cell 10) and the Cox model; div_* dummies appear in top-15 signal ratios (Cell 12.4).
EXTRA_TIME_VARYING_COLS = ['div_name']
COLUMN_CONFIG['model_time_varying_cols'] = (
    list(COLUMN_CONFIG.get('model_time_varying_cols', [])) + EXTRA_TIME_VARYING_COLS
)

# Dummies required for categoricals (div_name, yg, etc.); base config has create_dummies False
COLUMN_CONFIG['dummy_variables']['create_dummies'] = True

# Ensure override wins: force winsorize off for this run (so [90,100] interaction zoom has spread)
# STANDARDIZE_CONFIG['winsorize']['enabled'] = RUN_PROFILE.get('winsorize', {}).get('enabled', True)
# print_v(f"Winsorize enabled: {STANDARDIZE_CONFIG['winsorize']['enabled']}")

# Static: none in model for this run. To add yg (static), use EXTRA_STATIC_COLS and append to model_static_cols.
COLUMN_CONFIG['model_static_cols'] = []
# EXTRA_STATIC_COLS = ['yg']  # optional; then: COLUMN_CONFIG['model_static_cols'] += EXTRA_STATIC_COLS

# Use explicit CR plots (TB ratio by div_name, etc.) when True; when False, automated plots from expand_run_profile()
USE_OVERRIDE_CR_PLOTS = True

if USE_OVERRIDE_CR_PLOTS:
    # Variable names in data: z_ when RUN_SCALE='z', else raw
    # Individual CR plots (edit per-plot here; common settings come from RUN_CR_PLOT_DEFAULTS)
    _cr_var_tb = Z_TB_RATIO_SNR_COL if RUN_SCALE == 'z' else TB_RATIO_SNR_COL
    _cr_var_pool = (
        f'{Z_PREFIX}{POOL_MINUS_MEAN_SNR_COL}' if RUN_SCALE == 'z' else POOL_MINUS_MEAN_SNR_COL
    )
    PLOT_CONFIG['plots'] = [
        {**RUN_CR_PLOT_DEFAULTS, 'variable': _cr_var_tb, 'name': 'run1_cr_' + _cr_var_tb},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': _cr_var_pool, 'name': 'run1_cr_' + _cr_var_pool},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': 'star_pool_interaction', 'name': 'run1_cr_star_pool_interaction'},
        # TB ratio (z or raw) for filter_nan_variable / OER filters; curves = one per div_name (no variable bin).
        {
            **RUN_CR_PLOT_DEFAULTS,
            'variable': _cr_var_tb,
            'bin_continuous': False,  # skip useless binning; see group_only_curves
            'group_by': 'div_name',
            'group_only_curves': True,
            'exclude_unknown_div_name': True,  # omit Unknown/missing div for this plot only; base PLOT_CONFIG default is False
            # CR + CIF bar colors: husl/tab20/glasbey/set1 (see cox_plot_helpers.cr_discrete_group_colors). husl = most distinct for many groups.
            'cr_color_mode': 'husl',
            # CIF bars: tick labels = division when group_only_curves + group_by (or set cif_bar_xtick_labels to 'group' / 'quantile')
            'cif_bar_show_xlabels': True,
            'name': 'run1_cr_tb_by_div',
        },
    ]

# Filtering parameters for RUN 1
CA = ['IN', 'AR', 'EN', 'AV', 'FA', 'SF', 'AD']  # 7 branches
# CA = ['IN', 'AR', 'EN', 'AV', 'FA', 'AD']  # 6 branches (omit SF)
CS = ['CM', 'CA', 'MI', 'MP', 'SC']
CSS = ['AG', 'FI', 'OD', 'QM', 'TC', 'LG']

filtering_params['filter_dates'] = {
    'enabled': False,
    'start_date': '2000-01-01',
    'end_date': '2022-06-30',
}
filtering_params['filter_job_codes'] = {
    'enabled': True,
    'exclude_problematic': True,
    'problematic_codes': ['MC', 'DC', 'VC', 'SP', 'AN', 'JA', 'CH', 'MS'],
    'include_specific': CA + CS + CSS,
    'include_only_specific': True,
    # False = allow officers who had other job codes during CPT time; True = exclude them (CPT-only job code history)
    'exclude_other_jobs_during_target_rank': False,
}

# Year group filtering
filtering_params['filter_ygs'] = {
    'enabled': True,  # Set True to enable year group filtering
    'include_specific': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011],
    'exclude_specific': None,  # e.g., [2000, 2001] or None to exclude specific YGs
}

# --- Division: compute (CELL 7) and use (CELL 9) ---
# (1) DIVISION_CONFIG['enabled'] = True so CELL 7 creates div_name and division metrics;
# (2) filter_divisions['enabled'] = True so CELL 9 applies division filtering.
# CELL 7 & CELL 9 must be True in base pipeline_config (they are by default).
# For div_name in df_cox / Cell 11: re-run from CELL 7 so 08/09 are rebuilt with div_name, then 10, 10.5, 11.
filtering_params['filter_divisions'] = {
    'enabled': True,
    'gtw_only': False,  # Set True to include only GTW (Go To War) units
    'prestige_only': False,  # Set True to include only prestige units
    'include_divisions': None,  # e.g. ['101ABN', '82ABN'] or None for all
}

# Enable division name + metrics so div_name exists for filtering and CR plots (CELL 7)
DIVISION_CONFIG['enabled'] = True

# If you use PDE-keyed division lookup from 503:
DIVISION_CONFIG['uic_div_lookup_file'] = 'df_uic_div_lookup_pde'
DIVISION_CONFIG['backfill_early_fy'] = True
# Use earliest FY present in lookup table as floor for all prior years.
DIVISION_CONFIG['backfill_fy'] = 'lookup_min'
# Temporary diagnostics to trace UIC/FY join coverage and missing div_name causes.
DIVISION_CONFIG['debug_division'] = True

# Optional: keep legacy OER column in time_varying_cols for this run
if 'tb_ratio_bwd_snr_legacy' not in COLUMN_CONFIG['oer_variables']:
    COLUMN_CONFIG['oer_variables'].append('tb_ratio_bwd_snr_legacy')

# time_varying_cols = base + oer + prestige + model_time_varying_cols so Cell 10 carries all model TV cols into df_cox.
# Cell 10 MUST use model_time_varying_cols here (not base_time_varying_cols) so div_name and interactions are carried.
_tv_base = (
    COLUMN_CONFIG.get('base_time_varying_cols', [])
    + COLUMN_CONFIG.get('oer_variables', [])
    + COLUMN_CONFIG.get('prestige_variables', [])
)
_model_tv = COLUMN_CONFIG.get('model_time_varying_cols', [])
COLUMN_CONFIG['time_varying_cols'] = list(dict.fromkeys(_tv_base + _model_tv))

PLOT_CONFIG['show_metadata_cards'] = True
