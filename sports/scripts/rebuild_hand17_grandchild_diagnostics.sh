#!/usr/bin/env bash
# Rebuild HAND17 grandchild diagnostics + light AUTO slides from this session.
# Run from repo root with sports_net active:
#   bash sports/scripts/rebuild_hand17_grandchild_diagnostics.sh
# Optional: skip long steps
#   bash sports/scripts/rebuild_hand17_grandchild_diagnostics.sh --skip-rho
#   bash sports/scripts/rebuild_hand17_grandchild_diagnostics.sh --slides-only

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

PY="${PYTHON:-python}"
SKIP_RHO=0
SKIP_C=0
SKIP_CAPS=0
SKIP_INTERVAL=0
SKIP_MINUTES=0
SKIP_LAMBDA=0
SLIDES_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --skip-rho) SKIP_RHO=1 ;;
    --skip-c) SKIP_C=1 ;;
    --skip-caps) SKIP_CAPS=1 ;;
    --skip-interval) SKIP_INTERVAL=1 ;;
    --skip-minutes) SKIP_MINUTES=1 ;;
    --skip-lambda) SKIP_LAMBDA=1 ;;
    --slides-only) SLIDES_ONLY=1 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown flag: $arg" >&2
      exit 1
      ;;
  esac
done

run_diag() {
  if [[ "$SLIDES_ONLY" -eq 0 ]]; then
    "$@"
  fi
}

echo "=== HAND17 grandchild rebuild (repo: $REPO) ==="

if [[ "$SKIP_RHO" -eq 0 ]]; then
  echo "[1/6] rho sweep (about 30 min) ..."
  run_diag "$PY" sports/scripts/541_grandchild_rho_sweep.py --progress-every 10
else
  echo "[1/6] rho sweep skipped"
fi

if [[ "$SKIP_C" -eq 0 ]]; then
  echo "[2/6] C sweep 10/11/15 ..."
  run_diag "$PY" sports/scripts/grandchild_roster_size_c_sweep.py --rho 0.5 -C 10 11 15
else
  echo "[2/6] C sweep skipped"
fi

if [[ "$SKIP_CAPS" -eq 0 ]]; then
  echo "[3/6] empirical roster caps ..."
  run_diag "$PY" sports/scripts/grandchild_empirical_roster_caps_diagnostic.py --rho 0.5
else
  echo "[3/6] empirical roster caps skipped"
fi

if [[ "$SKIP_INTERVAL" -eq 0 ]]; then
  echo "[4/6] interval overlap with empirical caps ..."
  run_diag "$PY" sports/scripts/grandchild_league_interval_diagnostic.py \
    --season-min 2011 --season-max 2021 --empirical-roster-caps --rho 0.5
else
  echo "[4/6] interval overlap skipped"
fi

if [[ "$SKIP_MINUTES" -eq 0 ]]; then
  echo "[5/6] min_minutes ladder (optional) ..."
  run_diag "$PY" sports/scripts/hero_min_minutes_sensitivity_ladder.py --minutes 0 10 20
else
  echo "[5/6] min_minutes ladder skipped"
fi

if [[ "$SKIP_LAMBDA" -eq 0 ]]; then
  echo "[6/6] lambda SELECT sweep (empirical caps) ..."
  run_diag "$PY" sports/scripts/grandchild_lambda_select_sweep.py
else
  echo "[6/6] lambda SELECT sweep skipped"
fi

echo "=== light AUTO slides ==="
"$PY" sports/scripts/build_grandchild_rho_global_wss_slide.py --slides-only
"$PY" sports/scripts/build_grandchild_rho_assortativity_slide.py --slides-only
"$PY" sports/scripts/build_alex_roster_size_c_sweep_light_slides.py
"$PY" sports/scripts/build_alex_empirical_roster_caps_light_slides.py
"$PY" sports/scripts/build_alex_lambda_select_sweep_light_slides.py
if [[ "$SKIP_MINUTES" -eq 0 ]]; then
  "$PY" sports/scripts/build_alex_minutes_filter_light_slides.py
fi

echo "Done."
