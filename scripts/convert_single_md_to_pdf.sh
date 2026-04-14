#!/bin/bash
# Convert a single .md file to PDF using generate_pdf_playwright.sh
# PDFs are created alongside the source .md unless an output path is provided
# Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html]

# Parse optional flags and positional args
KEEP_HTML=false
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html]"
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

INPUT_FILE="${POSITIONAL[0]}"
OUTPUT_FILE="${POSITIONAL[1]}"
CSS_FILE_ARG="${POSITIONAL[2]}"

if [ -z "$INPUT_FILE" ]; then
    echo "❌ Error: input .md file is required"
    echo "Usage: ./convert_single_md_to_pdf.sh <input.md> [output.pdf] [styles.css] [--keep-html]"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: input file not found: $INPUT_FILE"
    exit 1
fi

# Repository root (parent of scripts/) and this script's directory
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"

# Path to the generate_pdf_playwright.sh script
GENERATE_PDF_SCRIPT="$SCRIPTS_DIR/generate_pdf_playwright.sh"

# Check if generate_pdf_playwright.sh exists
if [ ! -f "$GENERATE_PDF_SCRIPT" ]; then
    echo "❌ Error: generate_pdf_playwright.sh not found at: $GENERATE_PDF_SCRIPT"
    exit 1
fi

# Make sure generate_pdf_playwright.sh is executable
chmod +x "$GENERATE_PDF_SCRIPT"

# Resolve CSS file (optional)
CSS_FILE=""
if [ -n "$CSS_FILE_ARG" ]; then
    CSS_FILE="$CSS_FILE_ARG"
else
    # Default to workspace pdf_styles.css if present
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
