# Romania: response to Scholar VECTOR and a proposed beginning map

**Last synced:** 2026-09-29  
**Audience:** Charles and Scholar VECTOR.  
**Current status — September 29:** **PAUSED; preserved as an unexecuted scientific proposal.** The subsequent [Romania stopping decision](Scholar_EDUCATION_20260929_Romania_Stopping_Decision_and_Next_Search_Gate.md) supersedes the recommendation to proceed with a first outcome pass. Reopen only for a documented linked downstream scarce selection outcome, or a specific dissertation need for environmental development analysis, with a newly agreed scope. The proposal below is retained as the reasoning record, not the current task.  
**Purpose:** Explain what we can measure, what those measurements mean, and a bounded sequence for examining Romania without searching for a preferred curve.

## 1. My recommendation

**Begin with students who entered with comparable measured performance, and ask two separate questions:**

1. **Examination participation:** Are students in stronger peer environments more or less likely to take the Baccalaureate examination?
2. **Later examination performance:** Among students who took the examination and have a recorded grade, do students in stronger peer environments receive higher or lower grades?

Before comparing outcomes, establish whether comparable students actually occur across meaningfully different environments. Keep the three admission cohorts visible separately. Treat school-track groups as the proposed primary peer environment, with school groups as one planned comparison.

This first look can establish which comparisons are possible and what relationships deserve interpretation. It will not by itself identify a causal congestion penalty.

**My response to Scholar VECTOR:** I agree that we should define the scientific quantities before plotting. I also agree that a positive published admission-cutoff result does not settle the relationship across the wider population. I would sharpen three points:

- **Above prediction does not automatically mean school-caused development.** Actual minus predicted performance can reflect school influence, family support, measurement error, or a prediction model that missed something.
- **Own performance, peer mean, and own-minus-peer performance are algebraically linked.** They do not provide three independent sources of information.
- **A positive relationship could coexist with an adverse mechanism.** It neither establishes nor rules out that opposing mechanism.

These cautions should guide a simple first analysis, rather than become reasons to build an elaborate model before examining the basic evidence.

## 2. What we have, and what still needs verification

**Existing repository evidence:** The September 28 audit found 334,137 student records in three ordinary administrative files:

- **data-AER-4.dta:** 107,812 records, admission cohort 2001.
- **data-AER-5.dta:** 110,912 records, admission cohort 2002.
- **data-AER-6.dta:** 115,413 records, admission cohort 2003.

The relevant fields are **grade** for prior transition performance; **year** for cohort; **ua**, **us**, and **us2** for town, school, and school-track grouping; and **bct** and **bcg** for examination participation and the recorded examination-grade measure.

**Already established:** The group identifiers nest consistently. Prior transition performance and the principal grouping fields are complete. There are 5,002 cohort-by-school-track groups. Median track-group sizes are 50, 56, and 60 across the three cohorts. Five groups contain one student; 28 groups contain fewer than ten students. Those last figures count groups, not affected students.

**Still to verify before interpreting differences:** Confirm the stored scale of **bcg**, including whether any file contains a transformed grade; the construction of the prior transition score; the deposited sample's coverage; and the meaning of the enrollment identifiers. A structurally complete group is not proof that we have every relevant student or that an admission group remained an unchanged classroom for four years.

The earlier handoff's variable descriptions are a starting point. Abbreviated variables in expanded files should not become canonical definitions merely because our notes repeat them.

**Published background:** The article reports improved later examination performance at better-school access thresholds, alongside behavioral responses involving teachers, parents, and students. This motivates considering several channels, while avoiding attribution of the total effect to peers alone. [Published article](https://doi.org/10.1257/aer.103.4.1289)

**Domain boundary:** We have not identified student-level university applications, admissions, enrollment destinations, majors, or degrees in this deposit. Baccalaureate participation is not college admission or a fixed number of winners selected from these school-track groups.

## 3. The beginning quantity map

The symbols below are local to this document. In particular, $B_i$ denotes Baccalaureate performance here; it does not rename the benefit component in our broader environment model.

### A. Own prior performance

$$
P_i=\text{student }i\text{'s pre-assignment transition score}.
$$

- **Source:** The field called **grade**.
- **Meaning:** Measured preparation before the high-school environment under study.
- **Use:** Compare students who started with similar measured preparation.
- **Limit:** Similar scores do not make students identical in motivation, family resources, preferences, or underlying ability. This is a performance measure, not pure portable talent.

Initially preserve the documented score units and compare within admission cohort. Standardization may help presentation later, but should not conceal differences in test construction or year.

### B. Assigned peer environment

For a proposed group $g$ containing $n_g$ students:

$$
Q_i=\frac{\sum_{j\in g}P_j-P_i}{n_g-1}.
$$

- **Meaning:** The average prior performance of the other students in the assigned group.
- **Use:** Describe the academic preparation of the environment.
- **Why leave the focal student out:** Their own score should not directly raise the average used to describe their peers.
- **Limit:** Higher measured peer preparation does not by itself establish stronger teaching, greater learning, or greater competition for a particular scarce resource.

**Measure peers using the original entry group.** A student who never takes the later examination still belonged to that assigned environment. Removing students with missing later outcomes before calculating peer means would redefine the environment using something that happened afterward.

A one-student group has no leave-one-out mean. Keep such cases in the accounting and explicitly mark that quantity undefined.

### C. Relative position

$$
R_i=P_i-Q_i.
$$

- **Meaning:** How far above or below the average peer the student started.
- **Example:** A score of 8 is one point above peers averaging 7, but one point below peers averaging 9.
- **Use:** Explain position in an environment.
- **Limit:** At fixed own performance, increasing peer quality necessarily lowers this relative position.

A within-group percentile describes another aspect of position. It responds to the distribution of peers, not just their average, but requires explicit treatment of ties and group size. I would reserve it as a supporting description rather than another primary comparison immediately.

### D. Examination participation and recorded grade

Define:

$$
T_i=\mathbf{1}\{\text{student took the Baccalaureate examination}\},
$$

and, among takers:

$$
O_i=\mathbf{1}\{\text{an examination grade is recorded}\}.
$$

Let $B_i$ denote the grade measure on its verified scale, observed when $T_i=1$ and $O_i=1$.

- **Participation question:** Does the student reach and take this examination?
- **Grade question:** How does the student perform among those with an observed result?
- **Missingness question:** Among takers, whose grades are absent?

The existing audit reports 275,719 takers: 257,433 with a recorded grade and 18,286 without one. Another 58,418 students are coded as non-takers. These are different situations.

**Example:** An environment might help more struggling students reach the examination. Its average grade among takers could then fall even though more students progressed. Conversely, a high average could reflect only the strongest students remaining in the observed group. Participation and grade availability are essential companions to the grade comparison.

### E. Later performance relative to prior-score expectations

A possible secondary quantity is:

$$
D_i=B_i-\widehat m_0(P_i,c_i),
$$

where $c_i$ denotes admission cohort and $\widehat m_0$ predicts the recorded grade among takers with observed grades, using prior score and cohort.

- **Meaning:** How far actual later performance lies above or below a specified prediction.
- **Illustrative example:** On a hypothetical verified grade scale, a prediction of 7 and an observed grade of 8 produce a difference of +1.
- **Limit:** This is not a direct observation of learning, the school's causal contribution, or the student's outcome in a different school.
- **Why defer it:** The benchmark needs a declared form, population, and validation rule. It should clarify the comparison rather than supply another opportunity to find curvature.

Subtracting the prior transition score directly from the later examination grade would require evidence of a common measurement scale. Similar numerical ranges are insufficient. Separately standardizing both tests would measure a change in relative standing, not establish a common learning scale.

## 4. Three mathematical distinctions

### 4.1 Relative position does not independently identify a mechanism

Because $R_i=P_i-Q_i$, knowing $P_i$ and $Q_i$ determines $R_i$.

For a model linear in these quantities:

$$
aP_i+bQ_i+dR_i=(a+d)P_i+(b-d)Q_i.
$$

There is no unique way to recover three separate coefficients from this identity. More generally, conditioning on own score and relative position contains the same information as conditioning on own score and peer mean.

**Implication:** Describing the comparison in both languages is useful. It does not independently distinguish the benefit of strong peers from the cost of weaker standing. A percentile can add information about the distribution, but still does not automatically identify a causal rank effect.

### 4.2 Subtracting a prediction does not create an independent test

Within the same cohort, prior-score level, and observed-grade population:

$$
\begin{aligned}
&E[D_i\mid P_i=p,Q_i=q,c_i=c,T_i=1,O_i=1]\\
&\quad=E[B_i\mid P_i=p,Q_i=q,c_i=c,T_i=1,O_i=1]
-\widehat m_0(p,c).
\end{aligned}
$$

Holding the benchmark fixed, subtraction changes the vertical level. It does not change the shape across peer environments at that fixed prior score.

A pooled residual plot, $E[D_i\mid Q_i=q]$, can look different because different environments contain different mixtures of prior scores and observed students. Its shape can also reflect benchmark misspecification.

**Implication:** A residual chart can be a convenient presentation. It is not independent confirmation, a substitute for comparing comparable students, or a device that automatically reveals hidden congestion.

### 4.3 Flattening is not necessarily a downturn

- **Positive slope:** Later performance increases with peer quality.
- **Positive but diminishing slope:** Performance still improves, by smaller amounts.
- **Negative slope:** Performance falls over that range.
- **A peak followed by decline:** The descriptive pattern ordinarily called an inverted-U.

A decreasing slope does not itself show that stronger environments have become harmful. Estimated derivatives can amplify noise and dependence on a fitted curve. Direct levels and transparent comparisons should come first.

A positive net relationship may coexist with an adverse mechanism in a conceptual model. The curve alone cannot establish that mechanism or tell us its magnitude.

## 5. Proposed peer pool

**Primary proposal:** Admission cohort × school-track identifier, operationally **year** plus **us2**, retaining **us** and **ua** for school and town.

**Reason:** This is closer to the instructional subdivision students enter. The authors' accessible working paper describes school-track choices and distinguishes tracks from smaller classes. The clean public files identify tracks, which should not be renamed classrooms. [Authors' 2011 working paper, introduction and institutional discussion](https://www.columbia.edu/~cp2124/papers/Pop-Eleches_Urquiola_NBER.pdf)

**One planned comparison:** School × admission cohort. This describes the broader institution, including students in other tracks. It is a different environment definition, not simply an inferior measurement of the same thing.

Before adopting the primary definition:

1. Confirm the identifier-to-institution mapping.
2. Report students affected by small groups, as well as the number of such groups.
3. Describe variation in prior scores between schools, between tracks within schools, and within tracks.
4. Keep later-outcome availability out of the peer-group definition.

**Minimum group size:** A leave-one-out mean requires at least two students. Do not silently impose ten because ten sounds stable. Any higher stability restriction should be agreed from group-size accounting before inspecting outcome patterns.

**Comparison discipline:** When comparing school and track definitions, retain the same focal students wherever possible. Otherwise results could change because both the population and environment measure changed.

## 6. A bounded sequence for the first pass

### Step 1 — Lock the meaning of the fields

**Question:** Do the names and numerical scales mean what we think?

**Proposed work:** Confirm transition-score construction, stored examination-grade scale, sample coverage, group identifiers, and missing-grade interpretation. Use existing documentation and audit outputs first; specify any additional data checks before execution.

**It tells us:** Whether the proposed measures can be interpreted.

**It does not tell us:** Whether an environment helps or harms students.

**Checkpoint:** If outcome coding remains ambiguous, pause that part of the analysis and identify the unresolved definition.

### Step 2 — Establish which comparisons actually exist

**Question:** Do similarly prepared students occur in meaningfully different peer environments?

**Proposed work:** Within each cohort, describe own prior score against peer mean, group sizes, and outcome availability. Determine where comparisons have adequate overlap: similarly scoring students actually appear in different environments.

**Example:** If virtually every student scoring around 9 attends a strong track, the data cannot reliably tell us what similarly scoring students experience in weak tracks. A smooth curve cannot create the missing comparison.

**It tells us:** Which contrasts are supported, and where sorting itself restricts what we can learn.

**Checkpoint:** Choose score bands, environment bins, geographic comparisons, and minimum cell counts from the comparison structure before inspecting outcome curves. Report independent schools or tracks as well as student counts.

Record sorting as a description of assignment using the prior score. Do not equate a sorting index with the model's homophily parameter $\rho$, or infer the penalty $\lambda$ from it. Any sorting-index interpretation must account for group sizes and its reference benchmark.

### Step 3 — Examine two outcome relationships together

Let $c$ denote cohort and $u$ denote town where a local comparison is feasible.

**First target: participation.**

$$
\pi(p,q,c,u)
=\Pr(T_i=1\mid P_i=p,Q_i=q,c_i=c,u_i=u).
$$

**Second target: grade among observed takers.**

$$
\mu_{\mathrm{obs}}(p,q,c,u)
=E[B_i\mid P_i=p,Q_i=q,c_i=c,u_i=u,T_i=1,O_i=1].
$$

**Required diagnostic:** The probability that a taker's grade is recorded, conditional on the same variables.

**Plain meaning:** Compare similarly prepared students, retain cohort and local context, and ask both who takes the examination and how recorded takers perform. Town accounts for some local differences; it does not make assignment random. If within-town comparisons are too sparse, report that limitation rather than quietly pooling unlike places and claiming the same comparison.

**Proposed presentation:** A small, consistent set of plots with separate cohort panels, counts, and uncertainty that accounts for shared school environments. Use the same supported score and environment ranges across paired outcomes where feasible. Do not force a quadratic curve or connect unsupported gaps.

Students at the same school share circumstances. Treating every row as independent would exaggerate precision. The eventual specification should declare school-level clustering within cohort, or an appropriate alternative, before estimation.

### Step 4 — Make one planned environment comparison

**Question:** Does the result depend materially on describing peers at the school or track level?

**Proposed work:** Compare the two definitions with the same outcomes, focal population, and cohort treatment. Report differences in the comparisons the data support.

Use all three cohorts in the first scope, but display them separately before pooling. Pooling immediately could hide different relationships.

**Checkpoint:** Preserve disagreement between school and track results. It may tell us something about the scale of the environment. It is not a reason to choose the more attractive picture.

### Step 5 — Review before adding machinery

The first return should explain:

- What we measured and which comparisons were supported.
- What participation, missingness, and recorded grades showed.
- Whether patterns differed across cohorts or peer definitions.
- What we can reasonably conclude and what remains unidentified.

Only then choose whether a prior-score-expectation plot, a focused interaction, or examination of the admission-cutoff design adds the most value. These are alternatives, not an automatic expanding checklist.

No residual sweep, catalogue of transformations, new dataset search, synthetic top-$K$ examination winners, or survey/classroom expansion is part of this proposed first pass.

## 7. How different results would guide us

**Monotonically increasing grades.**  
With participation and missingness also examined, stronger measured peer environments are associated with better recorded outcomes among comparable students over the supported range. This would neither establish nor rule out a hidden cost. Absence of an inverted-U would not make the investigation a failure.

**Little discernible relationship.**  
With narrow uncertainty and adequate overlap, the descriptive relationship is small over that range. Wide uncertainty or sparse comparisons would make the result inconclusive. A flat picture does not prove that positive and negative mechanisms cancel.

**A threshold or abrupt change.**  
Check track differences, outcome recording, cohort composition, and available comparisons. A visible step does not automatically have the causal interpretation of the authors' admission-cutoff design.

**A peak followed by decline.**  
First examine student and group counts, prior-score balance, participation, missing grades, cohort consistency, and the school-versus-track comparison. A surviving pattern would be a nonmonotonic conditional association worth explaining. It would not identify congestion as the unique cause.

**Different relationships for different prior-score ranges.**  
This would bear on whether the same type of environment has different implications for stronger and weaker entrants. To examine a “band of excellence,” define the band from prior performance before seeing outcomes. Do not select it around a discovered peak.

**Participation and grades move differently.**  
Treat this as information about progression and the composition of the tested population. Do not combine the two into a success score that hides the disagreement.

**A pattern appears only after a residual transformation.**  
Check the benchmark and changing student mixture first. The transformed picture is not automatically more informative than the original conditional comparison.

## 8. What this contributes to our broader theory

**Assignment:** Prior scores, choices, and capacity constraints place students into environments. Measured sorting describes that allocation.

**Environment and later performance:** The clean files permit comparisons of peer composition and later examination outcomes. These are the first proposed objects of study.

**Scarce selection:** Admission has limited seats. The later examination is not documented as a fixed-$K$ selection among these peers. A cutoff can describe admission selectivity, but it cannot numerically replace $K/N$ without a defensible capacity and applicant population.

**Identification:** The authors' regression-discontinuity design compares students near admission thresholds. It addresses a local change in access to a bundle of school features. Our first conditional descriptive comparison does not inherit that design's identifying assumptions.

A positive local access effect neither proves a globally increasing curve nor requires an inverted-U elsewhere. A descriptive downturn would not overturn the published local estimate without comparing populations, outcomes, and questions.

**What could travel across domains:** Distinctions among prior performance, sorting, environment, relative position, and later outcomes; evidence of relationships that differ with prior performance; and separation of conditional association from identified causal effects.

**What remains Romania-specific:** Examination participation, grade patterns, track organization, and the local effects of this allocation institution.

This dataset alone cannot establish that assortativity is necessary for the broader congestion-and-selection mechanism. It can clarify which environmental relationships coexist with sorting in a setting with an informative assignment process.

## 9. Proposed first agreement and stopping rule

> Use the three ordinary student-cohort files. Begin with school-track peers and retain school peers as one planned comparison. Verify field meanings and comparable students first. Then examine participation and recorded grades separately. Stop and review before adding another outcome construction or causal model.

The remaining implementation choices are limited: minimum group size; exact comparable-score and geographic comparisons; verified grade scale; and display and uncertainty rules. None should be chosen to generate a preferred shape.

**Stopping rule:** A supported positive, null, negative, or mixed relationship is an informative answer. If comparable students are absent from the environments we want to contrast, report that limitation. Do not create apparent coverage through extrapolation or keep changing definitions until a downturn appears.

## 10. Evidence record

- **Collaboration proposal:** [Scholar VECTOR's scientific quantity map](Scholar_Romania_Scientific_Quantity_Map_Collaboration_20260929.md). Scientific guidance, not new empirical evidence.
- **Existing direct-file audit:** [Romania public schema gate report](../source_audit/EDUCATION_20260928_Romania_public_schema_gate_report.md).
- **Structural counts:** [Saved pool-structure audit](../../outputs/romania_schema_audit_20260928/pool_structure_gate.json). The counts above come from this saved audit; it was not rerun for this response.
- **Field names and labels:** [Complete variable inventory](../../outputs/romania_schema_audit_20260928/variable_inventory.csv).
- **Earlier interpretation:** [September 29 Scholar handoff](../../handoffs/EDUCATION_20260929_Romania_Scholar_VECTOR_handoff.md). Unresolved expanded-variable definitions remain unresolved.
- **Primary publication:** Pop-Eleches and Urquiola (2013), [Going to a Better School: Effects and Behavioral Responses](https://doi.org/10.1257/aer.103.4.1289).
- **Institutional background:** [Authors' February 2011 working-paper version](https://www.columbia.edu/~cp2124/papers/Pop-Eleches_Urquiola_NBER.pdf). Exact replication definitions and numerical results should be checked against the published article and deposit.

The algebra and proposed sequence are VECTOR's reasoning. This document reports no newly fitted relationship, computed sorting result, or generated figure.
