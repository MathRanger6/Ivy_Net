from pipeline_config import *

# RUN 3: Individual TB ratio vs pool rank (percentile), interactive surface.
# Set RUN_SCALE to 'raw' or 'z'; Run 3 uses z by default for apples-to-apples.

RUN_SCALE = 'z'

# One-swipe defaults for all CR plots (used by automated plots and by individual plots when USE_OVERRIDE_CR_PLOTS is True)
RUN_CR_PLOT_DEFAULTS = {
    'group_by': None,
    'plot_type': 'competing_risks',
    'bin_continuous': True,
    'n_bins': 8,
    'bin_method': 'quantile',
    'min_group_size': 3,
    'use_time_varying': True,
    'filter_zero_oer': True,
    'filter_nan_variable': True,
    'filter_nan_group_by': True,
    'strict_equal_n': False,
    'x_max_days': 4500,
    'bin_group_by': True,
    'group_bins': 3,
    'group_bin_method': 'equal_width',
}

# Quadratics: set in one place here via quadratic_bases. Order of operations (in Cell 10.5): raw → square → then z-score the square if RUN_SCALE is 'z'.
RUN_PROFILE = {
    'tv_vars': [TB_RATIO_SNR_COL, POOL_TB_RATIO_RANK_PCT_SNR_COL],
    'quadratic_bases': [POOL_TB_RATIO_RANK_PCT_SNR_COL],
    'interaction_name': 'standing_pool_interaction',
    'plot_prefix': 'run3',
    'var_x_label': 'TB ratio (z)',
    'var_y_label': 'Pool TB ratio rank pct (z)',
    'cr_plot_defaults': RUN_CR_PLOT_DEFAULTS,
}
globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))

# Use explicit CR plots below only when True; when False (default), automated plots from expand_run_profile() are used
USE_OVERRIDE_CR_PLOTS = False
# USE_OVERRIDE_CR_PLOTS = True   # example: set True to use the explicit individual CR plots below (edit per-plot as needed)

if USE_OVERRIDE_CR_PLOTS:
    # Individual CR plots (z-scale; edit per-plot here if needed). Example: {**RUN_CR_PLOT_DEFAULTS, 'n_bins': 5, 'variable': Z_TB_RATIO_SNR_COL, 'name': 'run3_cr_' + Z_TB_RATIO_SNR_COL}
    PLOT_CONFIG['plots'] = [
        {**RUN_CR_PLOT_DEFAULTS, 'variable': Z_TB_RATIO_SNR_COL, 'name': 'run3_cr_' + Z_TB_RATIO_SNR_COL},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': Z_POOL_TB_RATIO_RANK_PCT_SNR_COL, 'name': 'run3_cr_' + Z_POOL_TB_RATIO_RANK_PCT_SNR_COL},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': 'standing_pool_interaction', 'name': 'run3_cr_standing_pool_interaction'},
    ]

# Filtering parameters for RUN 3
# CA = ['IN','AR','EN','AV','FA','SF','AD'] # 7 branches
CA = ['IN','AR','EN','AV','FA','AD'] # 7 branches - SF = 6 branches
CS = ['CM','CA','MI','MP','SC']
CSS = ['AG','FI','OD','QM','TC','LG']
filtering_params['filter_dates'] = {
    'enabled': False,
    'start_date': '2000-01-01',
    'end_date': '2022-06-30',
}
filtering_params['filter_job_codes'] = {
    'enabled': True,
    'exclude_problematic': True,
    'problematic_codes': ['MC', 'DC', 'VC', 'SP', 'AN', 'JA', 'CH', 'MS'],
    'include_specific': CS + CSS,
    'include_only_specific': True,
}

PLOT_CONFIG['show_metadata_cards'] = True
