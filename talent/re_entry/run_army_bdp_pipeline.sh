#!/usr/bin/env bash
# Army BDP + HERO + 3×3 mosaic — run from repo root or AWS (feather in talent/talent_pipeline/running_vars/)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO"

echo "== Army BDP pipeline =="
echo "Repo: $REPO"
echo ""

INPUT_ARGS=()
if [[ "${1:-}" == "--input" && -n "${2:-}" ]]; then
  INPUT_ARGS=(--input "$2")
fi

python "$SCRIPT_DIR/army_basic_plots.py" --all "${INPUT_ARGS[@]}"
python "$SCRIPT_DIR/army_hero_slide_plot.py" "${INPUT_ARGS[@]}"
python "$SCRIPT_DIR/build_army_data_story.py"

echo ""
echo "Done. Mosaic: talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png"
