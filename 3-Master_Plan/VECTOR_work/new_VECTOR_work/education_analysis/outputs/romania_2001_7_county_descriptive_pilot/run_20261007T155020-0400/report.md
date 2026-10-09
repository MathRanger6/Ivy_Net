# Romania 2001: 7-county descriptive placement pilot

This researcher-run analysis uses saved 2001 Romanian Ministry admission webpages for Alba, Caraș-Severin, Galați, Tulcea, Arad, Sibiu, Bucharest–Ilfov. It asks whether actual placement in a designated selective program varies with the examination performance of *other observed admission-round applicants from the same originating gymnasium*. It is descriptive. It does not establish that peers caused placement differences or that all eighth graders are represented.

## County size and cross-county placements

These counts use all recovered applicants and all saved county placements, before vocational, peer-count, or outcome exclusions. Participating gymnasiums have at least one observed applicant; the directory can also list schools with none. Outgoing means a student from this county's gymnasium was placed in another county. Incoming means a placement here belongs to an applicant from another county's gymnasium. These are school-location changes, not evidence that families moved.

**Outgoing percentages divide by all applicants from the county's gymnasiums. Incoming percentages divide by all placements in the destination county.** They have different denominators and should not be subtracted. Incoming origins are identified from recovered gymnasium pages or the printed originating-school county in the County Applicant View, linked to the placement by name and admission score. For Bucharest, the complete incoming-admitted webpages and per-school results replace its incomplete county-wide applicant and unassigned webpages. Unknown origins/outcomes are reported separately, not counted as stayers.

- **Alba (AB):** 161 participating gymnasiums (149 with at least two applicants; 168 listed in the directory), 3,041 applicants. Outgoing: 77 (2.53% of origin applicants). Incoming: 19 (0.64% of 2,977 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Caraș-Severin (CS):** 143 participating gymnasiums (133 with at least two applicants; 171 listed in the directory), 2,606 applicants. Outgoing: 142 (5.45% of origin applicants). Incoming: 15 (0.64% of 2,333 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Galați (GL):** 185 participating gymnasiums (177 with at least two applicants; 190 listed in the directory), 5,345 applicants. Outgoing: 77 (1.44% of origin applicants). Incoming: 97 (1.88% of 5,169 placements here). Unresolved origin-applicant outcomes: 1; destination placements with unresolved origin/matching: 0.
- **Tulcea (TL):** 91 participating gymnasiums (85 with at least two applicants; 103 listed in the directory), 1,953 applicants. Outgoing: 148 (7.58% of origin applicants). Incoming: 7 (0.39% of 1,794 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Arad (AR):** 131 participating gymnasiums (125 with at least two applicants; 136 listed in the directory), 3,164 applicants. Outgoing: 43 (1.36% of origin applicants). Incoming: 71 (2.35% of 3,018 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Sibiu (SB):** 144 participating gymnasiums (133 with at least two applicants; 152 listed in the directory), 3,236 applicants. Outgoing: 41 (1.27% of origin applicants). Incoming: 118 (3.60% of 3,276 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.
- **Bucharest–Ilfov (B):** 275 participating gymnasiums (269 with at least two applicants; 289 listed in the directory), 22,216 applicants. Outgoing: 53 (0.24% of origin applicants). Incoming: 1,317 (5.99% of 21,969 placements here). Unresolved origin-applicant outcomes: 0; destination placements with unresolved origin/matching: 0.

The full counts, including unassigned applicants and local placements, are saved in `county_size_and_movement.csv`. Lower movement may make the county a more complete view of its selection market; it does not establish causal identification. The county list is not automatically changed in response to these counts or the curves.

## What counts

This run designates the top 1, 2 cumulative cutoff tier(s), separately, in each of the three combined groups, among fully occupied programs. Under the agreed primary specification, top one is primary and top two is a planned comparison. Actual placement is required. Vacancies, ties, number of winning programs, and the sum of their places are reported separately from the observed success fraction. No applicant preference list is available; the observed fraction is **not institutional K/N**.

Primary outcome participants have a confirmed placement in their originating county or are confirmed unassigned, and have at least one observed gymnasium peer. Confirmed placements outside the originating county and the one unresolved outcome are excluded from the outcome denominator but retained as peers. Applicants with more than one possible exact local program are included only when every possible program has the same top-program success label under this run's settings. A comparison omitting those applicants is saved when requested. Vocationally placed applicants remain in the primary denominator.

## County counts

| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Places in winning programs | Ambiguous exact program, binary known | Outside county | No observed peer |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AB | 1 | 3,041 | 2,953 | 150 | 5.08 | 3 | 150 | 109 | 77 | 12 |
| AB | 2 | 3,041 | 2,953 | 349 | 11.82 | 6 | 350 | 109 | 77 | 12 |
| CS | 1 | 2,606 | 2,454 | 100 | 4.07 | 3 | 100 | 271 | 142 | 10 |
| CS | 2 | 2,606 | 2,454 | 246 | 10.02 | 6 | 250 | 271 | 142 | 10 |
| GL | 1 | 5,345 | 5,260 | 124 | 2.36 | 3 | 125 | 0 | 77 | 8 |
| GL | 2 | 5,345 | 5,260 | 323 | 6.14 | 6 | 325 | 0 | 77 | 8 |
| TL | 1 | 1,953 | 1,799 | 298 | 16.56 | 3 | 300 | 178 | 148 | 6 |
| TL | 2 | 1,953 | 1,799 | 498 | 27.68 | 6 | 500 | 178 | 148 | 6 |
| AR | 1 | 3,164 | 3,115 | 199 | 6.39 | 3 | 200 | 125 | 43 | 6 |
| AR | 2 | 3,164 | 3,115 | 348 | 11.17 | 6 | 350 | 125 | 43 | 6 |
| SB | 1 | 3,236 | 3,185 | 194 | 6.09 | 3 | 200 | 447 | 41 | 11 |
| SB | 2 | 3,236 | 3,185 | 333 | 10.46 | 6 | 350 | 447 | 41 | 11 |
| B | 1 | 22,216 | 22,157 | 455 | 2.05 | 3 | 475 | 0 | 53 | 6 |
| B | 2 | 22,216 | 22,157 | 817 | 3.69 | 6 | 848 | 0 | 53 | 6 |

## What changes when we alter the denominator

Each line below uses the **same designated programs** as the primary row. Removing a group changes the people described by the rate; it does not recover anyone's unobserved program preferences.

- **AB, top 1:** primary 150/2,953 (5.08%). Exclude uncertain exact-program identities: 2,844 applicants, 5.27% selected. Exclude vocational destinations: 2,733 applicants, 5.49% selected.
- **AB, top 2:** primary 349/2,953 (11.82%). Exclude uncertain exact-program identities: 2,844 applicants, 12.27% selected. Exclude vocational destinations: 2,733 applicants, 12.77% selected.
- **CS, top 1:** primary 100/2,454 (4.07%). Exclude uncertain exact-program identities: 2,184 applicants, 4.58% selected. Exclude vocational destinations: 1,988 applicants, 5.03% selected.
- **CS, top 2:** primary 246/2,454 (10.02%). Exclude uncertain exact-program identities: 2,184 applicants, 11.26% selected. Exclude vocational destinations: 1,988 applicants, 12.37% selected.
- **GL, top 1:** primary 124/5,260 (2.36%). Exclude uncertain exact-program identities: 5,260 applicants, 2.36% selected. Exclude vocational destinations: 4,010 applicants, 3.09% selected.
- **GL, top 2:** primary 323/5,260 (6.14%). Exclude uncertain exact-program identities: 5,260 applicants, 6.14% selected. Exclude vocational destinations: 4,010 applicants, 8.05% selected.
- **TL, top 1:** primary 298/1,799 (16.56%). Exclude uncertain exact-program identities: 1,622 applicants, 18.37% selected. Exclude vocational destinations: 1,556 applicants, 19.15% selected.
- **TL, top 2:** primary 498/1,799 (27.68%). Exclude uncertain exact-program identities: 1,622 applicants, 30.70% selected. Exclude vocational destinations: 1,556 applicants, 32.01% selected.
- **AR, top 1:** primary 199/3,115 (6.39%). Exclude uncertain exact-program identities: 2,990 applicants, 6.66% selected. Exclude vocational destinations: 2,781 applicants, 7.16% selected.
- **AR, top 2:** primary 348/3,115 (11.17%). Exclude uncertain exact-program identities: 2,990 applicants, 11.64% selected. Exclude vocational destinations: 2,781 applicants, 12.51% selected.
- **SB, top 1:** primary 194/3,185 (6.09%). Exclude uncertain exact-program identities: 2,741 applicants, 7.08% selected. Exclude vocational destinations: 2,830 applicants, 6.86% selected.
- **SB, top 2:** primary 333/3,185 (10.46%). Exclude uncertain exact-program identities: 2,741 applicants, 12.15% selected. Exclude vocational destinations: 2,830 applicants, 11.77% selected.
- **B, top 1:** primary 455/22,157 (2.05%). Exclude uncertain exact-program identities: 22,157 applicants, 2.05% selected. Exclude vocational destinations: 18,466 applicants, 2.46% selected.
- **B, top 2:** primary 817/22,157 (3.69%). Exclude uncertain exact-program identities: 22,157 applicants, 3.69% selected. Exclude vocational destinations: 18,466 applicants, 4.42% selected.

The single unresolved Galați applicant remains outside the primary denominator. If that student later proves eligible for this outcome, the report's one-case low/high bounds treat the student as a nonsuccess or success, respectively; neither status is asserted now.


## Score bands and plots

The 75th–90th percentile band of excellence and top 10 percent are defined within each originating county from **all recovered admission-round applicants**, before outcome exclusions. The lower boundary is the 50th percentile. A separately saved plot applies pooled 7-county boundaries. Ties at a boundary enter the higher band, so actual band sizes may differ slightly from the named percentages. The horizontal axis is the mean national exam score of other observed gymnasium applicants on its original score scale. Figures and bin CSV files show applicant counts and distinct gymnasium counts; one large gymnasium is not many independent environments.

County exam-score boundaries (50th, 75th, and 90th percentiles):

- **AB:** 6.98, 8.01, 8.80 from 3,041 recovered applicants.
- **CS:** 6.65, 7.63, 8.53 from 2,606 recovered applicants.
- **GL:** 6.76, 7.70, 8.53 from 5,345 recovered applicants.
- **TL:** 6.83, 7.78, 8.51 from 1,953 recovered applicants.
- **AR:** 6.78, 7.70, 8.50 from 3,164 recovered applicants.
- **SB:** 6.83, 7.83, 8.65 from 3,236 recovered applicants.
- **B:** 7.08, 8.10, 8.86 from 22,216 recovered applicants.

## Limits and sensitivity

Each conditional score-band figure has 7 county panels and one additional combined panel. Each HERO figure likewise has one row per county plus a combined row, with equal-width and equal-number bars. Pooled panels use common peer-score bins and weight each applicant equally, so large counties contribute more. Pooled labels report the number of counties represented. A pooled slope can change because the county mix changes across bins; it is not a county-adjusted peer effect.

The ambiguous-program exclusion comparison changes the denominator, not the observed top-program numerator under the frozen six-category/full-program rule. The vocational exclusion comparison changes the described population and cannot reveal who actually applied to selective academic programs. One Galați applicant has no saved outcome; the summary CSV supplies a simple one-case low/high bound. Neither endpoint is asserted as the student's actual result. Source-status counts in the summary can overlap with 'no observed peer'; they are not meant to be added as mutually exclusive exclusions.

All source matches rely on printed name plus admission score because the archived personal identifier is masked. Examination scores were measured after time in the gymnasium. Geography, preferences, prior preparation, and other unobserved differences may explain descriptive patterns. Do not interpret a downturn or an upward slope as a causal congestion effect.

Every CSV here is free of applicant names and individual applicant rows. The program table includes public program names; the other CSVs contain aggregate counts or score boundaries. The private source pages remain in the Desktop cache. See the four-county design decision log and source-gate report for the exact prior choices and unresolved source item.
