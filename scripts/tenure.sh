#!/usr/bin/env bash
# Optional shortcut: same as typing `tenure` in zsh after conda is available.
# Must be sourced (not executed in a subshell):
#   source tenure.sh   (if scripts/ is on PATH) or: source scripts/tenure.sh
#
# Canonical definition: ~/.tenure_env.zsh (loaded by ~/.zshrc on every new terminal).

source "/opt/anaconda3/etc/profile.d/conda.sh"
source "$HOME/.tenure_env.zsh"
tenure
