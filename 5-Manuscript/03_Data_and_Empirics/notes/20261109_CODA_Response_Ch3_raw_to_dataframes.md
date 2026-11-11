# CODA response — Ch.3 raw Army data → analysis dataframes

**In reply to:** [`20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md`](20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md)  
**Prepared from:** Mac repo notebooks, configs, and overviews — **no new analysis.** Vantage migration **not** documented in repo (flagged uncertain).  
**Does not repeat:** LOO vs minus-mean authority — see [`20261018_CODA_Response_NVector_Army_LOO_Questions.md`](20261018_CODA_Response_NVector_Army_LOO_Questions.md).

**Legend:** **Verified (repo)** · **Recollection / not checked in repo** · **Uncertain — needs AWS/Vantage artifact**

**Charles decision (2026-11-09):** Chapter 3 promotion outcome = **any promotion to major** (`dor_maj` in code). Below-zone / early promotion = original motivation and possible future chapter; not the coded event on current histograms.

---

## Pipeline map (one glance)

```text
PostgreSQL PDE (cpdea) — master + OER sources
  → 501 / build_df_masters (table pulls) — legacy path
  → 502_working.ipynb → df_502_base.feather (snapshot panel + yg, dor_cpt, dor_maj, prestige)
  → 503_hierarchies + 504/509 UIC tools → lookups for unit trees
  → 512_oer_int_working.ipynb → df_oer_enriched (OER + rater/SNR + unit codes)
  → 520_pipeline_cox_working.ipynb
        Cell 1–3: load 502, commissioned + job filters, yg
        Cell 4: assign OERs → tb_ratio_fwd/bwd, cum counts
        Cell 5–6: pools
        Cell 9: filtering_params (YG, branch, gender, …)
        Cell 10: survival intervals + event 0/1/2
        Cell 11: CR plots + CIF **bar histograms** (chapter HERO)
```

**Cite for Chapter 3:** `talent/talent_pipeline/` (canonical Mac tree). Frozen runs: `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/` and `…20260421-0802/`.

---

### 1 · Raw sources

| Stage | **Verified (repo)** — source | One row is | Person key | Main date columns | Survives to Cox panel? |
|-------|------------------------------|------------|------------|-------------------|-------------------------|
| **Master snapshots** | PostgreSQL `cpdea` schema `study_talent_net` / materialized view `mv_master_ad_army_qtr_v3a` (502 overview); 501 + `build_df_masters.py` pull officer-quarter/snapshot tables | Officer on **HRC snapshot date** | `pid_pde` | `snpsht_dt`, appointment / DOR fields, `rank_pde`, UIC, `occ_crer_grp_cd` (job), `compo` | `pid_pde`, `snpsht_dt`, rank, job, unit, `yg`, `dor_cpt`, `dor_maj`, prestige vars → **yes**; most other master columns dropped via `master_remove_cols` / 502 SQL column list |
| **OER file** | Fed through 512 (from PDE OER tables — exact table names in 512 cells; **Recollection:** enriched export, not re-opened here) | One **evaluation period** for rated officer | `rated_ofcr` → links to `pid_pde` | `eval_strt_dt`, `eval_thru_dt` | Rater/SNR ids, `rater_box`, `snr_rater_box`, eval dates → mapped in Cell 4 to snapshot rows; raw eval ids usually **not** in 11_feather |
| **UIC / hierarchy** | 503, 504, 509 notebooks → JSON/feather lookups (`df_uic_div_lookup`, etc.) | Unit metadata / tree | UIC codes | FY-based | `div_name`, prestige expansion — partial; not every UIC field |

**Person key everywhere in 520:** `pid_pde` (PDE person id).

**Uncertain:** Whether Palantir Army Vantage now replaces PostgreSQL table names or connection path — no Vantage notebook checked into this repo as of Nov 2026.

---

### 2 · Filters in order (with reasons)

Two layers: **502 (snapshot build)** then **520 (Cox cohort)**.

#### A. In **502** (`502_DATA_PREP_OVERVIEW.md`)

| Order | Filter | Reason |
|-------|--------|--------|
| 0.5 | Bad MOS / PID cull (SQL) | Drop officers with unusable career field codes early |
| 1 | SQL date window + rank table (`b_502_base`) | Bound extract to study era; reduce load |
| 3 | Breaks in service | Snapshot gaps → unreliable timelines |
| 3 | Duplicate appointment dates (Regular Army) | Bad YG / career start |
| 3 | Duplicate CPT DOR | Bad promotion timeline |
| — | *(keeps all ranks on remaining officers)* | Career history for DOR logic |

**Saved counts:** Intermediate feathers `df_502_00_base` … `df_502_base` — **counts not pinned in git**; re-read notebook logs on AWS/Vantage if chapter needs numbers.

#### B. In **520** (after load)

| Order | Where | Filter | Reason |
|-------|-------|--------|--------|
| 1 | Cell 1 | Source | Prefer `df_502_base.feather` |
| 2 | Cell 2 | Commissioned ranks only | Analysis cohort = officers, not enlisted |
| 2 | Cell 2 | Problematic `occ_crer_grp_cd` (MC, DC, …) — drops **entire officer** | Chaplain, medical, etc. outside combat arms study frame |
| 3 | Cell 3 | `yg` from 502 | Demographic control / filtering |
| 4–6 | Cells 4–6 | Requires OER merge for metrics | Officers without assignable OER → NaN metrics (not always dropped here) |
| 9 | `filtering_params` | Job codes: CA+CS+CSS list; `exclude_other_jobs_during_target_rank` | Combat arms + support branches for promotion study |
| 9 | | Gender: drop dual-gender records | Data quality |
| 9 | | **`filter_ygs`** (when enabled) | **Censoring control:** include YGs that can plausibly complete CPT→MAJ observation; **exclude** tail YGs still mid-window at extract end so bar denominators are not mostly unresolved (`event = 0`). Charles: pair with **snapshot/study end** so officers are followed through promotion possibility. |
| 9 | | Divisions (optional) | Substudies only |
| 10 | Cell 10 | `snpsht_dt >= dor_cpt` | Captain-and-above observation window for CPT→MAJ study |
| 11 plot | `filter_zero_oer` | Officers with **no** OER metric on checked columns | `noOER` in plot filename |

**Component (`compo`, Charles 2026-11-09):** string codes; **`R` = Regular Army**. Pipeline does **not** globally drop officers who **ever** had non-`R` rows; `compo == 'R'` enters YG/duplicate QC at CPT. Mixed component histories possible. **Chapter annotation:** exit from Regular Army promotion pool ≈ **attrition** for CPT→MAJ RA study; MAJ in other component out of scope. Count mixed-comp officers on Vantage — TK.

**Flow table for the chapter:** **Not checked in** as one saved CSV. Closest fixed point: disposable thread band counts **31,692 officers** in 8 bins for March CIF bars (after plot filters, one row per officer). Cox person-interval count **~258k / ~15k** cited in disposable — **Recollection from deck; not re-verified in feather.**

**Charles action:** Run one logged 520 pass on run-of-record config and paste Cell 2/9 counts into chapter supplement.

---

### 3 · Promotion and attrition definitions

**Verified (repo)** — Cell 10 in `520_pipeline_cox_working.ipynb` + `520_PIPELINE_COX_OVERVIEW.md` + `CR_AND_HR_FOR_DUMMIES.md`:

| Code | Definition | Raw basis |
|------|------------|-----------|
| **1 — Promotion** | Officer has non-null **`dor_maj`** | **Any promotion to MAJ** inferred in 502 from snapshots when `rank_pde` becomes MAJ (not a separate “below-zone only” flag). **No BTZ-only filter in Cell 10.** Reference lines on plots (6–7 yr) are **visual** PZ/AZ guides — not used to code events. |
| **2 — Attrition** | `dor_maj` missing **and** `last_snapshot < study_end_date` | Officer **disappears from extract before study end** — treated as exit. **Not checked:** reserves, ID change, or temporary data gap vs true separation (no separate reserve flag in this logic). |
| **0 — Censored / open** | Still in extract at `study_end_date` without `dor_maj` | Right-censored for promotion; counts as **not promoted** in **final bar histogram** numerators/denominators |

**Time axis:** Days from **`dor_cpt`** to interval end (`stop_time`). Promotion event time = **`dor_maj`**.

**Chapter HERO histograms (Cell 11 CIF bars):** `plot_competing_risks_cif_bars` — per bin, **promotion bar** = `(event==1).sum() / n`, **attrition bar** = `(event==2).sum() / n`, on **one row per officer** (last interval) after plot filters. Officers with **event 0** contribute to **denominator only** (still “open” at study end). **Open count per band:** disposable gives ~≤5% unresolved in any band total; **per-band event=0 counts not in repo** — need plot_df export from run of record.

**Charles lock (Ch.3 prose):** Use **“promotion to major”** (any timing). Do not label the histogram as below-zone or early-promotion-only.

---

### 3a · Outcome history — BZ motivation vs what the figures show

**Charles narrative (2026-11-09) — aligned with repo:**

| Phase | What happened |
|-------|----------------|
| **Original question** | **Below-zone (BZ) / early promotion** was the first success concept: promotion is one of the few ways the Army can reward differential performance (no pay lever). That motivated **survival analysis** (time to promotion, not death) and **competing risks** (promotion vs attrition). Memos and `Pertinent_Thoughts.md` still discuss BZ / primary zone (PZ) / above zone (AZ) for **baseline hazard** and stratification. |
| **What Cell 10 codes today** | **Event 1** = officer has **`dor_maj`** (promotion to major in the extract). **No BTZ-only filter** in the survival block. PZ/AZ appear as **reference lines** on time-based CR curves (~6 yr from DOR CPT), not as event definitions. |
| **Display evolution** | Cell 11 **competing-risks curves** (cumulative promotion and attrition by performance band) → **final bar heights** (`plot_competing_risks_cif_bars`) → same grammar in **`army_hero_slide_plot.py`** and other domains as **HERO porches** (where the inverted-U pattern was first seen Army-side). |
| **Chapter 3 scope (PD52 / Alex)** | Tell the **histograms** (final promotion + attrition by band) in the data section. **Allude** to survival/Cox/3D as discovery path; full treatment optional later paper/chapter. |

**One sentence for the dissertation data section:** *The promotion bar is the share of officers in each performance band who reached major during the study window; attrition is exit before study end without major; officers still in the file at the end count as not promoted in the bar denominator.*

**Ch.3 prose scope (Alex + Charles, 2026-11-09):** Do **not** narrate the full BZ → survival → competing-risks lift in the body. Use **either** —

- **(A — recommended)** one **footnote**: early/BZ promotion motivated time-to-event work; **figures use any MAJ promotion**; full survival machinery deferred; or  
- **(D)** **omit** BZ/survival history entirely in Ch.3 (outcome defined in plain language only).

**Draft footnote (A):**

> The motivating policy question initially emphasized promotion timing (including below-zone boards). The displays in this chapter use **promotion to major at any time** and **exit before study end** as competing endpoints. The underlying time-to-event and Cox pipeline is described only briefly; a fuller treatment may appear in separate work.

---

### 4 · Top-box from evaluations

**Verified (repo):**

- **Top box value:** `NEW_OER_TB_VALUE = 50` in `pipeline_config.py`; boxes `rater_box`, **`snr_rater_box`** (senior rater is primary for SNR track).
- **Ratio:** `tb_ratio_fwd_snr` = cumulative share of SNR-rated evaluations (with non-null box) that are top-box — Cell 4 only increments `cum_*` when box present (see 520 overview).
- **Rater ids on OER row:** `rater`, `snr_rater` (512 enrichment); on snapshot after assign: `rtr_rater_*`, **`snr_rater_bwd`** (who defines peer pool key in Run 1).
- **Unit linkage:** 503 hierarchies + 504/509 UIC lookup for division/prestige — **weak when** UIC missing, FY backfill (pre-2015), or reassignment between snapshots (pools keyed off rating identity, not UIC).

**Published forward vs backward distinction:** `3-Master_Plan/re_entry/ARMY_fwd_bwd_and_pool_fix_for_dummies.md`.

---

### 5 · Run of record (HERO CIF bars)

**Verified (repo):** `EXTRACT_MANIFEST.txt`:

- Figure: `ARMY_G1_pool_minus_mean_fwd_cif_b8.png`
- Source notebook: **`talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb`**
- Original output name: `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png`
- Config stack: base **`pipeline_config.py`** + override **`pipeline_config_17_1.py`** (Run 1: `z_pool_minus_mean_snr_fwd`, 8 equal-width bins, `filter_zero_oer=True`)

**YG 2002–2011:** **Confirmed for March 20 export:** base `filter_ygs.enabled=True`; **March `17_1` does not disable YG.** Filename `2002-2022` is **first/last snapshot year in plotted data**, not only YG labels.

**Correction vs later Mac `17_1`:** Local `talent/talent_pipeline/pipeline_config_17_1.py` sets `filter_ygs.enabled = False` — **that is not** what the March artifact run used.

**Attrition panel:** Same plot spec family (competing-risks CIF bar figure — promotion + attrition subplots or paired outputs from same `plot_competing_risks_cif_bars` call).

**Still uncertain (disposable listed):** Exact snapshot min/max dates on that run; **event=0 count per bin** — retrieve from AWS export `cox_results/` metadata cards or re-read notebook output.

**20260421 export:** Exists in repo as newer snapshot — **not declared run of record** for flipbook HERO without Charles sign-off.

---

### 6 · Authoritative vs superseded

| Artifact | Cite? | Notes |
|----------|-------|-------|
| `talent/talent_pipeline/502_working.ipynb` | **Yes** | Current 502 spec |
| `talent/talent_pipeline/512_oer_int_working.ipynb` | **Yes** | OER enrichment |
| `talent/talent_pipeline/520_pipeline_cox_working.ipynb` | **Yes** | Active development |
| `talent/talent_pipeline/pipeline_config.py` + run overrides `17_1`, `19_1`, … | **Yes** | Always cite **pair** used for a figure |
| `501_working.ipynb`, `build_df_masters.py` | **Support** | Table-pull era; 502 SQL path preferred per docs |
| `508_*`, dated `520_*backup*` | **Ignore** unless diffing history | Listed in `CONVERSATION_HANDOFF.md` |
| `Army_AWS_download/TALENT_NET_export_20260320-1000/` | **Yes for March figures** | Frozen run |
| `…20260421-0802/` | **Verify** | Newer export; may supersede code copies only |

**Helpers:** `add_cum_oer_metrics_mod_working.py`, `join_oer_to_snapshots_working.py`, `cox_plot_helpers.py` — canonical under `talent/talent_pipeline/`.

---

### 7 · Quirks readers should know

**Verified / documented:**

- Two clocks: `snpsht_dt` vs OER `eval_*` (fwd/bwd assignment).
- Legacy pool = snapshot day × SNR → **inflated pool size** vs rating window (median ~23 vs official ~12 — disposable 2026-09-20).
- LT/1LT snapshot rows exist in 502/04a but **dropped** for Cox by `snpsht_dt >= dor_cpt`.
- Dual gender records excluded.
- `filter_dates` often **off** while dates still appear in filenames.
- De-identified `pid_pde` — no names in analysis files (**Publication_Plan.md**: proprietary, cannot share raw).

**Recollection / not re-verified:**

- Snapshot calendar gaps (quarterly vs ad hoc).
- OER coverage thin in early FYs for some branches.
- ID merge / reassignment edge cases for `snr_rater_bwd`.

---

### 8 · What can be said in print (IRB crosswalk — for Charles)

**Sources read (2026-11-09):** `5-IRB Process/USMA IRB Approval.pdf` (22-015, 13 Sep 2021), `To submit/Datasets IRB CLeared.docx`, `To submit/USMA_Exempt Request Form_REVISED COMMON RULE_Levine.docx`, `MFR_ETP_UIC_UNMASKED_TALENT_NET_26OCT21_signed.pdf`, plus `Request_Update_aggreements/Entity View _ OEMA_EES_*.pdf` (evaluation entities; confirm they are on your **approved** dataset list for the dissertation phase).

| Ch.3 content | **Generally aligned** with 2021 package | **Flag — check before print** |
|--------------|----------------------------------------|-------------------------------|
| Name **PDE / AAG-RFL**, secondary **de-identified** personnel data | Exempt form Part I; Peck notice | — |
| Purpose: officer careers, peer/rater pools, promotion timing, **dissertation + publications** | Form says YES to publish; officer talent / network framing | Peck **22-015 “not research”** because **not generalizable** — your dissertation *is* generalizing. **For your knowledge:** reconcile with HRPP/AAG if anyone asks whether the thesis is “research” under 32 CFR 219 (may be fine under program-evaluation / secondary-use framing, but the words differ). |
| **Aggregate** counts, band sizes (e.g. 31,692), year window, filters in prose | Consistent with “no identifiable private information” in analysis enclave | Re-identification / small-cell rules from PDE SOP still apply — **avoid tiny cells** that could identify individuals or units. |
| **Variable-level** description (snapshot dates, OER windows, top-box = 50, `pid_pde` coded) | Normal methods prose for secondary limited data | Full **codebook dump** or reproducing **raw field names at scale** — confirm current **DUA** allows in dissertation (not just notebook). |
| **OER / senior-rater box** construction detail | **Charles confirmed (2026-11-09):** evaluation (EES/OER) data **approved** under Talent Net / Combined Data DUAs | Ch.3 may describe top-box fields and eval windows in methods prose. *(2021 one-page “Datasets IRB Cleared” is personnel-only and **stale** for naming — do not treat absence of “EES” there as lack of approval.)* |
| **Unmasked UIC** / company-level prestige | **ETP 26 Oct 2021** — approved exception for TALENT_NET; individuals still de-identified | Do not publish **lists of UICs** or maps that break **FOUO** / low-density rules; ETP is for **analysis enclave**, not necessarily public tables. |
| **Palantir Army Vantage** as access path | **Charles (2026-11-09):** Vantage = same **PDE-A / Talent Net DUAs** — analysis enclave unchanged for compliance purposes | **Ch.3 prose:** say **PDE (AAG-RFL)** as the source name; Vantage is **workspace/ops detail** only (appendix or methods footnote if needed), not a second data system for IRB. |
| Sharing data/code that could re-identify | Peck + Part IV: **no transfer outside team without authorization** | Dissertation = no microdata release; repo `Publication_Plan` already says no Army share. |

**Charles decision (counts):** Embed **March** numbers where known; footnote **Vantage TBD** until bars match.

**Default for Ch.3:** Be **as detailed as methods need** (sources, row meaning, filters, outcomes). **Highlight in your own checklist** anything in the right column before final PDF.

---

## Suggested flow table placeholder (for Charles to fill from one Vantage/AWS log)

| Stage | Officers (unique pid) | Rows | Source |
|-------|----------------------|------|--------|
| SQL master pull | ? | ? | 502 Cell 2 log |
| After 502 QC | ? | ? | `df_502_base` |
| After 520 Cell 2 | ? | ? | notebook print |
| After Cell 9 filters (Run 1 config) | ? | ? | notebook print |
| Cell 11 plot cohort (`noOER`) | 31,692 | 31,692 | disposable / manifest era |

---

## Fix for Chapter 3 disposable draft (pool column)

**Do not use** the disposable line that defines group quality as “LOO mean of others only.” **Code definition:** `pool_minus_mean_snr_fwd = tb_ratio_fwd_snr − pool_tb_ratio_mean_snr_fwd`. For **pond level** (straight LOO), cite `pool_tb_ratio_mean_snr_fwd` — see NVector response.

---

**FOUNDY entry point:** [`20261109_FOUNDY_Handoff_Chapter3_data_empirics.md`](20261109_FOUNDY_Handoff_Chapter3_data_empirics.md) (writer-facing; this file = technical appendix).

*CODA draft 2026-11-09 — Charles approve before NVector send / final Ch.3 embed.*
