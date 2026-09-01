#!/usr/bin/env zsh
# Build reigning hero star-sweep PowerPoint from manifest.json.
# Usage (repo root):
#   zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_star_sweep_slides.zsh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$ROOT"
python sports/scripts/build_reigning_hero_star_sweep_slides.py "$@"
