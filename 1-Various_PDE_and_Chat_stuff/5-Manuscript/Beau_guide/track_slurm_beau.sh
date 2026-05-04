#!/usr/bin/env bash
# =============================================================================
# track_slurm_beau.sh — tail -f a Slurm job's stderr log (Rivanna)
#
# Ships inside Beau_guide/ (zip unpack root). Typical use after sbatch from Beau_guide/:
#   cd ~/Beau_guide && ./track_slurm_beau.sh [JOBID]
#
# Slurm writes slurm-<jobname>-<jobid>.err in the directory where you ran sbatch.
# Run this script from THAT SAME DIRECTORY (default), or set PROJECT_ROOT there.
#
# Usage:
#   cd ~/Beau_guide           # or wherever you ran sbatch
#   chmod +x ./track_slurm_beau.sh    # once
#   ./track_slurm_beau.sh [JOBID]
#
# Omit JOBID to follow the newest slurm-*.err in PROJECT_ROOT or this script's folder.
#
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${PROJECT_ROOT:-}" ]]; then
  SEARCH_ROOT="$(cd "${PROJECT_ROOT}" && pwd)"
else
  SEARCH_ROOT="$(pwd)"
fi

_pick_latest_slurm_err() {
  local a b
  a=$(ls -t "${SEARCH_ROOT}"/slurm-*.err 2>/dev/null | head -1)
  b=$(ls -t "${SCRIPT_DIR}"/slurm-*.err 2>/dev/null | head -1)
  if [[ -z "$a" ]]; then printf '%s\n' "$b"; return; fi
  if [[ -z "$b" ]]; then printf '%s\n' "$a"; return; fi
  if [[ "$a" -nt "$b" ]]; then printf '%s\n' "$a"; else printf '%s\n' "$b"; fi
}

_find_err_for_job() {
  local jid="$1" f
  for d in "${SEARCH_ROOT}" "${SCRIPT_DIR}"; do
    f=$(ls "${d}"/slurm-*"${jid}"*.err 2>/dev/null | head -1)
    [[ -n "$f" ]] && { printf '%s\n' "$f"; return 0; }
  done
  return 1
}

if [[ $# -lt 1 ]]; then
    LATEST_ERR="$(_pick_latest_slurm_err)"
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in ${SEARCH_ROOT} or ${SCRIPT_DIR}"
        echo "Hint: cd to the directory where you ran sbatch, then retry."
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
    echo "No .err file found for job ID $JOBID in ${SEARCH_ROOT} or ${SCRIPT_DIR}"
    echo "Try: cd /directory/where/you/ran/sbatch"
    squeue -j "$JOBID" 2>/dev/null || echo "  (job not found in queue)"
    exit 1
fi

echo "Job $JOBID — queue:"
squeue -j "$JOBID" 2>/dev/null || echo "  (job not in queue — may have finished)"
echo ""
echo "Tailing stderr (tqdm/warnings often here; Ctrl+C stops tail only — not the job):"
echo "$ERR_FILE"
echo "─────────────────────────────────────────"
tail -f "$ERR_FILE"
