from pipeline_config import *

# RUN 1: Individual TB ratio vs pool minus mean (one place for scale + variables).
# Set RUN_SCALE to 'raw' or 'z' to control model, CR plots, PE plots, and interaction plots.

RUN_SCALE = 'z'

# One-swipe defaults for all CR plots (used by automated plots and by individual plots when USE_OVERRIDE_CR_PLOTS is True)
RUN_CR_PLOT_DEFAULTS = {
    'group_by': None,
    'plot_type': 'competing_risks',
    'bin_continuous': True,
    'n_bins': 8,
    'cif_bar_hspace': 0.1,
    # Key name must match cox_plot_helpers.plot_competing_risks_cif_bars (cif_bar_show_legend)
    'cif_bar_show_legend': False,  # set True to show legend on CIF bar plots (read in cox_plot_helpers)
    'bin_method': 'equal_width',
    'min_group_size': 3,
    'use_time_varying': True,
    'filter_zero_oer': True,
    'filter_nan_variable': True,
    'filter_nan_group_by': True,
    'strict_equal_n': False,
    'x_min_days': 0,
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
    'interaction_percentile_range': None,  # e.g. [0, 100] to zoom high-high corner; None = no zoom
    'interaction_log_z': False,  # log scale for hazard ratio (z-axis / color)
    'interaction_log_xy': False,  # log scale x and y axes (only when both axes > 0, e.g. raw)
    # 1D slice: fix x at top (e.g. super top-block ratio), plot HR vs y over tip-top pool range
    'interaction_slice_x_at': None,  # 'max' or e.g. 99 for 99th percentile; None = no slice
    'interaction_slice_y_range': [90, 100],  # e.g. [90, 100]
}
globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))

# --- Extra time-varying columns (div_name, etc.). For static (e.g. yg) use EXTRA_STATIC_COLS below. ---
# These are carried into df_cox (Cell 10) and the Cox model; div_* dummies appear in top-15 signal ratios (Cell 12.4).
EXTRA_TIME_VARYING_COLS = [
    'div_name',
]
COLUMN_CONFIG['model_time_varying_cols'] = list(COLUMN_CONFIG.get('model_time_varying_cols', [])) + EXTRA_TIME_VARYING_COLS

# Dummies required for categoricals (div_name, yg, etc.); base config has create_dummies False
COLUMN_CONFIG['dummy_variables']['create_dummies'] = True

# Ensure override wins: force winsorize off for this run (so [90,100] interaction zoom has spread)
# STANDARDIZE_CONFIG['winsorize']['enabled'] = RUN_PROFILE.get('winsorize', {}).get('enabled', True)
# print_v(f"Winsorize enabled: {STANDARDIZE_CONFIG['winsorize']['enabled']}")

# Static: none in model for this run. To add yg (static), use EXTRA_STATIC_COLS and append to model_static_cols.
COLUMN_CONFIG['model_static_cols'] = []
# EXTRA_STATIC_COLS = ['yg']  # optional; then: COLUMN_CONFIG['model_static_cols'] += EXTRA_STATIC_COLS

# Use explicit CR plots (TB ratio by div_name, etc.) when True; when False, automated plots from expand_run_profile() are used
USE_OVERRIDE_CR_PLOTS = True
# USE_OVERRIDE_CR_PLOTS = True  # example: set True to use the explicit individual CR plots in the block below

if USE_OVERRIDE_CR_PLOTS:
    # Variable names in data: z_ when RUN_SCALE='z', else raw
    _cr_var_tb = Z_TB_RATIO_SNR_COL if RUN_SCALE == 'z' else TB_RATIO_SNR_COL
    _cr_var_pool = (f'{Z_PREFIX}{POOL_MINUS_MEAN_SNR_COL}' if RUN_SCALE == 'z' else POOL_MINUS_MEAN_SNR_COL)
    PLOT_CONFIG['plots'] = [
        {**RUN_CR_PLOT_DEFAULTS, 'variable': _cr_var_tb, 'name': 'run1_cr_' + _cr_var_tb},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': _cr_var_pool, 'name': 'run1_cr_' + _cr_var_pool},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': 'star_pool_interaction', 'name': 'run1_cr_star_pool_interaction'},
        # TB ratio, 1 bin, grouped by division (div_name in model → in df_cox after Cell 7/10)
        {**RUN_CR_PLOT_DEFAULTS, 'variable': _cr_var_tb, 'n_bins': 1, 'group_by': 'div_name', 'name': 'run1_cr_tb_by_div'},
    ]

# Filtering parameters for RUN 1
CA = ['IN', 'AR', 'EN', 'AV', 'FA', 'SF', 'AD']  # 7 branches
# CA = ['IN','AR','EN','AV','FA','AD']  # 6 branches (omit SF)
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
    'include_specific': None,
    'include_only_specific': True,
    # False = allow officers who had other job codes during CPT time; True = exclude them (CPT-only job code history)
    'exclude_other_jobs_during_target_rank': False,
}

# Year group filtering (must be a dict, not a tuple — no parentheses around the dict, no trailing comma)
filtering_params['filter_ygs'] = {
    'enabled': False,  # Set True to enable year group filtering
    'include_specific': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011],
    'exclude_specific': None,  # e.g. [2000, 2001] or None
}

# --- Division: compute (CELL 7) and use (CELL 9) ---
# (1) DIVISION_CONFIG['enabled'] = True so CELL 7 creates div_name and division metrics;
# (2) filter_divisions['enabled'] = True so CELL 9 applies division filtering.
# CELL 7 & CELL 9 must be True in base pipeline_config (they are by default).
# For div_name in df_cox / Cell 11: re-run from CELL 7 so 08/09 are rebuilt with div_name, then 10, 10.5, 11.
filtering_params['filter_divisions'] = {
    'enabled': True,
    'gtw_only': False,
    'prestige_only': False,
    'include_divisions': None,  # e.g. ['101ABN', '82ABN'] or None for all
}

# Enable division name + metrics so div_name exists for filtering and CR plots (CELL 7)
DIVISION_CONFIG['enabled'] = True

# Optional: keep legacy OER column in time_varying_cols for this run
if 'tb_ratio_bwd_snr_legacy' not in COLUMN_CONFIG['oer_variables']:
    COLUMN_CONFIG['oer_variables'].append('tb_ratio_bwd_snr_legacy')

# time_varying_cols = base + oer + prestige + model_time_varying_cols so Cell 10 carries all model TV cols into df_cox.
# No need to manually add div_name (or yg, etc.) here; model_time_varying_cols is the single source of truth.
_tv_base = (
    COLUMN_CONFIG.get('base_time_varying_cols', [])
    + COLUMN_CONFIG.get('oer_variables', [])
    + COLUMN_CONFIG.get('prestige_variables', [])
)
_model_tv = COLUMN_CONFIG.get('model_time_varying_cols', [])
COLUMN_CONFIG['time_varying_cols'] = list(dict.fromkeys(_tv_base + _model_tv))

PLOT_CONFIG['show_metadata_cards'] = True
