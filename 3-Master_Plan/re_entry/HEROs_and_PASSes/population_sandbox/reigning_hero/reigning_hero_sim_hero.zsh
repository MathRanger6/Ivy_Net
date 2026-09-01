#!/bin/zsh
# Reigning hero — empirical roster Gibbs SELECT → sim HERO vs empirical
set -euo pipefail
cd "$(dirname "$0")/../../../../.."
python sports/scripts/reigning_hero_sim_hero.py "$@"
