# Target workspace tree (names only) + move order

**Repo root:** `Cursor Workspace PDE/` (unchanged name; still your Cursor folder).

## Literal target tree

```text
Cursor Workspace PDE/
├── .cursor/
├── functionsG_working.py          # stays at root (imports from tenure_pipeline, notebooks)
├── pyproject.toml
├── python_packages/               # DBLP, etc. — stays at root for now (CELL 0 paths)
├── scripts/                       # PDF pipeline — stays at root for now
├── pdf_styles.css
├── pdf_styles_notebook.css
├── convert_md_to_pdf.py
├── run_stage3b_cli.py             # SYMLINK → tenure/run_stage3b_cli.py
│
├── tenure/                        # dissertation / R1 CS pipeline
│   ├── 540_tenure_pipeline.ipynb
│   ├── 541_ipeds_enrollment.ipynb
│   ├── run_stage3b_cli.py         # Stage 3B CLI (tenure-specific)
│   ├── tenure_pipeline/           # code + faculty_snapshots + JSONL outputs
│   └── documents/                 # was current_documents/tenure_documents/
│
├── 530_sports_pipeline.ipynb      # SYMLINK → sports/530_sports_pipeline.ipynb
├── sports/
│   ├── 530_sports_pipeline.ipynb
│   ├── sports_pipeline/
│   └── documents/                 # was current_documents/sports_documents/
│
├── talent/
│   ├── talent_pipeline/
│   └── documents/                 # was current_documents/talent_documents/
│
├── current_documents/             # thin folder: symlinks + Show_me (see below)
│   ├── tenure_documents   → ../tenure/documents
│   ├── sports_documents   → ../sports/documents
│   ├── talent_documents   → ../talent/documents
│   └── Show_me/                   # optional: move later to archive/
│
├── archive/                       # quarantine (phase 2+)
│   └── (obsolete_documents, obsolete_files, … when you are ready)
│
├── tenure_pipeline                # SYMLINK → tenure/tenure_pipeline  (compatibility)
├── 540_tenure_pipeline.ipynb      # SYMLINK → tenure/540_tenure_pipeline.ipynb
└── (other legacy / outputs / big_dfs / … unchanged in this phase)
```

## Move order (executed)

1. Create **`tenure/`**, **`sports/`**, **`talent/`**, **`archive/`**.
2. **Tenure:** move **`tenure_pipeline/`** → **`tenure/tenure_pipeline/`**; symlink **`tenure_pipeline`** at root → **`tenure/tenure_pipeline`**.
3. **Tenure:** move **`540_*`**, **`541_*`** notebooks → **`tenure/`**; symlink **`540_tenure_pipeline.ipynb`** at root → **`tenure/540_tenure_pipeline.ipynb`**.
4. **Tenure:** move **`current_documents/tenure_documents`** → **`tenure/documents`**; symlink **`current_documents/tenure_documents`** → **`../../tenure/documents`** (relative).
5. **Sports:** same pattern for **`sports_pipeline/`**, **`530_*.ipynb`**, **`sports_documents`**.
6. **Talent:** same for **`talent_pipeline/`**, **`talent_documents`**.
7. **`run_stage3b_cli.py`:** **done** — lives in **`tenure/run_stage3b_cli.py`**; **`chdir`** to **repo root** so CELL 0 sees **`python_packages/`**; root **`run_stage3b_cli.py`** is a symlink.

## Why symlinks at root?

**CELL 0** uses `WORKSPACE_ROOT / 'tenure_pipeline'` with **`WORKSPACE_ROOT = Path('.').resolve()`** = repo root when you run from root. Moving the real folder to **`tenure/tenure_pipeline`** without changing the notebook requires either:

- **Symlink** `tenure_pipeline` → `tenure/tenure_pipeline`, or  
- A **large CELL 0 edit** to use `tenure/tenure_pipeline` everywhere.

Phase 1 uses **symlinks** so nothing in **`540_tenure_pipeline.ipynb`** breaks. If Dropbox ever mis-syncs symlinks, switch to explicit paths in CELL 0.

## Next phases (not automatic)

- Move **`obsolete_*`**, **`deleted_files`**, **`zips`** into **`archive/`** when you are ready.
- **`git init`** + `.gitignore` per **`WORKSPACE_CLEANUP_ROADMAP.md`**.
- Optional: relocate **`python_packages/`** under **`shared/`** and update CELL 0 (later).

---

*Created as part of physical cleanup, April 2026.*
