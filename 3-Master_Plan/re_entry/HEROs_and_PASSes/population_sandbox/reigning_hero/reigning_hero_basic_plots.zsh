#!/usr/bin/env zsh
# Reigning hero (slide 12) — porch basic data plots.
# Usage (repo root):
#   zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_basic_plots.zsh
#   zsh .../reigning_hero_basic_plots.zsh --only overlap ai_tj

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$ROOT"
python sports/scripts/reigning_hero_basic_plots.py "$@"
