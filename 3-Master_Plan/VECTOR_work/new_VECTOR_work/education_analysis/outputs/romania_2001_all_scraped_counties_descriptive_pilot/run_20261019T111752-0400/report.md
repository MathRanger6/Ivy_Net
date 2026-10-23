# Romania 2001: 22-county descriptive pilot

This run combines the previously verified county-wide placement pipeline with the newer school-specific admitted/rejected-result pipeline. Printed name and admission score are provisional linkage keys because the archival ID is masked. The observed peer pool includes admission-round applicants, not all eighth graders.

Program rankings and outcome settings are recorded in `run_manifest.json`. Top one and top two are separate cumulative cutoff tiers. An admitted student is successful only when their actual local program belongs to the designated tier. Outside-county placements are excluded from the outcome denominator but retained as gymnasium peers; confirmed unassigned applicants remain in the denominator.

## County results

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |
|---|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,953 | 200 | 6.77 | 5 | 200 |
| AB | 2 | 3,041 | 2,953 | 474 | 16.05 | 10 | 475 |
| CS | 1 | 2,606 | 2,454 | 199 | 8.11 | 6 | 200 |
| CS | 2 | 2,606 | 2,454 | 419 | 17.07 | 12 | 425 |
| GL | 1 | 5,345 | 5,260 | 246 | 4.68 | 6 | 250 |
| GL | 2 | 5,345 | 5,260 | 569 | 10.82 | 12 | 575 |
| TL | 1 | 1,953 | 1,799 | 373 | 20.73 | 5 | 375 |
| TL | 2 | 1,953 | 1,799 | 648 | 36.02 | 10 | 650 |
| AR | 1 | 3,164 | 3,115 | 295 | 9.47 | 6 | 300 |
| AR | 2 | 3,164 | 3,115 | 494 | 15.86 | 10 | 500 |
| SB | 1 | 3,236 | 3,185 | 242 | 7.60 | 5 | 250 |
| SB | 2 | 3,236 | 3,185 | 478 | 15.01 | 10 | 500 |
| B | 1 | 22,216 | 22,157 | 714 | 3.22 | 6 | 750 |
| B | 2 | 22,216 | 22,157 | 1,271 | 5.74 | 12 | 1,323 |
| CT | 1 | 6,507 | 6,453 | 321 | 4.97 | 6 | 325 |
| CT | 2 | 6,507 | 6,453 | 764 | 11.84 | 12 | 775 |
| PH | 1 | 6,131 | 6,071 | 422 | 6.95 | 6 | 425 |
| PH | 2 | 6,131 | 6,071 | 716 | 11.79 | 12 | 725 |
| TM | 1 | 5,795 | 5,773 | 487 | 8.44 | 7 | 500 |
| TM | 2 | 5,795 | 5,773 | 846 | 14.65 | 13 | 875 |
| CJ | 1 | 4,885 | 4,827 | 292 | 6.05 | 5 | 300 |
| CJ | 2 | 4,885 | 4,827 | 510 | 10.57 | 10 | 525 |
| AG | 1 | 6,458 | 6,404 | 438 | 6.84 | 6 | 450 |
| AG | 2 | 6,458 | 6,404 | 757 | 11.82 | 11 | 775 |
| BR | 1 | 2,658 | 2,584 | 320 | 12.38 | 6 | 325 |
| BR | 2 | 2,658 | 2,584 | 544 | 21.05 | 11 | 550 |
| BT | 1 | 3,870 | 3,757 | 349 | 9.29 | 6 | 350 |
| BT | 2 | 3,870 | 3,757 | 696 | 18.53 | 12 | 700 |
| BV | 1 | 4,886 | 4,808 | 481 | 10.00 | 6 | 500 |
| BV | 2 | 4,886 | 4,808 | 773 | 16.08 | 11 | 800 |
| DB | 1 | 3,907 | 3,665 | 398 | 10.86 | 6 | 400 |
| DB | 2 | 3,907 | 3,665 | 669 | 18.25 | 11 | 675 |
| DJ | 1 | 5,579 | 5,518 | 526 | 9.53 | 7 | 550 |
| DJ | 2 | 5,579 | 5,518 | 838 | 15.19 | 12 | 875 |
| GJ | 1 | 3,930 | 3,694 | 396 | 10.72 | 6 | 400 |
| GJ | 2 | 3,930 | 3,694 | 793 | 21.47 | 12 | 800 |
| IL | 1 | 2,546 | 2,449 | 399 | 16.29 | 6 | 400 |
| IL | 2 | 2,546 | 2,449 | 708 | 28.91 | 12 | 725 |
| OT | 1 | 4,724 | 4,372 | 347 | 7.94 | 6 | 350 |
| OT | 2 | 4,724 | 4,372 | 691 | 15.81 | 11 | 700 |
| VL | 1 | 4,110 | 4,013 | 421 | 10.49 | 6 | 425 |
| VL | 2 | 4,110 | 4,013 | 787 | 19.61 | 12 | 800 |
| VN | 1 | 3,338 | 3,237 | 247 | 7.63 | 6 | 250 |
| VN | 2 | 3,338 | 3,237 | 744 | 22.98 | 12 | 750 |

Each plot point or bar has its applicant and gymnasium support recorded in the corresponding aggregate bin CSV. The applicant-weighted pooled plots compute a single rate over all applicants in each common peer-score bin. The equal-county pooled plots first compute one rate per represented county within each peer-score bin (and own-score band), then average those county rates equally. A county with no eligible applicants in a cell is absent, not assigned zero; the number of contributing counties is printed on the plot. Thus even equal-county curves can change composition across bins. The separate gymnasium-mean plot uses each observed gymnasium with at least two applicants once to set common peer-score quantile bins. All eligible students in that gymnasium inherit its bin; the colored own-score bands use pooled percentiles across the selected counties. Success rates within those cells weight eligible applicants equally. The matching equal-width plot changes only how the common gymnasium-mean bins are cut: equal score intervals replace equal-count gymnasium quantiles. Empty equal-width intervals remain visible as gaps. These are descriptive associations, not estimates of a causal peer or congestion effect. No applicant preferences are observed; the success fraction is not institutional K/N.

The new-county source gate had zero unresolved top-one/top-two labels. Galați retains its documented one-applicant outcome uncertainty. This is a selected-county descriptive comparison, not a 41-county national analysis. No individual-level output was exported.
