#!/usr/bin/env bash
# Stage 3B download (tenure_net Python). From repo root:
#   ./tenure/run_stage3b.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=lib/tenure_python.sh
source "$ROOT/tenure/lib/tenure_python.sh"
exec "$(tenure_python)" "$ROOT/tenure/run_stage3b_cli.py" "$@"
