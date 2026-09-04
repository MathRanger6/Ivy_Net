# Big data manifest — Git vs rsync

**Sync tool:** `./scripts/pull_big_data.sh` (run on **Mac** only).  
**Policy hub:** [`DATA_SYNC.md`](DATA_SYNC.md)

## Scopes (`pull_big_data.sh`)

| Scope | What moves | Typical size | Notes |
|-------|------------|--------------|-------|
| **`all`** | `datasets` + `tenure` + `sweep` | **10 GB+** | Full mirror; slow first run |
| **`datasets`** | All `datasets/` big trees below | ~7–8 GB | Default “all datasets” |
| **`big-fish`** | LoL + football **unzipped** CSVs | ~250 MB | Run `unzip` first on Mac for `to-hpc` |
| **`education`** | `nels88/`, `hsb80/` | ~15 MB | Also in Git; rsync is optional |
| **`apache`** | `Apache/` OSS panel | ~3 MB | Also in Git |
| **`mbb`** | `datasets/mbb/**` | **~7 GB** | Gitignored bulk MBB |
| **`tenure`** | `tenure/tenure_pipeline/` (excl. snapshots, dblp_parsed) | **0–3 GB+** | Panels grow on HPC |
| **`sweep`** | `sports/outputs/simulation_sweeps/` results | varies | Usually **from-hpc** (HPC → Mac) |

```bash
# Mac → Rivanna
./scripts/pull_big_data.sh to-hpc big-fish
./scripts/pull_big_data.sh to-hpc datasets
./scripts/pull_big_data.sh to-hpc all

# Rivanna → Mac
./scripts/pull_big_data.sh from-hpc tenure
./scripts/pull_big_data.sh from-hpc all
```

---

## Inventory by path

### `datasets/` — use `pull_big_data.sh`

| Path | In Git? | Rsync scope | Size (order of magnitude) |
|------|---------|-------------|---------------------------|
| `football/.../football_big_fish_player_season_panel.csv` | **No** (`.gitignore`) | `big-fish` | ~178 MB |
| `football/*.zip` | Yes | — (use `git pull`) | ~28 MB |
| `legends/lol_big_fish_player_split_panel.csv` | **No** | `big-fish` | ~72 MB |
| `legends/*.zip` | Yes | — | ~22 MB |
| `nels88/`, `hsb80/` | Yes | `education` | ~4–10 MB each |
| `Apache/` | Yes | `apache` | ~3 MB |
| `mbb/**` | **No** (except `empirical_perf_fit.json`) | `mbb` | **~7 GB** |
| `tenure/dblp.xml` | **No** | manual only | **~4 GB** — do not sync casually |

### `tenure/tenure_pipeline/` — scope **`tenure`**

| Path | In Git? | Should be |
|------|---------|-----------|
| `faculty_panel*.jsonl`, `openalex_*.jsonl`, snapshots_* | **No** (gitignore) | rsync ✓ |
| `author_year_career_master.jsonl` | **Yes (mistake ~30 MB)** | → gitignore + rsync |
| `openalex_author_ids.jsonl`, `openalex_works_by_year.jsonl` | **Yes (mistake; gitignore ignored)** | → `git rm --cached` + rsync |
| `R1_tenure_data.csv` | **Yes (~21 MB)** | → gitignore + rsync |
| `decision_year_cohort.jsonl`, `transfers_audit.jsonl` | Yes (small) | Git OK |

### `sports/` — scope **`sweep`** or existing `rsync_pull_recent_hpc.sh`

| Path | In Git? | Sync |
|------|---------|------|
| `outputs/simulation_sweeps/rivanna_faithful_*` | **No** | `sweep` / `rsync_pull_recent_hpc.sh` |
| `datasets/mbb/exports_inverted_u_v0/` | Yes (small exports) | Git |

### Not in `pull_big_data.sh` (by design)

| Path | Why |
|------|-----|
| `**/faculty_snapshots/` | HPC-only HTML archive (10s of GB) |
| `tenure/tenure_pipeline/dblp_parsed/` | 433 MB JSONL; regenerate from XML |
| `python_packages/dblp-parser/dblp.xml` | Multi-GB; manual |
| `slurm_out/` | Use `rsync_pull_recent_hpc.sh logs` |

---

## Git cleanup (recommended, one-time)

These were committed before gitignore rules; remove from Git **without deleting local files**:

```bash
git rm --cached tenure/tenure_pipeline/author_year_career_master.jsonl
git rm --cached tenure/tenure_pipeline/author_year_career_master_meta.json
git rm --cached tenure/tenure_pipeline/openalex_author_ids.jsonl
git rm --cached tenure/tenure_pipeline/openalex_works_by_year.jsonl
git rm --cached tenure/tenure_pipeline/openalex_low_confidence.jsonl
git rm --cached tenure/tenure_pipeline/R1_tenure_data.csv
# commit + push; then use pull_big_data.sh to-hpc tenure
```

`.gitignore` entries added for the above (see repo `.gitignore`).

---

## Rivanna vs Mac (again)

| Machine | Action |
|---------|--------|
| **Mac** | Run `pull_big_data.sh to-hpc …` or `from-hpc …` |
| **Rivanna** | `git pull` only — **do not** run `to-hpc` on Rivanna |
