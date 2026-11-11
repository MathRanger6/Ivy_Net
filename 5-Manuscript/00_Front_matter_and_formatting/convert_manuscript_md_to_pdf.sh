#!/usr/bin/env bash
# Manuscript printing through the repository's existing Pandoc/Playwright engine.
# No arguments: print the current Chapter 4 Markdown beside this script.
# Explicit input: ./convert_manuscript_md_to_pdf.sh "chapter.md" ["output.pdf"]
# Add --keep-html to retain the intermediate browser document for inspection.
# Appearance settings live in pdf_styles_manuscript.css beside this script.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEEP_HTML=false
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-html) KEEP_HTML=true; shift ;;
        -h|--help)
            cat <<'HELP'
Usage: convert_manuscript_md_to_pdf.sh [input.md] [output.pdf] [--keep-html]

No arguments prints Model_Chapter_Shared_Working_Draft.md beside this script.
Default output is <input-name>_manuscript.pdf beside the input.
Explicit relative paths are resolved from your terminal's current directory.

Style: Letter paper, 1-inch margins, 12-point serif text, 1.5-line spacing,
black headings and links, centered page numbers, and intact math blocks.
Edit pdf_styles_manuscript.css beside this script to change the appearance.

Uses the existing scripts/generate_pdf_playwright.sh and its conda/browser setup.
Page numbers use CSS page-margin boxes (Chrome/Chromium 131 or later).
HELP
            exit 0 ;;
        --) shift; while [[ $# -gt 0 ]]; do POSITIONAL+=("$1"); shift; done ;;
        -*) printf 'Unknown option: %s\nUse --help for usage.\n' "$1" >&2; exit 2 ;;
        *) POSITIONAL+=("$1"); shift ;;
    esac
done
[[ ${#POSITIONAL[@]} -le 2 ]] || { echo 'Expected at most input and output paths.' >&2; exit 2; }
INPUT="${POSITIONAL[0]:-$SCRIPT_DIR/Model_Chapter_Shared_Working_Draft.md}"
[[ -f "$INPUT" && "$INPUT" == *.md ]] || { printf 'Markdown input not found: %s\n' "$INPUT" >&2; exit 1; }
INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
OUTPUT="${POSITIONAL[1]:-${INPUT%.md}_manuscript.pdf}"
[[ "$OUTPUT" == *.pdf ]] || { echo 'Output filename must end in .pdf.' >&2; exit 2; }
[[ -d "$(dirname "$OUTPUT")" ]] || { echo 'Output directory does not exist.' >&2; exit 1; }
OUTPUT="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"
CSS="$SCRIPT_DIR/pdf_styles_manuscript.css"
[[ -f "$CSS" ]] || { printf 'Stylesheet missing: %s\n' "$CSS" >&2; exit 1; }

# Find the established engine without hard-coding Charles's Dropbox path.
# This also works if the whole repository is checked out elsewhere.
SEARCH_DIR="$SCRIPT_DIR"
while [[ ! -f "$SEARCH_DIR/scripts/generate_pdf_playwright.sh" ]]; do
    [[ "$SEARCH_DIR" != / ]] || { echo 'Cannot find scripts/generate_pdf_playwright.sh in the parent repository.' >&2; exit 1; }
    SEARCH_DIR="$(dirname "$SEARCH_DIR")"
done
ENGINE="$SEARCH_DIR/scripts/generate_pdf_playwright.sh"

# The legacy engine interpolates paths into embedded Python. Reject characters
# that it cannot safely represent rather than allowing a confusing syntax error.
for FILE_PATH in "$INPUT" "$OUTPUT" "$CSS"; do
    case "$FILE_PATH" in
        *'"'*|*'\'*|*$'\n'*|*$'\r'*)
            echo 'The existing PDF engine cannot safely accept double quotes, backslashes, or newlines in file paths.' >&2
            exit 2 ;;
    esac
done
printf 'Manuscript input: %s\nPDF output: %s\nStylesheet: %s\n' "$INPUT" "$OUTPUT" "$CSS"
echo 'The Markdown source is read only during conversion. An existing output PDF will be replaced.'
ARGS=("$INPUT" "$OUTPUT" "$CSS")
if "$KEEP_HTML"; then ARGS+=(--keep-html); fi
bash "$ENGINE" "${ARGS[@]}"
