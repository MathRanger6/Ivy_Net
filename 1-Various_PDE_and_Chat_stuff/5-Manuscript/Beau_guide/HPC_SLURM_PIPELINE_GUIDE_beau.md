# Rivanna — run **your** Jupyter notebook with Slurm (Beau)

**Bundle path:** `1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`  
**Maintainer:** Charles · **Audience:** Beau (or anyone with a **main notebook** + Rivanna)

This guide is **generic**: you supply the **`.ipynb`** path. It is **not** tied to OpenAlex, Wayback, or repo-specific maintenance scripts.

**How to read this file**

- **Normal body text** = do this in order (the “main lane”).
- **Indented blockquotes** (`>`) = optional explanations if a term or step is unfamiliar — skip them anytime without losing the thread.

---

## Step 1 — Preconditions

1. Rivanna SSH or OnDemand terminal works.
2. You know your **Slurm allocation** (`#SBATCH --account=`) and **partition** (often `standard`); your PI or [RC docs](https://www.rc.virginia.edu/userinfo/rivanna/) explain these.
3. Your work lives in a **Git project** (the folder contains a **`.git`** entry) *or* you will set **`BEAU_PROJECT_ROOT`** inside `pipe_job_beau.slurm` to your project root path.
4. You have (or will create) a **conda environment** that can import everything your notebook needs, with **`papermill`** or **`jupyter`** installed.

> **Deep dive — why `.git`?**  
> `pipe_job_beau.slurm` finds your *project root* by walking upward from where you ran `sbatch` until it sees **`.git`**, then `cd`s there before running `papermill`. That way your notebook path (`NB_IN`) can be written **relative** to project root (e.g. `notebooks/main.ipynb`). If you don’t use Git, fill in **`BEAU_PROJECT_ROOT`** in the script with an absolute path.

> **Deep dive — login node vs compute**  
> Light edits and `sbatch` are fine on the login node. Heavy/long notebook runs belong in a batch job so you get reserved CPUs/RAM and don’t violate login-node policies.

---

## Step 2 — Edit `pipe_job_beau.slurm`

Open **`pipe_job_beau.slurm`** and fix every **`## EDIT`** / **`YOUR_*`**:

| Item | Action |
|------|--------|
| **`YOUR_NETID@virginia.edu`** | Your UVa email for Slurm mail |
| **`YOUR_SLURM_ALLOCATION`** | Billing group |
| **`--partition`**, **`--mem`**, **`--cpus`**, **`--time`** | Match your workload |
| **`ENV_NAME`** | Conda env name (default shown in file) |
| **`NB_IN`** | **Your** notebook path **relative to project root**, e.g. `notebooks/beau_main.ipynb` |
| **`BEAU_PROJECT_ROOT`** | Only if auto **`.git`** discovery fails — set to absolute project root |

> **Deep dive — `NB_IN` must exist after `cd` to root**  
> The batch script checks that `NB_IN` is a real file under project root. If you get “not found”, your path or `BEAU_PROJECT_ROOT` is wrong.

---

## Step 3 — (Optional) Notebook design: flags in Cell 0

If you want **checkpoint-style** behavior: put tunables (paths, booleans like `RUN_STEP2 = True`) in an early code cell; in later cells use `if RUN_STEP2:` / `else:` to skip and load saved data. **Totally optional** — a plain linear notebook works with `papermill` too.

> **Deep dive — why people do this**  
> One `sbatch` runs the notebook **top to bottom once**. Booleans let you turn off expensive cells without maintaining multiple copies of the notebook.

The job script prints any code-cell lines starting with **`RUN_CELL`** before execute (harmless if you use different names).

---

## Step 4 — Submit from project root (recommended)

```bash
cd /path/to/your/project/root    # directory that contains .git
sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm
```

Slurm prints a **job ID**. Log files:

- **`slurm-<jobname>-<JOBID>.out`** — stdout  
- **`slurm-<jobname>-<JOBID>.err`** — stderr (often **tqdm** / warnings; not “errors only”)

They are created in the directory you were in when you typed **`sbatch`** (same as **`SLURM_SUBMIT_DIR`**).

> **Deep dive — JOBID**  
> The integer in the `Submitted batch job …` line is the **JOBID**; it appears in the log filenames.

---

## Step 5 — Watch logs

**Stderr** (usually livelier):

```bash
chmod +x 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh   # once
./1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/track_slurm_beau.sh <JOBID>
```

Or omit **`<JOBID>`** to pick the newest **`slurm-*.err`** under project root or this folder.

**Stdout:**

```bash
tail -f slurm-pipe_job_beau-<JOBID>.out
```

> **Deep dive — `tail` vs `tail -f`**  
> `tail file` prints the **end** of the file once. **`tail -f`** (“follow”) keeps printing **new** lines as Slurm writes them — like a live feed. **Ctrl+C** stops `tail`; it does **not** cancel the job (use **`scancel JOBID`**).

> **Deep dive — `chmod +x` and `./script.sh`**  
> **`chmod +x`** marks the script as executable. **`./`** means “run this file from the current directory” instead of searching `PATH`.

---

## Step 6 — Artifacts when the job finishes

| Output | Meaning |
|--------|---------|
| **`slurm-*-<JOBID>-output.ipynb`** | Executed notebook **with outputs** (good to archive or share). |

Path is under **project root** (where `papermill` ran).

---

## Step 7 — Cancel a job

```bash
scancel <JOBID>
```

---

## Optional: secrets (`.env`)

If **your** notebook loads **`python-dotenv`** or similar from project root:

1. Copy **`.env.example_beau`** ideas into a repo-root **`.env`** (keep **`.env`** git-ignored).
2. Never commit API keys.

> This bundle does **not** require OpenAlex or URL-maintenance scripts — only what **you** choose to use in your notebook.

---

## Troubleshooting (quick)

| Symptom | Check |
|---------|--------|
| **No `.git` found** | `cd` to project root before `sbatch`, or set **`BEAU_PROJECT_ROOT`**. |
| **`NB_IN` not found** | Path is relative to **project root**, not to `Beau_guide/`. |
| **Wrong `python` / no `playwright`** (unrelated to Slurm, for local PDF hacks) | On Rivanna, `which python` must point into your conda env — use `~/.../envs/your_env/bin/python` if needed. |
| **`Permission denied`** on `track_slurm_beau.sh` | `chmod +x .../track_slurm_beau.sh` |

---

## Reference copies in this folder

**`pipe_job_reference_beau.slurm`** / **`track_slurm_reference_beau.sh`** mirror Charles’s Ivy_Net production helpers. **Ignore them** unless you want to compare style; they are not required for your workflow.

**`myjob_reference_beau.slurm`** shows a pattern for heavier one-time conda installs via Slurm — optional.

---

## Naming note

Some people say “pip_job” — the file is **`pipe_job_beau.slurm`** (**pipe** = pipeline-style batch job).
