# Education analysis workspace

**Created:** 2026-09-28  
**Mission:** Audit and use the existing education panels before requesting additional data.

This folder isolates all new VECTOR education work from the original NELS:88 and HS&B:80 panels, the September 22 sandboxes, and the basketball assortativity investigation.

## Directory rules

- `docs/decisions/` — questions, specifications, stopping rules, and authorized choices.
- `docs/source_audit/` — construction, coding, provenance, and availability findings.
- `docs/results/` — completed analytical results and their limits.
- `code/` — new education-only audit or analysis programs.
- `outputs/` — generated tables, figures, and machine-readable summaries.

Original files under `datasets/nels88/`, `datasets/hsb80/`, and `3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/` are inputs or historical evidence. Do not overwrite them.

## Current stage

**Remaining source request:** Official survey documentation answers the general questions about sample design, waves, tests, attainment categories, and weights. Use [One unresolved construction question for the education panels](docs/source_audit/EDUCATION_20260928_Questions_for_Source_All_Three_Groups.md) only to learn whether the supplied columns were locally created or transformed and, if so, obtain the construction code or variable mapping. No message has been sent; no new model or sample definition has been adopted.

**Completed September 28:** [NELS source audit and next step](docs/source_audit/EDUCATION_20260928_NELS_source_audit_and_next_step.md). Start here for findings and the short source-clarification request. The audit code ran in `sports_net`; the original CSV is unchanged. Internal checks largely pass; source-variable mapping remains incomplete, so substantive transition fitting has not begun.

Read and execute the bounded plan in [`docs/decisions/EDUCATION_20260928_mission_and_source_audit_plan.md`](docs/decisions/EDUCATION_20260928_mission_and_source_audit_plan.md).

No substantive model is authorized until the source audit establishes how the supplied variables were constructed and whether the declared outcomes are internally consistent.
