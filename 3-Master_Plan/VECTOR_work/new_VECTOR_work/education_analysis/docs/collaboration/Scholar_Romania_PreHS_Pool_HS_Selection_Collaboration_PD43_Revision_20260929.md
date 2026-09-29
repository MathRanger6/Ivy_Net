# Scholar VECTOR ↔ new VECTOR Collaboration — Romania Pre-HS Pool → High-School Selection (PD43 Revision)

**Date:** 2026-09-29  
**Prepared by:** Scholar VECTOR  
**For:** Charles Levine and new VECTOR  
**Status:** Revised scientific-design record incorporating the 2026-09-29 PD43 discussion with Alex Gates. Structural feasibility checks are authorized as specified below; substantive outcome analysis is not yet authorized.

## 1. Why this revision exists

Charles briefed Alex Gates on the proposed Romania reframing. The discussion materially sharpened the design.

The revised idea remains:

\[
\boxed{
\text{middle-school/gymnasium environment}
\rightarrow
\text{individual performance}
\rightarrow
\text{competition for limited high-school/track seats}
\rightarrow
\text{realized selective placement}
}
\]

But PD43 added two decisive scientific gates:

1. **Before doing anything else, determine whether gymnasiums actually differ enough in student performance/composition to provide meaningful peer-environment variation.**
2. **If separate national-exam and grades/GPA components exist, do not automatically use the composite transition score as the performance variable.** The composite is also the mechanical score used for allocation, so using it as both performance and selection input can leave little room to identify an environmental/congestion mechanism.

Alex's preferred first question was essentially:

> Do gymnasiums show enough sorting/differentiation in exam scores, grades, or related performance to make the proposed peer-pool comparison meaningful?

Only after that should we spend effort defining a selection outcome.

---

# 2. What Charles told Alex — fact check

The conversation was broadly accurate. Several points should be preserved exactly; several should be qualified.

## Accurate

### Gymnasium is the pre-high-school environment

Students complete grades 5–8 in gymnasium before the centralized high-school allocation.

### Transition score combines two components

The paper states that the transition score equally weights:

1. performance on a national eighth-grade examination; and
2. grades 5–8 GPA.

Thus:

\[
T_i=\frac{1}{2}E_i+\frac{1}{2}G_i,
\]

where \(E_i\) is the national-exam component and \(G_i\) is the grades/GPA component, **if both components survive in our deposited files**.

### Students submit ranked school/track combinations

Students rank combinations such as a particular high school plus Mathematics, Natural Sciences, Social Studies, Literature, etc.

### Capacity is track-specific

Schools announce track-specific capacities in advance.

### Allocation is score-priority plus preferences

The Ministry's centralized computer processes students in descending transition-score order and gives each student the highest-ranked school/track preference that still has capacity.

No sibling preference, geographic priority, gymnasium diversity quota, or similar criterion is described in the paper's allocation algorithm.

### Our administrative replication data do not contain the submitted preference rankings

That is correct and remains the key limitation in interpreting realized placement as pure success/failure.

---

## Correct but requires qualification

### “They compete for high schools in the same town.”

The published authors treat towns as high-school markets and assume students generally restrict choices to their home towns because applicants are 13–14 years old.

However, the institutional rule itself allowed students to request high schools elsewhere in the country.

So use:

> **town × cohort is the authors' empirically motivated market approximation**

rather than:

> **students were legally restricted to compete only within town.**

### “The exam score is latent ability.”

Do **not** call the national exam score latent ability.

The national examination is a standardized measured performance component. It may be a useful **portable/pre-selection performance proxy** and may be less locally subjective than GPA, but it is still an observed test result after years of schooling.

Preferred language:

> national-exam performance / standardized performance proxy

not:

> innate or latent ability.

### “GPA is designed to differentiate people in a pool.”

GPA contributes directly to the transition score, so it clearly affects allocation.

But we have not yet established that Romanian middle-school grading is explicitly quota-based, rank-based, or otherwise rationed within gymnasiums.

Therefore GPA can be treated as an **environment-sensitive performance component**, but not yet as demonstrated congestion or a top-block equivalent.

---

## Needs correction

### “BCG/Baccalaureate entrance exam score”

The Baccalaureate is **not the high-school entrance exam**.

It is the high-stakes national examination taken near the end of high school. Passing is required to apply to university, and the grade is important for university admission.

Use:

> Baccalaureate grade / Baccalaureate performance

not:

> entrance-exam score.

### “The paper is about perceived emotional congestion.”

Too strong.

The paper studies the effect of access to better schools plus multiple behavioral/equilibrium responses involving:

- peers and relative standing;
- teacher sorting;
- parental effort;
- student behavior.

The relative-position/marginalization evidence is relevant to our drawback mechanism, but the paper is not primarily a paper about “emotional congestion.”

### “If you wanted math, did you get into the top math school?”

We cannot directly observe this because submitted preferences are absent.

We know assigned track, but we do not know whether the student preferred Mathematics, Literature, or another track.

Therefore we cannot define:

> success = received the top school in the track the student wanted

unless a separate source restores preference information.

---

# 3. PD43's central mechanistic insight

Alex raised the key concern:

> If high-school selection is mechanically determined by the same composite transition score we call “performance,” where is there room for congestion to matter?

This matters enormously.

If:

\[
T_i=\frac{1}{2}E_i+\frac{1}{2}G_i
\]

and \(T_i\) is exactly what the allocation computer uses, then conditioning on or treating \(T_i\) as the sole individual-performance variable may mechanically absorb the pathway we are trying to study.

The potentially interesting mechanism is instead:

\[
\text{gymnasium environment}
\rightarrow
\text{grades/GPA or other environment-sensitive performance}
\rightarrow
T_i
\rightarrow
\text{capacity-constrained placement}.
\]

Alex therefore suggested that if the separate components are available, we should consider the **national-exam component** and the **grades/GPA component** separately.

This becomes **Gate 0**.

---

# 4. Revised Gate 0 — Verify transition-score components before anything else

New VECTOR should determine, from the actual deposited data and codebooks, whether the clean 2001–2003 files contain separately identifiable:

- national eighth-grade exam performance \(E_i\);
- grades 5–8 GPA \(G_i\);
- composite transition score \(T_i\).

If the separate components exist, verify:

\[
T_i \stackrel{?}{=} 0.5E_i+0.5G_i
\]

up to rounding/documented transformations.

Also determine whether the national examination itself is decomposed by subject.

### Why this matters

If separate \(E_i\) and \(G_i\) exist, we can test a much sharper mechanism:

> Among students with similar standardized exam performance, does the gymnasium environment relate systematically to the grades/GPA component that enters the allocation score?

This is much closer to the Army analogy in which a relatively portable underlying-performance proxy and a more locally evaluated/subjective component can be distinguished.

### If the components do not exist

The design becomes weaker.

We may still study:

\[
\text{gymnasium peers}
\rightarrow
T_i
\rightarrow
\text{realized placement},
\]

but we must acknowledge that \(T_i\) is simultaneously the measured performance and the mechanical priority score for selection.

Do not conceal that limitation.

---

# 5. Revised Gate 1 — Test whether gymnasiums actually differentiate

Alex was explicit that this is the **first substantive empirical check**.

Before defining a success outcome, ask:

> Are gymnasiums meaningfully different in the academic composition/performance of their students?

Using only pre-high-school performance variables, report for gymnasium × cohort:

- pool sizes;
- mean and variance of \(E_i\), \(G_i\), and \(T_i\), as available;
- between-gymnasium versus within-gymnasium variation;
- distribution of gymnasium means within town/cohort;
- realized sorting measures, carefully defined;
- overlap in student performance across gymnasiums;
- number of gymnasiums per town/cohort;
- whether high- and low-performing students are meaningfully mixed across gymnasiums.

The key decision is not whether \(H_{\text{sort}}\) is “large” in the abstract.

The decision is:

> Is there enough cross-gymnasium differentiation and overlap to support comparisons among similarly performing students who developed in different peer environments?

If gymnasiums are nearly interchangeable mixtures, stop.

If gymnasiums are strongly differentiated but have no common-support students, causal/descriptive comparison is also limited.

The scientifically useful case is differentiation **plus some overlap**.

---

# 6. Revised peer and competitive pools

## Peer/development pool

Primary candidate:

\[
\boxed{\text{gymnasium}\times\text{cohort}}
\]

This is where grades 5–8 and the end-of-eighth-grade national exam are produced.

## Competitive pool

Primary approximation:

\[
\boxed{\text{town}\times\text{cohort}}
\]

because the authors treat towns as the relevant high-school market.

This must remain an empirical approximation, not a legal restriction of the allocation mechanism.

---

# 7. Revised Gate 2 — Only after Gate 1, define selection/success

Alex recommended keeping the first success measure simple and binary if possible:

> Did the student get into the top high school in the town?

This is attractive because it resembles:

\[
\text{drafted vs not drafted}
\]

or another easily interpretable selected/not-selected outcome.

However, preferences are missing, so the correct label is:

> **assigned to the top-ranked school in the town**

not:

> **successfully obtained the student's preferred top school.**

The outcome is **realized selective placement**, not pure preference-conditioned selection success.

---

# 8. How should “top school” be defined?

PD43 briefly suggested using average later Baccalaureate performance to identify prestigious schools.

Scholar VECTOR recommends **not** using same-cohort Baccalaureate performance as the primary ranking.

That would use a later outcome to define the prestige/selectivity of the placement we are trying to explain and risks post-treatment leakage/circularity.

## Preferred ranking measures

Use variables determined at or before assignment, such as:

1. school admission cutoff;
2. average incoming transition score;
3. minimum incoming transition score;
4. a prior-cohort version of one of these measures.

### Strongest option

A **prior-cohort selectivity ranking** is particularly attractive if stable enough:

\[
\text{prestige}_{s,t}
=
f(\text{incoming performance of school }s\text{ in cohort }t-1).
\]

Then the current student's own score cannot mechanically determine the school's prestige rank.

If prior-cohort ranking is too unstable or creates excessive missingness, use a same-cohort measure with explicit leave-one-out protection and report the mechanical-dependence risk.

## Baccalaureate outcomes

Baccalaureate performance can remain a **validation/descriptive indicator of school outcome quality**, but should not be the primary same-cohort ranking variable for the selection outcome.

---

# 9. Track-specific selection — defer unless preferences are recovered

Alex suggested simplifying to a single subject/track such as Mathematics or Literature.

This could be useful **if** we can define the relevant competitor population.

But because preferences are unobserved:

- assigned Mathematics students are not necessarily all students who wanted Mathematics;
- students assigned elsewhere may also have preferred Mathematics;
- students may rank cross-track alternatives.

Therefore:

> “Did you get the top Mathematics school if you wanted Mathematics?”

is not currently observable.

For the first pass, **top high school within town** is cleaner than track-specific success.

Track-specific analysis can be reconsidered only if:

- preference information is recovered; or
- a scientifically defensible competitor definition can be constructed without it.

---

# 10. Revised candidate outcome set

Do not choose yet. Develop and compare these options:

### A. Binary top-school placement

\[
Y_i=1\{\text{assigned to top-ranked school in town/cohort}\}.
\]

Advantages:

- simple;
- interpretable;
- close to Army/MBB binary selection.

Limitations:

- realized placement reflects preferences as well as ability/capacity;
- top-school rank must be defined without outcome leakage.

### B. Assigned-school selectivity percentile

Continuous or ordinal rank of the assigned school within the town.

Advantages:

- uses more information than binary top-school placement;
- less sensitive to a single arbitrary cutoff.

Limitations:

- still realized placement, not pure success;
- rank definition requires care.

### C. Admission-cutoff quality of assigned school

Assign each student the cutoff/selectivity of the school they enter.

Advantages:

- directly connected to capacity-constrained allocation.

Limitations:

- may mechanically covary with own transition score;
- needs prior-cohort or leave-one-out protection where possible.

---

# 11. Revised outcome leakage safeguards

For every placement/selectivity outcome, ask:

1. Does the focal student's own transition score enter the construction?
2. Does the focal student's gymnasium peer group enter the outcome construction?
3. Is the school ranking defined using the later outcome we are trying to explain?
4. Can prior-cohort ranking avoid same-cohort leakage?
5. If using same-cohort incoming scores, can leave-one-out construction materially reduce mechanical dependence?

Do not authorize a substantive HERO-style plot until these questions are answered.

---

# 12. Scarcity and \(K/N\)

The high-school/track capacities provide genuine \(K\).

But missing preferences still prevent a clean applicant denominator \(N\).

Town × cohort size is **not automatically the applicant pool for the top school** because not every student necessarily applied to it.

Therefore:

- do not call `capacity / town cohort` the true \(K/N\);
- treat admission cutoff/selectivity as the cleaner first scarcity measure;
- retain capacity as a documented institutional constraint.

If a future source recovers ranked preference sheets, then direct applicant-level \(K/N\) becomes possible.

---

# 13. Revised structural comparison with Army and MBB

## Romania

\[
\text{gymnasium peers}
\rightarrow
\text{exam/GPA/composite performance}
\rightarrow
\text{town-level HS competition}
\rightarrow
\text{capacity-constrained placement}
\]

## Army

\[
\text{unit/rating peers}
\rightarrow
\text{performance/evaluation}
\rightarrow
\text{broader advancement competition}
\rightarrow
\text{promotion/selection}
\]

## MBB

\[
\text{team peers}
\rightarrow
\text{performance/visibility}
\rightarrow
\text{national draft competition}
\rightarrow
\text{draft selection}
\]

The Romania design is structurally promising because the **peer pool and competitive pool are distinct**, as in the other domains.

The key Romania difference is that the selection algorithm is highly score-driven, making decomposition of the score components especially important.

---

# 14. Revised task for new VECTOR

**Recommended model: GPT-6 Astra — High.**

New VECTOR should produce a revised:

> **Romania Pre-HS Pool / HS Selection Feasibility Brief — PD43 Edition**

Do not run the substantive outcome model.

## Authorized structural checks

### Gate 0 — Score decomposition
- identify national-exam component;
- identify grades/GPA component;
- identify composite transition score;
- verify formula if possible;
- inspect subject decomposition if present.

### Gate 1 — Gymnasium differentiation
- gymnasium × cohort counts;
- pool-size distribution;
- mean/variance of available performance measures;
- within- versus between-gymnasium variation;
- differentiation within town;
- overlap/common support;
- preliminary sorting description.

### Gate 2 — Market structure
- verify gymnasium nesting within towns;
- quantify cross-town assignment if observable;
- identify exclusions/special markets such as Bucharest.

### Gate 3 — Candidate selection outcomes
Evaluate:
- binary top-school assignment;
- assigned-school selectivity percentile;
- assigned-school cutoff/selectivity.

For each, assess:
- preference ambiguity;
- own-score mechanical dependence;
- peer-score leakage;
- whether prior-cohort ranking can be used.

### Gate 4 — Go/no-go

Return one:

**GO**  
Gymnasium differentiation exists, score components permit a meaningful environmental mechanism, and a defensible realized-placement outcome can be defined.

**GO WITH LIMITATIONS**  
The design is scientifically useful, but placement must be interpreted as realized selectivity rather than preference-conditioned success and/or score decomposition is incomplete.

**NO-GO**  
Insufficient gymnasium differentiation, no meaningful overlap, missing score decomposition, or outcome circularity makes the mechanism test uninformative.

---

# 15. What not to do yet

Do not:

- generate HERO curves;
- inspect top-school outcome patterns;
- tune school-ranking definitions after looking at results;
- use Baccalaureate outcomes to select the prestige definition;
- define track-specific success from unobserved preferences;
- call the national exam “latent ability”;
- call GPA congestion without evidence of rank/quota-based grading;
- force a \(K/N\) denominator from town size.

---

# 16. Scholar VECTOR's parallel methodological work

Scholar VECTOR will examine:

1. whether a prior-cohort school-selectivity measure is the cleanest selection outcome;
2. how much preference omission biases binary top-school placement;
3. whether selection can be framed as **realized opportunity/placement** rather than preference-conditioned success;
4. whether exam-vs-GPA decomposition can support a benefits/drawbacks or congestion mechanism without overclaiming;
5. whether the gymnasium/town split provides a sufficiently close structural analogue to Army and MBB.

---

# 17. Updated immediate decision gate

The sequence after PD43 is now:

\[
\boxed{
\text{Gate 0: Do we have exam and GPA separately?}
}
\]

then

\[
\boxed{
\text{Gate 1: Are gymnasiums meaningfully differentiated with overlap?}
}
\]

then

\[
\boxed{
\text{Gate 2: Can we define non-circular realized selective placement?}
}
\]

Only if all three gates are satisfactory do we authorize substantive analysis.

---

# 18. PD43 takeaway

Alex did **not** recommend an open-ended Romania campaign.

His guidance was to:

1. simplify;
2. check gymnasium differentiation first;
3. see whether score components give room for an environmental mechanism;
4. define an intuitive selection outcome;
5. avoid spending excessive time if the structure is not there.

That is now the governing Romania plan.
