# ASSORT — Assortativity Investigation Workspace

**Created:** 2026-09-25

This folder contains newly created documentation, code, notebooks, derived data, outputs, and provenance records for the assortativity investigation.

## Scope

The investigation concerns the interaction among assortative assignment, congestion, and selection scarcity. The scientific brief provides the broader research rationale. The [detailed experiment decision record](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_experiment_choices_and_rationale.md>) records Charles's subsequent choices, detailed explanations, and questions still open. Read both before proposing implementation; accepted design choices are distinct from execution authorization.

## Documentation style

**Execution stop (September 25):** The first authorized construction attempt exposed [two source-data decisions](docs/source_review/ASSORT_20260925_initial_execution_stop.md). The experiment has not run. Keep this stop report with the decision record and construction specification until Charles settles the questions.

**Construction checkpoint (September 25):** The design and reporting decisions are settled. Read the [construction specification and source audit](docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md) for the implementation plan, code compatibility findings, and checks pending authorized construction. No analytical code or experiment has been executed for this investigation.

**Current reading checkpoint:** read the [data hygiene and model-history review](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_data_hygiene_and_model_history.md>) and companion [questions for SCOUT](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_questions_for_SCOUT.md>) before freezing the input population. Charles's one-game-opponent explanation prompted this review. The accepted 2015 season and experiment settings remain recorded; exact eligible rosters and filters are provisional. Existing generated outputs are historical evidence, not inputs or resumed runs for the new investigation.

Charles welcomes detailed explanations and brief examples. Unless Charles has himself used a shorthand expression, write the full term followed by the proposed shorthand in parentheses, and continue doing so until he uses that shorthand. Explain symbols in ordinary language. Ask one necessary design question at a time.

## Folder rules

- General Markdown belongs in `docs/`.
- New analysis code belongs in `code/`.
- New notebooks belong in `notebooks/`.
- Derived data and input manifests belong in `data/`.
- Tables, figures, and diagnostics belong in `outputs/`.
- Execution and provenance records belong in `docs/run_records/`.
- Superseded material belongs in `archive/`.

Existing source code, source data, historical outputs, and authoritative repository documents remain in their original locations. This workspace may link to those sources but does not silently replace them.

## Naming

Use the `ASSORT_YYYYMMDD_` prefix and a version suffix where needed. Related code, notebooks, outputs, and run records should share a common stem. Avoid ambiguous names such as `final.py`, `results.csv`, or `new_notebook.ipynb`.

## Evidence and execution status

Label artifacts as one of:

`proposed` · `authorized` · `executed` · `verified` · `superseded`

Every executed analysis must have a run record identifying the code, inputs, parameters, outputs, date, and verification status. Creating files here does not authorize execution of experiments or modification of existing repository research artifacts.

## Initial state

The folder structure was created on September 25, 2026. No analysis code, notebook, data file, figure, table, or experiment has been created yet.
