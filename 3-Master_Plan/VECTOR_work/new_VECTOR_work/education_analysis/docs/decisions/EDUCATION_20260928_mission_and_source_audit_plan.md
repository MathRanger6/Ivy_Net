# Education mission and source audit plan

**Date:** 2026-09-28  
**Status:** Authorized by Charles.  
**Scope:** Existing-data audit first; no request for additional data yet.

## 1. Current scientific objective

Determine what the supplied National Education Longitudinal Study of 1988 (NELS:88) and High School and Beyond 1980 (HS&B:80) panels can establish about:

1. Sorting into high-school peer environments.
2. A student's standing within the sampled high-school peer group.
3. Entry into postsecondary education.
4. Bachelor’s-degree completion by the observed follow-up.

The first substantive comparison, if the source audit passes, will ask whether local school standing and school-peer quality relate differently to postsecondary entry and later completion among students with comparable prior measured performance and declared baseline background characteristics.

## 2. Why the audit comes first

The panels were supplied as constructed files. The repository does not currently contain the raw National Center for Education Statistics files, the complete codebooks, or the extraction and recoding program that produced every supplied column. Before interpreting a transition, we must establish:

- Which source codes became zero, one, or missing in each binary outcome.
- Whether bachelor’s completion is nested within postsecondary entry in every observed row.
- Which students enter each analytic flag and why.
- Whether the peer counts and leave-one-out peer means agree with the recorded school cells.
- How baseline performance was standardized.
- Whether weights are present, positive, and appropriate for the intended estimate.
- Which survey-design variables needed for uncertainty are absent.

Internal consistency cannot replace the original codebook, but it can identify what is safe to analyze and what still requires source documentation.

## 3. Bounded audit sequence

### Stage A — repository provenance

1. Inventory the supplied panels, source emails, construction code, codebooks, and saved September 22 artifacts.
2. Search for the original extraction recipe and source-variable documentation.
3. Record missing provenance explicitly rather than reconstructing it from memory.

### Stage B — NELS internal construction audit

1. Confirm row count, student-identifier uniqueness, school-cell counts, and analytic-population counts.
2. Tabulate original degree and high-school-completion codes against the supplied binary outcomes and `outcome_observed`.
3. Test the nesting of high-school completion, any postsecondary entry, associate-or-higher, and bachelor-or-higher.
4. Audit missingness and positivity of the follow-up weight.
5. Test `unit_n`, `peer_n`, analytic flags, and leave-one-out peer-mean identities against the supplied school cells.
6. Describe how closely `own_performance_z` behaves like a single fixed standardization of `own_performance_raw` without assuming the undocumented reference population.

### Stage C — availability review

Verify the earlier augmentation research against official National Center for Education Statistics documentation:

1. College destination identifiers and postsecondary transcript records.
2. Historical Barron’s admissions-competitiveness linkage.
3. Applications and admission decisions, including the limit on reported institutions.
4. Transcript class rank and graduating-class size.
5. HS&B follow-up timing and comparable fields.
6. Public-use versus restricted-use status and the documentation or access conditions required.

### Stage D — decision gate

Proceed to a substantive NELS transition comparison only if:

1. The outcome hierarchy is internally coherent.
2. The analytic population can be reproduced from supplied fields.
3. The peer measures pass their recorded construction identities or discrepancies are understood.
4. The weight and uncertainty limitations are documented.
5. The outcome question is stated without treating enrollment, admission, and completion as interchangeable.

## 4. Stopping rules

- Do not change outcome definitions, peer measures, ability measures, covariates, bins, or sample thresholds successively to obtain a downturn.
- Do not interpret a positive or null relationship as evidence that all congestion mechanisms are absent.
- Do not interpret a negative standing association as proof of a fixed admissions quota or causal congestion.
- Do not request additional data merely because the existing result is monotonic.
- Request augmentation only for a named question the existing fields cannot answer.

## 5. Augmentation justification standard

Every requested field must be presented as:

1. **Existing limitation:** the precise ambiguity in the supplied panels.
2. **Requested field:** the variable and documentation needed.
3. **Enabled distinction:** the claims or transitions that become distinguishable.
4. **Remaining limitation:** what the requested field still would not establish.

Example: a first-college identifier plus historically appropriate selectivity would distinguish broad postsecondary entry from entry into a more selective destination. It would not, by itself, identify the causal effect of high-school peers or competition among students after college entry.

## 6. Protected artifacts

Do not modify or overwrite:

- `datasets/nels88/nels88_big_fish_panel.csv`
- `datasets/hsb80/hsb80_big_fish_panel.csv`
- `3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/`
- `scripts/big_fish_data_story.py`

All new files belong under `3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/`.
