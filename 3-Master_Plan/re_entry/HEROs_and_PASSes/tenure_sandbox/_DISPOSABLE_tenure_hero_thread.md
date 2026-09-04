# DISPOSABLE — Tenure hero thread (2026-09-01)

**Purpose:** YOU ARE HERE for Charles + COMPASS tenure HERO work on Mac.  
**Campaign plan:** [`TENURE_HERO_Campaign_Plan.md`](TENURE_HERO_Campaign_Plan.md)  
**PD29:** [`../../../../transcripts/PD29_notes.md`](../../../../transcripts/PD29_notes.md)  
**Say `anchor`** in chat to paste the table below.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | PEER handoff + Mac rsync verified | ✓ |
| **1** | Campaign plan + folder scaffold | ✓ |
| **2** | Run `tenure_pass_a_hero.py` → HERO + BDP porch | ✓ (2026-09-01–02) |
| **3** | Alex porch review (Sep 2) | ✓ — assortment high; censored understood; metric forks flagged |
| **4** | **PD29 delta** → career master + rebuild plan | panel ✓ cohort ✓ BDP ✓ **HERO ✓** (389 dept LOO · 280 own career) |
| **4b** | **Reigning tenure HERO lock** | **Q16 · cum mean pubs/year · dept pond LOO @ decision year** (Sep 2 night) — other BDP may still be v0 metric until regen |
| **4c** | **3×3 data story (Alex screening)** | Full grid ✓ incl. Act II probes 7–8 · `TENURE_DATA_STORY_plot_highlights.md` |
| **5** | Paper talk outline (50/50 w/ data; ~1 week) | **Parallel (PD29 P1–P4)** |
| **6** | Act III ρ diagnostic | Pending (after PD29 spine?) |
| **7** | PEER scrape bolster | Parked |

**Alex one-liner (Sep 2):** Porch direction **good**; next tenure build = **decision-year cohort + cum pubs/career length + dept pond at decision year** — not more bin variants on v0 alone.

---

## PD29 delta vs v0 (short)

Full table: [`TENURE_hero_pipeline.md` § PD29 delta](TENURE_hero_pipeline.md#pd29-delta-sep-2-2026--alex-locks-vs-v0).

| v0 now | PD29 target |
|--------|-------------|
| ASST-PS mean peer LOO; LAST-PS cum on some HERO | **Decision year ~5–6** rows only (up-or-out) |
| ASST-PS mean pubs/year (exploratory) | **ALL-PS · mean · own pubs at decision year** (`pubs_per_career_year`) |
| Uni×year **assistant** pools | **Whole dept** in decision year |
| `faculty_panel_with_pools.jsonl` | **Master author×year pubs** → running cum |

**Sep 2 porch:** overlap H_sort ✓; promoted-with-zero annual pubs = wrong lens → supports cumulative lock.

---

## Print stack

### Focus — **3 docs, PD29 right now** (`print_tenure focus` or bare `print_tenure`)

| # | Document | Path |
|---|----------|------|
| **1** | **YOU ARE HERE** | `…/tenure_sandbox/_DISPOSABLE_tenure_hero_thread.md` |
| **2** | **PD29 Alex locks** | `transcripts/PD29_notes.md` |
| **3** | Pipeline + grain naming + PD29 delta | `…/tenure_sandbox/TENURE_hero_pipeline.md` |

### Core — full campaign binder (`print_tenure core`, 7 docs)

Adds campaign plan, career-master handoff, Mac handoff, perf-metrics fork — see campaign plan § Print stack.

**CLI (Mac, after `sports`):** `print_tenure` · `print_tenure focus` · `print_tenure core` · `print_tenure full`

**Slides (not markdown PDF):** `hero/TENURE_HERO_slides_AUTO.pptx`, `basic_data_plots/TENURE_BDP_slides_AUTO.pptx`

---

## v0 lock (still valid for exploratory deck)

- File: `faculty_panel_with_pools.jsonl`
- Filter: HIGH/MEDIUM + LOO
- Grain: ASST-PS mean peer LOO / LAST-PS variants on slides (`--window` / `--stat`)
- Y: tenure rate among **resolved**; censored parked from **rates** but **in quantile rank**
- Out: `tenure_sandbox/hero/`, `tenure_sandbox/basic_data_plots/`

---

## Related (PD29, not tenure)

| Item | Path |
|------|------|
| LoL panel | `datasets/legends/lol_big_fish_player_split_panel.csv.zip` |
| Naming | **`legends`** → future `legends_sandbox/`, `legends/scripts/` |
| Notes | [`PD29_notes.md`](../../../../transcripts/PD29_notes.md) |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | Thread opened; scaffold + campaign plan; awaiting first plot. |
| 2026-09-01 | Censored-in-quantile pros/cons → `TENURE_hero_pipeline.md` § for Alex; campaign plan item #6. |
| 2026-09-02 | Alex porch (PD29 same call); BDP/HERO deck labels fixed; `PD29_notes.md` + pipeline § PD29 delta; `datasets/legends/` convention. |
| 2026-09-02 | `build_author_year_career_master.py` → `author_year_career_master.jsonl` (3,630 authors, 99,733 rows, Mac ~2s). |
| 2026-09-02 | Grain naming lock in code + `TENURE_hero_pipeline.md` § Grain naming; retire spell-mean; Alex Â = ALL-PS mean at decision year. |
| 2026-09-02 | `print_tenure focus` (3 docs default) + `core`/`full` tiers in `~/.project_envs.zsh`. |
| 2026-09-02 | `decision_year_cohort.jsonl` (60 rows yas 5–6); PD29 BDP plots + deck section (4 slides). |
| 2026-09-02 | `panel_builder.py` rewrite: dept-year censoring, `asst_time`, `transferred` (17); rebuild Stages 7–8. |
| 2026-09-02 | OTT lock: non-tenured title in Y+1 → `off_tenure_track` attrition; panel rebuilt. |
| 2026-09-02 | `decision_year_cohort.jsonl` rebuilt — all resolved infHM, `asst_time`, no 5–6 filter. |
| 2026-09-02 | BDP replot (v0 + decision cohort) on rebuilt panel; slides updated. |
| 2026-09-02 | Decision HERO: `tenure_pass_a_decision_hero.py` → dept LOO N=389, own career N=280; deck +2 slides. |
| 2026-09-02 | Decision HERO Q8/Q10 robustness (dept LOO + own career); deck now 15 slides. |
| 2026-09-03 | **Reigning tenure HERO** = Q16 cum pubs/career year · dept LOO (not necessarily all BDP on same metric). MBB 3×3 data story built (`MBB_DATA_STORY_reigning_3x3.png`); tenure grid next. |
| 2026-09-03 | Tenure PD29 3×3: dept LOO hist\|ECDF; Ai+Tj, tenure-mass ECDF, overlap, pool size; mosaic + plot highlights. |
| 2026-09-03 | Act II probes: `tenure_pass_a_congestion.py` → panels 7–8 in mosaic (CCT z[1,2] CCT=NO; elite top20% no tail dip). |
