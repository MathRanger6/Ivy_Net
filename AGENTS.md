# Agent instructions — read before editing this repository

**Binding project rules, not suggestions.**

## Always-on

0. **[`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](3-Master_Plan/BINDING_Selection_is_its_own_step.md)** — **Binding:** Environment (`L_net = B − D`) ≠ advancement. Advancement = **score** (Alex `S_i = A_i − λ·L_C`) then **select** (top K now; later stochastic). Hero = outcomes; never merge into “one model.” Charles #1 confusion (Jul 2026); score≠select sharpened Jul 2026.

1. **`.cursor/rules/notebook-blank-edit.mdc`** — Notebook **prime directive:** every `.ipynb` change in a reply should be **line/cluster red/green** reviewable. Each **user message**: usually **burn** first (`skip burn` if user says so), then substantive edits; **ask** when unsure; **`EditNotebook`** for cell bodies (no MCP `notebook_edit_cell` / raw JSON unless user says **`yes, skip rules for this`**). No cap on cells per reply.
2. **`.cursor/rules/incremental-writes.mdc`** — Network/large I/O loops: append + flush + resume-skip.
3. **`.cursor/rules/jupyter-notebook-workflow.mdc`** — `540_tenure_pipeline.ipynb`: burn at **cell index 3**; same-cell merge rule.

## Notebooks

- Follow **`notebook-blank-edit.mdc`** before any cell-body edit.
- If review UI fails: **ask** the user — do not plow ahead.
- New notebook scaffold via MCP: **ask first**.

## Charles re-entry (when lost or under deadline)

- **Start here:** [`3-Master_Plan/re_entry/00_READ_ME_FIRST.md`](3-Master_Plan/re_entry/00_READ_ME_FIRST.md) — three standalone narrative docs; no cross-reference scavenger hunt.
- **Do not** point Charles at `Charles_reading_list.md` (14-doc stack), shorthand memos, or agent mail until re_entry 01–03 are done.
- New explanatory prose for Charles → write under `3-Master_Plan/re_entry/` (narrative, inline glossary). Parked docs listed in [`re_entry/PARKED_FOR_LATER.md`](3-Master_Plan/re_entry/PARKED_FOR_LATER.md).

## Cursor Plan mirrors

- **Live IDE plans:** `~/.cursor/plans/` (Mac only; not in git). **Canonical repo copy:** [`3-Master_Plan/plans/`](3-Master_Plan/plans/) — Charles reads and PDFs from here.
- **After any substantive edit** to a **keep** plan in `~/.cursor/plans/`, run `./scripts/mirror_plan.sh <slug>` in the same reply (updates the matching `*_<slug>.plan.md` in the repo).
- **Keep (mirror):** scientific/sequencing plans, multi-section docs, Rivanna-relevant work, plans Charles should read. **Skip (ephemeral):** `fix_*` / `plans_git_*`, one-off tooling, or user says `skip mirror` — script skips ephemeral slugs unless `--force`.
- If a paired domain memo exists (e.g. `sports/documents/Hero_Model_Three_Layers_Memo.md`), update it when plan content changes materially; plan mirror is the minimum repo update.

## Git commits (when the user asks)

- Include `.specstory/history/*.md` (agent chat archives) unless they say otherwise.
- Include `3-Master_Plan/plans/*.md` when important Cursor Plan-mode work has been mirrored there (see [`3-Master_Plan/plans/README.md`](3-Master_Plan/plans/README.md)).
- **Not tracked:** `~/.cursor/plans/` lives outside the repo (Cursor IDE default). The repo mirror under `3-Master_Plan/plans/` is canonical for version control.
- Do **not** commit `.specstory/debug/` or `.specstory/history/debug/` (SpecStory CLI diagnostics; may contain auth paths and session IDs).
- Include small tracked artifacts under `datasets/mbb/` per `datasets/mbb/README_TRACKED_ARTIFACTS.md`.
- Usually exclude `tier1_cell10_playground_state.json`, large sweep outputs, etc.

## PDF from markdown

- **Charles runs PDF conversion** (`./scripts/convert_single_md_to_pdf.sh …` or `./scripts/convert_multiple_md_to_pdf.sh 01_ 02_ …`) on his machine unless he explicitly asks COMPASS to run it in that message.
- COMPASS may edit `.md` and suggest CSS (e.g. `pdf_styles_narrow.css`); **do not** run convert scripts or regenerate `.pdf` files unprompted — agent-side Playwright/Chrome often mis-renders or crashes vs Charles’s local run.
- Do not aggressively condense, reframe as “decision memos,” or regenerate PDFs without explicit ask.

## External-facing documents (advisor briefs, etc.)

- COMPASS drafts **markdown**; **Charles approves content** before send.

## Cross-project planning agent — COMPASS

- **COMPASS** (formerly “Master Planner”) — scientific coherence, sequencing, near-term plan. Does not own domain code or manuscript prose.
- Canonical guidance: `3-Master_Plan/COMPASS_Initial_Guidance_v6.md`, identity note: `3-Master_Plan/COMPASS_AGENT_IDENTITY.md`.
- Agent handoffs: `3-Master_Plan/{CODA,SCOUT,PEER}_report_to_COMPASS.md`.
- Question files: `3-Master_Plan/YYYYMMDD_HHMM_COMPASS_to_{AGENT}_questions.md`.

## Conflicts

These files win unless the user overrides **in that message** (e.g. `skip burn`, `yes, skip rules for this`).
