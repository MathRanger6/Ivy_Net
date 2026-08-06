# Rivanna notebook pipeline (Ivy_Net / tenure)

**Maintainer:** Charles (Ivy_Net / tenure pipeline).

Production batch launcher: **`pipe_job.slurm`** at the **Ivy_Net repo root** (runs **`tenure/540_tenure_pipeline.ipynb`** via **`papermill`**). Submit with **`cd ~/Ivy_Net && sbatch pipe_job.slurm`**.

**Collaborator note:** A generic Slurm + notebook starter for an external colleague was delivered as a **standalone zip** and is **not** versioned in this repository anymore.

---

## Reading logs without assuming Linux fluency

Slurm writes plain-text **log files** under **`slurm_out/`** relative to the directory you were in when you typed **`sbatch`** (for **`~/Ivy_Net`**, that is **`~/Ivy_Net/slurm_out/`**). **`tail -f`** reads those files like “streaming Notepad.”

### What is a JOBID?

When you **`sbatch`** **`pipe_job.slurm`**, Slurm replies with something like **`Submitted batch job 11807601`**. That number is the **job ID**. It appears in log filenames so each run stays separate.

### Two streams: `.out` vs `.err` (NOT “error-only”)

| Stream | Filename pattern | Typical contents |
|--------|------------------|------------------|
| **stdout** | **`slurm_out/slurm-<job_name>-<JOBID>.out`** | **`echo`** lines from the batch script, many **`print()`** statements from Python. |
| **stderr** | **`slurm_out/slurm-<job_name>-<JOBID>.err`** | Progress bars (**tqdm**), warnings, status lines — lots of Jupyter stacks write here **even when nothing failed.** |

So **`.err` is often where you see motion first**, not necessarily because anything broke.

### What does `tail` do? What does `tail -f` do?

- **`tail slurm_out/slurm-pipe_job-11807601.err`** shows only the **last ~10 lines** of that file — snapshot.
- **`tail -f`** (**follow**) keeps the terminal **attached**: whenever Slurm appends another line to that file on disk, your terminal prints it immediately — **near-live monitoring** while the compute node runs your notebook.

Stop watching with **Ctrl+C**. That **only stops tail**; it does **not** stop the Slurm job.

### Helper script: **`scripts/track_slurm.sh`**

From the **repo root**:

```bash
chmod +x scripts/track_slurm.sh    # once
./scripts/track_slurm.sh             # most recent .err under slurm_out/ (or legacy repo root)
./scripts/track_slurm.sh 11807601    # .err for that job ID
```

It looks in **`slurm_out/`** first, then the repo root for older **`slurm-*.err`** layouts.

---

## 1. Overview — how the system fits together

### Login node vs compute node

- **Login node**: fine for editing files and **`sbatch`**, bad for hour-long CPU/RAM/network jobs (fair-share policies).
- **Compute node**: Slurm reserves **CPUs**, **memory**, and **wall time** for one batch session.

### One notebook, many partial runs

- **Cell 0** holds paths, constants, and **`RUN_CELL*`** booleans (one flag per stage).
- Later cells use **`if RUN_CELL…:`** to run work, or **`else:`** to skip and reload artifacts from disk when flags are **`False`**.
- Submitting **`sbatch`** runs the notebook **top to bottom once**, honoring those flags — no need to click “Run” in Jupyter.

### Artifacts every batch run produces

| Location | Files |
|----------|--------|
| **Submit directory** / **`slurm_out/`** | **`slurm-<job_name>-<JOBID>.out`** / **`.err`** |
| **Notebook working directory** (repo root when using **`pipe_job.slurm`**) | **`slurm-<job_name>-<JOBID>-output.ipynb`** |

With **`pipe_job.slurm`**, **`job_name`** is **`pipe_job`** — e.g. **`slurm-pipe_job-11807601-output.ipynb`** at repo root.

### Execution engine

Inside the batch script: **`papermill`** (preferred; logs cell boundaries) or **`jupyter nbconvert --execute`** fallback. **`PYTHONUNBUFFERED=1`** + **`stdbuf`** push Python output out sooner so **`tail -f`** looks responsive instead of freezing until a huge buffer fills.

---

## 2. Step-by-step — Charles / Ivy_Net

### A. One-time setup

1. **SSH** to Rivanna (or use Open OnDemand terminal).
2. **Clone or rsync** **`~/Ivy_Net`**. Logs go under **`slurm_out/`** relative to where you **`sbatch`** (use **repo root**).
3. **`module load miniforge`** (same as in **`pipe_job.slurm`**).
4. **Conda env** whose name matches **`ENV_NAME`** in **`pipe_job.slurm`** (default **`tenure_net`**).
5. **Secrets:** **`OPENALEX_*`** etc. in repo-root **`.env`** (gitignored).

### B. Edit **`pipe_job.slurm`** (account, mail, time)

Replace placeholders for your allocation, email, partition, **`#SBATCH`** resources, and **`ENV_NAME`** if needed.

### C. Configure the notebook

1. Open **`tenure/540_tenure_pipeline.ipynb`**.
2. In **Cell 0**, set **`RUN_CELL*`** flags for this submission.
3. **Save**.

### D. Submit and monitor

```bash
cd ~/Ivy_Net
sbatch pipe_job.slurm
```

**Stdout:**

```bash
tail -f slurm_out/slurm-pipe_job-<JOBID>.out
```

**Stderr:**

```bash
./scripts/track_slurm.sh <JOBID>
```

**Queue:**

```bash
squeue -u $USER
```

### E. After the job finishes

- Open **`slurm-pipe_job-<JOBID>-output.ipynb`** in Jupyter or VS Code.
- If the job failed, read tail of **`.err`** first, then **`.out`**, then email from Slurm.

### F. Cancel a running job

```bash
scancel <JOBID>
```

---

## 3. Official Rivanna references

- Slurm overview / partitions / **`--account`**: [Research Computing — Rivanna user guide](https://www.rc.virginia.edu/userinfo/rivanna/)
- **`module load`** stacks change rarely but verify **`miniforge`** name if yours fails.

---

## 4. Troubleshooting quick hits

| Symptom | Check |
|---------|--------|
| **`conda env not found`** | **`conda env list`** — name matches **`ENV_NAME`**; **`module load miniforge`** is inside **`pipe_job.slurm`**. |
| **`Notebook … not found`** | **`pipe_job.slurm`** expects **`tenure/540_tenure_pipeline.ipynb`** from **repo root**. |
| **`Invalid account`** | **`#SBATCH --account=`** set to PI-approved string. |
| **`Permission denied`** on **`./scripts/track_slurm.sh`** | **`chmod +x scripts/track_slurm.sh`**. |
| **Nothing new with **`tail -f`** for a long time** | Slow imports or I/O; **`PYTHONUNBUFFERED`** + **`stdbuf`** help. |
| **Wrong directory / missing `.err`** | Logs are **`SLURM_SUBMIT_DIR/slurm_out/`** — **`cd`** to the folder where you ran **`sbatch`** before **`track_slurm.sh`**. |

---

For day-of checklists and “do not stage generated files,” see **`tenure/documents/VA_WEEKEND_CHECKLIST.md`**.

For **Git vs rsync** (what lives where, iPhone → HPC → Mac → Cursor, `rsync_pull_recent_hpc.sh`), see **`scripts/DATA_SYNC.md`**.
