#!/usr/bin/env bash
# Probe one faculty URL (Wayback + parse). From repo root:
#   ./probe_faculty_url.sh --url 'https://…'
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=tenure/lib/tenure_python.sh
source "$ROOT/tenure/lib/tenure_python.sh"
exec "$(tenure_python)" "$ROOT/tenure/tenure_pipeline/probe_faculty_url.py" "$@"
