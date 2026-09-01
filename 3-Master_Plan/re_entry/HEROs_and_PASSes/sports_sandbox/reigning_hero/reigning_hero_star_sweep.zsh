#!/usr/bin/env zsh
# Reigning hero star sweep — 5 EW bin counts × 4 season windows (20 runs).
# Usage (repo root):
#   zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/reigning_hero_star_sweep.zsh
#   zsh .../reigning_hero_star_sweep.zsh --dry-run

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$ROOT"
python sports/scripts/reigning_hero_star_sweep.py "$@"
