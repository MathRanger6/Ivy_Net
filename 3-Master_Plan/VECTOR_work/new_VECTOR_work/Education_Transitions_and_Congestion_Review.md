# Education — school standing, college access, and later attainment

**Last synced:** 2026-09-24  
**Status:** VECTOR working note for discussion with Charles. Read-only evidence and source review; no regressions, experiments, pipeline changes, or figure rebuilds. Proposed tests require separate approval.

## Recommendation

Examine education as **successive transitions between peer environments**. Distinguish sorting into a high school, standing within that school, access to a postsecondary destination, and completion after entry. Competition for selective college access could operate before college begins. The current degree-completion outcome combines these stages.

The most immediate comparison is entry versus completion using the existing panels, after validating their outcome coding. The closest match to Alex's specific question is access to a particular type or selectivity of college; that requires fields absent from the supplied extracts. Neither route presupposes a hidden negative effect.

## What Alex actually asked

In **PD41, September 22**, Charles suggests that congestion appears in college rather than high school (01:27–01:45). At **03:16–03:25**, Alex asks whether the college attended is available and recalls discussing its prestige. This is an inquiry about the destination measure, not a conclusion that school prestige has already been constructed. At **04:51–05:15**, Alex recommends not giving up on education, allowing roughly a day of focused work, and explicitly accepts that it might not work. At **06:55–07:48**, assortativity remains first, with education a bounded second investigation and presentation restructuring afterward. [R1]

**PD30, September 4**, supplies the earlier rationale: understand the variables and consider whether Alex's heavily processed panels retained what the model actually needs (06:00–07:30). Additional domains were a supplementary effort rather than the main time sink (07:30–09:09). **PD40, internally dated September 17**, frames local comparison as a congestion hypothesis and leaves assortativity's necessity open (27:18–29:35). Its filename incorrectly begins 20290917. PD30 and PD41 were read in full; PD40 was searched and its relevant passages inspected. [R2–R3]

The proposition that admissions competition might be visible through high-school context is Charles's current question and VECTOR's proposed interpretation. It is not attributed to Alex as an established result.

## What is actually available

**NELS:88:** the supplied panel has 10,545 student rows and 49 columns. The school identifier represents the tenth-grade high school; the panel describes the original 1988 eighth-grade cohort. It retains own performance, sampled-school peer means and standing, socioeconomic status, demographic fields, follow-up weights, and indicators for high-school diploma, any postsecondary education, associate-or-higher, and bachelor-or-higher attainment by 2000. It includes baseline reading and history score fields. [R4]

**HS&B:80:** the supplied panel has 22,889 rows and 59 columns, covering separate Sophomore and Senior cohorts. It retains corresponding school-standing variables, socioeconomic status, weights, school characteristics, grade/program fields, and high-school, any-postsecondary, two-year-or-higher, and BA-or-higher outcomes by 1986. Follow-up horizons differ by cohort. Do not pool the cohorts as if they shared the same age or time to complete a degree. [R5]

**Neither extract contains a college identifier, college name, selectivity/prestige field, application record, or admission decision.** Their school identifiers refer to high schools. The dataset directories contain the CSV and Alex's source email, not the original extraction program, raw NCES files, or codebook. A repository text search did not locate the original outcome-construction code. [R4–R6]

The row/column counts and field inventory above come from direct, read-only inspection. They do not validate all recodes or reproduce substantive results.

## What the existing results say

Saved September 22 overlap metadata report school sorting of approximately **0.251 (NELS), 0.284 (HS&B Sophomore), and 0.324 (HS&B Senior)**, on analytic samples of **7,238**, **12,184**, and **9,874** respectively. These are saved results, not newly estimated or independently reproduced values. Positive sorting is not proof of a particular homophilic assignment mechanism. [R7]

I inspected all three saved nine-panel mosaics. The overall BA-versus-peer-quality displays rise substantially; the fixed high-ability and top-20-percent displays also generally rise. Thus merely restricting to the existing high-ability bands has already been tried. The current figures do not supply evidence of a high-peer-quality penalty under those specifications. [R8]

The plotting implementation bins outcomes without survey weights. Its “fixed ability” probe restricts a restandardized score to a band from one to two standard deviations; it does not hold each student's ability exactly constant or adjust for socioeconomic differences. Its Wilson intervals are not a survey-design or school-cluster correction. These figures remain descriptive screens. [R9]

The primers contain mixed historical status statements, including obsolete “not wired yet” text and assertions that the no-homophily congestion question is already answered. Existing code and outputs contradict the former; our PD41 question remains open. The description of education as non-top-K attainment does not establish that earlier educational transitions lack competition. No primer was modified. [R10]

## The scientific lens

### School context may support learning and alter local standing

Compare students with similar prior measured performance and background who occupy different positions in their sampled high-school distributions. Stronger peers could provide information, academic expectations, and support while also lowering a student's relative standing. Limited recommendations, counseling attention, or distinctions are possible congestion mechanisms; these resources are not directly measured in the current panels.

A rank association could also reflect confidence or aspirations rather than competition for a fixed resource. Do not equate every negative rank/context association with the model's congestion penalty. In particular, a rising overall outcome curve can coexist with an offsetting cost, but it can also reflect no such cost. The current evidence does not choose between those explanations.

The relevant competition pool must be justified. A high-school cohort can be a local comparison group without being the complete applicant pool for a college. There is no evidence here of a fixed admissions quota per high school. Likewise, sampled classmates are not a census of peers: sample size is not a school's true capacity, and sampled test-score rank is not necessarily the rank perceived by teachers, admissions officers, or the student.

### Separate entry from completion

Let $E$ denote any postsecondary entry by the follow-up, $B$ denote BA-or-higher completion by that follow-up, and $X$ denote baseline performance, school context, and other declared covariates. If $B=1$ implies $E=1$, then

$$
P(B=1\mid X)
=
P(E=1\mid X)\,
P(B=1\mid E=1,X).
$$

This is a probability identity, not a causal decomposition. The panels' binary values are consistent with this nesting, but their source coding must still be checked. “Any postsecondary” includes pathways broader than selective four-year college admission. Among entrants, noncompletion by the follow-up does not necessarily mean dropout or permanent failure.

Comparing the two stages can localize an association that the final BA indicator hides. Conditioning on entry changes the selected population, however; it does not isolate a causal college-stage effect.

### Recover destination quality if feasible

Alex's prestige question suggests an outcome such as **first entry to a specified selectivity tier**, while retaining nonentrants and other destinations in the baseline population. Record first institution rather than silently substituting the degree-granting institution, which is observed only for completers and may follow transfers. Use historically appropriate selectivity, distinguished from prestige and from an institution's resources.

NCES's NELS analysis documents student reports of two institutions applied to and acceptance at those institutions. That is evidence that the parent study contains a closer admissions measure, not proof that a complete application set is available in our extract. [W1] NCES also lists linkable Barron's admissions-competitiveness data as restricted-use, and PETS among restricted-use supplemental files. Exact variable availability, linkage keys, and Charles's access remain unverified. Prefer checking existing public-use categories before planning a restricted-data project. [W2–W3]

Admission and enrollment must remain separate: enrollment also reflects applications, offers, finances, location, and student choice. Even a valid destination measure would not by itself measure peer congestion after entering college. That requires a defensible college peer group and appropriately timed measures.

## A bounded next test, for approval

**Scientific question:** At comparable prior measured performance, does local school standing relate differently to postsecondary entry and later completion, and is there a feasible destination measure closer to selective advancement?

**First prerequisite:** inspect the exact NCES codebook and the extraction recipe. Verify the performance composite, cohort timing, sampled-peer construction, weights, and all outcome recodes. In NELS, the supplied degree code -3 maps to zero entry and zero BA, while -9 maps to missing. That may reflect a legitimate no-PSE skip, but it must be checked against the original question universe and attendance fields; this review does not declare it a coding error. HS&B's attainment categories likewise need their original labels.

**Proposed initial comparison:** start with NELS's more mature 2000 horizon. Examine the declared entry outcome and BA outcome, plus descriptive completion among entrants, using the same baseline population wherever the estimand permits. Use school peer mean and one explicitly defined standing measure, with flexible control for baseline performance and pre-specified socioeconomic covariates. Verify common support, rank ties, and sample-peer reliability before interpretation. Treat HS&B Sophomore and Senior as separate follow-on comparisons.

**Held fixed:** source files, cohort and baseline definitions, peer construction, covariate timing, weight choice, and declared readouts. Completion-among-entrants necessarily changes the risk set and must be labeled as such. Do not successively change bins or sample thresholds to obtain a downturn.

**What changes:** the outcome stage and the declared standing readout. If source access allows a later destination comparison, its categories and risk set must be specified separately. Do not include own ability, peer mean, and their exact difference as three independently identified linear predictors. Do not automatically control for later GPA or aspirations if those are candidate mediators.

**Interpretation of possible results:**

- An adverse standing/context association concentrated in entry would motivate investigating access, application, or local recognition mechanisms; it would not prove a fixed admissions quota or a causal congestion effect.
- An association concentrated in completion among entrants would motivate investigating persistence and destination composition; selection into entry remains an alternative explanation.
- A difference only for selective destinations would make broad BA attainment an insufficient readout of that access question, provided the destination measure is valid.
- Continued positive or null conditional associations would support reporting no adverse association under this specification. They would not establish the absence of all congestion, nor justify searching indefinitely for a hump.

**Files and provenance:** source panels R4–R5 would remain unchanged. No modification of R9 or existing outputs is proposed for this review. Before execution, specify the new analysis file and separate output location, the final model and uncertainty procedure, and the complete data dictionary. Do not overwrite September 22 results. School clustering and appropriate survey-design information need to be addressed; follow-up weights alone are not a complete design correction.

## Published mechanism leads

Elsner and Isphording's *A Big Fish in a Small Pond* (Journal of Labor Economics, 2017) reports associations identified using cohort-composition variation within schools, with rank affecting later school completion and college attendance; expectations and perceived intelligence are candidate channels. The published abstract was inspected. Our current extracts do not automatically reproduce that identification strategy. [W4]

Murphy and Weinhardt's *Top of the Class* (Review of Economic Studies, 2020) distinguishes ordinal rank from prior achievement and studies later outcomes and confidence using English school data. Relevant identification and mechanism passages were inspected. It motivates keeping school quality and standing conceptually separate; it does not establish an effect in NELS or HS&B. [W5]

These are targeted literature leads, not completed paper readings or companion volumes. Any deeper review should use our established source-fidelity and mechanism-extraction methodology.

## Sources actually inspected

- **R1:** [PD41, September 22 (full transcript)](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20260922_Paper_Directions_41_otter_ai_transcript.docx>).
- **R2:** [PD30, September 4 (full transcript)](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20260904_Paper_Directions_30_otter_ai_transcript.docx>).
- **R3:** [PD40, internally September 17, 2026 (relevant passages)](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20290917_Paper_Directions_40_otter_ai_transcript.docx>).
- **R4:** [NELS supplied panel](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/datasets/nels88/nels88_big_fish_panel.csv>).
- **R5:** [HS&B supplied panel](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/datasets/hsb80/hsb80_big_fish_panel.csv>).
- **R6:** [Alex's dataset description (email body; no outgoing message)](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/datasets/nels88/Re_ New dataset for Big Fish.eml>).
- **R7a:** [NELS saved sorting metadata](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/nels88/basic_data_plots/NELS88_team_interval_overlap_meta.json>).
- **R7b:** [HS&B Sophomore saved sorting metadata](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/hsb80_soph/basic_data_plots/HSB80SOPH_team_interval_overlap_meta.json>).
- **R7c:** [HS&B Senior saved sorting metadata](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/hsb80_senior/basic_data_plots/HSB80SEN_team_interval_overlap_meta.json>).
- **R8a:** [NELS saved mosaic](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/nels88/data_story/NELS88_DATA_STORY_3x3.png>).
- **R8b:** [HS&B Sophomore saved mosaic](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/hsb80_soph/data_story/HSB80SOPH_DATA_STORY_3x3.png>).
- **R8c:** [HS&B Senior saved mosaic](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/education_sandbox/hsb80_senior/data_story/HSB80SEN_DATA_STORY_3x3.png>).
- **R9:** [Existing data-story implementation (education loaders and plot routines)](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/scripts/big_fish_data_story.py>).
- **R10a:** [Earlier education primer](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/education_dataset_primer.md>).
- **R10b:** [Researcher education primer](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/EDUCATION_dataset_primer.md>).
- **W1:** [NCES, Access to Postsecondary Education: application, acceptance, and enrollment](https://nces.ed.gov/pubs98/access/98105-13.asp).
- **W2:** [NCES, NELS overview and Barron's linkage access](https://nces.ed.gov/surveys/nels88/).
- **W3:** [NCES, available NELS data products (indexed text inspected; direct retrieval failed)](https://nces.ed.gov/surveys/nels88/data_products.asp).
- **W4:** [Elsner and Isphording (2017), published abstract](https://www.journals.uchicago.edu/doi/10.1086/690714).
- **W5:** [Murphy and Weinhardt (2020), published article passages](https://academic.oup.com/restud/article/87/6/2777/5831842).

## Addendum — targeted request to augment the education data

**Added:** September 24, 2026.  
**Access update:** Charles reports that a faculty colleague has the source access through which the original panels were obtained. This updates the earlier access discussion; the colleague's available files, linkage keys, and permitted working arrangements have not yet been independently verified. No new data have been received or analyzed.

Begin with **the same NELS:88 students**, with HS&B as a second step. Our existing panels already contain achievement, sampled-school peer measures, and degree outcomes. The largest gaps for this question are **where students applied, whether they were admitted, and where they enrolled**. These additions would help examine whether competition matters on the way into college, even when eventual degree attainment shows no downturn.

### Request to pass to the faculty colleague

Please help us augment the education panels previously supplied, beginning with **the same NELS:88 students**, using a stable student identifier that links to our existing extract. Please retain students who never entered college, did not graduate, or have missing follow-up information.

Our priorities are:

1. **College destinations and historical selectivity.** Please include the identifier of the first postsecondary institution attended, entry date, and institution type: two-year/four-year and public/private. Add historical admissions selectivity, preferably the NCES–Barron's 1992 classification or another documented measure appropriate to the attendance period. Where available, include separate identifiers for subsequent institutions and the institution awarding each degree. Distinguish an institution without a selectivity rating from a nonselective institution.

2. **Applications and admission decisions.** Please include each recorded college application, its institution identifier, survey wave or application year, and reported admission decision. Preserve accepted, rejected, pending, unknown, and missing responses separately where the questionnaire distinguishes them. Retain actual enrollment separately from admission. Include the questionnaire wording and any limit on the number of institutions respondents could report. Distinguish directly reported applications from applications inferred because a student subsequently enrolled.

3. **Actual high-school standing and academic preparation.** Please include transcript-reported class rank and graduating-class size, including NELS variables `F2RRANK` and `F2RCSIZE`, if present in your release. Include high-school identifiers at each available wave, particularly tenth and twelfth grade, and school-transfer information. Please also include GPA, SAT/ACT results, repeated achievement scores, and academic coursework, with measurement dates and source labels. These would supplement our existing rank measures, which describe sampled students rather than necessarily the entire graduating class.

4. **Enrollment and completion timing.** Please include first enrollment date, attendance spells, transfers, degree type and award date, and latest observed enrollment status. Include the original attendance and attainment variables underlying the binary outcomes already supplied.

5. **Documentation needed to use the augmentation correctly.** Please include the dataset release, source variable names, labels, question universes, missing/skip codes, and imputation flags; appropriate longitudinal weights and available survey-design variables or replicate weights; and the extraction and recoding script used to construct our existing panels, if available.

If readily available, a second priority is students' educational expectations across waves, college counseling or application assistance, family income and parental education, and financial-aid information.

For **HS&B**, please identify comparable destination and application fields separately for the senior and sophomore cohorts. We would also like the sophomore cohort's 1992 attainment follow-up to extend our current 1986 outcome horizon.

Please indicate which requested fields are available and the appropriate way to work with them under the existing access arrangement.

### Why these additions come first

**Selectivity linkage is feasible in principle.** NCES provides historical Barron's classifications with institution identifiers, including a 1992 file. This establishes that a linkage resource exists; it does not establish that our colleague has compatible identifiers or this particular file. Historical selectivity should remain distinct from prestige and from institutional resources. [A1]

**NELS application histories are incomplete by design.** The documented questions requested two institutions and acceptance information. Some published application measures also incorporate enrollment-inferred applications. We need those distinctions preserved rather than treating the records as a complete application set. [W1; A2]

**Actual class rank is a useful addition.** NCES documents transcript rank and class size as the inputs to its class-rank measure. These fields address a different measurement question from our sampled test-score rank. The longer HS&B follow-up applies specifically to the sophomore cohort. [A2–A3]

**Recommended minimum:** prioritize destinations/selectivity, applications/decisions, and actual school rank, together with their documentation. They would help locate where differences emerge along the educational pathway. They would not by themselves establish congestion. Measuring selection scarcity more directly would additionally require historical institution-year applicant counts, admission offers, and entering-class size, where available; obtaining those is a possible later extension, not a prerequisite for the initial request. Those counts would still not identify a fixed admissions quota per high school or competition among college peers.

This addendum records a data request, not approval to run an analysis. The earlier distinctions between application, admission, enrollment, and completion remain in force, as do the source-coding audit and the need to distinguish later mediators from baseline covariates.

### Supporting sources for the addendum

- **A1:** [NCES–Barron's Admissions Competitiveness Index Data Files](https://nces.ed.gov/use-work/dataset/nces-barrons-admissions-competitiveness-index-data-files-1972-1982-1992-2004-2008-2014). The official dataset description identifies historical ratings, institution linkage identifiers, and restricted-use status.
- **A2:** [NCES, Access to Postsecondary Education for the 1992 High School Graduates](https://nces.ed.gov/pubs98/98105.pdf), Appendix A, printed pages 80 and 85. The glossary identifies `F2RRANK` and `F2RCSIZE` as inputs to class rank and explains that the derived `EVR4YRA` application measure also counts reported four-year enrollment. These are documentation leads; field availability in the colleague's release still needs confirmation.
- **A3:** [NCES, HS&B Survey Design](https://nces.ed.gov/surveys/hsb/surveydesign.asp). The fourth follow-up in 1992 focused on the 1980 sophomore cohort.
- **W1, revisited:** [NCES, application, acceptance, and enrollment documentation](https://nces.ed.gov/pubs98/access/98105-13.asp). The survey asked students to name two institutions applied to and whether they were accepted.
