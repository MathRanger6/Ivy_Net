# Romania 2001: 22-county descriptive pilot

This run combines the previously verified county-wide placement pipeline with the newer school-specific admitted/rejected-result pipeline. Printed name and admission score are provisional linkage keys because the archival ID is masked. The observed peer pool includes admission-round applicants, not all eighth graders.

Program rankings and outcome settings are recorded in `run_manifest.json`. Top one and top two are separate cumulative cutoff tiers. An admitted student is successful only when their actual local program belongs to the designated tier. Outside-county placements are excluded from the outcome denominator but retained as gymnasium peers; confirmed unassigned applicants remain in the denominator.

## County results

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |
|---|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,953 | 100 | 3.39 | 1 | 100 |
| AB | 2 | 3,041 | 2,953 | 125 | 4.23 | 2 | 125 |
| CS | 1 | 2,606 | 2,454 | 50 | 2.04 | 1 | 50 |
| CS | 2 | 2,606 | 2,454 | 75 | 3.06 | 2 | 75 |
| GL | 1 | 5,345 | 5,260 | 74 | 1.41 | 1 | 75 |
| GL | 2 | 5,345 | 5,260 | 198 | 3.76 | 2 | 200 |
| TL | 1 | 1,953 | 1,799 | 100 | 5.56 | 1 | 100 |
| TL | 2 | 1,953 | 1,799 | 175 | 9.73 | 2 | 175 |
| AR | 1 | 3,164 | 3,115 | 50 | 1.61 | 1 | 50 |
| AR | 2 | 3,164 | 3,115 | 99 | 3.18 | 2 | 100 |
| SB | 1 | 3,236 | 3,185 | 48 | 1.51 | 1 | 50 |
| SB | 2 | 3,236 | 3,185 | 68 | 2.14 | 2 | 75 |
| B | 1 | 22,216 | 22,157 | 189 | 0.85 | 1 | 200 |
| B | 2 | 22,216 | 22,157 | 385 | 1.74 | 2 | 400 |
| CT | 1 | 6,507 | 6,453 | 50 | 0.77 | 1 | 50 |
| CT | 2 | 6,507 | 6,453 | 148 | 2.29 | 2 | 150 |
| PH | 1 | 6,131 | 6,071 | 100 | 1.65 | 1 | 100 |
| PH | 2 | 6,131 | 6,071 | 148 | 2.44 | 2 | 150 |
| TM | 1 | 5,795 | 5,773 | 119 | 2.06 | 1 | 125 |
| TM | 2 | 5,795 | 5,773 | 165 | 2.86 | 2 | 175 |
| CJ | 1 | 4,885 | 4,827 | 73 | 1.51 | 1 | 75 |
| CJ | 2 | 4,885 | 4,827 | 123 | 2.55 | 2 | 125 |
| AG | 1 | 6,458 | 6,404 | 144 | 2.25 | 1 | 150 |
| AG | 2 | 6,458 | 6,404 | 192 | 3.00 | 2 | 200 |
| BR | 1 | 2,658 | 2,584 | 99 | 3.83 | 1 | 100 |
| BR | 2 | 2,658 | 2,584 | 174 | 6.73 | 2 | 175 |
| BT | 1 | 3,870 | 3,757 | 100 | 2.66 | 1 | 100 |
| BT | 2 | 3,870 | 3,757 | 200 | 5.32 | 2 | 200 |
| BV | 1 | 4,886 | 4,808 | 48 | 1.00 | 1 | 50 |
| BV | 2 | 4,886 | 4,808 | 97 | 2.02 | 2 | 100 |
| DB | 1 | 3,907 | 3,665 | 99 | 2.70 | 1 | 100 |
| DB | 2 | 3,907 | 3,665 | 198 | 5.40 | 2 | 200 |
| DJ | 1 | 5,579 | 5,518 | 194 | 3.52 | 2 | 200 |
| DJ | 2 | 5,579 | 5,518 | 242 | 4.39 | 3 | 250 |
| GJ | 1 | 3,930 | 3,694 | 100 | 2.71 | 1 | 100 |
| GJ | 2 | 3,930 | 3,694 | 225 | 6.09 | 2 | 225 |
| IL | 1 | 2,546 | 2,449 | 100 | 4.08 | 1 | 100 |
| IL | 2 | 2,546 | 2,449 | 175 | 7.15 | 2 | 175 |
| OT | 1 | 4,724 | 4,372 | 123 | 2.81 | 1 | 125 |
| OT | 2 | 4,724 | 4,372 | 148 | 3.39 | 2 | 150 |
| VL | 1 | 4,110 | 4,013 | 75 | 1.87 | 1 | 75 |
| VL | 2 | 4,110 | 4,013 | 125 | 3.11 | 2 | 125 |
| VN | 1 | 3,338 | 3,237 | 99 | 3.06 | 1 | 100 |
| VN | 2 | 3,338 | 3,237 | 149 | 4.60 | 2 | 150 |

Each plot point or bar has its applicant and gymnasium support recorded in the corresponding aggregate bin CSV. The applicant-weighted pooled plots compute a single rate over all applicants in each common peer-score bin. The equal-county pooled plots first compute one rate per represented county within each peer-score bin (and own-score band), then average those county rates equally. A county with no eligible applicants in a cell is absent, not assigned zero; the number of contributing counties is printed on the plot. Thus even equal-county curves can change composition across bins. The separate gymnasium-mean plot uses each observed gymnasium with at least two applicants once to set common peer-score quantile bins. All eligible students in that gymnasium inherit its bin; the colored own-score bands use pooled percentiles across the selected counties. Success rates within those cells weight eligible applicants equally. The matching equal-width plot changes only how the common gymnasium-mean bins are cut: equal score intervals replace equal-count gymnasium quantiles. Empty equal-width intervals remain visible as gaps. These are descriptive associations, not estimates of a causal peer or congestion effect. No applicant preferences are observed; the success fraction is not institutional K/N.

The new-county source gate had zero unresolved top-one/top-two labels. Galați retains its documented one-applicant outcome uncertainty. This is a selected-county descriptive comparison, not a 41-county national analysis. No individual-level output was exported.
