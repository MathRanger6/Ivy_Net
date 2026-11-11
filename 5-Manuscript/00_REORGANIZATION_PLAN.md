# Manuscript reorganization plan (stage 2 complete, 2026-11-09)

Prepared 2026-11-09 for Charles. Companion file: `00_MOVE_MANIFEST_proposed.csv` (every entry, current path, proposed path, status).

**Binding rule:** see [`README.md`](README.md) — dissertation product in `5-Manuscript/`; code and heavy analysis in `new_VECTOR_work/`.

---

## Why

The repo fragmented: chapter drafts, agent mail, backups, and 3.7 GB of analysis code share one folder (`new_VECTOR_work/`). Committee-facing work and pipeline work need separate homes with clear rules for agents.

## Three zones (coherence model)

```
5-Manuscript/              DISSERTATION PRODUCT — chapters, ES, sources, formatting
3-Master_Plan/re_entry/    CAMPAIGN — disposable threads, YOU ARE HERE, HERO sandbox PNGs
3-Master_Plan/VECTOR_work/ PLANNING + ENGINEERING — analysis folders, archived PD-era planning
```

| Zone | What belongs | What does not |
|------|----------------|---------------|
| **5-Manuscript** | Word/md chapter drafts, executive summaries, per-chapter agent Q&A for prose, Zotero-facing masters, COS templates | Notebooks, `lg_exploration/`, raw scrape outputs |
| **re_entry** | `_DISPOSABLE_*_thread.md`, short-lived handoffs tied to a writing week | Full chapter text |
| **VECTOR_work** | `new_VECTOR_work/{education_analysis,lg_exploration,...}`, reorganized **archive/** for Aug–Sep planning PDFs, COMPASS briefs that are not chapter text | New chapter drafts (after stage 2) |

Transcripts stay in repo-root `transcripts/`. Domain code stays in `talent/`, `sports/`, `tenure/`.

## Target layout under 5-Manuscript

Chapter first. Same subfolders in every chapter:

```
5-Manuscript/
  README.md
  00_Front_matter_and_formatting/
  00_Project_wide/
  01_Introduction/          drafts/  backups/
  02_Literature_Review/     drafts/  notes/  sources/  backups/
  03_Data_and_Empirics/     drafts/  notes/  analysis_pointer/
  04_Model/                 drafts/  notes/  backups/  figures/  figures_pointer/  analysis_pointer/
  05_Assignment/            notes/  analysis_pointer/
  06_Consequences/
  _paper_track/             legacy paper-track from old 5-Manuscript
  _presentations/
  _backups/                 optional cross-chapter manuscript saves (if needed)
```

**`drafts/`** = exactly one “current” working surface per artifact (master Word, active md ES). Agents open paths here.

**`backups/`** = everything else for that chapter: dated copies, `before_*`, Dropbox “conflicted copy”, old PDF exports of the same draft. **Never** leave backups in `drafts/` (Charles, 2026-11-09).

**`analysis_pointer/`** = short README only, pointing at the real folder under `new_VECTOR_work/`.

## What stays in new_VECTOR_work (no move)

| Folder | Pointer from |
|--------|----------------|
| `lg_exploration/` | `05_Assignment/analysis_pointer/` |
| `education_analysis/` | `03_Data_and_Empirics/analysis_pointer/` |
| `manuscript_figures/` | `04_Model/figures_pointer/` |
| `assort_analysis/` | `05_Assignment/analysis_pointer/` |
| `jazz_night/` | `04_Model/analysis_pointer/` |

After stage 2, `new_VECTOR_work/` should contain **no new** chapter drafts—only code, data, and pointers from `5-Manuscript`.

## VECTOR_work tidying (stays in 3-Master_Plan, not 5-Manuscript)

Charles (2026-11-09): Aug–Sep VECTOR_work material **stays under VECTOR_work**, not dumped into `5-Manuscript/_archive/`. Re-house with a clear tree, e.g.:

```
3-Master_Plan/VECTOR_work/
  archive/2026_08-09_planning/     # loose root files: Quayle, ASSIGN PDFs, COMPASS briefs, storyboard
  agent_handoffs/                  # keep as-is if still referenced
  handoff_upload_no_repo/          # keep or fold into archive/ after inventory
  new_VECTOR_work/                 # engineering only (post stage 2)
  README.md                        # “product vs engineering” (to add in stage 2)
```

Same idea for clutter inside `new_VECTOR_work/`: dated `Model_Chapter_*before_*`, `Working_Manuscript_Backups/`, etc. → chapter `backups/` under `5-Manuscript/04_Model/backups/`, not mixed with active drafts.

## Charles decisions locked in (2026-11-09)

| # | Decision |
|---|----------|
| 1 | Introduction handoff files → `01_Introduction/drafts/` |
| 2 | Keep Dropbox conflicted lit-review copy → `02_Literature_Review/backups/` only |
| 3 | Manuscript product strictly under `5-Manuscript/`; VECTOR_work for coding/planning archives |
| 4 | `03_Dissertation_Tone.docx` = numbered handoff copy of `Dissertation Tone.docx`; **keep one** in `00_Front_matter_and_formatting/` after move |

## Former REVIEW rows — locked in manifest (Charles, 2026-11-09 ~15:45)

| File | Decision |
|------|----------|
| `Education_Transitions_and_Congestion_Review` | MOVE → `03_Data_and_Empirics/notes/` |
| `Scholar_Fine_Gray_and_Army_HERO_Explained` | MOVE → `03_Data_and_Empirics/notes/` (historical; not Ch.3 body) |
| `Charles_to_VECTOR_Army_band_and_theta_Sep24` | **COPY** → `04_Model/notes/`; original stays in `new_VECTOR_work/` |
| `Assortativity_MBB_issues.docx` | MOVE → `05_Assignment/notes/` |
| `Chapter_5_Survival_Model_outline.md` | MOVE → `5-Manuscript/_archive/` |
| `collab_test.docx` | **DELETE** |

## Stage 2 procedure (unchanged; run only when Charles says go)

1. Close Word; pause Dropbox if needed.
2. `git mv` per manifest (MOVE → MOVE_LAST).
3. Dedupe tone doc; delete or archive `03_Dissertation_Tone.docx` after confirming byte match.
4. Path-fix script for ~94 `new_VECTOR_work` references in md/agents docs.
5. Stub READMEs at old paths; add `analysis_pointer/` READMEs.
6. Add `3-Master_Plan/VECTOR_work/README.md` and `new_VECTOR_work/README.md`.

## Stage 3

Update `AGENTS.md` with the three-zone table; point `START_HERE_MANUSCRIPT.md` at `5-Manuscript/README.md`; relocate `convert_manuscript_md_to_pdf.sh` with callers.

## Risks

Unchanged: Word+Zotero master move; November one-chapter-per-week pace — schedule stage 2 in a gap.
