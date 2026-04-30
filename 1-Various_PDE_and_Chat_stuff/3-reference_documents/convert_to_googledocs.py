#!/usr/bin/env python3
"""
Convert Markdown files to .docx format for Google Docs collaboration.

This script converts markdown files (with LaTeX math) to .docx format
that can be imported into Google Docs for collaboration with advisors.

Requirements:
    pip install pypandoc-binary markdown pypandoc

Or install pandoc separately:
    macOS: brew install pandoc
    Then: pip install pypandoc
"""

import os
import sys
from pathlib import Path

def check_pandoc():
    """Check if pandoc is available."""
    try:
        import pypandoc
        return True, pypandoc
    except ImportError:
        return False, None

def install_instructions():
    """Print installation instructions."""
    print("=" * 70)
    print("PANDOC NOT FOUND")
    print("=" * 70)
    print("\nTo convert markdown to .docx, you need pandoc installed.")
    print("\nOption 1: Install pandoc-binary (easiest):")
    print("  pip install pypandoc-binary")
    print("\nOption 2: Install pandoc system-wide:")
    print("  macOS: brew install pandoc")
    print("  Then: pip install pypandoc")
    print("\nOption 3: Use online converter:")
    print("  Visit: https://cloudconvert.com/md-to-docx")
    print("=" * 70)
    return False

def convert_md_to_docx(md_file, output_dir=None):
    """Convert a markdown file to .docx format."""
    has_pandoc, pypandoc = check_pandoc()
    
    if not has_pandoc:
        return install_instructions()
    
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"Error: File not found: {md_file}")
        return False
    
    # Determine output directory
    if output_dir is None:
        output_dir = md_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output filename
    output_file = output_dir / f"{md_path.stem}.docx"
    
    try:
        print(f"Converting: {md_path.name}")
        print(f"Output: {output_file}")
        
        # Convert markdown to docx
        # Using 'markdown' as input format to preserve LaTeX math
        pypandoc.convert_file(
            str(md_path),
            'docx',
            outputfile=str(output_file),
            format='markdown',
            extra_args=['--mathml']  # Convert LaTeX to MathML for better compatibility
        )
        
        print(f"✓ Successfully created: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Upload {output_file} to Google Drive")
        print(f"2. Open with Google Docs")
        print(f"3. Share with your advisor")
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        print("\nTrying alternative method without MathML...")
        try:
            pypandoc.convert_file(
                str(md_path),
                'docx',
                outputfile=str(output_file),
                format='markdown'
            )
            print(f"✓ Successfully created: {output_file}")
            return True
        except Exception as e2:
            print(f"Error: {e2}")
            return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_googledocs.py <markdown_file> [output_dir]")
        print("\nExample:")
        print("  python convert_to_googledocs.py Cox_Modeling_Chapter_Section_I.md")
        print("  python convert_to_googledocs.py Cox_Modeling_Chapter_Section_I.md ./exports")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_md_to_docx(md_file, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()


