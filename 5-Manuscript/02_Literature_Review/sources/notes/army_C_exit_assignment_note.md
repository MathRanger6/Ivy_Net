# Army C — officer exit, mentoring, and assignment (source note)

Prepared 2026-11-02. Sources live under `sources/Talent_Net/files/`. Text came from `pdftotext -layout`. Printed page numbers were checked one page at a time with `pdftotext -f N -l N`. One exception: 368 has no text layer, so it was OCR'd with tesseract (see that section). HTML pages were stripped with Python `html.parser`, so they have no page numbers.

**Framing used:** the environment is peers plus the organization. It reaches officers through three channels: development, evaluation, and selection. A score is not the same thing as selection. Causal peer effects are not presumed. The note looks for three things:

- **(a)** Is exit from the officer corps selective by ability or performance? This matters because the cohort only shrinks, so departures change who is left to compete.
- **(b)** Do the leaders or mentors an officer is assigned to change that officer's career?
- **(c)** How much do officers choose their own assignments, and how much are they simply assigned?

**Quick map of what each source supplies:**

| Goal | Best source here | Strength |
|---|---|---|
| (a) selective exit | Spain, Lin & Farina 2023 | Administrative data, N = 13,309; observational |
| (b) assigned mentor changes career | Lyle & Smith 2014 (stands in for the missing Carter–Dudley–Lyle paper) | Assignment is argued to be as good as random; the outcome is **promotion**, not retention |
| (b) background | Johnson & Andersen 2010 | Review; no formal military evaluation exists |
| (c) who chooses assignments | Lyle & Smith 2014 (before 2019); STAND-TO! ATAP page (2019 onward) | Description of policy; ATAP page is official Army public relations |
| context: "best are leaving" claim | Kane 2011 (Atlantic) | Opinion essay; snapshot is paywall-truncated |

---

## 1. Spain, Lin & Farina (2023)

**Citation as printed:** Spain, Everett S. P., Eric Lin, and Andrew G. Farina. "Do the Best and Brightest West Point Officers Stay in or Leave the Army?" *Armed Forces & Society* 00(0), 1–31. © The Author(s) 2023. DOI: 10.1177/0095327X231194238. (Printed page numbers match the PDF page index.)

- **Design/data:** Archival, de-identified Office of Economic and Manpower Analysis (OEMA) data on West Point graduates from the classes of 1992–2007, N = 13,309. The data include cadet performance, yearly retention indicators, demographics, branch, deployments, and family size. Retention is observed through 2012.
  - **Outcomes:** whether the officer is still on active duty past year 6 (the company-command decision) and past year 10 (the field-grade decision, modeled only for those who stayed past year 6).
  - **How "best and brightest" is measured:** "Best" means the top third of the class on cumulative Military Development GPA (MGPA), mostly ratings in cadet leadership roles. "Brightest" means the top third on Academic GPA (AGPA). The "best and brightest" are in the top third on both, which works out to roughly the top 10%. The comparison group is officers in the middle third on both.
  - **Methods:** logit models with controls for physical GPA, prep school, recruited athlete, female, minority, deployment, family size, branch, graduation year, and home region. Kaplan–Meier survival curves with log-rank tests.
  - **Sample sizes:** Table 4 has 13,309 observations for year 6 and 5,660 for year 10 (conditional on staying past year 6). Table 2 has 9,851 for year 10.
- **Design/data — the measure is a pre-entry score.** "this study will consider those cadets who are in the top 33% of both MGPA and AGPA to be the best and brightest, which jointly approximates the top 10% overall" (printed p. 6).
- **Claim (a): the authors expected the best to leave more (from the turnover literature).** "we hypothesize that the best and brightest West Pointers will also be more likely to leave the Army than their average- and lower-performing peers" (printed p. 6).
- **Claim (a): no difference at year 6; the best stay more at year 10.** "When compared with their average-performing classmates, the best and brightest West Pointers show no statistical difference in Retaining past year 6 (β = 1.02, p = .69). Regarding Retaining past year 10 (if stay past year 6), the best and brightest West Pointers are predicted to have 38% increased odds (β = 1.38, p = .002) of retaining." (printed p. 15)
- **Claim (a): the narrower "elite" group (top ninth on both measures) stays more at both points.** "the elite-best and brightest West Pointers have 33% higher odds of Retaining past year 6 (β = 1.33, p = .023) and 79% higher odds (β = 1.79, p = .002) of retaining past year 10, if retained past year 6" (printed p. 15).
- **Claim (a): lower military performers leave more.** This is the direct evidence that exit is selective. "Being classified as not best, irrespective of grouping on the brightest dimension, is associated with lower retention on average." (printed p. 15). The raw retention rates past year 6 (Table 3, p. 16) are 0.60 for best-and-brightest, 0.69 for best-not-brightest, 0.59 for average, 0.49 for not-best-but-brightest, and 0.48 for not-best-not-brightest.
- **Claim (a): survival analysis.** "the EHA indicates the overall retention pattern of the best and brightest officers is different (higher) than their average-performing peers. Therefore, this is evidence that best and brightest remain on active duty longer than the average-performer, which is contrary to H1." (printed p. 19). Event hazard analysis (EHA) is the survival method above. The log-rank comparison of best-and-brightest against average is χ²(1) = 7.76, p ≤ .005, N = 2,545 (printed p. 18).
- **Claim (a): their exact conclusion.** "Though many have used their personal observations and self-report studies to claim the best and brightest officers are choosing to leave the Army, empirical evidence from this study does not support such claims. In fact, the evidence indicates that Army's best and brightest officers are as likely to stay in the Army long enough to serve as company commanders (serve past year 6) as their average-performing classmates are; additionally, they are much more likely to stay than their lowest performing classmates." (printed p. 22)
- **Claim (a): exit is built into the hierarchy.** This supports the point that the cohort only shrinks. "in hierarchical organizations like the U.S. Army, a certain rate of turnover is required- typically equal to the decreasing number of authorizations (positions) available at each subsequent level of responsibility/seniority" (printed p. 3).
- **Claim (a): exits are voluntary.** "Since almost all officer losses are voluntary, our research question is: Are the best and brightest Army officers choosing to leave the Army at a higher rate than their peers?" (printed p. 2)
- **Claim (a): heterogeneity among the best and brightest.** Best-and-brightest minority women have 70% lower odds, and minority men 40% lower odds, of staying past year 10 compared with Caucasian men. "the best and brightest officers who are minority women are predicted to have 70% lower odds of retaining in the Army past year 10 (if they retained past year 6) than the best and brightest Caucasian male officers who retained past year 6" (printed pp. 21–22). The authors call the gender evidence "mixed" (printed p. 20).
- **Claim (context for Kane): the authors' critique of the Atlantic survey.** "The Atlantic's article did not specifically define what constituted the "best" or the "brightest," and the study's sample size (N = 248) and survey response rate (4%) were low, rendering its findings less certain." (printed p. 26, note 1)
- **Causal language:** The paper is predictive and associational. It uses phrases like "predicted to have … increased odds" and "associated with lower retention." It does not claim that performance causes retention. It reports who stays, conditional on cadet scores.
- **Limits:**
  - The study covers only West Point graduates, active duty, classes 1992–2007. The data predate the Blended Retirement System.
  - "Best" and "brightest" come from cadet GPAs, not officer evaluation reports (OERs). That makes them a pre-commissioning score, not an Army selection decision.
  - Year-10 models condition on surviving to year 6.
  - The authors list possible omitted-variable bias: "officers' family's socio-economic status, quality of leadership received from senior officers, and assignment locations (Army posts) could all influence officers' retention decisions" (printed p. 25). This quote also connects to goals (b) and (c).
  - Evaluation measures may carry rater bias (p. 25).
  - The findings may not generalize to Officer Candidate School (OCS) officers (p. 25).

---

## 2. Requested: Carter, Dudley, Lyle et al., "The Effects of Mentor Quality, Exposure, and Type on Junior Officer Retention in the United States Army" — **NOT FOUND at the given path**

**What `files/368/2015Carter-1.pdf` actually is:** Carter, Dorothy R., Leslie A. DeChurch, Michael T. Braun, and Noshir S. Contractor. "Social Network Approaches to Leadership: An Integrative Conceptual Review." *Journal of Applied Psychology*, © 2015 American Psychological Association, http://dx.doi.org/10.1037/a0038922. The Talent Net `.bib` entry gives vol./pp. as no. 3, 597–622. The PDF prints pages 1–26, i.e., the advance-online pagination. The page numbers below refer to that PDF.

- **Design/data:** This is a conceptual and integrative review of 142 network-and-leadership works published 1999–2014, with 45 exemplar studies. **It is not about Army officers, mentoring, assignment, or retention.** The PDF has no text layer, so the text was recovered by tesseract OCR at 300 dpi, and quotes may contain OCR errors. It acknowledges Army Research Laboratory and Army Research Institute funding (printed p. 1).
- **Mentor matching (as-good-as-random?):** NOT FOUND (not in this document).
- **How mentor quality is measured:** NOT FOUND.
- **Effect on retention / magnitude:** NOT FOUND.
- **Claim (marginal relevance to environment → selection; correlational):** "These studies provide compelling evidence that individuals' social networks are associated with the attainment of leader roles." (printed p. 7; OCR)
- **Causal language:** The quoted line says "associated with." The review itself makes no causal claim about officers.
- **Limits:** This is the wrong document for goal (b). The Carter–Dudley–Lyle mentor-retention paper does not appear in `Talent_Net/files/` or anywhere under `sources/` by filename. A search for "carter" and "mentor" found only this file plus the Lyle & Smith 2014 PDFs, Kram & Isabella, Higgins & Kram, Ma et al. 2020, Ryckman, and Gomez. The closest available evidence for goal (b) is Lyle & Smith (2014), added below as **2-sub**.

### 2-sub. Substitute for goal (b): Lyle & Smith (2014)

Not on the requested list. Added because it is the published Army mentor paper by the same research group and sits in the same Talent_Net library (`files/241/`; a duplicate copy is at `files/285/`).

**Citation as printed:** David S. Lyle and John Z. Smith, US Military Academy. "The Effect of High-Performing Mentors on Junior Officer Promotion in the US Army." *Journal of Labor Economics*, 2014, vol. 32, no. 2, pp. 229–258. © 2014 by The University of Chicago. Stable URL https://www.jstor.org/stable/10.1086/673372. The PDF's first page is a JSTOR cover sheet, so printed page = PDF index + 227.

- **Design/data:**
  - Army administrative data from 1974–2010, from OEMA. Mentors are battalion commanders (lieutenant colonels) who commanded between 1998 and 2008. Protégés are captains in company command. The two are linked through OERs from 1998–2008.
  - **Sample:** N = 4,142 company commanders and 2,131 mentors. All protégés are male, combat-arms, commissioned through West Point or the Reserve Officers' Training Corps (ROTC). **They are selected on having stayed in the Army until 10 years of service.**
  - **Treatment:** ever being rated by a high-performing mentor. 44% of the sample (1,812 of 4,142) were.
  - **Outcome:** early ("below the zone") promotion to major. The sample mean is 9.2%.
  - **Methods:** linear probability model with year-group, branch, demographic, and unit controls. Standard errors are clustered by mentor.
- **Claim (b): how mentor quality is measured.** It is a prior Army selection decision, made before the pairing. "we define high-performing mentors as mentors who were previously promoted early to the rank of major. This early promotion decision is a signal of high performance potential within the army officer corps and is granted several years prior to the senior officer mentors in our sample interacting with their junior officer protégés" (printed p. 231, note 2).
- **Claim (b): all protégés are assigned a mentor, and only mentor quality varies.** "Our research design is also unique in that it affords the opportunity to compare high-performing mentors with lower-performing mentors in a setting where all protégés have a mentor assigned by the army." (printed p. 231)
- **Claim (b, c): matching works through a chain of third-party decisions.** "Junior officers receive their battalion commander mentor through a sequence of independent, third-party decisions. Military mentor relationships occur much like most other things related to the military—the army assigns them." (printed p. 233)
- **Claim (b): the matching is as good as random on observables.** "The lack of substantial differences across the demographic variables in table 2 supports our assertion that the assignment of company commanders to battalion commander mentors is as good as random with regard to observable characteristics." (printed p. 239). In Table 3, controls explain 1% of the variance in mentor quality, rising to 8% with structural controls added. No covariate is significant in the full specification (p. 239).
- **Claim (b): effect size.** "We find that junior officers who serve under a high-performing mentor are 29% more likely to be selected for early promotion to the rank of major." (printed p. 232). In absolute terms: "former company commanders who had a high-performing mentor are 2.8 percentage points more likely to be promoted early to the rank of major than former company commanders who did not have a high-performing mentor" (printed p. 242). With unit controls the estimate is 2.7 points (p. 242). Against the 9.2% base rate this is a "29% increase in the likelihood of early promotion to major" (printed pp. 242–243).
- **Claim (b): duration, ability, and number of mentors.** "We also find the impact of high-quality mentors on promotion increasing in the duration of the mentorship. These effects are most pronounced for protégés in the top half of the SAT distribution. We do not find an effect with exposure to an increasing number of high-quality mentors." (printed p. 250)
- **Claim (b): the mentor is also the evaluator.** Development and evaluation run through the same person. "Battalion commanders provide a majority of the input for company commander evaluation reports, but the only rater (mentor) information visible to the promotion board is the rater's name." (printed p. 235)
- **Claim (c): officers have little say over assignments (before ATAP).** "Other than listing installation preferences and special family considerations, junior officers have little influence over their next assignment." (printed pp. 233–234). And: "Within a given rank and occupational branch, the army treats officers as generic for assignment purposes; talents and experiences of officers do not factor into assignments." (printed p. 234)
- **Claim (b): effect on retention.** NOT FOUND. This paper studies promotion and conditions on retention to 10 years: "All captains in column 1 completed company command and remained on active duty until 10 years of service." (printed p. 237)
- **Causal language:** Explicitly causal, reduced form. "Together this suggests that the mentor relationships in our study provide a plausible source of variation to identify a reduced-form causal effect of mentor quality on protégé promotion." (printed p. 241). The authors admit they cannot pin down the mechanism: "we are unable to identify the exact pathways through which mentor effects work" (printed p. 232). They frame it as an "exogenous social effect" in the sense of Manski (1993) (p. 231). Note for our framing: the effect could run through development (coaching) or through evaluation and sponsorship (the mentor writes the OER that the board reads). The paper does not separate these channels.
- **Limits:**
  - The outcome is early promotion (selection), not retention.
  - The sample is male combat-arms officers from West Point or ROTC who stayed through year 10. That is survivor selection, which this note cares about directly.
  - Quality is a binary proxy based on the mentor's own early promotion.
  - Randomness is shown only on observables.
  - The authors call the estimate "probably an upper-bound estimate on the impact of mentoring on promotion" (printed p. 250).

---

## 3. Johnson & Andersen (2010)

**Citation as printed:** W. Brad Johnson and Gene R. Andersen. "Formal Mentoring in the U.S. Military—Research Evidence, Lingering Questions, and Recommendations." *Naval War College Review*, Spring 2010, Vol. 63, No. 2 (Article 9), pp. 113–126. The article byline spells the name "Andersen"; the repository cover page and filename spell it "Anderson." Page numbers below are the journal pages printed on each page, not the repository's 1–15 footer numbers.

- **Design/data:** A narrative literature review with recommendations. It contains no new data.
- **Claim (b): there is no evaluation of formal military mentoring.** "In spite of the fact that U.S. military commands have instituted broad and sweeping requirements for mentoring, including formal mentoring programs in many locations, a careful review of the literature reveals not a single published evaluation of the efficacy of formal military mentoring." (printed p. 117)
- **Claim (b): informal mentoring does better than assigned mentoring, in civilian evidence.** "In fact, not a single well-controlled study has shown formal mentoring to be superior to informal mentoring." (printed p. 117)
- **Claim (b, c): in the military, seniors start mentoring relationships.** "when mentoring occurs, it is often because a senior person in the military initiates the relationship; it is possible that hierarchical elements of the military culture make mentee-initiated relationships less likely" (printed p. 116).
- **Claim (b): mentoring is only part of career success.** "It is important to keep in mind that mentoring accounts for only a portion of the explained variance in career success for military personnel." (printed pp. 119–120)
- **Causal language:** The review leans on correlational civilian literature, e.g., meta-analytic findings of "significant positive correlations" (p. 114). Its conclusion section states "Mentoring matters" (p. 121) but immediately concedes that "there is nearly no published evidence regarding formal mentoring efforts in the military" (printed p. 121).
- **Limits:** The review is from 2010 and predates Lyle & Smith (2014). It is Navy-centric. Its main subject is formal mentoring programs, not mentors assigned through the chain of command.

---

## 4a. `files/390/16.html` — U.S. Army STAND-TO! page, "Army Talent Alignment Process"

**Citation as printed:** "Army Talent Alignment Process." U.S. Army STAND-TO! Provided by Headquarters, Deputy Chief of Staff, Army G-1/ Army Talent Management Task Force. Wednesday, October 16, 2019. URL (from `.bib`): https://www.army.mil/standto/archive/2019/10/16/ . HTML, so there is no page number.

- **Design/data:** An official Army public-affairs explainer. It gives no data on match outcomes.
- **Claim (c): officers and units express preferences in a regulated market.** "The Army Talent Alignment Process (ATAP) is a decentralized, regulated, market-style hiring system which aligns officers with jobs based on preferences."
- **Claim (c): both sides rank each other.** "ATAP is transparent- all participating units and officers can see each other. Officers are matched to available assignments based on their preferences as well as those of their organization."
- **Claim (c): when it began.** "ATAP First Iteration- The market for Assignment Cycle 20-01 (Winter 2019-20), the first in which officers and units were able to select and preference one another based on KSB-Ps, recently closed. These officers will begin Permanent Change of Station (PCS) moves starting in October 2019." KSB-Ps are knowledge, skills, behaviors, and preferences.
- **Claim (c): earlier steps.** "AIM 2.0 Implementation - The Army distributed orders to over 12,000 officers during the 19-02 (Summer) distribution cycle through the Assignment Interactive Module (AIM) 2.0 program."
- **Claim (c): officers get more choice.** "Army Talent Alignment Process gives officers the opportunity to choose from a wider variety of assignments which best suit their KSB-Ps. The organizations have access to a greater number of available officers to preference the right people for their teams."
- **Who makes the final match:** **NOT FOUND.** The page uses the passive voice ("Officers are matched …"). It does not say whether an algorithm, Human Resources Command, or someone else makes the final match. The only hint is a link label in the "Related videos" list: "Army Talent Alignment Process Algorithm." That label is not a statement about who decides.
- **Retention-related framing (focus quote on the same page):** "We must adapt to retain the best talent, which often has better options outside the Army." — Maj. Gen. JP McGee, director, Army Talent Management Task Force.
- **Causal language:** None. It is a description of policy.
- **Limits:**
  - This is promotional material.
  - It gives no figures on how many officers got a preferred assignment, how many went unmatched, or which side wins ties.
  - The 2019 start date means officers in Spain et al. (classes 1992–2007, observed through 2012) and in Lyle & Smith (1998–2008) were assigned under the older system those authors describe.
  - STAND-TO! stopped publishing in May 2022, per the banner on the page.

## 4b. `files/385/308346.html` — Kane (2011), *The Atlantic*

**Citation as printed:** Tim Kane. "Why Our Best Officers Are Leaving." *The Atlantic*, January/February 2011 Issue (section "U.S."). URL (from `.bib`): https://www.theatlantic.com/magazine/archive/2011/01/why-our-best-officers-are-leaving/308346/ . HTML, so there is no page number.

- **Design/data:** An opinion essay by Tim Kane, who writes in the first person and was a former Air Force Academy cadet. **The saved snapshot is truncated by the paywall** ("To read this story, Sign in or start a free trial."). Only the dek and the first two paragraphs are present.
- **Claim (main thesis, from the dek):** "Why are so many of the most talented officers now abandoning military life for the private sector? An exclusive survey of West Point graduates shows that it's not just money. Increasingly, the military is creating a command structure that rewards conformism and ignores merit."
- **Claim (main thesis, from the body):** "The military's problem is a deeply anti-entrepreneurial personnel structure. From officer evaluations to promotions to job assignments, all branches of the military operate more like a government bureaucracy with a unionized workforce than like a cutting-edge meritocracy."
- **Claim (Kane quoting the Army War College):** "Since the late 1980s … prospects for the Officer Corps' future have been darkened by … plummeting company-grade officer retention rates. Significantly, this leakage includes a large share of high-performing officers." Kane attributes this to "A widely circulated 2010 report from the Strategic Studies Institute of the Army War College."
- **Survey details:** **NOT FOUND in the snapshot.** It names only "An exclusive survey of West Point graduates." Secondhand details come from Spain et al. (2023): "more than 93% of West Point officers believed that at least one-half of the best officers they knew decided to leave the military instead of staying until retirement age" (Spain et al., printed p. 2), and "sample size (N = 248) and survey response rate (4%)" (Spain et al., printed p. 26, note 1).
- **Causal language:** The essay asserts causes ("the problem isn't cultural"; a personnel structure that "rewards conformism and ignores merit"). These claims are not empirically identified.
- **Limits:**
  - It is an opinion essay.
  - The survey measures perceptions of who leaves, not actual exit.
  - The response rate is low (about 4%, per Spain et al.).
  - The snapshot is truncated.
  - Spain et al. (2023) test the claim directly with administrative data and do not support it.

---

## Bottom line for (a), (b), (c) — no claims beyond the sources

- **(a) Selective exit:** In West Point classes 1992–2007, exit was selective, and it removed **lower** cadet military performers more than higher ones. Top performers stayed at the same rate past year 6 and at higher rates past year 10 (Spain et al. 2023, pp. 15, 19, 22). This is evidence that the pool left to compete is positively selected on a pre-entry score. It does not show that performance causes staying.
- **(b) Assigned leaders change careers:** Lyle & Smith (2014) give a reduced-form causal estimate under assignment that is as good as random on observables. A high-performing assigned battalion commander raises a protégé's early promotion by about 2.7–2.8 points, from a 9.2% base, or about 29% (pp. 232, 242–243). The outcome is selection (promotion), not retention. The paper cannot separate development from evaluation, because the mentor is also the rater. No source here gives a verified mentor effect on **retention**; the requested Carter–Dudley–Lyle paper was not in the library.
- **(c) Choice vs. assignment:** Before 2019, junior officers had "little influence over their next assignment" beyond listing installation and family preferences (Lyle & Smith 2014, pp. 233–234). From Assignment Cycle 20-01 (Winter 2019–20), ATAP is a "regulated, market-style" two-sided preference system (STAND-TO!, Oct. 16, 2019). The page does not say who makes the final match.
