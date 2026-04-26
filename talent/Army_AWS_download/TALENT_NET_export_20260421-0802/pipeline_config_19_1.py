from pipeline_config import *

# RUN 1: Individual TB ratio vs pool minus mean (one place for scale + variables).
# Set RUN_SCALE to 'raw' or 'z' to control model, CR plots, PE plots, and interaction plots.

RUN_SCALE = 'z'

# One-swipe defaults for all CR plots (used by automated plots and by individual plots when USE_OVERRIDE_CR_PLOTS is True)
RUN_CR_PLOT_DEFAULTS = {
    'group_by': None,
    'plot_type': 'competing_risks',
    'bin_continuous': True,
    'n_bins': 26,
    'cif_bar_hspace': 0.1,
    'cif_bar_legend_show': False, # set True to show legend on CIF bar plots (read in cox_plot_helpers)
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
# combined_effect_base: Which quadratic gets the 12.6A plot (must be in quadtratic_bases); default is quadratic_bases[0].
RUN_PROFILE = {
    'tv_vars': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'quadratic_bases': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'combined_effect_base': POOL_MINUS_MEAN_SNR_COL,  #12.6A plot: pool minus mean (not TB ratio)
    'interaction_name': 'star_pool_interaction',
    'plot_prefix': 'run1',
    'var_x_label': 'TB ratio',
    'var_y_label': 'Pool minus mean',
    'cr_plot_defaults': RUN_CR_PLOT_DEFAULTS,
    # Optional: one-swipe control (expand run_profile applies these)
    'winsorize': {'enabled':False}, # turn off for e.g. [90, 100] interaction zoom
    'interaction_percentile_range':None, # zoom to high-high corner
    'interaction_log_z': False, # log scale for hazard ratio (z-axis / color)
    'interaction_log_xy': False, # log scale a and y axes (only when both axes >0, e.g. raw)
    # 1D slice: fix x at top (e.g. super top-block ratio). plot HR vs y over tip-top pool range
    # 'interaction_slice_x_at': 'max',     # 'max' or e.g. 99 for 99th percentile; None = no slice
    'interaction_slice_x_at': None,     # 'max' or e.g. 99 for 99th percentile; None = no slice
    'interaction_slice_y_range': [90,100],  # e.g. [90,100] 
}
globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))

# Ensure override wins: force winsorize off for this run (so [90,100] interaction zoom has spread)
# STANDARDIZE_CONFIG['winsorize']['enabled'] = RUN_PROFILE.get('winsorize',{}).get('enabled', True)
# print_v(f"Winsorize enabled: {STANDARDIZE_CONFIG['winsorize']['enabled']}")

# Exclude  static variables (e.g. sex) from the Cox model so they don't skew results
COLUMN_CONFIG['model_static_cols'] = []

# Use explicit CR plots below only when True; when False (default), automated plots from expand_run_profile() are used
USE_OVERRIDE_CR_PLOTS = True
# USE_OVERRIDE_CR_PLOTS = True   # example: set True to use the explicit individual CR plots below (edit per-plot as needed)

if USE_OVERRIDE_CR_PLOTS:
    # Individual CR plots (edit per-plot here if needed; common settings come from RUN_CR_PLOT_DEFAULTS)
    # Example: override bins for one plot: {**RUN_CR_PLOT_DEFAULTS, 'n_bins': 5, 'variable': TB_RATIO_SNR_COL, 'name': 'run1_cr_' + TB_RATIO_SNR_COL}
    PLOT_CONFIG['plots'] = [
        # {**RUN_CR_PLOT_DEFAULTS, 'variable': TB_RATIO_SNR_COL, 'name': 'run1_cr_' + TB_RATIO_SNR_COL},
        {**RUN_CR_PLOT_DEFAULTS, 'variable': POOL_MINUS_MEAN_SNR_COL, 'name': 'run1_cr_' + POOL_MINUS_MEAN_SNR_COL},
        # {**RUN_CR_PLOT_DEFAULTS, 'variable': 'star_pool_interaction', 'name': 'run1_cr_star_pool_interaction'},
    ]

# Filtering parameters for RUN 1
CA = ['IN','AR','EN','AV','FA','SF','AD'] # 7 branches
# CA = ['IN','AR','EN','AV','FA','AD'] # 7 branches - SF = 6 branches
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
    'include_specific': CA + CS + CSS,
    'include_only_specific': True,
    # False to allow other jobs during target rank time
    'exclude_other_jobs_during_target_rank': False,    
}
# Year group filtering
filtering_params['filter_ygs'] = {
    'enabled': True,             # Set True to enable year group filtering
    'include_specific': [2002,2003,2004,2005,2006,2007,2008,2009,2010,2011],
    'exclude_specific': None      # e.g., [2000, 2001] or None to exclude specific YGs
}
    
# --- Division: compute/utilize division:  (1) DIVISION_CONFIG['enabled'] = True so CELL 7 creates div_name
# and division metrics; (2) filetr_divisions['enabled'] = True so CELL 9 applies division filtering.
# CELL 7 & CELL 9 must be True in piepline_config (they are by default).
# Division filtering
filtering_params['filter_divisions'] = {
    'enabled': True,             # Set True to enable division filtering
    'gtw_only': False,            # Set True to include only GTW (Go To War) units
    'prestige_only': False,       # Set True to include only prestige units
    'include_divisions': None     # e.g., ['101ABN', '82ABN'] or None for all
}

# Enable division name + metrics creation so div_name exists for filtering (CELL 7)
DIVISION_CONFIG['enabled'] = True

# Optional: keep legacy OER column in time_varying_cols for this run
# This only sets time_varying_cols (candidate set for selection); it does NOT modify time_varying_cols.
if 'tb_ratio_bwd_snr_legacy' not in COLUMN_CONFIG['oer_variables']:
    COLUMN_CONFIG['oer_variables'].append('tb_ratio_bwd_snr_legacy')
_tv_cols = (
    COLUMN_CONFIG.get('base_time_varying_cols', [])
    + COLUMN_CONFIG.get('oer_variables', [])
    + COLUMN_CONFIG.get('prestige_variables', [])
)
COLUMN_CONFIG['time_varying_cols'] = list(dict.fromkeys(_tv_cols))


PLOT_CONFIG['show_metadata_cards'] = True
