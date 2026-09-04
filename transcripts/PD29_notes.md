# Paper Directions 29 — my read (Sep 2, 2026)

**Source:** `transcripts/20260902_Paper_Directions_29_otter_ai_transcript.docx` (~24:51)  
**Context:** Charles walked Alex through **dirty tenure porch** (BDP + early HERO framing) same day as this call.  
**Prior:** [`PD28_notes.md`](PD28_notes.md) · tenure porch: [`../3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/`](../3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/)

---

## Headline

Two parallel mandates:

1. **Tenure** — Alex likes assortment on the porch; gives **new locks** on decision-year cohort, cumulative career pubs rate, and **pond** (department) construction.
2. **Paper by end of semester** — **50/50** next week: data progress + **paper-talk outline** (claims + figures + gap slides). Not another month in data-only mode.

> **Alex (tenure):** “Cumulative is correct… only look at those people in the fifth or sixth year… up or out — exactly like the army.”  
> **Alex (paper):** “Organize the **paper talk** — big question, figure, one-to-two sentence conclusion.”

---

## Transcript arc

| Block | Time | Content |
|-------|------|---------|
| **Porch review** | 00:04–03:30 | Overlap → high assortment ✓; censored = scrape gap; ALL-PS BDPs; promoted-with-zero annual pubs → need **cumulative** |
| **Tenure locks** | 03:45–12:43 | Yr ~6 decision; cum pubs ÷ career length; first-pub start; pond = whole dept at decision year; master author×year table |
| **Framing** | 05:21–06:44 | Alex adopts **“pond”** (big fish / small pond) vs “team” |
| **New domains** | 14:21–16:39 | **League of Legends** table sent; NCAA FB→NFL in progress |
| **Paper / time** | 16:39–23:54 | End-of-semester target; F-HERO still on Charles’s MBB list; **paper talk outline** deliverable ~1 week; **50/50** split |

---

## Alex ask — tenure (PD29 locks)

| # | Lock | Detail |
|---|------|--------|
| **T1** | **Decision cohort** | Typical tenure ~**year 6** (allow slight early/late). **Up-or-out** in that year — army-like. |
| **T2** | **HERO rows** | Only assistant-years with **decision signal** (tenured or out), not every assistant-year. |
| **T3** | **Own performance Â** | **ALL-PS · mean · own pubs at decision year** = cum pubs ÷ (focus_year − first_pub_year). Field: `pubs_per_career_year` in career master. **Not** LAST-PS cum (that's a stock slice, not Alex's rate). Career start = **first publication year** (OpenAlex). |
| **T4** | **Pond peer context** | **All faculty in department** in the **decision year** (for LOO / homophily). Not “cohort that arrived with me.” Not every dept×year in history — only years where someone has a decision. |
| **T5** | **Data spine** | Master table: every OpenAlex ID ever scraped × **pubs in each calendar year** → precompute running cum / rates; slice for analysis. |
| **T6** | **Homophily (open)** | May use **all faculty** in dept for assortativity — people join departments, not arrival cohorts. |

**Porch reaction (same call):** Interval overlap H_sort reads **high**; censored mass understood (should shrink as scrape fills); dirty data OK for exploratory pass.

---

## Alex ask — paper & time (next ~1 week)

| # | Deliverable | Shape |
|---|-------------|--------|
| **P1** | **Paper talk outline** | PowerPoint logic: **question → figure → 1–2 sentence claim** per slide; not generic IMRaD |
| **P2** | **Gap slides** | Blank / placeholder slides for open questions the narrative still needs |
| **P3** | **Data status** | Where scrape sits; tenure rebuild plan vs current v0 |
| **P4** | **Time budget** | **50/50** data vs outline (Charles picks days or half-days) |
| **P5** | **MBB F-HERO** | Still Charles’s cross-domain “same trend?” check — Alex wants **end-of-semester quality**, not minimal three-domain ship |

Intro / lit review explicitly **de-prioritized** vs narrative of claims.

---

## New domain — League of Legends (`legends`)

**PD29:** Alex sent esports table — dev league → pro promotion; team swapping; own + team performance columns.

**Repo layout (Charles, Sep 2):**

| Path | Role |
|------|------|
| `datasets/legends/lol_big_fish_player_split_panel.csv.zip` | Raw panel from Alex (PD29) |
| `legends/` (future) | Scripts / pipeline (mirror `tenure/`, `sports/`) |
| `3-Master_Plan/re_entry/HEROs_and_PASSes/legends_sandbox/` (future) | Porch + HERO outputs |

**Naming rule:** use **`legends`** (not `lol`, `esports`) for folders, sandboxes, and script prefixes when we add code — same pattern as `tenure`, `sports`, `talent`.

**Status:** Zip in place (~66k rows, 84 cols); unzip when scaffolding porch / HERO.

**Also incoming:** NCAA football → NFL (~300 draftees/yr; position-specific) — path TBD.

---

## Delta vs current tenure v0

See [`TENURE_hero_pipeline.md` § PD29 delta](../3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md#pd29-delta-sep-2-2026--alex-locks-vs-v0) and [`_DISPOSABLE_tenure_hero_thread.md`](../3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/_DISPOSABLE_tenure_hero_thread.md).

**COMPASS read:** Sep 2 porch + deck = **Act I exploratory** (Alex approved direction). **Act I-b** = implement PD29 spine before new HERO claims are paper-grade.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-02 | PD29 ingested; tenure locks + paper 50/50 + legends folder convention. |
