# Education analysis workspace

**Created:** 2026-09-28  
**Last synced:** 2026-09-29  
**Current mission:** Resolve the bounded PD43 Romania origin-school feasibility gate. The proposed sequence is gymnasium experience → measured performance → selective high-school placement. Distinguish performance before selection from performance before the peer environment itself. Preserve earlier education work without resuming it automatically.

This folder isolates all new VECTOR education work from the original NELS:88 and HS&B:80 panels, the September 22 sandboxes, and the basketball assortativity investigation.

## Directory rules

- `docs/decisions/` — questions, specifications, stopping rules, and authorized choices.
- `docs/source_audit/` — construction, coding, provenance, and availability findings.
- `docs/collaboration/` — Scholar/VECTOR exchanges, including the Romania stopping decision and the completed bounded-search report. These are linked from this overview rather than copied into competing records.
- `docs/results/` — completed analytical results and their limits.
- `code/` — new education-only audit or analysis programs.
- `outputs/` — generated tables, figures, and machine-readable summaries.
- `handoffs/` — dated upload bundles and their explanatory notes; snapshots, not live execution instructions.

Original files under `datasets/nels88/`, `datasets/hsb80/`, and `3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/` are inputs or historical evidence. Do not overwrite them.

## Current stage

**Standalone Ministry archive feasibility checked, September 29.** Read [VECTOR's standalone feasibility report](docs/collaboration/VECTOR_Romania_Standalone_Ministry_Archive_Feasibility_20260929.md). The revised PD43 design ends at high-school/track assignment, so linkage to the anonymous replication files is secondary.

**Direct evidence:** The 2001 Alba candidate report family was recovered across all six pages (2,982 displayed positions). Within one explicitly coded origin school, all 78 candidate records correspond exactly to placement records, supplying separate exam and school-grade components plus destination. This establishes local feasibility, not national completeness. The CNP column is masked and unusable as a key.

**Other years:** Actual 2002 student tables were recovered, correcting the previous checkpoint, but inspected views lack separate score components. The inspected 2003 view lacks separate school grades and later-page retrieval remains incomplete. No complete national cohort is verified for any year.

**Measurement:** Recovered general admission rules specify 75% examination and 25% school grades in all three years. All 2,982 Alba 2001 rows match that calculation with truncation to two decimals. The paper's equal-weight description remains a discrepancy; a within-2001–2003 rule change is not supported by these sources.

**Recommended next decision:** A bounded 2001 Alba construction-and-completeness audit, before any substantive analysis. It would test complete origin-school applicant coverage, exact record correspondence, geography, and cross-county omissions. No further reconstruction is underway. A de-identified source request to the authors is an alternative; a replication crosswalk is optional.

The [earlier recovery report](docs/collaboration/VECTOR_Romania_Origin_School_Recovery_Findings_20260929.md) has a superseding notice. Its old linkage gate and author-first recommendation do not govern the current checkpoint. Scholar documents remain unchanged.

## Earlier Romania stopping decision — high-school-to-Baccalaureate design

The following decision and search report predate the PD43 upstream reframing. They remain valid historical records of why the earlier outcome pass was paused, not instructions to ignore the newly investigated gymnasium-to-high-school possibility.

**Romania outcome analysis is paused.** Start with [Scholar's stopping decision and reopening conditions](docs/collaboration/Scholar_EDUCATION_20260929_Romania_Stopping_Decision_and_Next_Search_Gate.md). Romania is retained for supporting literature and mechanism discussion. It passed the structural peer-pool audit, but we have not identified an observed scarce selection event after time in those peer environments. The pause is a decision about institutional fit, made before outcome analysis. It is not a failed empirical result.

**Scientific interpretation:** Improved academic outcomes can coexist with adverse relative-position and behavioral responses. This supports considering competing environmental channels. It does not separately estimate the benefits and drawbacks in $L=B-D$, prove that the adverse responses caused a performance penalty, or establish congestion without specifying the scarce resource or opportunity. Baccalaureate participation and grades do not record university admission or a fixed-quota downstream award. Artificially selecting the highest scorers would not supply that missing institutional event.

**Reopen only if:** A documented downstream scarce selection outcome becomes available and can be linked to these students, or a specific dissertation need justifies examining environmental development itself. Agree the revised scope and obtain explicit analytical execution authorization before resuming.

## Bounded downstream-selection search — report received

The [Scholar search document](docs/collaboration/Scholar_EDUCATION_20260929_Bounded_Downstream_Selection_Search.md) is a **completed search report**, not only prospective criteria. Scholar reports that no public ready-to-run candidate met the entire requirement in that search and recommends stopping further broad exploration. This does not establish that such data do not exist.

Its access statements, paper interpretations, candidate variables, and numerical examples remain **Scholar-reported findings pending independent verification**. This update did not repeat the external search.

The proposed next steps are:

1. Consider Rosenzweig and Xu's peers-as-educators-and-competitors paper as a focused mechanism-reading task.
2. Consider a limited Gates Millennium Scholars codebook feasibility check.
3. Retain selective-major admissions as a possible targeted institutional data request if the fourth-domain objective warrants it.

These are recommendations for Charles's next decision, not authorization to run analyses, download another dataset, contact data holders, or initiate restricted-use acquisition. Possible faculty-colleague access remains an option, with its precise availability unverified.

**Keep the search gate precise:** Prior performance should precede the peer environment wherever possible; exposure must occur before the scarce outcome. Identify both the peer pool and the competitive pool, even if they differ. Distinguish eligible students, applicants, offers, recipients, and accepted places when reporting $K/N$.

**Additional feasibility safeguard:** A school identifier alone does not establish a usable peer pool. A sample drawn from scholarship applicants or finalists may omit most classmates. Check the number, sampling, and prior-score coverage of peers, and whether performance was measured before the chosen environment. Do not equate a winners/non-winners survey sample with the complete national applicant pool.

## Romania work retained for reference

- **Direct schema evidence:** [September 28 gate report](docs/source_audit/EDUCATION_20260928_Romania_public_schema_gate_report.md). It records 334,137 student rows across the 2001–2003 admission cohorts, prior transition scores, nested town/school/school-track identifiers, and later Baccalaureate measures. Its recommendation to proceed to an analysis specification is historical; the stopping decision now governs.
- **Scientific proposals:** [Scholar's quantity-map proposal](docs/collaboration/Scholar_Romania_Scientific_Quantity_Map_Collaboration_20260929.md) and [VECTOR's response and proposed first pass](docs/collaboration/VECTOR_Romania_Scientific_Quantity_Map_Response_and_Proposed_First_Pass_20260929.md). Preserved, unexecuted; the first-pass recommendation is paused.
- **Upload snapshot:** [September 29 handoff](handoffs/EDUCATION_20260929_Romania_Scholar_VECTOR_handoff.md) and [ZIP bundle](handoffs/EDUCATION_20260929_Romania_Scholar_VECTOR_upload.zip). Created before the stopping decision; preserved without repackaging. They document the schema and earlier assessment, not the current next action.

No substantive Romania sorting calculation, outcome model, or figure has been produced. Existing data, audit code, and audit results remain preserved. The dated public-source directories are Git-ignored and covered by the existing education synchronization scope. No synchronization transfer has been executed in this work.

## Earlier education checkpoints — historical, not active instructions

**Initial external shortlist:** [Scholar shortlist and Trinidad feasibility review](docs/source_audit/EDUCATION_20260928_Scholar_shortlist_and_Trinidad_feasibility_review.md). This predates the stricter downstream-selection requirement. Earlier candidate rankings and statements about the immediate public-data path are historical.

**Candidate source gates:** [Education candidate-dataset gate and minimum restricted-data request](docs/source_audit/EDUCATION_20260928_candidate_dataset_gate_and_restricted_request.md). The ELS:2002 and HSLS:09 public-file peer-identifier limitations remain source findings. Their earlier priority for restricted access is not an approved current acquisition plan; any candidate must also meet the downstream-selection requirement.

**Performance-column decision:** Do not use or attempt to defend the supplied constructed performance column. Alex created it during the earlier data preparation and no longer has a reproducible construction recipe. Any new analysis must define a transparent performance measure directly from documented public-source variables. The earlier source-question document is retained as history; its broad construction request is no longer current.

**NELS audit:** [Source audit and then-proposed next step](docs/source_audit/EDUCATION_20260928_NELS_source_audit_and_next_step.md). The audit ran in `sports_net` and preserved the original input. Its old source-request and next-step language does not override the current decision.

**Initial mission plan:** [September 28 mission and source-audit plan](docs/decisions/EDUCATION_20260928_mission_and_source_audit_plan.md) preserves the earlier scope. It is not a standing instruction to execute work now.

**Current authorization boundary:** The authorized standalone archive feasibility check is complete. Wait for Charles's direction before outreach, expanded cohort reconstruction, or substantive analysis. Do not duplicate Scholar VECTOR's completed broad search. Older proposed actions above remain historical.
