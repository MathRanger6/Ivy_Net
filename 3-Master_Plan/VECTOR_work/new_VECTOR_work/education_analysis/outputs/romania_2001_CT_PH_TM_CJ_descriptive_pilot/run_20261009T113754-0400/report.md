# Romania 2001: CT, PH, TM, CJ descriptive pilot

This run uses complete originating-gymnasium applicant reports and the matching admitted/rejected school-result reports. Printed name and admission score are provisional linkage keys because the archival ID is masked. The observed peer pool includes admission-round applicants, not all eighth graders.

Program rankings and outcome settings are recorded in `run_manifest.json`. Top one and top two are separate cumulative cutoff tiers. An admitted student is successful only when their actual local program belongs to the designated tier. Outside-county placements are excluded from the outcome denominator but retained as gymnasium peers; confirmed unassigned applicants remain in the denominator.

## County results

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |
|---|---:|---:|---:|---:|---:|---:|---:|
| CT | 1 | 6,507 | 6,453 | 321 | 4.97 | 6 | 325 |
| CT | 2 | 6,507 | 6,453 | 764 | 11.84 | 12 | 775 |
| PH | 1 | 6,131 | 6,071 | 422 | 6.95 | 6 | 425 |
| PH | 2 | 6,131 | 6,071 | 716 | 11.79 | 12 | 725 |
| TM | 1 | 5,795 | 5,773 | 487 | 8.44 | 7 | 500 |
| TM | 2 | 5,795 | 5,773 | 846 | 14.65 | 13 | 875 |
| CJ | 1 | 4,885 | 4,827 | 292 | 6.05 | 5 | 300 |
| CJ | 2 | 4,885 | 4,827 | 510 | 10.57 | 10 | 525 |

Each plot point or bar has its applicant and gymnasium support recorded in the corresponding aggregate bin CSV. Pooled curves weight applicants, so county composition can change across bins. These are descriptive associations, not estimates of a causal peer or congestion effect. No applicant preferences are observed; the success fraction is not institutional K/N.

The source gate had zero unresolved top-one/top-two labels in all four counties. No national outcome analysis was run, and no individual-level output was exported.
