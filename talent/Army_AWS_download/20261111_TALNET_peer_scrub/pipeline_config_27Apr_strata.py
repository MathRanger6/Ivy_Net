# Pipeline Configuration File for 520_pipeline_cox_working.ipynb
"""

This file contains all configuration settings for the Cox regression pipeline.
Import this file in the notebook to access all settings:

    from pipeline_config import *

Or import specific items:

    from pipeline_config import CELL0, CELL1, PLOT_CONFIG, COLUMN_CONFIG

This allows you to:
- Keep the notebook focused on execution logic
- Edit settings in a separate window
- Version control settings separately
- Maintain multiple configuration files for different runs
"""

# ============================================================================
# === 0. PRE-RUN FLAGS ===
# ============================================================================
# Optional pre-run steps before any notebook cells execute

RUN_503 = False  # Set True to (re)build prestige UIC lists via py_503_hierarchies.py
# pip_config_file = "pipeline_config_17_1.py"

# ============================================================================
# === 1. CELL EXECUTION FLAGS ===
# ============================================================================
# Boolean flags to control which cells execute
# Set to False to skip cells (e.g., if intermediate files already exist)

# PHASE 1: Data Loading & Basic Preparation
CELL0 = False   # Load lookup table dictionary (lu_table_dict)
CELL1 = False   # Load raw snapshot data
CELL2 = False   # Basic filtering (commissioned officers, remove irregular MOS)
CELL3 = False   # Calculate year group (yg) with multiple appointment handling

# PHASE 2: OER Integration
CELL4 = False   # Merge OER to snapshots + compute individual fwd/bwd metrics
CELL5_POOL_MEANS = False  # Pool means/minus-means/size (fwd+bwd)
CELL6_POOL_RANKS = False  # Pool ranks/percentiles/z-scores (fwd+bwd)

# PHASE 3: Variable Creation
CELL7 = True   # Create time-varying variables
CELL8 = True   # Create static variables

# PHASE 4: Advanced Filtering
CELL9 = True    # Advanced filtering (divisions, YG, etc.)

# PHASE 5: Cox Analysis
CELL10 = True   # Cox data preparation
CELL10_5 = True   # Cox standardize + interactions
CELL10_5S = False   # Cox standardize + splines + interactions (future; guarded execution)
CELL11 = True   # Cox analysis and plotting
CELL12 = True   # Cox regression models (static, full, competing risks)

# CELL 12 SUB-SECTION FLAGS (for modular troubleshooting)
# These allow running specific sections of CELL 12 independently
CELL12_1 = True  # 12.1: Prepare data for Cox regression
CELL12_2 = True  # 12.2: Fit static model (demographics only)
CELL12_3 = True  # 12.3: Fit full model (static + time-varying)
CELL12_4 = True  # 12.4: Model comparison and signal ratios
CELL12_5 = True  # 12.5: Competing risks analysis
CELL12_6 = True  # 12.6: Partial effects plots
CELL12_7 = True  # 12.7: Interaction effects (3D plots)
CELL12_8 = True  # 12.8: Model-based promotion curves for fixed X/Y values


# ============================================================================
# === 2. GLOBAL SETTINGS ===
# ============================================================================
# Standardize prefix for z-scores
Z_PREFIX = 'z_'

# Directory paths
var_dir = './running_vars/'          # Directory for saved variables/configs
uic_dir = './big_dfs/2_UIC_hier_data'  # Directory for UIC hierarchy data
cox_var_dir = "./cox/cox_vars"       # Directory for Cox analysis variables

# Output settings
verbose = True                       # Enable verbose output (print_v function)
null_reports = False                  # Boolean to run df_null_reports (data quality checks)


# ============================================================================
# === 3. ANALYSIS CONFIGURATION ===
# ============================================================================

# Rank configuration for promotion analysis
SOURCE_RANK = 'CPT'   # The rank we're analyzing FROM (source rank)
TARGET_RANK = 'MAJ'   # The rank we're analyzing promotion TO (target rank)
# Note: final_job_code will be set to the last SOURCE_RANK snapshot job_code
# (i.e., the job_code when promoted to TARGET_RANK)

# Set True to compute job_code_changed in Cell 8 (expensive groupby); False skips it and sets job_code_changed=0.
CREATE_JOB_CODE_CHANGED = False


# ============================================================================
# === 4. POOL METRICS SETTINGS (CELL 6) ===
# ============================================================================
# Pool metrics are computed in two steps with checkpoints (means/sizes, then ranks/z).

POOL_MIN_SIZE = 3
POOL_EXCLUDE_SELF = True
POOL_RANK_METHOD = 'average'
POOL_RANK_ASCENDING = True
POOL_Z_EPS = 1e-9

# CELL 6 LOGGING CONFIGURATION
CELL6_ENABLE_LOGGING = True          # Set False to disable file logging
CELL6_LOG_DIR = './cell6_logs'       # Directory for log files (created automatically)


# ============================================================================
# === 4.1. COLUMN NAME MAPPINGS ===
# ============================================================================

# Column name mappings (used in all cells)
# These map the function's expected column names to your actual column names
CELL6_COLUMN_MAPPING = {
    'pid_col': 'pid_pde',                    # Officer ID column
    'snapshot_date_col': 'snpsht_dt',        # Snapshot date column
    'rated_officer_col': 'rated_ofcr',       # Rated officer ID in OER data
    'thru_date_col': 'eval_thru_dt',         # OER completion date (end of rating period)
    'rater_box_col': 'rater_box',            # Rater box score (numeric, 50 = top block)
    'snr_rater_box_col': 'snr_rater_box',    # Senior rater box score (numeric, 50 = top block)
    'eval_id_col': 'eval_id',                # Unique OER identifier
    'start_date_col': 'eval_strt_dt',        # OER start date
    'rater_col': 'rater',                    # Rater pid_pde in OER data
    'snr_rater_col': 'snr_rater',            # Senior rater pid_pde in OER data
}

# ============================================================================
# === 4.1A. OER ASSIGNMENT MODES (TB METRICS + POOL ASSIGNMENT) ===
# ============================================================================
# Experimental: new forward/backward assignment (replaces CELL 5 + much of CELL 6A)
# Set True to use assign_oer_to_snapshots_fast in add_cum_oer_metrics_mod_working.py
USE_NEW_OER_ASSIGNMENT = True
NEW_OER_TB_VALUE = 50
NEW_OER_USE_TQDM = True
NEW_OER_COMPUTE_POOL_METRICS = False
CLEAN_OER_COLS = True
CLEAN_SNAP_COLS = True
oer_cols_keep = ['rated_ofcr', 'eval_strt_dt', 'eval_thru_dt', 'fy', 'rated_days','rated_rank', 'oer_uic_pde', 'rater', 'rater_box', 'snr_rater',
                 'snr_rater_box', 'rater_box_cd', 'sr_rater_global_box_cd', 'sr_rater_global_box_chk_txt', 'rated_dor', 'basic_brnch_cd',
                 'basic_branch_cd_enu', 'eval_id', 'rater_asg_uic_pde', 'snr_rater_asg_uic_pde']
snap_cols_clean = ['ofcr_act_stat_pe_dt','edu_tier_cd', 'edu_lvl_cd', 'grad_pro_edu_stat_cd','dty_svc_occ_cd', 'pri_dod_occ_cd', 'pri_svc_occ_cd', 'dty_dod_occ_cd',]
from functionsG import load_json, store_json
store_json(oer_cols_keep, 'oer_cols_keep', var_dir)
store_json(snap_cols_clean, 'snap_cols_clean', var_dir)

# TB assignment modes:
# - 'forward': use most recent OER thru_date (paint forward)
# - 'backward': apply OER across its rating window (start_date forward)
#   This paints TB outcomes backward to snapshots within the rating period.
# You can control TB assignment separately for:
#   - the focal officer (self metrics used in modeling)
#   - the pool peers (used to compute pool means/ranks)
# Pool membership always uses overlap-based logic (start <= snapshot <= thru).
TB_ASSIGNMENT_MODE = 'forward'
TB_ASSIGNMENT_MODE_SELF = TB_ASSIGNMENT_MODE
TB_ASSIGNMENT_MODE_POOL = TB_ASSIGNMENT_MODE
# Column helpers for new forward/backward naming
TB_MODE_MAP = {
    'forward': 'fwd',
    'backward': 'bwd',
    'fwd': 'fwd',
    'bwd': 'bwd',
}

TB_MODE_SELF = TB_MODE_MAP.get(TB_ASSIGNMENT_MODE_SELF, TB_ASSIGNMENT_MODE_SELF)
TB_MODE_POOL = TB_MODE_MAP.get(TB_ASSIGNMENT_MODE_POOL, TB_ASSIGNMENT_MODE_POOL)
TB_RATIO_FWD_RTR_COL = "tb_ratio_fwd_rtr"
TB_RATIO_FWD_SNR_COL = "tb_ratio_fwd_snr"
TB_RATIO_BWD_RTR_COL = "tb_ratio_bwd_rtr"
TB_RATIO_BWD_SNR_COL = "tb_ratio_bwd_snr"
TB_CUM_FWD_RTR_COL = "cum_tb_fwd_rtr"
TB_CUM_FWD_SNR_COL = "cum_tb_fwd_snr"
TB_CUM_BWD_RTR_COL = "cum_tb_bwd_rtr"
TB_CUM_BWD_SNR_COL = "cum_tb_bwd_snr"
EVALS_CUM_FWD_RTR_COL = "cum_evals_fwd_rtr"
EVALS_CUM_FWD_SNR_COL = "cum_evals_fwd_snr"
EVALS_CUM_BWD_RTR_COL = "cum_evals_bwd_rtr"
EVALS_CUM_BWD_SNR_COL = "cum_evals_bwd_snr"
TB_RATIO_RTR_COL = f"tb_ratio_{TB_MODE_SELF}_rtr"
TB_RATIO_SNR_COL = f"tb_ratio_{TB_MODE_SELF}_snr"
CUM_TB_RTR_COL = f"cum_tb_{TB_MODE_SELF}_rtr"
CUM_TB_SNR_COL = f"cum_tb_{TB_MODE_SELF}_snr"
CUM_EVALS_RTR_COL = f"cum_evals_{TB_MODE_SELF}_rtr"
CUM_EVALS_SNR_COL = f"cum_evals_{TB_MODE_SELF}_snr"
Z_TB_RATIO_RTR_COL = f"{Z_PREFIX}{TB_RATIO_RTR_COL}"
Z_TB_RATIO_SNR_COL = f"{Z_PREFIX}{TB_RATIO_SNR_COL}"
POOL_TB_RATIO_MEAN_RTR_COL = f"pool_tb_ratio_mean_rtr_{TB_MODE_POOL}"
POOL_TB_RATIO_MEAN_SNR_COL = f"pool_tb_ratio_mean_snr_{TB_MODE_POOL}"
POOL_MINUS_MEAN_RTR_COL = f"pool_minus_mean_rtr_{TB_MODE_POOL}"
POOL_MINUS_MEAN_SNR_COL = f"pool_minus_mean_snr_{TB_MODE_POOL}"
POOL_SIZE_RTR_COL = f"pool_size_rtr_{TB_MODE_POOL}"
POOL_SIZE_SNR_COL = f"pool_size_snr_{TB_MODE_POOL}"
POOL_TB_RATIO_MEAN_FWD_RTR_COL = "pool_tb_ratio_mean_rtr_fwd"
POOL_TB_RATIO_MEAN_FWD_SNR_COL = "pool_tb_ratio_mean_snr_fwd"
POOL_TB_RATIO_MEAN_BWD_RTR_COL = "pool_tb_ratio_mean_rtr_bwd"
POOL_TB_RATIO_MEAN_BWD_SNR_COL = "pool_tb_ratio_mean_snr_bwd"
POOL_MINUS_MEAN_FWD_RTR_COL = "pool_minus_mean_rtr_fwd"
POOL_MINUS_MEAN_FWD_SNR_COL = "pool_minus_mean_snr_fwd"
POOL_MINUS_MEAN_BWD_RTR_COL = "pool_minus_mean_rtr_bwd"
POOL_MINUS_MEAN_BWD_SNR_COL = "pool_minus_mean_snr_bwd"
POOL_SIZE_FWD_RTR_COL = "pool_size_rtr_fwd"
POOL_SIZE_FWD_SNR_COL = "pool_size_snr_fwd"
POOL_SIZE_BWD_RTR_COL = "pool_size_rtr_bwd"
POOL_SIZE_BWD_SNR_COL = "pool_size_snr_bwd"
POOL_TB_RATIO_RANK_FWD_RTR_COL = "pool_tb_ratio_rank_rtr_fwd"
POOL_TB_RATIO_RANK_FWD_SNR_COL = "pool_tb_ratio_rank_snr_fwd"
POOL_TB_RATIO_RANK_BWD_RTR_COL = "pool_tb_ratio_rank_rtr_bwd"
POOL_TB_RATIO_RANK_BWD_SNR_COL = "pool_tb_ratio_rank_snr_bwd"
POOL_TB_RATIO_RANK_PCT_FWD_RTR_COL = "pool_tb_ratio_rank_pct_rtr_fwd"
POOL_TB_RATIO_RANK_PCT_FWD_SNR_COL = "pool_tb_ratio_rank_pct_snr_fwd"
POOL_TB_RATIO_RANK_PCT_BWD_RTR_COL = "pool_tb_ratio_rank_pct_rtr_bwd"
POOL_TB_RATIO_RANK_PCT_BWD_SNR_COL = "pool_tb_ratio_rank_pct_snr_bwd"
POOL_TB_RATIO_ZPOOL_FWD_RTR_COL = "pool_tb_ratio_zpool_rtr_fwd"
POOL_TB_RATIO_ZPOOL_FWD_SNR_COL = "pool_tb_ratio_zpool_snr_fwd"
POOL_TB_RATIO_ZPOOL_BWD_RTR_COL = "pool_tb_ratio_zpool_rtr_bwd"
POOL_TB_RATIO_ZPOOL_BWD_SNR_COL = "pool_tb_ratio_zpool_snr_bwd"
POOL_TB_RATIO_RANK_RTR_COL = f"pool_tb_ratio_rank_rtr_{TB_MODE_POOL}"
POOL_TB_RATIO_RANK_SNR_COL = f"pool_tb_ratio_rank_snr_{TB_MODE_POOL}"
POOL_TB_RATIO_RANK_PCT_RTR_COL = f"pool_tb_ratio_rank_pct_rtr_{TB_MODE_POOL}"
POOL_TB_RATIO_RANK_PCT_SNR_COL = f"pool_tb_ratio_rank_pct_snr_{TB_MODE_POOL}"
POOL_TB_RATIO_ZPOOL_RTR_COL = f"pool_tb_ratio_zpool_rtr_{TB_MODE_POOL}"
POOL_TB_RATIO_ZPOOL_SNR_COL = f"pool_tb_ratio_zpool_snr_{TB_MODE_POOL}"
Z_POOL_MINUS_MEAN_RTR_COL = f"{Z_PREFIX}{POOL_MINUS_MEAN_RTR_COL}"
Z_POOL_MINUS_MEAN_SNR_COL = f"{Z_PREFIX}{POOL_MINUS_MEAN_SNR_COL}"
Z_POOL_TB_RATIO_RANK_PCT_RTR_COL = f"{Z_PREFIX}{POOL_TB_RATIO_RANK_PCT_RTR_COL}"
Z_POOL_TB_RATIO_RANK_PCT_SNR_COL = f"{Z_PREFIX}{POOL_TB_RATIO_RANK_PCT_SNR_COL}"

# Default pool context signal (use minus-mean by default)
POOL_CONTEXT_RTR_COL = POOL_MINUS_MEAN_RTR_COL
POOL_CONTEXT_SNR_COL = POOL_MINUS_MEAN_SNR_COL
Z_POOL_CONTEXT_RTR_COL = f"{Z_PREFIX}{POOL_CONTEXT_RTR_COL}"
Z_POOL_CONTEXT_SNR_COL = f"{Z_PREFIX}{POOL_CONTEXT_SNR_COL}"

# NaT handling for OER start/thru dates:
# - 'drop_low_impute_high': drop NaTs if rare; impute if frequent
# - 'drop': always drop rows with missing dates
# - 'impute': always impute using neighbor dates within officer
OER_NAT_POLICY = 'drop_low_impute_high'
OER_NAT_DROP_THRESHOLD = 0.01  # 1% threshold


# ============================================================================
# === 5. FILTERING PARAMETERS (CELL 9) ===
# ============================================================================
# Advanced filtering configuration for CELL 9

# Job code categories
# CA = ['IN','AR','EN','AV','FA','SF','AD'] # 7 branches
CA = ['IN','AR','EN','AV','FA','AD'] # 7 branches - SF = 6 branches
CS = ['CM','CA','MI','MP','SC'] # 5 branches
CSS = ['AG','FI','OD','QM','TC','LG'] # 6 branches

filtering_params = {
    # Date filtering
    'filter_dates': {
        'enabled': False,             # Set True to enable date filtering
        'start_date': '2000-01-01',   # Start date for snapshots (YYYY-MM-DD)
        'end_date': '2022-06-30',     # End date for snapshots (YYYY-MM-DD)
    },
    
    # Job code filtering
    'filter_job_codes': {
        'enabled': True,             # Set True to enable job code filtering
        'exclude_problematic': True, # Set True to exclude problematic job codes
        'problematic_codes': ['MC', 'DC', 'VC', 'SP', 'AN', 'JA', 'CH', 'MS'],  # List of problematic codes to exclude
        'include_specific': CA+CS+CSS,     # e.g., ['IN', 'AR', 'FA'] or None for all
        # 'include_specific':  ['AV'],
        'include_only_specific': True, # Legacy: see exclude_other_jobs_during_target_rank
        # If True, exclude officers who were other than include_specific during their source_rank time. set False to allow other jobs during target rank time
        'exclude_other_jobs_during_target_rank': True,
    },
    
    # Gender filtering
    'filter_gender': {
        'enabled': True,             # Set True to enable gender filtering
        'exclude_dual_gender': True,  # Set True to exclude officers with dual gender records
        'include_gender': None        # Options: 'male' or 'female' or None (for both). Filters to specific gender after excluding dual-gender
    },
    
    # Year group filtering
    'filter_ygs': {
        'enabled': True,             # Set True to enable year group filtering
        'include_specific': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011],  # e.g., [2006, 2007, 2008] or None
        'exclude_specific': None,     # e.g., [2000, 2001] or None to exclude specific YGs
    },
    
    # Division filtering
    'filter_divisions': {
        'enabled': False,             # Set True to enable division filtering
        'gtw_only': False,            # Set True to include only GTW (Ground Truth War) units
        'prestige_only': False,       # Set True to include only prestige units
        'include_divisions': None,    # e.g., ['101ABN', '82ABN'] or None for all
    },
}


# ============================================================================
# === 5B. PRESTIGE UNIT CONFIGURATION (CELL 7) ===
# ============================================================================
# Defines which top-level UIC roots are considered "prestige" for prestige_unit.
# These roots are expanded by FY using df_uic_div_lookup (from 503_hierarchies).
PRESTIGE_CONFIG = {
    # Master switch for CELL 7 prestige processing (unit + optional cumulative metrics)
    'enable_prestige_processing': True,
    # Top-level UIC roots to include as prestige (by-FY expansion)
    # Example: USASOC root () includes SFG, RGR, SOAR, etc.
    'prestige_uic_roots': ['WD45FF'],
    # Whether to include the root UIC itself (e.g., ) in the prestige list
    'include_top_uics': True,
    # Name used when saving/loading the by-FY prestige list JSON
    'prestige_list_name': 'prestige_uics_by_fy',
    # Backfill early FYs (e.g. 2001-2014) when UIC tables start in 2015
    'backfill_early_fy': True,
    # When backfilling, use the union of all available FY UICs (not just earliest FY)
    'backfill_use_union': True,
    # Start FY for backfill (inclusive)
    'backfill_start_fy': 2001,
    # Two-digit FY expansion (yy > pivot → 19yy, else 20yy). Full years >= 100 pass through (e.g. 1995, 2015).
    'fy_two_digit_pivot': 68,
    # Optional cumulative prestige metrics in CELL 7
    'create_prestige_sum': True,
    'create_prestige_mean': False,
}

# ============================================================================
# === 5C. DIVISION NAME CONFIGURATION (CELL 7)
# ============================================================================
# Controls optional merge for div_name and division service metrics
DIVISION_CONFIG = {
    # Core merge settings
    'enabled': False,                # Set True to create div_name if missing
    'uic_hierarchy_file': 'df_uic_hierarchy',
    'uic_col': 'asg_uic_pde',
    'div_col': 'div_name',
    'fy_col': 'fy',
    'use_fy_lookup': True,           # Use df_uic_div_lookup (FY-aware) when available
    'uic_div_lookup_file': 'df_uic_div_lookup_pde',
    'backfill_early_fy': True,       # Backfill early FYs using backfill_fy
    'backfill_fy': 2015,             # Use FY 2015 mapping for early years
    # Two-digit FY expansion (yy > pivot → 19yy, else 20yy). Values >= 100 unchanged (e.g. 1995–2026).
    'fy_two_digit_pivot': 68,
    'pid_col': 'pid_pde',
    'date_col': 'snpsht_dt',
    'rank_col': 'rank_pde',
    'source_rank': SOURCE_RANK,      # Used for final_div_cpt (last SOURCE_RANK snapshot)

    # Division service metrics
    'create_div_cum_time': True,     # Cumulative snapshots with any div_name
    'create_div_ratio_time': True,   # Cumulative ratio of time with any div_name
    'create_final_div_cpt': True,    # Division at last SOURCE_RANK snapshot

    # Optional per-division metrics (keep list short to avoid wide tables)
    'division_name_map': {},         # e.g., {'82nd Airborne Division': '82ABN'}
    'division_list': [],             # e.g., ['82ABN', '1AD', '75RR']
    'division_prefix': 'div',        # Prefix for per-division metric columns
}


# ============================================================================
# === 6. COLUMN CONFIGURATION (CELL 11) ===
# ============================================================================
# Defines which columns to include in analysis and how to handle them

COLUMN_CONFIG = {
    # Basic demographic columns (always included)
    'basic_demographic_cols': [
        'pid_pde',      # Officer ID
        'start_time',   # Start time for survival interval
        'stop_time',    # Stop time for survival interval
        'event',        # Event indicator (0=censored, 1=promoted, 2=attrited)
        # 'sex',          # Gender
        # 'yg',           # Year group
    ],
    
    # Static columns (one value per officer, doesn't change over time)
    # These variables have the same value for all snapshots/intervals for each officer
    # Useful for demographic and baseline characteristics that don't vary during the study period
    'static_cols': [
        # 'age_cpt',          # Age at Captain promotion (calculated once, remains constant)
        # 'final_job_code',   # Last job code before promotion/censoring/attrition (captured at end of observation)
    ],
    
    # Model-only static columns (optional; defaults to static_cols if empty)
    # Use this when you want a narrower model but keep a broader plotting candidate set
    # 'model_static_cols': ['sex'],
    
    # Base time-varying columns (non-OER, non-prestige)
    # These variables can have different values at different snapshots for the same officer
    # For survival analysis, each snapshot becomes a separate interval with its own covariate values
    'base_time_varying_cols': [
        # 'married',   # Marital status (can change over time)
        'snpsht_dt', # Snapshot date (needed for time-alignment diagnostics)
        # 'job_code',  # Current job code (changes as officer is assigned to different positions)
        # 'div_name', # Division name (time-varying, uncomment if available)
    ],

    # Model-only time-varying columns (optional; defaults to time_varying_cols if empty)
    # Use this when you want a narrower model but keep a broader plotting candidate set
    'model_time_varying_cols': [
        TB_RATIO_SNR_COL,
        POOL_CONTEXT_SNR_COL,
        'star_pool_interaction',
    ],
    
    # Optional: extra columns merged onto survival interval rows (Cell 10) without adding to the Cox formula.
    # Normally leave empty and put all model TV covariates (including categoricals) in model_time_varying_cols.
    'extra_survival_tv_cols': [],
    
    # OER-related variables (Officer Evaluation Report performance metrics)
    # These variables are used by plotting functions to identify OER variables for filtering purposes
    # When 'filter_zero_oer' is enabled in plot config, officers with NO OER data (all NaN) are excluded
    # Officers with OER data but 0 top blocks are KEPT (they have valid data, just low performance)
    # 
    # OER variables are typically time-varying (cumulative metrics that grow over time)
    # They track performance ratings received from raters (rtr) and senior raters (snr)
    'oer_variables': [
        # Cumulative counts (forward + backward)
        TB_CUM_FWD_RTR_COL,
        TB_CUM_FWD_SNR_COL,
        TB_CUM_BWD_RTR_COL,
        TB_CUM_BWD_SNR_COL,
        EVALS_CUM_FWD_RTR_COL,
        EVALS_CUM_FWD_SNR_COL,
        EVALS_CUM_BWD_RTR_COL,
        EVALS_CUM_BWD_SNR_COL,

        # Ratios (forward + backward)
        TB_RATIO_FWD_RTR_COL,
        TB_RATIO_FWD_SNR_COL,
        TB_RATIO_BWD_RTR_COL,
        TB_RATIO_BWD_SNR_COL,

        # Pool means / minus-means / sizes (forward + backward)
        POOL_TB_RATIO_MEAN_FWD_RTR_COL,
        POOL_TB_RATIO_MEAN_FWD_SNR_COL,
        POOL_TB_RATIO_MEAN_BWD_RTR_COL,
        POOL_TB_RATIO_MEAN_BWD_SNR_COL,
        POOL_MINUS_MEAN_FWD_RTR_COL,
        POOL_MINUS_MEAN_FWD_SNR_COL,
        POOL_MINUS_MEAN_BWD_RTR_COL,
        POOL_MINUS_MEAN_BWD_SNR_COL,
        POOL_SIZE_FWD_RTR_COL,
        POOL_SIZE_FWD_SNR_COL,
        POOL_SIZE_BWD_RTR_COL,
        POOL_SIZE_BWD_SNR_COL,

        # Pool ranks / percentiles / z-scores (forward + backward)
        POOL_TB_RATIO_RANK_FWD_RTR_COL,
        POOL_TB_RATIO_RANK_FWD_SNR_COL,
        POOL_TB_RATIO_RANK_BWD_RTR_COL,
        POOL_TB_RATIO_RANK_BWD_SNR_COL,
        POOL_TB_RATIO_RANK_PCT_FWD_RTR_COL,
        POOL_TB_RATIO_RANK_PCT_FWD_SNR_COL,
        POOL_TB_RATIO_RANK_PCT_BWD_RTR_COL,
        POOL_TB_RATIO_RANK_PCT_BWD_SNR_COL,
        POOL_TB_RATIO_ZPOOL_FWD_RTR_COL,
        POOL_TB_RATIO_ZPOOL_FWD_SNR_COL,
        POOL_TB_RATIO_ZPOOL_BWD_RTR_COL,
        POOL_TB_RATIO_ZPOOL_BWD_SNR_COL,

        # Mode-selected convenience aliases
        CUM_TB_RTR_COL,
        CUM_TB_SNR_COL,
        CUM_EVALS_RTR_COL,
        CUM_EVALS_SNR_COL,
        TB_RATIO_RTR_COL,
        TB_RATIO_SNR_COL,
        POOL_TB_RATIO_MEAN_RTR_COL,
        POOL_TB_RATIO_MEAN_SNR_COL,
        POOL_MINUS_MEAN_RTR_COL,
        POOL_MINUS_MEAN_SNR_COL,
        POOL_TB_RATIO_RANK_RTR_COL,
        POOL_TB_RATIO_RANK_SNR_COL,
        POOL_TB_RATIO_RANK_PCT_RTR_COL,
        POOL_TB_RATIO_RANK_PCT_SNR_COL,
        POOL_TB_RATIO_ZPOOL_RTR_COL,
        POOL_TB_RATIO_ZPOOL_SNR_COL,
        POOL_SIZE_RTR_COL,
        POOL_SIZE_SNR_COL,
    ],
    
    # Prestige-related variables (non-OER metrics derived from prestige_unit)
    # These can be added to time_varying_cols as a block for convenience
    'prestige_variables': [
        # Cumulative counts/means
        'prestige_sum',   # Cumulative prestige quarters (sum of quarters in prestige units)
        'prestige_mean',  # Mean prestige quarters (average prestige across snapshots)
        'prestige_unit',  # Current prestige unit indicator (0/1, changes as officer moves units)
        # Pool prestige normalized ranks (requires CELL 6C pool metrics)
        'prestige_ratio_rank_norm_rtr',  # Normalized rank (0-1, 1 = best) in rater pool
        'prestige_ratio_rank_norm_snr',  # Normalized rank (0-1, 1 = best) in senior rater pool
    ],
    
    # Time-varying columns (combined list used by CELL 11)
    'time_varying_cols': [],
    
    # Dummy variable configuration
    'dummy_variables': {
        'create_dummies': True,      # Set True to create dummy variables for categorical columns
        'exclude_reference': False,   # If True, drop first category (reference); if False, keep all
        'categorical_cols': {
            # Static: add via model_static_cols / EXTRA_STATIC_COLS in override, not time_varying.
            # 'yg': {                  # Year group dummy variables
            #     'prefix': 'yg',      # Prefix for dummy column names (e.g., 'yg_2006')
            #     'reference': None,   # Reference category (None = uses most common category, or specify category)
            # },
            # 'final_job_code': {      # Final job code dummy variables
            #     'prefix': 'final_job',  # Prefix for dummy column names (e.g., 'final_job_IN')
            #     'reference': None,   # Reference category (None = uses most common category, or specify category)
            # },
            # 'job_code': {    # Job code dummy variables
            #     'prefix': 'job',  # Prefix for dummy column names (e.g., 'job_IN')
            #     'reference': None,   # Reference category (None = uses most common category, or specify category)
            # },
            # Time-varying: add via EXTRA_TIME_VARYING_COLS in override so div_name is in df_cox.
            'div_name': {              # Division name dummy variables (time-varying)
                'prefix': 'div',       
                'reference': None,     # Reference category (None = uses most common category, or specify category)
            },
            # 'sex': {
            #     'prefix': 'sex',
            #     'reference': 'M',  # Use 'M' as reference category
            # },
        },
    },
}

# ============================================================================
# === 6.1. OPTIONAL STANDARDIZATION (Z-SCORE) ===
# ============================================================================
# Create standardized (z-score) versions of selected variables for model fitting.
# These are created in CELL 10 on the Cox-ready dataset and can optionally be used
# as the model inputs in CELL 12.
STANDARDIZE_CONFIG = {
    'enabled': True,         # Set True to create z_columns in CELL 10
    'cols': [TB_RATIO_SNR_COL,
             POOL_MINUS_MEAN_SNR_COL,
             POOL_TB_RATIO_RANK_PCT_SNR_COL,
            ],              # Explicit list of columns to standardize (empty = use model cols)
    'exclude_cols': [        # Columns to never standardize
        'pid_pde', 'start_time', 'stop_time', 'event'
    ],
    'prefix': Z_PREFIX,       # Prefix for standardized columns
    'use_for_model': False,  # If True, model_*_cols will use z_versions when available
    'winsorize': {           # Optional outlier clipping before z-score
        'enabled': True,
        'lower_q': 0.01,
        'upper_q': 0.999,
    
    },
}

# ============================================================================
# === 6.1A. QUADRATIC TERMS (CELL 10.5) ===
# ============================================================================
# Which variables get quadratic coefficients: set here via 'bases' or 'terms', or in run
# overrides via RUN_PROFILE['quadratic_bases'] (expand_run_profile() fills QUADRATIC_CONFIG).
#
# Order of operations (statistically correct):
#   (1) Square the RAW variable (so curvature is in the original scale).
#   (2) Optionally z-score the squared term (zscore: True) for scale comparability in the model.
# Do not z-score the raw variable then square—that would give curvature in z-space, not in
# the original variable. Cell 10.5 builds base_sq from the raw column, then if zscore=True
# creates z_base_sq from that squared series.
QUADRATIC_CONFIG = {
    'enabled': True,
    # Option A (simple): list base columns here, squared terms are auto-created
    # Example: 'bases': [POOL_MINUS_MEAN_SNR_COL, TB_RATIO_SNR_COL]
    'bases': [],
    # Default z-score behavior for auto-created squares (can be overridden per term)
    'default_zscore': False,
    'terms': [
        # Example:
        # {
        #     'name': f"{POOL_MINUS_MEAN_SNR_COL}_sq",
        #     'base': POOL_MINUS_MEAN_SNR_COL,
        #     'zscore': False,
        # },
    ],
    # Optional winsorization for quadratic terms (defaults to STANDARDIZE_CONFIG winsorize)
    'winsorize': {},
}

# ============================================================================
# === 6.1B. SPLINE TERMS (CELL 10.5S - FUTURE) ===
# ============================================================================
# Placeholder spline configuration (disabled by default).
# When enabled, Cell 10.5S can build spline basis columns from raw inputs.
SPLINE_CONFIG = {
    'enabled': False,
    'terms': [
        # Example:
        # {
        #     'base': TB_RATIO_SNR_COL,
        #     'df': 4,
        #     'knot_method': 'quantile',  # 'quantile' or 'uniform'
        #     'prefix': 'spline_',
        #     'use_z': False,
        # },
    ],
    # Optional winsorization for spline inputs (defaults to STANDARDIZE_CONFIG winsorize)
    'winsorize': {},
}

# ============================================================================
# === 6.1C. RUN SCALE & PROFILE (OPTIONAL – SIMPLIFIES OVERRIDES) ===
# ============================================================================
# Set RUN_SCALE and RUN_PROFILE in an override, then call expand_run_profile().
# One place controls raw vs z for model, CR plots, PE plots, and interaction plots.
#
# RUN_SCALE: 'raw' | 'z'
# RUN_PROFILE: dict with
#   - tv_vars: list of raw column names (e.g. [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL])
#   - quadratic_bases: list of raw columns that get a squared term — this is the one place
#     that sets which variables get quadratic coefficients when using the run profile
#     (e.g. [POOL_MINUS_MEAN_SNR_COL] or [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL])
#   - combined_effect_base: optional raw column name for Cell 12.6A combined-effect plot; must be
#     in quadratic_bases. If omitted, quadratic_bases[0] is used.
#   - interaction_name: str (e.g. 'star_pool_interaction')
#   - plot_prefix: optional str for CR plot names (e.g. 'run1')
#   - var_x_label, var_y_label: optional str for interaction plot axes
#   - cr_plot_defaults: optional dict of CR plot options (n_bins, bin_method, etc.) applied to all automated CR plots
#   - winsorize: optional dict to override STANDARDIZE_CONFIG['winsorize'] (e.g. {'enabled': False} to turn off)
#   - interaction_percentile_range: optional [low, high] for interaction plot axis range (e.g. [90, 100] to zoom)
#   - interaction_log_z: optional bool — use log scale for hazard ratio (z-axis / color)
#   - interaction_log_xy: optional bool — use log scale for x and y axes (only when both axes > 0, e.g. raw)
#   - interaction_slice_x_at: optional 'max' or percentile (e.g. 99) — 1D slice: fix x at top, plot HR vs y
#   - interaction_slice_y_range: optional [low, high] for that slice (e.g. [90, 100])
#
# In override: set RUN_SCALE, RUN_PROFILE, then globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))
# expand_run_profile() also returns USE_Z_FOR_RUN (True when RUN_SCALE=='z') for notebook/PE plots if needed.
RUN_SCALE = None   # Override sets to 'raw' or 'z'
RUN_PROFILE = None # Override sets dict; when set, expand_run_profile() fills the rest
USE_Z_FOR_RUN = False  # Set by expand_run_profile(); use in notebook for plot scale if desired
USE_OVERRIDE_CR_PLOTS = False  # Override: True = use explicit PLOT_CONFIG['plots'] from override; False = use automated plots

def expand_run_profile(run_scale, run_profile):
    """
    Fill STANDARDIZE_CONFIG, model_time_varying_cols, QUADRATIC_CONFIG['terms'],
    INTERACTION_CONFIG, and PLOT_CONFIG['plots'] from RUN_SCALE and RUN_PROFILE.
    Call from override: globals().update(expand_run_profile(RUN_SCALE, RUN_PROFILE))
    """
    import pipeline_config as _cfg
    prefix = _cfg.Z_PREFIX
    tv_vars = run_profile.get('tv_vars', [])
    quadratic_bases = run_profile.get('quadratic_bases', [])
    interaction_name = run_profile.get('interaction_name', '')
    plot_prefix = run_profile.get('plot_prefix', 'run')
    var_x_label = run_profile.get('var_x_label')
    var_y_label = run_profile.get('var_y_label')
    use_z = (run_scale == 'z')

    # Columns for model and plots (raw or z)
    linear_cols = [f"{prefix}{c}" for c in tv_vars] if use_z else list(tv_vars)
    sq_cols = [f"{prefix}{b}_sq" for b in quadratic_bases] if use_z else [f"{b}_sq" for b in quadratic_bases]
    left_col = linear_cols[0] if len(linear_cols) >= 1 else tv_vars[0]
    right_col = linear_cols[1] if len(linear_cols) >= 2 else (tv_vars[1] if len(tv_vars) >= 2 else None)

    _cfg.STANDARDIZE_CONFIG['cols'] = list(tv_vars) if use_z else []
    # When RUN_SCALE is 'z', Cell 12 must load df_pipeline_10_5_cox_zscored so z_ columns exist
    if use_z:
        _cfg.STANDARDIZE_CONFIG['use_for_model'] = True
    _cfg.COLUMN_CONFIG['model_time_varying_cols'] = linear_cols + sq_cols + [interaction_name]
    _cfg.QUADRATIC_CONFIG['enabled'] = True
    _cfg.QUADRATIC_CONFIG['bases'] = []
    _cfg.QUADRATIC_CONFIG['terms'] = [
        {'name': f"{b}_sq", 'base': b, 'zscore': use_z} for b in quadratic_bases
    ]
    _cfg.QUADRATIC_CONFIG['winsorize'] = {}
    _cfg.INTERACTION_CONFIG['terms'] = [{
        'name': interaction_name,
        'left': left_col,
        'right': right_col,
        'zscore': False,
    }]
    _cfg.INTERACTION_CONFIG['plots'] = [{
        'name': interaction_name,
        'var_x': left_col,
        'var_y': right_col,
        'use_z': False,
        'var_x_label': var_x_label or left_col,
        'var_y_label': var_y_label or (right_col or ''),
    }]
    # Override winsorize from RUN_PROFILE (e.g. {'enabled': False} to turn off for this run)
    if 'winsorize' in run_profile:
        _cfg.STANDARDIZE_CONFIG['winsorize'] = {**_cfg.STANDARDIZE_CONFIG.get('winsorize', {}), **run_profile['winsorize']}
    # Override interaction plot options from RUN_PROFILE (override key -> INTERACTION_CONFIG key)
    if 'interaction_percentile_range' in run_profile:
        _cfg.INTERACTION_CONFIG['percentile_range'] = run_profile['interaction_percentile_range']
    if 'interaction_log_z' in run_profile:
        _cfg.INTERACTION_CONFIG['log_z'] = run_profile['interaction_log_z']
    if 'interaction_log_xy' in run_profile:
        _cfg.INTERACTION_CONFIG['log_xy'] = run_profile['interaction_log_xy']            
    if 'interaction_slice_x_at' in run_profile:
        _cfg.INTERACTION_CONFIG['slice_x_at'] = run_profile['interaction_slice_x_at']   
    if 'interaction_slice_y_range' in run_profile:
        _cfg.INTERACTION_CONFIG['slice_y_range'] = run_profile['interaction_slice_y_range']    
    # CR plots: one per tv_var + interaction, same scale (raw or z); merge cr_plot_defaults for one-swipe bin/etc. changes
    plot_vars = linear_cols + [interaction_name]
    _base_cr = {
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
    cr_defaults = run_profile.get('cr_plot_defaults') or {}
    _cfg.PLOT_CONFIG['plots'] = [
        {**_base_cr, **cr_defaults, 'variable': v, 'name': f"{plot_prefix}_cr_{v}"}
        for v in plot_vars
    ]
    # Cell 12.6A combined-effect plot: which quadratic base to plot (override via combined_effect_base, else first)
    _combo_base_raw = run_profile.get('combined_effect_base') or (quadratic_bases[0] if quadratic_bases else None)
    combo_base_col = (f"{prefix}{_combo_base_raw}" if use_z else _combo_base_raw) if _combo_base_raw else None
    return {'USE_Z_FOR_RUN': use_z, 'COMBINED_EFFECT_BASE_COL': combo_base_col}


# ============================================================================
# === 6.2. INTERACTION SETTINGS (CELL 12.7) ===
# ============================================================================
# One centralized config controls interaction surface plots in Cell 12.7.
#
# plots: define which variable pairs to plot in Cell 12.7
#   - Each entry: {'name': str, 'var_x': str, 'var_y': str, 'use_z': bool}
#   - Optional labels: 'var_x_label' / 'var_y_label' for presentation-friendly axes
#   - Optional distribution overrides:
#       'dist_bins' (str or int), 'dist_min_bins', 'dist_max_bins', 'dist_color'
INTERACTION_CONFIG = {
    'enabled': True,
    # X/Y axis range: None = full range [5, 95]th percentile; set to [75, 100] to zoom to high-high corner
    'percentile_range': None,
    # Log scale: log_z = hazard ratio (z-axis / color); log_xy = x and y axes (only when both > 0, e.g. raw)
    'log_z': False,
    'log_xy': False,
    # 1D slice: fix x at top (e.g. super top-block TB ratio), plot HR vs y over top of pool range
    # slice_x_at: None | 'max' | float (percentile e.g. 99); slice_y_range: [90, 100] = y axis 90th-100th pct
    'slice_x_at': None,
    'slice_y_range': [90, 100],
    
    'terms': [
        {
            'name': 'star_pool_interaction',
            'left': TB_RATIO_SNR_COL,
            'right': POOL_CONTEXT_SNR_COL,
            'zscore': False,
        },
    ],
    'plots': [
        {
            'name': 'star_pool_interaction',
            'var_x': TB_RATIO_SNR_COL,
            'var_y': POOL_MINUS_MEAN_SNR_COL,
            'use_z': False,
            # Optional: override axis labels for presentation
            'var_x_label': None,
            'var_y_label': None,
        },
    ],
}

# ============================================================================
# === 6.3. DISTRIBUTION PLOT SETTINGS (CELL 12.7) ===
# ============================================================================
# Controls the histogram styling and binning rules used for the
# post-interaction variable distribution plots.
DISTRIBUTION_PLOT_CONFIG = {
    'bins': 'fd',          # 'fd', 'scott', 'sturges', or an int
    'min_bins': 10,        # Minimum bins when using a rule
    'max_bins': 60,        # Maximum bins when using a rule
    'color': 'steelblue',  # Histogram color
}

# Build combined time_varying_cols list (base + OER + prestige)
_tv_cols = (
    COLUMN_CONFIG.get('base_time_varying_cols', [])
    + COLUMN_CONFIG.get('oer_variables', [])
    + COLUMN_CONFIG.get('prestige_variables', [])
)
# Preserve order while removing duplicates
COLUMN_CONFIG['time_varying_cols'] = list(dict.fromkeys(_tv_cols))

# ============================================================================
# === 7. PLOT CONFIGURATION (CELL 11) ===
# ============================================================================
# Configuration for Kaplan-Meier and competing risks plots
#
# PLOT STRUCTURE:
# - Each plot is a dictionary with required keys: 'name', 'variable', 'group_by', 'plot_type'
# - Optional keys: 'bin_continuous', 'n_bins', 'bin_method', 'min_group_size', 
#   'use_time_varying', 'filter_zero_oer', 'filter_nan_variable', 'filter_nan_group_by'
# - Add plot dictionaries to the 'plots' list to generate them
#
# ENHANCED PLOT FEATURES (automatic):
# - Descriptive filenames: Auto-generated from plot configuration (includes plot type, variable,
#   grouping, binning method, filter status, and date range)
# - Enhanced titles: Human-readable titles with variable and grouping information
# - Subtitles: Configuration details (bins, sample size, filter status)
# - Enhanced legends: Statistics for each group (N, averages, ranges, final CIF)
# - Configuration boxes: Text box in bottom-right corner with full configuration details
# - Metadata files: JSON files saved alongside plots with complete configuration and data stats
#   (filename: {plot_filename}_metadata.json)

PLOT_CONFIG = {
    # === PLOT SETTINGS ===
    'plot_dir': './cox/cox_plots',   # Directory where plots will be saved (created automatically)
    'figsize': (10, 8),              # Figure size in inches (width, height) - larger = more detail but bigger files
    'dpi': 400,                      # Resolution for saved plots (dots per inch) - 300 is publication quality
    'font_size': None,               # Base font size (None = auto-calculate from figsize, or set to number like 12)
    'include_z_cols': False,         # If True, include z_ columns in Cell 11 when available
    'show_metadata_cards': True,     # If True, display metadata cards inline in CELL 11
    'plot_cif_bars': True,           # If True, add CIF bar plots for competing risks
    'cif_bar_legend_outside': True,  # If True, place CIF bar legend outside the plot
    # Appearance toggles (paper-friendly defaults; set True to restore legacy labels)
    'show_plot_titles': True,        # Main plot titles in Cell 11 (KM/CR) and Cell 12.7 (interaction / 3D)
    'show_plot_subtitles': False,    # Subtitles under titles (config summary text)
    'km_legend_outside': True,       # KM legend outside plot area (legacy style)
    'cr_legend_outside': False,      # CR legends outside plot area (legacy style)
    'legend_show_final_cif': False,  # Append final CIF values to legend labels
    'cif_bar_show_titles': False,    # CIF bar-panel titles ("Final CIF: Promotion/Attrition")
    'cif_bar_show_xlabels': False,   # CIF bar-panel x-axis label ("Bin" or group_by name)
    # Per-plot (plot_spec): cr_color_mode husl|tab20|set1|glasbey matches CR curves; cif_bar_xtick_labels group|quantile
    # If True, KM/CR drops rows where group_by is NaN or placeholder Unknown (title case from merge; any case matched)
    'exclude_unknown_div_name': False,
    
    # === REFERENCE LINE SETTINGS ===
    # Reference lines help visualize promotion zones (Primary Zone, Above Zone)
    # These vertical lines show when officers typically get promoted (PZ) or are "above zone" (AZ)
    'reference_lines': {
        'show_pz_line': True,        # Show Primary Zone reference line (typically 6 years from DOR CPT)
        'show_az_line': True,        # Show Above Zone reference line (typically 7 years from DOR CPT)
        'pz_years': 6,               # Primary zone years (converted to days for plotting)
        'start_time': 0,             # Start time for plots (days from dor_cpt, usually 0)
    },
    
    # === EXAMPLE PLOT SPECIFICATIONS ===
    # Uncomment and modify these examples to create your own plots
    # Copy the examples below into the 'plots' list to activate them
    
    # ========================================================================
    # EXAMPLE 1: KAPLAN-MEIER PLOT - TB Ratio by Year Group
    # ========================================================================
    # Kaplan-Meier plots show survival curves (probability of NOT being promoted over time)
    # This example groups officers by year group and shows how TB ratio affects promotion
    # {
    #     'name': 'km_tb_ratio_by_yg',                    # Unique plot name (used internally and in metadata)
    #                                                      # NOTE: Actual filename is auto-generated with enhanced description
    #                                                      #       Format: {plot_type}_{variable}_{group_by}_{bins}_{method}_{filter}_{dates}.png
    #                                                      #       Example: km_tb_ratio_bwd_snr_by_yg_b3_q_all_2000-2022.png
    #                                                      # Use descriptive names: km_ = Kaplan-Meier, cr_ = Competing Risks
    #     
    #     'variable': 'tb_ratio_bwd_snr',                # Variable to analyze (MUST be in COLUMN_CONFIG time_varying_cols or static_cols)
    #                                                      # This is the variable that will be binned/grouped
    #                                                      # Can be None if you just want to group by 'group_by' without analyzing a variable
    #     
    #     'group_by': 'yg',                               # Grouping variable (creates separate survival curves per group)
    #                                                      # Can be same as 'variable' or different (e.g., group by year group)
    #                                                      # Can be None if you just want to bin 'variable' without additional grouping
    #                                                      # Must be a column in your data
    #     
    #     'plot_type': 'kaplan_meier',                    # Plot type: 'kaplan_meier' (single event) or 'competing_risks' (multiple events)
    #                                                      # Kaplan-Meier: Shows probability of promotion over time (single curve per group)
    #                                                      # Competing Risks: Shows both promotion AND attrition probabilities (2 subplots)
    #     
    #     'bin_continuous': True,                         # Set True to bin continuous variables into groups (e.g., Low/Med/High)
    #                                                      # Required for continuous variables (more than ~10 unique values)
    #                                                      # Set False for categorical variables (yg, sex, prestige_unit, etc.)
    #     
    #     'n_bins': 3,                                    # Number of bins to create (e.g., 3 = Low/Med/High)
    #                                                      # For quantile method: creates equal-sized groups (33rd, 66th percentiles)
    #                                                      # For equal_width method: creates equal-width bins across value range
    #     
    #     'bin_method': 'quantile',                       # Binning method: 'quantile' (equal-sized groups) or 'equal_width' (equal-width bins)
    #                                                      # 'quantile': Divides data into n_bins groups with equal numbers of officers
    #                                                      #            Better for skewed distributions (most officers in one range)
    #                                                      # 'equal_width': Divides value range into n_bins equal-width bins
    #                                                      #               Better for uniform distributions
    #     
    #     'min_group_size': 50,                           # Minimum number of officers per group (groups smaller than this are excluded)
    #                                                      # Prevents plots with too few data points (unreliable estimates)
    #                                                      # Adjust based on your sample size (larger datasets can use higher thresholds)
    #     
    #     'use_time_varying': True,                       # Use time-varying values (True) or static values (False)
    #                                                      # True: Uses value at each snapshot (for time-varying variables like OER metrics)
    #                                                      #       Aggregates to officer-level using LAST snapshot value
    #                                                      # False: Uses value at last snapshot only (for static analysis)
    #                                                      # Default: True (recommended for time-varying variables)
    #     
    #     'filter_zero_oer': True,                        # Filter out officers with NO OER data (NaN values)
    #                                                      # True: Excludes officers who have NaN for OER variables (no OER records)
    #                                                      #       Keeps officers with OER data but 0 top blocks (valid data, just low performance)
    #                                                      # False: Includes all officers (may have many NaN values if OER data is sparse)
    #                                                      # Only applies if 'variable' is an OER-related variable (checked automatically)
    #
    #     'filter_nan_variable': False,                   # If True, drop rows where the plotted variable is NaN
    #                                                      # Use this to remove the 'nan' bin entirely
    #                                                      # Applies regardless of filter_zero_oer
    #
    #     'strict_equal_n': False,                        # Force equal-N bins using rank-based quantiles
    #
    #     'x_max_days': None,                             # Optional: cap x-axis at N days (trims long-tail outliers)
    #
    #     # OPTIONAL: Bin the group_by column separately (for 3x3, 4x2, etc.)
    #     'bin_group_by': False,                          # Set True to bin the group_by variable as well
    #     'group_bins': 3,                                # Number of bins for group_by (defaults to n_bins)
    #     'group_bin_method': 'quantile',                 # Binning method for group_by (defaults to bin_method)
    # },
    
    # ========================================================================
    # EXAMPLE 2: COMPETING RISKS PLOT - Prestige Unit Effect
    # ========================================================================
    # Competing risks plots show TWO curves: promotion probability AND attrition probability
    # This example compares officers in prestige units vs. non-prestige units
    # {
    #     'name': 'cr_prestige_unit',                     # Unique plot name (cr_ prefix indicates competing risks)
    #     
    #     'variable': 'prestige_unit',                    # Variable to analyze (binary: 0 = not prestige, 1 = prestige)
    #                                                      # Can be None if you just want to group by 'group_by'
    #     
    #     'group_by': 'prestige_unit',                    # Group by same variable (creates 2 groups: 0 and 1)
    #                                                      # Each group gets its own pair of curves (promotion + attrition)
    #                                                      # Can be None if you just want to bin 'variable'
    #     
    #     'plot_type': 'competing_risks',                 # Competing risks shows BOTH promotion (event=1) AND attrition (event=2)
    #                                                      # Creates 2 subplots: top = promotion CIF, bottom = attrition CIF
    #                                                      # CIF = Cumulative Incidence Function (probability of event by time t)
    #                                                      # Useful for understanding trade-offs (promotion vs. leaving)
    #     
    #     'bin_continuous': False,                        # No binning needed for binary variable (already 0 or 1)
    #                                                      # Set False for categorical variables (yg, sex, prestige_unit, etc.)
    #                                                      # Set True only for continuous variables (ratios, counts, etc.)
    #     
    #     'n_bins': 3,                                    # Ignored when bin_continuous=False, but must be present
    #     
    #     'bin_method': 'quantile',                       # Ignored when bin_continuous=False, but must be present
    #     
    #     'min_group_size': 50,                           # Minimum officers per group (excludes groups smaller than this)
    #                                                      # For binary variables, both groups should meet this threshold
    #     
    #     'use_time_varying': True,                       # Use time-varying values (prestige_unit can change over time)
    #                                                      # True: Officer can move in/out of prestige units
    #                                                      #       Uses last snapshot value when aggregating to officer-level
    #                                                      # False: Uses prestige_unit at last snapshot only
    #     
    #     'filter_zero_oer': False,                       # Not applicable for prestige_unit (not an OER variable)
    #                                                      # Set False for non-OER variables
    # },
    
    # === ACTIVE PLOTS ===
    # Add your plot specifications here (uncomment examples above or create new ones)
    # Each plot dictionary will generate:
    #   - A plot file in the plot_dir directory (with descriptive auto-generated filename)
    #   - A metadata JSON file alongside the plot (with complete configuration and data stats)
    'plots': [
        # Add plot specifications here
        # Each plot is a dictionary with required keys:
        #   - 'name': str (unique identifier, used internally and in metadata)
        #              NOTE: Actual filename is auto-generated with enhanced description
        #   - 'variable': str or None (column name to analyze, must be in COLUMN_CONFIG, or None for grouping only)
        #   - 'group_by': str or None (column name to group by, creates separate curves, or None)
        #   - 'plot_type': str ('kaplan_meier' or 'competing_risks')
        #   - 'bin_continuous': bool (True for continuous variables, False for categorical)
        #   - 'n_bins': int (number of bins, ignored if bin_continuous=False)
        #   - 'bin_method': str ('quantile' or 'equal_width', ignored if bin_continuous=False)
        #   - 'min_group_size': int (minimum officers per group)
        #   - 'use_time_varying': bool (True for time-varying vars, False for static, default True)
        #   - 'filter_zero_oer': bool (True to exclude officers with no OER data, only for OER variables)
        #   - 'filter_nan_variable': bool (True to drop rows where variable is NaN)
        #   - 'filter_nan_group_by': bool (True to drop rows where group_by is NaN)
        #   - 'strict_equal_n': bool (force equal-N bins with rank-based qcut)
        #   - 'x_max_days': int or None (cap x-axis at N days)
        #   - 'bin_group_by': bool (True to bin group_by separately)
        #   - 'group_bins': int (number of bins for group_by, defaults to n_bins)
        #   - 'group_bin_method': str ('quantile' or 'equal_width' for group_by)
        #
        # OUTPUT FILES:
        #   - Plot: {plot_type}_{variable}_{group_by}_{bins}_{method}_{filter}_{dates}.png
        #   - Metadata: {plot_type}_{variable}_{group_by}_{bins}_{method}_{filter}_{dates}_metadata.json
        ########################################################################################################################################
        {    # 1: TB ratio (mode-specific, raw)
            'variable': TB_RATIO_SNR_COL,
            'name': 'cr_' + TB_RATIO_SNR_COL,
            'group_by': None,
            'plot_type': 'competing_risks',
            'bin_continuous': True,
            'n_bins': 5,
            'bin_method': 'quantile',
            'min_group_size': 3,
            'use_time_varying': True,
            'filter_zero_oer': True,
            'filter_nan_variable': True,
            'filter_nan_group_by': True,
            'strict_equal_n': False,
            'x_min_days': 1000,
            'x_max_days': 4500,
            'bin_group_by': True,
            'group_bins': 3,
            'group_bin_method': 'equal_width',
        },
########################################################################################################################################
        {    # 2: Pool minus-mean (raw)
            'variable': POOL_MINUS_MEAN_SNR_COL,
            'name': 'cr_' + POOL_MINUS_MEAN_SNR_COL,
            'group_by': None,
            'plot_type': 'competing_risks',
            'bin_continuous': True,
            'n_bins': 5,
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
        },
########################################################################################################################################
        {    # 7: Interaction (raw)
            'variable': 'star_pool_interaction',
            'name': 'cr_' + 'star_pool_interaction',
            'group_by': None,
            'plot_type': 'competing_risks',
            'bin_continuous': True,
            'n_bins': 3,
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
        },
#######################################################################################################################################
#         {    # 10: TB ratio (backward)
#             'variable': TB_RATIO_BWD_SNR_COL,
#             'name': 'cr_' + TB_RATIO_BWD_SNR_COL,
#             'group_by': None,
#             'plot_type': 'competing_risks',
#             'bin_continuous': True,
#             'n_bins': 3,
#             'bin_method': 'quantile',
#             'min_group_size': 3,
#             'use_time_varying': True,
#             'filter_zero_oer': True,
#             'filter_nan_variable': True,
#             'filter_nan_group_by': True,
#             'strict_equal_n': False,
#             'x_max_days': 4500,
#             'bin_group_by': True,
#             'group_bins': 3,
#             'group_bin_method': 'equal_width',
#         },
# ########################################################################################################################################
#         {    # 15: Plot TB ratio vs rank norm
#             'variable': TB_RATIO_SNR_COL,
#             'name': 'cr_' + TB_RATIO_SNR_COL + '_vs_' + POOL_TB_RATIO_RANK_PCT_SNR_COL,
#             'group_by': POOL_TB_RATIO_RANK_PCT_SNR_COL,
#             'plot_type': 'competing_risks',
#             'bin_continuous': True,
#             'n_bins': 3,
#             'bin_method': 'equal_width',
#             'min_group_size': 3,
#             'use_time_varying': True,
#             'filter_zero_oer': True,
#             'filter_nan_variable': True,
#             'filter_nan_group_by': True,
#             'strict_equal_n': False,
#             'x_max_days': 4500,
#             'bin_group_by': True,
#             'group_bins': 3,
#             'group_bin_method': 'equal_width',
#         },
# #######################################################################################################################################
#         {    # 16: Pool TB ratio percentile (0-1, 1.0 = best)
#             'variable': POOL_TB_RATIO_RANK_PCT_SNR_COL,
#             'name': 'cr_' + POOL_TB_RATIO_RANK_PCT_SNR_COL,
#             'group_by': None,
#             'plot_type': 'competing_risks',
#             'bin_continuous': True,
#             'n_bins': 3,
#             'bin_method': 'quantile',
#             'min_group_size': 3,
#             'use_time_varying': True,
#             'filter_zero_oer': True,
#             'filter_nan_variable': True,
#             'filter_nan_group_by': True,
#             'strict_equal_n': False,
#             'x_max_days': 4500,
#             'bin_group_by': True,
#             'group_bins': 3,
#             'group_bin_method': 'equal_width',
#         },
    ],
}

# === 7.1. MODEL DEFAULTS FROM PLOT CONFIG ===
# ========================================================================
# Build plot_cols from PLOT_CONFIG['plots'] and use them as the default model
# variable lists when explicit model_*_cols are not provided
plot_cols = set()
for plot_spec in PLOT_CONFIG.get('plots', []):
    if isinstance(plot_spec, dict):
        var = plot_spec.get('variable')
        group_by = plot_spec.get('group_by')
        if var:
            plot_cols.add(var)
        if group_by:
            plot_cols.add(group_by)

# Default model variable lists to plot_cols (intersected with candidates)
if not COLUMN_CONFIG.get('model_static_cols'):
    COLUMN_CONFIG['model_static_cols'] = [
        col for col in COLUMN_CONFIG.get('static_cols', []) if col in plot_cols
    ]
if not COLUMN_CONFIG.get('model_time_varying_cols'):
    COLUMN_CONFIG['model_time_varying_cols'] = [
        col for col in COLUMN_CONFIG.get('time_varying_cols', []) if col in plot_cols
    ]

# Optionally swap model columns to use standardized versions
if STANDARDIZE_CONFIG.get('enabled') and STANDARDIZE_CONFIG.get('use_for_model'):
    _std_cols = STANDARDIZE_CONFIG.get('cols') or (
        COLUMN_CONFIG.get('model_static_cols', []) + COLUMN_CONFIG.get('model_time_varying_cols', [])
    )   
    _prefix = STANDARDIZE_CONFIG.get('prefix', 'z_')
    COLUMN_CONFIG['model_static_cols'] = [
        f"{_prefix}{col}" if col in _std_cols else col
        for col in COLUMN_CONFIG.get('model_static_cols', [])
    ]
    COLUMN_CONFIG['model_time_varying_cols'] = [
        f"{_prefix}{col}" if col in _std_cols else col
        for col in COLUMN_CONFIG.get('model_time_varying_cols', [])        
    ]


# ============================================================================
# === 8. HELPER FUNCTION ===
# ============================================================================

def print_v(message):
    """
    Print with verbose formatting for better readability.
    Only prints if verbose=True in global settings.
    """
    if verbose:
        print(message)
