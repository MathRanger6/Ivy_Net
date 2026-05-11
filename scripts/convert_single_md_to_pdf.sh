#!/bin/bash
# Convert a single .md file to PDF.
# Default: Playwright (best layout); Rivanna-friendly: --pandoc or IVY_NET_PDF_BACKEND=pandoc
# Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html]
#        ./convert_single_md_to_pdf.sh ... [--pandoc]
#
# Rivanna: Playwright’s cached Chromium often SIGTRAPs on login nodes — use --pandoc and a TeX module.

USE_PANDOC=false
KEEP_HTML=false
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --pandoc)
            USE_PANDOC=true
            shift
            ;;
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html] [--pandoc]"
            echo "   IVY_NET_PDF_BACKEND=pandoc  — same as --pandoc"
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

if [[ "${IVY_NET_PDF_BACKEND:-}" == "pandoc" ]]; then
    USE_PANDOC=true
fi

INPUT_FILE="${POSITIONAL[0]}"
OUTPUT_FILE="${POSITIONAL[1]}"
CSS_FILE_ARG="${POSITIONAL[2]}"

if [ -z "$INPUT_FILE" ]; then
    echo "❌ Error: input .md file is required"
    echo "Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html] [--pandoc]"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: input file not found: $INPUT_FILE"
    exit 1
fi

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"

if "$USE_PANDOC"; then
    PANDOC_SCRIPT="$SCRIPTS_DIR/generate_pdf_pandoc.sh"
    if [ ! -f "$PANDOC_SCRIPT" ]; then
        echo "❌ Error: generate_pdf_pandoc.sh not found at: $PANDOC_SCRIPT"
        exit 1
    fi
    chmod +x "$PANDOC_SCRIPT"
    echo "▶ Pandoc PDF: $INPUT_FILE → ${OUTPUT_FILE:-<same base>.pdf}"
    _pandoc_st=0
    if [ -n "$OUTPUT_FILE" ]; then
        "$PANDOC_SCRIPT" "$INPUT_FILE" "$OUTPUT_FILE" || _pandoc_st=$?
    else
        "$PANDOC_SCRIPT" "$INPUT_FILE" || _pandoc_st=$?
    fi
    # Do not use `if ! cmd; then st=$?` — inside that branch $? is not cmd's status (bash).
    if [ "$_pandoc_st" -ne 0 ]; then
        echo "❌ Pandoc PDF failed (exit $_pandoc_st). See messages above."
        exit "$_pandoc_st"
    fi
    if [ -n "$CSS_FILE_ARG" ]; then
        echo "ℹ️  Note: --pandoc / LaTeX PDF does not apply CSS the same way as Playwright; ignored: $CSS_FILE_ARG"
    fi
    exit 0
fi

GENERATE_PDF_SCRIPT="$SCRIPTS_DIR/generate_pdf_playwright.sh"
if [ ! -f "$GENERATE_PDF_SCRIPT" ]; then
    echo "❌ Error: generate_pdf_playwright.sh not found at: $GENERATE_PDF_SCRIPT"
    exit 1
fi
chmod +x "$GENERATE_PDF_SCRIPT"

CSS_FILE=""
if [ -n "$CSS_FILE_ARG" ]; then
    CSS_FILE="$CSS_FILE_ARG"
else
    if [ -f "$WORKSPACE_DIR/pdf_styles.css" ]; then
        CSS_FILE="$WORKSPACE_DIR/pdf_styles.css"
    fi
fi

KEEP_FLAG=""
if [ "$KEEP_HTML" = true ]; then
    KEEP_FLAG="--keep-html"
fi

if [ -n "$OUTPUT_FILE" ] && [ -n "$CSS_FILE" ]; then
    "$GENERATE_PDF_SCRIPT" "$INPUT_FILE" "$OUTPUT_FILE" "$CSS_FILE" $KEEP_FLAG
elif [ -n "$OUTPUT_FILE" ]; then
    "$GENERATE_PDF_SCRIPT" "$INPUT_FILE" "$OUTPUT_FILE" $KEEP_FLAG
elif [ -n "$CSS_FILE" ]; then
    "$GENERATE_PDF_SCRIPT" "$INPUT_FILE" "" "$CSS_FILE" $KEEP_FLAG
else
    "$GENERATE_PDF_SCRIPT" "$INPUT_FILE" $KEEP_FLAG
fi
