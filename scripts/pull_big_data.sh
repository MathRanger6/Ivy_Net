#!/usr/bin/env bash
# Pull gitignored large datasets: Big Fish panels + bulk MBB.
#
# Policy: scripts/DATA_SYNC.md § Big data
#
# Usage (run on Mac unless noted):
#   ./scripts/pull_big_data.sh                  # default: unzip Big Fish from git zips (no network)
#   ./scripts/pull_big_data.sh unzip            # same — football + legends CSVs from .zip in repo
#   ./scripts/pull_big_data.sh from-hpc         # HPC → Mac: Big Fish CSVs + datasets/mbb/
#   ./scripts/pull_big_data.sh from-hpc big-fish  # HPC → Mac: Big Fish CSVs only
#   ./scripts/pull_big_data.sh from-hpc mbb       # HPC → Mac: datasets/mbb/ only
#   ./scripts/pull_big_data.sh to-hpc             # Mac → HPC: Big Fish + MBB (Dropbox Mac = source)
#   ./scripts/pull_big_data.sh to-hpc big-fish
#   ./scripts/pull_big_data.sh to-hpc mbb
#   ./scripts/pull_big_data.sh --help
#
# Dry run (rsync modes only):  DRY_RUN=1 ./scripts/pull_big_data.sh from-hpc
#
# Overrides: HPC_USER, HPC_HOST, HPC_REPO, DRY_RUN=1

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_usage() {
  sed -n '2,20p' "$0" | sed 's/^# \?//'
}

_pull_from_hpc() {
  local scope="${1:-all}"
  case "${scope}" in
    all)
      ivy_rsync_pull_big_fish
      ivy_rsync_pull_mbb
      ;;
    big-fish|big_fish)
      ivy_rsync_pull_big_fish
      ;;
    mbb)
      ivy_rsync_pull_mbb
      ;;
    *)
      echo "Unknown from-hpc scope: ${scope}" >&2
      exit 1
      ;;
  esac
}

_push_to_hpc() {
  local scope="${1:-all}"
  case "${scope}" in
    all)
      ivy_unzip_big_fish
      ivy_rsync_push_big_fish
      ivy_rsync_push_mbb
      ;;
    big-fish|big_fish)
      ivy_unzip_big_fish
      ivy_rsync_push_big_fish
      ;;
    mbb)
      ivy_rsync_push_mbb
      ;;
    *)
      echo "Unknown to-hpc scope: ${scope}" >&2
      exit 1
      ;;
  esac
}

main() {
  local cmd="${1:-unzip}"
  local scope="${2:-all}"

  case "${cmd}" in
    -h|--help|help)
      _usage
      exit 0
      ;;
    unzip|local)
      ivy_unzip_big_fish
      ;;
    from-hpc|pull-hpc|pull)
      _pull_from_hpc "${scope}"
      ;;
    to-hpc|push-hpc|push)
      _push_to_hpc "${scope}"
      ;;
    *)
      echo "Unknown command: ${cmd}" >&2
      echo "Try:  ./scripts/pull_big_data.sh --help" >&2
      exit 1
      ;;
  esac
}

main "$@"
