# Education Dataset Search — Bounded Shortlist

**Prepared for:** Talent Net Research / VECTOR  
**Purpose:** Bounded education-data investigation aligned with PD41  
**Scientific structure:** prior ability → assignment/environment → peer composition/sorting → congestion/scarcity → later success

## Executive Summary

This bounded search identified **two unusually strong primary candidates, two useful component candidates, and one methodological benchmark**. Candidates were evaluated separately on prior ability, assignment, identifiable peer environment, assortative sorting, congestion, selection intensity K/N, later success, longitudinal linkage, and credible identification opportunity.

The strongest lead is the **Trinidad & Tobago centralized secondary-school assignment system**. It combines a common pre-assignment ability measure, ranked school preferences, capacity-constrained centralized assignment, identifiable school/cohort peer groups, and multiple later outcomes. A newer study covers approximately **329,481 students in 18 cohorts (1995–2012)**.

The second primary candidate is **Norway's centralized university-admissions system**, which provides scarce slots, rankings, thresholds, program peer environments, and later outcomes, but relies on restricted administrative microdata.

The remaining candidates—NYC exam schools, Charlotte-Mecklenburg school-choice lotteries, and Project STAR—are useful for particular components or methodological comparison but are less complete matches for the full congestion/selection mechanism.

## Shortlist

| Candidate | Classification | Ability | Assignment | Peer group / sorting | Scarcity K/N | Later success | Identification | Access |
|---|---|---|---|---|---|---|---|---|
| Trinidad & Tobago SEA → secondary schools | **Primary** | SEA entrance exam | Ranked choices + centralized allocation | School × cohort | Capacity / filled slots; promising reconstruction | Exams, tertiary qualification, adult outcomes | Assignment discontinuities / quasi-random assignment | Application; public replication code |
| Norway centralized university admissions | **Primary** | Application score | Ranked programs + centralized offers | Institution/field/cohort | Binding cutoffs/capacity | Enrollment, degree, earnings | Cutoff discontinuities | Restricted administrative |
| NYC exam schools | Component / strong benchmark | 8th-grade/admission scores | Cutoff | Exam-school peers | Oversubscribed seats; cutoff proxy | College outcomes | Sharp RD | Public replication package; microdata require verification |
| Charlotte-Mecklenburg lotteries | Component | Prior achievement | Lotteries | School/peer measures | Oversubscribed choice | Grades, course-taking, college completion | Randomized lottery | Mixed public/restricted |
| Project STAR | Methodological/component | Pre-assignment measures | Randomized classrooms | Classroom | No meaningful scarce advancement mechanism | Achievement/attainment extensions | Random assignment | Public variants/research data |

## 1. Trinidad & Tobago Centralized Secondary-School Assignment

**Classification: Primary candidate**

Students take the **Secondary Entrance Assessment (SEA)** at approximately age 11. Parents submit ranked secondary-school preferences, and the Ministry assigns students using examination scores and preferences through a centralized mechanism.

The Beuermann–Jackson–Navarro-Sola–Pardo dataset contains approximately **329,481 applicants across 18 SEA cohorts from 1995–2012**, covering 134 public secondary schools.

### Research fit

- **Prior ability:** SEA score before secondary-school assignment.
- **Assignment:** Ranked preferences combined with centralized assignment.
- **Peer environment:** Assigned secondary school × admitted cohort.
- **Sorting:** Incoming SEA scores permit characterization of cohort ability distributions and realized sorting.
- **Congestion/scarcity:** Limited school capacity and score/preference-based assignment. Replication materials include assignment/cutoff/selectivity routines. Exact applicant-level K/N should be verified before being called directly observed.
- **Later outcomes:** NCSE, CSEC and CAPE examinations; tertiary qualifications; scholarships; arrests; births; formal labor-market participation.
- **Longitudinal linkage:** Strong.
- **Identification:** Strong quasi-random variation around assignment thresholds.

The structure approaches:

**SEA ability → ranked choices → capacity-constrained assignment → school/cohort peer composition → later exams/attainment → adult outcomes.**

A dissertation-relevant question is: *Among students with comparable prior ability, how does assignment into school cohorts with different incoming ability distributions alter subsequent achievement or advancement, and does the relationship depend on selectivity or congestion?*

### Access

The administrative microdata are not an immediate public download. The public replication archive is substantial and includes analysis materials plus instructions for requesting raw data.

- Replication package: https://zenodo.org/record/6456606
- Review of Economic Studies paper: https://academic.oup.com/restud/article/90/1/65/6582595

### Limitation and next step

Do **not** begin a lengthy application yet. First inspect the public replication package and access instructions to determine whether acquisition is realistic within Alex's bounded education effort.

**Component assessment:** Ability strong; Assignment strong; Peer group strong; Sorting strong; Scarcity promising; K/N potentially reconstructable; Outcome strong; Longitudinal strong; Identification strong.

## 2. Norway Centralized University Admissions

**Classification: Primary candidate — access limited**

Applicants rank programs, possess application/admission scores, receive centralized offers, and face program-specific admission cutoffs. Published studies link these records to national administrative registers.

- **Prior ability:** Application/admission score.
- **Assignment:** Ranked preferences + centralized offers.
- **Peer environment:** Program/institution × cohort.
- **Sorting:** Peer quality constructible from applicant/admit scores.
- **Congestion/scarcity:** Limited program capacity and binding cutoffs. Exact K/N construction requires verification.
- **Later outcomes:** Enrollment, completed field/institution, attainment, earnings, and linked family outcomes.
- **Longitudinal linkage:** Strong.
- **Identification:** Excellent threshold/RD variation.
- **Access:** Restricted administrative microdata; documented researcher-access route, but not an immediate download.

Resources:
- https://leuven.economists.nl/2017/03/06/Field-of-Study-Earnings-and.html
- https://www.nber.org/papers/w20816

**Operational conclusion:** scientifically excellent, probably too slow for the current dissertation sprint.

## 3. NYC Exam Schools

**Classification: Component candidate / strong empirical benchmark**

Applicants just above and below exam-school cutoffs provide a strong comparison of similarly prepared students entering very different peer environments.

- **Prior ability:** Eighth-grade/admission performance.
- **Assignment:** Admission cutoff.
- **Peer environment:** Exam school × cohort.
- **Sorting:** Exceptionally clear.
- **Scarcity:** Oversubscribed seats; exact applicant-by-seat K/N not yet verified.
- **Later outcomes:** College enrollment, graduation, college quality.
- **Identification:** Excellent sharp RD.

Its weakness for this dissertation is that scarcity primarily governs **admission into the environment**, rather than an obvious scarce downstream distinction within the environment.

It may therefore be valuable as a **negative/comparison case**: a large peer-quality discontinuity does not automatically generate later outcome effects.

Replication package:
https://www.openicpsr.org/openicpsr/project/113901/version/V1/view

## 4. Charlotte-Mecklenburg School-Choice Lotteries

**Classification: Component candidate**

Lottery-based school assignment provides excellent identification and rich underlying administrative data.

- **Prior ability:** Repeated prior achievement.
- **Assignment:** Randomized school-choice lotteries.
- **Peer environment:** Assigned/chosen school.
- **Sorting:** Measurable.
- **Scarcity:** Oversubscribed choices; exact K/N availability requires verification.
- **Later outcomes:** Grades, course-taking, college enrollment, degree completion in richer studies.
- **Identification:** Excellent randomized-lottery variation.

Access is mixed. Public replication data exist for related school-effectiveness work, but the richer postsecondary-attainment package does not expose the complete underlying administrative microdata.

Resources:
- https://www.openicpsr.org/openicpsr/project/112805/version/V1/view
- https://www.openicpsr.org/openicpsr/project/112750/version/V1/view

## 5. Project STAR

**Classification: Methodological / component candidate**

Project STAR randomly assigned students and teachers to classrooms within Tennessee schools. Approximately **11,600 students across 79 schools** participated in the original K–3 experiment.

It is excellent for:

**prior ability → randomized classroom → peer composition → later performance/outcome**

but weak for:

**congestion → scarce SELECT**

because it lacks a natural limited-K advancement process analogous to Army top-block allocation, promotion, or the NBA draft.

**Conclusion:** retain as a methodological benchmark rather than pursue as the education replication.

## Recommended Next Step

**Stop the broad search.**

The clear lead is **Trinidad & Tobago**.

Conduct one small feasibility check on the public replication package and answer only:

1. What exactly is required to request the raw microdata?
2. Can N, K, or a defensible school-level selection-intensity measure be reconstructed?
3. Does the raw schema preserve student → assigned school → cohort sufficiently to calculate leave-one-out peer ability and H_sort?
4. Is the access burden compatible with Alex's bounded education-data effort?

If #4 is **no**, stop. The literature remains useful without creating another data-acquisition rabbit hole.

## Literature Value Independent of Acquisition

The Trinidad literature remains relevant even if the data are never acquired. Jackson's selective-school work directly examines whether higher-achieving peers explain selective-school benefits and uses assignment variation to distinguish peer quality from other school effects. It therefore belongs on VECTOR's literature-reading list regardless of whether Trinidad becomes a replication domain.

## Overall Recommendation

- **Pursue now:** Trinidad & Tobago — replication-package/access feasibility check only.
- **Preserve as high-value future possibility:** Norway centralized university admissions.
- **Preserve as empirical/methodological comparison:** NYC exam schools.
- **Do not pursue unless Trinidad fails and access appears easy:** Charlotte-Mecklenburg.
- **Retain for methodological context rather than replication:** Project STAR.

The purpose of this search was not to identify every plausible education dataset. It was to determine whether an unusually strong setting exists that preserves the distinctions among prior ability, assignment, peer environment, sorting, scarcity, and later selection. **Trinidad & Tobago is sufficiently strong to justify one additional bounded feasibility check.**
