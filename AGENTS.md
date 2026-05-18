# Agent instructions — read before editing this repository

**These are binding project rules, not suggestions.**

## Always-on rules

1. **`.cursor/rules/notebook-blank-edit.mdc`** — `alwaysApply: true`.  
   **Every** Agent run that might touch a Jupyter notebook must follow it **verbatim**: burn-slot first, **at most one substantive `EditNotebook` per assistant reply per `.ipynb`** (unless the user explicitly waives batching in chat), no raw JSON notebook patching for cell bodies, no `notebook_edit_cell` for content.

2. **`.cursor/rules/incremental-writes.mdc`** — `alwaysApply: true`.  
   Loops over network/large I/O must append + flush each iteration and resume-skip when applicable.

3. **`.cursor/rules/jupyter-notebook-workflow.mdc`** — Applies when editing `**/*.ipynb` (globs); **`540_tenure_pipeline.ipynb`** uses burn cell **index 3** and the same-cell “one `EditNotebook` per cell per pass” merge rule. It **reinforces** `notebook-blank-edit.mdc` and explains **why** review visibility matters.

## Before you edit `.ipynb` files

1. Open and follow **`notebook-blank-edit.mdc`** (it is injected, but **read** it when planning notebook work).
2. Plan **one** substantive cell change per user message (after burn), or ask for **explicit** batch permission.
3. Announce **"Blank edit done — Cell 1 updated."** (or EDIT BLANK for 540) after the burn edit succeeds.

## If instructions in chat conflict with these files

**These files win** unless the user explicitly overrides *in writing* for a specific task (e.g. “batch all header cells this once”).
