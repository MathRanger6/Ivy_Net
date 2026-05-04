# Rivanna notebook pipeline — starter kit for Beau

**Maintainer:** Charles (Ivy_Net / tenure pipeline).

Two layers: **this guide** explains the big picture and day-to-day steps; **`pipe_job_beau.slurm`** and **`track_slurm_beau.sh`** under **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`** repeat the same ideas inline with **`YOUR_*` placeholders** you edit once.

Charles keeps his production launcher as **`pipe_job.slurm`** at repo root (minimal comments). Beau’s annotated copies live in **`Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`** (anything matching **`*_beau.*`**).

---

## Reading logs without assuming Linux fluency

Slurm writes plain-text **log files** next to the directory you were in when you typed **`sbatch`** (your **submit directory**). Charles recommends **`cd`** into the **Ivy_Net repo root** first so **`*.out`** / **`*.err`** land beside **`tenure/`** — same layout as **`pipe_job.slurm`**. You read logs with terminal commands — think “streaming Notepad,” where **`tail -f`** keeps showing new lines as Slurm appends them.

### What is a JOBID?

When you run **`sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`** from repo root, Slurm replies with something like **`Submitted batch job 11807601`**. That number (**11807601**) is the **job ID**. It appears in log filenames so each run stays separate.

### Two streams: `.out` vs `.err` (NOT “error-only”)

Unix separates normal printed output into two pipes:

| Stream | Filename pattern | Typical contents |
|--------|------------------|------------------|
| **stdout** | **`slurm-<job_name>-<JOBID>.out`** | **`echo`** lines from the batch script, many **`print()`** statements from Python. |
| **stderr** | **`slurm-<job_name>-<JOBID>.err`** | Progress bars (**tqdm**), warnings, status lines — lots of Jupyter stacks write here **even when nothing failed.** |

So **`.err` is often where you see motion first**, not necessarily because anything broke.

### What does `tail` do? What does `tail -f` do?

- **`tail slurm-pipe_job_beau-11807601.err`** shows only the **last ~10 lines** of that file — snapshot.
- **`tail -f`** (**follow**) keeps the terminal **attached**: whenever Slurm appends another line to that file on disk, your terminal prints it immediately — **near-live monitoring** while the compute node runs your notebook.

Stop watching with **Ctrl+C**. That **only stops tail**; it does **not** stop the Slurm job.

### Running Charles’s helper script: `./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh`

Shell scripts must be marked **executable** once:

```bash
chmod +x 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh
```

What **`chmod +x`** means in plain English: “allow this file to run as a program.” Without it, **`./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh`** may say **Permission denied.**

The **`./`** means “run the script **from this path relative to where you **`cd`**’d**,” not a system-wide installed command.

Run from **repo root**:

```bash
./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh 11807601
```

That finds **`slurm-*11807601*.err`** under the Ivy_Net root (or under **`Beau_guide/`** if that’s where logs landed) and **`tail -f`** it — same idea as typing **`tail -f …`** yourself, but it picks the right filename.

---

## 1. DIY starter kit — what files to hand Beau

Give him enough to clone/run **the same workflow**, not necessarily every asset in Ivy_Net.

### Minimum (if he clones the whole repo)

| What | Why |
|------|-----|
| Full **`Ivy_Net`** repo | Notebook imports `functionsG_working.py`, `tenure/tenure_pipeline/*.py`, paths under `tenure/`. |
| **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`** | **Generic Rivanna onboarding** for Beau: **`README_beau.md`**, **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** (numbered steps + blockquote “deep dives”), **`pipe_job_beau.slurm`**, **`track_slurm_beau.sh`**, optional **`.env.example_beau`**, and **`*_reference_beau.*`** copies of Charles’s minimal **`pipe_job`** / **`track_slurm`** — **no bundled pipeline notebook**; Beau sets **`NB_IN`** to **his own** `.ipynb`. |

**`pipe_job_beau.slurm`** uses **`.git`** (walking up from **`sbatch`**) to find project root, then runs **`NB_IN`** relative to that root — Beau edits **`NB_IN`** to his notebook path. Charles’s **`pipe_job.slurm`** continues to target **`tenure/540_tenure_pipeline.ipynb`** by default.

This tutorial (**`tenure/HPC_SLURM_PIPELINE_GUIDE.md`**) focuses on the **tenure `540`** pipeline; Beau’s **step-by-step generic** doc is **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** in that folder.

### Nice additions

| What | Why |
|------|-----|
| **`.env.example_beau`** (in **`Beau_guide/`**; copy to repo **`.env`**) | Notebook loads repo-root **`.env`** for OpenAlex mail/API if those stages run. |
| **Export list / `environment.yml`** | So Beau can recreate **`tenure_net`** without guessing packages — coordinate with **Charles**. |
| **Large data** (DBLP XML, snapshots, CDH trees) | Only if Beau runs stages that read them — usually excluded from git; share separately or paths in Cell 0. |

---

## 2. Overview — how the system fits together

### Login node vs compute node

- **Login node**: fine for editing files and **`sbatch`**, bad for hour-long CPU/RAM/network jobs (fair-share policies).
- **Compute node**: Slurm reserves **CPUs**, **memory**, and **wall time** for one batch session.

### One notebook, many partial runs

- **Cell 0** holds paths, constants, and **`RUN_CELL*`** booleans (one flag per stage).
- Later cells use **`if RUN_CELL…:`** to run work, or **`else:`** to skip and reload artifacts from disk when flags are **`False`**.
- Submitting **`sbatch`** runs the notebook **top to bottom once**, honoring those flags — no need to click “Run” in Jupyter.

### Three artifacts every batch run produces

Files appear in the directory where **`sbatch`** was invoked — **recommended: Ivy_Net repo root** so logs sit next to **`tenure/`**:

| File pattern | Contents |
|--------------|----------|
| **`slurm-<job_name>-<JOBID>.out`** | Stdout — script echoes + much notebook **`print`** output. Use **`tail -f`** on this file to watch normal prints scroll by (see “Reading logs” above). |
| **`slurm-<job_name>-<JOBID>.err`** | Stderr — **tqdm**, warnings, much library chatter; often updates fastest. **`track_slurm_beau.sh`** opens this stream for you and **`tail -f`** follows it. |
| **`slurm-<job_name>-<JOBID>-output.ipynb`** | Full notebook copy **with executed cell outputs** — archive, proof-of-run, shareable artifact. |

With **`pipe_job_beau.slurm`**, **`job_name`** defaults to **`pipe_job_beau`** — so **`slurm-pipe_job_beau-11807601-output.ipynb`** style names.

### Execution engine

Inside the batch script: **`papermill`** (preferred; logs cell boundaries) or **`jupyter nbconvert --execute`** fallback. **`PYTHONUNBUFFERED=1`** + **`stdbuf`** push Python output out sooner so **`tail -f`** looks responsive instead of freezing until a huge buffer fills.

---

## 3. Step-by-step — Beau’s first Rivanna run

### A. One-time setup

1. **SSH** to Rivanna (or use Open OnDemand terminal).
2. **Clone** Ivy_Net (or rsync **Charles’s** tree) into the path you want, e.g.  
   **`~/Ivy_Net`** — remember this path; **`sbatch` logs write next to where you submit**.
3. **Load conda module** (same line as in **`pipe_job_beau.slurm`**):  
   **`module load miniforge`**
4. **Create conda env** whose **name matches** **`ENV_NAME`** in **`pipe_job_beau.slurm`** (default **`tenure_net`**):  
   **`conda create -n tenure_net python=3.11`**  
   Install **`papermill`**, **`jupyter`**, **`pandas`**, **`tqdm`**, and anything Cell 0 imports (**`lxml`**, **`requests`**, …).
5. **Copy secrets**: if Charles uses OpenAlex or similar, put **`OPENALEX_*`** vars in repo-root **`.env`** (gitignored); match **Charles’s** pattern.

### B. Edit Beau’s batch script (once per cluster/account)

Open **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`** and replace every placeholder:

| Marker | Put here |
|--------|-----------|
| **`YOUR_NETID@virginia.edu`** | Your UVa email for Slurm notifications. |
| **`YOUR_SLURM_ALLOCATION`** | Your Rivanna billing group / PI allocation string (Research Computing docs or **`accounts`** command). |
| **`## EDIT`** sections | **`--partition`**, **`--mem`**, **`--cpus-per-task`**, **`--time`** if defaults don’t fit your notebook. |
| **`NB_IN`** | In **`pipe_job_beau.slurm`** Beau sets **his own** notebook path relative to project root (script discovers root via **`.git`**). For Charles’s **`pipe_job.slurm`**, the notebook is **`tenure/540_tenure_pipeline.ipynb`**. |
| **`ENV_NAME`** | If you named the conda env something other than **`tenure_net`**, change the default or run **`ENV_NAME=myenv sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`**. |

If conda env binaries live outside **`~/.conda/envs/`**, edit the **`CONDA_PYTHON`** / **`CONDA_PAPERMILL`** / **`CONDA_NBCONVERT`** lines at the bottom of **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`**.

### C. Configure the notebook run

1. Open **your** notebook path as set in **`NB_IN`** (Beau), **or** **`tenure/540_tenure_pipeline.ipynb`** when using Charles’s **`pipe_job.slurm`**.
2. In **Cell 0**, set **`RUN_CELL*`** booleans for this submission only.
3. **Save** the notebook.

### D. Submit and monitor

```bash
cd ~/Ivy_Net                    # INSERT: your actual Ivy_Net repo root path
sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm
```

Note the numeric **JOBID** Slurm prints (see “Reading logs” if this is unfamiliar).

**Stdout** — watch **`print`**-heavy lines:

```bash
tail -f slurm-pipe_job_beau-<JOBID>.out
```

**Stderr** (often better “heartbeat”; tqdm lives here):

```bash
chmod +x 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh    # once per clone
./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh <JOBID>
```

Or omit JOBID to follow the newest **`slurm-*.err`** found under repo root or **`Beau_guide/`**.

**Queue:**

```bash
squeue -u $USER
watch -n 5 'squeue -u $USER'
```

### E. After the job finishes

- Open **`slurm-pipe_job_beau-<JOBID>-output.ipynb`** in Jupyter or VS Code — full outputs embedded.
- If the job failed, read tail of **`.err`** first, then **`.out`**, then email from Slurm.

### F. Cancel a running job

```bash
scancel <JOBID>
```

---

## 4. Naming note

Beau mentioned **`pip_job_beau`** — the checked-in Slurm script is **`pipe_job_beau.slurm`** (**pipe**, short for pipeline job, not Python **`pip`**) under **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`**, so job names and **`sbatch`** paths stay readable.

---

## 5. Official Rivanna references

- Slurm overview / partitions / **`--account`**: [Research Computing — Rivanna user guide](https://www.rc.virginia.edu/userinfo/rivanna/)
- **`module load`** stacks change rarely but verify **`miniforge`** name if yours fails.

---

## 6. Troubleshooting quick hits

| Symptom | Check |
|---------|--------|
| **`conda env not found`** | **`conda env list`** — name matches **`ENV_NAME`**; **`module load miniforge`** before **`sbatch`** is inside script already. |
| **`Notebook … not found`** | **`NB_IN`** is relative to **project root**. **`pipe_job_beau.slurm`** finds root via **`.git`** walking up from **`sbatch`** (or **`BEAU_PROJECT_ROOT`**). **`pipe_job.slurm`** still assumes Ivy_Net layout with **`functionsG_working.py`**. |
| **`Invalid account`** | **`YOUR_SLURM_ALLOCATION`** replaced with PI-approved string. |
| **`Permission denied`** running **`./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh`** | Run **`chmod +x 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh`** once (see “Reading logs”). |
| **Nothing new appears with **`tail -f`** for a long time** | Normal during slow imports or blocked I/O; eventually **`PYTHONUNBUFFERED`** + **`stdbuf`** flush lines — compare Beau script behavior with **`pipe_job.slurm`** if unsure. |
| **`tail` wrong directory / missing `.err`** | Logs land in **`SLURM_SUBMIT_DIR`** — whatever folder you **`cd`**’d to before **`sbatch`**. Prefer **`cd Ivy_Net`** then **`sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`**; **`track_slurm_beau.sh`** searches repo root **and** **`Beau_guide/`**. |

---

Questions are mostly **allocation/partition** and **conda package parity** with **Charles** — everything else is already parameterized in **`1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`**.
