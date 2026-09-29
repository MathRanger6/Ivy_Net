# Education analysis workspace

**Created:** 2026-09-28  
**Mission:** Qualify education datasets quickly, preserve provenance, and use only candidates that contain a defensible peer pool, prior performance, and later transition outcome.

This folder isolates all new VECTOR education work from the original NELS:88 and HS&B:80 panels, the September 22 sandboxes, and the basketball assortativity investigation.

## Directory rules

- `docs/decisions/` — questions, specifications, stopping rules, and authorized choices.
- `docs/source_audit/` — construction, coding, provenance, and availability findings.
- `docs/results/` — completed analytical results and their limits.
- `code/` — new education-only audit or analysis programs.
- `outputs/` — generated tables, figures, and machine-readable summaries.

Original files under `datasets/nels88/`, `datasets/hsb80/`, and `3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/` are inputs or historical evidence. Do not overwrite them.

## Current stage

**Romania public-file gate passed:** Read the [Romania public schema gate report](docs/source_audit/EDUCATION_20260928_Romania_public_schema_gate_report.md). The authenticated public archive preserves 334,137 student rows across the 2001–2003 admission cohorts, complete pre-assignment transition scores, nested town/school/school-track identifiers, and later Baccalaureate participation and grades. The school-track identifiers pass the nesting test and usually contain substantial peer groups. The external dataset search stops here: do not move to Chicago, Kenya, or restricted-data acquisition for the immediate investigation. No substantive analysis is authorized by this pass; the next stage is a bounded specification reviewed with Charles.

**External shortlist completed September 28:** Read [Scholar shortlist and Trinidad feasibility review](docs/source_audit/EDUCATION_20260928_Scholar_shortlist_and_Trinidad_feasibility_review.md). Trinidad and Tobago is the strongest conceptual and identification match, but its core records are confidential and the posted instructions warn that access may take about six months. Preserve it as a literature and possible future-data lead; do not allow it to displace the immediate public NELS:88 and HS&B:80 path.

**Candidate gate completed September 28:** Read [Education candidate-dataset gate and minimum restricted-data request](docs/source_audit/EDUCATION_20260928_candidate_dataset_gate_and_restricted_request.md) first. Official ELS:2002 and HSLS:09 public packages were downloaded and audited. Both contain strong transition outcomes but suppress the common student-to-school identifier in every public student record, so neither advanced to the peer-pool mosaic. They remain high-priority restricted-use candidates. NELS:88 and HS&B:80 remain the immediate public peer-pool datasets. Project Talent is parked as a secondary request candidate.

The dated public-source directories are Git-ignored and covered by `./scripts/pull_big_data.sh ... education`. No rsync transfer has been executed. No substantive education model has been fitted.

**Performance-column decision:** Do not use or attempt to defend the supplied constructed performance column. Alex created it during the earlier data preparation and no longer has a reproducible construction recipe. Any new analysis must define a transparent performance measure directly from documented public-source variables. The earlier source-question document is retained as history; its broad construction request is no longer current.

**Completed September 28:** [NELS source audit and next step](docs/source_audit/EDUCATION_20260928_NELS_source_audit_and_next_step.md). Start here for findings and the short source-clarification request. The audit code ran in `sports_net`; the original CSV is unchanged. Internal checks largely pass; source-variable mapping remains incomplete, so substantive transition fitting has not begun.

Read and execute the bounded plan in [`docs/decisions/EDUCATION_20260928_mission_and_source_audit_plan.md`](docs/decisions/EDUCATION_20260928_mission_and_source_audit_plan.md).

No substantive model is authorized until the source audit establishes how the supplied variables were constructed and whether the declared outcomes are internally consistent.
