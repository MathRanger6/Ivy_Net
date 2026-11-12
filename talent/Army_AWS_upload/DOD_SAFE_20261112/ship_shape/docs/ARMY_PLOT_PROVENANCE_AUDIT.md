# Army plot provenance audit (repo vs live AWS → Vantage)

**Purpose:** Charles’s reminder — **exported notebooks/configs in git are not guaranteed antecedents** of every PNG. Post-export edits to `pipeline_config*.py`, reruns, and **screen captures / slides** may be newer or better. Use this table to **match each figure to filename metadata first**, then verify against notebook Cell 11 logs (or metadata cards on the PNG) — not against today’s Mac `talent_pipeline/` alone.

**Last repo scan:** 2026-11-09 (Mac filesystem mtimes).

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| 1 | Inventory **tracked** Army PNGs + aws_originals | Done below |
| 2 | Map **filename tokens** → filters (Run 1 / Cell 11) | Done for flipbook set |
| 3 | Compare **three config trees** (do not merge blindly) | Done below |
| 4 | **Charles hunt:** screenshots, PPTX, Vantage, `Show_me/` | **Open** |
| 5 | Pick **run of record** per figure for Ch.3 | **Done** — promotion/attrition CIF bars only; see §10 |
| 4b | Sex / prestige / MOS exploratory (`First_good_plots.pdf`) | **OBE** for dissertation (another day) |

---

## 1 · Three code trees (configs diverge)

| Tree | Path | Export / modified | Role |
|------|------|-------------------|------|
| **A — March AWS export** | `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/` | 2026-03-20 | **Flipbook PNG source notebook** per `EXTRACT_MANIFEST.txt`. Base `filter_ygs.enabled=True` (2002–2011). March `pipeline_config_17_1` does **not** override YG. |
| **B — April AWS export** | `talent/Army_AWS_download/TALENT_NET_export_20260421-0802/` | 2026-04-21 | Newer notebook snapshot. April `pipeline_config_17_1` sets **`filter_ygs.enabled=False`**, **`filter_divisions.enabled=True`**. **Not** assumed equal to March plots unless filenames/logs match. |
| **C — Live Mac canonical** | `talent/talent_pipeline/` | `pipeline_config.py` touched 2026-09-22; `17_1` dated 2026-03-20 file but **content differs** from April export | Development / Vantage upload source. `POOL_GROUPING_MODE`, matrix checklists, BDP scripts — **may not match** any exported PNG. |

**Rule:** For a given PNG, provenance = **`(export folder that contains matching `cox/cox_plots/` name OR aws_originals copy)` + decoded filename + notebook output log**. Current Mac `17_1` with `filter_ygs=False` is **not** the March CIF bar default unless you intentionally reran with that override.

---

## 2 · Filename token decoder (Cell 11 / `cox_plot_helpers`)

Example: `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png`

| Token | Meaning |
|-------|---------|
| `cr_` | Competing-risks plot family |
| `z_` | Z-scored plotted variable (`RUN_SCALE='z'`, `pipeline_config_17_1`) |
| `pool_minus_mean_fw` | Forward **pool minus mean** (SNR track; `_fw` in legacy naming) |
| `none` | No `group_by` |
| `b8` | 8 bins |
| `ew` | Equal-width binning |
| `noOER` | `filter_zero_oer=True` (drop officers with no OER on checked cols) |
| `2002-2022` | First/last **snapshot year** in plotted cohort (not always = YG filter alone) |
| `cif_bars` | Final promotion + attrition **bar** panel (not time curves) |

**Run 1 profile (`17_1`):** `tv_vars` = own TB ratio + pool minus mean (SNR); interaction `star_pool_interaction`; CIF defaults above.

---

## 3 · Tracked figures in repo (`army_sandbox/`)

**Packaged for flipbook:** 2026-09-15 (Dropbox mtime — **after** AWS exports; these are **copies**, not fresh AWS pulls).

| Canonical PNG (sandbox) | AWS original name | Declared notebook export | Filters **from filename** (verify in log) |
|-------------------------|-------------------|--------------------------|---------------------------------------------|
| `ARMY_G1_pool_minus_mean_fwd_cif_b8.png` | `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png` | **20260320-1000** / 520 | z pool_minus_mean_fwd · b8 · ew · **noOER** · years 2002–2022 |
| `ARMY_own_tb_ratio_fwd_cif_b8.png` | `cr_z_tb_r_fwd_none_b8_ew_noOER_2002-2022_cif_bars.png` | same | z own TB ratio fwd · same bin/filter/years |
| `ARMY_G1_pool_minus_mean_fwd_CR_curves.png` | `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022.png` | same | Same var; **time curves** (not bars) |
| `ARMY_own_tb_ratio_fwd_CR_curves.png` | `cr_z_tb_r_fwd_none_b8_ew_noOER_2002-2022.png` | same | Own TB time curves |
| `ARMY_star_pool_interaction_cif_b8.png` | `cr_star_pool_interactio_none_b8_ew_noOER_2002-2022_cif_bars.png` | same | Interaction term · b8 · noOER |
| `ARMY_tb_by_division_cif_b1.png` | `cr_z_tb_r_fwd_divname_b1_ew_noOER_2002-2022_cif_bars.png` | same | TB by **div_name** · **1** bin (probe) |
| `ARMY_partial_effects_pool_minus_mean.png` | `combined_effect_z_pool_minus_mean_snr_fwd_stdz.png` | same | Cell 12.6A combined effect |
| `ARMY_combined_effect_pool_minus_mean_stdz.png` | regex `combined_effect.*pool_minus_mean` | same | Same family — **check axes** vs filename |
| `ARMY_cox_competing_risks_analysis_stdz.png` | `competing_risks_analysis_stdz` | same | Cell 12.5 diagnostic |
| `ARMY_cox_model_comparison_stdz.png` | `model_comparison_stdz` | same | Cell 12.4 diagnostic |

**`aws_originals/`** holds 3 preserved AWS filenames (subset of above).

**Band sizes (hero CIF):** disposable thread cites legend **N = 31,692** total, bins 49 … 256 — **from Charles’s read of this figure family**, not re-counted from repo today. **Verify** on PNG metadata card or notebook log.

---

## 4 · **Not** in git (likely live AWS / Vantage / desktop only)

| Asset class | Expected location when it existed | Repo status |
|-------------|-----------------------------------|-------------|
| Full `cox/cox_plots/*.png` tree | `./cox/cox_plots/` on 520 root | **Absent** under `talent/` (0 Army PNGs) |
| **BDP 3×3** `ARMY_DATA_STORY_run1_3x3.png` | `talent/re_entry/output/data_story/` on AWS | **Not** in repo (checklist only) |
| Post-2026 matrix runs (straight LOO, pool grain) | AVD screenshots / backup suffix folders | **Not** in repo unless you uploaded |
| **PowerPoint** embeds | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/*.pptx` | **No Army-named** slides found in that folder (MBB/PD20+ only) |
| Ad hoc screenshot | `current_documents/Show_me/Army Figure.png` | **Present** — single promotion incidence bar chart Q1–Q8 (~0.26→0.71→0.41); **not** same file as twin promo/attrition CIF bars unless cropped. **Provenance unknown** — treat as candidate “newer/different” until matched to a filename or log. |

---

## 5 · Config vs figure — known mismatches (don’t assume)

| Question | March 60320 + Run 1 | April 60421 `17_1` | Mac `talent_pipeline` today |
|----------|---------------------|---------------------|----------------------------|
| YG 2002–2011 filter | **On** (base config) | **Off** in `17_1` override | **Off** in `17_1` override |
| Division filter in `17_1` | (check base; manifest era used div **plot** b1) | **On** in Cell 9 | check current files |
| Pool grain | legacy in old runs; Mac default **`active_at_eval_thru`** | same as export snapshot | **active_at_eval_thru** + matrix docs |
| Peer axis on CIF | **z_pool_minus_mean** (minus-mean) | same in export `17_1` | BDP may use straight LOO on **different** runs |

**Implication:** A figure whose filename says `2002-2022` and `noOER` is **consistent with March-era Run 1**, not automatically with a rerun using April/Mac `17_1` with `filter_ygs=False`.

---

## 6 · Charles hunt checklist (beat screen captures)

Search **outside** this repo copy, in time order:

1. **AWS / Vantage** `cox/cox_plots/` — full filenames + metadata cards (if still on server).
2. **Dropbox / Dissertation / Show_me /** — PNG exports (e.g. `Army Figure.png`).
3. **Email / OneDrive / PowerPoint** — Sep 2025–2026 advisor decks (September deck cited ~2002–2013 CS+CSS in disposable — **may differ** from flipbook `2002-2022` in filename).
4. **Army Virtual Desktop** screenshots from 2026 matrix (`_run2_thru`, `_run6_activesnap`, etc.).
5. **Notebook executed outputs** inside `520_pipeline_cox_working.ipynb` on **60320 vs 60421** exports — compare Cell 11 “Created CIF…” lines.

**When you find a candidate:** record **full filename**, **date**, and whether **metadata card** on PNG lists `filter_ygs`, jobs, N.

---

## 7 · Verification recipe (one figure)

1. Read **AWS original** name from `EXTRACT_MANIFEST.txt` or PNG metadata.
2. Open **`TALENT_NET_export_YYYYMMDD/520_pipeline_cox_working.ipynb`** → search that basename in outputs.
3. Confirm **which `pipeline_config*.py`** was imported in Cell 0 for that run (log often prints `FILTERING PARAMETERS`).
4. Only then cite **YG / branch / noOER** in Ch.3.

---

## 10 · Ch.3 placeholder kit (promotion yes/no only)

Until Vantage bars match March, **embed these** and use the caption block in `_DISPOSABLE_Ch3_data_empirics_thread.md` § Army placeholder kit.

| Priority | Path | Role |
|----------|------|------|
| 1 | `army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png` | Main peer-band promo + attrition bars |
| 2 | `army_sandbox/ARMY_own_tb_ratio_fwd_cif_b8.png` | Own-performance companion |
| 3 (optional) | `army_sandbox/ARMY_G1_pool_minus_mean_fwd_CR_curves.png` | Time shape; not a survival chapter |
| Optional narrative | `2-Way_Ahead/Army_Combination_Data_Stories/Slide66.png` | Nine-panel story; **not** run of record (N, LOO differ) |

**Skip for Ch.3:** division probe, interaction, Cox comparison PNGs; all `First_good_plots` demographics/prestige panels.

**Do document in Ch.3 prose (not optional):** **`filter_ygs`** list + snapshot window on placeholder figures — Charles uses these to **minimize censoring**; distinct from dropping YG-faceted exploratory plots.

---

## 8 · `First_good_plots.pdf` (2026-01-06 PowerPoint export) vs repo — **OBE for Ch.3**

**Pages (rendered for scan):** `3-Master_Plan/re_entry/_tmp_first_good_plots/page-1..4.png`

| PDF page | Plot type | Log / plot name (from screenshot) | Closest repo match | Match? |
|----------|-----------|-----------------------------------|-------------------|--------|
| 1 | CR curves ×4 | `promotion_by_final_job_code`, `promotion_by_yg` | — | **No PNG in repo.** Same *plot engine* as `army_sandbox` CR curves. |
| 2 | CR curves ×2 | `promotion_by_sex` | — | **No PNG in repo.** |
| 3 | Kaplan–Meier | `promotion_by_tb_ratio_snr_binned` (3 groups) | `ARMY_own_tb_ratio_fwd_CR_curves.png` | **Partial:** own-TB **CIF** b8, not KM; different binning. |
| 4 | CR curves ×4 | `tb_ratio_snr_binned`, `prestige_mean_binned` | own-TB / prestige-adjacent CR in sandbox | **Partial:** visual family only; prestige plots not archived. |

**Repo image sweep:** under `talent/` — **0** plot PNGs; Army raster assets = **10** in `army_sandbox/` + `current_documents/Show_me/Army Figure.png`. AWS export folders contain **no** `cox/cox_plots` PNGs in git.

---

## 9 · Pre-shutdown PDE — `2-Way_Ahead/Army_Combination_Data_Stories`

**Not in git repo** (Dropbox dissertation folder). PNG exports **2025-09-24** from `Army_Combination_Data_Stories.pptx` / `.pptm` (PDF dated 2026-01-06).

| Slide PNG | Content | vs March flipbook |
|-----------|---------|-------------------|
| 15, 38, 56, 66, 76 | **Run 1** nine-panel **data story** (`build_data_story_mosaic.py`; EW8 `z_pool_minus_mean_snr_fwd` HERO) | Same **template** as MBB `2-Way_Ahead/Data_Stories/`; **N ≈ 39,517** on panel 1 (not 31,692); panel 9 shape **differs** across slides (LOO definition / filters). |
| 24, 42, 65, 75 | Section titles (e.g. **Run 2 straight LOO**) | No plots. |
| 1 | Title / divider | — |

Manifest in repo (`talent/re_entry/manifests/army_run1_3x3_manifest.json`) points at `talent/re_entry/output/{basic_data_plots,act2,hero}/` — those PNGs were **not** committed; **Way_Ahead slides are the surviving mosaic artifacts.**

---

## Thread log

- **2026-11-09** — Created after Charles note: exports ≠ live configs; hunt screenshots/PPTX/Vantage for newer provenance.
- **2026-11-09** — Crosswalked `First_good_plots.pdf` + `Army_Combination_Data_Stories` (2-Way_Ahead).
