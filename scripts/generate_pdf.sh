#!/bin/bash
# Script to generate PDF from markdown or Jupyter notebooks using pandoc and weasyprint
# Usage: ./generate_pdf.sh [input.md|input.ipynb] [output.pdf] [styles.css]

_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_WORKSPACE_ROOT="$(cd "$_SCRIPTS_DIR/.." && pwd)"
cd "$_WORKSPACE_ROOT" || exit 1

# Set default values
INPUT_FILE="${1:-CUMULATIVE_OER_METRICS_OVERVIEW.md}"

# Determine file type and set output PDF name and default CSS
if [[ "$INPUT_FILE" == *.ipynb ]]; then
    # Jupyter notebook input
    PDF_FILE="${2:-${INPUT_FILE%.ipynb}.pdf}"
    TEMP_MD_FILE="${INPUT_FILE%.ipynb}_temp.md"
    MD_FILE="$TEMP_MD_FILE"
    IS_NOTEBOOK=true
    DEFAULT_CSS="pdf_styles_notebook.css"
elif [[ "$INPUT_FILE" == *.md ]]; then
    # Markdown input
    PDF_FILE="${2:-${INPUT_FILE%.md}.pdf}"
    MD_FILE="$INPUT_FILE"
    IS_NOTEBOOK=false
    DEFAULT_CSS="pdf_styles.css"
else
    echo "Error: Input file must be .md or .ipynb"
    exit 1
fi

# Set CSS file (use provided CSS or default based on file type)
CSS_FILE="${3:-$DEFAULT_CSS}"

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

# Step 0: Convert Jupyter notebook to markdown if needed
if [ "$IS_NOTEBOOK" = true ]; then
    echo "Converting Jupyter notebook to markdown..."
    # Use pandoc for notebook conversion (simpler and more reliable)
    # pandoc can directly convert .ipynb to markdown
    pandoc "$INPUT_FILE" -o "$MD_FILE" --wrap=none
    if [ $? -ne 0 ]; then
        echo "Error: pandoc conversion from notebook failed"
        echo "   Make sure pandoc supports .ipynb format (pandoc >= 2.5)"
        exit 1
    fi
    echo "✅ Notebook converted to markdown: $MD_FILE"
fi

# Step 1: Convert markdown to HTML using pandoc
echo "Converting markdown to HTML..."
HTML_FILE="${MD_FILE%.md}.html"

if [ -n "$CSS_FILE" ]; then
    pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --css "$CSS_FILE" --syntax-highlighting=pygments --mathjax
else
    pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --syntax-highlighting=pygments --mathjax
fi

if [ $? -ne 0 ]; then
    echo "Error: pandoc conversion failed"
    exit 1
fi

# Step 2: Post-process HTML to add page-break styles to sections with H1
echo "Post-processing HTML to fix page breaks..."
python3 << 'PYTHON_EOF' "$HTML_FILE"
import re
import sys

html_file = sys.argv[1]

with open(html_file, 'r') as f:
    html = f.read()

# Find all sections with H1 as first child and add inline style for page break
# This is a workaround for WeasyPrint not respecting CSS :has() selector
# Pattern: <section...class="cell markdown"...> followed by <h1>
pattern = r'(<section[^>]*class="cell markdown"[^>]*>)\s*<h1>'
replacement = r'\1\n    <h1 style="page-break-before: always !important; break-before: page !important;">'

html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)

# Also add style to the section itself if it starts with H1
# This ensures the section breaks, not just the H1
# BUT CRITICALLY: Also add page-break-after: avoid to prevent breaking after the section
pattern2 = r'(<section[^>]*class="cell markdown"[^>]*)(>)\s*<h1'
def add_section_break(match):
    section_tag = match.group(1)
    closing = match.group(2)
    # Check if style attribute already exists
    if 'style=' in section_tag:
        # Add to existing style - break before but NOT after
        section_tag = re.sub(r'style="([^"]*)"', r'style="\1; page-break-before: always !important; break-before: page !important; page-break-after: avoid !important; break-after: avoid !important;"', section_tag)
    else:
        # Add new style attribute - break before but NOT after
        section_tag += ' style="page-break-before: always !important; break-before: page !important; page-break-after: avoid !important; break-after: avoid !important;"'
    return section_tag + closing + '\n    <h1'

html = re.sub(pattern2, add_section_break, html, flags=re.IGNORECASE)

# Also ensure code cells following markdown sections don't break
# Add inline style to code cells that follow markdown sections
pattern3 = r'(</section>)\s*(<div[^>]*class="cell code"[^>]*>)'
replacement3 = r'\1\n\2 style="page-break-before: avoid !important; break-before: avoid !important;"'
html = re.sub(pattern3, replacement3, html, flags=re.IGNORECASE)

with open(html_file, 'w') as f:
    f.write(html)

print("✅ HTML post-processed for page breaks")
PYTHON_EOF

# Step 3: Convert HTML to PDF using weasyprint
echo "Converting HTML to PDF..."
python -c "from weasyprint import HTML; HTML('$HTML_FILE').write_pdf('$PDF_FILE')"

if [ $? -ne 0 ]; then
    echo "Error: PDF conversion failed"
    exit 1
fi

echo "✅ Successfully created PDF: $PDF_FILE"
echo "   HTML file: $HTML_FILE (kept for inspection)"
echo "   💡 Tip: You can open the HTML file in a browser to inspect the structure"

# Clean up temporary markdown file if it was created from notebook
if [ "$IS_NOTEBOOK" = true ] && [ -f "$TEMP_MD_FILE" ]; then
    echo "   Temporary markdown file: $TEMP_MD_FILE (kept for inspection)"
    echo "   💡 Tip: You can inspect the markdown to see how pandoc converted the notebook"
    # Optionally remove temp file - uncomment the next line if you want to clean it up
    # rm "$TEMP_MD_FILE"
fi

