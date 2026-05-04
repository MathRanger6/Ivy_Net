#!/bin/bash
# =============================================================================
# pipe_job_beau.slurm — Rivanna: run YOUR Jupyter notebook on a compute node
#
# Intended layout: lives inside folder Beau_guide/ (zip unpack root). From there:
#   cd ~/Beau_guide && sbatch ./pipe_job_beau.slurm
# (Charles also keeps Beau_guide inside Ivy_Net under …/5-Manuscript/Beau_guide/.)
# =============================================================================
#
# IDEA
# ----
# Interactive Jupyter on the login node is fine for editing; long runs belong on
# Slurm so you get CPUs/RAM and stay within cluster rules.
#
# This job executes one .ipynb top-to-bottom using papermill (or nbconvert).
# Optional pattern: early cells define booleans (e.g. RUN_CELL3 = False) so later
# cells can skip expensive steps without deleting code.
#
# WORKING DIRECTORY (no Git required)
# -----------------------------------
# Before papermill runs, the script cds to:
#   1) BEAU_PROJECT_ROOT below (if non-empty), else
#   2) PROJECT_ROOT env var (if you exported it before sbatch), else
#   3) the folder you were in when you ran sbatch ($SLURM_SUBMIT_DIR).
#
# Put NB_IN relative to that folder (e.g. my_analysis.ipynb or notes/run.ipynb).
#
# FLOW
# ----
#   1. Edit ## EDIT blocks below (email, allocation, ENV_NAME, NB_IN).
#   2. Default: put your .ipynb in Beau_guide/, cd ~/Beau_guide, NB_IN=my.ipynb .
#      Else: cd to your notebook folder, or set BEAU_PROJECT_ROOT in this file.
#   3. sbatch ./pipe_job_beau.slurm
#   4. tail -f slurm-<jobname>-<JOBID>.err   # tqdm often here (live updates)
#
# =============================================================================

# ## EDIT — Slurm (Rivanna)
#SBATCH --time=6:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=standard
#SBATCH --job-name=pipe_job_beau
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err
#SBATCH --mail-user=YOUR_NETID@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=YOUR_SLURM_ALLOCATION

set -euo pipefail

# ## EDIT — Optional absolute working directory (overrides submit-dir default).
# Leave empty if you always `cd` to your notebook folder before sbatch.
# Example: BEAU_PROJECT_ROOT="/home/you/myproject"
BEAU_PROJECT_ROOT="${BEAU_PROJECT_ROOT:-}"

if [[ -n "${BEAU_PROJECT_ROOT}" ]]; then
  WORK_ROOT="$(cd "${BEAU_PROJECT_ROOT}" && pwd)"
elif [[ -n "${PROJECT_ROOT:-}" ]]; then
  WORK_ROOT="$(cd "${PROJECT_ROOT}" && pwd)"
else
  WORK_ROOT="$(cd "${SLURM_SUBMIT_DIR}" && pwd)"
fi

cd "${WORK_ROOT}"

# ## EDIT — Module providing conda (site-specific).
module load miniforge

export PYTHONUNBUFFERED=1

if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

# ## EDIT — Conda environment name.
ENV_NAME="${ENV_NAME:-tenure_net}"

# ## EDIT — Notebook path relative to WORK_ROOT above (must exist after cd).
# Examples: "analysis.ipynb"   "experiments/run.ipynb"
NB_IN="YOUR_NOTEBOOK.ipynb"

NB_OUT="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}-output.ipynb"

command -v conda >/dev/null || { echo "ERROR: conda not on PATH after module load." >&2; exit 1; }
conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}" \
  || { echo "ERROR: conda env '${ENV_NAME}' not found. Create it interactively." >&2; exit 1; }

test -f "${NB_IN}" || { echo "ERROR: ${NB_IN} not found under ${WORK_ROOT} — fix NB_IN or cd / BEAU_PROJECT_ROOT" >&2; exit 1; }

OUT_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
ERR_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo "==> Working dir : ${WORK_ROOT}"
echo "==> Notebook    : ${WORK_ROOT}/${NB_IN}"
echo "==> Output nb   : ${WORK_ROOT}/${NB_OUT}"
echo "==> Logs (.out/.err) use SLURM_SUBMIT_DIR = ${SLURM_SUBMIT_DIR}"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${OUT_FILE}"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${ERR_FILE}"
echo ""
echo "==> Lines starting with RUN_CELL in code cells (optional flags):"
python3 -c "
import json
nb = json.load(open('${NB_IN}', encoding='utf-8'))
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    for line in cell.get('source', []):
        l = line.strip().rstrip(',')
        if l.startswith('RUN_CELL') and '=' in l:
            print('   ', l)
" 2>/dev/null || true
echo ""

CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"
CONDA_PAPERMILL="${HOME}/.conda/envs/${ENV_NAME}/bin/papermill"
CONDA_NBCONVERT="${HOME}/.conda/envs/${ENV_NAME}/bin/jupyter"

if "${CONDA_PYTHON}" -c "import papermill" 2>/dev/null && [[ -x "${CONDA_PAPERMILL}" ]]; then
  echo "==> Executing via papermill …"
  run "${CONDA_PAPERMILL}" \
      --no-progress-bar \
      --log-output \
      --execution-timeout -1 \
      "${NB_IN}" "${NB_OUT}"
else
  echo "==> papermill not found — falling back to jupyter nbconvert …"
  run "${CONDA_NBCONVERT}" nbconvert \
      --to notebook \
      --execute \
      --ExecutePreprocessor.timeout=-1 \
      --output "${NB_OUT}" \
      "${NB_IN}"
fi

echo ""
echo "==> Job complete. Executed notebook saved to: ${NB_OUT}"
