# SCOUT response — MBB data lessons for Jazz night

**Prepared:** October 27, 2026  
**In reply to:** [`20261027_Request_to_SCOUT_MBB_Lessons_for_Jazz_Night.md`](20261027_Request_to_SCOUT_MBB_Lessons_for_Jazz_Night.md)  
**Status:** Consolidated history from prior SCOUT memos + read-only check of Jazz night scripts and pipeline code. **No panel rebuild, no pickle rewrite, no new sweeps.**

---

## How to read this document

| Tag | Meaning |
|-----|---------|
| **[Direct repo]** | Verifiable in code, config, or a named file today |
| **[Saved result]** | Named artifact or Jazz night validation string |
| **[Prior SCOUT]** | Carried forward from September 2026 ASSORT responses (see §References) |
| **[Charles-approved]** | Documented rollout / explicit decision in repo memos |
| **[Gap]** | Missing auditable record; do not treat as settled fact |

This reply **builds on** the September 25–27 SCOUT documents listed in the request. It adds an explicit **Jazz night source map** and flags where the frozen pickles **do** or **do not** apply each production rule.

---

## Jazz night sources — what they are (correcting scope)

**[Direct repo]** Immediate caches:

- `3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/cache/all.pkl`
- Same folder: `last.pkl`, `source_manifest.json`

**How pickles were built** (`roster_pressure_analysis.py` → `load_sources`):

| Pickle | `CctSpec` (via `pass_a_congestion_conditional._prepare_panel`) |
|--------|------------------------------------------------------------------|
| **`all.pkl`** | `season_min=2009`, `season_max=2021`, `min_minutes=20`, `min_team_season_games=10`, winsor 0.01–0.99 on **poolq_loo**, `perf_metric=ppm` (default), **`panel_rows=all-ps`**, `y_draft_mode=ever`, `dft=False` |
| **`last.pkl`** | Same filters + **`panel_rows=last-ps`**, rebuilt in `create_section_4_5_4_figure.load_verified_cohort()` and checked against reigning Pass A bin CSV (**22,795** rows, **615** ever-drafted at **2009–2021** before Jazz subsetting) |

**What Jazz night does on top** (not changing the pickles):

- **Analysis window 2011–2021** applied in plotting scripts (`build_eight_bin_plots.py`, `build_comparison.py`), not by rebuilding the cache.
- **Naïve own-performance plots** recompute **within-season z** from raw **`ppm`** (or **`BPM`**) on the **eligible full roster in 2011–2021**, then take **`last.pkl`** rows (final-PS) or **`all.pkl`** rows (all-PS). See validation lines in `jazz_night/02_eight_bin_comparison/ppm_8bins/validation.txt`.
- **Manifest SHA256** match proves **byte identity** of pickles vs `source_manifest.json`; it does **not** prove every historical cleaning decision is documented in one place.

**Request description check:** Your PPM totals (19,803 final-PS, 520 drafted; 46,306 all-PS records; 73 two-team athlete/seasons) align with **`03_ppm_all_vs_final_ps/provenance.json`** and the audit CSV. **[Saved result]**

---

## 1. One-game and partial-season records

### 1.1 What was wrong (combination, not one bug)

**[Prior SCOUT]** + **[Charles-approved]** The problem was **not** “one player logged one game on an otherwise normal team-season” alone. It was the **combination** of:

1. **Team-seasons with very few captured box games** in `mbb_df_player_box.csv` (including **one-game** team-seasons and partial schedules).
2. **ESPN `"-"` placeholder athlete names** on some rows (BYU-style dash roster lines).
3. **Survivorship through `min_minutes ≥ 20`** on those thin team-seasons → a **tiny subset** of players defines the team’s observed environment and means.

So: valid **player** one-game lines on a **full** team-season are a different issue from **team-seasons** represented by **one captured game** in our extract.

### 1.2 Remedy and exact MG10 rule

**[Direct repo]** Sequence in `panel_rebuild.build_from_box`:

1. Read game-level box → season window on config.
2. **`_apply_box_qc`:** optional dash-name drop; **`min_team_season_games`** filter on **distinct `game_id` per `(team_id, season)`** — keep only if **count > min_g** (strict inequality).
3. Aggregate to **`(athlete_id, season, team_id)`** → sum **minutes**, **points** → **`ppm = points/minutes`**.
4. **`min_minutes`** row drop on aggregated player-season rows (production default **20**).
5. Attach **ever-draft** `Y_draft` from lookup; optional SR merge.

**Naming (critical):** `min_team_season_games=10` / **MG10** means **drop team-seasons with ≤10 captured games** → **retain ≥11 distinct games**. Jazz night prose “**more than 10** team-season games” matches the code. **[Charles-approved]** Aug 17, 2026 rollout: mg5 → mg10 same day; **0** additional drafted hero rows lost at mg10 vs mg5. **[Prior SCOUT]** `BOX_QC_panel_build_policy.md`, SpecStory excerpts.

**Why min20 alone failed:** Low-minute **rows** can be dropped while a **one-game team-season** still leaves **1–3 high-minute players** whose team means / LOO / \(\hat{T}_j\) are **not** representative of a full roster. **[Prior SCOUT]** §1.4.

### 1.3 Evidence the remedy mattered (HERO — do not over-generalize to Jazz naïve plots)

**[Saved result]** Paired Pass A sensitivity (Aug 19, 2026): **mg0 vs mg10**, else matched (min20, dash, 2011–2021, 16 quantile bins, winsor, `poolq_loo`, PPM z, ALLT):

- **Elite LOO ventile:** ~**65.8%** of bin-16 rows were **CPRs** (cut-player-rows from dropped team-seasons) under mg0 → **fake right-tail dip** on **poolq_loo** HERO axis.
- **Post-QC:** that CPR contamination removed; middle rise / peak largely persist; **elite right-tail dip under July mg0 does not survive mg10** on that axis.

**[Interpretation]** Charles’s **\(\hat{T}_j\)** upward-bias concern for fragmentary teams is **mechanistically consistent** with small-\(n\) team means + min20 survivorship; **saved CPR tables document LOO**, not a full \(\hat{T}_j\) rank audit. **[Gap]**

**Jazz night naïve plots:** x-axis is **own `perf` (PPM z)**, not `poolq_loo` or \(\hat{T}_j\). MG10 still **drops entire thin team-seasons** before aggregation, so naïve bins **inherit** cleaner team environments but **do not reproduce** the HERO ventile CPR story line-for-line.

### 1.4 Plots that became inappropriate after cleaning

**[Prior SCOUT]** Any HERO / LOO figure built with **mg=0** or pre–box-QC panel as **primary evidence** for **elite-tail downturn** on **poolq_loo**. July replay and mg0 sensitivity are **historical contrast only**, not reigning estimand.

---

## 2. Players appearing under multiple teams

### 2.1 Production panel (HERO / Pass A / Jazz pickles)

**[Direct repo]** Grain is **`(athlete_id, season, team_id)`** — **no canonical-team collapse** in `panel_rebuild` or `conductor.prepare_panel`.

- **Same season, two teams:** **both rows retained** if each passes mg10 + min20 (e.g. mid-season transfer with two stints).
- **Different seasons, different teams:** normal career path; **all rows** in all-PS views.

**Ever-draft label:** `Y_draft = 1` on **every** row for a lookup draftee (**ever** mode), not “drafted this season.” **[Direct repo]** `panel_rebuild` + `y_draft_mode` docs.

### 2.2 Last-PS (final observed season) — authoritative rule

**[Direct repo]** `y_draft_mode.restrict_to_last_season_rows`:

1. Restrict to rows at **`max(season)`** per `athlete_id` **after** season window + mg10 + min20 (and perf/LOO path filters when used).
2. If **multiple rows** at that season (multi-team): keep row with **largest `minutes`**; tie-break uses sort order on **`minutes` descending** (`drop_duplicates` keep first).

**Not** “last row in sort order” without minutes; **not** ASSORT canonical-team games-first rule.

**Order vs filters:** **`max(season)` is computed on the filtered panel**, not on raw box before QC. **[Prior SCOUT]** Sept 27 alignment memo.

### 2.3 ASSORT audit / mechanism v1 (different product)

**[Charles-approved]** ASSORT **2015 audit** and **three-season mechanism** use **canonical team** selection (positive-minute games, then total minutes; **stop on unresolved tie**). That **reduces** multi-team **same-season** rows for those experiments.

**[Prior SCOUT]** ASSORT population **≠** reigning HERO population (2015 slice, global θ, global top-45, etc.).

### 2.4 Jazz night 73 two-team athlete/seasons

**[Saved result]** `jazz_night/03_ppm_all_vs_final_ps/multi_team_player_seasons_audit.csv` — **73** athlete/seasons, **71** players, **two `(team_id, season)` rows** each, **retained and flagged**.

**Assessment:**

| View | Multi-team handling |
|------|---------------------|
| **all-PS (Jazz)** | **Intentionally inherits** production grain — **both** rows kept; ever-Y repeated on each row → **1,133** positive **records**, **520** unique draftees. |
| **final-PS (Jazz)** | Uses **`last.pkl`** → one row per player via **`restrict_to_last_season_rows`** at **2011–2021** subset; at **max season**, **max minutes** wins among team rows. **Not** the same as keeping both stints. |

**Conclusion:** You are **not missing an approved production correction** by keeping 73 pairs in **all-PS**. You **are** applying the **HERO last-PS rule** for final-PS via `last.pkl`. **Do not** silently apply ASSORT canonical-team to these pickles without Charles authorization and a **new** cache build.

**[Gap]** Row-level adjudication (transfer vs data error) for the 73 pairs — not done in repo; audit is **flag only**.

---

## 3. Performance, minutes, standardization, missingness

### 3.1 Order of operations (production)

**[Direct repo]** For hero-style paths (`pass_a_congestion_conditional._prepare_panel`, ever-Y branch):

1. `conductor.prepare_panel` → **`build_from_box`** (box QC mg10, dash, aggregate, **ppm**, min20, ever-Y, SR merge).
2. `apply_perf_metric_for_analysis` → copy metric → **within-season z** of `perf` → **`poolq_loo`** (+ winsor on LOO when configured).
3. `filter_panel` (dropna LOO/Y; min_minutes again if cfg).
4. Optional **`restrict_to_last_season_rows`** if last-PS.

**PPM definition:** **`points` and `minutes` summed over captured games**, then **`ppm = points/minutes`** — **not** mean of game-level PPM ratios. **[Direct repo]** `panel_rebuild.py` ~167–186. **[Charles-approved]** Sep 25 clarification: exported `ppm` is **derived after filtering**, not a raw ESPN column.

### 3.2 Drop vs zero-PPM

| Mode | Where | Status |
|------|--------|--------|
| **Drop rows with `minutes < 20`** | Production Pass A, reigning hero, Jazz pickles, PD21 panel loader default | **[Charles-approved]** production |
| **`ppm = 0` if minutes < threshold, keep row** | PD21 **`--ppm-zero-below-minutes`** / calibration contrast | **Exploratory / sensitivity** — not Jazz naïve default |

Mutually exclusive philosophies; do not mix without labeling.

### 3.3 Standardization — Jazz vs pickle `perf`

**Pickles:** `perf` = within-season z of **ppm** on panel built with **2009–2021** seasons (each season’s mean/std on **that season’s eligible rows** after filters).

**Jazz PPM eight-bin scripts:** Subset **2011–2021**, finite **`ppm`**, recompute **`perf = (ppm - mean_season) / std_season`** on that subset, then align to **`last.pkl`** keys. **[Saved result]** `validation.txt` asserts match to reconstructed z.

**Naïve plots:** **No clipping** of `perf` for display (per request). **Winsor 0.01–0.99** applies to **`poolq_loo`** in hero pipeline, **not** to own-performance axis in Jazz scripts.

### 3.4 PPM vs BPM / SR measures

**[Prior SCOUT]** Sept 27 performance memo:

- **PPM:** ESPN box only; full pipeline control.
- **BPM/PER/WS:** require **`bpm_player_season_matched.csv`** (name + school_slug + season); ~**97.8%** BPM coverage on ASSORT audit keys; **match ≠ same filters** as audit construction.

**Jazz lesson:** Switching **BPM → PPM** on final-PS changed N (**19,289 → 19,803**) and drafted count (**510 → 520**) because **514 players** had PPM but not BPM on final row (**10** additional ever-draftees). **[Saved result]** `Jazz_Night_Experimental_Walkthrough.md` — **metric change confounded with sample change** unless explicitly matched.

**[Gap]** Formal “authoritative metric” for dissertation naïve plot — **Charles choice in progress** (Jazz documents both).

### 3.5 Missing final-row metrics

Low-minute and thin team-season drops happen **before** last-PS collapse; athletes with **no row ≥20 min** in exit season disappear from final-PS. Draft lookup can exist without panel row (~**269/789** draft-only lookup gap cited in exploratory work — **[Gap]** for exact current lookup sync).

---

## 4. Candidate populations and outcome timing

### 4.1 All-PS vs last-PS

| Estimand | Rows | Outcome | Typical use |
|----------|------|---------|-------------|
| **all-PS** | Every eligible player-season | **ever-Y** on each row | PD21 Bernoulli MLE (**46,306** rows / **1,133** Y=1 flags); mechanism panels |
| **last-PS** | One row per athlete at max season (minutes tie-break) | **ever-Y** on that row | Reigning HERO (**22,795** @ 09–21 full pickle; **19,803** @ 11–21 PPM Jazz) |

**[Prior SCOUT]** PD21 fit is **all-PS ever-Y**; HERO lock is **last-PS ever-Y** — **by design**, not accidental.

**Jazz all-PS naïve rate:** Pooled **record-weighted** ever-Y proportion (**~2.45%**) is **not** annual draft rate **K/N** and **not** “520 drafts per year.”

### 4.2 All colleges vs draftee-only teams (ALLT / +DFT)

**Reigning HERO default:** **ALLT** — all teams passing mg10/min20, not restricted to teams with a draftee. **[Direct repo]** `restrict_teams_by_draftees=False` in Jazz cache build.

**+DFT:** Optional restriction to team-seasons on teams with ≥1 draftee — **`dft.pkl`** in same cache folder; **not** used in current Jazz PPM eight-bin path.

### 4.3 Season window: 2009 vs 2011

**Pickles:** Built **2009–2021** (matches reigning **filename** and many campaign labels).

**Effective PD21 loader:** **`FULL_PANEL_SEASON_MIN = 2011`** in `grandchild_selection_inverted_u_diagnostic.py` — **2009–2010 never enter** MLE panel even if window says 2009. **[Prior SCOUT]** Sept 27; **[Gap]** confirm original run machine inputs.

**Jazz naïve products:** Explicit **2011–2021** analysis window on pickles.

### 4.4 Labels and matching

- **ever-Y:** from **`athlete_id_draft_lookup.csv`** — one flag per draftee athlete.
- **Season-Y / last-college-PS-only Y=1:** separate experiments; not Jazz naïve default.
- **Repeated Y=1 on all-PS:** same person counted on **freshman, sophomore, …** rows — Bernoulli likelihood **multiplies** rows; expected positives under season softmax ≈ **1 per season** in PD21 (misaligned with ~1133 flags). **[Prior SCOUT]** + model chapter §4.8.

### 4.5 Environment vs outcome row (HERO vs score)

**[Direct repo]** LOO / `poolq_loo` computed on **full team-season roster** (after row filters), then **last-PS** takes athlete’s **final-season** LOO. Compatible with “full roster for environment, exit row for outcome” **when** the panel is the hero pipeline — **not** when using ASSORT audit CSV alone.

**Congestion in score (`L_C`, sigmoid θ, γ) ≠ `poolq_loo` on HERO plots** — separate columns; do not merge in interpretation. **[Binding project rule]** score ≠ select.

---

## 5. What you can safely reuse

### 5.1 Authoritative for Jazz night (current frozen path)

| Item | Role |
|------|------|
| `roster_pressure_comparison/cache/all.pkl`, `last.pkl` + `source_manifest.json` | Frozen **ppm**, mg10, min20, ever-Y panel snapshots |
| `jazz_night/02_eight_bin_comparison/build_eight_bin_plots.py` | PPM/BPM naïve bins with **recomputed** 2011–21 z |
| `jazz_night/03_ppm_all_vs_final_ps/build_comparison.py` | all-PS vs final-PS **same players**, same z |
| `sports/sports_pipeline/panel_rebuild.py` | Box QC + aggregation truth |
| `sports/sports_pipeline/y_draft_mode.py` | last-PS + season-Y semantics |
| `sports/scripts/pass_a_congestion_conditional.py` | `_prepare_panel` order of operations |
| `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md` | MG10 policy mirror |

### 5.2 Authoritative for reigning HERO (different estimand than Jazz naïve)

| Item | Role |
|------|------|
| `sports/scripts/pass_a_empirical_bundle.py` | HERO figures, last-PS ever-Y |
| `reigning_hero/README.md` | Lock spec (09–21 label, EW16, ALLT, …) |
| `pass_a/sensitivity/` index | mg0 vs mg10 **LOO** evidence |

### 5.3 Use with explicit scope labels (not interchangeable)

| Item | Warning |
|------|---------|
| ASSORT `rotation_audit_2015` / replay v1 | Canonical team, 2015-only, global θ — **not** Jazz pickles |
| `player_season_panel_530.csv` | May predate box QC; check rebuild flag |
| Pre–Aug 2026 PNGs with **mg=0** | Elite-tail HERO claims |
| `REIGNING_PD21_*.json` | **MLE** estimates — not generative **λ**, **t_sel** without rescaling (see model §4.8 / 4A.4) |
| Filename **`2009_2021`** | May mean **campaign label** while **effective panel starts 2011** |

### 5.4 Other data lessons (brief)

- **Dash placeholder names:** drop `"-"` display names at box QC. **[Charles-approved]**
- **Draft lookup gaps:** ever-Y panel under-counts draftees vs lookup; track **not-in-panel** lists in y_draft audits. **[Direct repo]** `apply_y_draft_last_season`
- **Transfer careers (~5% draftees with >1 team_id in panel):** global first→last Δ dev spans teams; separate from **within-season** 73-row Jazz audit. **[Exploratory]** Δ dev sandbox 2026-10-08.
- **Binning:** Equal-width vs quantile **same outcomes, different shapes** — ASSORT λ=4 lesson; Jazz eight-bin repeats this for **own perf**. **[Saved result]** ASSORT penalty bars report.
- **Incremental I/O:** long network/disk loops should checkpoint — project rule for scrapers, not panel build (atomic rebuild).

---

## Requested conclusion

### Settled decisions to carry forward

1. **MG10 at panel build:** drop `(team_id, season)` with **≤10** captured **`game_id`** values; retain **≥11** games. **[Charles-approved]**
2. **Production low minutes:** **drop** player-season rows with **`minutes < 20`**, do not zero PPM, for hero/Jazz pickle spine.
3. **PPM:** sum points / sum minutes **after** box QC; within-season **z** for own-performance displays.
4. **Panel grain:** **`(athlete_id, season, team_id)`** in production — **no** canonical-team merge in hero pipeline.
5. **Last-PS:** **`max(season)`** then **`max(minutes)`** among ties — **`restrict_to_last_season_rows`**.
6. **Ever-draft label:** lookup-based **ever-Y**; all-PS repeats label; **not** annual draft events.
7. **Jazz naïve plot:** **own performance vs observed ever-draft rate** — **not** congestion HERO, **not** fitted softmax/Bernoulli without new auth.
8. **Score vs select:** environment (`poolq_loo`, congestion) and **score** (`A − λC`) remain separate from **selection** rule and from naïve marginal rates.

### Current-source discrepancies requiring attention

1. **Pickle window (2009–2021) vs Jazz analysis (2011–2021):** Document both whenever citing N or rates.
2. **`last.pkl` verification (22,795 / 615 @ 09–21) vs Jazz PPM final-PS (19,803 / 520 @ 11–21):** Same lineage, **different subset** — not a contradiction if labeled.
3. **Re-standardization:** Jazz PPM scripts recompute z on **2011–21**; do not assume pickle **`perf`** equals Jazz **`perf`** without the validation merge (`build_eight_bin_plots.py` asserts).
4. **73 multi-team athlete/seasons in all-PS:** Flagged, not adjudicated; **final-PS** collapses via minutes rule — document when comparing views.
5. **PD21 / reigning vs Jazz:** MLE **all-PS** + season softmax **≠** naïve pooled proportion **≠** exact-K **SELECT** — do not transport **λ_MLE** to generative **λ** without §4A.4 rescaling.
6. **ASSORT canonical-team rules:** **Not applied** to Jazz pickles — do not cite ASSORT population counts as Jazz counts.

### Genuinely open choices for Charles

1. **Canonical naïve metric for manuscript step 1:** **PPM** (full N) vs **BPM** (SR-dependent, smaller N) vs side-by-side with matched sample.
2. **Reporting window:** **2011–2021** only vs **2009–2021** to align with reigning deck label.
3. **All-PS vs final-PS** as primary naïve display (Jazz added both; outline step 1 still favors one focal population).
4. **Multi-team same-season rows:** keep both (current all-PS), canonical-team merge, or manual transfer table for sensitivity.
5. **Whether to rebuild pickles** after any future QC change vs continue subsetting frozen caches with explicit manifests.

### Smallest necessary reconciliation before further plotting

**No population replacement required** if Charles accepts:

- Frozen **`all.pkl` / `last.pkl`** + manifest hashes,
- **2011–2021** subset + **PPM re-z** as implemented in **`02_eight_bin_comparison`** / **`03_ppm_all_vs_final_ps`**,
- Captions stating **ever-draft pooled rate**, **final-PS vs all-PS**, and **MG10/min20** in plain language.

**Optional one-page addendum for NVECTOR:** Copy **`03_ppm_all_vs_final_ps/README.md`** “What each view counts” into the walkthrough — it already matches this SCOUT assessment.

---

## References (prior SCOUT / policy)

1. [`assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md`](assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md)
2. [`assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md`](assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md)
3. [`assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_performance_metric_provenance.md`](assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_performance_metric_provenance.md)
4. [`3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md`](../../re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md) (CPR / ventile tables)
5. [`3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md`](../../re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md)

---

*Thread log: 2026-10-27 — Initial consolidated Jazz night response; no pickle or pipeline edits.*
