#!/usr/bin/env zsh
# One-knob HERO probes from NEW FIXED HERO (13-21 · last-ps · q16 · LOO · ALLT).
# Usage: zsh hero_neighborhood_sweep.zsh [force]
set -euo pipefail
ROOT="${0:A:h}/../../../.."
cd "$ROOT"

OUT="3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/HERO_neighborhood"
SCRIPT="python sports/scripts/pass_a_empirical_bundle.py"
FORCE="${1:-}"

run() {
  local tag="$1"
  shift
  local png="${OUT}/HERO_q16_allt_min20_mg10_13_21_last_ps_${tag}.png"
  if [[ -f "$png" && "$FORCE" != "force" ]]; then
    echo "SKIP (exists): $tag"
    return 0
  fi
  echo "RUN: $tag"
  $SCRIPT \
    --season-min 2013 --season-max 2021 \
    --y-draft-mode ever --panel-rows last-ps \
    --roster-x poolq_loo --n-bins 16 --poolq-binning quantile \
    --output-tag "$tag" \
    --output-root "$OUT" \
    "$@"
}

mkdir -p "$OUT"

# Base
run NEW_FIXED_HERO

# One-knob neighbors
run probe_allps --panel-rows all-ps
run probe_ew16 --poolq-binning equal_width --n-bins 16
run probe_ew20 --poolq-binning equal_width --n-bins 20
run probe_q20 --poolq-binning quantile --n-bins 20
run probe_seasony --y-draft-mode season
run probe_dft --dft
run probe_11_21 --season-min 2011 --season-max 2021
run probe_mg0 --min-team-season-games 0
run probe_poolq --roster-x poolq

echo "Done — outputs in $OUT"
