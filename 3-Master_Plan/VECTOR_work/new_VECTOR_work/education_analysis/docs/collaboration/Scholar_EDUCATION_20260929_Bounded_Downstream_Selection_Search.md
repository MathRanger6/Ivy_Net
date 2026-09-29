# Scholar VECTOR — Bounded Downstream-Selection Education Search

**Date:** 2026-09-29  
**Prepared by:** Scholar VECTOR  
**For:** Charles Levine and new VECTOR  
**Status:** Bounded search completed. Romania remains paused. No new dataset is authorized for analysis.

## Executive conclusion

The narrower search used a harder gate than the earlier education search:

\[
\text{prior performance BEFORE}
\rightarrow
\text{identifiable peer environment DURING}
\rightarrow
\text{real scarce selection AFTER}.
\]

It also treated the **peer pool** and **competitive pool** as potentially different and kept eligible students, applicants, finalists/offers, and recipients separate.

### Bottom line

I did **not** find a public, ready-to-run dataset that cleanly satisfies all three layers at once.

However, the search produced three important results:

1. **Rosenzweig & Xu (2026)** is probably the closest scholarly mechanism paper to our theory yet found. It explicitly models classmates as both educators and competitors for rank-based academic rewards. But the authors state that their main NELS:88 analysis uses **restricted-use NELS:88**, augmented with external refugee-assignment data. This is a literature/mechanism lead, not an immediate public-data solution.
2. **Gates Millennium Scholars (GMS)** has the strongest real downstream scarce-selection event found in this pass: a national scholarship with applicants, finalists/non-recipients, and approximately 1,000 winners per cohort, plus longitudinal public-use data on winners and sampled non-winners. But I could not verify a usable public high-school identifier, so the preceding peer environment may be unreconstructable from public data.
3. **Selective-major systems** such as UC San Diego provide an almost ideal institutional competition after students have spent time at a university: continuing students apply for a limited number of major slots, applicants and selected students are counted, and selection uses prior college coursework/GPA. The missing piece is a research-ready longitudinal microdataset linking applicants to their preceding peer environments. This is a strong *data-acquisition target*, not a public replication dataset found today.

Therefore the search should **stop here rather than broaden again**.

---

# 1. Binding search architecture

A candidate had to be evaluated on:

### BEFORE
A defensible prior-performance measure observed before entry into the peer environment wherever possible.

### DURING
An identifiable peer environment with meaningful exposure and measurable peer composition.

### AFTER
A real, institutionally scarce opportunity with observed selection.

The competitive pool could differ from the peer pool.

For selection, distinguish where possible:

- eligible population;
- actual applicants;
- finalists/offers;
- selected recipients;
- accepted/enrolled participants.

A single \(K/N\) is not defensible unless its numerator and denominator describe a clearly defined competition.

---

# 2. Lead A — Rosenzweig & Xu: mechanism match, access problem

**Paper:** Mark R. Rosenzweig and Bing Xu, *Class Peers as Competitors and Educators: The Consequences of Rank-Based Academic Rewards* (2026 revision of NBER Working Paper 31135).

## Why it matters

This paper is unusually close to our conceptual model.

It explicitly treats classmates as simultaneously:

- **educators** through peer learning and assistance; and
- **competitors** because academic rewards depend on relative standing.

Their tournament model predicts that stronger peers can increase learning opportunities while also changing incentives for effort and peer assistance. Empirically, stronger peers reduce homework effort and peer assistance among high-performing students in schools where rank-based academic rewards are important.

This is extremely close to our benefits-minus-drawbacks logic and to the idea that competition is most consequential among students plausibly in the running for the scarce distinction.

## Data reality

The authors state that one of their two principal datasets is **restricted-use NELS:88**. They use its panel structure, effort measures, test scores, parent/teacher information, and school context, and augment the analysis with administrative information on refugee-cohort assignments.

Therefore:

- the paper should enter our core literature immediately;
- its variable definitions and competition-policy measures should inform how we inspect NELS/HS&B;
- but reproducing its design is **not** a quick public-data path.

## Classification

**High-priority theoretical/mechanism paper; restricted empirical path.**

---

# 3. Lead B — Gates Millennium Scholars: excellent competitive pool, uncertain peer pool

## Institutional competition

The Gates Millennium Scholars program awarded a genuinely scarce national scholarship.

The selection process had distinct stages:

1. completed/eligible applications;
2. reader scoring;
3. finalist/select/non-select status;
4. verification;
5. approximately 1,000 selected scholars per cohort.

Historical program reports document thousands to tens of thousands of applicants competing for 1,000 awards. One program report, for example, records 16,722 completed applications and 1,000 selected scholars; other years report applicant pools above 12,000.

The selection therefore has a real \(K\) and meaningful applicant/finalist populations.

## Public longitudinal data

ICPSR hosts the Gates Millennium Scholars data series.

The public survey data include:

- scholarship recipients;
- sampled non-recipients/finalists;
- high-school preparation and experiences;
- college choice;
- major choice;
- academic achievement;
- persistence and completion;
- graduate-education plans;
- later career outcomes.

Some cohorts have downloadable public-use files in Stata and other formats.

The program eligibility rules also include a pre-award GPA threshold (at least 3.3), Pell eligibility, and leadership/community-service criteria.

## The problem

The public data documentation reports the smallest geographic unit as **city** for the early cohort files. I did not verify a stable public high-school identifier that would allow us to reconstruct the student's actual high-school peer pool.

That is potentially fatal for our specific design.

GMS may give us:

\[
\text{prior preparation}
\rightarrow
\text{real national competition}
\rightarrow
\text{winner/non-winner}
\rightarrow
\text{longitudinal outcomes},
\]

but not necessarily:

\[
\text{identifiable high-school peer environment}
\rightarrow
\text{peer composition}.
\]

## Important sampling caution

The public longitudinal samples are not necessarily the complete original applicant pools. They contain scholars and sampled non-recipients/finalists. Program-level applicant counts can describe the competition, but the public analysis sample may not reproduce every applicant.

## Classification

**Component candidate with an excellent competitive pool; peer-pool gate unresolved and probably weak in public use.**

A future five-minute codebook check for a school identifier is justified. A larger acquisition effort is not yet justified.

---

# 4. Lead C — Selective/capped majors: institutionally almost perfect, no ready microdataset found

Several universities ration entry into majors **after students have already enrolled and completed college coursework**.

UC San Diego is an especially clean current example.

Continuing students apply to selective majors after completing required screening courses. Selection is explicitly capacity constrained: students with the highest selection scores are admitted until available slots are filled.

Published institutional statistics report both:

- number applied;
- number selected;
- selection percentage.

Examples from the Summer 2025 selective-major cycle include:

- Computer Science & Engineering: 76 applied, 25 selected;
- Mechanical Engineering: 126 applied, 35 selected;
- Public Health: 47 applied, 15 selected.

Historically, engineering major-change acceptance rates varied dramatically with the number of applicants and available slots.

## Why this is attractive

Conceptually:

\[
\text{college entry preparation}
\rightarrow
\text{university/course peer environment}
\rightarrow
\text{screening-course performance}
\rightarrow
\text{application to limited major slots}
\rightarrow
\text{selected/not selected}.
\]

This is much closer to Army/MBB than Romania because the scarce event occurs **after meaningful exposure to the educational environment**.

The competitive pool is explicit: applicants to a particular major in a particular cycle.

The peer pool could be:

- university cohort;
- college cohort;
- screening-course section/cohort;
- prerequisite-course peers.

## The problem

I found institutional counts and studies using internal applicant records, but **not a public longitudinal microdataset** that links:

- students' pre-environment preparation;
- their actual preceding peer environments;
- selective-major application;
- selected/not selected outcome.

## Classification

**Very strong institutional target for a direct data request or future collaboration; not an immediate public replication dataset.**

This may be more worth a targeted email/data request than a generic restricted NCES application because the institutional mechanism is exactly what we need.

---

# 5. Lead D — University of California STEM persistence: public and rich, but not scarce SELECT

Arcidiacono, Aucejo, and Hotz (AER 2016), *University Differences in the Graduation of Minorities in STEM Fields*, has a public AEA/openICPSR replication package containing student-level data.

The study observes:

- pre-college academic preparation;
- UC campus;
- intended/initial major;
- major persistence/switching;
- graduation and final major.

The paper finds that students whose preparation is weaker relative to their campus peers are more likely to leave science, especially at highly ranked campuses.

This is an excellent **relative preparation / pond-fit** setting.

But STEM graduation or switching is not a fixed scarce award allocated among applicants.

## Classification

**Strong public environment/relative-position comparison; not a downstream congestion-selection replication.**

It belongs beside Romania as supporting mechanism evidence rather than replacing Army/MBB structurally.

---

# 6. Lead E — Harvard Business School course allocation: excellent scarcity, weak longitudinal fit

Budish & Cantillon's AER course-allocation study has public openICPSR replication data containing student course preferences, course information, and allocation-related data.

The institutional mechanism is genuinely scarce: popular courses have limited seats and students submit preferences.

This cleanly identifies:

- preferences/applications;
- limited capacity;
- allocation outcomes.

However, the public package is designed to study the allocation mechanism itself. I did not find the necessary combination of:

- strong pre-environment student performance;
- meaningful prior peer environment;
- later individual success after course allocation.

## Classification

**Excellent market-design/scarcity example; poor fit for our longitudinal peer-environment question.**

---

# 7. Other settings screened

## Honors programs

Honors programs can have scarce admission and strong administrative data, and some studies exploit admission thresholds. But the most promising datasets I found are internal institutional administrative records rather than public replication microdata. Many honors admissions also occur at initial university entry, which repeats Romania's “scarcity creates the pond” issue rather than providing downstream selection.

## Undergraduate research

Research positions are genuinely scarce and occur after students enter college. Several studies document competitive selection and later outcomes. But I did not find a public applicant-level longitudinal dataset with a reconstructable preceding peer environment and winner/non-winner selection.

## Merit scholarships

Many scholarship studies observe eligibility or recipients, but most either:

- use threshold-based automatic aid rather than competition among peers;
- lack the preceding peer environment;
- or do not expose applicant-level public microdata.

GMS was the strongest scholarship candidate because it has real finalist/recipient stages and public longitudinal data.

---

# 8. What the bounded search teaches us

The difficulty is now very specific.

Public education datasets tend to give us **two of the three** pieces:

### Strong BEFORE + DURING, weak AFTER
Romania, UC STEM, NELS public files.

### Strong BEFORE + AFTER, weak DURING
Gates Millennium Scholars.

### Strong DURING + AFTER institutionally, data unavailable
Selective majors / competitive internal programs.

### Strong scarce AFTER, weak longitudinal person history
Course allocation.

This is useful. We are no longer searching vaguely for “better education data.” We know exactly which link is usually missing.

---

# 9. Recommended next decision

I recommend **not launching another broad search**.

Instead choose between two deliberate paths:

## Path 1 — Literature/mechanism path

Read Rosenzweig & Xu carefully and use it to sharpen the dissertation's theoretical account of peers as both educators and competitors.

This advances the science even if we never obtain their restricted data.

## Path 2 — Targeted data-acquisition path

Rather than immediately entering a generic restricted NCES process, target an institution where the mechanism is nearly ideal—especially **selective/capped major admission**.

Ask whether de-identified applicant-cycle records can provide:

- pre-college preparation;
- university entry cohort;
- screening-course performance;
- course/section or cohort peer identifiers;
- major application;
- major applied to;
- number of applicants;
- available slots;
- selected/not selected;
- later persistence/graduation.

A targeted institutional request may be scientifically more valuable than months spent obtaining a nationally representative dataset that still lacks the correct scarce event.

---

# 10. Current recommendation to Charles and new VECTOR

1. **Land and preserve the Romania stopping decision.**
2. **Add Rosenzweig & Xu (2026) to the immediate core reading list.**
3. **Do one tiny GMS public-codebook check for a usable high-school identifier; stop immediately if none exists.**
4. **Do not run a UC STEM replication now; retain it as supporting pond-fit evidence.**
5. **Do not broaden the public search again.**
6. If a fourth empirical domain is still needed after Alex's immediate assortativity work, consider a **targeted selective-major data request** before a generic restricted-use NCES application.

---

# 11. Most important conceptual result

The search supports new VECTOR's distinction:

> **The peer pool and competitive pool need not be the same.**

But both must be observable enough to define the mechanism.

The ideal education domain may involve students learning and developing among one set of peers, then competing against a broader or narrower set for a rationed opportunity.

That is structurally compatible with Army and MBB.

The missing dataset is not “one with better test scores.”

It is one that observes **both pools and the transition between them**.
