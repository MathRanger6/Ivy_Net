# Response to FOUNDY — Chapter 3, academic tenure (PEER)

**PEER → Charles / FOUNDY** | 13 November 2026 | **DRAFT** (no new scrape, no rerun, no edit to the manuscript or the pipeline)

Answers follow `20261113_Ch3_Questions_for_SCOUT_and_PEER.md` (Parts A and C). Part B is skipped.

The figure this response cites is the decision-year plot named in the questionnaire: `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM.png`, with provenance `HERO_tenure_q16_decision_dept_loo_infHM_provenance.json` (written 2026-09-02). The script that writes that provenance is `tenure/scripts/tenure_pass_a_decision_hero.py`. It calls `prepare_decision_hero_persons` in `tenure/tenure_pipeline/decision_hero_prep.py`, which calls `build_decision_cohort_records` in `tenure/tenure_pipeline/decision_year_cohort.py`, then `build_inverted_u` in `tenure/tenure_pipeline/stage9_analysis.py` with those people already built.

Older assistant-only plots (`tenure/scripts/tenure_pass_a_hero.py`, and Steps 1–4 of `TENURE_hero_pipeline.md`) are a different run. They are not the figure below.

---

## Correction to the executive-summary tenure paragraph

The paragraph in `5-Manuscript/03_Data_and_Empirics/drafts/20261109_Ch3_executive_summary_DRAFT.md` is right that rosters come from archived pages of US computer-science departments, that the peer measure leaves the person out, and that no school publishes a tenure quota. Four claims do not match the cited figure.

1. **Advancement is not “usually in the fifth or sixth year.”** Years 5 and 6 are a reference band that the code counts and then does not use as a filter. Of 391 resolved people, 63 (16%) fall in that band. The histogram runs from 1 to 9 assistant-years, and years 1–4 are the majority (70 + 91 + 76 + 72 = 309). **verified** — `decision_year_cohort.py` (`REFERENCE_ASST_TIME_MIN/MAX` are “tracked in stats, not an inclusion filter”) and the provenance `prep.asst_time_histogram`.
2. **The horizontal axis is not the person’s own publications per year of career.** Own career rate is Alex’s performance measure, and a separate figure uses it (`HERO_tenure_q16_decision_own_career_infHM.png`). The figure to cite plots the leave-one-out (LOO) mean of other faculty’s career rates. **verified** — provenance `spec.x_metric` = `decision_loo`.
3. **“Publication rate … in the year of the decision” is the career rate, not papers published that year.** The rate is cumulative works divided by years since the first counted publication, read in the last assistant year. Peers with no rate are left out of the average. They are not entered as zero. **verified** — `build_author_year_career_master.py` and `decision_hero_prep.py`.
4. **“The alternative is leaving” is only part of the non-tenure outcome.** Attrition includes a person who is gone while the department page still exists the next year, and a person who is still listed the next year under a title that is not associate or full (off the tenure track). Moves to another department under the same name are transfers and are excluded, not coded as “out.” **verified** — `panel_builder.py` `derive_dept_episode_outcome`.

The two limitations in the paragraph (no published quota; incomplete archives) still belong. Incomplete archives are handled by marking the person censored when the department has no saved page for the next year, and this figure drops censored people before the plot. The panel build recorded 1,225 censored episodes; the figure does not record how many of those were in the match tier it keeps. **verified** — `panel_rebuild_meta.json` and provenance `stage9_summary.n_censored` = 0.

---

## Part A — Shared outline

### A1. Why this system fits the five criteria

| Criterion | How tenure fits | Where it fits only partly |
|-----------|-----------------|---------------------------|
| **1. Observed performance** | Publication counts come from OpenAlex, not from the tenure decision. The locked performance measure is publications per year of career, `pubs_per_career_year`. **verified** — `build_author_year_career_master.py`. | The cited figure does not plot that measure. It plots other people’s career rates. A person’s own rate is missing for 111 of the 391 resolved people (`n_with_career_rate` 280). **verified** — provenance `prep`. |
| **2. Non-random groups** | The group is the computer-science department in the decision year. Hiring, not a random draw, puts faculty there. **verified** — `decision_hero_prep.py` builds `(uni_slug, decision_year)` rosters from the panel. | Whether departments are sorted by talent is a later chapter. Not answered here. |
| **3. Global selection** | A tenure case is a university decision about one person, not a contest that awards a fixed number of associate professorships inside the department and nowhere else. **recalled** — this is the institutional claim behind Alex’s criteria, not a column in the panel. | The code never observes a system-wide slate of openings. Each department’s cases are decided locally. The “global” part is an assumption about the academic labor market, not a measured field of candidates. |
| **4. Limited places** | The design treats the number of promotions as limited, so the bar can move. **recalled** — Alex’s criterion; no quota column exists. | No department in these data publishes a count of tenure slots. The chapter should call the limited-places claim an assumption. **verified** — nothing in the decision-hero scripts reads a slot count. |
| **5. Mostly closed** | The focal row is someone who was an assistant professor in the scraped department. Senior people who never appear as assistant are not decision events. **verified** — `load_panel_by_person` requires `ever_assistant`. | People enter as senior hires and can still sit in the peer roster. Assistants who show up later at another department are labeled transfers and removed (17 transfer episodes in the panel build). People still assistant when the archive stops are censored and removed from this figure. **verified** — `panel_builder.py`; `panel_rebuild_meta.json`. |

### A2. Search story (narrative)

**recalled** where the paragraph is project history; **verified** where a path is named.

The target was a setting in which an assistant professor’s record can be seen before the tenure decision, and the other people in the department that year can be seen too. College and Army data were already underway. Computer science at US research universities was chosen because department faculty pages are public, the Internet Archive has saved many of them, and publication databases can be joined to names. The school list was aimed at Carnegie research-university (R1) computer-science departments, not a convenience sample of pages that happened to parse. It started as nine schools chosen because their pages could be scraped, then grew in waves. The list in `tenure/tenure_pipeline/r1_schools_data.py` is the authority, and the overview records **168** schools. **verified** — `tenure/documents/TENURE_PIPELINE_OVERVIEW.md`, Cell 2 table (original 9; wave of 25 on 4 April 2026; wave of 80 on 5 April 2026; later waves to 168).

The first publication source considered alongside OpenAlex was DBLP. OpenAlex became the publication source for the panel. DBLP stayed as a cross-check, not the spine. **verified** — `tenure/documents/TENURE_DATA_GAMEPLAN.md` (OpenAlex primary; DBLP “cross-check spine only”).

Roster collection is a human-plus-archive loop, not a single download. For each school the pipeline queries the Internet Archive’s capture index for known faculty-page addresses, downloads saved HTML, and reads names and ranks with rules. Addresses that fail are hunted by opening a saved page and following the link that actually lists faculty. A person pastes an accepted address into `url_update_worksheet.csv`. That loop was still active in October 2026. It is why coverage is uneven: a school can have a roster in one era and a menu page, or nothing, in another.

Two designs were tried and then set aside for the chapter figure. The first peer pool was other assistant professors in the department that year, using papers published that year (`poolq_loo_mean` in `pool_metrics.py`). The second, locked with Alex on 2 September 2026 (PD29), is the whole department in the decision year, and the performance number is the career rate rather than that year’s paper count. The lock is written in `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md` and in `3-Master_Plan/transcripts/PD29_notes.md`. The reason for dropping the annual count was concrete: people who had just been promoted could show a zero annual rate, which is the wrong record of a career. **verified** — career-rate formula in `build_author_year_career_master.py`; PD29 table in `TENURE_hero_pipeline.md`.

What the code then did, and what the prose lock does not say, is that “around year 5 or 6” was stored as a reference band and not applied. The figure dated the same day includes every resolved assistant exit with a computable department mean.

### A3. Raw sources

| Source | Who publishes it | What one raw row is | Person identifier | Years in the file / years used | How it was obtained | Terms |
|--------|------------------|---------------------|-------------------|-------------------------------|---------------------|-------|
| Department faculty pages | Each university’s computer-science (or equivalent) site | One saved HTML page, not one person | None until parse | Plan targets 2000–2024, two seasons a year (near 15 March and 15 October). The figure does not record the calendar years of its 389 decisions. | Internet Archive capture index, then download of saved HTML. Ongoing on the Mac. **verified** — `TENURE_PIPELINE_OVERVIEW.md` Cell 3A. | **never checked** in the repo today |
| Parsed roster rows | This project, from those pages | A name and rank on one page in one year | `faculty_id` (department plus normalized name). It is stable inside one department episode. A move creates another id. | Panel build keeps 2000–2024. **verified** — `panel_rebuild_meta.json` `year_range`. | Rule-based HTML parse (`html_parser.py`), then the annual panel | Not a third-party license |
| OpenAlex authors and works | OurResearch, OpenAlex | Author-id resolution is one faculty member. Works-by-year is one faculty member in one publication year, with a count of works. | OpenAlex author id, joined to `faculty_id` | Career file years 1950–2026. Built 2 September 2026 from works last modified 19 April 2026. **verified** — `author_year_career_master_meta.json`. | Author search on the OpenAlex API. Works from the API or from the OpenAlex snapshot on Rivanna (`build_openalex_cache.py`). | Cite Priem, Piwowar, and Orr (2022), as the resolver docstring does. A formal terms review for the dissertation was **never checked**. |
| Career-rate table | This project | One faculty member in one calendar year from first counted publication through last | `faculty_id` | Same 1950–2026 span. 3,630 authors, all HIGH match, 99,733 rows. **verified** — the meta note says MEDIUM has no works rows in this file. | Derived from the works file. No new OpenAlex call. | — |

### A4. Linking records

**Roster name → OpenAlex author.** Match is on a normalized name plus the university’s OpenAlex institution, with a year-overlap check. Tiers, from `openalex_resolver.py`: **HIGH** (name, institution, and years overlap), **MEDIUM** (name and institution, years unclear), **LOW** (name only), **MULTI** (more than one HIGH or MEDIUM candidate; flagged for a person to review), **NONE** (no result). The decision cohort keeps HIGH and MEDIUM panel rows. The career-rate file used for the figure contains HIGH authors only. **verified.**

A single match-rate table for the whole panel was **not recorded** in the files read today. The low-confidence queue is `openalex_low_confidence.jsonl`. How many of those a person has reviewed, and the remaining error rate, were **never checked** today.

Known failure modes that the tiers themselves encode: a common name can attach the wrong author (LOW if the institution does not match; MULTI if several plausible authors match); a name change or a different spelling can return NONE. No saved count of those errors was read today.

**Same person, two departments.** A transfer is the same `name_key` appearing as an assistant at a different `faculty_id` and department. **verified** — `panel_builder.py` `_find_transfer`. That crosswalk is a rule, not a hand-edited alias file. Hand-curated inputs that should be described as such are the school URL list (`r1_schools_data.py`, edited through `url_update_worksheet.csv`) and any OpenAlex rows a person overrides. An override file was **not** confirmed today.

### A5. Cleaning and the final sample — flow table

Filters are in the order `tenure_pass_a_decision_hero.py` applies them. The peer mean is computed in `prepare_decision_hero_persons`, after the cohort exists and before binning.

The department roster used for that mean is **not** the cohort. `build_dept_year_rosters` takes every `faculty_id` with any panel row in that department and year, any rank, any match tier. The average then skips roster members who have no `pubs_per_career_year`.

| Step | What it does | Why | Before or after the peer mean | Count after |
|------|----------------|-----|-------------------------------|-------------|
| 1. Panel rows loaded | Stage 7 annual panel, all ranks | Spine | Before | **2,560,018** rows, **29,274** faculty ids. **verified** — `panel_rebuild_meta.json` |
| 2. Ever an assistant, with an outcome label | `panel_builder.py` labels tenure, attrition, censored, transferred | Defines an episode | Before | **2,331** ever assistant; **471** tenure events; **618** attrition; **140** of those off the tenure track; **1,225** censored; **17** transferred; **1,089** resolved (tenure or attrition). **verified** — same meta file. These counts are not limited to HIGH/MEDIUM. |
| 3. Match tier | Keep `match_confidence` HIGH or MEDIUM | Drop weak author links from the focal sample | Before | **not recorded** |
| 4. Drop transfers and `exclude_from_metrics` | Same-name move to another department is removed | A move is not an up-or-out outcome at the first department | Before | **not recorded** at this tier. Panel-level transfers are 17. |
| 5. Last assistant year, and resolved only | One row per person: the assistant row in `last_asst_year`. Keep if `tenure_event` or `attrition`. Drop if `asst_time` is missing. | Exit cross-section. Censored people are not “resolved,” so they drop here. | Before | People dropped for missing `asst_time`: **not recorded**. Next row is the first saved cohort count. |
| 6. Decision cohort | All resolved assistant-times. Years 5–6 are counted, not applied. | PD29 unit is a decision event; the code does not cut to year 5–6 | Before | **391** people: **191** tenure, **200** attrition, **47** off the tenure track (a subset of attrition), **280** with their own career rate, **63** in years 5–6. **verified** — provenance `prep` and `decision_year_cohort_meta.json` |
| 7. Leave-one-out department mean | At `(uni_slug, decision_year)`, average `pubs_per_career_year` of other roster members who have a rate. Drop the person if that mean is null. | This is the peer measure (B2) | This is the peer measure | **389** people kept; **2** dropped for a null mean; **0** had an empty department roster. **verified** — provenance `n_persons_with_x`, `n_dropped_null_x`, `n_empty_dept_pool` |
| 8. Bin and plot | 16 quantile bins on that mean. `exclude_censored=True` only changes the rate denominator. Everyone in this list already has `censored` false. No z-score. | Equal counts per bin | After | **389** people, **191** tenure, **198** attrition, **0** censored. **verified** — provenance `stage9_summary`. The two dropped people account for 200 − 198 attrition if both were attrition cases. That identity was not re-checked in the person file. |

### A6. The four concepts

**Performance.** Cumulative OpenAlex works divided by years since the first year with a counted work. In `build_author_year_career_master.py`: `career_age_years = year − first_pub_year`, and `pubs_per_career_year = cum_works / career_age_years` when age is at least 1. In the first publication year the rate is null, not zero. A later year with no new works stays in the series with `n_works` 0 and does not move the cumulative total, so the rate falls. Years before the first work are absent. There is no winsorizing on this figure (`z_score` false, `log_bin` false). Column: `pubs_per_career_year` in `author_year_career_master.jsonl`. On the plot row the person’s own value, when the other figure is drawn, is `own_career_rate`. **verified.**

Alex’s objection to a zero annual rate for promoted people is why this ratio replaced papers in the decision year. **verified** — `TENURE_hero_pipeline.md`, PD29 row “promoted-with-zero annual rate = wrong metric.”

**Group.** Everyone with a panel row in that `uni_slug` and decision year. The decision year is the last year the person is recorded as assistant (`last_asst_year`), not the later year in which an associate title may appear. Membership is whoever was parsed onto a saved page that year. The roster is not restricted to assistants and not restricted to HIGH match. **verified** — `build_dept_year_rosters`.

**Peer quality.** The cited figure uses **B2**, the leave-one-out mean: sum of other members’ `pubs_per_career_year`, divided by the number of other members who have a rate. Column on the plot row: `loo_mean` (also stored as `dept_loo_career_rate`). `pool_size_dept` is the full roster. `pool_size_rate_loo` is how many others contributed a rate. **verified** — `prepare_decision_hero_persons`.

| Label | In this code? | Used by the cited figure? |
|-------|----------------|---------------------------|
| **B1** full-group mean, including the person | Not computed in the decision-hero prep | No |
| **B2** leave-one-out mean of the others | Yes, `decision_loo` | Yes |
| **B3** own rate minus that leave-one-out mean | Not computed in this script | No |
| **B4** roster pressure (average of sigmoid-transformed competitive relevance) | No sigmoid or roster-pressure function under `tenure/` | No |

A department roster with nobody else who has a career rate produces a null mean, and the person is dropped. The saved run had 0 empty rosters and 2 null means. Groups of one are therefore out of the figure, not given a special peer value. **verified.**

The older column `poolq_loo_mean` is a different B2: leave-one-out mean of papers that year among assistants. It is not the axis of this figure.

**Advancement.** A tenure event is an associate, full, endowed, or distinguished rank at the same department in a year on or after the first assistant year. **verified** — `_PROMOTED_RANKS` in `panel_builder.py`.

Not advanced, among people who stay in the figure, is `attrition`: the department page exists the next year and the person is absent, or the person is present under a non-promoted title (`off_tenure_track`; 47 of 391). Those 47 stay in the denominator as not tenured.

Unresolved cases do not stay in this denominator. Censored means the department has no page for the next year, or the person is still an assistant at the edge of the scrape (`gap_tolerance` 0 in the panel rebuild). Transferred means the same name key is an assistant at another department. Both are excluded before the cohort. The figure’s `n_censored` is 0 because of that exclusion, not because nobody was censored in the panel.

### A7. Run of record

Cite `tenure/scripts/tenure_pass_a_decision_hero.py` with default arguments: `--x-metric decision_loo`, 16 quantile bins, inputs `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl` and `tenure/tenure_pipeline/author_year_career_master.jsonl`.

Provenance: `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json` (date in the file: 2026-09-02).

Sample: **389** people with a leave-one-out mean, **191** tenured, **198** attrition. Sixteen quantile bins. Filters are the table in A5. Sibling runs with 8 or 10 bins, and the own-career figure, are sensitivities. The 16-bin department leave-one-out figure is the one that matches the chapter’s peer-quality axis.

### A8. What is authoritative and what is superseded

For this chapter’s tenure figure, the authority is the decision-hero script, `decision_hero_prep.py`, `decision_year_cohort.py`, and the 2026-09-02 provenance. Outcome labels come from `panel_builder.py`. The career rate comes from `build_author_year_career_master.py`.

`TENURE_hero_pipeline.md` is right about the PD29 lock and wrong if a reader follows its “Step 1–4” v0 path (assistant-only leave-one-out, censored people included when bins are cut). Where that document and `decision_year_cohort.py` disagree, the code that wrote the provenance is the figure. The overview and the gameplan describe the scrape and OpenAlex spine; they are not the plot specification.

`tenure/scripts/tenure_pass_a_hero.py` and the `*_infHM_resolved_v0*` and `*_lastps_*` images are earlier exploratory plots. `pool_metrics.py` builds the old assistant-year pool. Do not cite them as the chapter figure.

### A9. Known quirks a careful reader should be told

- The decision is often early. Years 1–4 of assistant time are 309 of 391 resolved people. A last assistant year of 1 can be a real short spell, a broken rank parse, or a department page that only exists for one year. Which of those dominates was **never checked** in this pass.
- `asst_time` counts assistant-ranked years between the first and last assistant year. It is not years since the doctorate. **verified** — `asst_time_at_exit` in `panel_builder.py`.
- The career file for this build is HIGH-match authors only. MEDIUM focal people can enter the 391 and still have a null own rate. Peers without a HIGH works row are omitted from the mean rather than treated as having zero papers. **verified** — `author_year_career_master_meta.json`.
- Duplicate `(faculty_id, year)` work rows keep the max count, not the sum. **verified** — `build_author_year_career_master.py`.
- Two path prefixes exist for the same saved HTML (`tenure/tenure_pipeline/...` and `tenure_pipeline/...`). That is a scrape-storage quirk. It does not change the 389, which was already collapsed to people.
- Rank on a page is whatever the HTML rules return. A menu page can yield no names. A page the rules misread can yield the wrong rank. No rank-error rate was found in the files read today.
- Department coverage is lumpy. The panel build recorded 1,957 department-year pairs with any scrape row, and stage 8 recorded 621 department-years in the old assistant pool. **verified** — `panel_rebuild_meta.json`. The share of the 168 schools with a usable page in each year was **not recorded** as one number.

### A10. What can be said in print

The cited figure is binned rates. It does not print names. The panel itself stores `name_display`. Whether the dissertation may name a faculty member, and whether a human-subjects review applies to public faculty pages plus OpenAlex, was **never checked**.

OpenAlex should be cited as Priem, Piwowar, and Orr (2022), which is the citation in `openalex_resolver.py`. Internet Archive terms of use were **never checked** in the repo today.

### A11. Reproducibility

The plot inputs are on the Mac under `tenure/tenure_pipeline/`: `faculty_panel_with_pools.jsonl`, `author_year_career_master.jsonl`, and the OpenAlex works and author-id files those were built from. The HTML archive is `tenure/tenure_pipeline/faculty_snapshots/`. Rebuilding works from the OpenAlex snapshot is a Rivanna job (`build_openalex_cache.py` against a Connected Data Hub tree such as `~/cdh/OpenAlex1125`). Current byte sizes were **not measured** today.

Someone could rerun `tenure_pass_a_decision_hero.py` from the two JSONL inputs without scraping again. Rebuilding the panel from raw HTML requires the parse, the OpenAlex match, and the works cache. The expensive pieces to keep are the saved HTML, the school URL list, `openalex_author_ids.jsonl`, and `openalex_works_by_year.jsonl` (or the Rivanna snapshot cache).

### A12. Figures

| Figure | Path | Axis |
|--------|------|------|
| Chapter placeholder, peer quality | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM.png` (slide and binned CSV beside it) | **B2** |
| Own performance, same cohort | `.../hero/HERO_tenure_q16_decision_own_career_infHM.png` | Own `pubs_per_career_year`, not B1–B4 |
| 8-bin and 10-bin versions of both | `HERO_tenure_q8_decision_dept_loo_infHM.png`, `q10_...`, and the matching `own_career` files | Same axes, coarser bins |
| Performance-metric sensitivities | `.../tenure_sandbox/perf_story/panels/HERO_tenure_perf_q16_loo_career_rate_slide.png` and the cum-pubs and annual-pubs siblings | Leave-one-out on career rate, cumulative works, or papers that year. Not the locked 16-bin chapter file. |
| Exploratory assistant-pool and last-year plots | `HERO_tenure_q16_infHM_resolved_v0.png`, `HERO_tenure_q16_lastps_loo_cum_infHM.png`, and the other `*_loo_infHM*` / `*_poolq_*` files in that folder | Older pools. Do not use as the chapter peer-quality figure. |

No tenure Band of Excellence figure (advancement within a band of own performance) was found. `TENURE_hero_pipeline.md` still lists that as a later act. A coverage-by-year figure for the chapter was **not** identified in this pass. The gap chart `tenure/tenure_pipeline/url_gap_priority_plot.png` is an operations plot of saved snapshots, not a sample-flow figure for the 389.

---

## Part C — Tenure

### C1. Which departments

Carnegie R1 computer-science departments, grown from a nine-school pilot. The overview’s Cell 2 table is the search story: scrapability first, then waves on 4 April 2026 and 5 April 2026, then later additions to **168** entries in `r1_schools_data.py`. **verified** — `TENURE_PIPELINE_OVERVIEW.md`.

The figure’s provenance does not record how many of the 168 contribute one of the 389 decisions, or the calendar-year span of those decisions. Assistant-time (1 through 9) is recorded. Calendar coverage of the underlying panel is 2000–2024. **verified** — `panel_rebuild_meta.json`.

### C2. Finding faculty pages

Addresses start in the school list. The Internet Archive capture index is queried for each address. Saved HTML is downloaded and parsed. Weak addresses are replaced by hand through `url_update_worksheet.csv` after someone, or an agent, opens a saved page and follows the faculty link. **verified** — `TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` and Cell 3A in the overview.

A single “share of departments with usable coverage” was **not recorded**. The panel build recorded 1,957 department-years with any parsed row. A missing next year does not delete the person. If the department has no page for the year after the last assistant year, the outcome is censored, and this figure then drops censored people. **verified** — `derive_dept_episode_outcome` when `dept_has_next` is false.

### C3. Reading rank from pages

Names and ranks are regular expressions and a rank list in `html_parser.py` (`RANK_RE`, `_norm_rank`) and `panel_builder.py` (`_RANK_PRIORITY`). There is no language-model step in that parse. If several ranks appear, the panel keeps the one with the best priority (`_best_rank`).

Human review in the written workflow is for faculty-page addresses and for OpenAlex rows tagged MULTI or low confidence. A hand audit of rank accuracy, and an error rate, were **never checked**. None is written down in the files read today.

### C4. Publication records

OpenAlex. Works are counts by year for a resolved author id (`openalex_works_by_year.jsonl`), from the API or from the Rivanna snapshot. The career file sums those counts.

The focal sample requires HIGH or MEDIUM name-and-institution match. The career file used on 2 September 2026 contains HIGH only, so a MEDIUM match can be a decision row with no publication rate. Common names and name changes are the failure modes the tiers describe. A measured rate of wrong author ids was **not recorded** in the files read today.

### C5. The tenure decision

The decision year is the last year with rank `assistant` at that department. Tenure is an associate, full, endowed, or distinguished rank at that same department on or after the first assistant year. The peer mean is taken in the last assistant year, which can be the year before the promoted title appears.

Out, inside the figure, is attrition: absent on a department page that exists the next year, or present the next year in a title that is not a promotion (lecturer, teaching, research, and the other non-promoted labels). That second path is `off_tenure_track` and is still attrition.

A move to another school as an assistant, detected by the same name key at a new department, is `transferred`, `exclude_from_metrics` true, and is not in the 391. **verified** — `_find_transfer` and `load_panel_by_person`.

### C6. Performance measure

`pubs_per_career_year` = cumulative counted works ÷ (calendar year − year of first counted work), for age ≥ 1. The first publication year has a null rate. A year with zero new works, after the first, stays in the series and contributes 0 to the cumulative total.

Which works: whatever OpenAlex returned for that author id, with publication years outside 1950–2030 dropped, and duplicate year rows reduced by taking the max rather than summing. **verified** — `build_author_year_career_master.py`.

The change after Alex’s objection is the switch from papers in the decision year (`pubs_year`) to this career rate. The cited figure then uses other people’s career rates on the horizontal axis, not the focal person’s rate.

### C7. Group

The roster is every faculty id on a panel row for that department and year. The parser’s rank list includes emeritus, lecturers, teaching and research professors, adjuncts, visitors, postdocs, and `unknown`. Those people are in the roster if they were parsed. They enter the leave-one-out mean only when they have a career rate. Joint appointments are not a separate flag in the decision-hero code. **never checked** as a distinct class.

Department size for the 389 is stored on each row (`pool_size_dept`, `pool_size_rate_loo`) but was **not recorded** as a summary in the provenance. The run recorded 0 empty rosters and 2 people with no peer rate. How many departments are too small for a stable mean was **not recorded**.

### C8. Unresolved cases

Panel build: **1,225** censored, **17** transferred, among ever-assistant episodes, not limited to HIGH/MEDIUM. **verified** — `panel_rebuild_meta.json`.

Figure: censored and transferred people are not in the 389. `n_censored` on the figure is 0. Excluding them is what this run does. It changes the denominator relative to “all assistants still unresolved.” How many HIGH/MEDIUM censored people would be added if they were kept was **not recorded**. Including them would require a rule for the outcome (still unknown is not the same as “not tenured”). The v0 notes discuss that choice; this figure does not implement it.

### C9. Limited places

State it as an assumption. The data do not contain a quota, and the scripts do not turn department size into a number of slots. Calling it a department-size constraint would invent a rule the figure does not use.

### C10. Closed system

Senior and lateral hires who never appear as assistant are not decision rows. They can still be peers in the decision-year roster. A count of such hires in the 389 departments-years was **not recorded**. The panel has 29,274 faculty ids and 2,331 ever-assistant ids, so most parsed people are not focal cases. That is not the same as a count of lateral hires. **verified** for the two counts — `panel_rebuild_meta.json`. The interpretation as senior hires was **not** checked person by person.

Transfers of assistants are the recorded mid-career entries: 17 episodes, excluded from the figure.

### C11. What this system cannot give us

Beyond incomplete archives and no published quota:

- The cited figure is not an up-or-out decision at year 5 or 6. Most resolved spells end earlier in assistant-time, and the code does not explain which of those are real exits.
- Publication data for this build are HIGH OpenAlex matches only. MEDIUM names can be in the cohort with no rate, and unmatched or LOW names do not contribute a rate to the peer mean.
- Rank and name come from HTML rules. No measured rank-error rate is on file.
- “Out” mixes leaving the department with a title change to a non-tenure-track job.
- The same person at two schools is removed rather than followed.
- There is no system-wide list of openings, so global selection and limited places are assumptions.
- There is no Band of Excellence tenure figure yet, so the chapter cannot yet show the peer gradient inside a band of own performance.
- No B1, B3, or B4 tenure figure exists for this cohort.

---

## Open items

- Whether the chapter’s tenure result should stay on all 389 resolved exits, or be cut to assistant-years 5–6 (63 people). The code and the executive summary currently disagree. Alex has to choose. The figure that exists is the 389.
- Whether censored assistants belong in the denominator. This figure says no. A different choice needs a new run, which was not done here.
- Whether MEDIUM OpenAlex matches should get works before the chapter freezes the performance measure. The 2 September career file does not have them.
- A rank-accuracy check, an OpenAlex wrong-match rate, and a statement on human-subjects review and Internet Archive terms. Not in the files read today.
- How many of the 168 departments, and which calendar years, actually supply the 389. Not in the provenance.

## Conflicts

- The executive summary says the decision is usually in year 5 or 6. The provenance histogram says 16% are.
- `TENURE_hero_pipeline.md` PD29 table says “one row per tenure decision, around year 5–6,” and its Step 1–4 still describe the older assistant-only plot with censored people inside the bins. `decision_year_cohort.py` includes every resolved assistant-time and drops censored people before binning.
- The cohort filter allows MEDIUM matches. `author_year_career_master_meta.json` says this career file is HIGH only, and that MEDIUM has no works until the Rivanna cache is extended.
- Provenance `prep.n_attrition` is 200 at the cohort and `stage9_summary.n_attrition` is 198 after two people lose a null peer mean. The stage-9 tenure count stays 191. Those two files agree if both dropped people were attrition. The person file was not opened to confirm that.
- `stage9_analysis.py`’s own docstring still describes an assistant-year leave-one-out load. For this figure the script passes a prebuilt person list, so that load path does not run.

## For other chapters

- Sorting of faculty into departments (homophily, assignment, a sorting index) is not in this figure. PD29 left “homophily on all faculty versus assistants only” open. That belongs in the assignment chapter.
- The score, a congestion term, and selection of the top group are the model chapter. This response does not estimate them. B4 roster pressure is not implemented for tenure.
- Time-to-tenure, censoring as a survival outcome, and the Cox model named in `TENURE_DATA_GAMEPLAN.md` belong in the timing chapter. This figure converts censoring into “drop from the sample.”
- A zero or negative sorting parameter, or a comparison of tenure’s shape to the Army or basketball curves, is a result-chapter sentence. It is not a data definition.
