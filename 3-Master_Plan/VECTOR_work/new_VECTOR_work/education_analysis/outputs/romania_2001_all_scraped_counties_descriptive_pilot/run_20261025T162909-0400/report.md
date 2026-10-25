# Romania 2001: 22-county descriptive pilot

This run combines the previously verified county-wide placement pipeline with the newer school-specific admitted/rejected-result pipeline. Printed name and admission score are provisional linkage keys because the archival ID is masked. The observed peer pool includes admission-round applicants, not all eighth graders.

Program rankings and outcome settings are recorded in `run_manifest.json`. Top one and top two are separate cumulative cutoff tiers. An admitted student is successful only when their actual local program belongs to the designated tier. Outside-county placements are excluded from the outcome denominator but retained as gymnasium peers; confirmed unassigned applicants remain in the denominator.

## County results

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |
|---|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,733 | 200 | 7.32 | 5 | 200 |
| AB | 2 | 3,041 | 2,733 | 474 | 17.34 | 10 | 475 |
| CS | 1 | 2,606 | 1,988 | 150 | 7.55 | 6 | 200 |
| CS | 2 | 2,606 | 1,988 | 370 | 18.61 | 12 | 425 |
| GL | 1 | 5,345 | 4,010 | 174 | 4.34 | 6 | 250 |
| GL | 2 | 5,345 | 4,010 | 422 | 10.52 | 12 | 575 |
| TL | 1 | 1,953 | 1,556 | 373 | 23.97 | 5 | 375 |
| TL | 2 | 1,953 | 1,556 | 648 | 41.65 | 10 | 650 |
| AR | 1 | 3,164 | 2,781 | 247 | 8.88 | 6 | 300 |
| AR | 2 | 3,164 | 2,781 | 446 | 16.04 | 10 | 500 |
| SB | 1 | 3,236 | 2,830 | 242 | 8.55 | 5 | 250 |
| SB | 2 | 3,236 | 2,830 | 478 | 16.89 | 10 | 500 |
| B | 1 | 22,216 | 18,466 | 527 | 2.85 | 6 | 750 |
| B | 2 | 22,216 | 18,466 | 938 | 5.08 | 12 | 1,323 |
| CT | 1 | 6,507 | 5,604 | 296 | 5.28 | 6 | 325 |
| CT | 2 | 6,507 | 5,604 | 665 | 11.87 | 12 | 775 |
| PH | 1 | 6,131 | 5,140 | 348 | 6.77 | 6 | 425 |
| PH | 2 | 6,131 | 5,140 | 592 | 11.52 | 12 | 725 |
| TM | 1 | 5,795 | 4,750 | 440 | 9.26 | 7 | 500 |
| TM | 2 | 5,795 | 4,750 | 727 | 15.31 | 13 | 875 |
| CJ | 1 | 4,885 | 4,448 | 292 | 6.56 | 5 | 300 |
| CJ | 2 | 4,885 | 4,448 | 510 | 11.47 | 10 | 525 |
| AG | 1 | 6,458 | 5,572 | 388 | 6.96 | 6 | 450 |
| AG | 2 | 6,458 | 5,572 | 707 | 12.69 | 11 | 775 |
| BR | 1 | 2,658 | 2,462 | 320 | 13.00 | 6 | 325 |
| BR | 2 | 2,658 | 2,462 | 544 | 22.10 | 11 | 550 |
| BT | 1 | 3,870 | 3,034 | 324 | 10.68 | 6 | 350 |
| BT | 2 | 3,870 | 3,034 | 597 | 19.68 | 12 | 700 |
| BV | 1 | 4,886 | 4,445 | 387 | 8.71 | 6 | 500 |
| BV | 2 | 4,886 | 4,445 | 679 | 15.28 | 11 | 800 |
| DB | 1 | 3,907 | 3,458 | 348 | 10.06 | 6 | 400 |
| DB | 2 | 3,907 | 3,458 | 619 | 17.90 | 11 | 675 |
| DJ | 1 | 5,579 | 4,891 | 526 | 10.75 | 7 | 550 |
| DJ | 2 | 5,579 | 4,891 | 838 | 17.13 | 12 | 875 |
| GJ | 1 | 3,930 | 2,983 | 348 | 11.67 | 6 | 400 |
| GJ | 2 | 3,930 | 2,983 | 696 | 23.33 | 12 | 800 |
| IL | 1 | 2,546 | 1,945 | 349 | 17.94 | 6 | 400 |
| IL | 2 | 2,546 | 1,945 | 583 | 29.97 | 12 | 725 |
| OT | 1 | 4,724 | 3,772 | 272 | 7.21 | 6 | 350 |
| OT | 2 | 4,724 | 3,772 | 616 | 16.33 | 11 | 700 |
| VL | 1 | 4,110 | 3,316 | 373 | 11.25 | 6 | 425 |
| VL | 2 | 4,110 | 3,316 | 645 | 19.45 | 12 | 800 |
| VN | 1 | 3,338 | 2,645 | 199 | 7.52 | 6 | 250 |
| VN | 2 | 3,338 | 2,645 | 597 | 22.57 | 12 | 750 |

Each plot point or bar has its applicant and gymnasium support recorded in the corresponding aggregate bin CSV. The applicant-weighted pooled plots compute a single rate over all applicants in each common peer-score bin. The equal-county pooled plots first compute one rate per represented county within each peer-score bin (and own-score band), then average those county rates equally. A county with no eligible applicants in a cell is absent, not assigned zero; the number of contributing counties is printed on the plot. Thus even equal-county curves can change composition across bins. The separate gymnasium-mean plot uses each observed gymnasium with at least two applicants once to set common peer-score quantile bins. All eligible students in that gymnasium inherit its bin; the colored own-score bands use pooled percentiles across the selected counties. Success rates within those cells weight eligible applicants equally. The matching equal-width plot changes only how the common gymnasium-mean bins are cut: equal score intervals replace equal-count gymnasium quantiles. Empty equal-width intervals remain visible as gaps. These are descriptive associations, not estimates of a causal peer or congestion effect. No applicant preferences are observed; the success fraction is not institutional K/N.

The new-county source gate had zero unresolved top-one/top-two labels. Galați retains its documented one-applicant outcome uncertainty. This is a selected-county descriptive comparison, not a 41-county national analysis. No individual-level output was exported.
