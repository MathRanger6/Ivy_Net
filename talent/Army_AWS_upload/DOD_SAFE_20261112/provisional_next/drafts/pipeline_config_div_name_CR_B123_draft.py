"""
DRAFT — Phase 4: append B1/B2/B3 CR CIF-bar specs to pipeline_config_div_name.

**Do not import this file on Vantage.** After HERO smoke, merge the PLOT_CONFIG block
into live ``pipeline_config_div_name.py`` (or replace file from ``provisional_next/``).

Requires feather columns from Phase 1–2 Cell 5 / 10.5:
  z_pool_mean_snr_fwd, z_pool_loo_snr_fwd, z_pool_minus_loo_snr_fwd (+ bwd optional)
"""

# Paste below into pipeline_config_div_name.py inside ``if USE_OVERRIDE_CR_PLOTS:``
# after existing PLOT_CONFIG['plots'] entries (keep run1_cr_tb, pool minus, interaction, by_div).

_B123_CR_VARS_FWD = (
    (Z_POOL_MEAN_FWD_SNR_COL, "run1_cr_b1_fwd"),
    (Z_POOL_LOO_FWD_SNR_COL, "run1_cr_b2_fwd"),
    (Z_POOL_MINUS_LOO_FWD_SNR_COL, "run1_cr_b3_fwd"),
)

_B123_CR_VARS_BWD = (
    (Z_POOL_MEAN_BWD_SNR_COL, "run1_cr_b1_bwd"),
    (Z_POOL_LOO_BWD_SNR_COL, "run1_cr_b2_bwd"),
    (Z_POOL_MINUS_LOO_BWD_SNR_COL, "run1_cr_b3_bwd"),
)

# Example merge (RUN_SCALE must be 'z'):
# PLOT_CONFIG['plots'].extend(
#     {**RUN_CR_PLOT_DEFAULTS, 'variable': var, 'name': name, 'n_bins': 8}
#     for var, name in _B123_CR_VARS_FWD + _B123_CR_VARS_BWD
# )
