#!/usr/bin/env bash
# Rebuild Pass A/B/C PNGs → PASS_ABC slides → merge full Alex gallery deck.
#
# Requires: python with python-pptx, matplotlib, pandas (Anaconda base OK).
#   pip install python-pptx
#
# Usage (repo root):
#   ./scripts/rebuild_hero_gallery.sh              # full pipeline
#   ./scripts/rebuild_hero_gallery.sh --merge-only # assemble existing parts only
#   ./scripts/rebuild_hero_gallery.sh --slides-only # PNGs + PASS_ABC, no merge
#
# Knobs (export before run, or edit defaults below):
#   GALLERY_PRESET=539|540
#   GALLERY_HERO_BINS=16
#   GALLERY_HERO_SEED=42
#   GALLERY_RHO_LOW / GALLERY_RHO_MODERATE / GALLERY_RHO_HIGH / GALLERY_RHO_VERY_HIGH
#
# Deck parts (in order) — hand-maintained slides are separate files:
#   1. PASS_ABC_Gallery_Slides.pptx  (auto-built, in HEROs_and_PASSes/slides/)
#   2. Model.pptx                    (you edit — lives in re_entry/, not gallery/)
#   3. Future_Work_Slides.pptx       (optional; re_entry/ or gallery/)
#
# Output: So_Far_.pptx (override with GALLERY_OUT_NAME)
#
# Merge modes:
#   passes-only (default) — python replaces slides 1–3 in So_Far_.pptx; slide 4+ untouched (no PowerPoint)
#   hybrid              — python PASS_ABC; PowerPoint appends Model / Future (macOS permission prompts)
#   python              — all parts via python-pptx (Pass OK; Model groups often break)
#   native              — PowerPoint merges everything (can timeout)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GALLERY="${GALLERY_DIR:-$REPO_ROOT/3-Master_Plan/re_entry/HEROs_and_PASSes}"
SLIDES="$GALLERY/slides"
RE_ENTRY="${RE_ENTRY_DIR:-$REPO_ROOT/3-Master_Plan/re_entry}"
PYTHON="${PYTHON:-python}"

# --- Knob defaults (env overrides) ---
export GALLERY_PRESET="${GALLERY_PRESET:-539}"
export GALLERY_HERO_BINS="${GALLERY_HERO_BINS:-16}"
export GALLERY_HERO_SEED="${GALLERY_HERO_SEED:-42}"
export GALLERY_RHO_LOW="${GALLERY_RHO_LOW:-0.1}"
export GALLERY_RHO_MODERATE="${GALLERY_RHO_MODERATE:-1.0}"
export GALLERY_RHO_HIGH="${GALLERY_RHO_HIGH:-8.0}"
export GALLERY_RHO_VERY_HIGH="${GALLERY_RHO_VERY_HIGH:-32.0}"

OUT_NAME="${GALLERY_OUT_NAME:-So_Far_.pptx}"
MERGE_ONLY=0
SLIDES_ONLY=0
SKIP_PASS_A=0
MERGE_MODE="${GALLERY_MERGE_MODE:-passes-only}"  # passes-only (default) | hybrid | python | native

usage() {
  sed -n '2,24p' "$0" | sed 's/^# \?//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --merge-only) MERGE_ONLY=1 ;;
    --slides-only) SLIDES_ONLY=1 ;;
    --skip-pass-a) SKIP_PASS_A=1 ;;
    --merge-python) MERGE_MODE=python ;;
    --merge-native) MERGE_MODE=native ;;
    --merge-hybrid) MERGE_MODE=hybrid ;;
    --merge-passes-only) MERGE_MODE=passes-only ;;
    *) echo "Unknown option: $1" >&2; usage 1 ;;
  esac
  shift
done

cd "$REPO_ROOT"

if ! "$PYTHON" -c "import pptx" 2>/dev/null; then
  echo "ERROR: python-pptx not found for $PYTHON" >&2
  echo "Install:  pip install python-pptx" >&2
  exit 1
fi

echo "=== Gallery rebuild ==="
echo "  preset=$GALLERY_PRESET  bins=$GALLERY_HERO_BINS  seed=$GALLERY_HERO_SEED"
echo "  gallery=$GALLERY"
echo "  slides=$SLIDES"
echo "  out=$SLIDES/$OUT_NAME"
echo ""

if [[ "$MERGE_ONLY" -eq 0 ]]; then
  if [[ "$SKIP_PASS_A" -eq 0 ]]; then
    echo ">> Pass A (empirical PNGs)..."
    "$PYTHON" sports/scripts/pass_a_empirical_bundle.py
  else
    echo ">> Skip Pass A (--skip-pass-a)"
  fi

  echo ">> Pass B (lambda knockout PNGs)..."
  "$PYTHON" sports/scripts/pass_b_generative_knockout_bundle.py

  echo ">> Pass C (rho ablation PNG)..."
  "$PYTHON" sports/scripts/pass_c_rho_ablation_bundle.py

  echo ">> Build PASS_ABC_Gallery_Slides.pptx..."
  "$PYTHON" sports/scripts/build_pass_abc_slides.py
fi

if [[ "$SLIDES_ONLY" -eq 1 ]]; then
  echo "Done (--slides-only; merge skipped)."
  exit 0
fi

PASS_ABC="$SLIDES/PASS_ABC_Gallery_Slides.pptx"
MODEL="${MODEL_PPTX:-$RE_ENTRY/Model.pptx}"
FUTURE="${FUTURE_PPTX:-$RE_ENTRY/Future_Work_Slides.pptx}"
OUT="$SLIDES/$OUT_NAME"

if [[ ! -f "$PASS_ABC" ]]; then
  echo "ERROR: missing $PASS_ABC — run without --merge-only first." >&2
  exit 1
fi

if [[ ! -f "$MODEL" ]]; then
  echo "WARN: $MODEL not found." >&2
  echo "      Expected: 3-Master_Plan/re_entry/Model.pptx" >&2
fi

echo ">> Merge deck parts (mode=$MERGE_MODE)..."
NATIVE_MERGE="$REPO_ROOT/scripts/merge_pptx_native.applescript"

if [[ "$MERGE_MODE" == "passes-only" ]]; then
  if [[ -f "$OUT" ]]; then
    echo "  update Pass A/B/C in $OUT (slides 1–3); slide 4+ left unchanged"
    "$PYTHON" sports/scripts/merge_pptx.py --update-passes "$OUT" "$PASS_ABC"
  else
    echo "  first run: copying PASS_ABC → $OUT"
    cp "$PASS_ABC" "$OUT"
    echo ""
    echo "  So_Far_.pptx has 3 Pass slides only."
    echo "  One-time manual step: open it → Insert → Reuse Slides → Model.pptx → save."
    echo "  After that, re-runs will refresh slides 1–3 only."
  fi
elif [[ "$MERGE_MODE" == "hybrid" ]]; then
  # Intermediate decks live in /tmp, not Dropbox — hidden dotfiles under CloudStorage
  # trigger macOS "Grant File Access" when PowerPoint opens them via AppleScript.
  MERGE_TMPDIR="$(mktemp -d /tmp/hero_gallery_merge.XXXXXX)"
  cleanup_merge_tmp() { rm -rf "$MERGE_TMPDIR"; }
  trap cleanup_merge_tmp EXIT

  WORK="$MERGE_TMPDIR/pass_abc_merged.pptx"

  echo "  python: PASS_ABC_Gallery_Slides.pptx"
  "$PYTHON" sports/scripts/merge_pptx.py --python "$WORK" "$PASS_ABC"

  echo ""
  echo "  PowerPoint will open next to append Model (and Future, if present)."
  echo "  If macOS shows Grant File Access for Model.pptx, click Select and choose that file once."
  echo "  Leave PowerPoint in the foreground until the terminal prints Done."
  echo ""

  for extra in "$MODEL" "$FUTURE"; do
    if [[ -f "$extra" ]]; then
      NEXT="$MERGE_TMPDIR/merged_$(basename "$extra" .pptx).pptx"
      echo "  native append: $(basename "$extra")"
      if ! osascript "$NATIVE_MERGE" "$NEXT" "$WORK" "$extra"; then
        echo "" >&2
        echo "ERROR: PowerPoint append failed for $(basename "$extra")." >&2
        echo "  Partial deck (Pass slides only): $WORK" >&2
        echo "  Manual fix: open PASS_ABC_Gallery_Slides.pptx → Insert → Reuse Slides → Model.pptx → save as So_Far_.pptx" >&2
        exit 1
      fi
      WORK="$NEXT"
    fi
  done

  mv "$WORK" "$OUT"
  echo "Wrote $OUT (hybrid merge)"
else
  MERGE_ARGS=()
  if [[ "$MERGE_MODE" == "python" ]]; then
    MERGE_ARGS=(--python)
  else
    MERGE_ARGS=(--native)
  fi
  "$PYTHON" sports/scripts/merge_pptx.py "${MERGE_ARGS[@]}" --skip-missing "$OUT" \
    "$PASS_ABC" \
    "$MODEL" \
    "$FUTURE"
fi

echo ""
echo "Done. Open: $OUT"
