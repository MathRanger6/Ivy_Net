# Chapter 3 — decisions for Charles

13 November 2026. Print this. Do one item, write the answer on the blank line, then the next.

Sources: SCOUT’s basketball answers, the basketball section draft (including the code check), and PEER’s tenure answers. Army items are not on this list.

---

## Basketball (SCOUT)

**1. What does the basketball result in Chapter 3 show?**

The full-sample figure is flat: draft rate 1.9% to 3.5% across 16 peer-quality bins, labeled “flat / not concave.” Own scoring, on the same people, goes from 0% drafted in the bottom five bins to 16% in the top bin. A separate figure holds own performance in a band and varies teammates; it uses a different sample.

Choose one: full-sample peer figure only; full-sample plus the own-scoring figure; or also the banded figure.

Decision: _______________________________________________

**2. Players still in college after 2021.**

The draft list stops at the 2021 draft. A player whose last season in the file is 2021, and who was drafted in 2022 or later, is counted as not drafted. The box scores on disk run through 2025, so the number can be counted without a new scrape.

Choose one: leave it as a stated limitation; count how many people it affects and add the count; or shorten the window so every career in the sample had time to be drafted.

Decision: _______________________________________________

**3. Where did the draft list come from?**

`datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv` is verified on disk (drafts 1989–2021). The download page and the date are not written down. One sentence is enough, if you remember it.

Answer: _______________________________________________

**4. When was the box-score file last built?**

`datasets/mbb/mbb_df_player_box.csv` covers 2003–2025. The command and the date of the last full download are not written down.

Answer: _______________________________________________

**5. Draft-to-player match rate.**

Nobody has tabulated how many draft records matched an ESPN player, how many a person reviewed by hand, or how many college draftees are still unmatched. The 615 drafted players in the figure are not that rate (there were 780 picks in 2009–2021, and the two numbers mix different things).

Choose one: ask SCOUT to count it from the files already on disk; or leave the match rate out of the chapter and say the link was name, school, and a hand-checked school list.

Decision: _______________________________________________

**6. How many rows are in the draft file?**

SCOUT writes both 1,921 and 1,922. One of them is a slip.

Choose: ask SCOUT to recount the file before the number goes into the chapter.

Done: _______________________________________________

**7. Games against non–Division I teams.**

Nothing in the panel build drops those games, so season points and minutes appear to include the whole schedule. SCOUT did not re-read that line and left it open.

Choose one: accept “full schedule, including non–Division I games”; or ask SCOUT to confirm the line in `panel_rebuild.py` and, if you want those games out, that is a new run.

Decision: _______________________________________________

**8. Ask SCOUT to correct two answers.**

SCOUT says the 20-minute and 10-game floors are applied after peer quality is computed. For the figure we cite, both floors are applied first. The 20 minutes are the season total, not per game.

This is a send-back, not a science choice. The drafted section already follows the code.

Done: _______________________________________________

**9. What may the dissertation print?**

Public box scores and a public draft list. No human-subjects review was checked. Full player-level tables should not be republished until the site terms are checked.

Choose one: you will check the terms; or the chapter cites the sources and publishes only binned rates.

Decision: _______________________________________________

---

## Tenure (PEER)

**10. The figure caption is wrong. Do not paste it into the chapter.**

The saved run record says the horizontal axis is the leave-one-out mean of career publication rates for the whole department in the decision year, self excluded. The words printed on `HERO_tenure_q16_decision_dept_loo_infHM.png` say something else: mean publication rate of co-hired assistants, and that the person is included.

The section draft follows the run record, not the picture’s caption.

Choose one: have PEER fix the caption and regenerate the picture; or use the picture with a corrected caption written by us.

Decision: _______________________________________________

**11. Who is in the tenure result: all 389, or years 5–6 only?**

Alex’s 2 September note says a decision around year 5 or 6. The code counts that band and does not apply it. Of 391 resolved people, 63 (16%) are in years 5–6. Years 1–4 are 309 people. The figure that exists is the 389 (391 minus 2 people with no peer rate).

This one needs Alex if you do not want to overrule the note.

Choose one: keep the 389 and say the year 5–6 band was not applied; cut the chapter figure to the 63 (new run); or show both.

Decision: _______________________________________________

**12. Early exits.**

A last assistant year of 1, 2, 3, or 4 can be a real short spell, a rank read wrong off the web page, or a department page that exists for only one year. Nobody has checked which of those dominates.

Choose one: disclose it as a limitation and keep going; or have PEER inspect a sample of the short spells before the section is final.

Decision: _______________________________________________

**13. People the archive does not follow (censored).**

The panel build recorded 1,225 censored assistant episodes. This figure drops them. The denominator is resolved cases only: tenured, or gone.

Choose one: keep them out, and say so; or put them in the denominator (new run, and “still unknown” is not the same as “not tenured”).

Decision: _______________________________________________

**14. Who counts as a peer.**

The roster is whoever was parsed on that department’s page that year: assistants, associates, full professors, and also emeritus, lecturers, visitors, postdocs, and unknown titles, if a career rate exists for them. People with no rate are skipped, not entered as zero. Joint appointments are not flagged.

Choose one: accept “whoever was on the page and has a rate”; or restrict peers (for example tenure-track faculty only). A restriction is a new run.

Decision: _______________________________________________

**15. MEDIUM name matches have no publication counts.**

The decision rows keep HIGH and MEDIUM name matches. The career-rate file used on 2 September has HIGH matches only. A MEDIUM person can be in the 391 with no publication rate. 280 of 391 have their own rate. Peers who are not HIGH do not enter the average.

Choose one: freeze the chapter on the HIGH-only career file and say so; or extend the career file to MEDIUM matches before freezing (Rivanna job, not done).

Decision: _______________________________________________

**16. “Limited places” for tenure.**

No department publishes a tenure quota, and the scripts do not turn department size into a number of slots. PEER’s recommendation: call limited places an assumption.

Confirm or replace: _______________________________________________

**17. Moves to another school.**

Seventeen assistant episodes are the same name appearing as an assistant in another department. They are removed. They are not counted as “denied tenure.”

Confirm that wording, or say otherwise: _______________________________________________

**18. What the tenure figure actually shows, so the results sentence does not overclaim.**

389 people, about 24 or 25 per bin. Tenure rate by bin runs from 8% to 79%. Most bins’ intervals cover the overall rate of 49%. Two bins sit near 79% (bins 6 and 11). Bin 14, a high-peer bin, is 8%. The curve is jagged. It is not a clean inverted U, and it is not flat the way basketball is.

No decision unless you want a coarser binning (8-bin and 10-bin pictures already exist) before this is shown to Alex.

Decision: _______________________________________________

**19. Checks that are missing, and can be stated as unknown.**

No measured rate of wrong ranks. No measured rate of the wrong OpenAlex author. No count of how many of the 168 departments, or which calendar years, supply the 389. Human-subjects review and Internet Archive terms were not checked. The figure itself prints no names.

Choose, for each, “state as unknown in the chapter” or “do the check before the chapter freezes”:

- Rank errors: ________
- Wrong author: ________
- Which departments and years: ________
- Human subjects and archive terms: ________

**20. Two small confirmations for PEER, not for you to compute.**

The cohort has 200 attrition cases and the figure has 198. The two dropped people had no peer rate. PEER did not open the person file to confirm both were attrition cases. Also, SCOUT-style: ask PEER to fix the figure caption (item 10) in the same pass.

Done: _______________________________________________

---

## After both sections exist

**21. The executive summary’s results sentence.**

It is still in brackets. Basketball’s full-sample peer figure is flat. Tenure’s peer figure is jagged, with wide intervals. The Army bars are the inverted-U case, and those bars are still the March placeholders. Do not write “the same shape in all four systems” until you have chosen which figure represents each system (items 1, 11, and 18) and the Army rerun exists.

No action today beyond not filling that sentence in.

---

## Already settled, so they are not on the list above

- Basketball performance is points per minute, standardized within season. Peer quality for the cited figure is the leave-one-out teammate mean. The unit is the player’s last season, 2009–2021. Sample: 22,795 players, 615 drafted.
- Tenure performance is publications per year of career, not papers in the decision year. The cited axis is other faculty’s career rates, not the person’s own rate. Transfers are excluded. Censored people are out of this figure. No quota is published.
- Neither section gets a model, a causal peer claim, or the homophily material. Those stay in later chapters.
