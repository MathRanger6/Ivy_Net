# Romania 2001: 22-county descriptive pilot

This run combines the previously verified county-wide placement pipeline with the newer school-specific admitted/rejected-result pipeline. Printed name and admission score are provisional linkage keys because the archival ID is masked. The observed peer pool includes admission-round applicants, not all eighth graders.

Program rankings and outcome settings are recorded in `run_manifest.json`. Top one and top two are separate cumulative cutoff tiers. An admitted student is successful only when their actual local program belongs to the designated tier. Outside-county placements are excluded from the outcome denominator but retained as gymnasium peers; confirmed unassigned applicants remain in the denominator.

## County results

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |
|---|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,733 | 100 | 3.66 | 1 | 100 |
| AB | 2 | 3,041 | 2,733 | 125 | 4.57 | 2 | 125 |
| CS | 1 | 2,606 | 1,988 | 50 | 2.52 | 1 | 50 |
| CS | 2 | 2,606 | 1,988 | 75 | 3.77 | 2 | 75 |
| GL | 1 | 5,345 | 4,010 | 74 | 1.85 | 1 | 75 |
| GL | 2 | 5,345 | 4,010 | 198 | 4.94 | 2 | 200 |
| TL | 1 | 1,953 | 1,556 | 100 | 6.43 | 1 | 100 |
| TL | 2 | 1,953 | 1,556 | 175 | 11.25 | 2 | 175 |
| AR | 1 | 3,164 | 2,781 | 50 | 1.80 | 1 | 50 |
| AR | 2 | 3,164 | 2,781 | 99 | 3.56 | 2 | 100 |
| SB | 1 | 3,236 | 2,830 | 48 | 1.70 | 1 | 50 |
| SB | 2 | 3,236 | 2,830 | 68 | 2.40 | 2 | 75 |
| B | 1 | 22,216 | 18,466 | 189 | 1.02 | 1 | 200 |
| B | 2 | 22,216 | 18,466 | 385 | 2.08 | 2 | 400 |
| CT | 1 | 6,507 | 5,604 | 50 | 0.89 | 1 | 50 |
| CT | 2 | 6,507 | 5,604 | 148 | 2.64 | 2 | 150 |
| PH | 1 | 6,131 | 5,140 | 100 | 1.95 | 1 | 100 |
| PH | 2 | 6,131 | 5,140 | 148 | 2.88 | 2 | 150 |
| TM | 1 | 5,795 | 4,750 | 119 | 2.51 | 1 | 125 |
| TM | 2 | 5,795 | 4,750 | 165 | 3.47 | 2 | 175 |
| CJ | 1 | 4,885 | 4,448 | 73 | 1.64 | 1 | 75 |
| CJ | 2 | 4,885 | 4,448 | 123 | 2.77 | 2 | 125 |
| AG | 1 | 6,458 | 5,572 | 144 | 2.58 | 1 | 150 |
| AG | 2 | 6,458 | 5,572 | 192 | 3.45 | 2 | 200 |
| BR | 1 | 2,658 | 2,462 | 99 | 4.02 | 1 | 100 |
| BR | 2 | 2,658 | 2,462 | 174 | 7.07 | 2 | 175 |
| BT | 1 | 3,870 | 3,034 | 100 | 3.30 | 1 | 100 |
| BT | 2 | 3,870 | 3,034 | 200 | 6.59 | 2 | 200 |
| BV | 1 | 4,886 | 4,445 | 48 | 1.08 | 1 | 50 |
| BV | 2 | 4,886 | 4,445 | 97 | 2.18 | 2 | 100 |
| DB | 1 | 3,907 | 3,458 | 99 | 2.86 | 1 | 100 |
| DB | 2 | 3,907 | 3,458 | 198 | 5.73 | 2 | 200 |
| DJ | 1 | 5,579 | 4,891 | 194 | 3.97 | 2 | 200 |
| DJ | 2 | 5,579 | 4,891 | 242 | 4.95 | 3 | 250 |
| GJ | 1 | 3,930 | 2,983 | 100 | 3.35 | 1 | 100 |
| GJ | 2 | 3,930 | 2,983 | 225 | 7.54 | 2 | 225 |
| IL | 1 | 2,546 | 1,945 | 100 | 5.14 | 1 | 100 |
| IL | 2 | 2,546 | 1,945 | 175 | 9.00 | 2 | 175 |
| OT | 1 | 4,724 | 3,772 | 123 | 3.26 | 1 | 125 |
| OT | 2 | 4,724 | 3,772 | 148 | 3.92 | 2 | 150 |
| VL | 1 | 4,110 | 3,316 | 75 | 2.26 | 1 | 75 |
| VL | 2 | 4,110 | 3,316 | 125 | 3.77 | 2 | 125 |
| VN | 1 | 3,338 | 2,645 | 99 | 3.74 | 1 | 100 |
| VN | 2 | 3,338 | 2,645 | 149 | 5.63 | 2 | 150 |

Each plot point or bar has its applicant and gymnasium support recorded in the corresponding aggregate bin CSV. The applicant-weighted pooled plots compute a single rate over all applicants in each common peer-score bin. The equal-county pooled plots first compute one rate per represented county within each peer-score bin (and own-score band), then average those county rates equally. A county with no eligible applicants in a cell is absent, not assigned zero; the number of contributing counties is printed on the plot. Thus even equal-county curves can change composition across bins. The separate gymnasium-mean plot uses each observed gymnasium with at least two applicants once to set common peer-score quantile bins. All eligible students in that gymnasium inherit its bin; the colored own-score bands use pooled percentiles across the selected counties. Success rates within those cells weight eligible applicants equally. The matching equal-width plot changes only how the common gymnasium-mean bins are cut: equal score intervals replace equal-count gymnasium quantiles. Empty equal-width intervals remain visible as gaps. These are descriptive associations, not estimates of a causal peer or congestion effect. No applicant preferences are observed; the success fraction is not institutional K/N.

The new-county source gate had zero unresolved top-one/top-two labels. Galați retains its documented one-applicant outcome uncertainty. This is a selected-county descriptive comparison, not a 41-county national analysis. No individual-level output was exported.
