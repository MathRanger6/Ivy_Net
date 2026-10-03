# Romania 2001: four-county gymnasium source reconciliation

## What we compared

This is an **offline audit of saved Romanian Ministry admission webpages** for Alba (AB), Caraș-Severin (CS), Galați (GL), and Tulcea (TL). No webpages were requested during this run, and no HERO or peer-effect analysis was performed.

- **Gymnasium Applicant View:** a webpage listing the admission-round applicants from one originating gymnasium. We verified all 632 such pages listed in the four counties' origin-school directories, containing 12,945 applicant rows. These are participating applicants, not necessarily every eighth grader at each school.
- **County Applicant View:** a county-wide webpage listing admission-round applicants. We checked whether each gymnasium row appears in its own county's list or another county's saved list.
- **Placement and Unassigned Views:** Ministry webpages recording either a high-school/program placement or an unassigned applicant in the admission round. We checked these saved views across all 41 county report sets.

## What the saved sources show

Of 12,945 gymnasium applicant rows, 12,486 matched the County Applicant View in the same county and 297 matched in another county. 162 did not appear in the saved county applicant views; 161 of those nevertheless had one placement or unassigned report row. Thus, absence from a county applicant list is not evidence that the person did not participate or obtain a place.

The Placement and Unassigned Views contain one matching report row for 12,944 of the 12,945 gymnasium rows. The remaining 1 row remains **unresolved**; it must not be coded as an unsuccessful placement.

The archived `CNP` identifier is masked and cannot identify a student. A printed name plus admission score is only a provisional match; for the applicant-list comparison we also required the examination score and grades 5–8 average to agree. We exported only county counts, never names or individual scores.

| County | Gymnasium rows | Exact in own county applicant list | Exact in another county | Not in saved county applicant lists | One placement-report row | One unassigned-report row | Outcome ambiguous | Outcome not located |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AB | 3,041 | 2,963 | 55 | 23 | 3,035 | 6 | 0 | 0 |
| CS | 2,606 | 2,457 | 58 | 91 | 2,460 | 146 | 0 | 0 |
| GL | 5,345 | 5,263 | 68 | 14 | 5,149 | 195 | 0 | 1 |
| TL | 1,953 | 1,803 | 116 | 34 | 1,935 | 18 | 0 | 0 |

The four counties' own County Applicant and Unassigned webpage series were complete in the saved archive. Their placement sources were also complete: AB and TL through the original county webpages, CS and GL through the recovered program webpages. Some other counties' saved report series are incomplete. Duplicate rows shared by original and recovered placement views were counted only once.

## What remains unresolved

A complete admission-round webpage series does **not** establish that every eighth grader from a gymnasium applied in this round. Name-and-score agreement does not prove unique identity. The one school row with no saved outcome report is on Galați originating-gymnasium page 186. A targeted offline search found no row with the same printed name in the saved county applicant, placement, or unassigned reports. Its status stays unresolved; a missing row is not evidence of nonplacement.

We should not build a HERO curve or infer congestion from these counts. First we must decide whether the participating-applicant gymnasium group is the defensible peer group, and verify the selective-program outcome definition and its denominator.

The companion CSV gives every county count and source-status flag. It contains no student-level information.
