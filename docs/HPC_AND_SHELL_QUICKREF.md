# HPC & shell quick reference (Ivy_Net)

**Purpose:** One page of copy-paste commands and “gotchas” we hit often in chat.  
**Depth lives elsewhere** — follow links when you need full procedures.

| Topic | Long-form doc |
|-------|----------------|
| Git recipes (stash, rebase, recovery) | [`GIT_FOR_DUMMIES.md`](./GIT_FOR_DUMMIES.md) |
| Git mental model (Mac / HPC / GitHub) | [`GIT_MULTIPLE_MACHINES_ELEMENTARY.md`](./GIT_MULTIPLE_MACHINES_ELEMENTARY.md) |
| rsync, gitignore, what to pull/push | [`scripts/DATA_SYNC.md`](../scripts/DATA_SYNC.md) |
| Slurm logs, `tail -f`, `track_slurm.sh` | [`tenure/HPC_SLURM_PIPELINE_GUIDE.md`](../tenure/HPC_SLURM_PIPELINE_GUIDE.md) |
| Faithful **537** sweep on Rivanna | [`sports/documents/RIVANNA_RUNBOOK.md`](../sports/documents/RIVANNA_RUNBOOK.md) |
| Faithful **537** step-by-step | [`sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md`](../sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md) |
| Faithful **538** sweep | [`sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md`](../sports/documents/Rivanna_Faithful_538_Sweep_For_Dummies.md) |
| Doc index | [`README.md`](./README.md) |

**Convention:** Run Slurm and helper scripts from the **Ivy_Net repo root** (directory containing `sports/`, `tenure/`, `scripts/`, `sim_job.slurm`).

---

## 1. Two-second health checks

### Git

```bash
cd ~/Ivy_Net
git status -sb
git branch -vv
```

| Status line | Meaning |
|-------------|---------|
| `[behind N]` | Run `git pull origin main` (or merge/rebase) before building on old code. |
| `[ahead N]` | Local commits not on GitHub yet — `git push` when ready. |
| `M` / `??` | Uncommitted work — commit, stash, or discard before switching branches. |

### Rivanna queue

```bash
squeue -u $USER
```

### Matplotlib (same Python Slurm uses for sweep merge/plots)

```bash
"$HOME/.conda/envs/sports_net/bin/python" -c "import matplotlib; print(matplotlib.__version__)"
```

If that fails, merge jobs that write `candidate_plots/` will fail or skip plots — install in **`sports_net`**, not only in an interactive notebook kernel.

---

## 2. Git — daily habit

```bash
cd ~/Ivy_Net
git pull origin main
# … edit …
git add <paths-you-mean>     # prefer explicit paths over blind `git add .`
git commit -m "Short description"
git push origin main
```

**Normal `git push` does not overwrite GitHub `main`.** Only `git push --force` (avoid on shared `main`) replaces remote history.

---

## 3. Git — local changes + need to sync

### Uncommitted edits, origin moved

```bash
git stash push -u -m "WIP before sync"
git pull --rebase origin main
git stash pop
```

### On a feature branch; bring in latest `main`

```bash
git fetch origin
git merge origin main
# fix conflicts if any, then git add … && git merge --continue
```

### Preview merge conflicts (optional)

After you have committed locally:

```bash
git fetch origin
git merge origin/main --no-commit --no-ff
# inspect: git status, git diff
git merge --abort    # bail out without keeping the merge
```

---

## 4. Git — leave a branch, work on `main`

```bash
git switch main
git pull origin main
```

If the branch’s work should stay in history, **merge or PR first**:

```bash
git switch main
git merge local-sweep-fixes
git push origin main
```

### Delete the local branch

After merge into current branch:

```bash
git branch -d local-sweep-fixes
```

If Git refuses (`not fully merged` vs **remote** tracking branch) but **`main` already has your commits**:

```bash
git branch -D local-sweep-fixes
```

Optional remote cleanup:

```bash
git push origin --delete local-sweep-fixes
```

---

## 5. Git — accidental `chmod +x` on text files

Broad `chmod +x` on a folder can mark `.md` / `.txt` as executable. Git then shows **mode-only** diffs (`100644 → 100755`), not content changes.

```bash
chmod 644 scripts/DATA_SYNC.md scripts/requirements-notebook-mcp.txt
git status    # should be clean if only mode noise
```

At `git add -p`, type **`n`** for “Stage mode change?” on markdown unless you really want `+x`.

---

## 6. Slurm — submit jobs (not `bash job.slurm`)

Slurm scripts use **`${SLURM_SUBMIT_DIR}`**. Submit from repo root:

```bash
cd ~/Ivy_Net
sbatch sim_job.slurm          # Faithful 537 full pipeline
sbatch sim_job_538.slurm      # Faithful 538 full pipeline
sbatch pipe_job.slurm         # Tenure 540 papermill pipeline
```

Running `./sim_job.slurm` directly (without `sbatch`) often breaks under `set -u` because `SLURM_SUBMIT_DIR` is unset.

---

## 7. Slurm — monitor and cancel

```bash
squeue -u $USER
tail -f slurm_out/slurm-sim_job-<JOBID>.out
tail -f slurm_out/slurm-sim_job-<JOBID>.err
```

Helper (follow latest or a specific job’s `.err`):

```bash
./scripts/track_slurm.sh
./scripts/track_slurm.sh <JOBID>
```

Cancel:

```bash
scancel <JOBID>
```

**`.err` is not “errors only”** — tqdm and many libraries log progress there even when the job succeeds.

---

## 8. Clean logs vs clean sweep outputs

| Script | What it removes |
|--------|-----------------|
| `./scripts/clear_slurm.sh` | **All** `slurm_out/slurm-*` logs (and legacy root `slurm-*`) |
| `./scripts/clean_rivanna_faithful_537_sweep.sh --dry-run` | Lists 537 sweep tree + 537/sim_job logs only |
| `./scripts/clean_rivanna_faithful_537_sweep.sh --yes` | Deletes `rivanna_faithful_537/` + related logs |
| `… --yes --slurm-all` | Above + runs `clear_slurm.sh` |

538 has an analogous clean script — [`scripts/clean_rivanna_faithful_538_sweep.sh`](../scripts/clean_rivanna_faithful_538_sweep.sh) (same `--dry-run` / `--yes` pattern).

Typical **fresh 537 run** on Rivanna:

```bash
./scripts/clean_rivanna_faithful_537_sweep.sh --dry-run
./scripts/clean_rivanna_faithful_537_sweep.sh --yes
sbatch sim_job.slurm
```

---

## 9. Mac ↔ Rivanna sync (not Git)

Sweep **results** and Slurm logs are **gitignored**. Use rsync, not `git add`.

```bash
# Mac → Rivanna (sweep code only; not generated results)
./scripts/rsync_push_to_hpc.sh sweep

# Rivanna → Mac (results + logs)
./scripts/rsync_pull_from_hpc.sh sweep
./scripts/rsync_pull_recent_hpc.sh quick

# Preview
DRY_RUN=1 ./scripts/rsync_pull_from_hpc.sh sweep
```

After **code** changes on Mac: **`git push`**, then on Rivanna **`git pull`** in the same repo path **before** the next `sbatch`.  
`rsync_push sweep` does **not** sync repo-root `sim_job.slurm` — use Git for that file.

Details: [`scripts/DATA_SYNC.md`](../scripts/DATA_SYNC.md).

---

## 10. Faithful sweep outputs (537 / 538)

| Artifact | Path |
|----------|------|
| 537 merged Stage 2 | `sports/outputs/simulation_sweeps/rivanna_faithful_537/stage2_results_merged.csv` |
| 537 grouped ranking | `…/rivanna_faithful_537/grouped_candidates.csv` |
| 537 candidate plots | `…/rivanna_faithful_537/candidate_plots/` |
| 538 (same layout) | `…/rivanna_faithful_538/` |

**Not** `sports/outputs/simulation_sweeps/candidate_plots/` at the sweep root — Rivanna merge writes under **`rivanna_faithful_537/`** (or `_538/`).

Plots are created only in the **final merge** Slurm step (`537_merge` / `538_merge`). Check that job’s log for:

- `==> candidate_plots: N PNG(s) -> …`
- or `skipping candidate_plots/ — matplotlib is not installed`

---

## 11. 537 notebook Cell 10 vs sweep CSV (knob alignment)

- **Cell 10 widgets are authoritative** for the playground plot; `sim_config.py` is defaults only — use **Load defaults from sim_config.py** after editing config.
- **Promotions per run (K)** and **Pools (#)** are widget sliders (not hidden in config only).
- **Pool–talent bins (#)** is aggregation bin count — do not confuse with promotions **K**.
- Faithful sweep PNG titles use the same labels as Cell 10 via **`sports/cell10_knob_catalog.py`**.

To reproduce a sweep row in the notebook: match widget labels to `grouped_candidates.csv`, set **Binning → Pools: equal pool count**, and align **K**, **Pools (#)**, **Runs**, **N**, **Pool–talent bins (#)** with the CSV row.

Operator detail: [`sports/documents/537_Manual.md`](../sports/documents/537_Manual.md).

---

## 12. Common failure modes (from recent sessions)

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `SLURM_SUBMIT_DIR` / `set -u` error | Ran `.slurm` with bash instead of `sbatch` | `cd ~/Ivy_Net && sbatch sim_job.slurm` |
| No `candidate_plots/` after “successful” run | Merge never ran, or matplotlib missing in `sports_net` | Check `slurm-*_merge-*.err`; install matplotlib in Slurm env |
| Empty `candidate_plots/` folder, 0 PNGs | `grouped` empty or type mismatch in plot loop | Check merge `.out`; ensure consistent Stage 2 schema |
| `git pull` blocked | Uncommitted changes | Commit, stash, or discard |
| `git branch -d` refused | Branch not pushed / not merged to remote tracking ref | Use `-D` if `main` already has the commits |
| Git shows diff with **0 insertions** | File mode `755` vs `644` only | `chmod 644 <file>` |
| Old sweep rows after code change | Mixed shard CSVs from prior run | Run clean script, full re-`sbatch` |
| Merge `ValueError: Length of ascending …` (538) | Bug in `grouped_candidates` sort columns | Fix sweep code; re-run merge after patch |

---

## 13. Environment on Rivanna

```bash
module load miniforge
conda activate sports_net   # or ENV_NAME=… on sbatch line
```

Slurm jobs use **`$HOME/.conda/envs/${ENV_NAME:-sports_net}/bin/python`**, not necessarily the kernel you use in Cursor Remote SSH.

Override for one submission:

```bash
ENV_NAME=sports_net N_STAGE1_SHARDS=64 N_SHARDS=64 sbatch sim_job.slurm
```

---

## 14. Where to add new snippets

When a command keeps coming up in chat:

1. Add a **one-line entry** to the table in §12 or a new § if it’s a new category.
2. Put **full procedures** in the domain runbook (`RIVANNA_RUNBOOK.md`, `DATA_SYNC.md`, etc.) and **link** from here — avoid maintaining two long copies of the same checklist.
