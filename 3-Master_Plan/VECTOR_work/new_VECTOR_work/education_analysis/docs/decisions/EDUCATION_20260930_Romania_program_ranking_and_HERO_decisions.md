# Romania: program ranking and the path to the first HERO

**Date:** September 30, 2026.  
**Latest execution update:** Charles has run the first baseline HERO. The final section below records the authorized read-only inspection of its right edge and gymnasium contributions. Earlier implementation and repair paragraphs describe their then-current state; the experiment was not rerun during this follow-up.

**Status:** The first-pass design choices are agreed and implemented in a researcher-run notebook: highest-cutoff fully occupied programs within the six source categories, including ties; this yields five qualifying category leaders and no vocational leader. Retain vocationally placed applicants in the initial outcome denominator, with an option to exclude them in a separate comparison. Exclude confirmed outside-Alba placements from the outcome calculation; retain confirmed unassigned applicants as unsuccessful and leave unresolved outcomes unknown. Keep the full recovered applicant population for peer calculations. Cumulative second-ranked tiers and a separate three-group classification remain possible fallbacks. The implementation passed offline synthetic tests; no live placement acquisition or empirical HERO has run under this implementation.

**Source check completed:** The [program-cutoff source report](../source_audit/EDUCATION_20260930_Romania_program_cutoff_source_check.md) verifies 85 exact program-code joins and directly reported first/last admitted scores in the main-allocation tables. Fifty-five programs are full, 28 partially filled, and two empty. Empty entries have no observed cutoff. Program type, teaching language, and attendance form remain preserved, with no outcome eligibility rule imposed.

## Why we are taking this step

After seeing the gymnasium examination-score intervals, Charles reported the request: “show me the HERO.” The completed differentiation run covers 3,041 participating applicant records associated with 161 nonempty Alba origin-gymnasium codes in 2001. Its observed sorting index is 0.14918, compared with a mean of 0.05268 under 1,000 size-preserving random assignments. That describes grouping of examination performance. It does not provide a placement success column.

The next aim is a descriptive plot of realized selective placement against the average examination performance of the other observed applicants from each originating gymnasium. It is not yet a causal estimate or a model replay.

## Agreed ranking measure

Charles prefers program-level distinctions to a single whole-school ranking. One school may have the more selective mathematics program and another the more selective language/literature program. Compare like specializations and preserve source-native program codes and any language, attendance-format, or other admission distinctions before deciding which can be combined.

The agreed first measure is **the admission cutoff: the lowest admission score securing an observed place in the relevant program and allocation round**, subject to verifying what the source actually reports. A higher cutoff indicates greater realized entrance selectivity. It is not automatically a measure of teaching quality, causal school effectiveness, or individual preference satisfaction.

Use comparable program cutoffs across towns where available. A student receives the destination program's selectivity measure regardless of the reason for attending outside the originating community. A first-ranked program in one town may have a lower cutoff than a second-ranked program elsewhere; town rank alone does not give a common selectivity scale.

This is a same-cohort, descriptive ranking proposal. The admission composite includes the examination score and school grades; program cutoffs are themselves outcomes of allocation and demand. The later HERO must disclose that shared score construction. Do not silently treat the cutoffs as external, causally independent measures, or substitute a leave-one-out ranking without discussing the consequences.

## Minimum source requirements

1. Establish year and allocation round, distinguishing the main allocation from later redistribution rounds.
2. Identify whether a reported minimum is a contemporaneous cutoff, a previous-year information field, or another statistic.
3. Preserve program code, destination school, specialization, profile/route, teaching language, and attendance form when present.
4. Retain offered places, admitted counts, and vacancies where available. An unfilled program's lowest admitted score need not be a binding capacity cutoff.
5. Prefer a complete official program table. If a cutoff must be reconstructed from admitted records, require the relevant complete program roster. The minimum among Alba-origin applicants alone is not the program cutoff when applicants also arrived from elsewhere.
6. Do not treat missing cutoffs, unresolved ranks, or unmatched placements as unsuccessful outcomes.

## Transfer handling

The [quick cross-county check](../source_audit/EDUCATION_20260930_Romania_cross_county_quick_check.md) found 77 confirmed outside-Alba placements and one unassigned case among 78 records carried under another county. Same-town versus other-town-within-Alba placements have not yet been counted. Do not reconstruct family motives. Count observable geographic changes while attaching placements where the geography is explicit.

Keep the recovered origin-gymnasium applicant population when calculating peer averages. Charles subsequently approved excluding confirmed outside-Alba placements from the first outcome calculation, as specified below. This deliberately bounded first pass does not require recovering program rankings from other counties. Report the exclusion explicitly; it was chosen before viewing a HERO.

## September 30 decision: highest-ranked first, cumulative tiers if needed

Charles chose to start with the highest-cutoff program within each subject among the recovered Alba programs. He accepted counting **all programs tied at the highest cutoff** as equally top-ranked. A tie is not broken arbitrarily to enforce a fixed number of successful programs.

The first outcome is actual placement in the designated top-ranked program set. An applicant does not become successful merely because their score exceeds its cutoff. We do not observe whether they received their first preference.

Charles also endorsed a later expansion to the second-highest-ranked program tier, and potentially further tiers. This is cumulative: the expanded successful set would include the original highest tier plus the next tier, not replace the highest tier. Because ties can produce several programs at one cutoff, the number of included programs and places must be reported explicitly. Handling of ties at a later boundary must be specified consistently before that comparison runs.

The rationale is to examine the curve under a broader definition of selective placement if the first successful set yields too few observations for a useful plot. Preserve the first plot, counts, and uncertainty alongside any broader version. An absent downturn is a finding, not an automatic reason to expand tiers. No numerical adequacy threshold or automatic search over tiers has been approved.

Charles connected this choice to selection intensity, $K/N$. Report the observed success rate using selected applicants and the defined HERO population. Also retain program capacity and admitted counts as separate institutional quantities. Without preferences, the number who actually competed for those programs remains unknown; do not equate the observed success fraction with capacity divided by the true competitor population. Changing the successful set changes our outcome definition, not the historical allocation or its institutional capacity.

## Category decision and the separate three-group fallback

Charles approved all six source specializations for the first descriptive HERO: Mathematics–Informatics, Natural Sciences, Social Sciences, Philology, technological programs, and vocational programs. The first construction should not silently discard a category merely because it is nonacademic.

Charles proposed a later fallback with three broader groups: mathematics/sciences; social sciences/philology; and technology/vocational. His motivation includes allowing for students who value a school more than one narrow subject. This is a proposed sensitivity, not an inferred preference measure: neither actual preferences nor reasons for placement are observed.

The implementation of that fallback remains to be agreed. Merely relabelling the same six winning programs as three groups changes neither the successful set nor a pooled HERO. Re-ranking the combined groups and choosing only one winner per group could instead reduce successful placements. A broader-tier rule is a separate change. Specify the intended successful destinations before running the fallback; do not assume combining categories automatically increases counts or statistical precision.

## Vacancy issue and Charles's agreed full-capacity requirement

Reading the saved program table revealed one consequential exception among the six category leaders. The five non-vocational leaders each fill all offered places and have no tie at the highest score. Their combined admission counts are 200 (100 mathematics and 25 in each of the other four categories), before any match to our origin-gymnasium analysis population.

The vocational category leader is literal program `x37`, Grup Școlar Industrializarea Lemnului, Blaj: reported lowest admitted score 6.12, **two admitted to 100 places**, with 98 vacancies. The next two vocational cutoffs also come from very small intakes: `x80`, 5.95 with two of 25 places filled; `x41`, 5.83 with three of 50 filled. Across all 17 vocational entries, **none filled all places**; together they admitted 228 students to 1,325 places.

These facts are directly in the saved official aggregate tables. They do not prove that every student was eligible for every vocational place. They do mean the highest observed minimum cannot, by itself, establish a scarce capacity-constrained vocational award. Ranking it as the hardest vocational opportunity solely because its two admitted students had that minimum would be misleading.

VECTOR recommended requiring designated scarce-success programs to be fully occupied in this allocation table, and **Charles agreed**. A program must have admitted as many students as its listed places, with no vacancies, to qualify as a scarce-success destination. This retains the five non-vocational category leaders; no currently recovered vocational entry qualifies. Full occupancy is a necessary condition for this operational definition, not proof that every included applicant preferred or competed for that destination.

This source-based rule supersedes the earlier proposal to designate a winner in every category regardless of vacancies. It was agreed before inspecting any HERO. No applicant has been excluded or assigned a success/failure label, and peer pools remain unchanged. The subsequent denominator decision is recorded below.

## Vocational placements: retain initially, allow denominator exclusion

Charles chose to retain vocationally placed applicants in the initial outcome denominator, and required the ability to remove them in an explicitly labelled comparison. The implementation must expose this choice, defaulting to inclusion; it must not require manually deleting rows or rewriting the original data. This is a specification requirement, not a claim that the switch or HERO has already been implemented or run.

The exclusion acts only on focal applicants entering the success-rate calculation. Preserve their examination scores in the originating-gymnasium peer population. For an isolated denominator comparison, keep the five successful program destinations, each applicant's peer average, the examination-score standardization, and the initial bin boundaries fixed. Report counts of retained applicants, removed vocational placements, and successful placements per bin. Empty bins after exclusion must be shown as having no estimate rather than zero success. Save the comparison separately from the baseline.

An example explains why this matters: if a bin contains two successful applicants among 20 applicants, its success rate is 10%. Removing ten vocationally placed applicants changes it to two out of ten, or 20%, with no change in who obtained a successful placement. Since the five designated successful programs are non-vocational, the numerator should be unchanged by this switch. A changed curve or observed success fraction can therefore arise through denominator composition alone; it is not a changed historical allocation or a causal scarcity experiment.

Charles compared this option to earlier zero-TB or missing-PPM exclusions. The shared issue is defining a relevant comparison population. The justification is nevertheless different: these vocationally placed applicants have observed examination scores and observed destinations. This option is a sensitivity to educational route, not repair of a missing performance measure. Observed vocational placement does not establish whether a student wanted a vocational program, lacked access to another program, or preferred a different institution; preferences remain unobserved. Do not treat the analogy as authorization to remove low-scoring applicants or change the peer pool.

Do not silently classify unresolved placements as vocational. Apply the source-native vocational-level/category classification only when verified. How unresolved and outside-Alba destinations enter the analysis is a separate decision.

## Agreed first-pass geographic and missing-outcome rules

Charles approved the following bounded approach:

1. Applicants with confirmed outside-Alba placements do not enter the first HERO outcome denominator. The previous aggregate audit identified 77 such records; implementation must verify and report the exact matched count rather than force that total.
2. Their examination scores remain in the originating-gymnasium peer averages and the fixed full-population standardization.
3. Confirmed unassigned applicants remain in the outcome population as unsuccessful placements, provided they have a defined peer average. The one unassigned case among the 78 non-Alba-county records is not a confirmed outside-Alba placement and must not be excluded merely because of its candidate county field.
4. Unresolved or ambiguous placements and unresolved program identities remain unknown, with counts reported. They must not be assigned zero success silently.
5. Applicants with no other recovered applicant in their originating gymnasium have no leave-one-out peer average and cannot enter this HERO. The 12 singleton records remain in the source accounting. Exclusion categories may overlap; report a reconciled flow rather than subtracting their marginal counts blindly.

This is an outcome-population restriction, not a claim that all retained applicants competed for the five designated programs or that outside-Alba applicants were unsuccessful. The plot must identify Alba 2001, the recovered applicant population, and its outside-destination exclusion.

## Next action

Charles explicitly authorized implementation and allowed a one-time exception to the Cursor-specific notebook-editing tool rule for this new notebook. The [placement-and-HERO notebook](../../notebooks/EDUCATION_20260930_Romania_2001_placements_and_HERO.ipynb) is ready for him to run in Cursor using sports_net. Its [Python companion](../../code/EDUCATION_20260930_romania_placements_and_hero.py) contains the retrieval, exact matching, and plotting functions. No live acquisition or empirical HERO was run while preparing it.

The first run reuses the completed candidate cache and downloads only missing school-specific placement reports. Source-verified empty gymnasiums require no placement page. Each completed nonempty school is saved immediately with its raw page and checksums under `~/Desktop/VECTOR_temp/romania_alba_2001_differentiation_v1/placements_v1/`; unresolved addresses are saved after every attempt and retried in later passes. The existing adaptive archive client is reused. No identifying rows enter the synced workspace.

The offline stage verifies the frozen examination-score population and standardization, attaches exact unique names within origin code with a composite-score check, and calculates the peer mean over the complete recovered population. Program identity requires a unique exact school/profile/specialization match. Ambiguous source labels, including unresolved language or attendance variants, stay unknown; there is no approximate-name or score-threshold assignment of success.

Each execution creates a new timestamped folder under `outputs/romania_alba_2001_hero_v1/`, preserving the baseline, a narrated report, name-free applicant audit, program winners, matching/exclusion counts, bin edges, figures, and source/output hashes. The optional vocational exclusion produces an additional comparison and asserts that successful placements remain unchanged in every fixed bin. Sixteen equal-width and up to sixteen quantile bins are requested; repeated quantile boundaries are collapsed without splitting identical peer values by row order. Empty bins have no estimate. Counts on each bar expose sparse support; these descriptive plots do not supply a school-cluster-adjusted uncertainty estimate.

**Validation:** Eleven offline tests passed, covering tied program leaders and vacancies, actual placement versus score thresholds, ambiguous identities, origin-specific person matching, composite disagreement, fixed peers and bins under denominator changes, exclusion overlap, corrupted checkpoints, request retry, network-free resume, and a complete synthetic report/figure run. These tests validate implementation behavior, not real-data linkage or an empirical finding. Do not broaden years or counties, fit a curve, or launch either fallback automatically.

## September 30 repair: school 276 has a longer placement report

Charles's acquisition reached 167/168 checkpoints. The remaining page was downloading successfully, but the implementation repeatedly rejected 104 placement rows because the frozen candidate report contains 103 rows. This was an overly restrictive count check, not a rate-limit failure. Retrying the same page could not resolve it.

A focused source check verified all 103 candidate names match uniquely in the 104-row placement report, with zero admission-composite disagreements, zero missing candidates, and no duplicate names in either report. The additional placement person has no exact name-and-composite match in any other frozen origin report. Why that person is absent from the candidate reports remains unknown. This is another reason to describe our population as recovered participating applicants rather than a verified complete graduating cohort.

The repair accepts a longer placement report only after every frozen candidate has a unique exact name and matching composite. It preserves all placement rows and their raw source page in the Desktop cache, records a name-free coverage audit, and continues to join outcomes onto the unchanged candidate population. The extra placement row does not enter the denominator, global standardization, or peer averages. Missing, ambiguous, or score-disagreeing candidates still prevent acceptance of a longer report. Existing equal-count checkpoints remain reusable.

Source: origin code `276`, candidate cache `school_reports/school_276.json`, and [archived companion placement report](https://web.archive.org/web/20020824150445id_/http://www.edu.ro/adm2001/raport_total_per_scoala.asp-cj=AB&nj=ALBA&cs=276&ns=SCOALA+GENERALA+CLASELE+I+-+VIII+NR.3+CUGIR.htm). The retrieved raw-page SHA-256 is `7328a6b28e54e8ef470830c475764caad828534ca41ebbadd542f8fffd222433`; its decoded-body hash matches Charles's repeated retrieval log entries. The source discrepancy is retained rather than erased by trimming the report.

**Validation and execution boundary:** Fourteen offline synthetic tests pass after the repair, including longer-report acceptance, unchanged candidate population, and rejection of missing/ambiguous/disagreeing matches. VECTOR retrieved only the specific problematic source page for diagnosis; VECTOR did not execute notebook Section 6 or the empirical HERO. Charles should reload the Python companion in his existing kernel, rerun Section 5 (which skips the 167 saved checkpoints), then run Section 6 himself.

## First HERO inspection: what produces the right edge and the peak?

Charles subsequently ran the notebook and shared the first HERO. He authorized a narrow follow-up: inspect the three applicants beyond the equal-width peak and count originating gymnasiums in the upper bars. VECTOR read the saved outputs only. No retrieval, new filter, selection definition, plot rebuild, or HERO rerun occurred. The saved run is `run_20260930T181101_938202Z` under `outputs/romania_alba_2001_hero_v1/`. Its recorded output checksums passed, and counts and successes in both sets of sixteen bars reconciled exactly to the saved applicant audit and fixed bin edges.

The baseline contains 200 successful placements among 2,844 outcome-eligible applicants from 148 source-coded gymnasiums (7.03%). The underlying peer population remains 3,041 recovered applicants. The saved reconciliation also records 109 ambiguous program identities excluded from the outcome denominator. Those cases were not reclassified in this inspection.

### First we inspected the three applicants beyond the equal-width peak

All three have confirmed local program placements; their zeros are not missing placements or unknown identities.

- **Origin 102, generated applicant row 9:** examination score 5.20, school-grade average 7.31, admission composite 5.72. This applicant has eight observed peers, averaging 8.09625 on the examination. The actual destination is vocational program `x45` at Colegiul Economic “Dionisie Pop Martinan,” Alba Iulia (53 admitted to 100 places). This is equal-width bin 13. The applicant is a low examination scorer among stronger-scoring observed peers, not an otherwise exceptional examination performer visibly losing a top place.
- **Origin 123, generated applicant row 6:** examination score 5.66, school-grade average 8.00, admission composite 6.24. Five observed peers average 8.17. The destination is vocational program `xx3` at Grup Școlar Industrial Sebeș (39 admitted to 150 places). This is the other applicant in equal-width bin 13.
- **Origin 215, generated applicant row 2:** examination score 8.81, school-grade average 9.98, admission composite 9.10. There is only one observed peer, with examination score 9.06. This applicant entered technology program `x44` at Colegiul Economic “Dionisie Pop Martinan,” Alba Iulia, which filled all 150 places and reported a cutoff of 8.03. It is not the category-leading technology program `x19` in our designated successful set. Thus this is a strong applicant with a real placement, counted zero under our narrow outcome definition. The reason for that destination is unobserved. The other recovered applicant from origin 215 was placed outside Alba and is excluded from the outcome denominator, while retained as a peer.

These are recovered applicant groups of nine, six, and two people, respectively—not verified full graduating classes. Their far-right placement supplies no compelling evidence that strong students generally lost out because their peers were strong. It also does not prove congestion absent.

### Then we examined why lower-scoring applicants can be farthest right

The peer average excludes the focal applicant. Within any fixed group, removing a lower score leaves a higher average of the remaining scores. For a group of $n$ applicants with mean examination score $\bar E$, the other-applicant mean is

$$
\bar E_{-i}=\frac{n\bar E-E_i}{n-1}.
$$

This relationship is more pronounced in small observed groups. For example, in origin 123, the applicant scoring 9.28 has a peer average of 7.446 and appears in equal-width bin 10; the applicant scoring 5.66 has a peer average of 8.17 and appears in bin 13. Both belong to the same originating gymnasium. The higher scorer entered designated mathematics program `xx8`; the lower scorer entered vocational program `xx3`.

This is correct arithmetic for the agreed peer definition. It is not, by itself, evidence that the higher peer average caused the lower scorer's placement. It demonstrates why a curve mixing different own-score levels and small groups cannot establish a congestion mechanism on its own. No peer definition was changed.

### Finally we counted gymnasiums behind the upper bars

- **Equal-width bin 10:** 545 applicants, 60 successes, 29 gymnasiums.
- **Equal-width bin 11:** 367 applicants, 52 successes, 14 gymnasiums.
- **Equal-width bin 12, the peak:** 129 applicants, 38 successes, five gymnasiums. Origin **108** supplies **123 of the 129 applicants (95.35%) and all 38 successes**. The other four gymnasiums collectively supply six applicants and no successes. This peak is therefore dominated by one source-coded environment.
- **Equal-width bin 13:** two applicants from two gymnasiums, both described above. Bins 14 and 15 are empty; bin 16 contains the single strong applicant with one observed peer.
- **Quantile bins 11–16:** respectively 17, 12, 12, 16, six, and eight gymnasiums. These are per-bar counts, not disjoint sets; applicants from one gymnasium can fall in different bars because each has a different other-applicant average.
- **Quantile bin 15, the dip:** 178 applicants and nine successes from six gymnasiums. Origins 141 and 274 supply 77 and 69 applicants, respectively—146 of 178. Thus its apparent sample size should not be mistaken for 178 independent peer environments.
- **Quantile bin 16, the rebound:** 178 applicants and 38 successes from eight gymnasiums. Origin 108 again supplies 123 applicants and all 38 successes. These are the same successful applicants seen in equal-width bin 12, not an independent replication.

### What this check changes in our interpretation

The first HERO remains useful: it connects actual selective placement to observed gymnasium peer performance. The broad positive association has support across multiple gymnasiums. But its tallest bar is dominated by one gymnasium, and its extreme-right zeros arise from two lower examination scorers plus one strong applicant whose destination falls outside our narrow designated set. This inspection weakens a congestion interpretation of the dramatic right-edge fall. It does not invalidate the dataset or justify deleting inconvenient observations.

The bounded check is complete. The next scientific discussion should distinguish own examination performance from peer environment, rather than treating this unadjusted right edge as a demonstrated band-of-excellence penalty. Any further calculation, denominator comparison, or model remains a separate decision.

**Direct sources:** [saved run summary](../../outputs/romania_alba_2001_hero_v1/run_20260930T181101_938202Z/summary.json), [name-free applicant audit](../../outputs/romania_alba_2001_hero_v1/run_20260930T181101_938202Z/baseline_include_vocational/name_free_applicant_outcome_audit.csv.gz), the same run's `fixed_bin_edges.json` and two bin CSV files, the saved `program_cutoffs.json` under `romania_alba_2001_program_cutoffs_20260930/`, and the structural audit's `origin_school_directory.json`. Generated applicant-row numbers identify rows within an origin code; they are not historical personal identifiers.

## September 30: user-controlled top-two comparison

Charles authorized broadening success to the highest and second-highest cutoff tiers within each original subject. The existing notebook now exposes `TOP_PROGRAM_TIERS = 2` in its first settings cell. Setting 1 restores the original definition. A tier is a distinct reported cutoff among fully occupied programs; all programs tied at either included cutoff count. Thus two tiers can contain more than two programs. This remains a program-level definition, not a whole-school ranking.

The setting is passed to the program preview, independent reconciliation cell, and HERO execution. The selected number appears in the output-folder suffix, plot title, narrated report, summary, and run record. A fixed reference to Charles's saved original run (`run_20260930T181101_938202Z`) verifies that applicant identities, scores, destinations, peer averages, and denominator eligibility are unchanged. The exact original bin boundaries are reused. The original run is never overwritten. Acquisition is set False in the notebook because the saved placement reports suffice.

Seventeen offline synthetic tests passed, including cumulative tier selection with ties, exclusion of unfilled programs, propagation to actual placement labels, preservation of the reference population and bins, and output metadata. Notebook settings were also checked through preview/reconciliation/HERO calls using stubs only. No empirical two-tier result was calculated by VECTOR.

At this checkpoint, the meaning of the requested three-category option remained open. The subsequent implementation and its explicit meaning are recorded below.

## September 30: visible occupancy and category switches

Charles requested the ability to explore programs that did not fill all their seats and reiterated his request for the combined-category option. Both switches now appear in the notebook's first settings cell:

```python
REQUIRE_FULL_PROGRAMS = True
COMBINE_PROGRAM_CATEGORIES = False
```

**Occupancy:** With `REQUIRE_FULL_PROGRAMS = True`, only fully occupied programs qualify for ranking. With `False`, partially filled programs also qualify, provided they have positive capacity, at least one admitted student, and a finite observed last-admitted score. Empty programs and missing cutoffs remain excluded. A partially filled program's last-admitted score does not demonstrate that applicants were turned away for lack of seats. This is a change to our descriptive destination definition, not evidence of a capacity constraint.

**Combined categories:** With `COMBINE_PROGRAM_CATEGORIES = False`, ranking uses the six original subjects. With `True`, ranking uses three groups: mathematics/informatics plus natural sciences; social sciences plus philology; and technology plus vocational. The highest distinct cutoff tiers are selected afresh within each combined group, including ties. This can reduce the number of designated destinations relative to choosing the same number of tiers in each of six subjects. It changes which placements count as success; it is not simply a relabelling of the graph.

**Preserved personal settings:** Charles's saved notebook had `TOP_PROGRAM_TIERS = 1` and `INCLUDE_VOCATIONAL_IN_OUTCOME_DENOMINATOR = False`. Those values were preserved. He can change them alongside the new switches. The original top-one baseline remains saved separately.

**Interaction with vocational exclusion:** Allowing partially filled programs can make a vocational destination qualify as a success. If vocational placements are excluded from the outcome population, both those applicants and any qualifying successes must be removed. The code now reports both numbers explicitly. Their records remain in the frozen population used to calculate other applicants' peer averages.

**Review and reproducibility:** The preview lists ranking group, cutoff tier, original subject, destination, cutoff, and occupancy. Plot titles, output folders, reports, summaries, and run records identify the settings used. Existing population and bin-boundary checks remain in place. Twenty tests using artificial data passed, including the new occupancy choices, combined-group reranking, and removal of vocational successes. Notebook calls were checked with test substitutes for all four boolean combinations. No empirical notebook cells, acquisition, or HERO analysis were run by VECTOR for this update; Charles remains the operator of the actual runs.
