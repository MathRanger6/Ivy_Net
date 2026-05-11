# Rivanna Runbook — Faithful 537 Sweep

These files run the faithful `537_Sports_Simulation` parameter sweep as a
Slurm job array, without adding any new mechanisms.

## Files

- `faithful_537_sweep.py` — original local/staged sweep.
- `faithful_537_sweep_rivanna_worker.py` — Rivanna stage/array worker.
- `rivanna_stage1_faithful_537.slurm` — run broad Stage 1 once.
- `rivanna_stage2_array_faithful_537.slurm` — run Stage 2 verification as 64 shards.
- `rivanna_merge_faithful_537.slurm` — merge shard outputs and make ranked candidates/plots.

## Rivanna / Slurm Conventions

These scripts now mirror the repo-level `pipe_job.slurm` conventions:

- `#SBATCH --account=sds_ag`
- `#SBATCH --mail-user=dzk3ja@virginia.edu`
- `#SBATCH --constraint=rivanna`
- `module load miniforge`
- `ENV_NAME="${ENV_NAME:-sports_net}"`
- line-buffered stdout/stderr via `stdbuf` when available

If Rivanna’s module name differs, edit:

```bash
module load miniforge
```

The scripts first try:

```bash
$HOME/.conda/envs/sports_net/bin/python
```

and fall back to `python` on PATH.

## Submit From Repo Root

On Rivanna, `cd` to the repository root (the directory containing `sports/`), then:

```bash
sbatch sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
```

When Stage 1 finishes:

```bash
sbatch sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
```

When all Stage 2 array tasks finish:

```bash
sbatch sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```

Optional dependency style:

```bash
j1=$(sbatch --parsable sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm)
j2=$(sbatch --parsable --dependency=afterok:$j1 sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm)
sbatch --dependency=afterok:$j2 sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```

## Outputs

All outputs land under:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/
```

Important outputs:

- `stage1_results.csv`
- `stage2_shards/stage2_shard_*.csv`
- `stage2_results_merged.csv`
- `grouped_candidates.csv`
- `candidate_plots/`
- `README.md`

## Shards

Default Stage 2 array is 64 tasks:

```bash
#SBATCH --array=0-63
N_SHARDS="${N_SHARDS:-64}"
```

If you change the array range, set `N_SHARDS` to match. Example for 128 shards:

```bash
#SBATCH --array=0-127
N_SHARDS="${N_SHARDS:-128}"
```

Then submit with:

```bash
N_SHARDS=128 sbatch sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
```
