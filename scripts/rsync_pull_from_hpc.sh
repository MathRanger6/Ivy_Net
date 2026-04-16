#!/usr/bin/env bash
# Pull a repo subtree: UVA HPC → local clone (run on your Mac).
#
# Usage:
#   ./scripts/rsync_pull_from_hpc.sh
#   ./scripts/rsync_pull_from_hpc.sh tenure/tenure_pipeline
#   ./scripts/rsync_pull_from_hpc.sh python_packages/dblp-parser
#   ./scripts/rsync_pull_from_hpc.sh all
# Dry run: DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh
#
# Overrides: HPC_USER, HPC_HOST, HPC_REPO

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_run() {
  local target="${1:?}"
  ivy_rsync_pull "${target}"
}

if [[ "${1:-}" == "all" ]]; then
  for rel in "${IVY_RSYNC_DEFAULT_TARGETS[@]}"; do
    _run "${rel}"
  done
else
  _run "${1:-tenure/tenure_pipeline}"
fi
