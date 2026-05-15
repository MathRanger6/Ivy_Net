# Rivanna Faithful 537 Sweep — For Dummies

This guide runs the **faithful 537 simulation sweep** on Rivanna. “Faithful” means it uses the current `537_Sports_Simulation.ipynb` mechanics only: no new congestion or opportunity penalty terms.

## What The Rivanna Agent Needs To Know

If you open a fresh Cursor window on Rivanna, tell the agent:

```text
Please run the faithful 537 Rivanna sweep.

Use these docs:

- `sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md` (step-by-step)
- `sports/documents/RIVANNA_RUNBOOK.md` (Slurm reference, **clean slate script**, **fresh-run checklist**, `sim_job.slurm`)

First do the preflight checks in the Dummies guide.
Then submit Stage 1 array, Merge Stage 1, Stage 2 array, and final merge with Slurm dependencies.
Track the jobs with scripts/track_slurm.sh and squeue.
Do not edit the model unless I ask.
```

The required files are:

```text
sports/outputs/simulation_sweeps/faithful_537_sweep.py
sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py
sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm
sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
scripts/track_slurm.sh
scripts/clear_slurm.sh
```

## For This Sweep: The Simple Step-By-Step

### Step 1: On The Mac, Push Only The Sweep Files

Do:

```bash
./scripts/rsync_push_to_hpc.sh sweep
```

Because: Rivanna needs the sweep Python scripts, Slurm scripts, and this guide before the jobs can run.

Be careful of: do **not** use `./scripts/rsync_push_to_hpc.sh all` for this sweep. That broad sync can touch unrelated project folders.

In case of trouble: run a dry run first:

```bash
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep
```

The dry run should mention `sports/outputs/simulation_sweeps/`, not `python_packages/dblp-parser` or `tenure/tenure_pipeline`.

### Step 2: Open Cursor On Rivanna And Go To The Repo

Do:

```bash
cd ~/Ivy_Net
```

Because: the Slurm scripts assume you submit from the repo root, where `sports/`, `scripts/`, and `pipe_job.slurm` live. Stdout/stderr logs go to **`slurm_out/`** here (e.g. `~/Ivy_Net/slurm_out/slurm-*.out`).

Be careful of: if your Rivanna repo is not at `~/Ivy_Net`, use the actual repo path.

In case of trouble: check where you are:

```bash
pwd
ls sports scripts pipe_job.slurm
```

### Step 3: Run The Preflight Checks

Do:

```bash
ls sports/outputs/simulation_sweeps/faithful_537_sweep.py
ls sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py
ls sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
ls scripts/track_slurm.sh
module load miniforge
~/.conda/envs/sports_net/bin/python --version
```

Because: this catches missing files or environment problems before submitting a multi-hour job chain.

Be careful of: if `sports_net` is missing, the scripts may fall back to another Python. That might work, but only if it has `numpy` and `pandas`.

In case of trouble: either fix the environment on Rivanna or submit with a different env name, for example:

```bash
ENV_NAME=my_env_name sbatch sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
```

### Step 4: Submit Stage 1 Array, Stage 1 Merge, Stage 2 Array, Final Merge

**One submission (like `pipe_job.slurm`):** From the **Ivy_Net repo root**, if `sim_job.slurm` is present (see runbook), you can run the full dependency chain with:

```bash
sbatch sim_job.slurm
```

Optional: `N_STAGE1_SHARDS=64 N_SHARDS=64 ENV_NAME=sports_net sbatch sim_job.slurm`. The driver job holds a long wall time while it `sbatch --wait`s each child step.

**Manual chain (equivalent):**

Do:

```bash
j1=$(sbatch --parsable \
  sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm)

j1m=$(sbatch --parsable --dependency=afterok:$j1 \
  sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm)

j2=$(sbatch --parsable --dependency=afterok:$j1m \
  sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm)

sbatch --dependency=afterok:$j2 \
  sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm

echo "Stage 1 array: $j1"
echo "Stage 1 merge: $j1m"
echo "Stage 2 array: $j2"
```

**How to enter Step 4 (terminal mechanics):**

1. Use a **bash** shell on Rivanna (the default login shell is usually fine).
2. **`cd`** to **Ivy_Net repo root** first (same as Step 2), so paths like `sports/outputs/...` exist.
3. Copy the **whole block** above and paste it once. Lines ending in `\` mean “continued on the next line”; the shell runs it as one multi-line command sequence. Press **Enter** after the last line (`echo "Stage 2 array: $j2"`).
4. What it does:
   - **`sbatch --parsable`** prints **only the numeric job ID** (no extra words), so it can be stored in **`j1`** / **`j1m`** / **`j2`**.
   - **`--dependency=afterok:JOBID`** tells Slurm: start this job only after that job **finishes with exit code 0**. For **Stage 1**, `JOBID` is the array **job id**; Slurm waits until **all** array tasks finish successfully before starting Stage 1 merge.
5. The **final merge** job is submitted by the fourth `sbatch` line; Slurm prints its job ID on that line.

Same logic **without** line breaks (easier to type line-by-line):

```bash
j1=$(sbatch --parsable sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm)
j1m=$(sbatch --parsable --dependency=afterok:$j1 sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm)
j2=$(sbatch --parsable --dependency=afterok:$j1m sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm)
sbatch --dependency=afterok:$j2 sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
echo "Stage 1 array: $j1"
echo "Stage 1 merge: $j1m"
echo "Stage 2 array: $j2"
```

**Shard counts:** Stage 1 defaults to **64** tasks (`N_STAGE1_SHARDS`). If you change `#SBATCH --array=0-63` to another range, set the same count when submitting merge, e.g. `N_STAGE1_SHARDS=128 sbatch ... rivanna_merge_stage1_faithful_537.slurm`. Stage 2 still uses **`N_SHARDS`** (default 64) in `rivanna_stage2_array_faithful_537.slurm` and `rivanna_merge_faithful_537.slurm`.

Because: Stage 1 now runs as a **parallel array**; each shard does about **1/64** of the old single-core Stage 1 work (typically **a few minutes to tens of minutes** per task, not ~1.5 hours). **Merge Stage 1** builds a single `stage1_results.csv`. Stage 2 needs that file. The **final merge** needs all Stage 2 shard CSVs.

Be careful of: do not submit Stage 2 until `stage1_results.csv` exists. Do not submit **merge-stage1** before all Stage 1 array tasks finish.

**Single-node Stage 1 (legacy, not Slurm array):** from repo root, `python sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py stage1 --reset` writes `stage1_results.csv` directly (debug / small tests only).

In case of trouble: check the queue:

```bash
squeue -u dzk3ja
```

### Step 5: Track The Jobs

Do:

```bash
./scripts/track_slurm.sh
squeue -u dzk3ja
```

Because: `track_slurm.sh` tails the latest Slurm error log, while `squeue` shows whether the jobs are queued, running, or finished.

Be careful of: `Ctrl+C` only stops watching a log. It does not cancel the Slurm job.

In case of trouble: cancel a bad job only if needed:

```bash
scancel JOBID
```

### Step 6: Check Results On Rivanna

Do:

```bash
ls -lh sports/outputs/simulation_sweeps/rivanna_faithful_537/
ls sports/outputs/simulation_sweeps/rivanna_faithful_537/stage1_shards/ | head
ls sports/outputs/simulation_sweeps/rivanna_faithful_537/stage2_shards/ | head
```

Because: the final results should land under `rivanna_faithful_537/`, with merged candidate files and plots. While Stage 1 is running you should see **`stage1_shards/stage1_shard_*_of_0064.csv`** accumulating; after **Merge Stage 1**, **`stage1_results.csv`** appears at the top level of that folder.

Be careful of: if **`stage1_shards/`** never fills, Stage 1 array tasks may still be queued. If **`stage1_results.csv`** is missing after merge, check **`slurm_out/slurm-537_merge_s1-*.out`**. If **`stage2_shards/`** is empty, Stage 2 probably has not started, failed early, or is still queued.

In case of trouble: inspect the relevant Slurm logs:

```bash
tail -f slurm_out/slurm-537_stage1-*_0.out
tail -f slurm_out/slurm-537_merge_s1-*.out
tail -f slurm_out/slurm-537_stage2-*_0.out
tail -f slurm_out/slurm-537_merge-*.out
```

### Step 7: On The Mac, Pull Only The Sweep Results Back

Do:

```bash
./scripts/rsync_pull_from_hpc.sh sweep
```

Optional: pull **sweep results and** Rivanna **`slurm_out/`** logs in one go (useful for Cursor on your Mac):

```bash
./scripts/rsync_pull_recent_hpc.sh quick
```

Full **Git vs rsync** reference: `scripts/DATA_SYNC.md`.

Because: this brings back generated sweep results without using Git and without pulling source code back from Rivanna over your local edits.

Be careful of: do **not** use `./scripts/rsync_pull_from_hpc.sh all` for this sweep.

In case of trouble: dry run first:

```bash
DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh sweep
```

### Step 8: Inspect The Candidate File

Do:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/grouped_candidates.csv
```

Because: this is the first file to inspect for stable right-side downturn candidates.

Be careful of: one lucky seed is not enough. Look for rows where the grouped/stability columns show the downturn repeats across seeds.

In case of trouble: open:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/README.md
```

That file should summarize what the merge step found.

## Do I Run The Stage Files In Succession?

Yes. The stages depend on each other:

1. **Stage 1** runs as a **Slurm array** of shards; each task writes a CSV under `rivanna_faithful_537/stage1_shards/`.
2. **Merge Stage 1** concatenates those shards into **`stage1_results.csv`** (exact row count is validated).
3. **Stage 2** reads `stage1_results.csv`, then runs a Slurm array to verify candidate settings across seeds.
4. **Final merge** reads all Stage 2 shard files and creates the ranked **`grouped_candidates.csv`** and plots.

The easiest way is to submit them with Slurm dependencies, so each starts only after the prior step finishes successfully.

## Start In Cursor On Rivanna

Open Rivanna using `Rivanna.code-workspace`.

In the Rivanna terminal, go to the repo root, meaning the folder that contains `sports/`, `scripts/`, and `pipe_job.slurm`.

```bash
cd ~/Ivy_Net
```

If your repo is somewhere else on Rivanna, `cd` there instead.

## Preflight Checks On Rivanna

Before submitting, run these from the repo root:

```bash
pwd
ls sports/outputs/simulation_sweeps/faithful_537_sweep.py
ls sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py
ls sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
ls sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
ls scripts/track_slurm.sh
```

Check that Rivanna can see Python in the `sports_net` environment:

```bash
module load miniforge
~/.conda/envs/sports_net/bin/python --version
```

If that path does not exist, find Python with:

```bash
which python
```

The Slurm scripts will fall back to `command -v python`, but the preferred environment is `sports_net`.

Optional quick import check:

```bash
~/.conda/envs/sports_net/bin/python - <<'PY'
import numpy, pandas
print("numpy", numpy.__version__)
print("pandas", pandas.__version__)
try:
    import matplotlib
    print("matplotlib", matplotlib.__version__)
except ModuleNotFoundError:
    print("matplotlib missing; numeric sweep can still run, plots may be skipped")
PY
```

If files are missing on Rivanna, go back to the Mac Cursor window and push only the sweep folder:

```bash
./scripts/rsync_push_to_hpc.sh sweep
```

Do **not** use `./scripts/rsync_push_to_hpc.sh all` for this sweep. The `all` shortcut is a broad project sync and includes unrelated folders such as `python_packages/dblp-parser`.

## Submit The Whole Chain

From the repo root (same **four-step** dependency chain as Step 4):

```bash
j1=$(sbatch --parsable \
  sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm)

j1m=$(sbatch --parsable --dependency=afterok:$j1 \
  sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm)

j2=$(sbatch --parsable --dependency=afterok:$j1m \
  sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm)

sbatch --dependency=afterok:$j2 \
  sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```

That submits:

- **Stage 1** as a **64-task array** (shard CSVs under `stage1_shards/`).
- **Merge Stage 1** → **`stage1_results.csv`**.
- **Stage 2** as a 64-task array (unless you changed `N_SHARDS`).
- **Final merge** after all Stage 2 tasks succeed.

Print the job IDs so you can track them:

```bash
echo "Stage 1 array: $j1"
echo "Stage 1 merge: $j1m"
echo "Stage 2 array: $j2"
```

The final merge job ID is printed by the last `sbatch` command.

## Monitor Progress

Use the existing tracker:

```bash
./scripts/track_slurm.sh
```

With no argument, it tails the most recent `slurm_out/slurm-*.err` file (or a legacy repo-root `slurm-*.err`). With a job ID, it tails that job's `.err` file:

```bash
./scripts/track_slurm.sh JOBID
```

Or check the queue:

```bash
squeue -u dzk3ja
```

Or tail logs directly. **Stage 1** is an array job (one log per task). **Merge Stage 1** job name is **`537_merge_s1`**.

```bash
tail -f slurm_out/slurm-537_stage1-*_0.out
tail -f slurm_out/slurm-537_merge_s1-*.out
```

**Final merge** (Stage 2 outputs):

```bash
tail -f slurm_out/slurm-537_merge-*.out
```

Stage 2 is an array job, so it writes one log per array task:

```bash
tail -f slurm_out/slurm-537_stage2-*_0.out
tail -f slurm_out/slurm-537_stage2-*_0.err
```

Press `Ctrl+C` to stop watching a log. That does **not** cancel the job.

To cancel a job:

```bash
scancel JOBID
```

To clean old Slurm logs before a new run:

```bash
./scripts/clear_slurm.sh
```

Use that only if you no longer need the old logs.

## Where Results Land

Rivanna outputs land here:

```text
sports/outputs/simulation_sweeps/rivanna_faithful_537/
```

Important files after completion:

```text
stage1_shards/stage1_shard_*.csv
stage1_results.csv
stage2_shards/stage2_shard_*.csv
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

That means the setting produced a **stable inverted-U** shape under the sweep rule: interior peak, both endpoints below the peak, and mean left-side and right-side drops from the peak each at least 5%, on ≥60% of seeds.

During the run, quick progress checks:

```bash
ls -lh sports/outputs/simulation_sweeps/rivanna_faithful_537/
ls sports/outputs/simulation_sweeps/rivanna_faithful_537/stage1_shards/ | head
ls sports/outputs/simulation_sweeps/rivanna_faithful_537/stage2_shards/ | head
```

## Syncing Between Mac And Rivanna

The rsync shortcut for this job is:

```text
sweep
```

Push code/scripts to Rivanna:

```bash
./scripts/rsync_push_to_hpc.sh sweep
```

Pull results back to your Mac:

```bash
./scripts/rsync_pull_from_hpc.sh sweep
```

Generated results are gitignored, but rsync can still move them.

Important safety rule:

- Use `./scripts/rsync_push_to_hpc.sh sweep` to send sweep code/scripts to Rivanna.
- Use `./scripts/rsync_pull_from_hpc.sh sweep` to bring generated sweep results back.
- Do **not** use broad `all` syncs for the sweep run.
- Use `DRY_RUN=1` before a sync when unsure:

```bash
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep
DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh sweep
```

Rsync does not know Git history. The sweep shortcut is intentionally directional: push excludes generated results, and pull brings back generated results only so it does not overwrite sweep source code on the Mac.

## If I Accidentally Ran A Broad Sync

If you accidentally ran:

```bash
./scripts/rsync_push_to_hpc.sh all
```

and it started pushing unrelated files, stop it with `Ctrl+C`.

For this sweep, `all` is not the right command. Use:

```bash
./scripts/rsync_push_to_hpc.sh sweep
```

The warning below is from SSH and is not the immediate problem:

```text
WARNING: connection is not using a post-quantum key exchange algorithm.
```

The real problem is that `all` can sync unrelated project trees. We specifically do not want accidental DBLP XML pushes or broad code/data overwrites while preparing this sweep.

### On Rivanna: Check For A Partial DBLP Transfer

If the accidental sync reached `dblp.xml` and you interrupted it, check Rivanna for partial temp files:

```bash
ls -lh ~/Ivy_Net/python_packages/dblp-parser/dblp.xml* \
  ~/Ivy_Net/python_packages/dblp-parser/.dblp.xml* \
  2>/dev/null
```

Normal `rsync` usually writes a hidden temporary file first and renames it only after a successful transfer. That means interrupting usually does **not** replace the existing remote `dblp.xml`, but it can leave a hidden partial temp file.

If you see a hidden temp file like `.dblp.xml.*`, remove only that temp file:

```bash
rm -f ~/Ivy_Net/python_packages/dblp-parser/.dblp.xml*
```

Do **not** delete the real `dblp.xml` unless you intentionally want to remove the full DBLP dump.

### On The Mac: Use Dry Runs Before Syncing

Before pushing or pulling when unsure:

```bash
DRY_RUN=1 ./scripts/rsync_push_to_hpc.sh sweep
DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh sweep
```

The dry run should show only:

```text
sports/outputs/simulation_sweeps/
```

If it shows `python_packages/dblp-parser`, `tenure/tenure_pipeline`, or another unrelated tree, stop and do not run the real command.

### Git vs Rsync Mental Model

Use Git for code and history. Use rsync for generated data/results.

Git understands commits, branches, and conflict detection. Rsync only compares files and paths. It can overwrite a newer local file with a remote file if you ask it to pull that path. That is why the sweep pull command is intentionally narrow: it pulls generated sweep outputs only and avoids pulling sweep source code back from Rivanna.

Safe commands for this sweep:

```bash
./scripts/rsync_push_to_hpc.sh sweep
./scripts/rsync_pull_from_hpc.sh sweep
```

Avoid for this sweep:

```bash
./scripts/rsync_push_to_hpc.sh all
./scripts/rsync_pull_from_hpc.sh all
```

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

Stage 2 needs **`stage1_results.csv`**. With the array workflow: (**1**) wait until **all** Stage 1 array tasks finish, (**2**) run **`rivanna_merge_stage1_faithful_537.slurm`** (or use the full dependency chain in Step 4). If merge fails, check **`slurm_out/*.err`** and that **`stage1_shards/`** contains **`stage1_shard_*_of_NNNN.csv`** for every shard.

If you change **`N_STAGE1_SHARDS`**, you must update **`#SBATCH --array=...`** in **`rivanna_stage1_faithful_537.slurm`** and pass the **same** value to the merge script.

### `merge-stage1` fails with wrong row count

Some Stage 1 tasks may have failed or **`N_STAGE1_SHARDS`** does not match the Slurm array. Fix failed tasks or remove stale shard CSVs and re-run Stage 1 + merge.

### `sports_net` not found

The Slurm scripts default to:

```bash
ENV_NAME="${ENV_NAME:-sports_net}"
```

If your Rivanna env has a different name:

```bash
ENV_NAME=my_env_name sbatch \
  sports/outputs/simulation_sweeps/rivanna_stage1_faithful_537.slurm
```

Do the same for **Merge Stage 1**, Stage 2 array, and the **final merge** if you submit those jobs separately.

### I changed the Stage 1 shard count

If you edit **`rivanna_stage1_faithful_537.slurm`** so the array is not `0-63`, set **`N_STAGE1_SHARDS`** to the same task count when submitting **`rivanna_merge_stage1_faithful_537.slurm`**:

```bash
N_STAGE1_SHARDS=128 sbatch \
  sports/outputs/simulation_sweeps/rivanna_merge_stage1_faithful_537.slurm
```

### I changed the number of Stage 2 shards

If you edit Stage 2 from 64 shards to another number, make the Slurm array and `N_SHARDS` match.

For example, 128 shards:

```bash
#SBATCH --array=0-127
N_SHARDS=128 sbatch \
  sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_537.slurm
N_SHARDS=128 sbatch \
  sports/outputs/simulation_sweeps/rivanna_merge_faithful_537.slurm
```
