# Talent (Army) workspace — layout, symlinks, and AWS exports

**Audience:** You (and agents) when working on **501–520** officer pipelines, Cox helpers, and advisor-driven changes.  
**Canonical doc home:** this folder = `talent/documents/` (also reachable as `current_documents/talent_documents` → symlink at repo root).

---

## 1. Where the “real” code lives

- **Package / notebook tree:** `talent/talent_pipeline/`  
  (notebooks like `520_pipeline_cox_working.ipynb`, `cox_plot_helpers.py`, `pipeline_config*.py`, `py_503_hierarchies.py`, etc.)

- **Why you also see `talent_pipeline` at the repo root**  
  At the **Cursor / repo root** there is a **symbolic link**:
  - `talent_pipeline` → `talent/talent_pipeline`

  That keeps **CELL 0** and scripts that assume paths like `WORKSPACE_ROOT / 'talent_pipeline'` (with `cwd` = repo root) working after the **April 2026** physical move of code under `talent/`. The same pattern is used for **sports** and **tenure** (`sports_pipeline`, `tenure_pipeline`).

- **You are not maintaining two separate copies** — one directory is canonical, one is a **compatibility link**.

**Design reference:** `tenure/documents/TARGET_WORKSPACE_TREE.md` and `tenure/documents/WORKSPACE_CLEANUP_ROADMAP.md` (Phase 3).

---

## 2. `talent/Army_AWS_download/`

- **Role:** Staging area for **snapshots of “live” code** pulled from the **Army AWS** environment (e.g. `TALENT_NET_export_YYYYMMDD-hhmm/`) so you can **diff, merge, or reapply** changes **locally** in step with advisor guidance.
- **Not** the day-to-day working tree: treat it as a **source for comparison** until you explicitly fold files into `talent/talent_pipeline/`.
- **After** merging: note in your commit or lab notebook which export folder you aligned to (avoids “which 520 is truth?” later).

---

## 3. Agent conversations and SpecStory

- **SpecStory** stores portable chat history under **`.specstory/history/`** in the repo (dated `*.md` files).  
- Use that when you need the **narrative** for why a move or symlink was made (e.g. Phase 1 / roadmap work with Peer); the **architectural** answer is still **`TARGET_WORKSPACE_TREE.md`**.

---

## 4. Quick path cheat sheet

| You want | Path |
|----------|------|
| Edit 520 / helpers | `talent/talent_pipeline/` (or `talent_pipeline/` at root — same files) |
| Handoff / Cox / Coda memos | `talent/documents/` |
| Compare to AWS | `talent/Army_AWS_download/TALENT_NET_export_*/` |
| Workspace move rationale | `tenure/documents/TARGET_WORKSPACE_TREE.md` |

---

*Coda, April 2026 — adjust dates or export folder names as your snapshots change.*
