#!/bin/bash
# Convert only .md files in tenure/documents/ to PDF
# Uses generate_pdf_playwright.sh for each file
# PDFs are created in tenure/documents/
# Usage: ./convert_tenure_documents_md_to_pdf.sh [--keep-html]

# Parse optional flags
KEEP_HTML=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./convert_tenure_documents_md_to_pdf.sh [--keep-html]"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: ./convert_tenure_documents_md_to_pdf.sh [--keep-html]"
            exit 1
            ;;
    esac
done

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

# Activate conda environment
echo "🔧 Activating conda environment: tenure_net"
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate tenure_net

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate conda environment 'tenure_net'"
    exit 1
fi

echo "✅ Conda environment activated"
echo ""

# Look directly in tenure/documents/ (the real directory, no symlink needed)
TENURE_DOCS_DIR="$WORKSPACE_DIR/tenure/documents"
if [ ! -d "$TENURE_DOCS_DIR" ]; then
    echo "❌ Error: tenure/documents directory not found at: $TENURE_DOCS_DIR"
    exit 1
fi

echo "🔍 Finding all .md files in: $TENURE_DOCS_DIR"
MD_FILES=$(find "$TENURE_DOCS_DIR" -type f -name "*.md" | sort)

# Count total files (handle case where no files found)
if [ -z "$MD_FILES" ]; then
    TOTAL_FILES=0
else
    TOTAL_FILES=$(echo "$MD_FILES" | wc -l | tr -d ' ')
fi

if [ "$TOTAL_FILES" -eq 0 ]; then
    echo "⚠️  No .md files found in current_documents/tenure_documents"
    exit 0
fi

echo "📄 Found $TOTAL_FILES .md file(s) to convert"
echo ""

# Counter for progress
COUNT=0
SUCCESS_COUNT=0
FAIL_COUNT=0

# Process each .md file
while IFS= read -r md_file; do
    # Skip if empty line
    [ -z "$md_file" ] && continue
    
    COUNT=$((COUNT + 1))
    
    # Get directory and filename
    MD_DIR=$(dirname "$md_file")
    MD_BASENAME=$(basename "$md_file")
    # Save PDF alongside the source .md in tenure/documents/
    PDF_FILE="$TENURE_DOCS_DIR/${MD_BASENAME%.md}.pdf"
    
    # Make path relative to workspace for cleaner output
    RELATIVE_PATH="${md_file#$WORKSPACE_DIR/}"
    
    echo "[$COUNT/$TOTAL_FILES] Processing: $RELATIVE_PATH"
    
    # Change to the directory containing the .md file so relative paths work correctly
    cd "$MD_DIR" || {
        echo "   ❌ Error: Could not change to directory: $MD_DIR"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    }
    
    # Find CSS file relative to workspace root (not current directory)
    # CSS file should be in workspace root
    CSS_FILE="$WORKSPACE_DIR/pdf_styles.css"
    
    # Run the PDF generation script
    # Use absolute path for the input file to avoid path issues
    # Pass CSS file path if found
    KEEP_FLAG=""
    if [ "$KEEP_HTML" = true ]; then
        KEEP_FLAG="--keep-html"
    fi
    if [ -f "$CSS_FILE" ]; then
        "$GENERATE_PDF_SCRIPT" "$md_file" "$PDF_FILE" "$CSS_FILE" $KEEP_FLAG
    else
        "$GENERATE_PDF_SCRIPT" "$md_file" "$PDF_FILE" $KEEP_FLAG
    fi
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Success: Created PDF at $PDF_FILE"
        
        # Also clean up any temporary markdown files (if generated from notebooks)
        TEMP_MD_FILE="$MD_DIR/${MD_BASENAME%.md}_temp.md"
        if [ -f "$TEMP_MD_FILE" ]; then
            rm "$TEMP_MD_FILE"
            echo "   🧹 Cleaned up temporary markdown file"
        fi
        
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "   ❌ Failed: Could not create PDF for $RELATIVE_PATH"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    echo ""
    
done <<< "$MD_FILES"

# Summary
echo "=" 
echo "📊 Conversion Summary:"
echo "   Total files: $TOTAL_FILES"
echo "   ✅ Successful: $SUCCESS_COUNT"
echo "   ❌ Failed: $FAIL_COUNT"
   echo "   📁 PDFs saved to: tenure/documents/"
echo ""

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "🎉 All conversions completed successfully!"
    exit 0
else
    echo "⚠️  Some conversions failed. Check the output above for details."
    exit 1
fi
