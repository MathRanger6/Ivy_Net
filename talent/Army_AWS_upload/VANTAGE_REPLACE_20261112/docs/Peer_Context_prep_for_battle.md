# Peer context — prep for battle (Army / Vantage)

**Created:** 2026-11-11  
**For:** Charles + CODA/COMPASS — ship-shape in Cursor, then hand-transcribe to Vantage  
**Companion:** [`PEER_INFLUENCE_AXES_MISMATCH.md`](PEER_INFLUENCE_AXES_MISMATCH.md) (B1–B4 definitions and near-term HERO task)

This memo inventories repo Army **code** (no data), checks alignment with recent pool-grain / plot work, lists gaps, and records open questions before edits.

---

## 1. Army code in the repo (no data) — what you have

**Canonical working tree** (per [`../../talent/documents/README_Talent_Layout_Symlinks_And_AWS_Export.md`](../../talent/documents/README_Talent_Layout_Symlinks_And_AWS_Export.md)):

| Layer | Path | Role |
|--------|------|------|
| **520 pipeline** | [`../../talent/talent_pipeline/`](../../talent/talent_pipeline/) (same as root `talent_pipeline/` symlink) | Notebook `520_pipeline_cox_working.ipynb`, Cell 5/6 helpers, Cox, configs |
| **BDP / HERO / mosaic** | [`../../talent/re_entry/`](../../talent/re_entry/) | `army_basic_plots.py`, `army_hero_slide_plot.py`, `army_act2_probes.py`, `build_army_data_story.py`, `army_gallery_paths.py`, `army_pool_size_probe.py`, `run_army_bdp_pipeline.sh`, manifest |
| **Shared plot infra** | [`../../sports/scripts/`](../../sports/scripts/) | All eight files in [`../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md`](../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) are **present** |
| **Ops helper** | [`../../scripts/backup_rename_suffix.sh`](../../scripts/backup_rename_suffix.sh) | Run-matrix archive renames |
| **Memos / runbooks** | `talent/re_entry/*.md`, this folder, `ARMY_PLOT_PROVENANCE_AUDIT.md`, etc. | Not executed on Vantage, but part of the finish line |
| **AWS snapshots (read-only)** | [`../../talent/Army_AWS_download/TALENT_NET_export_*`](../../talent/Army_AWS_download/) | **Comparison only** — not ground truth |

**520 notebook directly reloads / imports these `.py` files** (all in `talent/talent_pipeline/` unless noted):

`pipeline_config.py`, override modules (`pipeline_config_div_name.py`, `_17_1`, `_19_1`, …), `add_cum_oer_metrics_mod_working.py`, `cox_plot_helpers.py`, `NATO_lvl.py`, `py_503_hierarchies.py`, `init_ray_cluster_working.py`, `build_yg_dict_501.py`, `cr_tb_stratify.py`, `cox_lifelines_significance.py`, Cell 0 import of **`functionsG`** (see gaps below).

**Plot chain on Vantage** (per checklist): whole `talent/re_entry/` + the `sports/scripts/` bundle above. No separate `re_entry` inside the April export folders.

**Upstream notebooks** (`501`–`512`, etc.) exist under `talent/talent_pipeline/` if you ever rebuild from scratch; for **B1–B3 HERO on a frozen feather**, the sprint is usually **520 + re_entry + sports scripts**.

---

## 2. Agreement with recent conversation changes

| Topic | Canonical `talent/talent_pipeline/` | Plot layer `talent/re_entry/` | April export `TALENT_NET_export_20260421-0802/` |
|--------|--------------------------------------|-------------------------------|--------------------------------------------------|
| **`active_at_eval_thru`** + pool toggles | **Yes** — `POOL_GROUPING_MODE`, `POOL_EXCLUDE_PEER_TB_ZERO`, eval cols in `base_time_varying_cols` | Reads `pipeline_config` for overlap grain | **No** — `pipeline_config.py` there is **pre–pool-grain** (no `POOL_GROUPING_MODE` block) |
| **`_peer_anchor` merge** (Run 6 / snapshot) | **Yes** in `add_cum_oer_metrics_mod_working.py` | **Yes** in `army_basic_plots.py` | **No** in that export’s `add_cum_oer_metrics_mod_working.py` |
| **B2 vs B3 on plots** | Feather: `pool_tb_ratio_mean_snr_fwd` = B2, `pool_minus_mean_snr_fwd` = B3 (with `POOL_EXCLUDE_SELF=True`) | **Drift:** `army_basic_plots.py` line 42 → `COL_LOO = pool_minus_mean_snr_fwd` (**B3**); `army_hero_slide_plot.py` default **`z_pool_minus_mean_snr_fwd` (B3)**. Memo wants **B1/B2/B3 comparison** on one run — scripts are still **B3-biased**. |
| **Straight LOO run matrix** | Config supports it | Comment on line 36 says “Run 1” but LOO column is minus-mean | N/A |
| **Band of Excellence (own Â=0)** | N/A in pipeline | **Design in** [`../../talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md`](../../talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md); plot code still uses legacy **`filter_zero_oer`**, not the memo’s own–TB=0 gate | N/A |
| **B1 full-group T_j column** | **Not stored** — only LOO mean + minus-mean + size; B1 must be **reconstructed** or added (per peer-axes memo) | Panel 2 label mentions “T̂_j includes self” while `COL_TJ` is the LOO mean column — **wording vs B1/B2 taxonomy** needs a pass | N/A |

**Bottom line:** For Vantage, treat **`talent/talent_pipeline/` + `talent/re_entry/` + `sports/scripts/`** as source of truth — **not** the snapshot under `Army_AWS_download/.../520_pipeline_cox_working.ipynb` (that export is behind on pool grain and Cell 5).

---

## 3. Gaps in the repo (notebook refers, we don’t have)

| Item | Status | Impact |
|------|--------|--------|
| **`functionsG.py`** | **In repo** (2026-11-12, from peer-scrub download) | Still treat as **sensitive** (DB helpers); archive copy in `Army_AWS_download/20261111_TALNET_peer_scrub/` |
| **`more_functions.py`** | In repo at `talent/talent_pipeline/more_functions.py` | **Supplement** to `functionsG` — explicit imports only; does **not** satisfy Cell 0 `from functionsG import *` |
| **April AWS export** | Stale vs Mac canonical | Fine for **diff history**; bad as upload source for eval-thru |
| **`talent/re_entry/` on export** | Never bundled in `TALENT_NET_export_*` | You add that on import to Vantage (by design) |
| **Optional H_sort** | `sports/541_grandchild_homophily_assign.py` | Only if overlap title uses realized sorting index |

**Not missing (confirmed):** `NATO_lvl.py`, `cr_tb_stratify.py`, `join_oer_to_snapshots_working.py`, `build_df_masters.py`, Cox helpers — in canonical tree; April export omits some of these (`NATO_lvl`, `cr_tb_stratify`) but canonical has them.

---

## 4. Files to get from you / Vantage (before ship-shape edits)

Confirm or supply when ready:

1. **`functionsG.py`** — sanitized copy from Vantage (or permission to stub only the symbols 520 actually calls — needs a quick Cell 0 scrape from your running box).
2. **Vantage directory layout** — Still **520 root** = `Network_1P_shell/` with `big_dfs/`, flat `pipeline_config.py`, and `talent/re_entry/` under that root? Or different?
3. **What’s already on Vantage today** — Full Mac sync of `pipeline_config` + `add_cum_oer_metrics_mod_working`, or still April-ish code?
4. **Run of record** — Name/path of the frozen feather for the **B1–B3** comparison (`df_pipeline_11_cox_analysis.feather` or archived `*_run2_thru.feather`?). Drives whether we only touch plots vs re-run Cells 0–11.
5. **`pipeline_config_div_name` vs base** — Notebook Cell 0 sets `pip_config_file = 'pipeline_config_div_name'`. Confirm that override doesn’t **clobber** `POOL_GROUPING_MODE` on Vantage.
6. **Band of Excellence for this sprint** — Implement own–TB=0 filter in HERO/BoE now, or HERO full sample first then BoE pass?
7. **Any Vantage-only modules** beyond `functionsG` that 520 touches in your current run.

---

## 5. Suggested “ship-shape then mirror-coding” order

1. **Freeze canonical paths** — Edit only `talent/talent_pipeline/` + `talent/re_entry/` (+ maybe one small helper for **B1** if we don’t reconstruct on the fly).
2. **Align plot defaults** with [`PEER_INFLUENCE_AXES_MISMATCH.md`](PEER_INFLUENCE_AXES_MISMATCH.md): explicit **B2 HERO**, labeled **B3**, add **B1** path (column or derived).
3. **Refresh** [`../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md`](../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) for the B1–B3 bundle (manifest paths, three HERO variants, BoE).
4. **One-shot Vantage import** — checklist of files + `chmod` + smoke: `reload_pipeline_config()` → plot chain.
5. **Mirror-coding** only after a single agreed diff list per file.

---

## 6. Charles decisions (2026-11-11)

| ID | Decision |
|----|----------|
| **A** | **`functionsG.py`** → pull from Vantage into Cursor first (see download column below). |
| **B** | **Not** editing from `Army_AWS_download/` export notebooks. Download **latest live Vantage** copies, diff against `talent/talent_pipeline/`, agree on winner, then upload from Cursor only if needed. |
| **C** | Full **520 Cells 0–11** run still to nail down later. **This sprint:** focus **Cell 7+** in the notebook plus plot/mosaic stack (`talent/re_entry/`). Cells 0–6 helpers upload only when re-pool or full rebuild is in scope. |
| **D** | *(still open)* Finish line v1: **B1/B2/B3 axis alignment** first vs **Band of Excellence** in the same pass? |

---

## 7. Vantage ↔ Cursor file sync (working list)

**Charles confirmed Vantage layout (2026-11-11):** see **§8** — pipeline helpers **next to** the notebook; `big_dfs/`, `talent/`, `sports/` at workspace root; **no** `3-Master_Plan/` on Vantage; **`functionsG.py`** beside `520`.

**Workflow (per B):** download → drop into repo for diff (e.g. under `talent/Army_AWS_download/` or direct path) → merge into **`talent/talent_pipeline/`** → mirror-coding upload only for rows marked **after sync**.

| Files to **upload to Vantage** (from Cursor, after ship-shape) | Files to **download to Cursor** (from Vantage, for diff / repo) |
|----------------------------------------------------------------|------------------------------------------------------------------|
| **`talent/re_entry/`** — all plot/mosaic scripts, `manifests/`, `run_army_bdp_pipeline.sh` | **`functionsG.py`** → `talent/talent_pipeline/functionsG.py` (**A — priority**) |
| **`sports/scripts/`** — `build_data_story_mosaic.py`, `story_page_layout.py`, `hero_plot_style.py`, `empirical_team_interval_overlap.py`, `hero_gallery_paths.py`, `interval_overlap_paths.py`, `gallery_mathtext.py`, `plot_provenance.py` | **`520_pipeline_cox_working.ipynb`** (live Vantage copy — compare Cell **7+** to [`talent/talent_pipeline/520_pipeline_cox_working.ipynb`](../../talent/talent_pipeline/520_pipeline_cox_working.ipynb)) |
| **Cell 7+ notebook** — only when Cell 7–11 sections change in Cursor (not the April export snapshot) | **`pipeline_config.py`** |
| **`pipeline_config.py`** / **`pipeline_config_div_name.py`** — when pool grain / Cell 7–11 cols agreed (**defer** if sprint is plots-only on frozen feather) | **`pipeline_config_div_name.py`** (Cell 0 override — confirm it keeps `POOL_GROUPING_MODE`) |
| **`cox_plot_helpers.py`** — if Cell 11–12 / survival plots change | **`add_cum_oer_metrics_mod_working.py`** (compare; needed before any Cell 5 re-run) |
| **`cr_tb_stratify.py`**, **`cox_lifelines_significance.py`** — if stratified CR / significance cells change | **`cox_plot_helpers.py`**, **`cr_tb_stratify.py`**, **`cox_lifelines_significance.py`** |
| *(optional)* **`sports/541_grandchild_homophily_assign.py`** — H_sort in panel 5 title | Any other **520-root `.py`** on Vantage not listed in repo inventory (note names when found) |
| *(optional)* **`scripts/backup_rename_suffix.sh`** | *(not data)* — do **not** download `big_dfs/*.feather` into git unless you explicitly stage a sandbox |

**Sprint scope (C):** prioritize **upload** rows for **`re_entry` + sports scripts**; prioritize **download** for **`functionsG.py`** + live **notebook/config** for diff. **Cell 5** files (`add_cum_oer_metrics_mod_working.py`, pool config) stay **compare-only** until you reopen a full rebuild.

---

## 8. Vantage workspace layout (Charles lock)

**Vantage “home”** = folder where Jupyter runs `520` (same idea as old AWS 520 root). **Not** the full Mac git repo.

```text
<vantage workspace root>/
├── 520_pipeline_cox_working.ipynb
├── pipeline_config.py              ← always next to notebook
├── pipeline_config_div_name.py
├── functionsG.py                   ← alongside 520 (download into git first)
├── add_cum_oer_metrics_mod_working.py
├── cox_plot_helpers.py
├── … other pipeline helpers (flat here, same folder as notebook)
├── big_dfs/
├── talent/
│   └── re_entry/                   ← plot stack (not loose at workspace root)
└── sports/
    ├── scripts/
    └── 541_grandchild_homophily_assign.py   ← optional H_sort (if uploaded)
```

**Not on Vantage:** `3-Master_Plan/` (plot scripts still work; sandbox sync paths in `army_gallery_paths.py` pointing at `HEROs_and_PASSes/` are Mac-only unless you add that tree later).

### Mirror-coding path map (Cursor → Vantage)

| Edit in Cursor (git) | Paste on Vantage |
|----------------------|------------------|
| `talent/talent_pipeline/520_pipeline_cox_working.ipynb` | **workspace root** (next to `pipeline_config.py`) |
| `talent/talent_pipeline/*.py` (helpers) | **same workspace root** (flat — **not** `talent/talent_pipeline/` on Vantage) |
| `talent/re_entry/*` | `talent/re_entry/*` (unchanged) |
| `sports/scripts/*` | `sports/scripts/*` (unchanged) |

**Download `functionsG.py`:** Vantage root → save in git as `talent/talent_pipeline/functionsG.py` → when uploading again, back to **Vantage root** beside the notebook.

**Jupyter cwd:** open/run from **workspace root** so `./big_dfs/...` and `python talent/re_entry/army_basic_plots.py` match `army_gallery_paths.resolve_repo()`.

---

## 9. Mirror-coding checklist (use each session)

1. **Scope** — plots-only (feather exists) vs Cell **7+** vs full **0–11**.
2. **Kernel** — if not cold-starting Cell 0, `functionsG` upload can wait.
3. **Per file** — use **§8** table (flat helpers vs `talent/` vs `sports/`).
4. **Smoke** — from workspace root: `python talent/re_entry/army_basic_plots.py --all` (or your HERO command).

---

## Revision record

| Date | Note |
|------|------|
| 2026-11-11 | Initial inventory from CODA/COMPASS chat — no code changes in this commit |
| 2026-11-11 | §6 Charles A/B/C; §7 Vantage ↔ Cursor sync table |
| 2026-11-11 | §3 + `more_functions.py`: supplement-to-`functionsG` note (Charles) |
| 2026-11-11 | §8–§9 Vantage layout lock + mirror-coding checklist (Charles) |
| 2026-11-12 | Vantage peer-scrub archived under `talent/Army_AWS_download/20261111_TALNET_peer_scrub/` (+ zip); `functionsG.py` ingested; file-by-file verdict = Cursor canonical except `functionsG` from download |
| 2026-11-12 | Upload bundle: `talent/Army_AWS_upload/VANTAGE_PEER_CONTEXT_REPLACE_20261112.zip` + staged tree `VANTAGE_REPLACE_20261112/` |
