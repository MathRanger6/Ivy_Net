#!/usr/bin/env bash
# =============================================================================
# track_slurm_beau.sh — Tail stderr for your notebook Slurm job (Rivanna)
# Maintainer: Charles — starter script for Beau.
# Lives in: Ivy_Net/5-Manuscript/Beau_guide/
# =============================================================================
#
# OVERVIEW
# --------
# Charles's batch script asks Slurm to write TWO plain-text logs next to sbatch dir:
#   *.out = stdout (normal prints)
#   *.err = stderr (progress bars like tqdm + warnings — lots goes here even when OK)
#
# Jupyter/papermill often send progress to STDERR, so watching *.err feels more “live.”
#
# What “tail” means
# -----------------
# `tail FILE` shows the last lines of FILE once.
# `tail -f FILE` (“follow”) keeps printing NEW lines as Slurm appends them — like a live feed.
# Ctrl+C stops tail only — it does NOT cancel your Slurm job (use `scancel JOBID`).
#
# Why chmod +x and ./5-Manuscript/Beau_guide/...
# ---------------------------------------------
# Scripts must be executable once:
#   chmod +x 5-Manuscript/Beau_guide/track_slurm_beau.sh
# “chmod +x” = permission to run this file as a program.
# Run from Ivy_Net repo root:
#   ./5-Manuscript/Beau_guide/track_slurm_beau.sh [JOBID]
#
# REPO ROOT DETECTION
# -------------------
# This script walks upward from its own folder until it finds functionsG_working.py
# (Ivy_Net root). It looks for slurm-*.err there AND in Beau_guide — so logs still work
# if you accidentally submitted sbatch from inside Beau_guide (logs land there instead).
#
# STEP-BY-STEP
# ------------
#  1. After `sbatch …/pipe_job_beau.slurm`, note JOBID (integer Slurm prints).
#  2. cd /YOUR/PATH/TO/Ivy_Net    ← Typically repo root (same place you ran sbatch).
#  3. chmod +x 5-Manuscript/Beau_guide/track_slurm_beau.sh   # once per clone if needed
#  4a. ./5-Manuscript/Beau_guide/track_slurm_beau.sh          # newest slurm-*.err found
#  4b. ./5-Manuscript/Beau_guide/track_slurm_beau.sh 11807601 # explicit JOBID
#
# OPTIONAL — stdout instead (progress may be quieter here):
#     tail -f slurm-pipe_job_beau-<JOBID>.out
#
# INSERT PATH HERE — Override Ivy_Net root ONLY if automatic detection fails:
# IVY_NET_ROOT="/your/full/path/to/Ivy_Net"
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_find_ivy_net_root_from() {
  local d="$SCRIPT_DIR"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/functionsG_working.py" ]]; then
      printf '%s\n' "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

if [[ -z "${IVY_NET_ROOT:-}" ]]; then
  IVY_NET_ROOT="$(_find_ivy_net_root_from)" || {
    echo "Cannot find Ivy_Net repo root (expected functionsG_working.py walking up from ${SCRIPT_DIR})."
    exit 1
  }
fi

_pick_latest_slurm_err() {
  local a b
  a=$(ls -t "${IVY_NET_ROOT}"/slurm-*.err 2>/dev/null | head -1)
  b=$(ls -t "${SCRIPT_DIR}"/slurm-*.err 2>/dev/null | head -1)
  if [[ -z "$a" ]]; then printf '%s\n' "$b"; return; fi
  if [[ -z "$b" ]]; then printf '%s\n' "$a"; return; fi
  if [[ "$a" -nt "$b" ]]; then printf '%s\n' "$a"; else printf '%s\n' "$b"; fi
}

_find_err_for_job() {
  local jid="$1" f
  for d in "${IVY_NET_ROOT}" "${SCRIPT_DIR}"; do
    f=$(ls "${d}"/slurm-*"${jid}"*.err 2>/dev/null | head -1)
    [[ -n "$f" ]] && { printf '%s\n' "$f"; return 0; }
  done
  return 1
}

if [[ $# -lt 1 ]]; then
    LATEST_ERR="$(_pick_latest_slurm_err)"
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in ${IVY_NET_ROOT} or ${SCRIPT_DIR}"
        echo "Usage: $(basename "$0") [JOBID]"
        exit 1
    fi
    JOBID=$(basename "$LATEST_ERR" | grep -oE '[0-9]+' | tail -1)
    echo "No job ID given — using most recent: $JOBID ($(basename "$LATEST_ERR"))"
    echo ""
else
    JOBID="$1"
fi

ERR_FILE="$(_find_err_for_job "$JOBID")"

if [[ -z "$ERR_FILE" ]]; then
    echo "No .err file found for job ID $JOBID in ${IVY_NET_ROOT} or ${SCRIPT_DIR}"
    echo "Job may still be queued, or file hasn't been created yet."
    echo "Queue status:"
    squeue -j "$JOBID" 2>/dev/null || echo "  (job not found in queue)"
    exit 1
fi

echo "Job $JOBID — queue status:"
squeue -j "$JOBID" 2>/dev/null || echo "  (job not in queue — may have finished)"
echo ""
echo "Streaming new lines from (stderr log — tqdm/warnings often appear here):"
echo "$ERR_FILE"
echo "─────────────────────────────────────────"
echo "(Ctrl+C stops tail — does NOT cancel the Slurm job)"
echo ""

tail -f "$ERR_FILE"
