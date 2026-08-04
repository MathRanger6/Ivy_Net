#!/usr/bin/env bash
# Phase B characterization — refresh PNGs and/or auto-generated slide decks.
#
# YOUR HAND-EDITED DECK IS NEVER OVERWRITTEN:
#   slides/CHAR_Phase_B_characterization.pptx
#
# Usage (repo root):
#   ./scripts/build_characterization_slides.sh
#       → figures only (default) — updates PNG/CSV; no .pptx touched
#
#   ./scripts/build_characterization_slides.sh --auto-slides
#       → also rebuild script decks under slides/auto/ (safe to overwrite)
#
#   ./scripts/build_characterization_slides.sh --auto-slides --no-merge
#       → per-knob auto parts only, no merged auto deck
#
# Hand deck workflow:
#   1. Format equations/layout once in slides/CHAR_Phase_B_characterization.pptx
#   2. Re-run default (figures-only) when sim outputs change
#   3. In PowerPoint: right-click plot → Change Picture → pick updated PNG
#      (paths in pass_b/, pass_c_rho/, theta/, sort_chop_lambda/)
#   4. Use --auto-slides only when you want a fresh disposable template to compare

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="${PYTHON:-python}"
GALLERY="${GALLERY_DIR:-$REPO_ROOT/3-Master_Plan/re_entry/HEROs_and_PASSes}"
SLIDES="$GALLERY/slides"
AUTO="$SLIDES/auto"
HAND="$SLIDES/CHAR_Phase_B_characterization.pptx"
MODE="figures"
MERGE=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --figures-only) MODE="figures" ;;
    --auto-slides) MODE="auto-slides" ;;
    --no-merge) MERGE=0 ;;
    -h|--help)
      sed -n '2,23p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

cd "$REPO_ROOT"
mkdir -p "$AUTO"

_run_figures() {
  echo ">> ρ figures ..."
  "$PYTHON" sports/scripts/pass_c_rho_ablation_bundle.py

  echo ">> λ figures ..."
  "$PYTHON" sports/scripts/pass_b_lambda_ablation_bundle.py

  echo ">> θ figures ..."
  "$PYTHON" sports/scripts/theta_kn_sweep_diagnostic.py
  "$PYTHON" sports/scripts/theta_oat_diagnostic.py

  echo ">> γ figures ..."
  "$PYTHON" sports/scripts/gamma_sweep_diagnostic.py
  "$PYTHON" sports/scripts/build_lambda_gamma_threshold_figure.py
  "$PYTHON" sports/scripts/build_viability_hard_vs_smooth_figure.py
}

echo "=== Phase B characterization refresh ==="
echo "  mode=$MODE"
echo "  hand deck (never overwritten): $HAND"
echo ""

if [[ "$MODE" == "figures" ]]; then
  _run_figures
  echo ""
  echo "Done (figures only). PNG/CSV updated; no .pptx written."
  echo "  To refresh plots in your hand deck, use Change Picture in PowerPoint."
  echo "  Disposable auto decks: ./scripts/build_characterization_slides.sh --auto-slides"
  exit 0
fi

if ! "$PYTHON" -c "import pptx" 2>/dev/null; then
  echo "ERROR: python-pptx required for --auto-slides" >&2
  exit 1
fi

echo ">> Building auto slide decks (slides/auto/) ..."

echo ">> intro slide ..."
"$PYTHON" sports/scripts/build_intro_characterization_slide.py

echo ">> ρ slides ..."
"$PYTHON" sports/scripts/build_rho_characterization_slide.py

echo ">> λ slides ..."
"$PYTHON" sports/scripts/build_lambda_characterization_slide.py

echo ">> θ slides ..."
"$PYTHON" sports/scripts/build_theta_characterization_slide.py

echo ">> γ slides ..."
"$PYTHON" sports/scripts/build_gamma_characterization_slide.py

if [[ "$MERGE" -eq 0 ]]; then
  echo ""
  echo "Done (--no-merge). Auto parts in $AUTO/CHAR_*_characterization_AUTO.pptx"
  exit 0
fi

OUT_AUTO="$AUTO/CHAR_Phase_B_characterization_AUTO.pptx"
echo ""
echo ">> Merge auto deck → $OUT_AUTO"
"$PYTHON" sports/scripts/merge_pptx.py --python "$OUT_AUTO" \
  "$AUTO/CHAR_intro_characterization_AUTO.pptx" \
  "$AUTO/CHAR_rho_characterization_AUTO.pptx" \
  "$AUTO/CHAR_lambda_characterization_AUTO.pptx" \
  "$AUTO/CHAR_theta_characterization_AUTO.pptx" \
  "$AUTO/CHAR_gamma_characterization_AUTO.pptx"

echo ""
echo "Done."
echo "  Auto (disposable): $OUT_AUTO"
echo "  Hand (yours):      $HAND"
