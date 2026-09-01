#!/usr/bin/env zsh
# Reigning hero paired F-HERO (same population as porch BDPs + HERO lock).
# Usage (repo root):
#   zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_fhero.zsh
#   zsh .../reigning_hero_fhero.zsh --with-dft-overlay

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$ROOT"
python sports/scripts/reigning_hero_fhero.py "$@"
