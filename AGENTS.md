# Agent instructions — read before editing this repository

**Binding project rules, not suggestions.**

## Always-on

1. **`.cursor/rules/notebook-blank-edit.mdc`** — Notebook **prime directive:** every `.ipynb` change in a reply should be **line/cluster red/green** reviewable. Each **user message**: usually **burn** first (`skip burn` if user says so), then substantive edits; **ask** when unsure; **`EditNotebook`** for cell bodies (no MCP `notebook_edit_cell` / raw JSON unless user says **`yes, skip rules for this`**). No cap on cells per reply.
2. **`.cursor/rules/incremental-writes.mdc`** — Network/large I/O loops: append + flush + resume-skip.
3. **`.cursor/rules/jupyter-notebook-workflow.mdc`** — `540_tenure_pipeline.ipynb`: burn at **cell index 3**; same-cell merge rule.

## Notebooks

- Follow **`notebook-blank-edit.mdc`** before any cell-body edit.
- If review UI fails: **ask** the user — do not plow ahead.
- New notebook scaffold via MCP: **ask first**.

## Git commits (when the user asks)

- Include `.specstory/history/` unless they say otherwise.
- Include small tracked artifacts under `datasets/mbb/` per `datasets/mbb/README_TRACKED_ARTIFACTS.md`.
- Usually exclude `tier1_cell10_playground_state.json`, large sweep outputs, etc.

## Conflicts

These files win unless the user overrides **in that message** (e.g. `skip burn`, `yes, skip rules for this`).
