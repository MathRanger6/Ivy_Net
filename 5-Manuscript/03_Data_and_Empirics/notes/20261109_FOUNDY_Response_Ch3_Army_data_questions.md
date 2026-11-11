# Response to FOUNDY — Army data questions (Chapter 3)

**Charles → FOUNDY** | 9 November 2026  
**These answers follow the eight questions in** [`20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md`](20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md) (the list we opened this morning). They are drawn from the Mac repo notebooks and configs, the March 2026 AWS export, and our thread decisions—not from new analysis on Vantage.

**How to use this:** background for the Army subsection of Chapter 3. Technical tables and pipeline shorthand live in [`20261109_CODA_Response_Ch3_raw_to_dataframes.md`](20261109_CODA_Response_Ch3_raw_to_dataframes.md). Plain-language prose seed: [`_DISPOSABLE_Ch3_data_empirics_thread.md`](../../re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md) (§ Army — draft of the data section). Peer-metric vocabulary (pond LOO mean vs own−mean): [`20261018_CODA_Response_NVector_Army_LOO_Questions.md`](20261018_CODA_Response_NVector_Army_LOO_Questions.md).

**Legend:** *Verified in repo* · *Charles decision* · *Still to confirm on Vantage / old AWS logs*

---

## 1 · What the raw sources are

The Army analysis joins **two kinds of record**.

**Personnel snapshots (master file).** *Verified:* Built in notebook **502** from the Army Analytics Group **Person–Event Data Environment (PDE)**—PostgreSQL schema around `study_talent_net` / materialized views such as `mv_master_ad_army_qtr_v3a` (exact pull path also documented via **501** and `build_df_masters.py`). **One row** is an **officer on one snapshot date** (`snpsht_dt`), not a whole career in one row. The person key everywhere downstream is **`pid_pde`** (de-identified). Dates that matter early include snapshot date, rank and appointment dates, **`dor_cpt`**, **`dor_maj`**, and year group **`yg`**. Typical fields kept through cleaning: rank, job code (`occ_crer_grp_cd`), unit UIC, component, gender flags, prestige-related fields from hierarchies. Many administrative columns are dropped via `master_remove_cols` and the 502 SQL column list once they are no longer needed.

**Officer evaluation reports (OER file).** *Verified:* Enriched in **512** from PDE evaluation tables. **One row** is an **evaluation period** for a rated officer. Keys: `rated_ofcr` (links to `pid_pde`), **`eval_strt_dt`**, **`eval_thru_dt`**, rater and senior-rater identifiers, rater box scores (`rater_box`, **`snr_rater_box`**). Unit codes on the evaluation support linkage to **503 / 504 / 509** hierarchy lookups (division name, prestige expansion by fiscal year). After Cell 4 in **520**, evaluation-level ids are mapped onto snapshot rows; raw evaluation ids are usually not in the final one-row-per-officer analysis feather.

**What survives to the chapter histograms:** one **last snapshot row per officer** (Cell 11 grain) with merged performance metrics, pool metrics, and an outcome code—after the filter stack described in §2.

*Uncertain:* Whether every table name is unchanged on **Palantir Army Vantage**; treat Vantage as the same DUAs and semantics until Charles confirms a renamed source.

**Print name:** cite **PDE (AAG-RFL)** / Talent Net approved use; Vantage is the current workspace, not a second data system for IRB prose.

---

## 2 · What is kept and what is dropped, in order

Filters apply in **two stages**: 502 (build the snapshot panel) then 520 (Cox cohort and plots).

### Stage A — 502 (snapshot panel)

| Step | What happens | Why |
|------|----------------|-----|
| SQL extract | Date/rank window on master table | Bound load; study era |
| Quality culls | Bad MOS/PID, breaks in service, duplicate appointment dates, duplicate CPT DOR | Unreliable timelines and year groups |
| Outcome | `df_502_base.feather` — **all ranks** on surviving officers | Career history for later DOR logic |

*Not in repo:* a single saved table of officer counts after each 502 substep. Those counts would come from re-running 502 on Vantage and reading notebook logs.

### Stage B — 520 (analysis cohort)

| Order | Filter / rule | Why |
|-------|----------------|-----|
| 1 | Load `df_502_base.feather` | Standard entry |
| 2 | **Commissioned officers only** | Enlisted outside scope |
| 2 | Drop officers with **excluded job codes** (chaplain, medical, etc.—list in `filtering_params`) | Combat arms + selected support frame |
| 3 | **`yg`** attached | Demographics and **cohort window control** |
| 4–6 | OER assignment → cumulative top-box metrics | Officers without assignable OER get NaN metrics |
| 9 | Job list (e.g. CS+CA+CSS), gender dual-record drop, optional divisions | Study population |
| 9 | **`filter_ygs`** when **enabled** | *Charles:* restrict **year groups** so the youngest included cohort has had time to face major promotion before the extract ends—**reduces censoring** (many officers still “open” at last snapshot). March hero run: **YG 2002–2011** enabled in base `pipeline_config.py` of export **`20260320-1000`** (Run 1 `17_1` does not turn YG off in that tarball). |
| 10 | `snpsht_dt >= dor_cpt` | CPT→MAJ study window |
| 11 plots | **`filter_zero_oer`** (`noOER` in filenames) | Drop officers with no OER on checked columns |

**Component (`compo`).** In PDE, `compo` is a string; **`R` = Regular Army**. The **502 → 520** chain does **not** remove every officer who **ever** had a non-`R` snapshot. `compo == 'R'` is applied when building year group and some duplicate-date checks (e.g. CPT + RA appointment rows). An officer may still have later snapshots with **non-`R` component**.

*Charles (2026-11-09):* The chapter describes the **Regular Army CPT→MAJ promotion pool**. **Leaving Regular Army** (transfer to reserve/guard or otherwise leaving that pool) is **substantively attrition** for this study—not a promotion opportunity in another component. **Promotion to major in another component** is a **different system** and is out of scope. Methods prose should say so explicitly; if the extract codes disappearance as `event = 2`, that aligns with treating exit from the RA pool as attrition. **TK:** count officers with mixed component histories on Vantage.

*Draft annotation:* “Analyses refer to the Regular Army competitive promotion pool; exit from Regular Army service before major selection is treated like other attrition from the study cohort, not as censoring within reserve or guard promotion systems.”

**Snapshot / study end:** The extract’s last snapshot dates define who can still be in the file without `dor_maj`. Charles pairs **YG restriction** with that window so bar charts are not dominated by young captains who have not yet reached the board. Filename token **`2002-2022`** on March figures is the **first and last snapshot year among plotted rows**, not a substitute for stating the YG list in prose.

**Flow table the chapter wants most:** *Not checked in* as one CSV. Best fixed points today: **31,692** officers in eight bands on the March CIF bars (sandbox legend); Charles will fill intermediate counts from one Vantage log when available.

---

## 3 · How promotion and attrition are defined

*Verified in Cell 10* (`520_PIPELINE_COX_OVERVIEW.md`, `CR_AND_HR_FOR_DUMMIES.md`).

| Code | Meaning | How it is built |
|------|---------|-----------------|
| **1 — Promotion** | Promoted to **major** | Non-null **`dor_maj`** (from snapshots when rank becomes MAJ). *Charles decision (2026-11-09):* Chapter 3 uses **any promotion to major**, not below-zone-only. Primary-zone / above-zone vertical lines on time plots are **visual guides**, not event filters. |
| **2 — Attrition** | Left before study end without major | `dor_maj` missing and **last snapshot before study end date**—officer disappears from extract. *Not fully disambiguated in code:* reserves, ID change, or a gap in snapshots vs true separation. |
| **0 — Open / censored** | Still in file at study end, no `dor_maj` | Contributes to **denominator** of bar charts; counts as **not promoted** in the promotion bar. |

**Time axis for curves:** days from **`dor_cpt`**; promotion time uses **`dor_maj`**.

**What the chapter histograms show:** Cell 11 function `plot_competing_risks_cif_bars`. On **one row per officer** (after plot filters), **promotion bar** in a performance bin = share with `event==1`; **attrition bar** = share with `event==2`. Officers with `event==0` are in the **denominator only**. This is a **final incidence** picture by band, not a full survival treatise.

**Original research path:** early work emphasized **below-zone** timing; Alex and Charles agreed Chapter 3 should **not** reopen that as the coded outcome. A **single footnote** may note that motivation; the figures use **any MAJ promotion** (draft footnote in CODA §3a).

**Still needed for precise prose:** **event=0 count per band** on the run of record—metadata on PNGs or notebook output, not in git today.

---

## 4 · How a top-box rating is built from evaluations

*Verified:*

- **Top box** on the senior-rater track: numeric value **`50`** in config (`NEW_OER_TB_VALUE`); columns **`snr_rater_box`** (and rater box where used).
- **`tb_ratio_fwd_snr`:** among senior-rater evaluations with a non-null box, the **cumulative share** that are top-box **as of the snapshot date** (forward assignment: latest evaluation whose **through date** is on or before the snapshot).
- **`snr_rater_bwd`:** senior rater on the evaluation window that **covers** the snapshot (backward assignment)—defines **who is in the peer group** in the legacy pool rule.

**Pool and peer quality (Run 1 March figures):**

- **`pool_tb_ratio_mean_snr_fwd`:** mean of peers’ forward top-box ratios in the pool (leave-one-out style peer mean—pond level).
- **`pool_minus_mean_snr_fwd`:** **`tb_ratio_fwd_snr − pool_tb_ratio_mean_snr_fwd`** (own minus peer mean). Plots z-score this for the hero bins.
- Do **not** describe `pool_minus_mean` in prose as “the LOO mean of others only”—that was a wording slip; see LOO response memo.

**Unit / rater reliability:** weakest when UIC is missing, early fiscal years need prestige backfill, or officers move between rating chains; pools are keyed on **rating identity**, not only UIC.

**Plain-language note for readers:** the performance measure is already **relative to a constructed peer group**; the group definition (snapshot-day × senior rater) is wider than the rating window on the form—see §7.

---

## 5 · Run of record for the hero CIF bars

*Verified:* `EXTRACT_MANIFEST.txt` and `army_sandbox` copies.

| Item | Value |
|------|--------|
| **Figure (peer)** | `ARMY_G1_pool_minus_mean_fwd_cif_b8.png` |
| **AWS original name** | `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png` |
| **Notebook export** | `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb` |
| **Configs** | Base `pipeline_config.py` + **`pipeline_config_17_1.py`** (Run 1) |
| **Plotted variable** | Z-scored **`pool_minus_mean_snr_fwd`**, 8 equal-width bins, no group-by |
| **Plot filters** | `filter_zero_oer=True`; **YG 2002–2011** on in March **base** config |
| **Total N in bins** | **31,692** (legend band counts: 49, 1,423, 7,644, 8,131, 7,906, 4,130, 2,153, 256) |
| **Attrition panel** | Same call family—paired promotion + attrition CIF bars |

*Charles:* Local Mac `pipeline_config_17_1.py` later set `filter_ygs.enabled = False`; that is **not** what the March artifact used.

**April 20260421 export** exists in repo; **not** declared run of record for these flipbook figures without Charles sign-off.

**Vantage:** figures stay **placeholders** until a rerun matches these bars; captions should say so.

**Companion figure (own TB):** `ARMY_own_tb_ratio_fwd_cif_b8.png` — same run, `z_tb_ratio_fwd_snr`.

---

## 6 · What is authoritative and what is superseded

**Cite for “how the data were built”:**

- `talent/talent_pipeline/502_working.ipynb`, `512_oer_int_working.ipynb`, `520_pipeline_cox_working.ipynb`
- `pipeline_config.py` **plus** the run override used for the figure (`17_1` for March hero)
- Helpers: `join_oer_to_snapshots_working.py`, `add_cum_oer_metrics_mod_working.py`, `cox_plot_helpers.py`

**Frozen run for March figures:** `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/`

**Support / legacy:** 501, `build_df_masters.py` (older pull path); ignore dated `520_*backup*` unless diffing history.

**Mac tree vs export:** `talent/talent_pipeline/` is **development** (pool grain modes, matrix checklists); always pair claims with **which export or log** produced the PNG.

---

## 7 · Known quirks readers should be told about

**Two clocks.** Snapshot date (`snpsht_dt`) and OER window (`eval_strt_dt` / `eval_thru_dt`) are different. Forward vs backward assignment is documented in `ARMY_fwd_bwd_and_pool_fix_for_dummies.md`.

**Inflated pools (important).** Peers are often everyone on the **same snapshot day** with the **same senior-rater id**. The Army’s true rating pool is officers in one chain for one evaluation window. Median computed pool size at last snapshot **~23** vs median “official” pool size on the form **~12** (2026-09 check). Chapter should say measured peer environment is **wider** than the form’s pool until the pipeline uses evaluation-window grouping (`active_at_eval_thru` etc.—future Vantage work).

**Censoring and YG.** Many officers **open at study end** count as not promoted in bars; **YG + snapshot end** are chosen to limit that unresolved mass—methods prose, not a side remark.

**De-identification.** `pid_pde` only; no names; no public microdata (`Publication_Plan.md`).

**Thin or uneven coverage:** early fiscal years, some branches—*recollection*; not re-audited here.

**Identities:** dual-gender records dropped; reassignment can shuffle `snr_rater_bwd`.

---

## 8 · What can be said in print (IRB / DUA)

*Charles confirmed 2026-11-09:* OER/EES fields are **approved** for detailed methods prose under Talent Net / Combined Data DUAs.

| Generally OK in Ch.3 | Check before final PDF |
|----------------------|-------------------------|
| PDE as source; snapshot + OER logic; top-box = 50; aggregate **N** and filters; band sizes | Tiny cells that could identify units or individuals |
| Variable names at methods depth | Full codebook dump beyond DUA if AAG asks |
| **No** release of microdata or re-identifiable lists | UIC lists/maps beyond ETP enclave rules |

Peck **22-015** “not generalizable research” wording differs from dissertation intent—Charles reconciles with HRPP if challenged; FOUNDY can use CODA §8 table for detail.

**Counts:** embed **March** numbers where known; footnote **Vantage TBD** when rerun pending.

---

## Concepts → columns (quick reference for drafting)

| Concept | Column (March Run 1) |
|---------|----------------------|
| Own performance | `tb_ratio_fwd_snr` |
| Peer group key | `snr_rater_bwd` (legacy pool) |
| Peer / group quality (hero) | `pool_minus_mean_snr_fwd` (then z-scored in plots) |
| Promotion | `dor_maj` → event 1 |
| Attrition | exit before study end → event 2 |
| Still in file | event 0 |

---

## Gaps we already know about (honest limits)

- No single **filter flow table** with officer counts at every step in git.
- **Per-bin event=0** counts on run of record not archived.
- **Vantage** not fully documented in repo yet.
- **Attrition** vs reserves / ID break not cleanly coded.

Charles can supply logs when Vantage is back; until then Chapter 3 uses March placeholders with explicit caption language.

---

*End of response. Questions doc: `20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md`.*
