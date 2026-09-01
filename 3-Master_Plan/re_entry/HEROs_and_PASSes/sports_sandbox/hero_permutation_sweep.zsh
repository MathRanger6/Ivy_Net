#!/usr/bin/env zsh
# HERO permutation sweep + PowerPoint deck (Aug 2026)
# Run from repo root: zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero_permutation_sweep.zsh
#
# Tiers:
#   core      — 8 combos (roster-x × y-mode × panel-rows) + FIXED HERO baseline
#   extended  — core + ±DFT (16 non-baseline + baseline)
#   full      — extended + EW20 binning (32 non-baseline + baseline)
#   real_full — full × both season windows (64 runs; ignores arg 2)
#
# Season window (arg 2, ignored for real_full):
#   11_21 (default) | 13_21 | both (doubles run count)

set -euo pipefail
ROOT="${0:A:h}/../../../.."
cd "$ROOT"

TIER="${1:-core}"   # core | extended | full | real_full
SEASON_WIN="${2:-11_21}"   # 11_21 | 13_21 | both
FORCE="${3:-}"      # pass "force" to re-run existing PNGs

if [[ "$TIER" == "real_full" ]]; then
  SEASON_WIN="both"
fi

echo "=== HERO permutation sweep · tier=$TIER · season=$SEASON_WIN ==="
SWEEP=(python sports/scripts/hero_permutation_sweep.py --tier "$TIER" --season-window "$SEASON_WIN")
[[ -n "$FORCE" ]] && SWEEP+=("--force")
"${SWEEP[@]}"

echo ""
echo "=== Build PowerPoint ==="
python sports/scripts/build_hero_permutation_slides.py

echo ""
echo "Done."
echo "  PNGs:     3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero/"
echo "  Manifest: 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero_permutation_slides/manifest.json"
echo "  Deck:     3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero_permutation_slides/HERO_permutation_slides_AUTO.pptx"
