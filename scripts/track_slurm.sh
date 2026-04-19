#!/usr/bin/env bash
# Usage: track_slurm.sh <JOBID>
# Tails the .err file for a slurm job in real time.
# Example: ./scripts/track_slurm.sh 11766185

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ $# -lt 1 ]]; then
    # No job ID given — find the most recently written .err file
    LATEST_ERR=$(ls -t "$REPO_ROOT"/slurm-*.err 2>/dev/null | head -1)
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in $REPO_ROOT"
        echo "Usage: $(basename "$0") [JOBID]"
        exit 1
    fi
    # Extract the numeric job ID from the filename
    JOBID=$(basename "$LATEST_ERR" | grep -oE '[0-9]+' | tail -1)
    echo "No job ID given — using most recent: $JOBID ($(basename "$LATEST_ERR"))"
    echo ""
else
    JOBID="$1"
fi
# Find matching .err file only (job name may vary: slurm-*, slurm-pipe_job-*, etc.)
ERR_FILE=$(ls "$REPO_ROOT"/slurm-*"${JOBID}"*.err 2>/dev/null | head -1)

if [[ -z "$ERR_FILE" ]]; then
    echo "No .err file found for job ID $JOBID in $REPO_ROOT"
    echo "Job may still be queued, or file hasn't been created yet."
    echo "Queue status:"
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
