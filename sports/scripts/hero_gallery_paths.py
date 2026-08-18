"""Canonical paths under re_entry/HEROs_and_PASSes/."""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
HERO_ROOT = _REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"

PASS_A = HERO_ROOT / "pass_a"
PASS_B = HERO_ROOT / "pass_b"
PASS_C_RHO = HERO_ROOT / "pass_c_rho"
SIM_INPUTS = HERO_ROOT / "sim_inputs"
EMPIRICAL_PD17 = HERO_ROOT / "empirical_pd17"
GRANDCHILD_ASSIGN = HERO_ROOT / "grandchild_assign"
PD20_TEMPERATURE = HERO_ROOT / "pd20_temperature"
PD21_MLE = HERO_ROOT / "pd21_mle"
PD21_RHO = HERO_ROOT / "pd21_rho"
PD22_MINUTES = HERO_ROOT / "pd22_minutes"
SORT_CHOP_LAMBDA = HERO_ROOT / "sort_chop_lambda"
SOFT_ASSIGN_LAMBDA = HERO_ROOT / "soft_assign_lambda"
THETA = HERO_ROOT / "theta"
SLIDES = HERO_ROOT / "slides"
GRANDCHILD_LEAGUE_ANALYSIS_DECK = SLIDES / "CHAR_grandchild_league_analysis.pptx"
# Hand-edited masters (scripts never write these).
SLIDES_AUTO = SLIDES / "auto"
HAND_PD16_DECK = SLIDES / "CHAR_PD16_HAND.pptx"
HAND_PD17_DECK = SLIDES / "CHAR_PD17_HAND.pptx"
HAND_PD20_DECK = SLIDES / "CHAR_PD20_HAND.pptx"
# Legacy alias (Aug 2026 rename from CHAR_Phase_B_characterization_HAND.pptx)
HAND_PHASE_B_DECK = HAND_PD16_DECK
HAND_RHO_DECK = SLIDES / "CHAR_rho_characterization.pptx"
HAND_LAMBDA_DECK = SLIDES / "CHAR_lambda_characterization.pptx"
HAND_THETA_DECK = SLIDES / "CHAR_theta_characterization.pptx"
HAND_GAMMA_DECK = SLIDES / "CHAR_gamma_characterization.pptx"
# Disposable script output — always *_AUTO.pptx under SLIDES_AUTO/.
AUTO_INTRO_DECK = SLIDES_AUTO / "CHAR_intro_characterization_AUTO.pptx"
AUTO_SIM_INPUTS_DECK = SLIDES_AUTO / "CHAR_sim_input_distributions_AUTO.pptx"
AUTO_EMPIRICAL_AI_TJ_DECK = SLIDES_AUTO / "CHAR_empirical_ai_tj_distributions_AUTO.pptx"
AUTO_EMPIRICAL_LC_DECK = SLIDES_AUTO / "CHAR_empirical_lc_distributions_AUTO.pptx"
AUTO_EMPIRICAL_GAMMA_LC_DECK = SLIDES_AUTO / "CHAR_empirical_gamma_lc_sweep_AUTO.pptx"
AUTO_EMPIRICAL_OVERLAP_DECK = SLIDES_AUTO / "CHAR_empirical_team_interval_overlap_AUTO.pptx"
AUTO_EMPIRICAL_PD17_INTRO_DECK = SLIDES_AUTO / "CHAR_empirical_pd17_intro_AUTO.pptx"
AUTO_EMPIRICAL_RHO_COVERAGE_DECK = SLIDES_AUTO / "CHAR_empirical_rho_coverage_overlay_AUTO.pptx"
AUTO_RHO_DECK = SLIDES_AUTO / "CHAR_rho_characterization_AUTO.pptx"
AUTO_LC_CONGESTION_DECK = SLIDES_AUTO / "CHAR_lc_congestion_characterization_AUTO.pptx"
AUTO_LAMBDA_DECK = SLIDES_AUTO / "CHAR_lambda_characterization_AUTO.pptx"
AUTO_THETA_DECK = SLIDES_AUTO / "CHAR_theta_characterization_AUTO.pptx"
AUTO_GAMMA_DECK = SLIDES_AUTO / "CHAR_gamma_characterization_AUTO.pptx"
AUTO_SOFT_ASSIGN_GAMMA_DECK = SLIDES_AUTO / "CHAR_soft_assign_gamma_sweep_AUTO.pptx"
AUTO_PD20_DECK = SLIDES_AUTO / "CHAR_PD20_HAND_AUTO.pptx"
AUTO_PD21_RHO_DECK = SLIDES_AUTO / "CHAR_PD21_rho_hsort_calibrate_AUTO.pptx"
AUTO_PD21_RHO_TIMESERIES_DECK = SLIDES_AUTO / "CHAR_PD21_rho_hsort_timeseries_AUTO.pptx"
AUTO_PD22_DRAFTED_MINUTES_DECK = SLIDES_AUTO / "CHAR_PD22_drafted_minutes_audit_AUTO.pptx"
AUTO_PD22_RAW_MINUTES_DECK = SLIDES_AUTO / "CHAR_PD22_raw_minutes_distribution_AUTO.pptx"
AUTO_PD22_PPM_DISTRIBUTION_DECK = SLIDES_AUTO / "CHAR_PD22_ppm_distribution_AUTO.pptx"
AUTO_PD22_PPM_OVERLAY_DECK = SLIDES_AUTO / "CHAR_PD22_ppm_full_vs_filtered_AUTO.pptx"
AUTO_PD22_PPM_ZERO_ABILITY_DECK = SLIDES_AUTO / "CHAR_PD22_ppm_zero_ability_distribution_AUTO.pptx"
AUTO_PD22_PPM_ZERO_HSORT_DECK = SLIDES_AUTO / "CHAR_PD22_ppm_zero_hsort_mechanism_AUTO.pptx"
AUTO_PD22_PANEL_POLICY_COMPARE_DECK = SLIDES_AUTO / "CHAR_PD22_panel_policy_compare_AUTO.pptx"
AUTO_PD22_RAW_ROSTER_SIZE_DECK = SLIDES_AUTO / "CHAR_PD22_raw_roster_size_distribution_AUTO.pptx"
AUTO_PD22_RAW_ROSTER_SIZE_BEFORE_QC_DECK = (
    SLIDES_AUTO / "CHAR_PD22_raw_roster_size_distribution_before_qc_AUTO.pptx"
)
AUTO_PD22_RAW_ROSTER_SIZE_AFTER_QC_DECK = (
    SLIDES_AUTO / "CHAR_PD22_raw_roster_size_distribution_after_qc_AUTO.pptx"
)
AUTO_PD22_TEAM_SEASON_GAMES_DECK = SLIDES_AUTO / "CHAR_PD22_team_season_games_count_AUTO.pptx"
AUTO_PD22_TEAM_SEASON_GAMES_AFTER_QC_DECK = (
    SLIDES_AUTO / "CHAR_PD22_team_season_games_count_after_qc_AUTO.pptx"
)
AUTO_PD22_ESPN_COVERAGE_DECK = SLIDES_AUTO / "CHAR_PD22_espn_coverage_by_season_AUTO.pptx"
AUTO_PHASE_B_DECK = SLIDES_AUTO / "CHAR_Phase_B_characterization_AUTO.pptx"

_ALL_DIRS = (
    PASS_A,
    PASS_B,
    PASS_C_RHO,
    SIM_INPUTS,
    EMPIRICAL_PD17,
    GRANDCHILD_ASSIGN,
    PD20_TEMPERATURE,
    PD21_MLE,
    PD21_RHO,
    PD22_MINUTES,
    SORT_CHOP_LAMBDA,
    SOFT_ASSIGN_LAMBDA,
    THETA,
    SLIDES,
    SLIDES_AUTO,
)


def ensure_hero_dirs() -> None:
    for d in _ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)
