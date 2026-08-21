# SCOUT — Round 3 questions for Charles

**Date:** 2026-08-19  
**Context:** Read full `SCOUT_and_COMPASS_Q_and_A.md` after Round 1 (SCOUT) + Round 2 (COMPASS).  
**Round 3 finding:** No blocking disagreements between SCOUT and COMPASS. Three **decisions** need your call before Round 4 work starts.

------------------------------------------------------------------------

## 1. Near-term priority stack (pick ordering)

COMPASS and SCOUT agree on **what** is unblocked vs blocked; **you** choose **order**:

| Track | Unblocked? | Effort (rough) | Delivers |
|-------|------------|----------------|----------|
| **A** | Yes | Low | Alex HAND / PD20–22 on locked **2011–2021 POST-QC** (mg=10, min=20) |
| **B** | Yes | Medium (hours–overnight) | **ρ/H_sort to 2025** via `scripts/regenerate_pd21_rho_hsort_13_25.sh` |
| **C** | Yes | ~1 day | **OBPM/BPM sensitivity** (39-spec Pass A grid or `--quick` slice; `pass_a_hero_sensitivity_plots.py`) |
| **D** | Partial | ~0.5 day if hoopR works | **Draft register 2022–2025** append + matcher refresh (blocks forward **Y_draft** hero only) |

**Question for Charles:** Which two tracks run **before Alex**, and which are **explicitly parked** until after?

COMPASS default recommendation (Round 2): **A first**, then **B** if time; **C** appendix-only unless you want perf-metric robustness in the brief; **D** parallel / post-Alex unless you need 2022+ draft ventiles now.

------------------------------------------------------------------------

## 2. HAND deck — add B6 CPR table?

COMPASS (B6) flagged optional: small table (bins 13–16 CPR %, culminating in **66.8% bin 16**) next to July replay PNG.

**Question for Charles:** Include in Alex HAND deck, appendix only, or skip?

**Artifact paths if yes:**
- July replay: `pass_a/sensitivity/PASS_A_sensitivity_loo_mg0_2011_2021_b16q_w0199_july_replay_mg0.png`
- Canonical POST-QC hero: `pass_a/PASS_A_empirical_talent_vs_roster_side_by_side.png` (or `_2013_2021`)

------------------------------------------------------------------------

## 3. Backward ESPN scrape (2005–2010)?

SCOUT: data **in-file** and matchable; COMPASS: **park** unless dissertation needs long-panel credibility.

**Question for Charles:** Green-light **2005–2010 back-scrape** now, or **explicitly defer** (document as “not pursued” in Q&A)?

------------------------------------------------------------------------

## SCOUT follow-up for Round 4 (not a Charles decision)

Before executing **A5 / draft append**, SCOUT will verify:

1. **hoopR / sportsdataverse-py NBA draft loader** — exists, schema vs `nbaplayersdraft.csv`, 2022–2025 row counts.
2. **2022–2025 box QC** — team-season games-per-TS histogram under mg=10 when panel window extends (parallel to PD22 slide 6/7).

No COMPASS ↔ SCOUT cross-questions beyond these verification tasks.

------------------------------------------------------------------------

## Round 3 verdict

| Item | Action |
|------|--------|
| Cross-agent conflict | **None** — COMPASS accepts SCOUT verified counts |
| New sub-question in main Q&A | **B5a** added (POST-QC bin 12–16 draft rates — SCOUT verified) |
| Separate COMPASS→SCOUT question doc | **Not needed** |
| This doc | **Charles decisions only** — reply inline or in chat |
