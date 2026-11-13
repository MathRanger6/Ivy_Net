# Questions for SCOUT (basketball) and PEER (tenure): what Chapter 3 needs from your data

Charles | 13 November 2026 | DRAFT for Charles to approve before sending (SCOUT response draft started 13 Nov; PEER pending)

**SCOUT:** answer Part A and Part B. **PEER:** answer Part A and Part C. Part D says how to return your answers.

---

## Why you are getting this

Chapter 3 of the dissertation is the data-and-empirics chapter. It describes four systems in which the dissertation's question can be measured: the Army, Romanian high-school admissions, college basketball and the NBA draft, and academic tenure. You built the basketball and tenure data, so you know the parts of the story that the code does not show: what was searched for, what was tried and dropped, why each filter exists, and what is still weak.

Alex Gates (advisor) said the data description is the science of this chapter. In a journal article it would become the supplementary data section. So the chapter has to tell a reader where the records came from, how they were found, how they were cleaned and linked, and which variable stands for which concept.

We are writing each system's section on its own first, then assembling the chapter and rewriting the executive summary. Your answers are the raw material for your system's section.

**Please answer from the existing code, documents, provenance files and saved runs. No new analysis, scraping or reruns are requested.** Where the honest answer is "I don't remember," "never checked," or "the docs and the code disagree," say so. A gap we know about is useful. A confident guess is not.

### What the chapter is and is not

- **Is:** a description of the system, the data, and the descriptive result (how often people advance, binned by peer quality).
- **Is not:** the model (Chapter 4), how groups form or homophily (the assignment chapter), timing or survival analysis (a separate chapter), or any causal claim about peer effects. If something you know belongs in one of those, put it in the "for other chapters" box at the end of your answers and keep it out of the main answers.

### Every system's section will have this outline

1. Why this system fits the selection criteria
2. How the data were found (the search story)
3. Sources and how they were linked
4. Cleaning and the final sample (a flow table)
5. The four concepts: performance, group, peer quality, advancement
6. What this system cannot give us
7. The descriptive result (placeholder figure)

The questions below are organized to fill that outline.

---

## Part A — Questions for both agents

### A1. Why this system fits the five criteria

Alex's criteria for a usable system:

1. A person's performance is observed and recorded, not inferred from the advancement it earned.
2. People sit in groups, and the groups are not a random draw.
3. Selection is global: the opportunities are filled from across the whole system, not separately inside each group.
4. The number of opportunities is limited, so the bar moves with the number of places.
5. The system is mostly closed: few people enter partway through.

For your system, say in a sentence or two how it meets each one, and **where it meets it only partly**. Be specific about the weak ones. The chapter will say plainly what each system cannot give us.

### A2. The search story

Tell the story of how the data were found, in order. This is the part only you can supply.

- What were we looking for at the start, and why this domain?
- Which sources were considered or tried and then dropped? Why (coverage, cost, terms of use, identifiers, quality)?
- What dead ends cost real time, and what did they teach us? One sentence each is enough.
- When did the current design settle, and what decided it? If Alex or Charles made a call that changed the data (for example a change of unit, window, or performance measure), give the date and the source document or transcript if you know it.

Please write this part as a short narrative (about one page), not a list of files. A reader should understand why the final data look the way they do.

### A3. Raw sources

For each source that feeds the final panel:

- What it is and who publishes it.
- What one raw row represents (a player in a game, a player-season, a faculty member on a department page, a paper).
- The identifier that marks a person, and whether it is stable.
- The years it covers, and the years actually used.
- How it was obtained (download, API, scrape, archive), and roughly when.
- Terms of use, licensing, or citation requirements, if any.

### A4. Linking records

Where two sources had to be joined (for example box scores to draft lists, or faculty pages to publication records):

- What was matched on, and how (exact, fuzzy, manual review, a crosswalk file).
- The match rate, if it was ever measured, and what happened to records that did not match.
- How many matches a human checked, and what kinds of errors are known to remain.
- Which crosswalk or alias files are hand-curated and should be described as such.

### A5. Cleaning and the final sample: the flow table

The chapter needs one flow table: raw records, then the count kept after each filter, then the final analysis sample. For each filter, in the order applied:

- what it does,
- why it exists,
- the count after it, if a saved run recorded one (point to the file), or "not recorded."

Also say which filters are applied **before** the peer-quality measure is computed and which are applied **after**. This matters: the peer measure should be computed on the full eligible group, then the focal sample restricted.

### A6. The four concepts

For each concept, give the plain-language definition, the formula if there is one, and the column name in the run of record:

- **Performance:** what is measured, over what period, on what scale, and any standardization or winsorizing.
- **Group:** what defines membership, and at what point in time.
- **Peer quality:** how it is computed from the group. Use the labels in `3-Master_Plan/re_entry/PEER_INFLUENCE_AXES_MISMATCH.md`:
  - **B1** full-group mean, including the person;
  - **B2** leave-one-out mean of the others;
  - **B3** own performance minus the leave-one-out mean;
  - **B4** roster pressure (average of sigmoid-transformed competitive relevance).

  Say which of these exist in your code, which one the canonical figure uses, and how groups of one (no peers) are handled.
- **Advancement:** the event, when it is measured, what counts as "not advanced," and how unresolved cases (still in the pipeline, left the data, transferred) are coded and whether they stay in the denominator.

### A7. Run of record

Which script, configuration, and saved output produced the figure you would put in the chapter? Give the provenance file path, the sample size, the number who advanced, the binning, and the filters. If there are several candidate runs, say which one you would cite and why.

### A8. What is authoritative and what is superseded

Which scripts, notebooks and documents are the pipeline of record, and which are earlier versions to ignore? If two versions of a document disagree, which is right?

### A9. Known quirks a careful reader should be told

Anything surprising that is not written down: coverage gaps, changes in how a source recorded something over time, years with thin data, identifiers that change, people counted twice, known biases in who appears in the data.

### A10. What can be said in print

Any restriction on what the dissertation may publish: terms of use of the sources, whether individuals can be named, whether a figure could identify a person, whether a human-subjects review applies. If you do not know, say so and we will ask.

### A11. Reproducibility

Where the data and code live now (Mac, Rivanna, archive), roughly how large they are, and whether someone could rebuild the final panel from the raw sources with what exists today. Name the durable inputs that would be expensive to re-create.

### A12. Figures

List the existing figures that could serve as placeholders in your section: the descriptive result binned by peer quality, the result within bands of own performance (the Band of Excellence views), and any data figures (coverage by year, sample flow). Give paths and say what axis each uses (B1, B2, B3 or B4).

---

## Part B — Additional questions for SCOUT (college basketball and the NBA draft)

What the repo already says (please confirm or correct):

- The canonical figure is `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.png`, with provenance in `HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json`: seasons 2009–2021; **horizontal axis = B2** (`poolq_loo`, leave-one-out teammate mean of **z-scored** points per minute, self excluded; LOO clipped at 1%/99% when winsor is on); 16 quantile bins on that axis; **min20** = player-season minutes ≥ 20; **mg10** = drop team-seasons with ≤ 10 **distinct** scheduled games (`min_team_season_games` in `sports_pipeline/config.py`); **panel: last-ps** (one row per athlete at final college season); **Y = ever-draft** on that row; **n = 22,795** player-seasons, **615** drafted; run script `sports/scripts/pass_a_empirical_bundle.py` (locked window 2009–2021).
- Box scores come from ESPN through sportsdataverse. Draft picks come from `nbaplayersdraft.csv`. Sports-Reference advanced statistics were scraped and matched onto the same rows.

Questions:

- **B1. Draft list.** Where did `nbaplayersdraft.csv` come from, and what years does it cover? Are both rounds included? How were draftees with no college (international, high school, G League) handled? What share of all draft picks in 2009–2021 are in the analysis?
- **B2. Box scores.** Which divisions and seasons were pulled? Are games against non–Division I opponents included in a player's season totals?
- **B3. Draft matching.** How were draft names matched to ESPN players (name, school, alias file)? Match rate? How many unmatched draftees remain, and who are they?
- **B4. Sports-Reference.** What role does it play in the chapter's run? If the canonical figure uses only ESPN points per minute, say so, and say what Sports-Reference adds (box plus-minus, as a sensitivity measure) and whether it belongs in the chapter at all.
- **B5. Performance measure.** Why points per minute? What did Alex say about it? What alternatives exist in the code (minutes, box plus-minus, offensive and defensive box plus-minus), and were they compared?
- **B6. Minutes and games thresholds.** What do "min20" and "mg10" mean exactly, and why those values? Are they applied before or after the teammate mean is computed?
- **B7. Final season only.** Why one row per player (the final season) instead of every season? How is "ever drafted" attached to that row?
- **B8. Group.** The team-season is the group. How are players who transferred or appeared for two teams in one season handled?
- **B9. Limited places.** The draft has 60 picks a year, but not all go to college players from these data. How should the chapter state the number of places this system actually fills?
- **B10. Who enters late.** Players who leave early (one season and out), redshirts, and players drafted after their final college season: how does each show up in the data?
- **B11. What this system cannot give us.** Beyond "points per minute is one box-score statistic," what else is weak?

---

## Part C — Additional questions for PEER (academic tenure)

What the repo already says (please confirm or correct):

- Faculty rosters come from archived (Wayback Machine) faculty pages of US computer science departments, discovered and scraped in stages, then adjudicated.
- Alex's lock on 2 September 2026 (PD29): one row per tenure decision, around year 5–6 as an assistant professor; performance = publications per career year at the decision year (`pubs_per_career_year`); group = the whole department in the decision year, all ranks; outcome = up or out in the decision year.
- The documented figure is described by `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json`: department leave-one-out mean (B2), resolved outcomes only, censored and transferred cases excluded.

Questions:

- **C1. Which departments.** How was the list of departments chosen (a ranking, a classification such as research universities, a convenience list)? How many departments, and what years?
- **C2. Finding faculty pages.** How were archived faculty-page addresses found? What share of departments had usable archive coverage, and for which years? What does a missing year do to the panel?
- **C3. Reading rank from pages.** How were names and ranks (assistant, associate, full, other) extracted: rules, a language model, human adjudication? What was checked by hand, and what error rate is known?
- **C4. Publication records.** Which publication database was used, and how were faculty names matched to author records (disambiguation)? Known failure modes, such as common names or name changes?
- **C5. The tenure decision.** How is the decision year identified? What counts as tenured (assistant to associate at the same school) and what counts as out (disappears, moves to another school, leaves academia)? How are moves to another school as an assistant handled?
- **C6. Performance measure.** Define `pubs_per_career_year` exactly: which publications count, the start of the career clock, and how zero-publication years are treated. Alex flagged that a zero annual rate for promoted people was the wrong metric; say what changed because of that.
- **C7. Group.** The whole department in the decision year. Does it include emeriti, lecturers, teaching faculty, joint appointments? How large are departments, and how many have too few faculty for a leave-one-out mean?
- **C8. Unresolved cases.** How many decision events are censored (archive ends before the decision) or transferred, and is excluding them from the figure what the chapter should report? Would including them change the denominator?
- **C9. Limited places.** No school publishes a tenure quota. How should the chapter state the "limited places" criterion here: as an assumption, as a department-size constraint, or something else?
- **C10. Closed system.** Senior hires and lateral moves bring faculty in partway. How common are they in the data, and how are they treated?
- **C11. What this system cannot give us.** Beyond incomplete archives and no published quota, what else is weak?

---

## Part D — How to return your answers

- **SCOUT:** write `5-Manuscript/03_Data_and_Empirics/notes/20261113_SCOUT_Response_Ch3_basketball.md`.
- **PEER:** write `5-Manuscript/03_Data_and_Empirics/notes/20261113_PEER_Response_Ch3_tenure.md`.

In that file:

1. Answer the questions in order, using the same numbers (A1–A12, then B1–B11 or C1–C11).
2. For each factual claim, mark it **verified** (you checked the code, data or provenance file today; give the path) or **recalled** (from memory or an older document). Do not mix the two without saying which is which.
3. Put the search-story narrative (A2) in plain prose, about one page.
4. Put the flow table (A5) as a markdown table.
5. End with three short boxes:
   - **Open items:** what only Charles or Alex can decide.
   - **Conflicts:** places where documents, code and saved outputs disagree.
   - **For other chapters:** anything about homophily, assignment, the model, or timing that came up but does not belong in Chapter 3.

Write for a reader who did not build the pipeline. Spell out terms the first time (for example, "leave-one-out (LOO) peer mean"). Do not edit the manuscript, notebooks or pipelines in answering.

### Files for reference

- `3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md` (what Chapter 3 has established so far)
- `5-Manuscript/03_Data_and_Empirics/drafts/20261109_Ch3_executive_summary_DRAFT.md` (the current one-paragraph summary of each system; correct anything wrong in it)
- `3-Master_Plan/re_entry/PEER_INFLUENCE_AXES_MISMATCH.md` (the B1–B4 peer-quality labels)
- `5-Manuscript/03_Data_and_Empirics/notes/20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md` (the same request we sent for the Army, for comparison)
- **SCOUT:** `sports/documents/SPORTS_DATA_GAMEPLAN.md`, `3-Master_Plan/re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md`, `datasets/mbb/DO_NOT_ERASE/README.txt`, **`5-Manuscript/03_Data_and_Empirics/notes/20261113_MBB_DATA_SOURCES_register.md`** (file-level sources)
- **PEER:** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md`, `tenure/documents/TENURE_DATA_GAMEPLAN.md`, `tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`, `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md`
