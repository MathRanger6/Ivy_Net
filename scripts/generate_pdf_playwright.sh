#!/bin/bash
# Script to generate PDF from markdown or Jupyter notebooks using pandoc and Playwright
# Playwright uses a real browser engine and has much better page break support than WeasyPrint
# Usage: ./generate_pdf_playwright.sh [input.md|input.ipynb] [output.pdf] [styles.css] [--keep-html]

set -euo pipefail

# Run relative to workspace root (so default CSS paths and inputs resolve when invoked from PATH)
_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_WORKSPACE_ROOT="$(cd "$_SCRIPTS_DIR/.." && pwd)"
cd "$_WORKSPACE_ROOT" || exit 1

# Argument parsing
KEEP_HTML=false
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./generate_pdf_playwright.sh [input.md|input.ipynb] [output.pdf] [styles.css] [--keep-html]"
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

# Set default values
INPUT_FILE="${POSITIONAL[0]:-CUMULATIVE_OER_METRICS_OVERVIEW.md}"

# Determine file type and set output PDF name and default CSS
if [[ "$INPUT_FILE" == *.ipynb ]]; then
    # Jupyter notebook input
    PDF_FILE="${POSITIONAL[1]:-${INPUT_FILE%.ipynb}.pdf}"
    TEMP_MD_FILE="${INPUT_FILE%.ipynb}_temp.md"
    MD_FILE="$TEMP_MD_FILE"
    IS_NOTEBOOK=true
    DEFAULT_CSS="pdf_styles_notebook.css"
elif [[ "$INPUT_FILE" == *.md ]]; then
    # Markdown input
    PDF_FILE="${POSITIONAL[1]:-${INPUT_FILE%.md}.pdf}"
    MD_FILE="$INPUT_FILE"
    IS_NOTEBOOK=false
    DEFAULT_CSS="pdf_styles.css"
else
    echo "Error: Input file must be .md or .ipynb"
    exit 1
fi

# Set CSS file (use provided CSS or default based on file type)
CSS_FILE="${POSITIONAL[2]:-$DEFAULT_CSS}"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found: $INPUT_FILE"
    exit 1
fi

# Check if CSS file exists
if [ ! -f "$CSS_FILE" ]; then
    echo "Warning: CSS file not found: $CSS_FILE (using default styling)"
    CSS_FILE=""
fi

# Activate conda environment and run conversion (HPC Miniforge + Mac Anaconda)
# Override env name:   IVY_NET_PDF_ENV=talent_net ./generate_pdf_playwright.sh ...
# Default: tenure_net if present, else talent_net (legacy Mac).
init_conda_shell() {
    if [[ -f /opt/anaconda3/etc/profile.d/conda.sh ]]; then
        # shellcheck source=/dev/null
        source /opt/anaconda3/etc/profile.d/conda.sh
        return 0
    fi
    for _conda_sh in "${HOME}/miniforge3/etc/profile.d/conda.sh" \
                     "${HOME}/.conda/etc/profile.d/conda.sh"; do
        if [[ -f "$_conda_sh" ]]; then
            # shellcheck source=/dev/null
            source "$_conda_sh"
            return 0
        fi
    done
    if command -v conda >/dev/null 2>&1; then
        eval "$(conda shell.bash hook)"
        return 0
    fi
    return 1
}

if [[ "${IVY_NET_PDF_FORCE_ACTIVATE:-}" != "1" && -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
    case "${CONDA_DEFAULT_ENV:-}" in
        tenure_net|talent_net)
            echo "Using already-activated conda: ${CONDA_PREFIX}"
            CONDA_PYTHON="${CONDA_PREFIX}/bin/python"
            ;;
        *)
            _need_activate=1
            ;;
    esac
fi
if [[ "${_need_activate:-0}" == "1" ]] || [[ -z "${CONDA_PYTHON:-}" ]]; then
    if ! init_conda_shell; then
        echo "❌ Error: conda not found. On Rivanna: module load miniforge && re-run."
        exit 1
    fi
    if [[ -n "${IVY_NET_PDF_ENV:-}" ]]; then
        conda activate "${IVY_NET_PDF_ENV}"
    elif conda env list | awk '{print $1}' | grep -qx 'tenure_net'; then
        conda activate tenure_net
    elif conda env list | awk '{print $1}' | grep -qx 'talent_net'; then
        conda activate talent_net
    else
        echo "❌ Error: No tenure_net (or talent_net) env. Create tenure_net or set IVY_NET_PDF_ENV."
        exit 1
    fi
    CONDA_PYTHON="${CONDA_PREFIX}/bin/python"
fi

# Step 0: Convert Jupyter notebook to markdown if needed
if [ "$IS_NOTEBOOK" = true ]; then
    echo "Converting Jupyter notebook to markdown..."
    pandoc "$INPUT_FILE" -o "$MD_FILE" --wrap=none
    if [ $? -ne 0 ]; then
        echo "Error: pandoc conversion from notebook failed"
        exit 1
    fi
    echo "✅ Notebook converted to markdown: $MD_FILE"
fi

# Step 1: Convert markdown to HTML using pandoc
echo "Converting markdown to HTML..."
HTML_FILE="${MD_FILE%.md}.html"

# Important:
# - tex_math_single_backslash lets pandoc parse TeX math
# - tex_math_dollars allows $...$ and $$...$$
# - yaml_metadata_block OFF: standalone --- lines must stay *horizontal rules* (user preference).
#   With yaml_metadata_block on, Pandoc can treat --- as YAML boundaries and error on long docs.
# - --katex: LaTeX-quality math in HTML/PDF (better than --mathml in Chromium)
#   Requires network on first load (CDN) unless you vendor KaTeX.
PANDOC_FORMAT="markdown+tex_math_single_backslash+tex_math_dollars-yaml_metadata_block"

if [ -n "$CSS_FILE" ]; then
    pandoc "$MD_FILE" \
        -f "$PANDOC_FORMAT" \
        -o "$HTML_FILE" \
        --standalone \
        --css "$CSS_FILE" \
        --syntax-highlighting=pygments \
        --katex
else
    pandoc "$MD_FILE" \
        -f "$PANDOC_FORMAT" \
        -o "$HTML_FILE" \
        --standalone \
        --syntax-highlighting=pygments \
        --katex
fi

if [ $? -ne 0 ]; then
    echo "Error: pandoc conversion failed"
    exit 1
fi

# Step 2: Post-process HTML to add page-break styles to sections with H1
echo "Post-processing HTML to fix page breaks..."
"$CONDA_PYTHON" << PYTHON_EOF
import re

html_file = "$HTML_FILE"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Find all sections with H1 as first child and add inline style for page break
pattern = r'(<section[^>]*class="cell markdown"[^>]*>)\s*<h1>'
replacement = r'\1\n    <h1 style="page-break-before: always !important; break-before: page !important;">'
html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)

# Also add style to the section itself if it starts with H1
pattern2 = r'(<section[^>]*class="cell markdown"[^>]*)(>)\s*<h1'
def add_section_break(match):
    section_tag = match.group(1)
    closing = match.group(2)
    if 'style=' in section_tag:
        section_tag = re.sub(
            r'style="([^"]*)"',
            r'style="\1; page-break-before: always !important; break-before: page !important; page-break-after: avoid !important; break-after: avoid !important;"',
            section_tag
        )
    else:
        section_tag += ' style="page-break-before: always !important; break-before: page !important; page-break-after: avoid !important; break-after: avoid !important;"'
    return section_tag + closing + '\n    <h1'

html = re.sub(pattern2, add_section_break, html, flags=re.IGNORECASE)

# Ensure code cells following markdown sections don't break
pattern3 = r'(</section>)\s*(<div[^>]*class="cell code"[^>]*>)'
replacement3 = r'\1\n\2 style="page-break-before: avoid !important; break-before: avoid !important;"'
html = re.sub(pattern3, replacement3, html, flags=re.IGNORECASE)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ HTML post-processed for page breaks")
PYTHON_EOF

# Step 3: Convert HTML to PDF using Playwright (much better page break support)
echo "Converting HTML to PDF using Playwright..."
"$CONDA_PYTHON" << PYTHON_EOF
import sys
from pathlib import Path

html_file = "$HTML_FILE"
pdf_file = "$PDF_FILE"

try:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the HTML file
        html_path = Path(html_file).absolute()
        page.goto(html_path.as_uri(), wait_until="networkidle")

        # KaTeX loads from CDN; networkidle + short delay lets it finish rendering
        page.wait_for_timeout(1200)
        page.emulate_media(media="print")

        # Generate PDF with proper page break settings
        page.pdf(
            path=pdf_file,
            format="Letter",
            margin={
                "top": "0.25in",
                "right": "0.25in",
                "bottom": "0.25in",
                "left": "0.25in"
            },
            print_background=True,
            prefer_css_page_size=True
        )

        browser.close()

    print("✅ Successfully created PDF using Playwright")

except ImportError:
    print("❌ Error: Playwright not installed")
    print("   Install it with: pip install playwright")
    print("   Then run: playwright install chromium")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF

if [ $? -ne 0 ]; then
    echo "Error: PDF conversion failed"
    exit 1
fi

echo "✅ Successfully created PDF: $PDF_FILE"
if [ "$KEEP_HTML" = true ]; then
    echo "   HTML file: $HTML_FILE (kept for inspection)"
else
    if [ -f "$HTML_FILE" ]; then
        rm "$HTML_FILE"
        echo "   🧹 Cleaned up intermediate HTML file"
    fi
fi

if [ "$IS_NOTEBOOK" = true ] && [ -f "$TEMP_MD_FILE" ]; then
    echo "   Temporary markdown file: $TEMP_MD_FILE (kept for inspection)"
fi
