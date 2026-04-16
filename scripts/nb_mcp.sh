#!/usr/bin/env bash
# Start cursor-notebook-mcp for Cursor MCP (Mac laptop or Rivanna over SSH).
#
# Usage:
#   ./scripts/nb_mcp.sh
#
# Optional env:
#   CONDA_ENV              default: tenure_net  (e.g. talent_net on an older Mac checkout)
#   NOTEBOOK_MCP_ALLOW_ROOT  repo root allowed by the server; default: parent of scripts/
#   NOTEBOOK_MCP_PORT      default: 8080 (match ~/.cursor/mcp.json url)
#   NOTEBOOK_MCP_BACKGROUND  default: 1  (set 0 to run in foreground for logs)
#
# Transport: use **streamable-http** (PyPI default). Cursor mcp.json URL must be:
#   http://127.0.0.1:<port>/mcp
# Legacy **sse** uses http://127.0.0.1:<port>/sse — do not mix with /mcp.
#
# On Rivanna you may need:  module load miniforge
# Ensure:  conda activate $CONDA_ENV && which cursor-notebook-mcp
#
# If the server crashes with Pydantic "default and default_factory", try:
#   pip install "pydantic>=2.7,<2.12"
# then re-run this script.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONDA_ENV="${CONDA_ENV:-tenure_net}"
ALLOW_ROOT="${NOTEBOOK_MCP_ALLOW_ROOT:-$REPO_ROOT}"
PORT="${NOTEBOOK_MCP_PORT:-8080}"
BACKGROUND="${NOTEBOOK_MCP_BACKGROUND:-1}"

_init_conda() {
  if [[ -f /opt/anaconda3/etc/profile.d/conda.sh ]]; then
    # shellcheck source=/dev/null
    source /opt/anaconda3/etc/profile.d/conda.sh
    return 0
  fi
  for _sh in "${HOME}/miniforge3/etc/profile.d/conda.sh" \
             "${HOME}/.conda/etc/profile.d/conda.sh"; do
    if [[ -f "$_sh" ]]; then
      # shellcheck source=/dev/null
      source "$_sh"
      return 0
    fi
  done
  if command -v conda >/dev/null 2>&1; then
    eval "$(conda shell.bash hook)"
    return 0
  fi
  echo "ERROR: conda not found. Install Miniforge/Anaconda or: module load miniforge" >&2
  return 1
}

_init_conda
conda activate "${CONDA_ENV}"

if ! command -v cursor-notebook-mcp >/dev/null 2>&1; then
  echo "ERROR: cursor-notebook-mcp not on PATH in env ${CONDA_ENV}. Try: pip install cursor-notebook-mcp" >&2
  exit 1
fi

echo "Starting notebook MCP:"
echo "  CONDA_ENV=${CONDA_ENV}"
echo "  allow-root=${ALLOW_ROOT}"
echo "  port=${PORT}"
echo "  Cursor mcp.json should point to something like: http://127.0.0.1:${PORT}/mcp"
echo ""

_run() {
  exec cursor-notebook-mcp \
    --transport streamable-http \
    --host 127.0.0.1 \
    --log-level DEBUG \
    --allow-root "${ALLOW_ROOT}" \
    --port "${PORT}"
}

if [[ "${BACKGROUND}" == "1" ]]; then
  _run &
  echo "cursor-notebook-mcp PID $! (background). Stop with: kill $!"
else
  _run
fi
