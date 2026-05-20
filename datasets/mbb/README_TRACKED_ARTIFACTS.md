# Git-tracked small artifacts (`datasets/mbb/`)

Everything under `datasets/mbb/` is **gitignored by default** except files listed here.
Large panels, SR tables, and exports stay **rsync-only** (or rebuilt on HPC).

## Tracked files

| File | Produced by | Used by |
|------|-------------|---------|
| `empirical_perf_fit.json` | `530_sports_pipeline.ipynb` **CELL 5b** → `sports_pipeline.empirical_perf_fit.save_fit()` | 538 sweep (`empirical_530`), `tier1_pool_assignment`, CELL 10 overlays |

**Regenerate:** re-run CELL 5b after changing `perf` metric, z-within-season, or analysis filters.

**Rivanna:** `git pull` after push — no `rsync_push sweep538-deps` needed *only* for this file (still use `sweep` + `sweep538-deps` or `git pull` for Python code).

## Adding another small artifact

1. Write it under `datasets/mbb/` (not `sports/datasets/mbb/`).
2. Add a `!datasets/mbb/your_file.json` line in the repo root `.gitignore` (next to `empirical_perf_fit.json`).
3. List it in this README.

Keep files **small** (≪ 1 MB). Do not track panels, `DO_NOT_ERASE/`, or `exports_inverted_u_v0/`.
