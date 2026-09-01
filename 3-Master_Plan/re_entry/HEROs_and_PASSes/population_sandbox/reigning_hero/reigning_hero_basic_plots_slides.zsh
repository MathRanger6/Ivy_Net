#!/usr/bin/env zsh
# Build reigning hero BDP porch PowerPoint from basic_data_plots/.
# Usage (repo root):
#   zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_basic_plots_slides.zsh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$ROOT"
python sports/scripts/build_reigning_hero_basic_plots_slides.py "$@"
