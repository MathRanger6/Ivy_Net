# SCOUT response — selection replay vs reigning HERO aperture

**Prepared:** September 27, 2026  
**In reply to:** [`ASSORT_20260927_SCOUT_selection_population_and_reigning_alignment_questions.md`](ASSORT_20260927_SCOUT_selection_population_and_reigning_alignment_questions.md)  
**Status:** Read-only review. No code executed, no artifacts modified.

---

## Recommendation (plain English)

**Do not treat ASSORT v1 as a test of the reigning HERO or of Alex’s “apply the fitted model to empirical players” idea in the form we actually care about.** The driver is internally consistent with its written scope, but it answers a **different estimand** than the reigning lock:

| Layer | Reigning HERO + PD21 fit (historical) | ASSORT empirical replay v1 |
|-------|--------------------------------------|----------------------------|
| Row grain | **last-ps** for HERO; **all-ps** for PD21 MLE | **Single 2015 audit slice** (not last-ps; includes players with later college seasons) |
| Outcome (primary) | **ever-Y** on last-ps (HERO); **ever-Y on every PS row** (PD21 likelihood) | **`draft_year == 2015`** (45 annual picks) |
| Selection rule | HERO = binned **draft rate vs poolq_LOO**; PD21 = **season softmax** + Bernoulli (top-K only a diagnostic) | **Global top-45** by score on one pooled 2015 roster |
| Congestion θ | **Per season:** `θ = Q_{1−K/N}(A)` with **K = draft count that season** (`gsel._season_k_theta`) | **One global θ** from **105 ever-drafted / 4,267** on audit file |
| Population | ESPN panel **mg10 · min20**, 2009–2021 pipeline | ASSORT **2015 audit** (canonical team, ≥11 captured games, ≥20 min, own PPM z) |

**Smallest defensible correction:** one new **scoped** run (Charles must authorize) with **two linked pieces**, not a sweep:

1. **Outcome / candidate rows:** Identify **2015 exit cross-section** using the **same last-ps rule** as Pass A (`restrict_to_last_season_rows` after filters), on a panel built with **documented** mg10/min20 — *or* explicitly label a **2015-season all-ps** slice as “PD21-season replay” if the question is annual draft within 2015 rosters only. **Do not mix labels.**

2. **Score transport (unchanged coefficients):** For each **season** in the comparison window, compute **θ, congestion, and logits** with the **same functions as PD21** (`attach_player_level_lc` → `pool_c_smooth_team`, `board_logits`), then apply the **same winner rule Charles chooses** (season-wise top-K vs global top-K). Compare **curve** (EW16 bins on **poolq_loo** with winsor) **and** overlap **on the same row set**.

**Essential Charles decision:** Is Monday’s story **(A)** “match the **2015 NBA draft class** by name” or **(B)** “match **HERO shape** on **last-ps ever-draft** at career exit”? v1 is a narrow attempt at (A) on a non-standard population; reigning work is (B) on 09–21.

---

## Evidence tags

| Tag | Meaning |
|-----|---------|
| **[Inspected]** | Read file or code in repo this session |
| **[Reported]** | Prior project memo / Charles relay |
| **[Inferred]** | Logical synthesis — not re-run |
| **[Unresolved]** | Needs Charles or a bounded rebuild |

---

## 1. Authoritative outcome population (reigning)

**[Inspected]** Lock spec: `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md` — **2009–2021**, **last-ps**, **y-draft-mode ever**, **poolq_loo**, **EW16**, **ALLT**, **min20 · mg10**, winsor 0.01–0.99, PPM z within season.

**[Inspected]** Deck manifest: `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json` — cohort text **N = 22,795 last-ps rows**, **615** ever-drafted; panel 9 PNG `HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png`.

**[Inspected]** Typical HERO build command pattern (from README / SCOUT memo 2026-08-27):

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --season-min 2009 --season-max 2021 \
  --panel-rows last-ps --y-draft-mode ever \
  --min-team-season-games 10 --min-minutes 20 \
  --poolq-binning equal_width --n-bins 16
```

**[Inspected]** Order of operations for **ever-Y + last-ps** (`sports/scripts/pass_a_empirical_bundle.py`, `_prepare_hero_panel`, `y_mode != "season"` branch, ~466–488):

1. `conductor.prepare_panel(cfg)` — box rebuild, mg10, min20, **ever-Y** from lookup on **all player-season rows**.
2. `apply_perf_metric_for_analysis` — within-season PPM z, **poolq_loo** / winsor on **full filtered panel** (`panel_build.recompute_teammate_loo_pool_quality`, team-season groups).
3. `filter_panel` — dropna poolq_loo, Y_draft.
4. Optional +DFT.
5. **`restrict_to_last_season_rows`** — one row per athlete at **`max(season)`**; transfer tie → max **minutes** (`y_draft_mode.py` ~190–216).

So **`max(season)` is taken after** season-window and mg10/min20 filters, **not** on raw box before QC. **[Inferred]** Athletes whose **only** eligible rows are before 2021 still exit at their last **eligible** season in window; this is not the same as “verified NBA eligibility date.”

**[Inspected]** **Season-Y** path (same file, ~420–464): labels **Y=1 only on last college PS** via `apply_y_draft_last_season` **before** min/minutes filters, then filters, then last-ps. Used in season-Y experiments (`pass_a/season_y_experiment/`), not the reigning ever-Y lock.

**[Reported]** Panels **7–8** use **2011–21 +DFT all-ps** screening specs; not last-ps (see `MBB_DATA_STORY_plot_highlights.md`, manifest notes).

**2015-only exit population from longitudinal sources:** **[Unresolved]** without a authorized rebuild. The **audit freeze** is **not** last-ps: it is **all accepted 2015 player-team rows**, including athletes with **later** college seasons in the box. **Censoring:** players still in college after 2015 are **in** the audit file but are **not** “2015 career exits.” Do not call them last-ps.

---

## 2. Who defines peer environment?

**[Inspected]** **Reigning HERO path:** `poolq_loo` = leave-one-out mean teammate **`perf`** (z-scored PPM) within **`(team_id, season)`**, computed on the panel **before** last-ps restriction; last-ps keeps each athlete’s **final-season** LOO value (`pass_a_empirical_bundle.py` + `panel_build.py` ~210–234).

**[Inspected]** **PD21 congestion path:** `sports/scripts/pd21_draft_bernoulli_mle.py` → `attach_player_level_lc` → `tier1_pool_assignment.add_team_pool_columns`: **`pool_c_smooth_team`** = team mean **σ(γ(A−θ))** including focal player; **`poolq_loo`** on same roster for diagnostics. **θ per season** from `_season_k_theta` (`grandchild_selection_inverted_u_diagnostic.py` ~139–158): **K = count of Y_draft=1 that season**, θ = quantile **1 − K/N** of **perf** that season.

**[Inspected]** **ASSORT replay v1** (`ASSORT_20260927_empirical_selection_replay_v1.py` ~185–195):

- **Congestion:** team mean **σ(γ\*(A−θ))** on **4267 audit rosters** — aligns with **team L_C** conceptually.
- **θ:** **global** `1 − 105/4267` on audit **A** — **does not** match PD21 **per-season K/N** rule.
- **Peer axis for figure:** **LOO mean of audit `ability_standardized`** on same teams — **not** winsorized **poolq_loo** from Pass A; **not** recomputed from a multi-season panel.

**[Reported]** VECTOR proposal: full roster for environment, exit rows for outcomes. **[Inspected]** Reigning Pass A already computes LOO on **full team-season rosters**, then optionally restricts **rows** to last-ps — **compatible in spirit** with that proposal **if** the underlying panel is the hero pipeline, not the audit file alone.

**[Inferred]** Using **only** the frozen audit CSV **cannot** reproduce Pass A poolq_loo without either rebuilding from box or documenting that audit LOO is a **proxy**, not the reigning axis.

---

## 3. Population and outcome behind saved coefficients

**[Inspected]** JSON: `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json`:

- **`n_player_seasons`: 46,306** · **`n_drafted`: 1,133** (sum of **Y_draft** flags across rows) · **11 seasons** · script **`pd21_draft_bernoulli_mle.py`**
- **`board_form`:** logits **`A/t − λ L^C`**; likelihood **Bernoulli × season softmax** (K not in likelihood).

**[Inspected]** Panel loader: `pd21_draft_bernoulli_mle.main` → **`gsel._prepare_hero_panel(season_min, season_max)`** — **no `last-ps` step** (`grandchild_selection_inverted_u_diagnostic.py` ~108–122). Default filters: **min20**, **mg10 via filter_panel**, **ppm z**, **ever-Y** on **every player-season row**.

**[Inspected]** Score placement matches replay driver: `board_logits` = **`A/t − λ*lc`** (not `(A−λL)/t`) — replay’s `A/t* − λ*C` is **consistent** with PD21, and replay verifies algebra vs `A − tλC` (~197–203).

**Transport vs refit:**

| Element | Transport as-is | Changes estimand |
|---------|-----------------|------------------|
| **γ*, λ*, t*** | Yes, as **declared transport** | Always — different N, teams, z-scores |
| **Season-wise θ, softmax** | Should be **recomputed** on comparison panel | Yes if omitted |
| **Global θ from 105/4267** | **No** — not the MLE convention | v1 used this — **spec mismatch**, not necessarily code bug |
| **Global top-45 vs season top-K** | Changes selection | **Yes** — v1 is global |
| **last-ps vs all-ps rows** | Changes who is in season batches | **Yes** for HERO; PD21 fit was **all-ps** |

**[Inferred]** “Reigning” in the filename marks **storage location**, not “fit on last-ps cross-section.” HERO and MLE **disagree on row grain** by design.

---

## 4. Smallest aligned comparison (one bounded spec)

**Proposed spec (pending Charles — pick A or B):**

### Option B — **HERO-aligned (recommended for Alex curve talk)**

| Knob | Setting |
|------|---------|
| **Build** | `pass_a_empirical_bundle.py` (or conductor + same cfg) **2009–2021**, **mg10 · min20 · ALLT · ppm z · winsor 0.01–0.99** |
| **Roster / LOO / L_C** | Full panel through `apply_perf_metric_for_analysis` + PD21 attach at **(γ\*, λ\*, t\*)** per **season** |
| **Candidate rows** | **`--panel-rows last-ps`** · **`--y-draft-mode ever`** |
| **2015-only slice** | Restrict to rows with **`season == 2015`** *after* last-ps ( athletes whose **last eligible college season is 2015** ) |
| **Selection diagnostic** | **Season 2015 only:** top **K = 45** by **`A/t − λ L^C`** vs **`Y_draft`** with **season-Y** or **`draft_year==2015`** from lookup — **state which label** |
| **Curve** | Same rows: **EW16** on **poolq_loo** (reigning), overlay observed vs model-selected indicators — **descriptive**, not MLE replay |
| **Coefficients** | **Transport only** — no refit |

**Requires:** **[Unresolved]** hero panel row count for 2015 last-ps vs audit 4267 — populations **will differ** (ASSORT canonical-team / 11-game audit ≠ pipeline mg10 alone).

### Option A — **PD21-season replay (annual draft emphasis)**

| Knob | Setting |
|------|---------|
| **Rows** | **all-ps**, **season == 2015**, same pipeline filters as PD21 |
| **θ, L_C, logits** | **`_season_k_theta` + attach_player_level_lc`** for 2015 only |
| **Selection** | Top **K = 45** **within 2015 season** by logits (matches softmax support) |
| **Outcome** | **`draft_year == 2015`** (or season-Y on 2015 PS) |
| **Curve** | Optional secondary — primary is overlap |

**Tradeoff:** Option B matches **deck panel 9** and ever-draft **rate** story; Option A matches **MLE season structure** and **annual** draft class better. **Neither** equals “NBA eligible pool” without further rules.

**2015-only from audit file alone:** **[Inspected]** Possible for **ranking** on fixed audit teams, but **not** aligned to reigning LOO/congestion without recomputing from box or accepting audit proxies.

---

## 5. Completed ASSORT v1 run

**[Inspected]** Report: `docs/results/ASSORT_20260927_empirical_selection_replay_v1_report.md` — **3/45** overlap for fitted vs **3/45** ability-only; **43/45** identity overlap between rules; displaced four non-draftees.

**Implementation error vs question mismatch:**

| Finding | Verdict |
|---------|---------|
| Score formula vs PD21 `board_logits` | **[Inspected]** Consistent with scope doc |
| Top-K tie-break, hashes, 45 lookup IDs | **[Inspected]** Report claims independent check passed |
| **Research question** | **[Inferred]** **Mismatch** — not last-ps, not season softmax selection, not reigning LOO axis, global θ, audit population, in-sample transport |

**Three-of-45:** **[Inspected]** Correct arithmetic for stated rules. **[Inferred]** **Not** strong evidence that congestion is useless globally; **not** evidence about ρ or assignment. Expected random overlap **45²/4267 ≈ 0.47** — observed 3 is above that trivial benchmark but **no test** was run (appropriately).

**What remains interpretable:** On this **audit population**, **transported** congestion **changed 2 of 45 slots** vs ability-only and **did not increase** annual draft hits. **Qualify in report:** “annual 2015 draft class · audit freeze · global top-45 · not reigning HERO estimand.”

**Curve panel:** **[Inspected]** 16 bins on audit **peer_mean_loo** — sparse (45 events). Use only as **porch** beside overlap, not HERO reproduction.

---

## Charles must decide (compact)

1. **Primary Monday claim:** **Annual 2015 names (A)** vs **HERO / ever-draft shape on exit cohort (B)**?
2. **Population anchor:** **Hero pipeline mg10** vs **ASSORT 2015 audit** (can’t merge without explicit merge doc)?
3. **Selection rule for model side:** **Season top-K** (PD21-native) vs **global top-K** (v1)?
4. **Accept transport** of **γ\*, λ\*, t\*** with **no refit** for this meeting, yes/no?

**Do not** expand into refit sweeps, ρ simulation, or reassignment without a new authorization.

---

*SCOUT read-only review — response path as requested.*
