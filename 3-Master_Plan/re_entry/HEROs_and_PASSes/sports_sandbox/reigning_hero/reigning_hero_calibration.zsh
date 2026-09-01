#!/bin/zsh
# Reigning hero — PD28 calibration (ρ, MLE, temperature)
set -euo pipefail
cd "$(dirname "$0")/../../../../.."
python sports/scripts/reigning_hero_calibration.py "$@"
