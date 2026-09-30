# Alba 2001: quick cross-county check before defining HERO success

**Date:** September 30, 2026.  
**Purpose:** Charles asked whether community changes affect enough applicants to warrant additional work before the first HERO. This was a local read-only check of saved source reports and audit records. No archive requests, placement model, filtering change, or HERO execution occurred.

## What could be checked quickly

The temporary Desktop cache contains all 168 originating-school candidate reports. It includes examination scores and a `Judeţ` county field, but no destination school or destination town. The permanent score file also lacks placement. Thus a complete same-town / other-town-within-Alba / other-county classification cannot be produced from the saved individual records alone.

Across the cache, 2,963 records have `Judeţ = ALBA` and 78 have another county value. For every originating-school code, the number of non-Alba records equals the earlier audit's count of additional names absent from the Alba county candidate list. This is an aggregate correspondence check; the old placement audit did not persist the individual placement-to-score link.

The saved additional-placement descriptions account for all 78: 77 show an institution outside Alba, and one is marked unassigned. Therefore **77 / 3,041 = approximately 2.53%** are confirmed out-of-county placement records. Earlier shorthand calling all 78 cross-county placements should be corrected. These are educational placements, not evidence of residential moves.

## Examination scores of the 78 non-Alba-county records

The comparison below includes the one unassigned case because its individual score cannot be distinguished from the 77 placed cases using the preserved aggregate placement results alone.

- Non-Alba county group: 78 records; mean examination score 6.6836; median 6.66; range 5.05–9.06.
- Alba county group: 2,963 records; mean 7.1028; median 6.98; range 5.00–9.86.
- The full-population 90th-percentile examination score is 8.80, using linear interpolation. Including all ties, 315 records meet or exceed that score.
- Two of the 78 non-Alba records meet or exceed 8.80 (2.56% of that group), compared with 313 of 2,963 Alba records (10.56%).

This group is not concentrated at the very highest examination scores, although it contains some high scorers. The top-decile check is a descriptive reference, not a newly chosen eligibility rule or a definition of the band of excellence. A score may be competitive for one program but not another. These figures do not establish the score distribution of students crossing towns within Alba.

## Recommendation and limits

Do not expand into reconstructing family moves or transfer motives. Retain these applicants in the source dataset and in their originating-gymnasium peer calculations. When attaching placement and defining program selectivity, report any destination whose rank remains unavailable as unknown; do not count an unresolved rank as a failed placement.

If ranking outside-Alba destinations becomes disproportionate, a first HERO restricted to observed Alba destinations is a possible explicitly limited scope, to be agreed before plotting. Such a restriction changes the population and may be selective. It should not remove excluded focal applicants from the gymnasium peer averages, and should not be chosen or revised to obtain a preferred curve. No such restriction was applied in this check.

## Source trail and calculation

- Temporary individual source: `~/Desktop/VECTOR_temp/romania_alba_2001_differentiation_v1/school_reports/school_*.json`, fields `source_code`, `rows[].Judeţ`, and `rows[].Medie Capacitate`. Names were neither displayed nor copied into this note.
- Saved placement evidence: `education_analysis/outputs/romania_alba_2001_structural_audit_20260929/origin_report_checks.jsonl`, using the last record for each source code and its `extra_placement_descriptions` and `candidate_extra_to_county` fields.
- Population and prior analysis: `education_analysis/outputs/romania_alba_2001_differentiation_v1/EDUCATION_20260929_romania_gymnasium_differentiation_v1_summary.json`.
- Computation: local Python standard-library JSON reads, grouping by whether `Judeţ` equals `ALBA`, arithmetic means and medians, and `statistics.quantiles(all_scores, n=10, method="inclusive")[-1]`. All ties at the threshold were included. No research output files were overwritten.
