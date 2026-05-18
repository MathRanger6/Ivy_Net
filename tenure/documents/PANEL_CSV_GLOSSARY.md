# Faculty Panel CSV — Column Glossary

Applies to:
- `tenure_pipeline/R1_tenure_data.csv`
- `tenure_pipeline/faculty_panel_advisor.csv`
- Source: `tenure_pipeline/faculty_panel_with_pools.jsonl`

Generated from `panel_builder.py`, `pool_metrics.py`, and `openalex_resolver.py`.

---

## Section 1 — Person Identifiers

| Column | Type | Description |
|--------|------|-------------|
| `name_display` | string | Full name as it appeared on the department faculty page (e.g. `"Jane A. Smith"`). Scraped from HTML; may vary slightly across years for the same person. |
| `name_key` | string | Normalized lowercase version of the name used for de-duplication and matching (e.g. `"smith_jane_a"`). Not intended for display. |
| `faculty_id` | string | Internal unique identifier assigned by the pipeline (slug + name hash). Stable within a pipeline run; used to link rows for the same person across years. |
| `openalex_id` | string | OpenAlex author identifier (e.g. `"A2345678901"`). Used to pull publication counts from the [OpenAlex](https://openalex.org/) open scholarly index. Blank if no match was found (`match_confidence = NONE`). |

---

## Section 2 — Institution and Year

| Column | Type | Description |
|--------|------|-------------|
| `university` | string | Full institution name (e.g. `"Carnegie Mellon University"`). |
| `uni_slug` | string | Short machine-readable identifier for the institution (e.g. `"cmu"`). Used for joins and file naming. |
| `year` | integer | Calendar year of the observation. Each row represents one person–year. Data window is approximately 2000–2023. |

---

## Section 3 — Academic Rank

| Column | Type | Description |
|--------|------|-------------|
| `rank` | string | Rank of the person in that year, as parsed from the faculty page. |

### Rank values observed in the data

| Value | Meaning |
|-------|---------|
| `assistant` | Assistant professor — the tenure-track rank that triggers all tenure-related outcomes |
| `associate` | Associate professor — typically indicates tenure has been granted |
| `full` | Full professor |
| `endowed` | Endowed / named chair |
| `distinguished` | Distinguished professor |
| `lecturer` | Non-tenure-track lecturer |
| `senior_lecturer` | Senior lecturer (non-tenure-track) |
| `instructor` | Instructor (non-tenure-track) |
| `teaching_prof` | Teaching-focused professor (non-tenure-track) |
| `clinical` | Clinical professor |
| `adjunct` | Adjunct faculty |
| `postdoc` | Postdoctoral researcher |
| `fellow` | Research or visiting fellow |
| `visiting` | Visiting faculty |
| `research_prof` | Research professor |
| `research_scientist` | Research scientist |
| `senior_researcher` | Senior researcher |
| `scientist` | Scientist |
| `emeritus` | Emeritus faculty |
| `unknown` | Rank could not be parsed from the page (most common reason: title ambiguous or missing) |

> **Note for analysis:** The tenure outcome model focuses on rows where `rank = assistant`. Rows with other ranks are retained in the panel for context (e.g. to confirm a promotion event) but are not the unit of analysis for the survival model.

---

## Section 4 — Publications

Publication counts come from OpenAlex. They are **only populated when `match_confidence` ∈ {`HIGH`, `MEDIUM`, `MULTI`}**. Rows with `NONE` or `LOW` confidence have blank/zero publication counts and should be excluded from publication-based analyses.

| Column | Type | Description |
|--------|------|-------------|
| `pubs_year` | integer | Number of publications attributed to this person in OpenAlex for this specific calendar `year`. |
| `pubs_cumulative` | integer | Running cumulative publication count from the person's first observed year through the current `year`. Resets if the person's panel has gaps. |

---

## Section 5 — Tenure Track Spell

These columns describe the person's assistant-professor spell across all years in the data. They are the **same value repeated on every row** for a given person (person-level, not year-level).

| Column | Type | Description |
|--------|------|-------------|
| `ever_assistant` | boolean | `True` if the person was ever observed as an assistant professor in the data. `False` for people observed only at higher ranks (e.g. someone hired directly as an associate). |
| `first_asst_year` | integer | First calendar year the person appeared as `assistant`. Blank if `ever_assistant = False`. |
| `last_asst_year` | integer | Last calendar year the person appeared as `assistant`. Blank if `ever_assistant = False`. |
| `years_as_asst_so_far` | integer | In a given year-row, how many years the person has accumulated as assistant professor up to and including that year. Non-null only when `rank = assistant` in that row; blank for non-assistant-rank rows. |

---

## Section 6 — Tenure Outcomes

These are the three mutually exclusive outcome flags. Every person with `ever_assistant = True` falls into exactly one category: tenure, attrition, or censored.

| Column | Type | Description |
|--------|------|-------------|
| `tenure_event` | boolean | `True` if the person was observed transitioning to associate/full/endowed/distinguished rank within **2 years** of their last assistant-professor year (`gap_tolerance = 2`). This is the primary outcome variable. |
| `year_of_tenure` | integer | Calendar year of the promotion event. Blank if `tenure_event = False`. |
| `attrition` | boolean | `True` if the person was last observed as an assistant professor and then **disappeared from the data before the end of the observation window** without a promotion. Interpreted as leaving academia or leaving the field. |
| `censored` | boolean | `True` if the person was still appearing as an assistant professor near the **end of the observation window** (within `gap_tolerance = 2` years of the last data year). Their outcome is unknown — they may yet be promoted or leave. Right-censored in survival analysis terms. |

> **Survival analysis note:** `tenure_event` is the "event," `attrition` and `censored` are competing exit states. The Cox model treats censored observations appropriately; attrition is treated as a competing risk.

---

## Section 7 — Data Quality

| Column | Type | Description |
|--------|------|-------------|
| `n_snapshots` | integer | Number of times the person's faculty page was successfully scraped in a given year. A value of 1 is typical; higher values occur when multiple scrape passes captured the page. Used internally to assess data reliability. |
| `match_confidence` | string | Quality tier of the OpenAlex author match. See table below. |

### `match_confidence` values

| Value | Meaning | Use in analysis |
|-------|---------|-----------------|
| `HIGH` | Name match + institution found in OpenAlex affiliations + panel years overlap with affiliation years | Most reliable; use freely |
| `MEDIUM` | Name match + institution in affiliations, but year overlap was unclear | Reasonably reliable |
| `MULTI` | Multiple HIGH or MEDIUM candidates found — resolver picked the first one but the correct match is ambiguous | Use with caution; publication counts may belong to the wrong person |
| `LOW` | Name match only — institution was not found in OpenAlex affiliations | Weak match; treat publication counts as unreliable |
| `NONE` | No OpenAlex result returned for this person | No publication data; `pubs_year` and `pubs_cumulative` will be blank |

> **Recommended filter for publication analyses:** `match_confidence IN ('HIGH', 'MEDIUM')`. Excluding `MULTI` is conservative but appropriate for submitted work; including `MULTI` adds coverage but increases noise.

---

## Section 8 — Peer Pool Metrics

The "peer pool" for person *i* in year *t* is defined as **all other assistant professors at the same institution in the same year** who also have OpenAlex publication data. These metrics capture the quality of the talent pool surrounding each individual — the core theoretical construct of the research.

> **LOO = Leave-One-Out.** All pool statistics exclude person *i* themselves, so a person's own publications do not inflate their own peer benchmark.

| Column | Type | Description |
|--------|------|-------------|
| `pool_size_all` | integer | Total number of assistant professors at the institution in that year (regardless of OpenAlex data availability). |
| `pool_size_oa` | integer | Number of assistant professors with OpenAlex data in that year (subset of `pool_size_all`). |
| `pool_size_oa_loo` | integer | Number of OpenAlex-matched assistants **excluding person *i***. Equals `pool_size_oa − 1` if person *i* has OA data, otherwise equals `pool_size_oa`. |
| `poolq_loo_mean` | float | Leave-one-out mean of annual publications (`pubs_year`) among peer pool members. The primary "pool quality" regressor in the Cox model. Blank if `pool_size_oa_loo = 0`. |
| `poolq_loo_sd` | float | Leave-one-out standard deviation of annual publications in the peer pool. Blank if `pool_size_oa_loo < 2`. |
| `pool_rank_loo` | integer | Person *i*'s ordinal rank within the full OA peer pool by publications (1 = lowest, `pool_size_oa` = highest). Blank if no OA data. |
| `pool_pctile_loo` | float | Person *i*'s percentile (0–100) within the full OA peer pool. Blank if no OA data. |

---

## Quick-Reference: Recommended Filters for Common Analyses

| Analysis goal | Suggested filter |
|---------------|-----------------|
| Tenure outcome model (main analysis) | `ever_assistant = True` |
| Publication-based covariates | `match_confidence IN ('HIGH', 'MEDIUM')` |
| Conservative publication filter | `match_confidence = 'HIGH'` |
| Pool quality regressions | `pool_size_oa_loo >= 2` (need SD) or `>= 1` (need mean) |
| Exclude right-censored | `censored = False` (caution: biases survival estimates — use Cox model instead) |
| Assistant-professor rows only | `rank = 'assistant'` |

---

*Glossary generated 2026-05-18. Contact: Charles Levine. Pipeline source: `tenure/tenure_pipeline/`.*
