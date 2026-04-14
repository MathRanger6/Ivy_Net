# Workspace cleanup roadmap (talent / sports / tenure + shared)

**Intent:** Follow the phased “sane cleanup” plan without big-bang moves.  
**Hold:** Do **not** move, rename, or reorganize **`tenure_pipeline/faculty_snapshots/`** (or paths the pipeline writes there) until **Dropbox sync is stable** and you are confident files are not mid-transfer.

---

## Phase 0 — Wait on Dropbox (only for `faculty_snapshots`)

- Let **Dropbox finish** syncing the merged / large HTML tree under `tenure_pipeline/faculty_snapshots/`.
- Avoid **mass moves** of `tenure_pipeline/` that would change **`FACULTY_SNAPSHOTS_WRITE_ROOT`** / `resolve_faculty_snapshot_path()` expectations until this settles.
- **You can still do Phase 1–2** (Git, `.gitignore`, quarantine) without touching that directory.

---

## Phase 1 — Git without rearranging folders yet

**Goal:** One source of truth for code; no physical tree change required.

1. Create a **private GitHub repo** (name it e.g. `dissertation-pde` or `pde-workspace`).
2. In the workspace root, **`git init`** (if not already).
3. Add a **`.gitignore`** before the first real commit. Include at least:
   - `__pycache__/`, `*.pyc`, `.DS_Store`
   - `.env`, secrets
   - `venv/`, `.venv/`
   - **Large / sync-heavy trees you do not want in Git** — e.g. `tenure_pipeline/faculty_snapshots/` (optional but recommended: keep snapshots **out of Git**; they stay on disk + Dropbox).
   - Optional: `*.html` under `faculty_snapshots` if you ever stop ignoring the whole folder.
4. **First commit** = small: config, `functionsG_working.py`, `tenure_pipeline/*.py` **excluding** or ignoring bulk data dirs as above.
5. **`git remote add origin …`** and **`git push -u origin main`**.

**Why before moves:** `git mv` later preserves history; you get a safety net if a move goes wrong.

---

## Phase 2 — Quarantine clutter (no pipeline path changes)

**Goal:** Shrink what you look at every day; **do not** delete until you are sure.

1. Create **`archive/`** (or use existing **`obsolete_documents/`** / **`obsolete_files/``** consistently).
2. Move **clearly dead** copies: duplicate notebooks, old zips you will not reopen, **`deleted_files`** review (or leave as-is if too scary).
3. **Do not** move **`faculty_snapshots`** in this phase.

---

## Phase 3 — Introduce the target layout (when ready — after Dropbox OK for snapshots)

**Status (April 2026):** Physical layout **started**. See **`TARGET_WORKSPACE_TREE.md`** for the literal tree, symlinks, and move order.

**Done in repo:**

- **`tenure/`** — `540_tenure_pipeline.ipynb`, `541_ipeds_enrollment.ipynb`, `tenure_pipeline/`, `documents/` (ex–`tenure_documents`), `run_stage3b_cli.py`.
- **`sports/`** — `530_sports_pipeline.ipynb`, `sports_pipeline/`, `documents/`.
- **`talent/`** — `talent_pipeline/`, `documents/`.
- **Root compatibility symlinks:** `tenure_pipeline` → `tenure/tenure_pipeline`, `540_tenure_pipeline.ipynb` → `tenure/…`, `sports_pipeline`, `talent_pipeline`, `530_sports_pipeline.ipynb`, `run_stage3b_cli.py` → `tenure/run_stage3b_cli.py`.
- **`current_documents/`** — `tenure_documents`, `sports_documents`, `talent_documents` are **symlinks** into `../tenure/documents`, etc. **`Show_me/`** left in place.

**Not done yet:** `shared/`, moving **`scripts/`** / **`python_packages/`**, **`archive/`** bulk moves.

**Target shape (full vision):**

```text
<repo>/
  shared/              # optional later — functionsG_working, scripts, pdf_styles, python_packages
  talent/
  sports/
  tenure/
```

**Remaining order (suggested):**

1. Optional: **`shared/`** — move **`functionsG_working.py`**, **`scripts/`**, **`pdf_styles*.css`**, **`python_packages/`** when you update CELL 0 / paths.
2. **`archive/`** — quarantine **`obsolete_*`**, **`zips`**, etc., when ready.

**After each future move:** search for broken paths (`WORKSPACE_ROOT`, `sys.path`, notebook CELL 0). **Kernels** should use **repo root** as cwd so symlinks `tenure_pipeline` keep CELL 0 valid.

---

## Phase 4 — Fix imports and notebook roots

1. **Single rule:** Either always **open the Git repo root** in Cursor, or update every **`WORKSPACE_ROOT = Path('.').resolve()`** cell to match the new notebook location.
2. Ensure **`tenure_pipeline/`** stays importable (e.g. `sys.path` includes repo root and/or `tenure/tenure_pipeline`).
3. Run **one** short smoke test: import `functionsG_working`, run a tiny cell from `540_tenure_pipeline` that only loads CELL 0.

---

## Phase 5 — Rivanna

1. **`git clone`** the same repo under your **`cdh` / `Chas_Working`** (or wherever you keep code).
2. **`conda env create`** from an **`environment.yml`** when you add one (tenure_net equivalent on HPC).
3. **Env vars** for OpenAlex bulk paths — **not** committed to Git.

---

## What to skip until `faculty_snapshots` is stable

- Moving **`tenure_pipeline/`** wholesale if that would confuse Dropbox paths mid-sync.
- Git-committing **gigabytes** of HTML under **`faculty_snapshots`** (ignore in `.gitignore` regardless).

---

## Quick checklist (copy/paste)

- [ ] Dropbox stable for `faculty_snapshots` (user judgment).
- [ ] `.gitignore` includes `tenure_pipeline/faculty_snapshots/` (or similar).
- [ ] `git init` / remote / first push.
- [ ] `archive/` or tidy obsolete.
- [ ] Create `shared/`, `talent/`, `sports/`, `tenure/` and move in order above.
- [ ] Fix CELL 0 / `sys.path` / workspace file.
- [ ] Smoke test tenure notebook.
- [ ] Clone on Rivanna.

---

*Companion docs: `GIT_MULTIPLE_MACHINES_ELEMENTARY.md`, `RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md`, `TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md`.*
