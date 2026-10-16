#!/usr/bin/env bash
# Daily Wayback wave (tenure_net Python). From repo root:
#   ./tenure/run_wayback_wave.sh --slugs university_of_minnesota --steps apply,cell2,cdx,download,parse
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=lib/tenure_python.sh
source "$ROOT/tenure/lib/tenure_python.sh"
exec "$(tenure_python)" "$ROOT/tenure/run_wayback_wave.py" "$@"
