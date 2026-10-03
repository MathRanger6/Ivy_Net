# Tenure scripts — entry points

Run from **repository root** unless noted. Prefer conda env **`tenure_net`** for pipeline work.

## Daily Wayback enrichment

| Script | Purpose |
|--------|---------|
| [`../run_wayback_wave.py`](../run_wayback_wave.py) | Cells 2, 3A, 3B, 4 (+ optional apply, post-parse report) |
| [`../run_stage3b_cli.py`](../run_stage3b_cli.py) | Stage 3B only when Jupyter/Dropbox write is flaky |
| [`../tenure_pipeline/apply_url_updates.py`](../tenure_pipeline/apply_url_updates.py) | Worksheet `new_url` → `r1_schools_data.py` |
| [`../apply_url_updates.sh`](../apply_url_updates.sh) | Shell wrapper for apply |

## URL quality & discovery

| Script | Purpose |
|--------|---------|
| [`../tenure_pipeline/probe_faculty_url.py`](../tenure_pipeline/probe_faculty_url.py) | One URL: CDX + Wayback download + parse verdict |
| [`../tenure_pipeline/wayback_wave_report.py`](../tenure_pipeline/wayback_wave_report.py) | Plan snaps \| HTML on disk \| mean parse recs per URL |
| [`../tenure_pipeline/discover_faculty_urls.py`](../tenure_pipeline/discover_faculty_urls.py) | CDX wildcard discovery for low mean-rec schools |
| [`../tenure_pipeline/rebuild_plan.py`](../tenure_pipeline/rebuild_plan.py) | Backup + truncate plan/index, or `--slug` / `--slugs` for one school |

## Analysis / slides (not daily scrape)

| Script | Purpose |
|--------|---------|
| `tenure_basic_plots.py`, `tenure_hero_slide_plot.py`, … | Pass A / hero figures (see filenames) |

**Notebook conductor:** [`../540_tenure_pipeline.ipynb`](../540_tenure_pipeline.ipynb) — Cell 0: `run_wayback_url_report()` after parse when `RUN_WAVE_REPORT_AFTER_PARSE` is True.

**GA walkthrough:** [`../documents/GA_GUIDE_NEW_WAYBACK_FACULTY_URLS.md`](../documents/GA_GUIDE_NEW_WAYBACK_FACULTY_URLS.md)
