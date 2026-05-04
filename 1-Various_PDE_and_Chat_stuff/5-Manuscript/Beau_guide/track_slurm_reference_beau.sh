#!/usr/bin/env bash
# Reference copy — Charles Ivy_Net scripts/track_slurm.sh logic, adapted for Beau_guide location:
# repo root = directory containing .git (walk upward from this script), not "parent of Beau_guide".
#
# Usage: ./track_slurm_reference_beau.sh [JOBID]
# Example from unpacked Beau_guide/:   ./track_slurm_reference_beau.sh 11766185

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
while [[ "$REPO_ROOT" != "/" && ! -e "$REPO_ROOT/.git" ]]; do
  REPO_ROOT="$(dirname "$REPO_ROOT")"
done
if [[ ! -e "$REPO_ROOT/.git" ]]; then
  echo "No .git found walking up from ${SCRIPT_DIR}"
  exit 1
fi

_pick_latest_err() {
  local a b
  a=$(ls -t "${REPO_ROOT}"/slurm-*.err 2>/dev/null | head -1)
  b=$(ls -t "${SCRIPT_DIR}"/slurm-*.err 2>/dev/null | head -1)
  if [[ -z "$a" ]]; then printf '%s\n' "$b"; return; fi
  if [[ -z "$b" ]]; then printf '%s\n' "$a"; return; fi
  if [[ "$a" -nt "$b" ]]; then printf '%s\n' "$a"; else printf '%s\n' "$b"; fi
}

if [[ $# -lt 1 ]]; then
    LATEST_ERR="$(_pick_latest_err)"
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in ${REPO_ROOT} or ${SCRIPT_DIR}"
        echo "Usage: $(basename "$0") [JOBID]"
        exit 1
    fi
    JOBID=$(basename "$LATEST_ERR" | grep -oE '[0-9]+' | tail -1)
    echo "No job ID given — using most recent: $JOBID ($(basename "$LATEST_ERR"))"
    echo ""
else
    JOBID="$1"
fi

ERR_FILE=""
for d in "${REPO_ROOT}" "${SCRIPT_DIR}"; do
  f=$(ls "$d"/slurm-*"${JOBID}"*.err 2>/dev/null | head -1)
  [[ -n "$f" ]] && { ERR_FILE="$f"; break; }
done

if [[ -z "$ERR_FILE" ]]; then
    echo "No .err file found for job ID $JOBID in ${REPO_ROOT} or ${SCRIPT_DIR}"
    squeue -j "$JOBID" 2>/dev/null || echo "  (job not found in queue)"
    exit 1
fi

echo "Job $JOBID — queue status:"
squeue -j "$JOBID" 2>/dev/null || echo "  (job not in queue — may have finished)"
echo ""
echo "Tailing: $ERR_FILE"
echo "─────────────────────────────────────────"
echo "(Ctrl+C to stop)"
echo ""

tail -f "$ERR_FILE"
