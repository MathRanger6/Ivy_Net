# Beau_guide — Slurm batch execution for **your** Jupyter notebook

**Treat this folder as Beau’s workspace.** Zip or share **`Beau_guide/`** as-is; after unpacking on Rivanna, **`cd`** into it — paths below assume **that folder is your current directory**.

**Goal:** Run **your** `.ipynb` on a **compute node** (not heavy work on the login node), with optional **boolean** switches in early cells and **live log tailing**.

No Git repo required. **`NB_IN`** is relative to the working directory you choose (**`cd`** before **`sbatch`**, or **`BEAU_PROJECT_ROOT`** / **`PROJECT_ROOT`**).

---

## Files (everything beside this README)

| File | Role |
|------|------|
| **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** | **Read this first** — numbered steps + optional blockquotes. |
| **`pipe_job_beau.slurm`** | Edit **`NB_IN`**, allocation, conda **`ENV_NAME`** → **`sbatch ./pipe_job_beau.slurm`**. |
| **`track_slurm_beau.sh`** | **`tail -f`** the job’s **`.err`** log (`chmod +x ./track_slurm_beau.sh` once). |
| **`pipe_job_reference_beau.slurm`**, **`track_slurm_reference_beau.sh`**, **`myjob_reference_beau.slurm`** | Optional comparison with Charles’s Ivy_Net helpers. |
| **`.env.example_beau`** | Optional if your notebook reads **`.env`**. |

---

## Minimal pattern (bundle root = here)

Put **`your_notebook.ipynb`** in **`Beau_guide/`** next to **`pipe_job_beau.slurm`**, set **`NB_IN="your_notebook.ipynb"`**, then:

```bash
cd ~/Beau_guide                         # unpacked zip — folder that contains pipe_job_beau.slurm
chmod +x ./track_slurm_beau.sh          # once
sbatch ./pipe_job_beau.slurm
./track_slurm_beau.sh <JOBID>           # or: tail -f slurm-pipe_job_beau-<JOBID>.err
```

If your notebook stays **outside** this folder, **`cd`** to that folder before **`sbatch`**, or set **`BEAU_PROJECT_ROOT`** in **`pipe_job_beau.slurm`** — see **`HPC_SLURM_PIPELINE_GUIDE_beau.md`**.

---

**Charles:** The same **`Beau_guide/`** contents also live inside Ivy_Net at **`Ivy_Net/1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`**. Beau only needs the zipped folder.

Charles’s tenure-focused narrative (**`540`** pipeline) is **`tenure/HPC_SLURM_PIPELINE_GUIDE.md`**.
