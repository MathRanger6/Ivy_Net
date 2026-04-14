# Google Docs Collaboration Workflow

This document tracks the sync process between markdown files (edited in Cursor) and Google Docs (for advisor collaboration).

## Setup Instructions

### 1. Install Required Tools

**Option A: Install pandoc-binary (Recommended - easiest)**
```bash
pip install pypandoc-binary
```

**Option B: Install pandoc system-wide**
```bash
# macOS
brew install pandoc
pip install pypandoc
```

### 2. Convert Markdown to .docx

Run the conversion script:
```bash
cd "Various PDE and Chat stuff/reference_documents"
python convert_to_googledocs.py Cox_Modeling_Chapter_Section_I.md
python convert_to_googledocs.py Cox_Modeling_Chapter_Section_II.md
```

This creates `.docx` files that can be imported into Google Docs.

### 3. Import to Google Docs

1. Upload the `.docx` file to Google Drive
2. Right-click → "Open with" → "Google Docs"
3. Share the document with your advisor (with comment/edit permissions)

## Sync Workflow

### Exporting to Google Docs (Cursor → Google Docs)

1. **Make your edits** in Cursor on the markdown files
2. **Convert to .docx** using the script:
   ```bash
   python convert_to_googledocs.py <filename>.md
   ```
3. **Update Google Doc**:
   - Option A: Replace the entire document (File → Upload → Replace)
   - Option B: Copy/paste new sections if only small changes
4. **Update sync log** below with date and changes made

### Importing from Google Docs (Google Docs → Cursor)

1. **Review advisor's comments/changes** in Google Docs
2. **Manually apply changes** to the markdown file in Cursor:
   - Read through comments and suggested edits
   - Apply accepted changes to the markdown file
   - Note any questions or discussions needed
3. **Update sync log** below with date and changes applied
4. **Re-export** if needed to show advisor you've incorporated their feedback

## Sync Log

### Section I (Cox_Modeling_Chapter_Section_I.md)

| Date | Action | Changes | Status |
|------|--------|---------|--------|
| [Date] | Initial export | Created .docx, uploaded to Google Docs | ✓ Complete |
| [Date] | Import feedback | [Describe changes from advisor] | ✓ Complete |
| [Date] | Re-export | [Describe updates made] | ✓ Complete |

### Section II (Cox_Modeling_Chapter_Section_II.md)

| Date | Action | Changes | Status |
|------|--------|---------|--------|
| [Date] | Initial export | Created .docx, uploaded to Google Docs | ✓ Complete |
| [Date] | Import feedback | [Describe changes from advisor] | ✓ Complete |
| [Date] | Re-export | [Describe updates made] | ✓ Complete |

## Tips for Collaboration

### LaTeX Formulas
- LaTeX formulas in markdown (`$$...$$` and `$...$`) should convert to MathML in .docx
- If formulas don't render correctly in Google Docs, you may need to:
  - Use Google Docs' equation editor to recreate them
  - Or keep formulas as text and note they need formatting

### Tracking Changes
- Use Google Docs' "Suggesting" mode for advisor edits
- Use comments for questions/discussions
- Keep this sync log updated to track what's been synced

### Version Control
- Keep the markdown files as the "source of truth"
- Google Docs is for collaboration, markdown is for editing
- Always merge changes back to markdown files

## Troubleshooting

### Conversion Issues
- If `pypandoc` not found: Install with `pip install pypandoc-binary`
- If formulas don't convert: Try the alternative method in the script
- If formatting is off: You may need to manually adjust in Google Docs

### Sync Issues
- If advisor's changes conflict with your edits: Review both versions and merge manually
- If formulas are lost: Re-add them using Google Docs equation editor or note in comments

## Quick Reference

**Export (Cursor → Google Docs):**
```bash
python convert_to_googledocs.py Cox_Modeling_Chapter_Section_I.md
# Upload .docx to Google Drive, open with Google Docs
```

**Import (Google Docs → Cursor):**
1. Review comments/edits in Google Docs
2. Manually apply to markdown file in Cursor
3. Update sync log


