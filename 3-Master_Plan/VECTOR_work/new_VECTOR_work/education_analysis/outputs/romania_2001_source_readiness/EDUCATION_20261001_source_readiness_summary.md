# Romania 2001 offline county source readiness

This is a source inventory, not a national outcome analysis or a list of counties approved for HERO curves. It reads only saved private checkpoints. No student names or individual scores are exported.

Counties inspected: **41**. Placement views available to occupancy total: **41**. Candidate page families complete: **22**. Unassigned page families complete: **40**.

## What we have, and what is still missing

Each county has three lists to compare: (1) people who applied, (2) people placed in a program, and (3) people left without a placement. A school directory is a fourth list used to identify each applicant's originating gymnasium. Here, a 'complete' list means its expected archived report pages were saved; it does not yet establish that the list includes every child who attended a gymnasium. The two-letter labels below are county abbreviations (for example, AB means Alba and B means Bucharest).

- **All three applicant/placement report sets are present in 22 counties:** AB, AR, BC, BR, BT, BZ, CL, CS, CV, DB, GJ, GL, GR, HR, IL, MH, OT, SB, SJ, TL, VL, VN. The next check for these counties is whether the gymnasium name printed beside each applicant can be matched reliably to one school in the directory. We must also review the provisional person match between the applicant and outcome lists. Having all three lists does not yet make a county ready for a HERO curve.
- **The applicant list still has missing archived pages in 19 counties:** AG, BH, BN, BV, CJ, CT, DJ, HD, IS, MM, MS, NT, PH, SM, SV, TM, TR, VS, B. We can read the applicant pages already saved, but cannot yet say we have the full participating applicant list for those counties. The immediate source task is to recover or account for those pages.
- **The unassigned-applicant list still has missing pages in 1 counties:** B. A person absent from the placement list is not automatically an unsuccessful applicant; the missing list must be checked too.
- **The placement reports are still unresolved in 0 counties:** none. Until those reports are accounted for, some applicants' destinations may be absent.

These are overlapping descriptions, not four separate sets of counties. A county can appear in more than one missing-page line. The four-way 'next task' field in the detailed CSV records only the first issue the script encountered, so use the separate completeness columns to see every open issue.

## What this check means for the study

For counties with all three report sets, the saved applicant names and admission scores could be matched one-to-one to a saved placement or unassigned record within that county. This is an encouraging consistency check, not proof of a unique national student identifier or complete gymnasium peer groups. Next, verify school-name-to-directory-code mapping and the meaning of the applicant population before producing outcome curves.

## Interpretation limits

- A complete archived applicant report covers that report's participating applicants; it does not prove that every eighth grader at each gymnasium participated.
- The candidate roster contains school labels, while the directory contains school codes. This audit does not equate them or certify complete origin-school groups.
- Name plus admission score is only a provisional within-county comparison. An unmatched candidate may have a cross-county outcome or a missing report. Never count it as unsuccessful by default.
- Recovered placement reports are used only when the existing placement worker marked the county reconciled and saved report hashes and row counts still verify.
- The CSV contains name-free aggregates. The private source pages remain on the Desktop. A researcher must review the source gates and authorize any national outcome analysis.

Detailed name-free counts are in `EDUCATION_20261001_county_source_readiness.csv`.
