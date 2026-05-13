#!/usr/bin/env bash
# Pull recent HPC outputs for local Cursor / debugging: Slurm logs, sweep results, and/or tenure data.
# Companion doc: scripts/DATA_SYNC.md
#
# Run on your Mac (not on Rivanna). Uses the same host/repo defaults as rsync_pull_from_hpc.sh.
#
# Usage:
#   ./scripts/rsync_pull_recent_hpc.sh           # default: all
#   ./scripts/rsync_pull_recent_hpc.sh all       # slurm_out + sweep + tenure/tenure_pipeline
#   ./scripts/rsync_pull_recent_hpc.sh quick     # slurm_out + sweep only (lighter, good after sim_job / 537)
#   ./scripts/rsync_pull_recent_hpc.sh logs      # slurm_out only
#   ./scripts/rsync_pull_recent_hpc.sh sweep     # faithful 537 sweep artifacts only
#   ./scripts/rsync_pull_recent_hpc.sh tenure    # tenure/tenure_pipeline only
#   ./scripts/rsync_pull_recent_hpc.sh --help
#
# Dry run (no writes):  DRY_RUN=1 ./scripts/rsync_pull_recent_hpc.sh quick
#
# Overrides: HPC_USER, HPC_HOST, HPC_REPO, DRY_RUN=1

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_usage() {
  sed -n '2,19p' "$0" | sed 's/^# \?//'
}

_pull_all() {
  ivy_rsync_pull slurm_out
  ivy_rsync_pull_sweep
  ivy_rsync_pull tenure/tenure_pipeline
}

_pull_quick() {
  ivy_rsync_pull slurm_out
  ivy_rsync_pull_sweep
}

main() {
  local mode="${1:-all}"
  case "${mode}" in
    -h|--help|help)
      _usage
      exit 0
      ;;
    all)
      _pull_all
      ;;
    quick)
      _pull_quick
      ;;
    logs)
      ivy_rsync_pull slurm_out
      ;;
    sweep)
      ivy_rsync_pull_sweep
      ;;
    tenure)
      ivy_rsync_pull tenure/tenure_pipeline
      ;;
    *)
      echo "Unknown mode: ${mode}" >&2
      echo "Try:  ./scripts/rsync_pull_recent_hpc.sh --help" >&2
      exit 1
      ;;
  esac
}

main "$@"
