# Education B — classroom / roommate / cohort peer effects: source note

**Purpose:** verbatim, page-cited extracts for the EDUCATION background subsection of the dissertation introduction. Not dissertation prose.

**Conventions**

- "p. N" = printed journal (or working-paper) page number. "PDF p. M" given when it differs.
- Quotes are copied from the PDF text layer (`pdftotext -layout`). Hyphenation at line breaks is rejoined; nothing else is changed unless marked `[OCR fix: ...]` (only for the scanned Sacerdote 2001 and Lyle 2007 JSTOR copies, whose text layers contain OCR character errors).
- Limitation tags: [small data], [imperfect measure], [single system], [no model of mechanism], [model not fit to data], [outcome is not selection].
- "Channel / source" lines are **assistant judgment**, not the authors' claims. Channels: development (what a person becomes), evaluation (how a performance is measured/perceived), selection (who wins a scarce slot). Sources: peers vs organization.

**Contents (in order written)** — Sacerdote 2001; Hoxby 2000; Carrell, Fullerton & West 2009; Carrell, Sacerdote & West 2013; Booij, Leuven & Oosterbeek 2017; Feld & Zölitz 2017; Duflo, Dupas & Kremer 2008/2011; Jackson & Bruegmann 2009; Lyle 2007; Angrist 2014; Sacerdote 2011 & 2014 (abstract-only).

---

## Assistant synthesis (8–12 lines; ASSISTANT SYNTHESIS, not source text)

_(to be written after all papers are read)_

---

## 1. Sacerdote (2001) — Dartmouth roommates

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
