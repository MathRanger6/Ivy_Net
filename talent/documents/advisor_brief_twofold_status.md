# Advisor briefing — twofold plan (coding + publication)

**For:** Alex Gates  
**Context:** Follow-up to **2026-03-13** conversation (`260313_Paper_directions_otter_ai.txt` in repo root).  
**Purpose:** One-page-style status on the **two parallel lines**: (A) **525 / pipeline coding** and (B) **publication plan** (mechanism, venues, external data) — **without** assuming he has read the repo.

---

## 1. What you asked for (from that conversation)

| Theme | Your guidance (paraphrase) |
|--------|-----------------------------|
| **Parallel tracks** | Keep **writing / mechanism / venues** and **coding** moving; “a little of both” beats all-or-nothing. |
| **UIC / pool consistency** | Who is **consistently** in a strong pool (e.g., by UIC ranking on mean top-block in pool)? Year-to-year stability vs noise? |
| **Senior raters** | Do certain **senior raters** consistently host strong pools? → “Talent on **people** vs **organizations**.” |
| **LT OERs (longitudinal)** | Richer path: same rater as **BN then BDE** commander over time (longitudinal senior-rater story). |
| **Mechanism** | **Articulate mechanism** underlying inverted-U; iterate with GPT; **reframe for different communities** (management science, OR/systems, business dynamics, etc.). |
| **Literature ↔ mechanism** | Two-stage loop: mechanism → literature → refine mechanism; **different bodies of literature** per community. |
| **Venues** | Likely **management-science / Contractor–type** visibility; not AER / core labor econ; interdisciplinary “big” journals need more results and/or more data. |
| **External replication** | Brainstorm **public** data where same pattern might appear; “magic number **three**” (Army + two) strengthens an interdisciplinary story; **articulation first**, then data search. |
| **Pragmatic floor** | Story can be built around **two figures** if needed; maximize what we have. |

---

## 2. Where we stand — **Line A: Coding / 525 / 520**

| Your goal | Status | Notes |
|-----------|--------|--------|
| **LT OERs integrated** | **Done** | LT OERs are merged into the **snapshot** data used in 520 (same merge logic as other OER rows by officer × date). |
| **Longitudinal senior-rater story (LT path)** | **Unblocked at data layer** | LT rows exist on snapshots for analyses that **keep** them; the **Cox / promotion interval** build in Cell 10 **drops** LT rows by design — so 525-style or dedicated analyses should use snapshot-level or alternate cohort logic where LTs remain. |
| **UIC × strong pools; consistency over time** | **Planned + specified** | **`525_plans.md`** lays out UIC aggregation (rated officer company → battalion/brigade), pool-strength definition (mean TB in pool), and senior-rater-first design; notebook still **planning / not yet executed** as primary deliverable. |
| **Senior rater × consistent strong pools** | **Planned** | Same doc; parameterized for senior rater now, rater role extensible later. |
| **Division / unit context for pools** | **In progress** | **`div_name`** (and division-aware plots) depends on **DIVISION_CONFIG** path + columns flowing through 08 → 09 → 10 → 11; currently **troubleshooting in 520** (nearly resolved). |
| **520 core result (inverted U, CIF, Cox)** | **Stable baseline** | Run profile **17_1** and pipeline outputs remain the empirical backbone; refinements are **structure** (divisions, UIC, rater consistency) not replacement of core finding. |

**One-line summary for you:** *Data integration ahead of the transcript (LT OERs on snapshots) is in place; 525 is fully planned on paper; execution is next once division/UIC plumbing in 520 is clean.*

---

## 3. Where we stand — **Line B: Publication plan (non-coding)**

| Your goal | Status | Notes |
|-----------|--------|--------|
| **Single publication roadmap** | **Done** | **`Publication_Plan.md`** — intro, way ahead, mechanism section, venues, external data, links to artifacts. |
| **Scholar GPT / replication landscape** | **Done** | **`replication_data_search.md`** — datasets, papers, repos, keywords (summarized inside Publication Plan §4.1). |
| **LLM brief for *datasets*** | **Done** | **`External_Data_Search_Brief.md`** (paste into GPT for “where is public data like this?”). |
| **LLM brief for *mechanism × venues*** | **Done** | **`venues_and_mechanism_articulation_llm_brief.md`** — project summary, community table (incl. **people analytics** as co-equal), copy-paste prompts, rollup table, **30-minute prompt workflow**. |
| **Draft mechanism paragraphs in the plan** | **Not yet** | **`Publication_Plan.md` §2** is still a placeholder; next step is to run the venue/mechanism brief in Scholar GPT and **paste short drafts** back into §2–§3. |
| **Pick primary community + citations** | **In progress** | Framing tools exist; **decision** waits on mechanism drafts + your feedback. |

**One-line summary for you:** *The publication track is **documented and tool-ready** (plans + LLM briefs + replication memo); the **substance** of mechanism wording and venue choice is the next hour-generation task, not the scaffolding.*

---

## 4. Crosswalk: your asks → artifacts

| Ask (transcript) | Artifact / location |
|------------------|---------------------|
| UIC / consistent strong pools | `525_plans.md` §2.1, §5–8 |
| Senior raters / people vs orgs | `525_plans.md` §2.2; `Publication_Plan.md` §1 item 3 |
| LT OER longitudinal | Snapshot merge in 520; `525_plans.md` §2.2, §8 (Cell 10 caveat) |
| Mechanism + multi-community framing | `venues_and_mechanism_articulation_llm_brief.md` |
| External data / “three settings” | `External_Data_Search_Brief.md`, `replication_data_search.md` |
| Integrated roadmap | `Publication_Plan.md`, `525_plans.md` |

---

## 5. Suggested **60-second** oral lead-in

> “Since we talked, I’ve kept both threads moving. On the **data side**, LT OERs are now on the snapshot stack, so we can do the longitudinal senior-rater story where we don’t rely on the Cox-only row set. I’m closing the loop on **division labels (`div_name`)** in 520 so pools and plots can be tied to org context. On **525**, the analysis plan is written end-to-end—UIC aggregation, senior rater consistency, longevity/path—we’re ready to implement once division plumbing is stable.  
> On the **paper side**, the publication plan is in one doc, we captured the Scholar GPT replication landscape, and I built two LLM briefs—one for finding public datasets, one for mechanism-by-venue articulation with a structured prompt workflow. What’s **not** done yet is parking final mechanism paragraphs into the plan; that’s the next writing block after one good Scholar GPT pass.”

---

## 6. Questions / decisions that would help from you

1. **525 priority:** Start with **UIC consistency** vs **senior-rater consistency** vs **division-level** summary first?  
2. **Longitudinal LT story:** Minimum viable output for a first meeting — **one figure** (e.g., rater fixed effects on pool mean TB over time) or **table** only?  
3. **Venue:** Still comfortable with **management science / Contractor genre** as the *default* primary, with **people analytics** as an explicit parallel candidate, or do you want to **rank** them after skimming the LLM rollup once?  
4. **External data:** Time horizon for a **second** public setting — thesis milestone only, or worth a **lightweight** replication attempt before defense?

---

## 7. File index (repo: `current_documents/` unless noted)

| File | Role |
|------|------|
| `advisor_brief_twofold_status.md` | **This briefing** |
| `525_plans.md` | 525 coding / analysis plan |
| `Publication_Plan.md` | Publication + way-ahead hub |
| `replication_data_search.md` | Scholar GPT replication memo |
| `External_Data_Search_Brief.md` | LLM brief for dataset discovery |
| `venues_and_mechanism_articulation_llm_brief.md` | LLM brief for mechanism × venues |
| `260313_Paper_directions_otter_ai.txt` | **Root** — original transcript |

---

*Prepared as a briefing aid; numbers and “done” refer to state as described by the student for this meeting.*
