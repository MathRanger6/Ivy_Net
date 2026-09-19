#!/usr/bin/env bash
# Army BDP + HERO + 3×3 mosaic — run from AWS 520 root (e.g. Network_1P_shell).
# No PYTHONPATH needed. Feather: ./big_dfs/df_pipeline_11_cox_analysis.feather
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -f "./sports/scripts/build_data_story_mosaic.py" ]]; then
  REPO="$(pwd)"
elif [[ -f "$SCRIPT_DIR/../../sports/scripts/build_data_story_mosaic.py" ]]; then
  REPO="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  echo "ERROR: Run from 520 root (folder with sports/ and talent/re_entry/)." >&2
  exit 1
fi
cd "$REPO"

echo "== Army BDP pipeline =="
echo "Repo: $REPO"
echo ""

INPUT_ARGS=()
if [[ "${1:-}" == "--input" && -n "${2:-}" ]]; then
  INPUT_ARGS=(--input "$2")
fi

python "$SCRIPT_DIR/army_basic_plots.py" --all "${INPUT_ARGS[@]}"
python "$SCRIPT_DIR/army_act2_probes.py" --plot all_probes "${INPUT_ARGS[@]}"
python "$SCRIPT_DIR/army_hero_slide_plot.py" "${INPUT_ARGS[@]}"
python "$SCRIPT_DIR/build_army_data_story.py"

echo ""
echo "Done. Mosaic: talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png"
