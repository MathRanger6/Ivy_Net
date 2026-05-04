# Rivanna notebook pipeline — starter kit for Beau

**Maintainer:** Charles (Ivy_Net / tenure pipeline).

Two layers: **this guide** explains the big picture and day-to-day steps; **`pipe_job_beau.slurm`** and **`track_slurm_beau.sh`** ship inside folder **`Beau_guide/`** — Beau treats that folder as his zip unpack root (**`cd ~/Beau_guide`**, **`sbatch ./pipe_job_beau.slurm`**). Charles keeps the same files in Ivy_Net at **`Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`**.

Charles keeps his production launcher as **`pipe_job.slurm`** at Ivy_Net repo root (minimal comments). Anything matching **`*_beau.*`** is Beau-facing (generic notebook launcher).

---

## Reading logs without assuming Linux fluency

Slurm writes plain-text **log files** next to the directory you were in when you typed **`sbatch`**. Charles often **`cd`**’s **Ivy_Net repo root** so logs sit beside **`tenure/`**; Beau typically **`cd`**’s **`~/Beau_guide`** so logs sit **inside** his unpacked bundle — either way, **`tail -f`** reads those files like “streaming Notepad.”

### What is a JOBID?

When you **`sbatch`** **`…/pipe_job_beau.slurm`**, Slurm replies with something like **`Submitted batch job 11807601`**. That number (**11807601**) is the **job ID**. It appears in log filenames so each run stays separate.

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

### Helper script: **`track_slurm_beau.sh`**

Shell scripts must be marked **executable** once:

```bash
BEAU=~/Beau_guide              # unpacked Beau_guide zip (contains track_slurm_beau.sh)
chmod +x "$BEAU/track_slurm_beau.sh"
```

What **`chmod +x`** means in plain English: “allow this file to run as a program.” Without it, the script may say **Permission denied.**

Run it from your **submit directory** — the folder where **`sbatch`** wrote **`slurm-*.out`** / **`*.err`** ( **`cd`** there before **`tail`**). If **`sbatch`** was from **`~/Beau_guide`**, **`cd ~/Beau_guide`** first:

```bash
cd ~/Beau_guide
./track_slurm_beau.sh 11807601
```

That finds **`slurm-*11807601*.err`** in **`pwd`** or next to **`track_slurm_beau.sh`**, then **`tail -f`**. **`export PROJECT_ROOT=/submit/dir`** works too if **`cd`** is awkward.

---

## 1. DIY starter kit — what files to hand Beau

Give him enough to clone/run **the same workflow**, not necessarily every asset in Ivy_Net.

### Minimum for Beau (**zip only** — no Ivy_Net clone)

| What | Why |
|------|-----|
| **`Beau_guide/`** folder (zip) | **`README_beau.md`**, **`HPC_SLURM_PIPELINE_GUIDE_beau.md`**, **`pipe_job_beau.slurm`**, **`track_slurm_beau.sh`**, optional **`.env.example_beau`**, **`*_reference_beau.*`** — Beau puts **`his_notebook.ipynb`** here (or sets **`NB_IN`** / **`BEAU_PROJECT_ROOT`**). |

### Minimum if Beau clones Ivy_Net

| What | Why |
|------|-----|
| Full **`Ivy_Net`** repo | Only when his notebook imports Ivy_Net-only modules (`functionsG_working.py`, **`tenure/`**, …). Otherwise the **`Beau_guide/`** zip above is enough. |
| **`Ivy_Net/…/Beau_guide/`** | Same **`Beau_guide`** files as the zip — **`cd Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide`** then **`sbatch ./pipe_job_beau.slurm`**. |

**`pipe_job_beau.slurm`** cds to **`BEAU_PROJECT_ROOT`** (optional inline edit), else **`PROJECT_ROOT`** from the shell, else **wherever Beau ran `sbatch` from** — **`NB_IN`** is relative to that **working directory** (Git not required). Charles’s **`pipe_job.slurm`** continues to target **`tenure/540_tenure_pipeline.ipynb`** by default.

This tutorial (**`tenure/HPC_SLURM_PIPELINE_GUIDE.md`**) focuses on the **tenure `540`** pipeline; Beau’s **step-by-step generic** doc is **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** inside **`Beau_guide/`**.

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

Files appear in two separate places:

| Location | Files |
|----------|--------|
| **Submit directory** (where **`sbatch`** ran) | **`slurm-<job_name>-<JOBID>.out`** / **`.err`** |
| **Notebook working directory** ( **`cd`** before **`sbatch`** or **`BEAU_PROJECT_ROOT`**) | **`slurm-<job_name>-<JOBID>-output.ipynb`** |

Charles typically **`cd`**’s **Ivy_Net repo root** so logs sit next to **`tenure/`**. Beau typically **`cd`**’s **`~/Beau_guide`** so logs sit **in** his bundle — **`papermill`** working dir may still differ if **`NB_IN`** points elsewhere (see **`HPC_SLURM_PIPELINE_GUIDE_beau.md`**).

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
2. **Beau:** unzip **`Beau_guide`** → **`cd ~/Beau_guide`** (put **`his_notebook.ipynb`** here). **Charles / Ivy_Net:** clone or rsync **`~/Ivy_Net`** — **`sbatch` logs write next to where you submit**.
3. **Load conda module** (same line as in **`pipe_job_beau.slurm`**):  
   **`module load miniforge`**
4. **Create conda env** whose **name matches** **`ENV_NAME`** in **`pipe_job_beau.slurm`** (default **`tenure_net`**):  
   **`conda create -n tenure_net python=3.11`**  
   Install **`papermill`**, **`jupyter`**, **`pandas`**, **`tqdm`**, and anything Cell 0 imports (**`lxml`**, **`requests`**, …).
5. **Copy secrets**: if Charles uses OpenAlex or similar, put **`OPENALEX_*`** vars in repo-root **`.env`** (gitignored); match **Charles’s** pattern.

### B. Edit Beau’s batch script (once per cluster/account)

Open **`~/Beau_guide/pipe_job_beau.slurm`** (zip layout) **or** **`Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm`** (clone layout) and replace every placeholder:

| Marker | Put here |
|--------|-----------|
| **`YOUR_NETID@virginia.edu`** | Your UVa email for Slurm notifications. |
| **`YOUR_SLURM_ALLOCATION`** | Your Rivanna billing group / PI allocation string (Research Computing docs or **`accounts`** command). |
| **`## EDIT`** sections | **`--partition`**, **`--mem`**, **`--cpus-per-task`**, **`--time`** if defaults don’t fit your notebook. |
| **`NB_IN`** | Beau sets **his own** notebook path **relative to the working directory** (**`cd`** before **`sbatch`**, or **`BEAU_PROJECT_ROOT`** / **`PROJECT_ROOT`**). For Charles’s **`pipe_job.slurm`**, the notebook is **`tenure/540_tenure_pipeline.ipynb`**. |
| **`ENV_NAME`** | Change the default or run **`ENV_NAME=myenv sbatch ./pipe_job_beau.slurm`** from **`~/Beau_guide`** (or pass full path to **`pipe_job_beau.slurm`**). |

If conda env binaries live outside **`~/.conda/envs/`**, edit the **`CONDA_PYTHON`** / **`CONDA_PAPERMILL`** / **`CONDA_NBCONVERT`** lines at the bottom of **`pipe_job_beau.slurm`** (same file in **`Beau_guide/`**).

### C. Configure the notebook run

1. Open **your** notebook path as set in **`NB_IN`** (Beau), **or** **`tenure/540_tenure_pipeline.ipynb`** when using Charles’s **`pipe_job.slurm`**.
2. In **Cell 0**, set **`RUN_CELL*`** booleans for this submission only.
3. **Save** the notebook.

### D. Submit and monitor

```bash
# Beau (zip): notebook + NB_IN live under ~/Beau_guide
cd ~/Beau_guide
sbatch ./pipe_job_beau.slurm

# Beau from Ivy_Net clone:
cd ~/Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide
sbatch ./pipe_job_beau.slurm
```

Note the numeric **JOBID** Slurm prints (see “Reading logs” if this is unfamiliar).

**Stdout** — watch **`print`**-heavy lines:

```bash
tail -f slurm-pipe_job_beau-<JOBID>.out
```

**Stderr** (often better “heartbeat”; tqdm lives here):

```bash
chmod +x ~/Beau_guide/track_slurm_beau.sh    # once (adjust path if unzip location differs)
cd ~/Beau_guide
./track_slurm_beau.sh <JOBID>
```

Or omit JOBID to follow the newest **`slurm-*.err`** in **`pwd`** or **`Beau_guide/`** — **`cd`** to your submit directory first.

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

Beau mentioned **`pip_job_beau`** — the checked-in Slurm script is **`pipe_job_beau.slurm`** (**pipe**, short for pipeline job, not Python **`pip`**) inside **`Beau_guide/`**.

---

## 5. Official Rivanna references

- Slurm overview / partitions / **`--account`**: [Research Computing — Rivanna user guide](https://www.rc.virginia.edu/userinfo/rivanna/)
- **`module load`** stacks change rarely but verify **`miniforge`** name if yours fails.

---

## 6. Troubleshooting quick hits

| Symptom | Check |
|---------|--------|
| **`conda env not found`** | **`conda env list`** — name matches **`ENV_NAME`**; **`module load miniforge`** before **`sbatch`** is inside script already. |
| **`Notebook … not found`** | **`NB_IN`** is relative to **working directory**: **`BEAU_PROJECT_ROOT`** / **`PROJECT_ROOT`** / folder you **`cd`**’d to before **`sbatch`**. **`pipe_job.slurm`** still assumes Ivy_Net layout with **`functionsG_working.py`**. |
| **`Invalid account`** | **`YOUR_SLURM_ALLOCATION`** replaced with PI-approved string. |
| **`Permission denied`** running **`./track_slurm_beau.sh`** | **`chmod +x ~/Beau_guide/track_slurm_beau.sh`** once (see “Reading logs”). |
| **Nothing new appears with **`tail -f`** for a long time** | Normal during slow imports or blocked I/O; eventually **`PYTHONUNBUFFERED`** + **`stdbuf`** flush lines — compare Beau script behavior with **`pipe_job.slurm`** if unsure. |
| **`tail` wrong directory / missing `.err`** | Logs land in **`SLURM_SUBMIT_DIR`** — folder where **`sbatch`** ran. **`track_slurm_beau.sh`** searches **`pwd`** (and **`Beau_guide/`**) — **`cd`** to that submit folder before calling it. |

---

Questions are mostly **allocation/partition** and **conda package parity** with **Charles** — everything else is already parameterized in **`Beau_guide/pipe_job_beau.slurm`**.
