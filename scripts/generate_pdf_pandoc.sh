#!/bin/bash
# PDF from Markdown or .ipynb via pandoc (no browser). Works on Rivanna if a PDF engine is on PATH.
# Engines tried (first wins): IVY_NET_PDF_ENGINE, then xelatex, pdflatex, lualatex, wkhtmltopdf.
#
# Usage: ./generate_pdf_pandoc.sh [input.md|input.ipynb] [output.pdf] [--keep-md]
#
# Rivanna: TeX Live module (exact name from  module spider texlive ):
#   module avail 2>&1 | grep -i texlive
#   module load texlive/2025
# Long .md → PDF: xelatex/pdflatex may run **several minutes** with almost no output — let it finish.
#
set -euo pipefail

_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_WORKSPACE_ROOT="$(cd "$_SCRIPTS_DIR/.." && pwd)"
cd "$_WORKSPACE_ROOT" || exit 1

KEEP_MD=false
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-md)
            KEEP_MD=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./generate_pdf_pandoc.sh [input.md|input.ipynb] [output.pdf] [--keep-md]"
            echo "   IVY_NET_PDF_ENGINE=xelatex|pdflatex|lualatex|wkhtmltopdf  — force first try"
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

INPUT_FILE="${POSITIONAL[0]:-}"

if [[ -z "$INPUT_FILE" || ! -f "$INPUT_FILE" ]]; then
    echo "❌ Error: input .md or .ipynb required and must exist"
    echo "Usage: ./generate_pdf_pandoc.sh <input> [output.pdf] [--keep-md]"
    exit 1
fi

if [[ "$INPUT_FILE" == *.ipynb ]]; then
    PDF_FILE="${POSITIONAL[1]:-${INPUT_FILE%.ipynb}.pdf}"
    TEMP_MD_FILE="${INPUT_FILE%.ipynb}_temp.md"
    MD_FILE="$TEMP_MD_FILE"
    IS_NOTEBOOK=true
    pandoc "$INPUT_FILE" -o "$MD_FILE" --wrap=none || {
        echo "❌ pandoc failed converting notebook to markdown"
        exit 1
    }
elif [[ "$INPUT_FILE" == *.md ]]; then
    PDF_FILE="${POSITIONAL[1]:-${INPUT_FILE%.md}.pdf}"
    MD_FILE="$INPUT_FILE"
    IS_NOTEBOOK=false
else
    echo "Error: input must be .md or .ipynb"
    exit 1
fi

# Resolve PDF path for messages (relative to repo root after cd above)
_PDF_ABS="$(cd "$(dirname "$PDF_FILE")" 2>/dev/null && pwd)/$(basename "$PDF_FILE")" 2>/dev/null || _PDF_ABS="$PDF_FILE"
echo "▶ generate_pdf_pandoc: $INPUT_FILE → $PDF_FILE"
echo "   (absolute: $_PDF_ABS)"

PANDOC_FORMAT="markdown+tex_math_single_backslash+tex_math_dollars-yaml_metadata_block"

command -v pandoc >/dev/null || {
    echo "❌ pandoc not on PATH (Rivanna:  module avail 2>&1 | grep -i pandoc )"
    exit 1
}

ENGINES=()
add_engine() {
    local e="$1"
    # Always return 0 on skip: with set -e, a non-zero return from this function
    # would abort the caller (e.g. xelatex not on PATH before module load texlive).
    [[ -z "$e" ]] && return 0
    command -v "$e" >/dev/null 2>&1 || return 0
    local x
    for x in "${ENGINES[@]}"; do
        [[ "$x" == "$e" ]] && return 0
    done
    ENGINES+=("$e")
    return 0
}

if [[ -n "${IVY_NET_PDF_ENGINE:-}" ]]; then
    add_engine "${IVY_NET_PDF_ENGINE}"
fi
for e in xelatex pdflatex lualatex wkhtmltopdf; do
    add_engine "$e"
done

_eng_list="${ENGINES[*]}"
echo "   PDF engines to try (${#ENGINES[@]}): ${_eng_list:-none}"

if [[ ${#ENGINES[@]} -eq 0 ]]; then
    echo "❌ No PDF engine on PATH (need one of: xelatex pdflatex lualatex wkhtmltopdf)."
    echo ""
    echo "   Rivanna: discover modules, then load before re-running:"
    echo "     module avail 2>&1 | grep -iE 'texlive|latex|wkhtml'"
    echo "     module spider texlive"
    echo "     module load texlive/2025"
    echo ""
    echo "   Or set a specific binary:  export IVY_NET_PDF_ENGINE=wkhtmltopdf"
    echo "   Docs: https://www.rc.virginia.edu/userinfo/rivanna/software/"
    exit 1
fi

run_with_engine() {
    local eng="$1"
    # Do not rely on set -e inside this function: a failed pandoc would abort the whole script
    # before the caller can try the next engine.
    if [[ "$eng" == wkhtmltopdf ]]; then
        # HTML intermediate path; math may be crude vs LaTeX.
        pandoc "$MD_FILE" \
            -f "$PANDOC_FORMAT" \
            -o "$PDF_FILE" \
            --pdf-engine=wkhtmltopdf \
            --syntax-highlighting=pygments || return 1
    else
        pandoc "$MD_FILE" \
            -f "$PANDOC_FORMAT" \
            -o "$PDF_FILE" \
            --pdf-engine="$eng" \
            -V geometry:margin=1in \
            -V colorlinks=true \
            --syntax-highlighting=tango || return 1
    fi
}

OK=0
echo "ℹ️  TeX PDF: first run can take several minutes on long markdown (normal). Avoid Ctrl+C unless it hangs 10+ min."
for eng in "${ENGINES[@]}"; do
    echo "==> Trying pandoc --pdf-engine=$eng → $PDF_FILE"
    if run_with_engine "$eng"; then
        echo "✅ PDF created: $PDF_FILE (engine: $eng)"
        if [[ -f "$PDF_FILE" ]]; then
            echo "   $(ls -l "$PDF_FILE")"
        fi
        OK=1
        break
    fi
    echo "⚠️  Engine $eng failed, trying next…"
done

if [[ "$OK" -ne 1 ]]; then
    echo "❌ All PDF engines failed: ${ENGINES[*]}"
    exit 1
fi

if [[ "$IS_NOTEBOOK" == true && "$KEEP_MD" != true && -f "${TEMP_MD_FILE:-}" ]]; then
    rm -f "$TEMP_MD_FILE"
    echo "   🧹 Removed temporary markdown"
elif [[ "$IS_NOTEBOOK" == true && "$KEEP_MD" == true ]]; then
    echo "   Kept: $TEMP_MD_FILE"
fi
