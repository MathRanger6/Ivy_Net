# Start here

This folder is the handoff for the LG exploration project, prepared 6 October 2026.

1. Read `documents/LG_Model_Exploration_Executive_Summary.docx` for the one-page scientific overview.
2. Read `documents/LG_Model_Exploration_for_Alex.docx` for Charles’s six-page specification with editable Word equations.
3. Read `documents/LG_Model_Exploration_Agent_Handoff.md` for agreed decisions, implementation findings, and open questions.
4. Inspect `reference_snapshot/` for original source copies. `reference_snapshot/SOURCE_MANIFEST.json` records their original repository paths and hashes.

## Model distinction

LG combines metadata-based attachment preference with fixed prescribed roster sizes. Relaxing those sizes is a distinct exploratory model. Neither uses degree-based attraction. Preserve this distinction in filenames, settings, plots, and prose.

## Folder ownership and isolation

Charles will give the new agent access ONLY to this folder. Treat it as the project root; broader repository access is neither expected nor required. Leave the original sports code, Romania code, dissertation chapter, and other project work unchanged. Keep `reference_snapshot/` as an untouched reference copy. Create adapted working copies in `code/`, notebooks in `notebooks/`, and portable configurations in `settings/`.

These working directories are intentionally empty. This is a DOCUMENTED SOURCE HANDOFF, not yet a runnable, dependency-isolated implementation. Copied legacy scripts retain their original import paths and output conventions. Do not execute them in place: some can resolve paths into existing work or try to load empirical data.

If a required supporting file is absent, report its exact filename/import name, which supplied file needs it, and why. Charles and NVector will supply a copy here. Do not search outside this folder or request full-repository visibility as a prerequisite. Record supplied dependencies and their provenance, and continue independent work while waiting. Historical repository paths in the handoff and manifest identify source provenance; locate the included copies under `reference_snapshot/`.

Before execution, resolve supporting dependencies into the working project, replace legacy path assumptions with explicit project-local/configurable paths, and verify that imports and output destinations stay within the intended project/environment. Third-party libraries may use the existing sports_net environment. No need to copy Python itself or unrelated datasets.

Use Git for code/configuration and rsync for bulk checkpoints/results. Before larger runs, add an appropriate synchronization scope and validate ignore behavior. A local .gitignore provisionally excludes generated output directories and notebook checkpoints. This handoff does not submit jobs or authorize broad sweeps.

Charles controls running notebooks and jobs. Keep visible settings and generous comments. Ask scientific questions one at a time. The notebook editing rule is waived until further notice except the explicitly identified Army manual-transcription context.
