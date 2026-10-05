# Romania 2001: 6-county descriptive placement pilot

This researcher-run analysis uses saved 2001 Romanian Ministry admission webpages for Alba, Caraș-Severin, Galați, Tulcea, Arad, Sibiu. It asks whether actual placement in a designated selective program varies with the examination performance of *other observed admission-round applicants from the same originating gymnasium*. It is descriptive. It does not establish that peers caused placement differences or that all eighth graders are represented.

## County size and cross-county placements

These counts use all recovered applicants and all saved county placements, before vocational, peer-count, or outcome exclusions. Participating gymnasiums have at least one observed applicant; the directory can also list schools with none. Outgoing means a student from this county's gymnasium was placed in another county. Incoming means a placement here belongs to an applicant from another county's gymnasium. These are school-location changes, not evidence that families moved.

**Outgoing percentages divide by all applicants from the county's gymnasiums. Incoming percentages divide by all placements in the destination county.** They have different denominators and should not be subtracted. Incoming origins are identified from recovered gymnasium pages or the printed originating-school county in the County Applicant View, linked to the placement by name and admission score. Unknown origins/outcomes are reported separately, not counted as stayers.

- **Alba (AB):** 161 participating gymnasiums (149 with at least two applicants; 168 listed in the directory), 3,041 applicants. Outgoing: 77 (2.53% of origin applicants). Incoming: 19 (0.64% of 2,977 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Caraș-Severin (CS):** 143 participating gymnasiums (133 with at least two applicants; 171 listed in the directory), 2,606 applicants. Outgoing: 142 (5.45% of origin applicants). Incoming: 15 (0.64% of 2,333 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Galați (GL):** 185 participating gymnasiums (177 with at least two applicants; 190 listed in the directory), 5,345 applicants. Outgoing: 77 (1.44% of origin applicants). Incoming: 97 (1.88% of 5,169 placements here). Unresolved origin-applicant outcomes: 1; destination placements with unresolved origin/matching: 0.
- **Tulcea (TL):** 91 participating gymnasiums (85 with at least two applicants; 103 listed in the directory), 1,953 applicants. Outgoing: 148 (7.58% of origin applicants). Incoming: 7 (0.39% of 1,794 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Arad (AR):** 131 participating gymnasiums (125 with at least two applicants; 136 listed in the directory), 3,164 applicants. Outgoing: 43 (1.36% of origin applicants). Incoming: 71 (2.35% of 3,018 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Sibiu (SB):** 144 participating gymnasiums (133 with at least two applicants; 152 listed in the directory), 3,236 applicants. Outgoing: 41 (1.27% of origin applicants). Incoming: 118 (3.60% of 3,276 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.

The full counts, including unassigned applicants and local placements, are saved in `county_size_and_movement.csv`. Lower movement may make the county a more complete view of its selection market; it does not establish causal identification. The county list is not automatically changed in response to these counts or the curves.

## What counts

This run designates the top 1, 2 cumulative cutoff tier(s), separately, in each of the six original program categories, among fully occupied programs. Under the agreed primary specification, top one is primary and top two is a planned comparison. Actual placement is required. Vacancies, ties, number of winning programs, and the sum of their places are reported separately from the observed success fraction. No applicant preference list is available; the observed fraction is **not institutional K/N**.

Primary outcome participants have a confirmed placement in their originating county or are confirmed unassigned, and have at least one observed gymnasium peer. Confirmed placements outside the originating county and the one unresolved outcome are excluded from the outcome denominator but retained as peers. Applicants with more than one possible exact local program are included only when every possible program has the same top-program success label under this run's settings. A comparison omitting those applicants is saved when requested. This run excludes vocationally placed applicants from the primary denominator; it is not the agreed primary specification.

## County counts

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Places in winning programs | Ambiguous exact program, binary known | Outside county | No observed peer |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,733 | 200 | 7.32 | 5 | 200 | 109 | 77 | 12 |
| AB | 2 | 3,041 | 2,733 | 474 | 17.34 | 10 | 475 | 109 | 77 | 12 |
| CS | 1 | 2,606 | 1,988 | 150 | 7.55 | 6 | 200 | 271 | 142 | 10 |
| CS | 2 | 2,606 | 1,988 | 370 | 18.61 | 12 | 425 | 271 | 142 | 10 |
| GL | 1 | 5,345 | 4,010 | 174 | 4.34 | 6 | 250 | 0 | 77 | 8 |
| GL | 2 | 5,345 | 4,010 | 422 | 10.52 | 12 | 575 | 0 | 77 | 8 |
| TL | 1 | 1,953 | 1,556 | 373 | 23.97 | 5 | 375 | 178 | 148 | 6 |
| TL | 2 | 1,953 | 1,556 | 648 | 41.65 | 10 | 650 | 178 | 148 | 6 |
| AR | 1 | 3,164 | 2,781 | 247 | 8.88 | 6 | 300 | 125 | 43 | 6 |
| AR | 2 | 3,164 | 2,781 | 446 | 16.04 | 10 | 500 | 125 | 43 | 6 |
| SB | 1 | 3,236 | 2,830 | 242 | 8.55 | 5 | 250 | 447 | 41 | 11 |
| SB | 2 | 3,236 | 2,830 | 478 | 16.89 | 10 | 500 | 447 | 41 | 11 |

## What changes when we alter the denominator

Each line below uses the **same designated programs** as the primary row. Removing a group changes the people described by the rate; it does not recover anyone's unobserved program preferences.

- **AB, top 1:** primary 200/2,733 (7.32%). Exclude uncertain exact-program identities: 2,624 applicants, 7.62% selected. Exclude vocational destinations: 2,733 applicants, 7.32% selected.
- **AB, top 2:** primary 474/2,733 (17.34%). Exclude uncertain exact-program identities: 2,624 applicants, 18.06% selected. Exclude vocational destinations: 2,733 applicants, 17.34% selected.
- **CS, top 1:** primary 150/1,988 (7.55%). Exclude uncertain exact-program identities: 1,718 applicants, 8.73% selected. Exclude vocational destinations: 1,988 applicants, 7.55% selected.
- **CS, top 2:** primary 370/1,988 (18.61%). Exclude uncertain exact-program identities: 1,718 applicants, 21.54% selected. Exclude vocational destinations: 1,988 applicants, 18.61% selected.
- **GL, top 1:** primary 174/4,010 (4.34%). Exclude uncertain exact-program identities: 4,010 applicants, 4.34% selected. Exclude vocational destinations: 4,010 applicants, 4.34% selected.
- **GL, top 2:** primary 422/4,010 (10.52%). Exclude uncertain exact-program identities: 4,010 applicants, 10.52% selected. Exclude vocational destinations: 4,010 applicants, 10.52% selected.
- **TL, top 1:** primary 373/1,556 (23.97%). Exclude uncertain exact-program identities: 1,379 applicants, 27.05% selected. Exclude vocational destinations: 1,556 applicants, 23.97% selected.
- **TL, top 2:** primary 648/1,556 (41.65%). Exclude uncertain exact-program identities: 1,379 applicants, 46.99% selected. Exclude vocational destinations: 1,556 applicants, 41.65% selected.
- **AR, top 1:** primary 247/2,781 (8.88%). Exclude uncertain exact-program identities: 2,656 applicants, 9.30% selected. Exclude vocational destinations: 2,781 applicants, 8.88% selected.
- **AR, top 2:** primary 446/2,781 (16.04%). Exclude uncertain exact-program identities: 2,656 applicants, 16.79% selected. Exclude vocational destinations: 2,781 applicants, 16.04% selected.
- **SB, top 1:** primary 242/2,830 (8.55%). Exclude uncertain exact-program identities: 2,386 applicants, 10.14% selected. Exclude vocational destinations: 2,830 applicants, 8.55% selected.
- **SB, top 2:** primary 478/2,830 (16.89%). Exclude uncertain exact-program identities: 2,386 applicants, 20.03% selected. Exclude vocational destinations: 2,830 applicants, 16.89% selected.

The single unresolved Galați applicant remains outside the primary denominator. If that student later proves eligible for this outcome, the report's one-case low/high bounds treat the student as a nonsuccess or success, respectively; neither status is asserted now.


## Score bands and plots

The 75th–90th percentile band of excellence and top 10 percent are defined within each originating county from **all recovered admission-round applicants**, before outcome exclusions. The lower boundary is the 50th percentile. A separately saved plot applies pooled 6-county boundaries. Ties at a boundary enter the higher band, so actual band sizes may differ slightly from the named percentages. The horizontal axis is the mean national exam score of other observed gymnasium applicants on its original score scale. Figures and bin CSV files show applicant counts and distinct gymnasium counts; one large gymnasium is not many independent environments.

County exam-score boundaries (50th, 75th, and 90th percentiles):

- **AB:** 6.98, 8.01, 8.80 from 3,041 recovered applicants.
- **CS:** 6.65, 7.63, 8.53 from 2,606 recovered applicants.
- **GL:** 6.76, 7.70, 8.53 from 5,345 recovered applicants.
- **TL:** 6.83, 7.78, 8.51 from 1,953 recovered applicants.
- **AR:** 6.78, 7.70, 8.50 from 3,164 recovered applicants.
- **SB:** 6.83, 7.83, 8.65 from 3,236 recovered applicants.

## Limits and sensitivity

Each conditional score-band figure has 6 county panels and one additional combined panel. Each HERO figure likewise has one row per county plus a combined row, with equal-width and equal-number bars. Pooled panels use common peer-score bins and weight each applicant equally, so large counties contribute more. Pooled labels report the number of counties represented. A pooled slope can change because the county mix changes across bins; it is not a county-adjusted peer effect.

The ambiguous-program exclusion comparison changes the denominator, not the observed top-program numerator under the frozen six-category/full-program rule. The vocational exclusion comparison changes the described population and cannot reveal who actually applied to selective academic programs. One Galați applicant has no saved outcome; the summary CSV supplies a simple one-case low/high bound. Neither endpoint is asserted as the student's actual result. Source-status counts in the summary can overlap with 'no observed peer'; they are not meant to be added as mutually exclusive exclusions.

All source matches rely on printed name plus admission score because the archived personal identifier is masked. Examination scores were measured after time in the gymnasium. Geography, preferences, prior preparation, and other unobserved differences may explain descriptive patterns. Do not interpret a downturn or an upward slope as a causal congestion effect.

Every CSV here is free of applicant names and individual applicant rows. The program table includes public program names; the other CSVs contain aggregate counts or score boundaries. The private source pages remain in the Desktop cache. See the four-county design decision log and source-gate report for the exact prior choices and unresolved source item.
