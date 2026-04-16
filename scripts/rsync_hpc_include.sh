# Shared rsync settings for Ivy_Net ↔ UVA HPC (sourced by rsync_* wrappers).
#
# Callers must set:
#   IVY_NET_SCRIPTS_DIR   Absolute path to this scripts/ directory (dirname of the wrapper).
#
# Optional env overrides: HPC_USER, HPC_HOST, HPC_REPO, DRY_RUN=1

: "${IVY_NET_SCRIPTS_DIR:?IVY_NET_SCRIPTS_DIR must be set before sourcing rsync_hpc_include.sh}"

set -euo pipefail

REPO_ROOT="$(cd "${IVY_NET_SCRIPTS_DIR}/.." && pwd)"

HPC_USER="${HPC_USER:-dzk3ja}"
HPC_HOST="${HPC_HOST:-login.hpc.virginia.edu}"
HPC_REPO="${HPC_REPO:-~/Ivy_Net}"

REMOTE="${HPC_USER}@${HPC_HOST}"

# Default relative paths (under repo root) for convenience / docs.
IVY_RSYNC_DEFAULT_TARGETS=(
  "tenure/tenure_pipeline"
  "python_packages/dblp-parser"
)

_ivy_rsync_build_opts() {
  RSYNC_OPTS=(-avz --progress)
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    RSYNC_OPTS+=(-n)
    echo "==> DRY RUN (no files changed)"
  fi
}

# Usage: ivy_rsync_push <relative-path>   e.g. tenure/tenure_pipeline
ivy_rsync_push() {
  local rel="${1:?relative path required}"
  _ivy_rsync_build_opts
  local src="${REPO_ROOT}/${rel}/"
  local dst="${REMOTE}:${HPC_REPO}/${rel}/"
  echo "==> Push ${rel}"
  echo "    from: ${src}"
  echo "    to:   ${dst}"
  rsync "${RSYNC_OPTS[@]}" "${src}" "${dst}"
  echo "==> Done."
}

# Usage: ivy_rsync_pull <relative-path>
ivy_rsync_pull() {
  local rel="${1:?relative path required}"
  _ivy_rsync_build_opts
  local src="${REMOTE}:${HPC_REPO}/${rel}/"
  local dst="${REPO_ROOT}/${rel}/"
  echo "==> Pull ${rel}"
  echo "    from: ${src}"
  echo "    to:   ${dst}"
  mkdir -p "${dst}"
  rsync "${RSYNC_OPTS[@]}" "${src}" "${dst}"
  echo "==> Done."
}
