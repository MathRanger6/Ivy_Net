# Beau_guide bundle

Self-contained folder under **`Ivy_Net/5-Manuscript/Beau_guide/`**. Maintainer: Charles.

Everything Beau needs for **Slurm + notebook pipeline onboarding**, plus reference copies of scripts the **`540`** notebook or **`pipe_job`** workflow mentions. Filenames use **`_beau`** (documents / primary Beau scripts) or **`_reference_beau`** (verbatim-ish copies from elsewhere in Ivy_Net for comparison).

---

## Read first

| File | Purpose |
|------|---------|
| **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** | Full Rivanna walkthrough (stdout/stderr, **`tail -f`**, **`sbatch`**, placeholders). |
| **`pipe_job_beau.slurm`** | Annotated batch job — edit **`YOUR_*`**, then **`sbatch`** from Ivy_Net root. |

---

## Notebook format example

| File | Purpose |
|------|---------|
| **`540_tenure_pipeline_beau.ipynb`** | Copy of **`tenure/540_tenure_pipeline.ipynb`** — shows Cell 0 paths, **`RUN_CELL*`** flags, and skip/reload pattern. **`pipe_job_beau.slurm`** defaults **`NB_IN`** here so Beau can execute the example without touching production paths (still requires full Ivy_Net tree + conda deps). |

---

## Beau scripts (primary)

| File | Purpose |
|------|---------|
| **`pipe_job_beau.slurm`** | Batch-execute **`NB_IN`** with papermill/nbconvert. |
| **`track_slurm_beau.sh`** | **`tail -f`** on **`slurm-*-<JOBID>.err`** — repo root + Beau_guide aware. **`chmod +x`** once. |

---

## Reference scripts (Charles / notebook-mentioned)

Same contents as upstream paths unless noted — rename only so this folder stays grep-friendly.

| File | Upstream / notes |
|------|------------------|
| **`pipe_job_reference_beau.slurm`** | Repo-root **`pipe_job.slurm`** — minimal Charles launcher. |
| **`track_slurm_reference_beau.sh`** | **`scripts/track_slurm.sh`** — minimal **`tail -f`** helper (expects logs in repo root). |
| **`build_openalex_cache_reference_beau.slurm`** | Repo-root **`build_openalex_cache.slurm`** — **`540`** mentions **`sbatch build_openalex_cache.slurm`**. |
| **`apply_url_updates_reference_beau.sh`** | Repo-root **`apply_url_updates.sh`** — referenced in notebook session log comments. |
| **`myjob_reference_beau.slurm`** | Repo-root **`myjob.slurm`** — conda env bootstrap pattern (sometimes cited when conda env missing). |

---

## Environment template

| File | Purpose |
|------|---------|
| **`.env.example_beau`** | Copy of repo **`.env.example`**. Copy to **Ivy_Net repo root** as **`.env`** (never commit secrets); notebook loads **`OPENALEX_*`** etc. from there. |

---

## Commands (from Ivy_Net repo root)

```bash
# one-time
chmod +x 5-Manuscript/Beau_guide/track_slurm_beau.sh

# submit
sbatch 5-Manuscript/Beau_guide/pipe_job_beau.slurm

# watch stderr
./5-Manuscript/Beau_guide/track_slurm_beau.sh <JOBID>
```

Canonical copy of this guide may also be updated at **`tenure/HPC_SLURM_PIPELINE_GUIDE.md`**; **`HPC_SLURM_PIPELINE_GUIDE_beau.md`** here is the bundle-local duplicate.
