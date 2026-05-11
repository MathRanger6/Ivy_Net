# Rivanna Faithful 537 Sweep — For Dummies

This guide runs the **faithful 537 simulation sweep** on Rivanna. “Faithful” means it uses the current `537_Sports_Simulation.ipynb` mechanics only: no new congestion or opportunity penalty terms.

## Do I Run The Stage Files In Succession?

Yes. The stages depend on each other:

1. **Stage 1** runs a broad screen and writes `stage1_results.csv`.
2. **Stage 2** reads `stage1_results.csv`, then runs a Slurm array to verify candidate settings across seeds.
3. **Merge** reads all Stage 2 shard files and creates the final ranked candidate table and plots.

The easiest way is to submit them with Slurm dependencies, so each starts only after the prior stage finishes successfully.

## Start In Cursor On Rivanna

Open Rivanna using `Rivanna.code-workspace`.

In the Rivanna terminal, go to the repo root, meaning the folder that contains `sports/`, `scripts/`, and `pipe_job.slurm`.

```bash
cd ~/Ivy_Net
```

If your repo is somewhere else on Rivanna, `cd` there instead.

## Submit The Whole Chain

From the repo root:

```bash
j1=$(sbatch --parsable sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm)
j2=$(sbatch --parsable --dependency=afterok:$j1 sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm)
sbatch --dependency=afterok:$j2 sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```

That submits:

- Stage 1 as one job.
- Stage 2 as a 64-task array.
- Merge as one final job after all Stage 2 tasks succeed.

## Monitor Progress

Use the existing tracker:

```bash
./scripts/track_slurm.sh
```

Or check the queue:

```bash
squeue -u dzk3ja
```

Or tail logs directly:

```bash
tail -f slurm-537_stage1-*.out
tail -f slurm-537_stage2-*.out
tail -f slurm-537_merge-*.out
```

Press `Ctrl+C` to stop watching a log. That does **not** cancel the job.

To cancel a job:

```bash
scancel JOBID
```

## Where Results Land

Rivanna outputs land here:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/
```

Important files after completion:

```text
stage1_results.csv
stage2_results_merged.csv
grouped_candidates.csv
candidate_plots/
README.md
```

The file to inspect first is:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/grouped_candidates.csv
```

Look for rows where:

```text
moderate_stable = True
```

That means the setting produced a stable moderate right-side downturn under the rule we chose.

## Syncing Between Mac And Rivanna

The rsync shortcut `all` now includes:

```text
sports/outputs/simulation_sweeps
```

Push code/scripts to Rivanna:

```bash
./scripts/rsync_push_to_hpc.sh all
```

Pull results back to your Mac:

```bash
./scripts/rsync_pull_from_hpc.sh sports/outputs/simulation_sweeps
```

Generated results are gitignored, but rsync can still move them.

## Can I Delete The Old Local Results File?

Yes. The old local file:

```text
sports/outputs/simulation_sweeps/faithful_537_sweep_results.jsonl
```

came from the aborted local run. It is safe to delete if you are switching to the Rivanna run.

The Rivanna run writes new outputs under:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/
```

## Common Problems

### `stage1_results.csv` missing

Stage 2 needs Stage 1 output. Run Stage 1 first, or use the dependency chain above.

### `sports_net` not found

The Slurm scripts default to:

```bash
ENV_NAME="${ENV_NAME:-sports_net}"
```

If your Rivanna env has a different name:

```bash
ENV_NAME=my_env_name sbatch sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
```

Do the same for Stage 2 and Merge.

### I changed the number of shards

If you edit Stage 2 from 64 shards to another number, make the Slurm array and `N_SHARDS` match.

For example, 128 shards:

```bash
#SBATCH --array=0-127
N_SHARDS=128 sbatch sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
N_SHARDS=128 sbatch sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```
