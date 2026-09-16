# Manifest — upload this folder to VECTOR

**Folder:** `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/`  
**Charles action:** Zip this folder (or upload files individually). VECTOR has **no repo access** — everything he needs to **read** is here.

---

## Included (markdown copies)

| File | Description |
|------|-------------|
| `00_READ_ME_FIRST_FOR_VECTOR.md` | **Start here** — phase, assignment, read order |
| `01_ASSIGNMENT_story_outline.md` | Deliverable spec + skeleton |
| `03_CHARLES_locks_Sep16.md` | Judgment calls + gap priorities |
| `02_paper_flipbook_PD30.md` | Slide claims (mine for story; don’t mirror 1:1) |
| `04_Problem_in_Plain_English.md` | Thesis / phenomenon |
| `05_Three_Kinds_of_Model.md` | Layer A/B/C |
| `06_BINDING_Selection_is_its_own_step.md` | **Binding** score ≠ select |
| `07_PAPER_Campaign_Plan.md` | Campaign sequencing |
| `08_Pass_A_and_Pass_B_plain_English.md` | Mechanism sim plain English |
| `09_PD30_Alex_notes.md` | Alex PD30 locks |
| `99_BACKGROUND_COMPASS_questionnaire_full.md` | **Optional** — full COMPASS prefill (~730 lines) |

---

## Send separately (not in repo for VECTOR)

Charles attaches these out-of-band (email / drive):

| Asset | Why |
|-------|-----|
| `_DISPOSABLE_paper_flipbook_PD30_FIGURE_DECK.pptx` (or `.html`) | Talk skeleton — visual skim |
| `_DISPOSABLE_paper_flipbook_PD30_FIGURE_INVENTORY.pptx` (or `.html`) | Full figure catalog |
| `_DISPOSABLE_paper_flipbook_PD30.pdf` | Flipbook print-friendly |
| Key PNGs if VECTOR needs to *see* heroes (optional): Army G1, MBB 3×3, tenure 3×3, λ knockout | Visual literacy for outline |

---

## VECTOR returns

| File | To |
|------|-----|
| `STORY_OUTLINE_Charles_Alex.md` | Charles + Alex — then Charles shares with COMPASS if useful |

---

## Regenerate copies after repo edits

From repo root:

```bash
rsync -av --delete \
  3-Master_Plan/VECTOR_work/handoff_upload_no_repo/ \
  /tmp/vector_handoff/  # or re-run COMPASS copy step
```

Or ask COMPASS to refresh copies when flipbook or locks change materially.

**Last copied:** 2026-09-16
