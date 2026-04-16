#!/usr/bin/env bash
# Push a repo subtree: local clone → UVA HPC (run on your Mac).
#
# Usage:
#   ./scripts/rsync_push_to_hpc.sh
#   ./scripts/rsync_push_to_hpc.sh tenure/tenure_pipeline
#   ./scripts/rsync_push_to_hpc.sh python_packages/dblp-parser
#   ./scripts/rsync_push_to_hpc.sh all    # tenure/tenure_pipeline then dblp-parser
# Dry run: DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh
#
# Overrides: HPC_USER, HPC_HOST, HPC_REPO

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_run() {
  local target="${1:?}"
  ivy_rsync_push "${target}"
}

if [[ "${1:-}" == "all" ]]; then
  for rel in "${IVY_RSYNC_DEFAULT_TARGETS[@]}"; do
    _run "${rel}"
  done
else
  _run "${1:-tenure/tenure_pipeline}"
fi
