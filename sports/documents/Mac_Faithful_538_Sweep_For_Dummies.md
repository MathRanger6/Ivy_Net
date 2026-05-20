# Faithful 538 Sweep — Mac Local → Rivanna Slurm

Step-by-step for the **538 generative** parameter sweep with **viable-peer share** crowding (`pool_c_loo`).  
Rivanna-only details also live in `sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md`.

---

## What this sweep does

| Piece | Source | Notes |
|-------|--------|--------|
| Assign players to teams | `tier1_pool_assignment.simulate_generative_rosters` | Soft assign to fixed \(T_j\) |
| L_Q | `poolq_loo` | LOO mean teammate ability |
| L_C | `pool_c_loo` | LOO **viable-peer share** = (# teammates with \(A>\theta\)) / (pool size − 1) |
| θ | `sports/tier1_sim_config.py` → `VIABILITY_THETA` | Match 530 CELL 5d (median drafted perf) |
| Selection | `assign_selection` | `loo_pool_l_mode=quality` → gap on L_Q; `crowding` → weight on L_C share |
| Inverted-U curve | `faithful_538_sweep.run_scenario` | Bins on **the same L** as selection (not always poolq) |

**Pilot grid:** ~192 Stage-1 scenarios (both `quality` and `crowding` in the grid).  
**Full grid:** ~103,680 Stage-1 scenarios.

---

## Phase 0 — Prerequisites (Mac)

**1. Repo root** (folder with `datasets/`, `sports/`, `scripts/`):

```bash
cd "/path/to/Cursor Workspace PDE"
```

**2. Python env** with `numpy`, `pandas`, `matplotlib` (your usual sports env).

**3. Empirical fit JSON** (only needed if the grid hits `empirical_530`):

- Run **530 CELL 5b** → saves **`datasets/mbb/empirical_perf_fit.json`** (workspace root; **Git-tracked**)
- Commit + push so Rivanna gets it via **`git pull`** (no rsync required for this file alone)
- Pilot includes `empirical_530`; without the file, pilot will error.

**4. θ aligned with 530** (optional refresh):

- After 530 CELL 5d, confirm `VIABILITY_THETA` in `sports/tier1_sim_config.py` matches your panel dial.

**5. Quick import check:**

```bash
cd sports/outputs/simulation_sweeps
python -c "import faithful_538_sweep as s; print('pilot scenarios', len(list(s.iter_stage1(pilot=True))))"
```

Expect: `pilot scenarios 192`.

---

## Phase 1 — Local pilot (Mac)

Smoke-test the full pipeline on your Mac before Rivanna.

```bash
cd sports/outputs/simulation_sweeps
python faithful_538_sweep.py --pilot --reset
```

**What runs**

- Stage 1 only in a **single process** (~192 scenarios × 40 runs each — can take a while on a laptop; start it and let it run).
- Writes under `sports/outputs/simulation_sweeps/`:
  - `faithful_538_sweep_results.jsonl` (append log; resume-friendly)
  - `faithful_538_sweep_stage1_results.csv`
  - `faithful_538_sweep_README.md`

**Faster smoke** (optional): edit `faithful_538_sweep.py` temporarily to run 2 scenarios, or use the one-liner:

```bash
python -c "
import faithful_538_sweep as s
sc = next(x for x in s.iter_stage1(pilot=True) if x.loo_pool_l_mode=='crowding')
r = s.run_scenario(sc)
print(r['curve_bin_l_col'], r['viability_theta'], r['moderate_downturn'])
"
```

Expect `curve_bin_l_col` = `pool_c_loo` for crowding rows and `poolq_loo` for quality rows.

**Stage 1 only** (skip Stage 2 verify):

```bash
python faithful_538_sweep.py --pilot --stage1-only --reset
```

---

## Phase 2 — Local full sweep (Mac, optional)

Only if you have time and cooling; full Stage 1 is **~103k** scenarios.

```bash
cd sports/outputs/simulation_sweeps
python faithful_538_sweep.py --stage1-only --reset   # Stage 1 only, days
# or
python faithful_538_sweep.py --reset                   # Stage 1 + Stage 2 (very long)
```

Most people **skip** full local and go to Rivanna after a successful `--pilot`.

---

## Phase 3 — Push code to Rivanna (Mac)

From repo root:

```bash
# Sweep scripts + Slurm (538 + 537) — if you already git push + pull on Rivanna, optional
./scripts/rsync_push_to_hpc.sh sweep

# Tier 1 Python modules only (empirical_perf_fit.json is in Git at datasets/mbb/)
./scripts/rsync_push_to_hpc.sh sweep538-deps
```

**Git-first workflow:** `git push` on Mac → `git pull` on Rivanna covers code + `datasets/mbb/empirical_perf_fit.json`. Use rsync when you have not pushed yet or Rivanna clone is stale.

Dry run first:

```bash
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep538-deps
```

Do **not** use `rsync_push_to_hpc.sh all` for this job.

---

## Phase 4 — Rivanna preflight

SSH to Rivanna, `cd` to repo root (`~/Ivy_Net` or your clone):

```bash
pwd
ls sim_job_538.slurm
ls sports/outputs/simulation_sweeps/faithful_538_sweep.py
ls datasets/mbb/empirical_perf_fit.json
module load miniforge
~/.conda/envs/sports_net/bin/python -c "import numpy, pandas, matplotlib; print('ok')"
```

---

## Phase 5 — Rivanna pilot Slurm

**One driver job (recommended):**

```bash
PILOT=1 sbatch sim_job_538.slurm
```

Track:

```bash
./scripts/track_slurm.sh
squeue -u "$USER"
tail -f slurm_out/slurm-sim_job_538-*.out
```

**Manual four-step chain** (same stages as the driver):

```bash
PILOT=1 j1=$(sbatch --parsable sports/outputs/simulation_sweeps/rivanna_stage1_faithful_538.slurm)
PILOT=1 j1m=$(sbatch --parsable --dependency=afterok:$j1 sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_538.slurm)
PILOT=1 j2=$(sbatch --parsable --dependency=afterok:$j1m sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_538.slurm)
PILOT=1 sbatch --dependency=afterok:$j2 sports/outputs/simulation_sweeps/rivanna_merge_faithful_538.slurm
```

**Clean old outputs before a fresh run:**

```bash
./scripts/clean_rivanna_faithful_538_sweep.sh --dry-run
./scripts/clean_rivanna_faithful_538_sweep.sh --yes
```

---

## Phase 6 — Rivanna full production

When pilot finishes and merges look sane:

```bash
./scripts/clean_rivanna_faithful_538_sweep.sh --yes   # if you want a clean tree
sbatch sim_job_538.slurm
# optional:
# N_STAGE1_SHARDS=64 N_SHARDS=64 ENV_NAME=sports_net sbatch sim_job_538.slurm
```

Stage 1 is an **array** (~103k tasks sharded); Stage 2 re-runs top Stage-1 specs across multiple seeds.

---

## Phase 7 — Pull results to Mac

```bash
./scripts/rsync_pull_from_hpc.sh sweep
```

Key paths after merge:

| Path | Meaning |
|------|---------|
| `sports/outputs/simulation_sweeps/rivanna_faithful_538/stage1_results.csv` | Merged Stage 1 |
| `sports/outputs/simulation_sweeps/rivanna_faithful_538/grouped_candidates.csv` | Stable inverted-U settings |
| `sports/outputs/simulation_sweeps/rivanna_faithful_538/candidate_plots/` | PNG curves |
| `sports/outputs/simulation_sweeps/rivanna_faithful_538/README.md` | Counts summary |

Filter crowding runs in pandas:

```python
import pandas as pd
df = pd.read_csv("sports/outputs/simulation_sweeps/rivanna_faithful_538/stage1_results.csv")
c = df[df["loo_pool_l_mode"] == "crowding"]
print(c[["moderate_downturn", "curve_bin_l_col", "viability_theta"]].head())
```

---

## Reading results

- **`moderate_downturn`:** interior peak on the binned curve; both ends ≥5% below peak.
- **`moderate_stable`:** (Stage 2 grouped) same rule on ≥60% of seeds.
- **`loo_pool_l_mode=crowding`:** curve is over **viable-peer share** (0–1), not LOO mean ability.
- Compare **`coverage_peak`** and **`median_pool_sd`** to 530 forensics (overlap and roster SD).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `empirical_perf_fit.json` missing | 530 CELL 5b, commit `datasets/mbb/empirical_perf_fit.json`, `git pull` on Rivanna |
| Crowding rows still bin on `poolq_loo` | Pull latest `faithful_538_sweep.py` (uses `pool_l_column`) |
| Pilot “96 scenarios” in old notes | Grid is **192** pilot / **103,680** full Stage 1 |
| Stage 1 timeout | 538 soft-assign is heavy; see `rivanna_stage1_faithful_538.slurm` time limit |
| Mixed 537/538 folders | `rivanna_faithful_537` vs `rivanna_faithful_538` |

---

## File index

| Role | Path |
|------|------|
| Sweep logic | `sports/outputs/simulation_sweeps/faithful_538_sweep.py` |
| HPC worker | `sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py` |
| Slurm driver | `sim_job_538.slurm` |
| θ + defaults | `sports/tier1_sim_config.py` |
| L_C implementation | `sports/tier1_pool_assignment.py` |
| This guide | `sports/documents/Mac_Faithful_538_Sweep_For_Dummies.md` |
| Rivanna detail | `sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md` |
