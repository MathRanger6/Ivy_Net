# Beau_guide — generic Slurm + Jupyter notebook

**Location:** `1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/`  
**Purpose:** Help Beau run **his own** main notebook on Rivanna via **`sbatch`**, without tying him to Charles’s tenure/OpenAlex/Wayback tooling.

---

## Files

| File | What it is |
|------|------------|
| **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** | **Start here** — numbered steps + optional “deep dive” notes (blockquote margins). |
| **`pipe_job_beau.slurm`** | Batch script: edit **`NB_IN`**, allocation, conda env → **`sbatch`**. |
| **`track_slurm_beau.sh`** | **`tail -f`** the **`.err`** log for a Slurm job ID. **`chmod +x`** once. |
| **`pipe_job_reference_beau.slurm`** | Charles’s minimal **`pipe_job.slurm`** copy for comparison only. |
| **`track_slurm_reference_beau.sh`** | Minimal **`scripts/track_slurm.sh`** copy (expects `.git` project root). |
| **`myjob_reference_beau.slurm`** | Optional pattern for installing conda deps via Slurm (reference only). |
| **`.env.example_beau`** | Optional template if **your** notebook loads secrets from repo-root **`.env`**. |

There is **no** bundled pipeline notebook — you point **`NB_IN`** at whatever `.ipynb` you maintain.

---

## One-line paths (copy-paste)

Replace **`/path/to/Ivy_Net`** with your clone root (must contain **`.git`**).

```bash
export BEAU='1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide'
chmod +x "$BEAU/track_slurm_beau.sh"
cd /path/to/Ivy_Net
sbatch "$BEAU/pipe_job_beau.slurm"
./"$BEAU/track_slurm_beau.sh" <JOBID>
```

Canonical tenure-focused narrative (Charles’s **`540`** pipeline) lives at **`tenure/HPC_SLURM_PIPELINE_GUIDE.md`** when he works inside Ivy_Net’s tenure stack — **this folder is the simplified pass for Beau.**
