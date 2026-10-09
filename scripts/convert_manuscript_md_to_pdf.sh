#!/usr/bin/env bash
# Repo-root entry point for manuscript PDFs. Explicit relative input/output paths
# remain relative to your terminal; no arguments prints the current Chapter 4.
set -euo pipefail
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"
CONVERTER="$REPO_DIR/3-Master_Plan/VECTOR_work/new_VECTOR_work/convert_manuscript_md_to_pdf.sh"
if [[ ! -f "$CONVERTER" ]]; then
    printf 'Manuscript converter not found: %s\n' "$CONVERTER" >&2
    exit 1
fi
exec bash "$CONVERTER" "$@"
