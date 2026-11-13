# VANTAGE_UPTOPDE_20261112_b13_FULL — file manifest

Use this to **archive live Vantage paths** before copying from `ship_shape/`.

Suggested archive folder on VDI: `~/archive_pre_b13_20261112/` mirroring workspace layout.

---

## A. Flat 520 workspace root (`ship_shape/` → copy here)

| File |
|------|
| `520_pipeline_cox_working.ipynb` |
| `NATO_lvl.py` |
| `add_cum_oer_metrics_mod_working.py` |
| `build_df_masters.py` |
| `build_yg_dict_501.py` |
| `composite_cif_curve_snippet.py` |
| `cox_lifelines_significance.py` |
| `cox_plot_helpers.py` |
| `cox_plt_chnge.py` |
| `cr_tb_stratify.py` |
| `functionsG.py` |
| `init_ray_cluster_working.py` |
| `join_oer_to_snapshots_working.py` |
| `more_functions.py` |
| `pipeline_config.py` |
| `pipeline_config_17_1.py` |
| `pipeline_config_19_1.py` |
| `pipeline_config_div_name.py` |
| `py_503_hierarchies.py` |

---

## B. `docs/` (workspace root)

| File |
|------|
| `docs/00_READ_ME_FIRST.md` |
| `docs/512_520_CELL_COLUMN_INVENTORY.md` |
| `docs/ARMY_PLOT_PROVENANCE_AUDIT.md` |
| `docs/ARMY_RUN_MATRIX_CHECKLIST.md` |
| `docs/ARMY_fwd_bwd_and_pool_fix_for_dummies.md` |
| `docs/ARMY_promotion_plots_CR_vs_Cox_partial_effects.md` |
| `docs/AWS_UPLOAD_CHECKLIST_re_entry.md` |
| `docs/BAND_OF_EXCELLENCE_ARMY_PORCH.md` |
| `docs/BINDING_Selection_is_its_own_step.md` |
| `docs/Hero_Model_Three_Layers_Memo.md` |
| `docs/INDEX_FOR_AGENTS.md` |
| `docs/MARKDOWN_FOR_PDF_PLAYWRIGHT.md` |
| `docs/PARKED_FOR_LATER.md` |
| `docs/PEER_INFLUENCE_AXES_MISMATCH.md` |
| `docs/Peer_Context_prep_for_battle.md` |
| `docs/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md` |
| `docs/Scholar_Fine_Gray_and_Army_HERO_Explained.md` |
| `docs/_DISPOSABLE_Alex_hero_population_thread.md` |
| `docs/_DISPOSABLE_Ch3_data_empirics_thread.md` |
| `docs/rating_window_mode_explanation.md` |
| `docs/talent_layout_README.md` |

---

## C. `talent/re_entry/`

| File |
|------|
| `talent/re_entry/ARMY_RUN_MATRIX_CHECKLIST.md` |
| `talent/re_entry/AWS_UPLOAD_CHECKLIST.md` |
| `talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md` |
| `talent/re_entry/README.md` |
| `talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md` |
| `talent/re_entry/army_act2_probes.py` |
| `talent/re_entry/army_basic_plots.py` |
| `talent/re_entry/army_gallery_paths.py` |
| `talent/re_entry/army_hero_axes.py` |
| `talent/re_entry/army_hero_grid_runner.py` |
| `talent/re_entry/army_hero_slide_plot.py` |
| `talent/re_entry/army_pool_size_probe.py` |
| `talent/re_entry/build_army_data_story.py` |
| `talent/re_entry/diag_mosaic_panel_paths.py` |
| `talent/re_entry/manifests/army_run1_3x3_manifest.json` |
| `talent/re_entry/rating_window_mode_explanation.md` |
| `talent/re_entry/run_army_bdp_pipeline.sh` |
| `talent/re_entry/output/act2/.gitkeep` |
| `talent/re_entry/output/basic_data_plots/.gitkeep` |
| `talent/re_entry/output/data_story/.gitkeep` |
| `talent/re_entry/output/hero/.gitkeep` |

---

## D. `sports/`

| File |
|------|
| `sports/541_grandchild_homophily_assign.py` |
| `sports/scripts/build_data_story_mosaic.py` |
| `sports/scripts/empirical_team_interval_overlap.py` |
| `sports/scripts/gallery_mathtext.py` |
| `sports/scripts/hero_gallery_paths.py` |
| `sports/scripts/hero_plot_style.py` |
| `sports/scripts/interval_overlap_paths.py` |
| `sports/scripts/plot_provenance.py` |
| `sports/scripts/story_page_layout.py` |

---

## E. New in bundle — optional archive targets (may not exist on Vantage yet)

Under workspace root:

| Path |
|------|
| `talent_pipeline_mirror/` (entire folder — mirror-only, do not deploy as live root unless you intend to) |

Contents if you did create it earlier:

- `talent_pipeline_mirror/corrected_merge.py`
- `talent_pipeline_mirror/pipeline_config_17_2.py`
- `talent_pipeline_mirror/pipeline_config_17_3.py`
- `talent_pipeline_mirror/f506_working.py`
- `talent_pipeline_mirror/f509_uic_tools_working.py`
- `talent_pipeline_mirror/uic_*.py`
- `talent_pipeline_mirror/add_dor_col.py`, `cmd_lvl_from_rank.py`, `data_synthetic.py`, `division_colors.py`
- `talent_pipeline_mirror/520_pipeline_cox_working.ipynb` (duplicate of root notebook)

---

## F. Not deployed — keep in staging only

| Folder | Action |
|--------|--------|
| `provisional_next/` | Do **not** replace live root; diff after smoke |
| `continue_tonight/` | Edit docs here; copy to `docs/` when ready |
| `archive_peer_scrub/` | Reference snapshot (~69 files); store read-only beside workspace |

---

## G. Zip root (after unzip)

`README.md`, `README_TRANSFER.md`, `CONTINUE_ON_VDI.md`, `ship_shape/README_UPLOAD.md` (inside ship_shape)

---

**Counts:** ~88 deploy paths under `ship_shape/` (excl. empty dirs); 187 total entries in zip.
