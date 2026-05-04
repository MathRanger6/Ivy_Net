#!/usr/bin/env bash
# Wrapper — run from the Ivy_Net repo root:
#   ./apply_url_updates.sh              # apply new_url entries from worksheet + rebuild
#   ./apply_url_updates.sh --build-only # just rebuild the worksheet (no URL edits)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/tenure/tenure_pipeline/apply_url_updates.py" "$@"
