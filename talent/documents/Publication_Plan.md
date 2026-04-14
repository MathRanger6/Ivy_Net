# Publication Plan — Mechanism, Venues, External Data

**Analytical roadmap** (525 analyses, divisions, UIC/senior rater, longevity, path): see **525_plans.md**.

This document covers: mechanism articulation, research communities/venues, and external data search for replication.

**Brief for LLMs** (full context + data criteria for external data search): see **External_Data_Search_Brief.md**. Use that document when pasting into GPT, Scholar GPT, or other models to ask for dataset suggestions.

**Brief for LLMs** (mechanism × venues, per-community articulation + rollup table prompts): see **venues_and_mechanism_articulation_llm_brief.md**. Use with Scholar GPT / GPT for §1.2–§1.4 (mechanism + communities); transcript: `260313_Paper_directions_otter_ai.txt`.

**Advisor status briefing** (twofold plan: 525/coding vs publication, mapped to 2026-03-13 conversation): **advisor_brief_twofold_status.md**.

---

## 0. Intro — Research, data, and initial findings (summary)

- **Research**: We study whether **rating-pool quality** (mean performance of peers in your evaluation pool) predicts **promotion probability** for U.S. Army officers. Pools are defined by senior rater × time (and optionally rank/branch); performance is "top block" (TB) share; outcome is promotion (e.g., CPT→MAJ), analyzed with competing-risks CIF.
- **Data we use**: Personnel snapshots (502), OERs (512), and a Cox/pool pipeline (520) that builds cohort, pool definitions, pool-level metrics (mean TB, pool-minus-mean), and time-to-promotion. Unit (UIC) data exist for future division/battalion/brigade linkage. Data are proprietary; we cannot share.
- **Coding**: 502 → 512 (OER assignment) → 520 (pool metrics, Cox, CIF). Run 1 (17_1): TB ratio and pool-minus-mean as predictors; equal-width bins; CIF and Final CIF by bin.
- **Initial finding**: **Inverted U**: Promotion probability **increases** as pool quality increases, then **decreases** at very high pool quality (diminishing returns). Result holds with 8 and 25 equal-width bins. We want to test whether this pattern replicates in other settings using **public** data — hence the external data search.

---

## 1. Way ahead (overview)

1. **Data & structure** — Get divisions (and UIC → battalion/brigade) working so rating pools can be associated with units. Supports both “which units are consistently strong-pool?” and “which senior raters (and at what echelon)?”
2. **Mechanism articulation** — Articulate what the mechanism is (why pool quality → promotion then diminishing returns); reframe for different audiences (management science, people analytics, OR/systems, business dynamics). Do this in parallel with coding.
3. **Analytical questions** — Use 525: which divisions/brigades/battalions are consistently high top-block pools? Which senior raters consistently have top pools? Optional: longitudinal look via LT OERs (senior rater as BN/BDE commander).
4. **Venues & communities** — Use mechanism framings to choose primary community (e.g. management science / Noshir Contractor–type; people analytics; OR/systems; business dynamics). One primary + one or two alternative framings.
5. **External data & robustness** — Use articulated mechanism to brainstorm domains where the same effect could appear; search for publicly available data and apply same style of analysis (Army + 2 others = stronger interdisciplinary story).

---

## 2. Mechanism articulation

- **Goal**: Develop a clear articulation of the mechanism underlying the main result (promotion probability rises with pool quality, then diminishing returns at very high pool quality).
- **Process**: Brainstorm and refine with GPT (or similar); articulate for **different communities** so we get distinct framings and literatures.
- **Outputs**: Short mechanism statements tailored to (a) management science, (b) people analytics, (c) operations research/systems, (d) business dynamics (MIT). Use these to refine the “thing we are measuring” and to guide literature search and venue choice.

*To be filled in as articulation work progresses.*

---

## 3. Research communities and venues

- **Primary candidates (evaluate in parallel)**: Management science (e.g. Noshir Contractor–type networks/orgs); **people analytics** as a co-equal track; operations research/systems (e.g. Peter Bailey–style flows, resource allocation, dynamic networks); business dynamics (MIT, dynamical systems framing: people in/out, flows). Not aiming at AER or core labor economics as primary home.
- **Not pursuing (as default primary)**: Deep labor-economics-only framing; generic HR trade press (not peer-reviewed research venues).
- **Interdisciplinary**: Major interdisciplinary journals would require either more results, additional data, or both; not the first target.

*To be updated with specific journals and literatures as mechanism framings solidify.*

---

## 4. External data search (replication / robustness)

- **Goal**: Identify **publicly available** datasets where the same type of algorithmic approach could be applied (performance/ratings/competition, with ranking or relative evaluation).
- **Use**: If the same “inverted U” or diminishing-returns pattern appears in 2–3 settings (Army + others), much stronger interdisciplinary paper.
- **Process**: Use articulated mechanism to brainstorm domains (e.g. scientific careers, sports, other hierarchical performance systems); then search for concrete, public data that fits.
- **Note**: Advisor suggested not ruling out scientific-career data (lab expertise); “magic number three” (Army + 2 other datasets) would support a more robust story.

- **Brief for LLMs**: For a **thorough, self-contained document** to paste into GPT-4/5, Scholar GPT, Claude, or other models when asking "where can I find data that meets these criteria?", use **External_Data_Search_Brief.md**. It includes full research context, data we have had access to, pipeline summary, initial findings, mechanism, explicit data criteria (required/preferred), and an explicit request section for the LLM.

### 4.1 Scholar GPT response (replication_data_search.md)

Full response is in **replication_data_search.md**. Summary:

**Recommended public datasets (from Scholar GPT):**

| Dataset | Access | Performance | Pool | Outcome | Limitation |
|--------|--------|--------------|------|---------|------------|
| U.S. OPM FedScope / EHRI | opm.gov/data | Grade / pay progression | Agency × unit × year | Promotion (grade) | No direct ratings |
| LEHD (Census) | lehd.ces.census.gov | Earnings growth | Firm × establishment | Job mobility / promotion | No ratings |
| NLSY97 | bls.gov/nls | Test scores, wages | Employer / occupation | Promotions | Weak pool definition |
| Add Health | addhealth.cpc.unc.edu | GPA, test scores | School × cohort | College admission | Educational setting |
| Florida Teacher Data | replication packages | Value-added scores | School × grade | Promotion / reassignment | — |
| IPEDS + OpenAlex | nces.ed.gov/ipeds, openalex.org | Publications, citations | Department × institution | Promotion (inferred) | — |
| Sports (NBA, etc.) | Kaggle / sports-reference | Player stats | Team × season | Selection / advancement | — |

**Key papers cited:** DeVaro (2006) promotion tournaments; Hoffman & Tadelis (2021) manager ratings & promotion; Bode et al. (2022) corporate promotion panel; Araki et al. (2016) personnel evaluations; Landry et al. (2018) bureaucratic promotion; Chingos & West (2011) teacher advancement; Du et al. (2012) performance ratings (SOEs); Grabner & Moers (2013) promotion decision metrics; Huang et al. (2019) ratings + promotion; Kroll & Vogel (2021) public performance systems.

**Repositories:** ICPSR, Harvard Dataverse, OSF, NBER Data.

**Keywords / literatures:** Promotion tournaments; relative performance evaluation (RPE); peer effects; rank effects ("big fish, small pond"); bureaucratic promotion.

**Scholar GPT conclusion — best replication opportunities:** (1) Firm personnel datasets, (2) Teacher administrative data, (3) Bureaucratic promotion data, (4) Academic career datasets. These settings best match defined pools, relative evaluation, and competitive advancement.

---

## 5. References

- **Advisor conversation**: 260313_Paper_directions (transcript).
- **Run 1 results**: 17_1 pipeline; CR CIF and bar plots (equal-width bins); diminishing returns at highest pool quality.
- **External data search (Scholar GPT)**: replication_data_search.md — full response with datasets, papers, repositories, and keywords.
