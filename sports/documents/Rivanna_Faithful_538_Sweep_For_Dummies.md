# Rivanna Faithful 538 Sweep — For Dummies

This guide runs the **faithful 538 generative Tier 1 sweep** on Rivanna. It mirrors the 537 sweep workflow but targets **538** mechanics: soft assign to fixed \(T_j\), LOO pool-Q bins, selection score, and optional **`empirical_530`** draws for \(A_i\) and \(T_j\) (530 CELL 5b fit).

For generic Slurm habits, `track_slurm.sh`, and Git vs rsync policy, also see:

- `sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md` (parallel 537 guide)
- `scripts/DATA_SYNC.md`

## What The Rivanna Agent Needs To Know

```text
Please run the faithful 538 Rivanna sweep.

Use:
- sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md
- sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md (Slurm mechanics reference)

Preflight: empirical_perf_fit.json must exist (530 CELL 5b).
Submit via sim_job_538.slurm or the four rivanna_*_faithful_538.slurm scripts.
Pilot first: PILOT=1 sbatch sim_job_538.slurm
Do not edit the model unless I ask.
```

Required files:

```text
sim_job_538.slurm
sports/outputs/simulation_sweeps/faithful_538_sweep.py
sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py
sports/outputs/simulation_sweeps/rivanna_stage1_faithful_538.slurm
sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_538.slurm
sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_538.slurm
sports/outputs/simulation_sweeps/rivanna_merge_faithful_538.slurm
sports/datasets/mbb/empirical_perf_fit.json
scripts/track_slurm.sh
scripts/clean_rivanna_faithful_538_sweep.sh
```

## Mac → Rivanna: Push Code

### Step 1: Sweep scripts + Slurm

```bash
./scripts/rsync_push_to_hpc.sh sweep
```

Pushes `sports/outputs/simulation_sweeps/` (538 + 537 scripts). Does **not** push HPC-generated result trees.

Dry run:

```bash
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep
```

### Step 2: Tier 1 model + empirical fit (538 only)

After **530 CELL 5b** saves `empirical_perf_fit.json` on your Mac:

```bash
./scripts/rsync_push_to_hpc.sh sweep538-deps
```

Pushes `tier1_*.py`, `sports/sports_pipeline/`, and `sports/datasets/mbb/empirical_perf_fit.json`.

Be careful: without the JSON, any grid point with `ability_draw=empirical_530` or `target_mean_dist=empirical_530` will fail on Rivanna.

## Rivanna: Preflight

From repo root (`~/Ivy_Net` or your clone):

```bash
pwd
ls sim_job_538.slurm
ls sports/outputs/simulation_sweeps/faithful_538_sweep.py
ls sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py
ls sports/outputs/simulation_sweeps/rivanna_stage1_faithful_538.slurm
ls sports/datasets/mbb/empirical_perf_fit.json
module load miniforge
~/.conda/envs/sports_net/bin/python -c "import numpy, pandas, matplotlib; print('ok')"
```

## Submit The Sweep

### One driver job (recommended)

```bash
sbatch sim_job_538.slurm
```

**Pilot grid** (~96 Stage-1 scenarios, good smoke test):

```bash
PILOT=1 sbatch sim_job_538.slurm
```

Optional env:

```bash
N_STAGE1_SHARDS=64 N_SHARDS=64 ENV_NAME=sports_net PILOT=1 sbatch sim_job_538.slurm
```

### Manual chain (same stages)

```bash
j1=$(sbatch --parsable sports/outputs/simulation_sweeps/rivanna_stage1_faithful_538.slurm)
j1m=$(sbatch --parsable --dependency=afterok:$j1 sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_538.slurm)
j2=$(sbatch --parsable --dependency=afterok:$j1m sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_538.slurm)
sbatch --dependency=afterok:$j2 sports/outputs/simulation_sweeps/rivanna_merge_faithful_538.slurm
echo "Stage 1: $j1  merge s1: $j1m  Stage 2: $j2"
```

Pilot on manual steps: prefix each `sbatch` with `PILOT=1`, e.g. `PILOT=1 sbatch ... rivanna_stage1_faithful_538.slurm`.

### Clean slate before a full re-run

On Rivanna (or Mac if you sync logs back):

```bash
./scripts/clean_rivanna_faithful_538_sweep.sh --dry-run
./scripts/clean_rivanna_faithful_538_sweep.sh --yes
```

## Track Jobs

```bash
./scripts/track_slurm.sh
squeue -u dzk3ja
tail -f slurm_out/slurm-538_stage1-*_0.out
```

538 Stage 1 uses **2 h** per array task (soft assign is heavier than 537). Stage 2 uses **6 h** per shard.

## Results On Rivanna

```bash
ls -lh sports/outputs/simulation_sweeps/rivanna_faithful_538/
ls sports/outputs/simulation_sweeps/rivanna_faithful_538/stage1_shards/ | head
```

Key outputs:

| Path | Meaning |
|------|---------|
| `rivanna_faithful_538/stage1_results.csv` | After merge-stage1 |
| `rivanna_faithful_538/grouped_candidates.csv` | After final merge |
| `rivanna_faithful_538/candidate_plots/` | Top-setting PNGs |
| `rivanna_faithful_538/README.md` | Merge summary |

## Mac: Pull Results

```bash
./scripts/rsync_pull_from_hpc.sh sweep
```

Pulls **537 and 538** result trees (not sweep `.py` sources). Optional logs:

```bash
./scripts/rsync_pull_from_hpc.sh slurm_out
```

Dry run:

```bash
DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh sweep
```

## Local Mac Test (before Rivanna)

```bash
cd sports/outputs/simulation_sweeps
python faithful_538_sweep.py --pilot --reset
```

Requires `../../datasets/mbb/empirical_perf_fit.json`.

## Grid Notes (538 vs 537)

- **Stage 1 full grid:** on the order of **~51,840** scenarios (ability/target `empirical_530`, `bin_mode` quantile vs equal_width, etc.).
- **Pilot:** **~96** Stage-1 scenarios; use `PILOT=1` on Rivanna for a fast end-to-end check.
- **Not** the 537 sort-and-chop / pool-mean bin sweep — do not mix result folders (`rivanna_faithful_537` vs `rivanna_faithful_538`).

## Troubleshooting

| Symptom | Check |
|---------|--------|
| `empirical_perf_fit.json` missing | 530 CELL 5b + `rsync_push_to_hpc.sh sweep538-deps` |
| Stage 1 tasks fail immediately | `tail slurm_out/slurm-538_stage1-*_0.err` |
| merge-stage1 row count mismatch | All Stage 1 array tasks finished? Same `N_STAGE1_SHARDS` and `PILOT` flag as Stage 1? |
| No plots after final merge | `matplotlib` in `sports_net` (merge script checks this) |
| Wrong Python | `ENV_NAME=your_env sbatch ...` |

## File Index

| Role | File |
|------|------|
| Driver | `sim_job_538.slurm` |
| Sweep logic | `faithful_538_sweep.py` |
| Shard worker | `faithful_538_sweep_rivanna_worker.py` |
| Stage 1 array | `rivanna_stage1_faithful_538.slurm` |
| Merge S1 | `rivanna_merge_stage1_faithful_538.slurm` |
| Stage 2 array | `rivanna_stage2_array_faithful_538.slurm` |
| Final merge | `rivanna_merge_faithful_538.slurm` |
| Clean outputs | `scripts/clean_rivanna_faithful_538_sweep.sh` |
| Push code | `scripts/rsync_push_to_hpc.sh sweep` |
| Push deps | `scripts/rsync_push_to_hpc.sh sweep538-deps` |
| Pull results | `scripts/rsync_pull_from_hpc.sh sweep` |
