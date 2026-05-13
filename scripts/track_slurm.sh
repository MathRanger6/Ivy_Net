#!/usr/bin/env bash
# Usage: track_slurm.sh <JOBID>
# Tails the .err file for a slurm job in real time.
#
# Stdout/stderr logs live under Ivy_Net/slurm_out/ (see #SBATCH --output/--error in *.slurm).
# Still checks repo root for legacy slurm-*.err from older submissions.
#
# Example: ./scripts/track_slurm.sh 11766185

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SLURM_OUT="${REPO_ROOT}/slurm_out"

_newest_err_in_dir() {
    local d="$1"
    [[ -d "$d" ]] || return 0
    ls -t "$d"/slurm-*.err 2>/dev/null | head -1
}

_pick_latest_err() {
    local a b newest=""
    a="$(_newest_err_in_dir "$SLURM_OUT")"
    b="$(_newest_err_in_dir "$REPO_ROOT")"
    newest="$a"
    if [[ -n "$b" ]]; then
        if [[ -z "$newest" || "$b" -nt "$newest" ]]; then
            newest="$b"
        fi
    fi
    printf '%s\n' "$newest"
}

_find_err_for_job() {
    local jid="$1" f d
    for d in "$SLURM_OUT" "$REPO_ROOT"; do
        [[ -d "$d" ]] || continue
        f=$(ls "$d"/slurm-*"${jid}"*.err 2>/dev/null | head -1)
        [[ -n "$f" ]] && { printf '%s\n' "$f"; return 0; }
    done
    return 1
}

if [[ $# -lt 1 ]]; then
    LATEST_ERR="$(_pick_latest_err)"
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in ${SLURM_OUT} or ${REPO_ROOT}"
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
    echo "No .err file found for job ID $JOBID in ${SLURM_OUT} or ${REPO_ROOT}"
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
