#!/usr/bin/env bash
# Dump --help for HERO / F-HERO CLI scripts → population_sandbox/cli_help_dump.txt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/cli_help_dump.txt"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/mpl}"
cd "$ROOT"
{
  echo "HERO / F-HERO CLI help dump — $(date '+%Y-%m-%d %H:%M')"
  echo "Repo: $ROOT"
  echo
  for s in \
    sports/scripts/pass_a_empirical_bundle.py \
    sports/scripts/pass_a_congestion_conditional.py \
    sports/scripts/pass_a_hero_sensitivity_plots.py; do
    echo "================================================================================"
    echo "$s"
    echo "================================================================================"
    python "$s" --help 2>/dev/null || python "$s" --help
    echo
  done
  echo "================================================================================"
  echo "sports/scripts/compare_hero_mg_sandbox.py (no argparse — see docstring)"
  echo "================================================================================"
  head -n 8 sports/scripts/compare_hero_mg_sandbox.py
  echo
} > "$OUT"
echo "Wrote $OUT"
