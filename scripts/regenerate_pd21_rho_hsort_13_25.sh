#!/usr/bin/env bash
# Extend the locked hero panel through 2022–2025 and rerun PD21 ρ* / H_sort calibration.
#
# ESPN box rows for 2022–2025 are already in datasets/mbb/mbb_df_player_box.csv (no box
# rescrape). Draft register still stops at 2021 — Y_draft on new seasons is mostly 0; this
# run is for sorting-index (H_sort) and bracket ρ*, not draft-rate ventiles.
#
# Does NOT overwrite 2011–2021 or 2013–2021 artifacts:
#   PNG/JSON → pd21_rho/PD21_rho_hsort_calibrate_2013_2025[_ppm0lt20]_*
#   AUTO pptx → slides/auto/CHAR_PD21_rho_hsort_calibrate[_ppm0lt20]_13_25_AUTO.pptx
#
# Usage (repo root):
#   ./scripts/regenerate_pd21_rho_hsort_13_25.sh
#   RHO_SEEDS=10 RHO_JOBS=4 ./scripts/regenerate_pd21_rho_hsort_13_25.sh   # faster smoke
#   SLIDES_ONLY=1 ./scripts/regenerate_pd21_rho_hsort_13_25.sh    # decks from existing JSON
#   PLOT_ONLY=1 ./scripts/regenerate_pd21_rho_hsort_13_25.sh      # replot bracket PNGs only
#   HERO_ONLY=1 ./scripts/regenerate_pd21_rho_hsort_13_25.sh      # skip ppm0lt20 contrast
#   SEASON_MIN=2011 SEASON_MAX=2025 ./scripts/regenerate_pd21_rho_hsort_13_25.sh
#
# Env:
#   PY          Python executable (default: python3)
#   RHO_SEEDS   Seeds per season (default: 50)
#   RHO_JOBS    Process pool workers (default: 8)
#   SEASON_MIN  Panel floor (default: 2013 — Alex primary window)
#   SEASON_MAX  Panel ceiling (default: 2025)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="${PY:-python3}"
SEASON_MIN="${SEASON_MIN:-2013}"
SEASON_MAX="${SEASON_MAX:-2025}"
AUTO_SUFFIX="${AUTO_SUFFIX:-_${SEASON_MIN}_${SEASON_MAX}}"

export PD20_22_SEASON_MIN="$SEASON_MIN"
export PD20_22_SEASON_MAX="$SEASON_MAX"
export PD20_22_AUTO_SUFFIX="$AUTO_SUFFIX"

SEASON_WIN=(--season-min "$SEASON_MIN" --season-max "$SEASON_MAX")
SLIDE_WIN=(--season-min "$SEASON_MIN" --season-max "$SEASON_MAX" --auto-suffix "$AUTO_SUFFIX")

SLIDES_ONLY="${SLIDES_ONLY:-0}"
PLOT_ONLY="${PLOT_ONLY:-0}"
HERO_ONLY="${HERO_ONLY:-0}"
RHO_SEEDS="${RHO_SEEDS:-50}"
RHO_JOBS="${RHO_JOBS:-8}"

slide_flags=("${SLIDE_WIN[@]}")
if [[ "$SLIDES_ONLY" == "1" ]]; then
  slide_flags+=(--slides-only)
fi

run_py() {
  echo ""
  echo "=== $*"
  "$PY" "$@"
}

echo "PD21 ρ / H_sort extension · seasons ${SEASON_MIN}–${SEASON_MAX} · suffix ${AUTO_SUFFIX}"
echo "  SLIDES_ONLY=$SLIDES_ONLY  PLOT_ONLY=$PLOT_ONLY  HERO_ONLY=$HERO_ONLY"
echo "  RHO_SEEDS=$RHO_SEEDS  RHO_JOBS=$RHO_JOBS"
echo ""
echo "Note: draft register ends 2021 — new seasons add player-seasons; Y_draft unchanged."

if [[ "$SLIDES_ONLY" != "1" ]]; then
  echo ""
  echo "--- Phase 1: PD21 bracket search (hero panel, min_minutes=20, box QC on) ---"
  if [[ "$PLOT_ONLY" == "1" ]]; then
    run_py sports/scripts/pd21_rho_hsort_calibrate.py --plot-only "${SEASON_WIN[@]}"
  else
    run_py sports/scripts/pd21_rho_hsort_calibrate.py \
      --n-seeds "$RHO_SEEDS" --n-jobs "$RHO_JOBS" --fresh \
      "${SEASON_WIN[@]}"
  fi

  if [[ "$HERO_ONLY" != "1" ]]; then
    echo ""
    echo "--- Phase 2: PD21 bracket search (contrast: ppm0lt20) ---"
    if [[ "$PLOT_ONLY" == "1" ]]; then
      run_py sports/scripts/pd21_rho_hsort_calibrate.py \
        --plot-only --ppm-zero-below-minutes 20 "${SEASON_WIN[@]}"
    else
      run_py sports/scripts/pd21_rho_hsort_calibrate.py \
        --n-seeds "$RHO_SEEDS" --n-jobs "$RHO_JOBS" --fresh \
        --ppm-zero-below-minutes 20 \
        "${SEASON_WIN[@]}"
    fi
  fi
fi

echo ""
echo "--- Phase 3: AUTO slides (bracket + per-season timeseries) ---"
run_py sports/scripts/build_pd21_rho_hsort_calibrate_slide.py "${slide_flags[@]}"
run_py sports/scripts/build_pd21_rho_hsort_timeseries_slide.py "${slide_flags[@]}"
if [[ "$HERO_ONLY" != "1" ]]; then
  run_py sports/scripts/build_pd21_rho_hsort_calibrate_slide.py \
    --ppm-zero-below-minutes 20 "${slide_flags[@]}"
  run_py sports/scripts/build_pd21_rho_hsort_timeseries_slide.py \
    --ppm-zero-below-minutes 20 "${slide_flags[@]}"
fi

TAG="${SEASON_MIN}_${SEASON_MAX}"
echo ""
echo "Done."
echo "  Fit JSON (hero):     3-Master_Plan/re_entry/HEROs_and_PASSes/pd21_rho/PD21_rho_hsort_calibrate_${TAG}_fit_bracket.json"
echo "  Bracket PNG:         .../pd21_rho/PD21_rho_hsort_calibrate_${TAG}_bracket.png"
echo "  Timeseries PNG:      .../pd21_rho/PD21_rho_hsort_calibrate_${TAG}_bracket_rho_hsort_timeseries.png"
echo "  AUTO deck (hero):    3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/CHAR_PD21_rho_hsort_calibrate${AUTO_SUFFIX}_AUTO.pptx"
echo ""
echo "Compare longitudinal rho_star and H_sort vs 2013–2021 fit:"
echo "  .../pd21_rho/PD21_rho_hsort_calibrate_2013_2021_fit_bracket.json"
