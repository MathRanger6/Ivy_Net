# FOUNDY → NVECTOR — Chapter 3 handoff

**From:** FOUNDY (thesis drafting)  
**To:** NVECTOR, taking the Chapter 3 drafting seat temporarily  
**Date:** 13 November 2026

## Preface — paste this to NVECTOR

NVECTOR,

FOUNDY is handing you Chapter 3 drafting for a while. Charles is stepping away from that agent for financial reasons. This file is the whole brief. Read it before you draft anything.

Chapter 3 is the data-and-empirics chapter. It describes four systems (Army, Romanian high-school admissions, college basketball and the NBA draft, academic tenure) and then the descriptive results. No model, no causal peer-effect language, no assignment or homophily, no survival analysis inside this chapter. Charles is writing each system on its own, then assembling, then rewriting the executive summary. Basketball and tenure are drafted. Romania is not started. The Army section is still a seed.

Two warnings:

1. The 9 November handoff, `5-Manuscript/03_Data_and_Empirics/notes/20261109_FOUNDY_Handoff_Chapter3_data_empirics.md` (and its PDF), is no longer the front door. Survival is now its own chapter, and the drafts live under `5-Manuscript/`. A banner on that old file points here. Use the old file only for Army background this one does not repeat.
2. Do not resolve Charles's decision list, do not rerun any pipeline, do not trust SCOUT's filter order, and do not paste the tenure figure caption. SCOUT says the basketball minute and game floors come after the peer measure; for the figure we cite, they come first, and the draft follows the code. The words printed on the tenure figure say co-hired assistants and include the person; the run record says the whole department, leave-one-out, person excluded. The tenure draft follows the run record.

Charles is working the decision list himself, one item at a time: `5-Manuscript/03_Data_and_Empirics/notes/20261113_Ch3_Charles_decisions_SCOUT_and_PEER.md`. When he has written a decision on an item, apply it to the matching section and say which item you applied. Do not fill in an item he has left blank.

If he asks what to do next, and he has not named something else: apply the decisions he has already written, then draft Romania (not started; start from `5-Manuscript/03_Data_and_Empirics/notes/LASZLO_ROMANIA_HANDOFF.md`), then the Army section from the existing Army answers, and only after the four sections exist assemble the chapter and rewrite the executive summary. Do not write "the same shape across all four systems." Basketball's full-sample peer figure is flat. Tenure's is jagged. The Army inverted U is still the March placeholder.

The rest of this file is the map: what changed since 9 November, where each product is, and what each drafted section actually says.

FOUNDY

---

The 9 November handoff (`20261109_FOUNDY_Handoff_Chapter3_data_empirics.md`, and its PDF) is **out of date** on two locks: survival is now its own chapter, and the manuscript files live under `5-Manuscript/`. Use this file as the front door. Use the 9 November file only for Army background that this one does not repeat.

Live campaign log: `3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md`. If Charles says **anchor**, paste the YOU ARE HERE table from that file. Some rows in that table still cite the old 9 November paths; the paths in this handoff are the ones that exist.

---

## What this chapter is

Chapter 3 is the data-and-empirics chapter (Alex, 4 November, PD52). Two halves, in this order:

1. **The systems.** What a system has to be like for the question to be measurable, then four systems: Army, Romanian high-school admissions, college basketball and the NBA draft, academic tenure. For each: where the records came from, how they were cleaned, and which variable is performance, group, peer quality, and advancement.
2. **The results.** How often people advance when grouped by peer quality. No model. No causal peer-effect language. Assignment and homophily are a later chapter. Survival and timing are a later chapter.

Charles is not ready to read the chapter as a whole. The plan he set on 13 November: write each system's section on its own, then assemble, then rewrite the executive summary. Basketball and tenure are drafted. Romania is not started. The Army section is still a seed that starts too far downstream.

Every system section uses the same seven parts: why it fits, how the data were found, sources and linking, cleaning (with a flow table), the four concepts, what the system cannot give us, the descriptive result.

---

## What changed since the 9 November handoff

- **11 November, Alex.** A competing-risks plot (top performers promoted early, then a lower final promotion rate, with attrition rising) is the reason to write a **survival chapter**. Chapter 3 keeps the endpoint bars and points forward. The 9 November "footnote only" lock is superseded. Outline already in the repo: `5-Manuscript/_archive/Chapter_5_Survival_Model_outline.md`.
- **11 November, Alex.** The LG assignment work is its own chapter. Do not pull it into Chapter 3. Notes live under `5-Manuscript/05_Assignment/notes/`. The canonical Word draft from the other agent has not been filed in `05_Assignment/drafts/` yet.
- **11 November.** Army 520 is running on Vantage. Charles is provisioning mosaic code there. COMPASS is tasked to specify HERO and Band of Excellence plots for three peer axes (B1, B2, B3) on one frozen 520 run, then B4 later. Spec: `3-Master_Plan/re_entry/PEER_INFLUENCE_AXES_MISMATCH.md` (handoff status at the top, 11 November). Chapter 3 does not wait on those plots. The March Army bars remain placeholders, and they plot own-minus-peer (B3), not peer quality alone (B2).
- **13 November.** SCOUT answered the basketball questionnaire. PEER answered the tenure questionnaire. FOUNDY drafted both sections and a printable decision list. Charles has that list and is working it one item at a time.

---

## Where the products are

All of these are under `5-Manuscript/03_Data_and_Empirics/` unless noted.

| What | Path |
|---|---|
| **Charles's decision list (start here if he asks what he still owes)** | `notes/20261113_Ch3_Charles_decisions_SCOUT_and_PEER.md` |
| Basketball section draft | `drafts/20261113_Ch3_basketball_section_DRAFT.md` |
| Tenure section draft | `drafts/20261113_Ch3_tenure_section_DRAFT.md` |
| Executive summary (v2, patched 13 November) | `drafts/20261109_Ch3_executive_summary_DRAFT.md` |
| Questionnaire SCOUT and PEER answered | `notes/20261113_Ch3_Questions_for_SCOUT_and_PEER.md` |
| SCOUT's answers | `notes/20261113_SCOUT_Response_Ch3_basketball.md` |
| Basketball file register | `notes/20261113_MBB_DATA_SOURCES_register.md` |
| PEER's answers | `notes/20261113_PEER_Response_Ch3_tenure.md` |
| Campaign log | `3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md` |
| Peer-axis labels (B1–B4) | `3-Master_Plan/re_entry/PEER_INFLUENCE_AXES_MISMATCH.md` |

Army, already done before this week:

| What | Path |
|---|---|
| Questions sent to CODA | `notes/20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md` |
| CODA's answers | `notes/20261109_CODA_Response_Ch3_raw_to_dataframes.md` |
| FOUNDY's Army Q&A (the prose seed) | `notes/20261109_FOUNDY_Response_Ch3_Army_data_questions.md` |
| Stale handoff (do not follow its locks) | `notes/20261109_FOUNDY_Handoff_Chapter3_data_empirics.md` |

Romania has a separate handoff and no Chapter 3 section yet: `notes/LASZLO_ROMANIA_HANDOFF.md`.

---

## What each drafted section actually says

**Basketball.** Seasons 2009–2021. Performance is points per minute, standardized within season. Peer quality on the cited figure is the leave-one-out teammate mean (B2). One row per player, the last season. Sample 22,795, of whom 615 were drafted. The full-sample peer figure is **flat** (draft rate 1.9% to 3.5%). Own scoring on the same people runs from 0% drafted to 16%. The 20-minute floor is the season total, and both floors are applied **before** the peer mean. SCOUT's answers A5 and B6 have that order backward; the draft follows the code (`sports/scripts/pass_a_empirical_bundle.py`, `y_draft_mode = ever`).

**Tenure.** Performance is cumulative works per year of career (OpenAlex), not papers in the decision year. The cited figure's axis is the leave-one-out mean of other faculty's career rates in the whole department (B2). Sample **389** resolved people (191 tenured). Years 5–6 are a counted band (63 of 391), not a filter. The curve is **jagged** (8% to 79% by bin, about 25 people per bin), not a clean inverted U. The words printed on the PNG contradict the run record: the caption says co-hired assistants and includes the person. Do not paste that caption.

**Executive summary.** The basketball and tenure paragraphs were patched on 13 November so they match those facts. The results sentence is still in brackets. Do not write "the same shape across all four systems." Basketball's full-sample peer figure is flat. Tenure's is jagged. The Army inverted U is still the March placeholder, on the B3 axis.

---

## What NVECTOR should not do

- Do not resolve the decision list. Charles is printing it and answering one item at a time. When he writes a decision on an item, apply it to the matching section and say which item you applied.
- Do not rerun basketball, tenure, or Army code to fill the "not recorded" counts. Those are marked TK on purpose.
- Do not treat SCOUT's filter order, or the tenure PNG caption, as the truth. The drafts already flag both.
- Do not move homophily, the score, selection, or survival into these sections. Both agents put that material in a "for other chapters" box.

## Sensible next work, if Charles asks for more drafting

1. Apply whatever decisions he has already written on the list.
2. Romania, from `notes/LASZLO_ROMANIA_HANDOFF.md`, in the same seven-part shape. It has not been started.
3. Army section prose from `notes/20261109_FOUNDY_Response_Ch3_Army_data_questions.md`, starting at the raw files rather than at `tb_ratio_fwd_snr`. Keep the March figures labeled as placeholders on the B3 axis, and point timing at the survival chapter.
4. Only after the four sections exist: assemble them and rewrite the executive summary, including the results sentence.
