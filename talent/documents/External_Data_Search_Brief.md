# External Data Search — Brief for LLM / Scholar GPT

Given the research, data, and criteria below, please suggest specific publicly available datasets, data repositories, or published papers that provide data meeting these criteria, so we can test whether our main finding replicates in other settings. Include names of datasets, where to access them, and why they fit.

---

## 1. Research context (plain language)

We study **career advancement in a hierarchical organization** (U.S. Army officers). The central idea is that **performance is evaluated in relative terms within "pools"** — groups of people who are compared to each other (e.g., everyone rated by the same senior rater in a given period). We ask: **Does the quality of your rating pool — the average performance level of your peers in that pool — predict your own probability of promotion?**

- **Setting**: Military officers; promotion from Captain to Major (and related career outcomes).
- **Performance measure**: "Top block" (TB) share — the fraction of top performance ratings an officer receives. This is analogous to a forced-curve or relative ranking.
- **Pool**: We define a "rating pool" by **senior rater × time window** (and optionally rank, branch). So everyone rated by the same senior rater in a given period is in the same pool. Pool quality = mean TB (or mean of a standardized performance measure) in that pool.
- **Outcome**: Promotion (time to promotion, or binary promotion by a cutoff), analyzed with survival / competing-risks methods (Cumulative Incidence Function, CIF).

We are **not** only asking "do higher-performing people get promoted more?" (they do). We are asking whether **the average quality of the pool you are in** — independent of your own performance — predicts your promotion probability, and whether that relationship is linear or nonlinear.

---

## 2. Data we have had access to

- **Personnel snapshots** (project internal: "502"): Officer-level records at fixed points in time — rank, unit (UIC), dates (commissioning, promotion to CPT/MAJ), snapshot date. Used to define the cohort and time axes.
- **Performance evaluations** (project internal: "512"): Officer Evaluation Reports (OERs) — who was rated, by which rater and senior rater, evaluation period, and "top block" (TB) outcome (e.g., percentage of top ratings). We use **senior rater** as the key for defining pools.
- **Pipeline outputs** (project internal: "520"): Combined cohort with OERs attached to snapshots; **pool definitions** (senior rater × time/rank); **pool-level metrics** (e.g., mean TB in pool, "pool minus mean" — individual TB minus pool mean); **time to promotion** and event indicators; covariates (branch, job code, etc.). Unit identifiers (UIC) available for linking to battalion/brigade/division in future work.
- **Restrictions**: Our data are proprietary (Army); we cannot share them. We are looking for **public** data with a similar structure so we can test replication.

---

## 3. Coding and analysis pipeline (summary)

- **Data construction**: Snapshots (502) + OERs (512) → assignment of OERs to officers at snapshot dates → cohort with time-varying pool metrics (520).
- **Pool definition**: Pools = senior rater × time window (and optionally rank/branch). For each officer at each snapshot we compute: (a) the mean TB (or similar) in that officer’s current pool; (b) individual TB ratio or "pool minus mean" (deviation from pool).
- **Analysis (Run 1, "17_1")**: We model **promotion** (competing risks) as a function of pool quality and individual performance. Predictors include **mean TB in the rating pool** (or pool-minus-mean). We use **equal-width bins** of the pool-quality variable (not quantiles) and plot **Cumulative Incidence of Promotion (CIF)** by bin and **Final CIF** (promotion probability by end of observation) by bin.

---

## 4. Initial findings (what we want to replicate)

- **Main result**: As **mean TB in the rating pool** (pool quality) **increases**, **promotion probability (CIF) first increases** — officers in higher-quality pools are more likely to be promoted, consistent with positive signaling or positive peer context.
- **Second part of the result**: At **very high pool quality**, we see **diminishing returns** — promotion probability **declines** for the highest pool-quality bins. The relationship is an **inverted U**: low pool → lower promotion; medium/high pool → higher promotion; very high pool → lower promotion again.
- **Robustness**: The pattern holds with **8 bins** and with **25 equal-width bins**; it is not an artifact of a single binning choice.
- **Interpretation (working)**: Relative evaluation in pools; pool quality may act as context or signal. At very high pool quality, increased competition for a limited number of promotion slots, or greater visibility/comparison, may reduce individual promotion likelihood — a "diminishing returns" or "too much talent in the room" effect.

We want to know whether this **inverted-U relationship** (pool quality → promotion first up, then down at the top) appears in **other domains** with **public data**.

---

## 5. Mechanism (concise, for data search)

- **Relative evaluation**: Performance is assessed relative to others in a defined group (pool).
- **Pool quality**: The average performance level in that group can be measured (e.g., mean rating, mean percentile).
- **Outcome**: A discrete advancement event (promotion, selection, admission to next tier) that is at least partly competitive (limited slots or places).
- **Hypothesis**: Advancement probability increases with pool quality up to a point, then may decrease at very high pool quality (inverted U), due to competition, slot constraints, or visibility effects.

Any setting with **individuals**, **defined peer/pool groups**, **performance or ranking within the group**, and **an advancement/selection outcome** could in principle be used to test this.

---

## 6. Data criteria for replication (required and preferred)

Use these criteria when suggesting datasets. We need data that are **publicly available** (or at least replicable with a standard request) and that allow the following:

### Required

| Criterion | Description |
|-----------|-------------|
| **Individual-level records** | Each row (or linked records) corresponds to a person, not only aggregates. |
| **Performance or ranking measure** | Some measure of performance, rating, rank, or relative standing (e.g., score, percentile, top-block share, grade, publication count). Can be repeated over time. |
| **Defined "pool" or peer group** | A way to group individuals so that we can compute **mean performance (or mean of the measure) within the group**. Examples: same manager/rater, same firm, same cohort, same department, same team, same geographic unit, same time window. |
| **Advancement / selection outcome** | A clear outcome that reflects "moving up" or "being selected": promotion, hire, admission, selection to next tier, retention to next period, etc. Ideally with timing (time to event) or at least binary by a cutoff. |
| **Public or replicable** | Data accessible to researchers (repository, replication package, open data, or standard application process). |

### Strongly preferred

- **Longitudinal or repeated measures**: Multiple time periods or repeated evaluations so we can define pools over time and observe outcomes after pool exposure.
- **Multiple pools**: Many distinct pools (e.g., many managers, many firms, many cohorts) so we can compare pool quality across groups.
- **Hierarchy or competition**: Setting where advancement is at least partly competitive (limited slots, relative evaluation, or tournament-like).

### Domains that might fit (non-exhaustive)

- **Employment / HR**: Performance ratings by manager or unit; promotion or turnover; firm or team as pool.
- **Academia / science**: Publications, citations, or rankings; department or field as pool; promotion, tenure, or job move as outcome.
- **Sports**: Performance metrics; team or league as context; selection to national team, draft, or next level as outcome.
- **Education**: Test scores or grades; school, class, or cohort as pool; admission or graduation as outcome.
- **Military / government (other)**: Other countries’ personnel or evaluation data if public.
- **Competitions / contests**: Rankings or scores; cohort or round as pool; advancement to next round or tier as outcome.

---

## 7. What we are asking you (the LLM) to do

# External Data Search — Brief for LLM / Scholar GPT

Given the research context, data we have used, initial findings, mechanism, and criteria above:

1. **Suggest specific publicly available datasets** that meet (or closely meet) the criteria in Section 6. For each suggestion, please give:
   - **Name of dataset** (and citation or URL if you know it).
   - **Where to access it** (repository, paper, institution).
   - **Why it fits**: which variables would serve as (a) individual performance/ranking, (b) pool definition, (c) advancement/selection outcome.
   - **Any limitations** (e.g., no time dimension, pools too small, outcome not quite "promotion").

2. **Suggest published papers** that use data with this structure (individuals + pools + performance + advancement) and that might provide replication data or point to public datasets. Paper name, authors, and what data they use.

3. **Suggest repositories or search strategies** (e.g., ICPSR, Harvard Dataverse, OSF, discipline-specific repositories, or search terms) that are likely to return datasets with: performance/ratings + group/pool definition + promotion/selection outcome.

4. **Optional**: If you know of settings where this *mechanism* (relative evaluation, pool quality, competitive advancement) has been studied under another name, mention them so we can search for data in those literatures.

---

## 8. References (internal)

- **Analytical roadmap**: 525_plans.md (UIC, senior rater, longevity, path analyses).
- **Publication strategy**: Publication_Plan.md (mechanism, venues, external data).
- **Advisor conversation**: 260313_Paper_directions (transcript) — emphasis on replication in 2–3 settings for a stronger interdisciplinary story.

---

*End of brief. Paste this document into your chosen LLM and add your specific request (e.g., the sentence in the "How to use" box at the top).*
