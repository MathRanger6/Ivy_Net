# Education B — classroom / roommate / cohort peer effects: source note

**Purpose:** verbatim, page-cited extracts for the EDUCATION background subsection of the dissertation introduction. Not dissertation prose.

**Conventions**

- "p. N" = printed journal (or working-paper) page number. "PDF p. M" given when it differs.
- Quotes are copied from the PDF text layer (`pdftotext -layout`). Hyphenation at line breaks is rejoined; nothing else is changed unless marked `[OCR fix: ...]` (only for the scanned Sacerdote 2001 JSTOR copy, whose text layer contains OCR character errors). Hoxby 2000's PDF has no usable text layer; it was OCR'd with tesseract, so Hoxby quotes are OCR output checked for obvious errors.
- Limitation tags: [small data], [imperfect measure], [single system], [no model of mechanism], [model not fit to data], [outcome is not selection].
- "Channel / source" lines are **assistant judgment**, not the authors' claims. Channels: development (what a person becomes), evaluation (how a performance is measured/perceived), selection (who wins a scarce slot). Sources: peers vs organization.

**Contents** — numbered as in the request; sections appear in the order written (Hoxby §1 was written after Lyle §9 because its PDF needed OCR): §2 Sacerdote 2001; §3 Carrell, Fullerton & West 2009; §4 Carrell, Sacerdote & West 2013; §5 Booij, Leuven & Oosterbeek 2017; §6 Feld & Zölitz 2017; §7 Duflo, Dupas & Kremer 2008 WP; §8 Jackson & Bruegmann 2009 WP; §9 Lyle 2007; §1 Hoxby 2000 WP; §10 Angrist 2014; §11 Sacerdote 2011 & 2014 (abstract-only).

---

## Assistant synthesis (ASSISTANT SYNTHESIS, not source text)

1. **Sign and size.** Random or quasi-random peer variation usually gives positive but modest average effects on academic outcomes: about +.05 GPA per SD of roommate GPA at Dartmouth (an outcome-on-outcome correlation; the causal roommate-background effects are "modest"), +.05 grade points per SD of peer SAT-verbal in USAFA squadrons, +1.26% of an SD per SD of peer GPA at Maastricht, and 0.15–0.4 points per point of peer score in Texas cohorts. At West Point the effects are close to zero once common shocks are handled (§§1–3, 6, 9).
2. **The estimate depends on definition and measurement.** Roommates and dorm floors understate the effect relative to the full assigned cohort (CFW 2009). Measurement error and weak-instrument mechanics can create or inflate "peer effects" (Angrist 2014; Feld & Zölitz 2017) [imperfect measure].
3. **Averages hide winners and losers.** In Maastricht sections, high-achieving peers help high- and middle-GPA students but hurt low-GPA students (Feld & Zölitz). In Amsterdam, low-ability students gain from able peers only in heterogeneous groups and are hurt by heterogeneity in low-ability groups (Booij et al.). In Kenya, peer gains appear at the top and bottom but not in the middle quartiles (DDK). In Texas, effects are strongest within racial groups (Hoxby).
4. **The CSW 2013 policy test.** Nonlinear reduced-form estimates from randomly assigned squadrons predicted a +0.053 gain for the bottom third. Implementing them produced −0.061 for that group and +0.082 for middle-ability students.
5. CSW attribute the reversal to endogenous subgroup formation (homophily in study partners and friends) that their reduced-form model did not contain. They conclude: "Regrettably, we do not now see such a methodology." Angrist instead reads the reversal as evidence that the pre-treatment estimate was spurious. On either reading, reduced-form peer coefficients do not carry over to new group configurations [no model of mechanism].
6. **Mechanisms are rarely modeled, and the models are not fit.** DDK is the exception: a model of teacher targeting under convex, exam-linked rewards, tested only by rejecting special cases [model not fit to data]. Jackson & Bruegmann use a verbal framework. The rest offer survey correlates or speculation.
7. **What is left open for selection among competitors for scarce slots:**
   - Every outcome is a grade, test score, credit count, or individual choice (major, fraternity, staying in the Army); none is a contest for a fixed number of slots [outcome is not selection]. CFW state outright that USAFA has "no explicit grading curves," so one student's gain is not another's loss. Booij et al.'s dropout outcome is an absolute 45-credit threshold.
   - Each study uses one institution or one state [single system], often with few independent groups (48 tutorial groups; 108 squadrons) [small data].
   - No study models how peers shift evaluation or rank in a competition. The closest are Jackson & Bruegmann, who show colleagues contaminate individual value-added evaluation, and DDK, where a later selection exam shapes teacher effort.

---

## 2. Sacerdote (2001) — Dartmouth roommates

**Citation.** Sacerdote, Bruce. 2001. "Peer Effects with Random Assignment: Results for Dartmouth Roommates." *Quarterly Journal of Economics* 116(2): 681–704. DOI 10.1162/00335530151144131. (PDF is a scanned JSTOR copy; printed pp. 681–703 = PDF pp. 1–23.)

**Data / setting.** Dartmouth College (US), graduating classes of 1997 and 1998; freshmen randomly assigned to dorms and roommates after a 1993 policy change. Start sample 2,181; final N = 1,589 (drops singles, substance-free dorm, missing housing forms, special roommate requests) (p. 686). Outcomes: GPA (freshman–senior), time to graduation, fraternity/sorority membership, choice of major, varsity athletics (p. 684). Pre-treatment: SAT, HS class rank, admissions "academic index," UCLA HERI freshman survey (beer use, honors expectation) (pp. 684–685).

**Design.** Random assignment within 32 blocks defined by gender and four housing-form questions (smoke, music while studying, late hours, neat); forms shuffled by hand (p. 685). Balance test: own background regressed on roommate background; F-test p = .78 (Table II, p. 689).

**Main findings (verbatim).**

> "I find that peers have an impact on grade point average and on decisions to join social groups such as fraternities. Residential peer effects are markedly absent in other major life decisions such as choice of college major." (abstract, p. 681)

> "The coefficient on roommate GPA implies that a one-standard-deviation increase in roommate GPA is associated with a .05 increase in own GPA. This coefficient is moderate in size and seems plausible given that we are dealing with students who have reached college age and have already been heavily prescreened for admission to Dartmouth." (p. 694)

> "If my freshman year roommate joins a fraternity, I am 8 percent more likely to do so myself." (p. 699); dorm-level participation coefficient "of 32 percent" (p. 700).

- Outcome-on-outcome coefficient = .12 (t = 3.1), but "One cannot give this coefficient a causal interpretation due to the reflection problem created by regressing outcomes on outcomes." (p. 694) [OCR fix: "refiection" → "reflection"]
- The roommate GPA effect "disappears by senior year" (p. 695).
- Reduced-form (causal) background effects are weaker: "The effects on GPA from randomly assigned roommate background are modest in size and statistical significance." (p. 697)

**Nonlinearity / heterogeneity (who gains, who loses).**

> "The results imply that top roommates can help a student from the bottom of the distribution. Row 3 shows that top roommates also can help a student in the top of the distribution. This last result is significant at the 10 percent level." (p. 701)

> "Bottom roommates do not seem to deliver any effect that is statistically worse than having a middle roommate. ... Furthermore, middle students do not appear to be helped or hurt much by their roommates." (p. 701)

- Table VI (p. 702): own-bottom/roommate-bottom −0.331 vs own-bottom/roommate-top −0.160 (p = .013). Redistribution experiment 1 (mix top+bottom): net "social gain" .14, p = .42 — "does not yield statistically significant gains" (Table VI notes, p. 702). [OCR fix in notes: "eacb"/"hottom" read as "each"/"bottom"]
- Caveat on redistribution: "such results on redistribution of students are certainly more suggestive than conclusive." (p. 702)
- Earlier summary: "The data do not provide strong evidence that the peer effects on grade point average (GPA) and fraternity membership are nonlinear in roommate's background or outcomes." (p. 683)

**Model / mechanism.** Simple linear framework (eqs. 1–4, p. 691): own GPA on own ability, roommate ability, roommate GPA; reduced form estimated by OLS. Mechanisms not distinguished: "peer effects observed in the data may work through a variety of mechanisms, and I do not distinguish among these." (p. 683). Structural parameters (contextual vs endogenous) require "very restrictive assumptions" (p. 691). → [no model of mechanism]

**Sorting vs effect.** Random assignment conditional on housing-question blocks; balance shown; in earlier non-randomized classes "roommate math SAT predicts own SAT with a t-statistic of 5.0" (p. 690). [OCR fix: "(-statistic" → "t-statistic"]. Common-shock check: dorm fixed effects; random non-roommate floor member shows no correlation (p. 697).

**Limitations (authors' words where possible).**

- [single system] "The students are older, live on campus, and are a highly selected group." (p. 683); "A fruitful area of future research would be to examine similar data in other educational settings." (p. 703)
- [small data] N = 1,589, two cohorts; honors-expectation variable "only available for one-third of the sample" (p. 696); peer-vs-own ratio "not particularly robust" (p. 696).
- [imperfect measure] "We do not observe actual ability, but instead noisy measures of ability such as SAT scores and high school class rank." (p. 690)
- Roommates are a partial peer set: "My estimates based on roommates alone will be very much a lower bound on the total peer effects that influence GPA." (p. 690)
- [outcome is not selection] Outcomes are GPA and club membership; choice of major (a choice, not a scarce slot) shows no effect.

**Channel / source (assistant judgment).** Development (GPA, social behavior) via peers (roommates). Fraternity joining is a peer-influenced *choice* into a social group, not a competitive scarce slot. Evidence of heterogeneity: top roommates help bottom students; no group clearly hurt.

---

## 3. Carrell, Fullerton & West (2009) — US Air Force Academy squadrons ("Does your cohort matter?")

**Citation.** Carrell, Scott E., Richard L. Fullerton, and James E. West. 2009. "Does Your Cohort Matter? Measuring Peer Effects in College Achievement." *Journal of Labor Economics* 27(3): 439–464. DOI 10.1086/600143. (Printed p. 439 = PDF p. 1; printed p = PDF p + 438.)

**Data / setting.** United States Air Force Academy (USAFA), graduating classes 2005–2007; Table 1 N ≈ 3,490 students (p. 446); "108 separate squadron peer groups with an average of 32.7 freshman students" (p. 447). Outcome: course grades in mandatory core courses (4.0 scale); persistence into sophomore–senior years. Roommates matched for "approximately two-thirds of freshman students" via dorm key logs (p. 447).

**Design.** Stratified random assignment to squadrons by admissions office (females, then minority males, then recruited athletes, then prep-school attendees, then the rest) (p. 444). Freshmen "are not allowed to enter the premises of another squadron" for 7 months (p. 444). Registrar assigns core course sections; "Students have no ability to choose their professors" (p. 446). Randomization check: SD of peer-group SAT verbal 11.4 vs 11.7 expected under random assignment (p. 447).

**Main findings (verbatim).**

> "For freshman students, a 100-point increase in the peer-group average SAT verbal score increases individual GPA by roughly .4 grade points on a 4.0 scale." (p. 441)

> "The model estimates that a 1 standard deviation increase in peer SAT verbal results in an increased own GPA of .05 grade points (one-twelfth of a standard deviation). In terms of standard deviations, this effect is nearly 2.5 times greater in magnitude than that found by Zimmerman (2003) for roommates at Williams College." (p. 455)

> "Results provide strong evidence that the freshman peer effects persist into follow-on academic performance but at a diminished rate roughly one-half in magnitude." (p. 457)

- Peer group definition matters: "roommates and dorm floors capture only a limited proportion of an individual's peer group" (p. 441); false (geographic) peer groups containing ~67% of actual squadron show "virtually undetectable" effects (p. 460).
- Effects largest in math/science (peer SAT verbal .509), absent in PE and foreign language (pp. 455, 457).

**Nonlinearity / heterogeneity.**

> "The magnitude of the estimated effect for students in the bottom third of the academic ability distribution (.565) is larger, although not statistically different, than that estimated for students in the top (.312) and middle (.361) third of the distribution. These results indicate that the lowest ability students in the sample may benefit the most from having high-quality peers." (pp. 459–460)

- This nonlinearity is the basis for the later CSW 2013 intervention: "These results suggest there may be an opportunity for social gains through sorting individuals into peer groups." (p. 462)
- No evidence anyone is hurt here (all thirds positive).

**Model / mechanism.** Reduced-form linear-in-means regressions on peer pre-treatment characteristics (eq. 1). Mechanism is speculation: "the peer effects may be working through study partnerships versus a social norm of effort. ... But we recognize that this hypothesis is not testable within our models as specified." (p. 457); "Again, we can only speculate, but after informal discussions with faculty and students ..." (p. 457). → [no model of mechanism]

**Sorting vs effect.** Random squadron assignment + registrar-assigned sections; course-by-section fixed effects to absorb common shocks (p. 447 fn. 19). Uses exogenous pre-treatment peer traits (reduced form), not peer outcomes.

**Evaluation detail relevant to selection.**

> "There are no explicit grading curves at USAFA. Therefore, a benefit to one student or group is not, mechanically, at the expense of another student or group." (p. 446, fn. 16)

(Assistant note: this explicitly rules out the zero-sum / scarce-slot setting the dissertation cares about — the outcome is an absolute grade, not a rank-based selection.)

**Limitations.**

- [single system] "We recognize that questions could be raised about the generalizability of our findings, given USAFA students are a subset of traditional college students." (p. 443); "Further information regarding peer group formation at other institutions would be required to empirically test which effect dominates." (p. 444)
- [imperfect measure] Roommates identified only via key logs, ~two-thirds matched (p. 447); peer "quality" measured by SAT verbal / fitness / leadership composites.
- [no model of mechanism] see above (p. 457).
- [outcome is not selection] Outcome = GPA under no grading curve (p. 446 fn. 16).
- Heterogeneity across thirds "not statistically different" (p. 459).

**Channel / source (assistant judgment).** Development via peers (squadron cohort), with the organization designing the peer group (squadron assignment). Peers help, strongest for lowest-ability; no one shown hurt.

---

## 4. Carrell, Sacerdote & West (2013) — "optimally" designed USAFA squadrons backfire

**Citation.** Carrell, Scott E., Bruce I. Sacerdote, and James E. West. 2013. "From Natural Variation to Optimal Policy? The Importance of Endogenous Peer Group Formation." *Econometrica* 81(3): 855–882. DOI 10.3982/ECTA10168. (Printed p. 855 = PDF p. 1; printed p = PDF p + 854.)

**Text-layer caveat.** The PDF text layer drops decimal points (e.g., prints "0053"). Decimals below are restored; the key p. 856 numbers (0.053, −0.061, p = 0.055, 0.082, p = 0.041) were confirmed by OCR of the page image. Other restored decimals marked `[dec.]`.

**Data / setting.** USAFA (US). Pre-treatment (randomly assigned) classes of 2005–2010; experimental subjects = classes of 2011 and 2012 (fall 2007 and 2008 entry) (pp. 856–857). Table I observations: pre-treatment 7,160; control 1,228; treatment 1,219 (p. 858). Outcome: freshman fall-semester GPA in common core courses. Survey of study partners/friends: "usable responses from approximately 25 percent of the experimental subjects" (p. 877).

**Design.** Step 1: estimate nonlinear reduced-form peer effects (coefficients by own predicted-GPA third × fraction of high/low SAT-Verbal peers) on randomly assigned historical squadrons. Step 2: randomly split incoming cohorts; control = random squadrons; treatment = algorithm-sorted squadrons intended to maximize GPA of the bottom third. This produced "bimodal" squadrons (low-ability + high-SAT-V) and "homogeneous" squadrons of middle-ability students (p. 856). Objective set by the organization: "This objective function was determined by USAFA senior leadership, who had a strong desire to reduce the academic probation rate, then at roughly 20 percent." (p. 856, fn. 4)

**Pre-treatment estimate that motivated the policy.** "For Column 4, the coefficient on the fraction of peers in the top quartile of the SAT Verbal distribution is positive and significant for low (0.474) ability students and insignificant for high (0.233) and middle ability students (−0.119)." (p. 860) `[dec.]`

**Key result (verbatim).**

> "We find a negative and significant treatment effect for the students we intended to help. We provide evidence that within our 'optimally' designed peer groups, students avoided the peers with whom we intended them to interact and instead formed more homogeneous subgroups." (abstract, p. 855)

> "The reduced form coefficients (using the pre-treatment data) predicted a Pareto-improving allocation in which grades of students in the bottom third of the academic distribution would rise, on average, 0.053 grade points while students with higher predicted achievement would be unaffected. Despite this prediction, actual outcomes from the experiment yielded quite different results. For the lowest ability students, we observe a negative and statistically significant treatment effect of −0.061 (p = 0.055). For the middle ability students, expected to be unaffected, we observe a positive and significant treatment effect of 0.082 (p = 0.041). High ability students are unaffected by the treatment." (p. 856)

**Their explanation (endogenous peer-group formation / homophily).**

> "When designing the experimental squadrons, the model implicitly assumed that the peer dynamics within the treatment squadrons would remain similar to those observed in the randomly assigned pre-treatment squadrons." (p. 873)

> "Hence, the unexpected results from the experiment could stem from endogenous sorting of students into peer groups in a way that is not fully captured in our model estimated with pre-treatment data." (p. 876)

- Survey decomposition (Table VIII, p. 878): low-ability treatment students 17.1 pp `[dec.]` more likely to have low-GPA study partners; 12.5 pp from composition, 4.6 pp attributed to "additional homophily" (p. 877).
- "low predicted GPA students in the treatment squadrons purposefully selected high SAT Verbal study partners with less frequency (−3.9 `[dec.]` percentage points) than in the control squadrons over and above compositional effects. ... We believe this is a critical piece of evidence in understanding the outcome of our experiment." (pp. 878–879)
- Threshold idea (not modeled): "It is entirely possible that once the fraction of study partners who are low ability reaches a certain threshold, a student's outcomes suffer a great deal." (p. 879)
- Not detectable ex ante: "we find no evidence that the unexpected negative treatment effect could have been predicted, ex ante, in our pre-treatment data" (p. 874).
- Alternative not rejected: "we are unable to reject a related story in which the presence of middle ability students is a crucial part of generating positive peer effects for the lower ability students." (p. 881)

**Policy lesson (verbatim).**

> "On the basis of our experience, we would like to be able to suggest a methodology in which a structural model of peer effects, such as our equation (1), could lead to a reduced form peer effects model, such as our equation (2), which could be used for successful policy predictions. Regrettably, we do not now see such a methodology." (p. 880)

> "We conclude that social processes are so rich and complex that one needs a deep understanding of their formation before one can formulate 'optimal policy.'" (p. 881)

**Model / mechanism.** Structural linear-in-means model (eq. 1, p. 859) with endogenous/exogenous effects varying by ability third; only the reduced form (eq. 2) is estimated and used for the policy. No model of network/friendship formation is specified or fit; homophily is measured descriptively by comparing actual choices to a random-choice simulation (p. 877). → [no model of mechanism] for peer-group formation; [model not fit to data] for the structural eq. 1.

**Sorting vs effect.** Pre-treatment effects from random squadron assignment; the experiment itself randomizes students into treatment vs control. Within-squadron sorting (study partners, friends, second-semester roommates) is the *endogenous* response they document; first-semester roommates are assigned (p. 879 fn. 24).

**Limitations.**

- [single system] USAFA only; two experimental cohorts.
- [small data] [imperfect measure] Survey response ~25%, "response rate was positively correlated with academic ability" (p. 877, fn. 23); roommate data partial: "we obtained a partial list of roommate pairs for the class of 2012" (p. 879).
- [no model of mechanism] "We cannot know with certainty the exact cause of our unexpected treatment effects." (p. 880)
- [model not fit to data] reduced-form extrapolation to squadron compositions that were rare in the historical data ("the bimodality of ability in the treatment squadrons was not commonly present in the pre-treatment data", p. 874).
- [outcome is not selection] Outcome = GPA, though the organization's objective was the academic probation rate (fn. 4, p. 856), which is closer to a retention/selection outcome.

**Channel / source (assistant judgment).** Development via peers, with the **organization** as the designer of peer groups. Strongest evidence in this set that the same peer manipulation **helps some (middle-ability, +0.082) and hurts others (low-ability, −0.061)**, and that reduced-form estimates do not transport to a new configuration because peer interaction is itself endogenous.

---

## 5. Booij, Leuven & Oosterbeek (2017) — randomized tutorial-group composition, University of Amsterdam

**Citation.** Booij, Adam S., Edwin Leuven, and Hessel Oosterbeek. 2017. "Ability Peer Effects in University: Evidence from a Randomized Experiment." *Review of Economic Studies* 84(2): 547–578. DOI 10.1093/restud/rdw045. (Advance access 12 Sept 2016; bib key `booij_ability_2016`. Printed p = PDF p + 546.)

**Data / setting.** First-year bachelor's programme in economics and business, University of Amsterdam (Netherlands), entering cohorts 2009/10, 2010/11, 2011/12. "Approximately, 600 students that enter each year are assigned to tutorial groups of around 40 students" (p. 548). Estimation sample "N = 1,876, N clusters = 48" tutorial groups (Table 4 notes, p. 558). Outcomes: first-year credit points (main; max 60), average grade, and "Drop-out" = fewer than 45 credits, which means students "are not allowed to continue studying in the second year" (p. 555). Survey (~70% response) on peer interaction and teacher behaviour (p. 566).

**Design.** Researchers manipulated each group's shares of three prior-ability categories (secondary-school exit-exam GPA <6.5, 6.5–7, ≥7) and randomly assigned students conditional on category (p. 551). This widened support: mean standardized peer GPA range "[−1] to [1.6]" vs "[−0.3] to [0.3]" under pure randomization (p. 549). Balance test p = 0.94 (p. 555).

**Main findings (verbatim).**

> "When we assess the aggregate implications of these peer effects regressions for group assignment, we find that low- and medium-ability students gain on an average 0.19 SD units of achievement by switching from ability mixing to three-way tracking. Their dropout rate is reduced by 12 percentage points (relative to a mean of 0.6). High-ability students are unaffected." (abstract, p. 547)

> "In summary, we find peer effects for low-ability students, but not for high-ability students. Low-ability students benefit from being with more able peers but not in very homogenous groups, and they are harmed by heterogeneity unless they are placed in a high-ability group." (p. 559)

> "Interestingly, when we simulate the group composition that Carrell et al. believed to be optimal—place low-ability and high-ability students together and keep middle-ability students separate—we reproduce what Carrell et al. find in their experiment: low-ability students are harmed and middle-ability students benefit." (p. 568)

- Three-way tracking reduces dropout of low-GPA students "by 16 percentage points, relative to an average dropout rate for this group of 72%" (p. 562).

**Heterogeneity (who gains, who loses).** Peer response depends on mean, SD, their interaction, and own ability (p. 559). Low-ability students gain from more able peers only in heterogeneous groups, and are hurt by heterogeneity in low-ability groups; high-ability students unaffected. Under the CSW 2013 configuration, low-GPA achievement "goes down by (an insignificant) 2% of a SD" and middle-GPA rises 16% of a SD (p. 550). Authors' policy claim: "This gain comes at no financial cost, nor do we find indications that some groups of students are harmed in the form of lower achievement." (p. 568) (refers to tracking vs mixing)

**Model / mechanism.** Flexible reduced-form "peer response function" in mean/SD of peer GPA; no structural/behavioral model. Mechanisms assessed by survey: "Low-GPA students in tracked groups have more positive interaction with other students and are more involved with their studies than low-GPA students in mixed groups. The survey responses give no support for teachers as a mediating factor" (p. 550). Group size ruled out (p. 550). → [no model of mechanism] (survey correlates only).

**Sorting vs effect.** Random assignment within GPA category; design explicitly addresses extrapolation: "Compared to previous quasi-experimental studies, we do not have to extrapolate beyond the support of our data." (p. 568). They note the optimal assignment problem "is a mixed integer non-linear programming problem for which no general analytical solutions exist" and may lie outside data support (p. 561, fn. 18).

**Evaluation detail.** Exams identical and graded centrally; "It is thus not the case that the grades of students in a tutorial group with many low-GPA peers are inflated to secure a minimum pass rate or average grade within the tutorial group." (p. 551)

**Limitations.**

- [single system] one programme, one university; "Even the non-selective undergraduate programme in economics in our study recruits its students from the top 20% of the ability distribution of their age cohorts." (p. 568)
- [imperfect measure] Assignment used a coarse 3-category GPA (p. 551); peer group partially defined: "We do not claim, however, that the tutorial group is the only peer group, or the most relevant one." (p. 550)
- [small data] 48 tutorial groups (clusters) (p. 558).
- [no model of mechanism] survey-based mechanism evidence only.
- [outcome is not selection] Outcomes are credits/grades; Drop-out (<45 credits) is an absolute threshold for continuation, not a competition for a fixed number of slots.

**Channel / source (assistant judgment).** Development via peers, with the **organization** controlling group composition. Shows the sign of peer exposure depends on the joint distribution (mean × spread × own ability) — same peer mean can help or hurt. Drop-out/continuation is the closest outcome to selection but is threshold-based.

---

## 6. Feld & Zölitz (2017) — randomly assigned sections, Maastricht University

**Citation.** Feld, Jan, and Ulf Zölitz. 2017. "Understanding Peer Effects: On the Nature, Estimation, and Channels of Peer Effects." *Journal of Labor Economics* 35(2): 387–428. DOI 10.1086/689472. (Printed p = PDF p + 386.)

**Text-layer caveat.** Minus signs in tables appear as "2" in the text layer (e.g., "2.1449" = −.1449). Restored below.

**Data / setting.** School of Business and Economics (SBE), Maastricht University (Netherlands), academic years 2009–10 to 2011–12. "In total, we have 7,672 students, 395 courses, 3,703 sections, and 39,813 grades in our estimation sample." (p. 400). Sections of 10–15 students "who spend most of their contact hours together in one classroom" (p. 389). Outcome: standardized course grade; peer quality = peers' past GPA. Course-evaluation survey for channels: "38% of the students start filling out the questionnaire" (p. 412).

**Design.** Section assignment by scheduling software ("allocate randomly"; post-2010 stratified by nationality); "The schedulers do not know the students nor do they observe their previous grades." (p. 399); "neither students nor teachers, and not even course coordinators, have any influence on the composition of the sections in our estimation sample." (p. 400). Randomization test with Guryan–Kroft–Notowidigdo leave-me-out correction (p. 404).

**Main findings (verbatim).**

> "While students benefit from better peers on average, low-achieving students are harmed by high-achieving peers. Analyzing students' course evaluations suggests that peer effects are driven by improved group interaction rather than adjustments in teachers' behavior or students' effort." (abstract, p. 387)

> "A one standard deviation increase in the average peer GPA causes an increase of 1.26% of a standard deviation in student grades. This result, however, masks important heterogeneity: low-achieving students are actually harmed by high-achieving peers." (p. 389)

> "In terms of the Dutch grading scale, this estimate means that, for example, an increase of peer GPA from 6.5 to 7.0 is associated with a grade increase from 6.50 to 6.523, a small and economically insignificant effect." (p. 406); corrected for reliability (split-half 0.72) "This increases the estimate to 1.75% of a standard deviation." (p. 406)

**Heterogeneity (who gains, who loses).**

> "The results for high- and middle-GPA students are in line with the linear-in-mean model: high- and middle-GPA students are positively affected by high-GPA peers and negatively affected by low-GPA peers. The results for low-GPA students, however, are noticeably different. The point estimate suggests that low-GPA students are negatively affected by high-GPA peers. They are also negatively affected by peers from their own GPA group—low-GPA peers." (p. 408)

- Table 6 (p. 409): Low GPA × fraction high-GPA peers = −.1449 (p < .10); Low GPA × fraction low-GPA peers = −.1315 (p < .05); High GPA × fraction low-GPA peers = −.1047 (p < .05). Low vs middle difference in response to high peers: F = 5.40, p = .0207.
- "Overall, the estimated effects are small in magnitude" — e.g., replacing 3 of 15 middle peers with low peers lowers a low-GPA student's grade "by 2.63% of a standard deviation" (p. 408).
- Conclusion: "These average effects hide important heterogeneity however. While high- and middle-ability students benefit from better peers, low-ability students are harmed by their high-ability peers." (pp. 414–415)

**Model / mechanism.**

- Analytical/Monte Carlo model of **measurement error** in peer regressions (building on Angrist 2014): "We show, both analytically and using Monte Carlo simulations, that in settings where peers are randomly assigned, classical measurement error will only lead to attenuation bias. With systematic student assignment, however, measurement error can lead to substantial overestimation of peer effects. This bias is distinct from selection bias." (p. 388). This is a model of the *estimator*, not of behavior.
- Behavioral channel evidence is survey-based and caveated: "All results, however, should be interpreted with caution, and we interpret them as providing suggestive evidence." (p. 412). Group interaction effect is linear, so "the inverse U-shaped pattern for low-GPA students we found in Section VII is driven by other unobserved factors." (p. 414) [sic: authors' section reference]
- Welfare caveat: "Without knowing the process that generates the observed peer effects, however, it is not clear whether this would be welfare enhancing." (p. 415)
→ [no model of mechanism]

**Sorting vs effect.** Random section assignment by schedulers blind to grades; leave-me-out randomization test; uses pre-treatment peer GPA to avoid reflection.

**Limitations.**

- [single system] one business school.
- [imperfect measure] ability = past GPA (reliability 0.72, p. 406); evaluation response "is selective. We observe, for example, that students with higher GPAs are more likely to take part in the evaluation" (p. 412).
- [no model of mechanism] see above; heterogeneous pattern for low-GPA students unexplained (p. 414).
- [outcome is not selection] outcome = course grades.
- Effect sizes small (p. 406).

**Channel / source (assistant judgment).** Development via peers (classroom sections), organization assigns. Clear evidence that the **same high-achieving peers help high/middle students and hurt low students**. Measurement-error result bears on *evaluation* of peer effects themselves (estimator bias), relevant to how much reduced-form estimates can be trusted.

---

## 7. Duflo, Dupas & Kremer (2008 WP / 2011 AER) — tracking experiment, Kenya

**Citation (version read).** Duflo, Esther, Pascaline Dupas, and Michael Kremer. 2008 (revised October 2009). "Peer Effects, Teacher Incentives, and the Impact of Tracking: Evidence from a Randomized Evaluation in Kenya." NBER Working Paper 14475. DOI 10.3386/w14475. **Pages below are the working paper's printed page numbers** (printed p = PDF p − 1; abstract is on unnumbered PDF p. 2). Published version: *American Economic Review* 101(5): 1739–1774 (2011) — not read here; published page numbers will differ and the published text may differ from the WP.

**Data / setting.** Western Kenya, Extra Teacher Program (ETP), 2005. "In 2005, 140 primary schools in western Kenya received funds to hire an extra grade one teacher. Of these schools, 121 had a single first-grade class and split their first-grade class into two sections" (p. 2). "The sample frame consists of approximately 10,000 students enrolled in first grade in March 2005." (p. 16); 60 students per school tested; test attrition 18% (p. 16). Outcome: standardized math and language test 18 months after program start, plus follow-up one year after program ended.

**Design.** School-level randomization: "In 60 randomly selected schools, students were assigned to sections based on prior achievement. In the remaining 61 schools, students were randomly assigned to one of the two sections." (p. 2). Within non-tracking schools, random section assignment gives random peer variation; within tracking schools, regression discontinuity at the median.

**Main findings (verbatim).**

> "We find that tracking students by prior achievement raised scores for all students, even those assigned to lower achieving peers. On average, after 18 months, test scores were 0.14 standard deviations higher in tracking schools than in non-tracking schools (0.18 standard deviations higher after controlling for baseline scores and other control variables)." (p. 2)

> "In non-tracking schools, students randomly assigned to academically stronger peers scored higher, consistent with a positive direct effect of academically strong peers." (abstract, WP PDF p. 2)

> "If effects were linear, column 1 would imply that one standard deviation increase in average peer endline test score would increase the test score of a student by 0.52 standard deviations, an effect comparable to that usually found in previous literature, with the exception of Lyle (2007), which finds insignificant peer effects with a similar strategy." (p. 24)

- Persistence: "One year after the program ended, students in tracking schools performed 0.16 standard deviations higher than those in non-tracking schools." (p. 31)

**Heterogeneity / nonlinearity.**

> "the estimated effect is 0.9 standard deviations in the top quartile; insignificant and negative in the middle two quartiles, and 0.5 standard deviations in the bottom quartile." (p. 25)

> "This effect was very strong for students at the top of the distribution, absent for students in the middle of the distribution and positive but not as strong at the bottom of the distribution. Together, these results suggest that peers affect students both directly and indirectly by influencing teacher behavior, in particular teacher effort and choice of target teaching level." (p. 31)

- RD: students near the median "scored similarly on the endline exam whether they were assigned to the top or bottom section" (p. 31).
- Naive prediction (Proposition 1, pure direct peer effects): tracking "will reduce test scores for those below the median of the original distribution and increase test scores for those above the median" (p. 8) — rejected by the data.

**Model / mechanism — proposed AND tested.**

> "We propose a simple model nesting these effects." (abstract) ... "In the model, students can potentially generate direct student-to-student spillovers as well as indirectly affect both the overall level of teacher effort and teachers' choice of the level at which to target instruction. Teacher choices depend on the distribution of students' test scores in the class as well as on whether the teacher's reward is a linear, concave, or convex function of test scores." (p. 2)

- Testing is by rejecting special cases (propositions), not by structural estimation: "This first set of findings allows us to reject a special case of the model, in which all students benefit from higher-achieving peers but teacher behavior does not respond to class composition." (p. 2); results "are consistent with the assumption that teachers' rewards are a convex function of test scores" (p. 3).
- Organizational incentive is explicit: teacher incentives "are based on the scores of their students on the national primary school exit exam given at the end of eighth grade. But since many students drop out before then, the teachers have incentives to focus on the students who are likely to take the exam, students at the very top of the first-grade class." (p. 3)
→ Model proposed and qualitatively tested; **parameters not estimated** [model not fit to data].

**Sorting vs effect.** Randomization of tracking at the school level and of students to sections in non-tracking schools; initial assignment used throughout (p. 24 fn. 14); RD within tracking schools.

**Limitations.**

- [single system] / generalization: "It is impossible to know if the results of this study will generalize until further studies are conducted in different contexts" (p. 5); "caution is needed in generalizing from these results in which teacher ability was held constant between tracking and non-tracking schools." (pp. 32–33)
- [imperfect measure] baseline = school grade sheets "which are not comparable across schools" (p. 24); linear extrapolation caveat: "the extrapolation to one standard deviation may not actually be legitimate" (p. 24 fn. 15).
- [small data] for the peer-variation analysis: "we use actual random variation in peer group composition, but have lower sample size" (p. 24).
- [model not fit to data] see above.
- [outcome is not selection] outcome = test scores; but the mechanism runs through a downstream *selection* (who sits the grade-8 exit exam), which shapes teacher effort.

**Channel / source (assistant judgment).** Development via peers **and** organization (teacher incentives/targeting). Unusual in giving a mechanism: peer composition changes teacher behavior. Peer exposure under random variation helps top and bottom quartiles but not the middle — peers' effect depends on the organization's evaluation/reward scheme (convex payoffs tied to a later selection exam).

---

## 8. Jackson & Bruegmann (2009) — peer learning among teachers, North Carolina

**Citation (version read).** Jackson, C. Kirabo, and Elias Bruegmann. 2009. "Teaching Students and Teaching Each Other: The Importance of Peer Learning for Teachers." NBER Working Paper 15202 (July 2009). DOI 10.3386/w15202. **Pages = WP printed page numbers** (printed p = PDF p − 2). Published version: *American Economic Journal: Applied Economics* 1(4): 85–108 (2009) — not read here.

**Data / setting.** "We use data on all third-grade through fifth-grade students in North Carolina between 1995 to 2006 from the North Carolina Education Research Data Center." (p. 8). Teacher value-added estimated on pre-sample 1995–2000; effects estimated on 2001–2006 (p. 11). Main regressions ≈ 1.2 million student observations (Table 1, "Observations 1200633", PDF p. 30). Outcome: students' math and reading test-score gains. The "peers" here are **teachers' colleagues** (same school, same grade, same year) (p. 6).

**Design.** Observational, not randomized. Value-added model with teacher peer quality as covariate; teacher-by-school fixed effects (variation only from colleague turnover / reassignment) and school-by-year fixed effects (p. 7). Peer quality measured by (1) observable characteristics and (2) out-of-sample pre-period value-added (p. 2).

**Main findings (verbatim).**

> "we further show that a teacher's students have larger achievement gains in math and reading when she has more effective colleagues (based on estimated value-added from an out-of-sample pre-period). Spillovers are strongest for less-experienced teachers and persist over time, and historical peer quality explains away about twenty percent of the own-teacher effect, results that suggest peer learning." (abstract, p. 1)

> "The coefficient on peer value-added for math in column 3 is 0.0398, suggesting that a one-standard-deviation increase in the mean estimated value-added of a teacher's peers is associated with a 3.98 percent of a standard deviation increase in math test scores. ... For the average teacher with three peers, replacing one peer with another that has one standard deviation higher value-added will increase her students' math test scores by 1.3 percent of a standard deviation." (p. 15)

> "The cumulative effect over three years of having peers with one standard deviation higher effectiveness is 0.078 standard deviations in math and 0.072 standard deviations in reading. Because teachers have about three peers on average, this is about one third of the size of the own-teacher effect" (p. 22)

**Heterogeneity.** "less experienced teachers are generally more responsive to changes in peer quality than more experienced teachers" (p. 22). No evidence reported here of anyone being hurt.

**Model / mechanism.** A verbal theoretical framework distinguishing (1) joint production/shared resources, (2) motivation and effort, (3) peer learning, with testable predictions (persistence; stronger for novices; historical peers explain own effect) (pp. 4–5). Tested by reduced-form patterns, not by fitting a formal model. Authors' limit: "Because all learning explanations could yield the same empirical predictions, we are unable to distinguish a peer learning story from the peer-induced learning story." (p. 6); "Although we acknowledge that we cannot prove peer related learning, we believe these pieces of evidence lend themselves most naturally to a peer related learning interpretation" (pp. 22–23). → [model not fit to data] (verbal model, predictions checked).

**Sorting vs effect.** Fixed effects + falsification tests; explicitly non-random: "Although we are careful to control for a variety of possible confounding influences, we do not have random assignment of students to teachers or of teachers to peers. Because the possibility of spurious correlation remains, we present several specification and falsification tests." (p. 3)

**Evaluation and organization (key for the dissertation).**

> "This paper contributes to the nascent literature questioning the validity of standard value-added models by evaluating the assumption of no spillovers across teachers—a key identification assumption in teacher value-added models. Also, the findings here should give pause to advocates of individual-level merit-based pay because such pay schemes could reduce teachers' incentives to help their colleagues and could undermine peer learning." (pp. 3–4)

> "For example, compensation schemes that reward a teacher's performance relative to her peers may be detrimental to fostering peer learning." (p. 23)

> "we do show that the assumption of no spillovers across teachers is not valid." (p. 23)

**Limitations.**

- [single system] one state; "Although teachers in elementary school may be a somewhat unique group" (p. 23).
- [imperfect measure] peer quality = estimated value-added (noisy); peers defined narrowly so estimates are "a lower bound" (p. 3, p. 6).
- [model not fit to data] verbal framework only.
- No random assignment (p. 3).
- [outcome is not selection] outcome = students' test-score gains, not teacher promotion/tenure.

**Channel / source (assistant judgment).** Bridges education and workplace: **development** of workers (teachers) via peers (colleagues). Also bears on **evaluation**: individual value-added measures attribute to a teacher output that partly reflects colleagues, so individual-performance evaluation is contaminated by environment. Relative pay schemes (organization) could suppress the peer channel.

---

## 9. Lyle (2007) — randomly assigned companies at West Point

**Citation.** Lyle, David S. 2007. "Estimating and Interpreting Peer and Role Model Effects from Randomly Assigned Social Groups at West Point." *Review of Economics and Statistics* 89(2): 289–299. DOI 10.1162/rest.89.2.289. (Printed p = PDF p + 288. Two-column layout; extracted without `-layout`.)

**Data / setting.** US Military Academy (USMA, West Point), graduating classes 1992–1998, Office of Economic and Manpower Analysis data (admissions, Survey of Incoming Freshmen, cadet and officer personnel records) (p. 291). "data are available for plebes in 252 companies—that is 36 companies over seven years." (p. 291); ~35 plebes per company (p. 290); Table 2 individual regressions N ≈ 8,508–8,555 (p. 293). Army-retention outcome available for 180 companies only (p. 292 fn. 2). Outcomes: two performance (plebe-year academic GPA, math grade) and two choice outcomes (academic major; remaining in the Army past the 5-year obligation) (p. 289).

**Design.** Conditional random assignment ("scrambling"): random number, then shuffling "in an attempt to equalize the means of the eight characteristics with the aim of producing comparable companies" (p. 292). "Not only does 'Uncle Sam' issue a uniform and a 'tight haircut,' but he also issues peers and role models." (p. 292). Peers = other plebes in company; role models = sophomores in company (p. 290).

**Main findings (verbatim).**

> "Estimates of contemporaneous group effects in human capital production are typically positive and significant; however, evidence in this study suggests that occurrences common to a group may account for much of this correlation. Models that address these biases provide little evidence of group effects in academic performance, although there is evidence of group influences in choice outcomes such as the selection of academic major and the decision to remain in the Army." (abstract, p. 289)

> "Comparing column 6 with column 7 reveals that common shocks attributed to the characteristics of the company's upperclassmen reduce the contemporaneous peer effect by almost half ... Consequently, common shocks may account for most or even all of the measured correlation between own and peer GPA." (p. 295)

> "the economic magnitude of the effect is negligible; a one-standard-deviation increase in the average math SAT scores of the peer group affects an individual's math grade by 0.003 points." (p. 296)

- Choice outcomes: "A 10-percentage-point increase in the fraction of role models who intend to study engineering leads to a 1.5-percentage-point increase in the probability that a plebe will choose engineering as a major." (p. 297)
- "A 10-percentage-point increase in the fraction of peers who anticipated a military career increases the chance of remaining in the military at least six years after graduation by 2.5 percentage points." (p. 298); role models' leadership score: "A 100-point increase in the average LPS of role models results in a 15-percentage-point-higher chance of remaining on active duty six years past graduation" (marginally significant) (p. 298).

**Heterogeneity.** Not a focus; no who-gains/who-loses analysis by ability reported in the sections read.

**Model / mechanism.** Linear-in-means framework (Manski endogenous/exogenous/common shocks); reduced form preferred: "the reduced-form specification in equation (3) provides the most credible method of estimating social group effects." (p. 296). Mechanisms for role-model effects are conjectures (major chosen by end of sophomore year; leadership experience) (pp. 297–298). → [no model of mechanism]

**Sorting vs effect.** Random assignment conditional on 8 scrambling controls; balance tests in Table 2 (p. 292). Separates **common shocks** from peer effects (upperclassmen/company-commander attributes as proxies, p. 295) — the paper's main methodological contribution.

**Limitations.**

- [imperfect measure] Equalizing scrambling limits variation: "It is possible that the scrambling process reduces the variation in average pretreatment ability measures to the extent that no effect is identifiable." (p. 296); scrambling also creates "a mechanically driven negative correlation between the peer SAT score and the individual's GPA" (p. 296 fn. 10). CFW 2009 notes USAFA peer-SAT variance is 49% greater than in Lyle's data (CFW p. 443 fn. 10).
- [single system] one military academy.
- [small data] retention outcome for 180 of 252 companies due to Global War on Terror stop-loss (p. 292 fn. 2).
- [no model of mechanism]
- [outcome is not selection] Choice outcomes (major, staying in Army) are individual choices, not competitive scarce slots; authors' own call: "research on social relationships other than peers and on measures of outcomes other than academic performance may provide valuable insights" (p. 298).

**Channel / source (assistant judgment).** Development of preferences/choices via peers (plebes) and **role models** (sophomores, an organizationally designated hierarchy). Academic peer effects ≈ zero; effects show up in career choices (retention), which feed later military selection pipelines but are not themselves selection decisions.

---

## 1. Hoxby (2000) — cohort-to-cohort gender and race variation, Texas elementary schools

**Citation.** Hoxby, Caroline. 2000. "Peer Effects in the Classroom: Learning from Gender and Race Variation." NBER Working Paper 7867 (August 2000). DOI 10.3386/w7867. **Pages = WP printed page numbers** (printed p = PDF p − 2; abstract on unnumbered PDF p. 2). **Text source = tesseract OCR** (the PDF's text layer is unreadable); quotes are OCR output, with "|" read as "1" where marked.

**Data / setting.** Texas Schools Microdata Panel (UT-Dallas Texas Schools Project); TAAS state tests, grades 3–6, 1990–91 to 1998–99; "about 3,300 schools in Texas that enrolled third graders and the size of the median cohort was about 80 students" (p. 20). Observations are group averages: "Number of observations is 22,496 in third grade regressions, 19,084 in fourth grade regressions, 14,974 in fifth grade regressions, and 9,743 in sixth grade regressions. An observation is a gender group in a cohort in a school." (Table 5 notes, PDF p. 45). Outcome: reading and math test scores (TAAS reading mean ≈ 29.5 points, SD ≈ 2.3, p. 20).

**Design (quasi-random, not randomized).** Within-school, within-grade variation between adjacent cohorts: "Both strategies depend on the idea that there is some variation in adjacent cohorts' peer composition within a grade within a school that is idiosyncratic and beyond the easy management of parents and schools." (p. 3). Strategy 1: changes in gender/racial shares; Strategy 2: correlated idiosyncratic achievement residuals across groups (p. 4). Specification test: drop schools where "actual years explain more variation (in cohort composition or in achievement) than false, randomly assigned years." (p. 4)

**Main findings (verbatim).**

> "I find that students are affected by the achievement level of their peers: a credibly exogenous change of 1 point in peers' reading scores raises a student's own score between 0.15 and 0.4 points, depending on the specification. Although I find little evidence that peer effects are generally non-linear, I do find that peer effects are stronger intra-race and that some effects do not operate through peers' achievement." (abstract, PDF p. 2) [OCR: "acredibly" → "a credibly"; "|" → "1"]

> "If one translates the peer effect estimates from strategy 1 into test scores, then strategy 1 generates estimates in the range of 0.15 to 0.40. Strategy 2 tends to generate estimates in the range of 0.10 to 0.55." (p. 36)

> "Males' scores rise by 0.0471 points for 10 percentage change in the share of their class that is female. To put this in perspective, an all-female class would score about one-fifth of a standard deviation higher in reading, all else equal." (p. 23)

**Heterogeneity (who gains, who loses).**

> "The translation suggests that the effect of mean peer achievement varies from small (0.092) to substantial (0.676), and that the most substantial effects of mean peer achievement are intra-racial group." (p. 26) — e.g., a 1-point-lower peer mean "lowers a black student's own score by 0.676 points in reading and 0.402 points in math" vs Anglo "0.168 points in reading and 0.092 points in math" (p. 26).

> "In any case, it is clear that the baseline model of peer effects is inadequate: peer effects do not operate solely through peers' mean achievement in the same subject." (pp. 24–25)

- Female share in math: translated effects "so large that they suggest that peer effects do not operate purely through peers' mean achievement in math." (p. 24)
- Nonlinearity mostly not found: Table 14 quadratic terms "all small (in the range of 0.001 to 0.008) and statistically insignificantly different from zero. These results do not provide any evidence of non-linearities" (p. 34); but female-share effects "tends to be largest in classes that are initially at least 66 percent female" (p. 25).

**Model / mechanism.** Framework = test of the linear "baseline model" (own outcome linear in peers' mean): "Regardless of how one allocates peers, total societal achievement remains the same under the baseline model. In order to give one student a better peer, one must take that peer away from another student; the two effects exactly cancel." (p. 2). Channels listed but not separated: "I make some effort to distinguish among the channels by which peer effects operate, but my primary purpose is to establish the existence and direction of peer effects." (p. 35). Proposed channels for the female effect are speculative ("more female classes may simply have fewer disruptive students or a more learning-oriented culture", p. 24). → [no model of mechanism]

**Sorting vs effect.** Concedes selection into schools and classrooms ("I take for granted that parents choose a school based on its population of peers and that parents and schools manipulate the assignment of students to classes within their grades", p. 3); relies on unpredictable cohort composition + time-trend falsification ("drop if more than random"; "Almost two-thirds of the observations are dropped in this very stringent test for time trends", p. 28). Common shocks probed via between-grade regressions and low-teacher-turnover schools (pp. 31–32).

**Limitations.**

- [imperfect measure] Strategy 2 residual-based: between-grade estimates "are almost certainly underestimates because of attenuation bias and because migration of students limits between-grade correlation" (p. 31); Asian residual coefficients "vary widely, which suggests that measurement error (both classical and due to common shocks) generates a large share of the total variation" (p. 32 fn.). Peer "group" = cohort within grade within school, not the actual classroom.
- [single system] one state's public schools and one test (TAAS).
- [small data] for small groups: Native American/Asian results "based on relatively few observations" (p. 26 fn. 18); idiosyncratic variation "is sufficiently uncommon that a large number of observations are needed" (p. 4).
- [no model of mechanism]
- [outcome is not selection] outcomes = elementary test scores.
- Not randomized; identification rests on cohort-composition variation being idiosyncratic.

**Channel / source (assistant judgment).** Development via peers (school cohort). Heterogeneity is by race/gender composition rather than by ability rank; establishes that composition (not just mean) matters, which is the precondition for any reallocation gains.

---

## 10. Angrist (2014) — "The perils of peer effects" (methodological claims only)

**Citation.** Angrist, Joshua D. 2014. "The Perils of Peer Effects." *Labour Economics* 30: 98–108 (pages per Crossref). DOI 10.1016/j.labeco.2014.05.008. **PDF read is the "article in press" version** (pages printed 1–11, volume/pages "xxx"). Page cites below are in-press pages; journal page = in-press page + 97 (**inferred** from 11 pages ↔ 98–108; not checked against the final typeset version).

**Claim 1 — outcome-on-outcome peer regressions are mechanical.**

> "Individual outcomes are highly correlated with group average outcomes, a fact often interpreted as a causal peer effect. Without covariates, however, outcome-on-outcome peer effects are vacuous, either unity or, if the average is defined as a leave-out mean, determined by a generic intraclass correlation coefficient." (abstract, in-press p. 1 / journal p. 98)

> "If the group average in question involves the dependent variable, the estimated peer effect is a mechanical phenomenon, either affirming an identify in the algebra of expectations or providing a measure of group clustering devoid of behavioral content." (in-press p. 1 / p. 98) [sic "identify"]

**Claim 2 — with pre-determined peer covariates, "peer effects" = 2SLS ≠ OLS, which has many non-social causes (weak IV under random small groups; measurement error under systematic grouping).**

> "When pre-determined peer characteristics are introduced as covariates in a model linking individual outcomes with group averages, the question of whether peer effects or social spillovers exist is econometrically identical to that of whether a 2SLS estimator using group dummies to instrument individual characteristics differs from OLS estimates of the effect of these characteristics. The interpretation of results from models that rely solely on chance variation in peer groups is therefore complicated by bias from weak instruments. With systematic variation in group composition, the weak IV issue falls away, but the resulting 2SLS estimates can be expected to exceed the corresponding OLS estimates as a result of measurement error and for other reasons unrelated to social effects." (abstract, in-press p. 1 / p. 98)

> "There are many reasons why 2SLS estimates might differ from the corresponding OLS estimates. While peer effects are on the list of causes behind such divergence, they should not usually be at the top of it." (in-press p. 2 / p. 99)

**Claim 3 — credible designs separate subjects from peers and manipulate peer exposure orthogonally to own traits; these find little.**

> "Research designs that manipulate peer characteristics in a manner unrelated to individual characteristics provide the most compelling evidence on the nature of social spillovers. As an empirical matter, designs of this sort have mostly uncovered little in the way of socially significant causal effects." (abstract, in-press p. 1 / p. 98)

**On Carrell–Sacerdote–West 2013 (directly relevant to the "policy from reduced form" point).**

> "I read these findings as illustrating the proposition that estimates of equations like (20) are unlikely to have predictive value for interventions that change peer groups. The disappointing Carrell et al. (2013) results seem to me more likely to originate in the spurious nature of econometric estimates of peer effects than in endogenous social stratification." (in-press p. 8 / p. 105)

- He notes the motivating CSW estimate is "a large significant estimate for a single group ... estimated in a model with 6 peer interactions," while other specifications give smaller or mixed effects (in-press pp. 8–9 / pp. 105–106).

**On network models.** "In my view, this new literature follows the old in confusing technical questions of identification with the more fundamental question of whether any of the effects that might be identified should be seen as causal." (in-press p. 9 / p. 106)

**Limitation tags (as they bear on the literature he critiques).** [imperfect measure] (measurement error inflates 2SLS); [small data] (many small random groups = weak instruments); [no model of mechanism] (identified parameters "reveal little about human behavior", in-press p. 1).

**Channel / source (assistant judgment).** Bears on **evaluation of the evidence** itself: much reduced-form peer evidence is not behavioral and should not be used to forecast reallocations. Offers a rival reading of CSW 2013 (spurious pre-treatment estimate) vs CSW's own (endogenous subgroup formation) — both readings imply reduced-form peer coefficients are a poor basis for designing groups.

---

## 11. Sacerdote (2011) and Sacerdote (2014) — reviews (ABSTRACT-ONLY; no PDFs)

### 11a. Sacerdote (2011) — Handbook chapter — ABSTRACT ONLY

**Citation.** Sacerdote, Bruce. 2011. "Peer Effects in Education: How Might They Work, How Big Are They and How Much Do We Know Thus Far?" In *Handbook of the Economics of Education*, vol. 3, ed. E. A. Hanushek, S. Machin, and L. Woessmann, 249–277. Elsevier. DOI 10.1016/B978-0-444-53429-3.00004-1. (Editors not in the bib entry; listed from general knowledge — verify.)

**Source of abstract.** Crossref returned no abstract; Semantic Scholar returned `abstract: null` ("elided by the publisher"). Abstract below was taken from the saved ScienceDirect page in the Zotero folder (`files/848/...ScienceDirect.mhtml`), HTML tags stripped. No page number (abstract).

> "This chapter summarizes the recent literature on peer effects in student outcomes at the elementary, secondary, and post-secondary levels. Linear-in-means models find modest sized and statistically significant peer effects in test scores. But the linear-in-means model masks considerable heterogeneity in the effects experienced by different types of students. Using nonlinear models, one prevalent finding is larger peer effects in which high ability students benefit from the presence of other high ability students. Studies that stratify students by race and ability often find that students are affected both by the racial composition of their peers and by the achievement of their same-race peers. At the university level, several studies find modest sized effects from dormmate and roommate background on own academic performance. For both university and high school students, the measured peer effects on 'social' outcomes such as drinking are larger than the effects on academic outcomes. Many authors find substantial peer effects in drinking, drug use, and criminal behavior. This chapter suggest areas for future investigation and data collection." [sic "suggest"]

**Use (assistant judgment).** Review-level support for: modest linear-in-means effects; heterogeneity masked by the mean; social outcomes > academic outcomes. Do not cite specific numbers from this chapter — body not read.

### 11b. Sacerdote (2014) — Annual Review of Economics — ABSTRACT ONLY

**Citation.** Sacerdote, Bruce. 2014. "Experimental and Quasi-Experimental Analysis of Peer Effects: Two Steps Forward?" *Annual Review of Economics* 6: 253–272. DOI 10.1146/annurev-economics-071813-104217. (Volume/pages from Crossref.)

**Source of abstract.** Crossref API (JATS tags stripped).

> "In the past 10 years, there has been an explosion of well-identified studies that measure peer effects across many settings and for many outcomes. The emphasis on natural experiments and randomization is a highly useful one; in more standard observational studies, the self-selection of people into peer groups can make the measurement of peer effects extremely difficult. In the absence of exogenous variation, knowing that people have similar outcomes as their friends, classmates, and coworkers may tell us little about peer effects. I examine the successes, failures, and findings of experimental analyses of peer effects. I draw three broad conclusions. First, even more than in other areas of social science, the size and nature of peer effects estimated are highly context specific; peer effects in student test scores and grades are prominent in some cases and absent in others. That said, there is a pattern across studies suggesting that social outcomes (e.g., crime, drinking behavior) and career choices show larger peer influences than do test scores. Second, researchers have shown that the linear-in-means model of peer effects is often not a good description of the world, although we do not yet have an agreed-upon model to replace it. Third, despite potential temptation, we have not reached the point at which we can reliably use knowledge of peer effects to implement policies that improve outcomes for students and other human subjects."

**Use (assistant judgment).** The three conclusions map directly onto the gap tags: context specificity → [single system]; "we do not yet have an agreed-upon model to replace it" → [no model of mechanism] / [model not fit to data]; policy not reliable → CSW 2013. Note "career choices show larger peer influences than do test scores" — consistent with Lyle 2007 (Army retention) and Sacerdote 2001 (fraternities).

---
