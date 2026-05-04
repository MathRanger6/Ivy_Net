#!/usr/bin/env bash
# =============================================================================
# track_slurm_beau.sh — tail -f your job’s stderr log (Rivanna)
# Folder: 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/
# =============================================================================
#
# Usage (from project root — the directory that contains .git):
#   chmod +x 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh
#   ./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh [JOBID]
#
# Override project root if needed:
#   export PROJECT_ROOT=/path/to/repo
#
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_find_repo_root_from() {
  local d="$SCRIPT_DIR"
  while [[ "$d" != "/" ]]; do
    if [[ -e "$d/.git" ]]; then
      printf '%s\n' "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

if [[ -z "${PROJECT_ROOT:-}" ]]; then
  PROJECT_ROOT="$(_find_repo_root_from)" || {
    echo "Cannot find repo root (no .git walking up from ${SCRIPT_DIR}). Set PROJECT_ROOT export."
    exit 1
  }
fi

_pick_latest_slurm_err() {
  local a b
  a=$(ls -t "${PROJECT_ROOT}"/slurm-*.err 2>/dev/null | head -1)
  b=$(ls -t "${SCRIPT_DIR}"/slurm-*.err 2>/dev/null | head -1)
  if [[ -z "$a" ]]; then printf '%s\n' "$b"; return; fi
  if [[ -z "$b" ]]; then printf '%s\n' "$a"; return; fi
  if [[ "$a" -nt "$b" ]]; then printf '%s\n' "$a"; else printf '%s\n' "$b"; fi
}

_find_err_for_job() {
  local jid="$1" f
  for d in "${PROJECT_ROOT}" "${SCRIPT_DIR}"; do
    f=$(ls "${d}"/slurm-*"${jid}"*.err 2>/dev/null | head -1)
    [[ -n "$f" ]] && { printf '%s\n' "$f"; return 0; }
  done
  return 1
}

if [[ $# -lt 1 ]]; then
    LATEST_ERR="$(_pick_latest_slurm_err)"
    if [[ -z "$LATEST_ERR" ]]; then
        echo "No slurm .err files found in ${PROJECT_ROOT} or ${SCRIPT_DIR}"
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
    echo "No .err file found for job ID $JOBID in ${PROJECT_ROOT} or ${SCRIPT_DIR}"
    squeue -j "$JOBID" 2>/dev/null || echo "  (job not found in queue)"
    exit 1
fi

echo "Job $JOBID — queue:"
squeue -j "$JOBID" 2>/dev/null || echo "  (job not in queue — may have finished)"
echo ""
echo "Tailing stderr (tqdm/warnings often here; Ctrl+C stops tail only):"
echo "$ERR_FILE"
echo "─────────────────────────────────────────"
tail -f "$ERR_FILE"
