# SCOUT → VECTOR research handoff

**Agent:** SCOUT (NCAA men's basketball / `sports/` domain — panel, empirical hero, generative sim, HPC sweeps, BDP porch plots)  
**Prepared for:** VECTOR (theory, manuscript, cross-domain integration)  
**Date:** 2026-09-22  
**Evidence basis:** Repository Markdown, implementation artifacts under `sports/` and `3-Master_Plan/re_entry/HEROs_and_PASSes/`, SpecStory session exports in `.specstory/history/`, and Alex meeting notes in `transcripts/PD*.md`.  
**Not executed during this assignment:** research code, notebooks, or new analyses.

---

## How to use this document (repo-native onboarding)

VECTOR now has **direct read access** to this repository. This handoff is an **annotated map and history guide**, not a substitute for the repo.

- Follow **repository-relative paths** below to read originals.
- Older material in `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/` assumed **no repo access** — treat as orientation only; paths and “upload this folder” instructions there are **obsolete** (see `00_READ_ME_FIRST_FOR_VECTOR.md`, dated 2026-09-16).
- **Do not** treat agent prose (including this file) as independent verification of empirical results — check JSON sidecars, CSVs, and PNGs cited in repo.

**Path note (common confusion):** Reigning-hero and disposable MBB sandboxes live under  
`3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/`  
(not `population_sandbox/` — that name appears in some Aug 2026 chat logs and older agent text).

---

## 1. Role and working relationship

### What SCOUT owns

| Area | Responsibility | Primary repo home |
|------|----------------|-------------------|
| **Empirical MBB panel** | ESPN box → player-season panel, draft match, `poolq_loo`, ventile hero, LPM | `sports/sports_pipeline/`, `sports/scripts/pass_a_empirical_bundle.py`, conductor notebooks |
| **Performance metrics** | PPM (canonical), SR merge (BPM, PER, WS, TS%), box-built shooting rates | `sports/sports_pipeline/panel_rebuild.py`, `perf_metric.py`, `bpm_merge.py` |
| **Generative sim (Tier 1 / 540)** | Assign → score → select; λ and ρ knockouts; modular engines | `sports/tier1_*.py`, `sports/540_READ_ME_SIM.md`, `sports/scripts/540_*`, `hero_model_reset_bundle.py` |
| **PD20–22 characterization** | Homophily (ρ), MLE (γ, λ, t), temperature sweeps, BDP porch diagnostics | `sports/scripts/pd21_*.py`, `bdp_*.py`, `reigning_hero_calibration.py` |
| **HERO / F-HERO / CCT empirics** | Pass A bundles, conditional plots, reigning hero lock, star sweeps | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/` |
| **Data engineering** | SR scrape/match, skip lists, incremental I/O | `datasets/mbb/`, `sports/scripts/run_sr_rescrape_2009_21.sh` |

**Binding scientific guardrail (Charles lock):** Environment (`L_net = B − D`) ≠ advancement. Advancement = **score** (`S_i = A_i − λ·L_C`) then **select** (top K / Gibbs). Hero porch = Layer A **outcomes**, not causal peer effects.  
**Source:** `3-Master_Plan/BINDING_Selection_is_its_own_step.md`

### What SCOUT does not own

| Agent | Domain | Overlap with SCOUT |
|-------|--------|-------------------|
| **COMPASS** | Cross-project sequencing, claim language, campaign plans | SCOUT implements; COMPASS sets aperture and narrative guardrails (e.g. CCT campaign, perf-metric kill criterion) |
| **CODA** | Army / `talent/` | Shared hero vocabulary; Army is scientific anchor — SCOUT does not edit Army pipelines |
| **PEER** | Tenure / academia | Parallel replication setting only |
| **VECTOR** | Manuscript, theory integration, story | SCOUT supplies figures, numbers, and honest limitation sentences |

### Working relationship with Charles

- Charles drives **aperture locks** (season window, last-ps vs all-ps, min minutes, mg filter) and **Alex meeting follow-through**.
- SCOUT prefers **script-first** reproducible bundles over notebook-only workflows for campaign artifacts (Jul 2026 reset — `540_READ_ME_SIM.md`).
- Charles uses **disposable sandboxes** (`_DISPOSABLE_*`) for exploratory EDA that must not overwrite reigning-hero canonical outputs.
- Notebook edits in Cursor follow **reviewable diff** rules (`.cursor/rules/notebook-blank-edit.mdc`) — relevant when transcribing to locked JupyterLab environments.

---

## 2. Chronological research history

History is **not linear**. Major threads interleave; several “locks” were superseded. Dates below come from repo docs and transcripts unless noted.

### 2026-05 — Tier 1 generative lab and axis-conditioning (foundation)

- Charles and SCOUT built the **modular generative stack** (`tier1_pool_assignment.py`, soft assign τ≈0.65, congestion score `S_i = A_i − λ·L_C`) alongside legacy notebooks (`537`, `538`, `538D`, `539`).
- **Key finding (documented June 2026):** Same score preset, different Plot B x-axis → different curve shape: **inverted-U vs team_mean** but mostly **decreasing vs LOO `poolq_loo`** — generative does **not** bin-for-bin replicate empirical hero on the LOO axis without qualification.  
  **Sources:** `3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md` §2; `5-Manuscript/obsolete/superseded_status_updates/Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md`  
  **Conversation:** `.specstory/history/2026-05-24_12-52-09-0400-scout.md` (τ calibration, playground state, floor model intuition)

### 2026-06 — SCOUT → COMPASS ground-truth report; COMPASS named

- Formal handoff snapshot: empirical inverted-U **replicated** on real rosters; Wang ladder in `538`; generative = proof-of-concept with axis caveat.  
  **Source:** `3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md` (dated 2026-06-08)  
- Agent rename Master Planner → **COMPASS** (`3-Master_Plan/COMPASS_AGENT_IDENTITY.md`, 2026-06-11).

### 2026-07 — Hero model reset; 540 sim path; re-entry docs

- Pivot from extending **538D CELL 10 widgets** to **thin script bundles** and `540_three_step_sim.ipynb`.  
  **Sources:** `sports/540_READ_ME_SIM.md`; `3-Master_Plan/re_entry/00_READ_ME_FIRST.md`; `3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md`
- **Pass A** = empirical hero; **Pass B** = generative λ knockout on fixed rosters; **Pass C (ρ)** parked as optional ablation.  
  **Binding:** score ≠ select (`3-Master_Plan/BINDING_Selection_is_its_own_step.md`)

### 2026-08-04 — PD16: Phase B characterization agenda

- Alex meeting shifted emphasis to **team-level congestion**, θ from K/N, L_C vs ρ diagnostics, calibration roadmap.  
  **Sources:** `transcripts/PD16_notes.md`; `3-Master_Plan/re_entry/08_PD16_Alex_meeting_takeaways.md`  
  **Conversation:** `.specstory/history/2026-08-06_13-07-25-0400-regenerate-pd17-auto-slide.md`, `.specstory/history/2026-08-19_09-30-12-0400-pd20-22-campaign-slide.md`

### 2026-08-19–21 — PD20–22 campaign; CCT (Central Contention and Theme)

- **BDP porch plots** (Â, T̂_j, roster size, overlap) closed Act I.  
- **CCT question:** at **fixed Â**, does draft rate fall as pond thickens (Squid → Jackal)? Conditional plots shipped (P1, P2b, P3). PPM canonical; BPM/OBPM robustness only.  
  **Sources:** `3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md`; `20260820_COMPASS_Charles_CCT_porch_reading.md`; `20260821_SCOUT_CCT_campaign_review.md`  
- Working aperture at that time: **mg10 min20 11_21** (later superseded for reigning lock).

### 2026-08-27 — Aperture shift to **2009–2021 last-ps**; reigning hero named

- Charles green-light: **09–21 · last-ps · ever-draft · ALLT · min20 · mg10 · PPM z** as working primary (K=615 draftees vs 424 for old 13–21 lock).  
  **Source:** `3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md`
- **Reigning hero** = permutation deck slide 12 (`perm_loo_ever_lastps_ew16`) — first **named** hero, not the earlier `FIXED_HERO`.  
  **Source:** `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`
- **Parallel:** SR re-scrape 2009–21 started (~4 hr); does not block PPM runs. BPM absent on SR for 2009–10 (historical SR limitation, not pipeline bug).  
  **Conversation / implementation:** `.specstory/history/2026-08-25_14-26-39-0400-find-old-hero-specs.md`, `.specstory/history/2026-08-28_10-53-57-0400-explore-player-loo-and.md` (porch build-out)

### 2026-08-28 — PD28 calibration; perf-metric fork explored and closed

- Alex (PD28): report **ρ\*, γ\*, λ\*, temperature** on reigning panel — “Give me those numbers.”  
  **Source:** `transcripts/PD28_notes.md`
- **Calibration completed** on 09–21 all-ps: ρ\*≈0, γ\*≈19.57, λ\*≈1.30, t\*≈1.07; temperature sweep shows inverted-U survives at some (λ, t).  
  **Source:** `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/CAMPAIGN_COMPARE.md`
- **Empirical tension documented:** reigning PPM hero LPM β₂ ≈ +0.00172 (flat / tail drop, not clean inverted-U) while sim can show inverted-U at calibrated λ, t — “monotone/flat empirical vs structured generative.”  
  **Source:** reigning hero README § sim_hero; CAMPAIGN_COMPARE
- **Perf-metric EDA (disposable):** Charles worried ρ≈0 on PPM reflects congestion confounding. SCOUT built H_sort ladder + LOO-shape batch; COMPASS ruled **H_sort ≠ promotion gate** — alternates must break monotone draft-vs-LOO. Result: **keep PPM**; BPM helps assign identification, fails hero geometry.  
  **Sources:** `sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/H_SORT_LADDER_REPORT.md`; `loo_shape/LOO_SHAPE_REPORT.md`; `_DISPOSABLE_perf_metric_rho_eda_thread.md`  
  **Conversation:** `.specstory/history/2026-08-28_10-53-57-0400-explore-player-loo-and.md` (continued in agent transcript `bc7b1f66-181d-49f9-a58c-4171629490e3`)

### 2026-09-15–22 — Paper campaign; PD30 story mandate; PD41 assortativity screen

- **PD30 (Sep 15):** Alex asks “what’s the story?” — flipbook / narrative outline priority.  
  **Source:** `transcripts/PD30_notes.md`; `3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md`
- **Pass B λ knockout PNG (G2)** regenerated for deck — core model slide.  
  **Source:** `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/PASS_B_generative_lambda_knockout_side_by_side.png` (referenced in flipbook)
- **PD41 (Sep 22):** Priority flip — **assortativity (H_sort) is the blocker** before narrative can move; MBB ~0.064 framed as **low-sorting boundary condition**; education one-day probe; story PowerPoint by EOW/weekend.  
  **Source:** `transcripts/PD41_notes.md`
- **Same-day repo work (post-call, documented in PD41 notes):** NELS + HSB education 3×3 decks via `scripts/big_fish_data_story.py` — **not SCOUT domain** but affects cross-domain H_sort table Alex requested.

---

## 3. Work actually completed

Legend: **Impl** = code/artifacts exist in repo; **Emp** = numeric result documented in sidecar/report (not re-run for this handoff).

### Empirical panel and Pass A

| Item | Status | Artifact |
|------|--------|----------|
| Panel conductor + ventile hero + LPM | Impl ✅ | `sports/sports_pipeline/`, `sports/scripts/pass_a_empirical_bundle.py` |
| Pass A gallery outputs | Impl ✅ | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/` |
| Reigning hero EW16 PNG | Impl ✅ | `sports_sandbox/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png` (path per reigning README) |
| Reigning **basic_data_plots** porch (items 1–6) | Impl ✅ | `sports_sandbox/reigning_hero/basic_data_plots/` + `manifest.json` |
| Reigning **hero_star_sweeps** (20 runs) | Impl ✅ | `sports_sandbox/reigning_hero/hero_star_sweeps/manifest.json` (`complete=true` per README) |
| Reigning **F-HERO** paired overlay | Impl ✅ | `sports_sandbox/reigning_hero/fhero/` |
| CCT conditional plots (P1, P2b, P3) | Impl ✅ | Documented complete in `CCT_Campaign_Plan.md` §1; PNGs under `sports_sandbox/` and `basic_data_plots/` (specific filenames in campaign plan §3) |

### Calibration (PD21 chain on reigning panel)

| Item | Status | Artifact |
|------|--------|----------|
| ρ\* H_sort bracket | Impl ✅ Emp ✅ | `reigning_hero/calibration/rho/REIGNING_PD21_rho_hsort_calibrate_2009_2021_*_fit_bracket.json`; ρ\*=0 in `CAMPAIGN_COMPARE.md` |
| γ\*, λ\*, t\* Bernoulli MLE | Impl ✅ Emp ✅ | `reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_*.json` |
| Gibbs SELECT temperature sweep | Impl ✅ Emp ✅ | `reigning_hero/calibration/temperature/REIGNING_GRANDCHILD_temperature_select_sweep_*_meta.json` |
| Driver script | Impl ✅ | `sports/scripts/reigning_hero_calibration.py` |

### Sim hero (empirical roster → SELECT → sim HERO)

| Item | Status | Artifact |
|------|--------|----------|
| Reigning sim HERO (Gibbs / topk / bernoulli) | Impl ✅ Emp ✅ | `sports_sandbox/reigning_hero/sim_hero/`; README documents emp 615 vs sim 617 draftees, flat β₂ both sides |
| Gibbs t-sweep overlay | Impl ✅ | `REIGNING_SIM_HERO_gibbs_t_sweep_*` in `sim_hero/` |

### Generative Pass B

| Item | Status | Artifact |
|------|--------|----------|
| λ knockout side-by-side (G2 deck figure) | Impl ✅ | `pass_b/PASS_B_generative_lambda_knockout_side_by_side.png` (+ CSV variants in `pass_b/`) |
| 540 bundle runners | Impl ✅ | `sports/scripts/hero_model_reset_bundle.py`, `540_rho_ablation_bundle.py` |

### Data engineering (2026-08)

| Item | Status | Artifact |
|------|--------|----------|
| SR re-scrape 2009–21 | Impl ✅ (reported complete Aug 2026) | `datasets/mbb/sr_rescrape_2009_21.log`; raw/matched CSVs |
| `bpm_merge.py` extended merge (`has_sr_match`, extra SR columns) | Impl ✅ | `sports/sports_pipeline/bpm_merge.py` |
| 404 skip pairs + alias fix | Impl ✅ | `datasets/mbb/bpm_scrape_skip_pairs.csv`; alias fix in `datasets/mbb/DO_NOT_ERASE/sr_school_slug_aliases.csv` |
| Box shooting aggregates (FG%, eFG%, ts_pct_box) | Impl ✅ | `sports/sports_pipeline/panel_rebuild.py`, `perf_metric.py` |
| `--perf-metric` on PD21 calibrator | Impl ✅ | `sports/scripts/pd21_rho_hsort_calibrate.py` |

### Disposable perf-metric EDA (Aug 2026)

| Item | Status | Artifact |
|------|--------|----------|
| H_sort ladder (9 metrics) | Impl ✅ Emp ✅ | `sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/h_sort/Hsort_ladder_summary_2009_2021.csv`, `H_SORT_LADDER_REPORT.md` |
| LOO-shape promotion batch | Impl ✅ Emp ✅ | `sports/scripts/perf_metric_loo_shape_batch.py` → `loo_shape/LOO_SHAPE_REPORT.md` |
| Acronym-first glossary in auto-report | Impl ✅ | `sports/scripts/perf_metric_rho_eda.py` (`ACRONYM_REFERENCE`, `write_ladder_report`) |

### Verified vs reported

- **Verified by this handoff author:** file existence, README/manifest status flags, CAMPAIGN_COMPARE and LOO_SHAPE tables as written in repo Markdown/CSV.
- **Not re-run:** panel rebuild, calibration JSON numbers, hero PNG regeneration.
- **Reported complete in docs but Charles should spot-check before external claims:** SR rescrape row counts (conversation summary: 4,387 ok, 7 fail 404); exact `%` match rates in merge.

---

## 4. Proposed but unfinished work

| Proposal | Source | Status |
|----------|--------|--------|
| Generative **bin-for-bin match** to empirical LOO inverted-U | `SCOUT_report_to_COMPASS.md` §2 “Not done”; Charles Path A deferred | **Deferred** |
| **538 CELL 7+** robustness (FE, clustering) | SCOUT report §2 | **Placeholder** |
| **Division I filter** for MBB panel | `20260827_SCOUT_to_COMPASS_2009_21_aperture.md` | **Parked** — zero K loss on last-ps mg10 |
| **Min1 vs min20** minutes sensitivity (reigning porch) | `reigning_hero/README.md` | **Parked** |
| **ρ calibration per alternate perf metric** (`--run-rho` on BPM, etc.) | `_DISPOSABLE_perf_metric_rho_eda_thread.md` step 5 | **Parked** — no LOO-shape winner |
| **LOO in SCORE** sensitivity (align SELECT congestion with HERO axis) | `reigning_hero/README.md` § sim_hero options 2–3 | **Proposed, not run** |
| **Refit MLE on LOO L_C** | same | **Proposed, not run** |
| **P2 heatmap** (CCT campaign) | `CCT_Campaign_Plan.md` header | **Parked** |
| **Draft matcher 2c** human label loop | `SCOUT_report_to_COMPASS.md` | **Planned** in gameplan |
| **13–21 vs 09–21 knee overlay** side-by-side | `20260827_SCOUT_to_COMPASS_2009_21_aperture.md` checklist | **Optional**, unchecked |
| **Football QB/WR/TE and DB H_sort** | `transcripts/PD41_notes.md` | **Not computed** |
| **Cross-domain H_sort one-pager** for Alex | `PD41_notes.md` post-call | **Requested**, unclear if finished outside SCOUT |
| **Metric fork BPM-for-assign / PPM-for-advancement** | COMPASS feedback Aug 2026 | **Rejected** unless LOO-shape passes — it did not (except minutes, not substantive) |

---

## 5. Negative results and abandoned approaches

| Result | Why it matters | Source |
|--------|----------------|--------|
| **Generative inverted-U on team_mean, decreasing on LOO axis** | Cannot claim 538D “replicates 530” on same x-axis | `SCOUT_report_to_COMPASS.md` §2 table |
| **ρ\* ≈ 0** on PPM (2011–21 campaign and 2009–21 reigning) | Near-zero homophily at empirical H_sort — assign layer weakly identified on PPM | `CAMPAIGN_COMPARE.md`; disposable H_sort ladder |
| **Alternate perf metrics fail LOO promotion gate** | High H_sort (BPM) → **more convex** draft-vs-LOO β₂, not less | `loo_shape/LOO_SHAPE_REPORT.md` |
| **PPM hero flat LPM β₂** (~+0.0017) with tail-drop bins, not clean inverted-U | Core empirical/generative tension for manuscript | `reigning_hero/README.md`; PD28 sim_hero section |
| **CCT P1 on full panel “NO”**; whisper only on +DFT PPM subsample | Cannot claim universal fixed-Â pond effect from one plot | `CCT_Campaign_Plan.md` win condition §1 |
| **Track C BPM/OBPM robustness** — no “elite dip rescue” | PPM choice not overturned by OBPM | `20260820_1302_SCOUT_to_COMPASS_track_c_bpm_obpm_robustness.md` |
| **537 legacy sort-and-chop sim** | **Frozen** — benchmark only | `540_READ_ME_SIM.md` “Revolution vs evolution” |
| **538D CELL 10 playground UI** | **Legacy** — do not extend | `540_READ_ME_SIM.md` |
| **Education HS pond → BA+ as congestion story** | Alex PD41: “none of them work” for that claim | `transcripts/PD41_notes.md` (cross-domain, but sets MBB boundary framing) |

---

## 6. Current state as of 2026-09-22

### Within SCOUT responsibility

| Category | State |
|----------|-------|
| **Verified artifacts** | Reigning hero porch suite, calibration JSONs, Pass B G2 PNG, disposable perf-metric reports, panel pipeline code |
| **Documented empirical findings** | PPM reigning hero flat β₂; ρ\*≈0; MBB H_sort ~0.064 (ladder + PD41); BPM highest H_sort, worst convex β₂; sim inverted-U at some (λ,t) |
| **Working hypotheses** | MBB is **low-assortativity boundary** (PD41); empirical hero may show **tail drop** without global inverted-U; **score axis (L_C team) ≠ HERO axis (poolq_LOO)** by design |
| **Proposed / unfinished** | Assortativity cross-domain one-pager; LOO-in-SCORE sensitivity; optional ρ-by-metric; football position H_sort |
| **Reported not independently verified here** | Exact SR scrape completion stats; education sandbox numbers; Army H_sort 0.255→0.279 from PD41 live screen |

### Alex priority stack (PD41 — affects how MBB is **used**, not re-run)

1. **P0:** Nail assortativity — “does it matter?” (cross-domain)  
2. **P1:** Education one-day (college prestige / college attended — not SCOUT)  
3. **P2:** Narrative restructure / new PowerPoint by EOW Sep 2026  

**SCOUT read:** MBB work shifts from “fix the hero metric” to **supplying boundary-condition evidence** (low H_sort, familiar porch) in a cross-domain assortativity table. Reigning lock and calibration numbers remain canonical for any MBB slide that needs them.

### Important dependencies

- **ESPN box** `datasets/mbb/mbb_df_player_box.csv` — PPM and box shooting rates  
- **SR matched** `datasets/mbb/bpm_player_season_matched.csv` — BPM/PER/WS (2011+ reliable for BPM)  
- **Grandchild modules** `541_grandchild_homophily_assign` — H_sort and ρ calibration  
- **Alex deck locks** — EW16, last-ps, ever-Y, ALLT for reigning hero claims  

### Outstanding scientific questions

1. Is **ρ≈0 on PPM** “true zero homophily” or **metric/aperture** artifact? (Partially addressed — metric fork closed; assign identification may need BPM H_sort context without switching hero metric.)  
2. Can **generative SELECT** be aligned with **LOO HERO axis** without refitting everything? (Options listed in reigning README — untested.)  
3. How should **flat empirical β₂** coexist with **sim inverted-U** in Act IV prose? (COMPASS/VECTOR narrative problem.)  
4. Does **MBB low H_sort** support or undermine the **cross-domain assortativity thesis** Alex prioritized PD41? (Interpretation open.)

---

## 7. Contradictions, uncertainty, and unresolved decisions

| Issue | Sources | Notes / resolution path |
|-------|---------|-------------------------|
| **Empirical inverted-U vs flat β₂** | Early SCOUT report claims “inverted-U replicated”; reigning lock β₂≈+0.0017 “flat / tail drop” | Not necessarily contradictory — **bin shape** can show tail drop while **quadratic LPM** is flat; shape tags vs LPM are both in reigning README. **Needs:** explicit deck sentence on which object is claimed. |
| **ρ\* = 0 interpretability** | CAMPAIGN_COMPARE; H_sort ladder; COMPASS “metric-specific” | **Unresolved:** structural zero vs weak identification. BPM H_sort high but LOO-shape fails promotion. **Needs:** Charles/Alex decision on whether to report BPM H_sort for assign layer only. |
| **Working season aperture** | CCT plan: **11_21**; reigning lock: **09_21** | Supersession documented in `20260827_SCOUT_to_COMPASS_2009_21_aperture.md`. Older PNGs may still say 11_21 — check `plot_provenance` / filename slugs. |
| **`population_sandbox` vs `sports_sandbox`** | Aug 2026 agent chats; `hero_gallery_paths.py` | **Canonical:** `sports_sandbox/`. Treat `population_sandbox` references as stale unless file exists. |
| **MBB role in dissertation** | PD30 story focus; PD41 boundary condition | **In flux Sep 22:** lead domain vs assortativity appendix. **Needs:** Charles + Alex after assortativity one-pager. |
| **Sim matches draft count but not curvature** | `reigning_hero/README.md` sim_hero | Reported 617 vs 615 ever-drafted; β₂ both flat. **Verified in README text**; PNG inspec not repeated here. |
| **Education decks “work” for sorting contrast but not congestion** | PD41; COMPASS read in PD41_notes | Cross-agent; SCOUT should not overclaim. |

**Questions requiring Charles confirmation**

1. Is the **cross-domain H_sort table** for Alex assembled from repo scripts or ad-hoc meeting numbers?  
2. Should SCOUT **rerun any MBB figures** under PD41 P0, or only supply documented 0.064?  
3. Is **`handoff_upload_no_repo/`** still distributed to VECTOR, or fully retired now that repo access works?

---

## 8. Annotated repository reading list

Prioritized for SCOUT / MBB history. Read in roughly this order.

| Priority | Path | Type | Why read | Start here |
|----------|------|------|----------|------------|
| 1 | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | Binding spec | Non-negotiable score/select/environment separation | Full file |
| 2 | `3-Master_Plan/re_entry/00_READ_ME_FIRST.md` | Re-entry index | Charles-approved reading order for lost re-entry | Table “Your only reading list” |
| 3 | `3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md` | Narrative spec | Pass A/B vocabulary before sim code | Full file |
| 4 | `sports/540_READ_ME_SIM.md` | Technical spec | 540 sim contract; what to ignore (538D playground) | “What to open vs ignore” |
| 5 | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md` | **Current-status** | Aug 2026 lock spec, porch manifest, calibration, sim_hero axis mismatch | Lock spec; calibration; sim_hero |
| 6 | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/CAMPAIGN_COMPARE.md` | Implementation record | PD28 numbers vs PD21 campaign | Headline numbers table |
| 7 | `transcripts/PD28_notes.md` | Historical (Alex) | Origin of calibration ask | Alex ask table |
| 8 | `transcripts/PD41_notes.md` | **Current-status** (Alex) | Sep 22 assortativity priority; MBB as boundary | Headline; H_sort screen |
| 9 | `3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md` | Implementation record | 09–21 aperture decision + SR scrape | Decision table |
| 10 | `3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md` | Working plan | CCT conditional empirics; win conditions | §0–§3 |
| 11 | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/H_SORT_LADDER_REPORT.md` | Empirical finding | H_sort ladder + COMPASS kill criterion | Acronym table; results; LOO batch headline |
| 12 | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/loo_shape/LOO_SHAPE_REPORT.md` | Empirical finding | Promotion gate outcomes | Summary table |
| 13 | `3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md` | Historical context | June 2026 baseline; axis-conditioning finding | §2 status table |
| 14 | `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md` | Working plan | G2 Pass B ownership; Acts I–IV | Figure gaps G1–G3 |
| 15 | `sports/scripts/hero_gallery_paths.py` | Technical spec | Canonical output paths for all hero campaigns | Path constants |

### Key implementation entry points (code)

| Path | Purpose |
|------|---------|
| `sports/scripts/pass_a_empirical_bundle.py` | Pass A empirical hero bundle |
| `sports/scripts/reigning_hero_basic_plots.py` | Reigning porch BDP plots |
| `sports/scripts/reigning_hero_calibration.py` | PD28 ρ / MLE / temperature driver |
| `sports/scripts/reigning_hero_sim_hero.py` | Empirical roster → sim HERO |
| `sports/scripts/pd21_rho_hsort_calibrate.py` | ρ H_sort calibration (+ `--perf-metric`) |
| `sports/scripts/perf_metric_rho_eda.py` | Disposable H_sort ladder |
| `sports/scripts/perf_metric_loo_shape_batch.py` | Disposable LOO-shape promotion batch |
| `sports/sports_pipeline/panel_rebuild.py` | Panel aggregates + shooting rates |

### SpecStory sessions (conversation evidence)

| Session file | Topic |
|--------------|-------|
| `.specstory/history/2026-05-24_12-52-09-0400-scout.md` | Early Tier 1 τ, playground, floor model |
| `.specstory/history/2026-08-19_09-30-12-0400-pd20-22-campaign-slide.md` | PD20–22 campaign slides |
| `.specstory/history/2026-08-25_14-26-39-0400-find-old-hero-specs.md` | Hero spec archaeology |
| `.specstory/history/2026-08-28_10-53-57-0400-explore-player-loo-and.md` | Reigning porch, SR scrape, perf-metric EDA arc |

### Obsolete but useful orientation

| Path | Note |
|------|------|
| `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md` | Pre-repo-access onboarding; **§ “no repo” is obsolete** |
| `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md` | File manifest for manual upload era — use repo paths instead |

---

## Thread log (this handoff)

| Date | Entry |
|------|--------|
| 2026-09-22 | Initial SCOUT handoff for VECTOR repo-native onboarding. No code executed. |

---

*End of SCOUT handoff.*
