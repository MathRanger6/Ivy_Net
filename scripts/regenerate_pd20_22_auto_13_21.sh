#!/usr/bin/env bash
# Regenerate PD20–22 AUTO slides + PNGs for 2013–2021 (drops 2011–2012).
#
# Does NOT overwrite the default 2011–2021 artifacts:
#   PNG/JSON/CSV → *_2013_2021.*
#   AUTO .pptx   → *_13_21_AUTO.pptx  (under slides/auto/)
#
# Usage (repo root):
#   ./scripts/regenerate_pd20_22_auto_13_21.sh
#   SLIDES_ONLY=1 ./scripts/regenerate_pd20_22_auto_13_21.sh   # decks only
#   PLOT_ONLY=1   ./scripts/regenerate_pd20_22_auto_13_21.sh   # replot, no panel rebuild
#   RHO_SEEDS=20 ./scripts/regenerate_pd20_22_auto_13_21.sh  # faster ρ bracket (smoke)
#
# Env:
#   PY          Python executable (default: python)
#   RHO_JOBS    Parallel workers for pd21_rho_hsort_calibrate (default: 8)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="${PY:-python}"
# Figure/analysis scripts: season window only (no --auto-suffix).
SEASON_WIN=(--season-min 2013 --season-max 2021)
# Slide builders: season window + AUTO .pptx suffix.
SLIDE_WIN=(--season-min 2013 --season-max 2021 --auto-suffix _13_21)

export PD20_22_SEASON_MIN=2013
export PD20_22_SEASON_MAX=2021
export PD20_22_AUTO_SUFFIX=_13_21

SLIDES_ONLY="${SLIDES_ONLY:-0}"
PLOT_ONLY="${PLOT_ONLY:-0}"
RHO_SEEDS="${RHO_SEEDS:-50}"
RHO_JOBS="${RHO_JOBS:-8}"

slide_flags=("${SLIDE_WIN[@]}")
plot_flags=()
if [[ "$SLIDES_ONLY" == "1" ]]; then
  slide_flags+=(--slides-only)
fi
if [[ "$PLOT_ONLY" == "1" ]]; then
  plot_flags=(--plot-only)
fi

run_py() {
  echo ""
  echo "=== $*"
  "$PY" "$@"
}

echo "PD20–22 AUTO regeneration · window 2013–2021 · suffix _13_21"
echo "  SLIDES_ONLY=$SLIDES_ONLY  PLOT_ONLY=$PLOT_ONLY  RHO_SEEDS=$RHO_SEEDS"

if [[ "$SLIDES_ONLY" != "1" ]]; then
  if [[ "$PLOT_ONLY" == "1" ]]; then
    echo ""
    echo "--- Phase 1: skipped (PLOT_ONLY — temperature scripts have no --plot-only) ---"
  else
    echo ""
    echo "--- Phase 1: PD20 temperature (figures) ---"
    run_py sports/scripts/grandchild_temperature_select_sweep.py "${SEASON_WIN[@]}"
    run_py sports/scripts/grandchild_temperature_cold_limit_diagnostic.py "${SEASON_WIN[@]}"
  fi

  echo ""
  echo "--- Phase 2: PD22 panel backup (figures) ---"
  run_py sports/scripts/pd22_raw_roster_size_distribution.py --before-qc-only "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_team_season_games_count.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_team_season_games_count.py --after-qc-only "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_raw_roster_size_distribution.py --after-qc-only "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_espn_coverage_by_season.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_drafted_minutes_audit.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_raw_minutes_distribution.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_ppm_distribution.py "${SEASON_WIN[@]}" "${plot_flags[@]}"

  echo ""
  echo "--- Phase 3: PD21 ρ calibration (slow — bracket search) ---"
  if [[ "$PLOT_ONLY" == "1" ]]; then
    run_py sports/scripts/pd21_rho_hsort_calibrate.py --plot-only "${SEASON_WIN[@]}"
    run_py sports/scripts/pd21_rho_hsort_calibrate.py --plot-only --ppm-zero-below-minutes 20 "${SEASON_WIN[@]}"
  else
    run_py sports/scripts/pd21_rho_hsort_calibrate.py --n-seeds "$RHO_SEEDS" --n-jobs "$RHO_JOBS" --fresh "${SEASON_WIN[@]}"
    run_py sports/scripts/pd21_rho_hsort_calibrate.py --n-seeds "$RHO_SEEDS" --n-jobs "$RHO_JOBS" --fresh --ppm-zero-below-minutes 20 "${SEASON_WIN[@]}"
  fi

  echo ""
  echo "--- Phase 4: PD22 policy + overlap (figures) ---"
  run_py sports/scripts/pd22_ppm_zero_ability_distribution.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_ppm_zero_hsort_mechanism.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_panel_policy_compare.py "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_interval_overlap_season.py --season 2012 "${SEASON_WIN[@]}" "${plot_flags[@]}"
  run_py sports/scripts/pd22_interval_overlap_season.py --season 2013 "${SEASON_WIN[@]}" "${plot_flags[@]}"
fi

echo ""
echo "--- Phase 4b: Pass A hero (empirical inverted-U, 2013–2021) ---"
run_py sports/scripts/pass_a_empirical_bundle.py "${SEASON_WIN[@]}"
run_py sports/scripts/build_pass_abc_slides.py "${SLIDE_WIN[@]}"

echo ""
echo "--- Phase 5: AUTO slide decks ---"
run_py sports/scripts/build_pd20_hand_slides.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_raw_roster_size_before_qc_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_team_season_games_count_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_team_season_games_count_after_qc_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_raw_roster_size_after_qc_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_espn_coverage_by_season_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_drafted_minutes_audit_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_raw_minutes_distribution_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_ppm_distribution_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd21_rho_hsort_calibrate_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd21_rho_hsort_calibrate_slide.py --ppm-zero-below-minutes 20 "${slide_flags[@]}"
run_py sports/scripts/build_pd21_rho_hsort_timeseries_slide.py --ppm-zero-below-minutes 20 "${slide_flags[@]}"
run_py sports/scripts/build_pd22_ppm_zero_ability_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_ppm_zero_hsort_mechanism_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_panel_policy_compare_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd22_interval_overlap_season_slide.py --season 2012 "${slide_flags[@]}"
run_py sports/scripts/build_pd22_interval_overlap_season_slide.py --season 2013 "${slide_flags[@]}"
run_py sports/scripts/build_pd20_22_takeaways_memo.py "${SLIDE_WIN[@]}"

echo ""
echo "Done. AUTO decks: 3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/*_13_21_AUTO.pptx"
echo "Figures/JSON:    pd20_temperature/, pd21_rho/, pd22_minutes/ (*_2013_2021.*)"
