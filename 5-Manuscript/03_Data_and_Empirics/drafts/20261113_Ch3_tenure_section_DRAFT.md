# Chapter 3 — Academic tenure (section draft)

FOUNDY | 13 November 2026 | DRAFT for Charles

**Built from:** PEER's answers (`notes/20261113_PEER_Response_Ch3_tenure.md`) and a read of the saved run record, the binned table, and the figure. The pipeline was not rerun, and the tenure scripts were not re-opened line by line. Where a footnote says **PEER, verified**, that is PEER's tag from 13 November, with the file PEER named. Where it says **Verified**, the run record or the binned table was read again for this draft.

**Do not copy the words printed on the figure.** They disagree with the run record. See the flags.

Section numbers are placeholders. Open choices are written as such, not resolved.

---

## X.1 Why this system fits

An assistant professor's publication record is observed in a bibliographic database, independently of the tenure decision.[^fit-perf] The group is the department in the year of that decision. Hiring, not a random draw, puts people there. The outcome is whether the person is promoted in that department or leaves the tenure track there.

Two of the five criteria hold only as assumptions. Nothing in these data is a slate of openings filled from across universities, so "selection from the whole system" is a claim about the academic labor market, not a field of candidates we observe. No department publishes how many people it may tenure, so "a limited number of places" is an assumption, not a count.[^fit-assume] The system is also only partly closed. The people in the result are those who were assistant professors in a department we scraped. Senior hires never appear as those cases, but they can still sit in the department and enter the peer average. Assistants who move to another department are taken out of the result rather than followed.[^fit-closed]

## X.2 How the data were found

The target was a setting where an assistant professor's record is visible before the decision, and the rest of the department that year is visible too. Computer science at US research universities was chosen because faculty pages are public, the Internet Archive has saved many of them, and publication records can be joined to names. The list was aimed at Carnegie research-university computer-science departments. It began as nine schools whose pages could be scraped and grew in waves to 168.[^story-schools]

Department pages are not a single download. For each school the pipeline asks the Internet Archive for saved copies of a known address, downloads the HTML, and reads names and ranks with rules. When an address fails, a person opens a saved page, follows the link that actually lists the faculty, and pastes the new address into a worksheet. That is why coverage is uneven: a department can have a roster in one year and a menu page, or nothing, in another.[^story-loop]

OpenAlex is the publication source. DBLP was considered and kept as a cross-check, not as the record the figure uses.[^story-dblp]

The peer group was redesigned once. The first version used other assistant professors and the papers they published that year. On 2 September 2026 the lock changed to the whole department in the decision year, and to a career publication rate rather than that year's count. The reason was concrete: someone just promoted could show zero papers that year, which is the wrong record of a career.[^story-lock] The same note described the decision as around the fifth or sixth year as an assistant. The code counts that band and does not apply it. The figure includes every resolved exit.[^story-band]

## X.3 Sources and how they were linked

**Faculty pages.** Each raw object is one saved HTML page. Names and ranks are read from it by rules, not by a language model. A person is identified inside one department by the department plus a normalized name. The same person in another department gets a new identifier.[^src-pages] Terms of use for the Internet Archive were not checked.

**Publications.** OpenAlex supplies an author identifier and a count of works by year. The career file used here was built on 2 September 2026 from works last modified on 19 April 2026. It holds 3,630 authors, all of them high-confidence matches, and 99,733 author-year rows.[^src-oa] Cite OpenAlex as Priem, Piwowar, and Orr (2022). A formal terms review for the dissertation was not done.

Names on the pages are matched to OpenAlex authors by normalized name plus the university's OpenAlex institution, with a check that the years overlap. Matches are tiered: high (name, institution, and years), medium (name and institution, years unclear), low (name only), several plausible authors, or none. The decision sample keeps high and medium matches. The career file contains high matches only, so a medium match can be in the sample with no publication rate.[^src-match] How many matches a person has reviewed, and the rate of wrong authors, were not recorded.

## X.4 Cleaning and the final sample

The order below is the order of the script that wrote the cited figure. The peer average is computed after the cohort exists, on a roster that is wider than the cohort: every person parsed in that department that year, of any rank. People on the roster with no career rate are skipped. They are not entered as zero.[^flow-order]

| Step | What it does | Count after |
|---|---|---|
| Annual panel, all ranks, years 2000–2024 | The scraped rosters, one person per department per year | 2,560,018 rows; 29,274 people |
| Ever an assistant, with an outcome | Tenure, attrition, censored, or transferred | 2,331 people ever an assistant. Among episodes: 471 tenure, 618 attrition (140 of them off the tenure track), 1,225 censored, 17 transferred |
| High or medium author match only | Drops weak name matches from the focal sample | Not recorded |
| Drop transfers | A move to another department is not an outcome at the first one | 17 transfers at the panel level; the count inside the match tier was not recorded |
| One row per person, resolved outcomes only | Last year as an assistant. Censored people drop here. | 391 people: 191 later tenured, 200 attrition, of whom 47 are off the tenure track. 280 have their own career rate. 63 are in assistant-years 5–6. |
| Peer average | Leave-one-out department mean. Drop the person if it cannot be computed. | **389 people: 191 tenured, 198 attrition.** Two people dropped. No department roster was empty. |

The first two rows are all assistants, not only high and medium matches. The 389 is the analysis sample.[^flow-counts]

## X.5 The four concepts

| Concept | Definition | Variable |
|---|---|---|
| Performance | Cumulative works divided by years since the first counted publication | `pubs_per_career_year` |
| Group | Everyone parsed on the department page in the decision year | department and year |
| Peer quality | Mean career rate of the others who have a rate | `loo_mean` |
| Advancement | Promoted in the same department, versus gone or off the tenure track | tenure or attrition |

**Performance.** Cumulative OpenAlex works divided by the years since the first year with a counted work. The first publication year has no rate, because the age would be zero. A later year with no new works stays in the series, adds nothing to the cumulative count, and so lowers the rate. There is no winsorizing.[^c-perf] The cited figure does not put this number on the horizontal axis. A separate figure does, for the same people.

**Group.** The decision year is the last year the person is recorded as an assistant, which can be the year before a promoted title appears. The group is whoever was parsed that year, any rank, including emeritus, lecturers, visitors, postdocs, and unknown titles when the parser returned them. Joint appointments are not identified.[^c-group]

**Peer quality.** This is the leave-one-out mean of career rates, the measure labeled B2. The person is excluded. Roster members with no rate are excluded. It is not the department mean including the person, and it is not the person's own rate minus the peer mean. An older column averages papers published that year among assistant professors only. That column is not this figure.[^c-peer]

**Advancement.** Tenure is an associate, full, endowed, or distinguished rank in the same department. Attrition, which stays in the denominator as not tenured, is either absence from a department page that exists the next year, or a title that is not a promotion. A move to another school as an assistant is neither outcome: those 17 episodes are removed. A person still an assistant when the archive stops, or whose department has no page the next year, is censored and is also removed. The figure's count of censored people is zero because they were dropped, not because the panel had none.[^c-adv]

## X.6 What this system cannot give us

There is no published quota and no list of openings, so limited places and selection from the whole system are assumptions. Archives are incomplete, and the figure responds by dropping anyone whose next year cannot be seen: 1,225 censored episodes in the full panel, against 389 people in the figure. Most resolved spells end in assistant-years 1 through 4 (309 of 391), and the data do not say how many of those are real short careers rather than a bad rank parse or a one-year page. Publication rates exist for high-confidence author matches only. Rank and name come from rules applied to HTML, with no measured error rate. "Not tenured" mixes leaving the department with moving to a non-tenure-track title. A person who changes schools is removed rather than followed. No figure yet shows the peer gradient inside a band of the person's own publication rate.

## X.7 The descriptive result

**Placeholder figure:** `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM.png`

The figure splits 389 people into 16 groups of 24 or 25 by the leave-one-out career rate of the department, and plots the share tenured. Overall, 191 of 389 are tenured (49%). Across bins the share runs from 8% to 79%. Two bins reach 79% (bins 6 and 11). Bin 14, among the higher peer groups, is 8% (2 of 24). With about 25 people in a bin, a true rate of 49% has a sampling error near 10 percentage points, and the intervals drawn on the figure cover the overall rate in most bins.[^res-bins] The curve is jagged. It should not be described as a clean rise and fall, and it should not be described as flat.

The words along the bottom of the saved picture say the average is of co-hired assistants and that the person is included. The run record says the average is the whole department, career rate, person excluded. The picture can be a placeholder only with a corrected caption.[^res-caption]

---

## Flags for Charles

The printable list is `notes/20261113_Ch3_Charles_decisions_SCOUT_and_PEER.md`. The tenure items that this draft does not decide are: the figure caption (item 10), all 389 versus years 5–6 (item 11), whether to inspect the short spells (item 12), censored people (item 13), who sits in the peer roster (item 14), and medium author matches (item 15).

## Executive summary

The tenure paragraph was corrected where it was simply false: peer quality is the others' career rate, not papers in the decision year, and "the alternative is leaving" now mentions that moves to another school are excluded. The year 5–6 sentence is left as an explicit open choice, because Alex's note and the figure disagree. Open item 5 in the summary points at this draft.

---

[^fit-perf]: **PEER, verified.** `tenure/tenure_pipeline/build_author_year_career_master.py`.
[^fit-assume]: **PEER, recalled** for the labor-market claim. **PEER, verified** that no script reads a slot count.
[^fit-closed]: **PEER, verified.** `panel_builder.py`; 17 transfer episodes in `panel_rebuild_meta.json`.
[^story-schools]: **PEER, verified.** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md`; 168 entries in `r1_schools_data.py`.
[^story-loop]: **PEER, verified.** `TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` and the overview. **Recalled** that the worksheet loop was still active in October 2026.
[^story-dblp]: **PEER, verified.** `tenure/documents/TENURE_DATA_GAMEPLAN.md`.
[^story-lock]: **PEER, verified.** `TENURE_hero_pipeline.md`, PD29 table, 2 September 2026.
[^story-band]: **Verified.** Provenance `prep.n_in_reference_band` = 63 of 391 (16%), and `reference_asst_time_band` [5, 6] is recorded as a band, not as the sample.
[^src-pages]: **PEER, verified.** `html_parser.py`, `panel_builder.py`.
[^src-oa]: **PEER, verified.** `author_year_career_master_meta.json`.
[^src-match]: **PEER, verified.** `openalex_resolver.py`. A single match-rate table was not recorded.
[^flow-order]: **PEER, verified.** `tenure/scripts/tenure_pass_a_decision_hero.py` and `decision_hero_prep.py`. Not re-read for this draft.
[^flow-counts]: **Verified** for the 391, the histogram, the 389, 191 tenure, and 198 attrition: `HERO_tenure_q16_decision_dept_loo_infHM_provenance.json`. **PEER, verified** for the panel-level counts in `panel_rebuild_meta.json`. The two dropped people account for 200 − 198 attrition only if both were attrition cases; the person file was not opened.
[^c-perf]: **PEER, verified.** Formula in `build_author_year_career_master.py`. Provenance `z_score` false.
[^c-group]: **PEER, verified.** `build_dept_year_rosters`. Joint appointments **never checked**.
[^c-peer]: **Verified.** Provenance `spec.x_metric` = `decision_loo` and `spec.peer_pool` = whole department, career-rate leave-one-out. **PEER, verified** that B1, B3, and B4 are not computed for this figure.
[^c-adv]: **PEER, verified.** `_PROMOTED_RANKS` and `derive_dept_episode_outcome` in `panel_builder.py`. Provenance `n_censored` = 0 on the figure; 1,225 censored episodes in the panel build.
[^res-bins]: **Verified.** `HERO_tenure_q16_decision_dept_loo_infHM_binned.csv`. Bin 6 and bin 11 are each 19/24 = 79%. Bin 14 is 2/24 = 8%. Binomial standard error at p = 0.49 and n = 25 is about 0.10. Provenance `shape.peak_vent` = 5 names only the first of the two 79% bins.
[^res-caption]: **Verified** by reading the figure. The footer says "mean pubs/yr of all OA-matched co-hired assistants in same dept-year (includes self when matched)." That is not the provenance sentence.
