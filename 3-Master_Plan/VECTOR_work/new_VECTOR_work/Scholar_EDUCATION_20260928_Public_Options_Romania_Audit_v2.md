# Education Dataset Search — Revision 2 and Romania Feasibility Audit

**Date:** 2026-09-28  
**Prepared by:** Original VECTOR / Scholar GPT  
**For:** Charles Levine and new VECTOR  
**Status:** Bounded follow-up to the September 28 education shortlist

## Why this revision exists

The first bounded search correctly identified Trinidad & Tobago as an unusually strong conceptual and identification match, but it was too pessimistic about the remaining public-data options. After new VECTOR established that Trinidad's confidential microdata are not practical on the dissertation timetable, Charles asked whether public or near-public possibilities had truly been exhausted.

They had not.

A second targeted search focused specifically on **published education studies with downloadable replication microdata**, rather than only on conceptually ideal administrative systems. That search identified a substantially stronger immediate candidate:

> **Romania — Pop-Eleches & Urquiola, “Going to a Better School: Effects and Behavioral Responses,” American Economic Review 103(4), 2013.**

The associated openICPSR replication archive contains multiple downloadable Stata microdata files plus code and documentation. Romania therefore deserves an immediate bounded feasibility audit **before moving to restricted-use education data**.

This document updates the earlier shortlist and records the first feasibility findings.

---

# Updated Decision

## Do not move to restricted-use data yet.

The revised sequence is:

1. **Romania — immediate priority.** Public replication microdata are posted. Determine whether they support the peer-pool / performance / later-outcome analysis directly.
2. **Chicago selective-enrollment high schools — quick access audit only if Romania fails.**
3. **Kenya secondary-school admissions — quick access audit only if Romania and Chicago fail.**
4. Then reassess whether restricted-use NELS/ELS/HSLS acquisition is justified.

The broad search remains bounded. This is not authorization for another open-ended dataset hunt.

---

# 1. Romania: Why It Is Scientifically Interesting

Romanian students transition from middle school into high school using a nationally centralized allocation system.

A student's **transition score** is based on performance on a nationwide 8th-grade examination and prior GPA. Students submit preferred **high-school/academic-track combinations**. The Ministry then assigns students in score order to their preferred school/track combinations until predetermined capacity constraints bind.

This creates admission cutoffs at the transition score of the student filling the final available slot.

The published study exploits almost 2,000 school-level regression-discontinuity quasi-experiments.

## The empirical sequence is unusually close to our architecture

**PRIOR PERFORMANCE**

Transition score based on 8th-grade national testing and GPA.

↓

**ASSIGN**

Centralized, score-ordered assignment to school/track combinations subject to predetermined capacity.

↓

**PEER ENVIRONMENT**

Assigned high school and, importantly, assigned academic track.

Tracks function approximately as “schools within schools”: students in a track take their coursework together and generally do not take classes with other tracks.

↓

**SORTING / RELATIVE POSITION**

The same transition score that determines assignment can characterize incoming peer quality and the focal student's relative standing inside the assigned environment.

↓

**LATER PERFORMANCE / SUCCESS**

For the 2001–2003 admission cohorts, administrative records are linked to whether students took the Baccalaureate examination and how they performed.

This is not a perfect port of Army/MBB congestion. Scarcity primarily governs **entry into the peer environment**, while the later Baccalaureate outcome is not itself a fixed-K award. Nevertheless, the setting is exceptionally useful for separating prior performance, assigned environment, peer quality, relative position, and later outcomes.

---

# 2. Public Replication Archive — Verified Availability

The openICPSR archive for the AER paper publicly lists:

- `data-AER-1.dta` — approximately **314.3 MB**
- `data-AER-2.dta` — approximately **123.2 MB**
- `data-AER-3.dta` — approximately **429.8 MB**
- `data-AER-4.dta` — approximately **4.8 MB**
- `data-AER-5.dta` — approximately **5 MB**
- additional smaller `.dta` files on the second archive page
- three Stata `.do` files
- README files in PDF and DOCX formats

The archive is therefore materially different from a “code only” replication package.

**openICPSR project:**  
https://www.openicpsr.org/openicpsr/project/112645/version/V1/view

**DOI:**  
https://doi.org/10.3886/E112645V1

**AER paper:**  
https://pubs.aeaweb.org/doi/10.1257/aer.103.4.1289

A free ICPSR login may be required to download files through the current interface. That is an access-interface issue, not a restricted-data application.

---

# 3. What the Published Data Documentation Establishes

The published paper states that the administrative data cover the **2001–2007 admission cohorts** and contain:

- student identity/name in the authors' source data;
- originating gymnasium;
- transition score;
- allocated high school;
- allocated academic track.

For the first three cohorts, **2001–2003**, these records were linked to:

- whether the student took the Baccalaureate examination;
- the student's Baccalaureate exam grade.

The paper explicitly defines peer quality using the **average transition score of the students encountered at school** and shows discontinuities in this peer-quality measure at admission cutoffs.

The paper also reports that crossing a school cutoff raises average peer transition score by roughly **0.2 standard deviations on average** in its RD setting.

This confirms that prior performance and peer-quality construction are not speculative uses invented for our project; they are central variables in the published study.

---

# 4. Peer-Pool Feasibility

## School-level pool

**Feasible in principle.**

Allocated school plus transition score are explicitly documented. If the public replication files preserve those identifiers at the individual level, we can calculate:

- school/cohort mean prior ability;
- leave-one-out school/cohort peer ability;
- focal student's relative position;
- realized sorting measures such as `H_sort`.

## School × track pool

**Potentially even better.**

Students apply to and are allocated into school/track combinations. Students in a track take their coursework together, making track a more behaviorally meaningful peer environment than the entire school.

If the public files preserve school, track, and cohort identifiers, the natural pool candidate becomes:

> **admission cohort × school × academic track**

This should be evaluated before defaulting to school-level pools.

## Classroom-level pool

**Partial / not primary.**

When schools have multiple classes within a track, the Ministry does not determine the class allocation. The paper reports classroom information for only a subset of schools and indicates that many schools further sort students by transition score.

Classroom should therefore be treated as a possible secondary analysis, not the primary public-data design.

---

# 5. Prior Performance

Romania has a particularly strong baseline measure.

The transition score is observed **before assignment to the high-school environment** and is based on:

- nationwide 8th-grade test performance; and
- prior GPA.

That gives us a defensible temporal ordering:

> prior performance → assigned peer environment → later outcome.

This is cleaner for our conceptual experiment than constructing “performance” from a measure observed after the student enters the pond.

---

# 6. Later Outcome

For the 2001–2003 cohorts, the published administrative linkage provides at least two later outcomes:

1. **Baccalaureate taken** — binary.
2. **Baccalaureate exam grade** — continuous.

The paper treats the Baccalaureate as a high-stakes graduation examination and reports effects on exam performance.

For our purposes:

- `Baccalaureate taken` provides a binary transition/outcome measure.
- `Baccalaureate grade` provides a continuous later-performance measure.
- A passing/high-performance threshold may potentially create an additional binary success measure, but it should be used only if directly supported by the replication data/documentation and scientifically justified.

Do not manufacture a binary “success” variable merely to imitate Army promotion or NBA drafting.

---

# 7. Scarcity and K/N

Romania contains genuine capacity constraints, but its scarcity architecture needs careful interpretation.

Schools submit **track-specific capacities** before assignment. Students are processed through a centralized mechanism that prioritizes higher transition scores and honors preferences until those capacities bind.

The admission cutoff is the transition score of the student filling the last slot.

This provides:

- a directly meaningful **cutoff/selectivity measure**;
- known conceptual capacity `K` at the school/track level;
- a real competition-for-entry mechanism.

However, the published administrative description says the authors' data do **not** contain students' ranked school/track preferences. Therefore a clean applicant denominator `N` for every school/track may not be reconstructable from the replication microdata.

As with Trinidad, do not force a complex matching/choice system into a misleading single `K/N` if the risk set cannot be defined defensibly.

For Romania, the **admission cutoff / cutoff percentile** may be a more faithful empirical measure of selection intensity than an artificial K/N.

---

# 8. Identification Opportunity

The study provides a strong regression-discontinuity design.

Students just below and just above school/track admission cutoffs have very similar transition scores but access meaningfully different school environments.

This is valuable because it separates:

> rich description of peer environments

from

> credible variation in assignment to different peer environments.

However, the original authors explicitly caution against interpreting the cutoff effect as a pure peer effect. Multiple school characteristics and behavioral responses change at the cutoff.

For our dissertation, that means:

- Romania is excellent for studying the consequences of assignment into a stronger pond.
- It is not automatically a causal identification of **peer quality alone**.
- Our descriptive LOO/HERO analysis and the paper's RD analysis would answer related but distinct questions.

That distinction should be preserved.

---

# 9. Behavioral / Relative-Position Relevance

The Romania paper is especially interesting because the stronger environment changes more than test scores.

The published study reports that students entering more selective schools recognize that they are relatively weaker and report feeling more marginalized; teacher and parent behavior also responds to the stratified environment.

That makes Romania relevant not merely as another peer-quality dataset but as a setting in which **relative position inside a stronger pond is itself behaviorally salient**.

This is close to the conceptual territory motivating the Army and MBB work, even though the institutional selection process differs.

---

# 10. Initial Component Score

| Criterion | Romania assessment |
|---|---|
| Prior ability/performance | **Strong** |
| Assignment process | **Strong** |
| Identifiable peer environment | **Strong if school/track identifiers survive in public files; published source confirms they exist in administrative data** |
| Assortative sorting | **Strongly measurable in principle** |
| Congestion/competition | **Strong for entry into school/track; weaker for downstream within-pool competition** |
| Selection intensity K/N | **Capacity/cutoff strong; denominator N may be unavailable** |
| Later success/outcome | **Strong for Baccalaureate participation and grade** |
| Longitudinal linkage | **Strong for 2001–2003 cohorts** |
| Identification opportunity | **Excellent RD assignment variation; not a pure peer-effect instrument** |
| Immediate accessibility | **Promising: public replication microdata are posted** |

---

# 11. What Still Must Be Verified in the Actual Public Files

The public archive's existence does not by itself prove that every variable used by the paper survives in the posted microdata in a form suitable for our analysis.

Before declaring Romania ready, inspect the actual `.dta` files and README and answer:

1. Which data file contains the 2001–2003 administrative student panel?
2. Is there a stable individual identifier?
3. Are admission cohort/year, town, assigned school, and assigned track present?
4. Is transition score present at the individual level?
5. Can school/track/cohort pools be constructed directly?
6. Are Baccalaureate participation and grade present?
7. Are school/track cutoff variables or sufficient information to reconstruct them present?
8. Are the public data already transformed into cutoff-relative observations in a way that destroys the original peer-group identifiers?
9. What is the usable sample size after requiring prior performance, pool identifier, and later outcome?
10. Can LOO peer ability and `H_sort` be calculated without importing external restricted information?

This is the decisive feasibility gate.

---

# 12. Minimal Proposed Empirical Experiment if the Files Pass the Gate

Do not execute this yet. This is the conceptual target for the audit.

For each student in a defensible cohort × school/track pool:

**Own prior performance:** transition score.

**Peer environment:** leave-one-out mean transition score among assigned peers.

**Sorting:** realized `H_sort` using transition score and assigned pool.

**Later outcome:** Baccalaureate participation and/or grade.

Then ask:

> Conditional on prior performance, how does later success/performance vary with the prior ability of the peer environment into which the student was assigned?

A second layer can exploit admission cutoffs to examine students with nearly identical prior scores who gained access to different environments.

This would let Romania contribute both:

- our common descriptive peer-environment experiment; and
- a stronger assignment-based identification analysis.

Again, those are separate estimands and should not be conflated.

---

# 13. Updated Status of Other Candidates

## Trinidad & Tobago

**Preserve as the strongest conceptual/full-architecture future candidate.**

Do not pursue immediately because confidential SEA records require a research application and the posted instructions warn of an access process on the order of months.

## Norway

Scientifically excellent but restricted administrative access makes it unsuitable for the immediate sprint.

## NYC exam schools

Retain as a strong methodological/comparison case. Public replication materials exist, but it is less directly matched to downstream congestion.

## Charlotte-Mecklenburg

Retain as a component candidate; richer administrative outcomes are not immediately public.

## Project STAR

Retain as a peer-effects methodological benchmark, not a congestion replication.

## Chicago selective-enrollment high schools

**New quick-audit backup.** Scientifically interesting because published work links admission to stronger environments with relative-rank mechanisms and later outcomes. Verify whether usable student microdata are actually included in the replication archive only if Romania fails.

## Kenya secondary-school admissions

**New quick-audit backup.** Centralized selective-school admission and RD variation are promising. Verify public microdata availability only if Romania and Chicago fail.

---

# 14. Operational Recommendation

### Immediate action

**Audit the Romania public replication files.**

Do not initiate restricted-data applications yet.

### Stop rule

If the public Romania files preserve:

- prior transition score;
- assigned school/track/cohort;
- later Baccalaureate outcome;

then stop searching and build a bounded Romania analysis specification.

If those identifiers were stripped or the public files cannot reconstruct peer pools, perform a quick access audit of Chicago, then Kenya.

Only after those public possibilities fail should restricted-use education data become the immediate path.

---

# 15. Message to New VECTOR

Original VECTOR is actively conducting this Romania feasibility audit.

This revision supersedes the earlier implication that the feasible public education search was exhausted after Trinidad. The Trinidad feasibility work remains valid and should be preserved.

**Do not duplicate the Romania external search while Original VECTOR is auditing it.**

New VECTOR should preserve the current NELS:88 / HS&B:80 work and provenance, but should **not invest substantial effort in restricted-use acquisition until the Romania gate is resolved**.

Once Original VECTOR reports the public-file schema, Charles and new VECTOR can decide whether Romania should enter the immediate education-analysis workspace.

---

# Current Judgment

Romania is not yet declared usable.

But it is sufficiently promising—and sufficiently accessible—that **restricted-use education data should wait until this public replication package is audited.**
