#!/bin/bash
# Script to generate PDF from markdown or Jupyter notebooks using pandoc and Playwright
# Playwright uses a real browser engine and has much better page break support than WeasyPrint
# Usage: ./generate_pdf_playwright.sh [input.md|input.ipynb] [output.pdf] [styles.css] [--keep-html]

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

# Activate conda environment and run conversion
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate talent_net

# Ensure we use the conda environment's Python (not system python3)
CONDA_PYTHON="/opt/anaconda3/envs/talent_net/bin/python"

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

if [ -n "$CSS_FILE" ]; then
    pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --css "$CSS_FILE" --syntax-highlighting=pygments --mathml
else
    pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --syntax-highlighting=pygments --mathml
fi

if [ $? -ne 0 ]; then
    echo "Error: pandoc conversion failed"
    exit 1
fi

# Step 2: Post-process HTML to add page-break styles to sections with H1
echo "Post-processing HTML to fix page breaks..."
"$CONDA_PYTHON" << PYTHON_EOF
import re
import sys

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
        section_tag = re.sub(r'style="([^"]*)"', r'style="\1; page-break-before: always !important; break-before: page !important; page-break-after: avoid !important; break-after: avoid !important;"', section_tag)
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
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
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

