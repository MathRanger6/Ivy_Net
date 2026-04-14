# PDF Conversion Guide

This guide describes the three supported ways to convert Markdown to PDF and how to control cleanup of intermediate HTML files.

Shell helpers live in **`scripts/`** at the workspace root. That directory is prepended to **`PATH`** in **`~/.project_envs.zsh`** (sourced from **`~/.zshrc`**), so you can run e.g. `convert_all_md_to_pdf.sh` from any terminal. **New terminal windows** pick this up automatically; in an existing session run `source ~/.zshrc` or open a new tab. You can also call scripts explicitly: `scripts/convert_all_md_to_pdf.sh` from the workspace directory.

---

## Methods

### 1) Convert **all** `.md` files (recursive)

Uses Playwright via `generate_pdf_playwright.sh`.

```bash
convert_all_md_to_pdf.sh
```

**Keep HTML files**:
```bash
convert_all_md_to_pdf.sh --keep-html
```

---

### 2) Convert only `current_documents/`

Uses Playwright via `generate_pdf_playwright.sh`.

```bash
convert_current_documents_md_to_pdf.sh
```

**Keep HTML files**:
```bash
convert_current_documents_md_to_pdf.sh --keep-html
```

---

### 3) Convert a single `.md` file

Uses Playwright via `generate_pdf_playwright.sh`.

```bash
convert_single_md_to_pdf.sh current_documents/COX_PLOT_HELPERS_OVERVIEW.md
```

**Keep HTML files**:
```bash
convert_single_md_to_pdf.sh current_documents/COX_PLOT_HELPERS_OVERVIEW.md --keep-html
```

**Optional output and CSS**:
```bash
convert_single_md_to_pdf.sh input.md output.pdf pdf_styles.css --keep-html
```

---

## Legacy / WeasyPrint path (single file)

This method uses `convert_md_to_pdf.py` (WeasyPrint). It also deletes intermediate HTML by default, with `--keep-html` to preserve it.

```bash
python convert_md_to_pdf.py current_documents/PIPELINE_CONFIG_OVERVIEW.md
python convert_md_to_pdf.py current_documents/PIPELINE_CONFIG_OVERVIEW.md --keep-html
```

---

## Notes

- Playwright generally yields better page breaks and layout consistency.
- The `--keep-html` flag is supported by all Playwright-based scripts and by `convert_md_to_pdf.py`.
