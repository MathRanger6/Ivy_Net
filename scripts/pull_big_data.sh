#!/usr/bin/env bash
# Sync large datasets/ trees between Mac (Dropbox) and Rivanna.
#
# *** RUN ON YOUR MAC, NOT ON RIVANNA ***
#   to-hpc    = Mac → Rivanna  (push big files up)
#   from-hpc  = Rivanna → Mac  (pull big files down)
#   unzip     = Mac only, no SSH (unzip git-tracked .zip archives)
#
# Policy: scripts/DATA_SYNC.md §4b
#
# Usage (Mac terminal):
#   ./scripts/pull_big_data.sh unzip
#   ./scripts/pull_big_data.sh to-hpc big-fish     # LoL + football panels (~250 MB)
#   ./scripts/pull_big_data.sh to-hpc education    # NELS88 + HS&B80
#   ./scripts/pull_big_data.sh to-hpc              # big-fish + education + datasets/mbb/
#   ./scripts/pull_big_data.sh from-hpc education
#   ./scripts/pull_big_data.sh --help
#
# Dry run:  DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc big-fish
#
# Overrides: HPC_USER, HPC_HOST, HPC_REPO, DRY_RUN=1

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_usage() {
  sed -n '2,22p' "$0" | sed 's/^# \?//'
}

_pull_from_hpc() {
  ivy_rsync_pull_big_data "${1:-all}"
}

_push_to_hpc() {
  ivy_rsync_push_big_data_scoped "${1:-all}"
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
