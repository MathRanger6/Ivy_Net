#!/bin/bash
# =============================================================================
# pipe_job_beau.slurm — Rivanna: batch-run YOUR main Jupyter notebook with Slurm
# Lives in: 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/
# =============================================================================
#
# OVERVIEW
# --------
# Submits one job that executes your notebook top-to-bottom on a compute node.
# Optional pattern: Cell 0 defines booleans (e.g. RUN_CELL*) and later cells only
# run heavy steps when True — entirely up to your notebook design.
#
# QUICK FLOW
# ----------
#  1. Edit ## EDIT sections below (allocation, email, NB_IN, conda env).
#  2. cd /your/project/root    # folder that contains .git (recommended)
#  3. sbatch 1-Various_PDE_and_Chat_stuff/5-Manuscript/Beau_guide/pipe_job_beau.slurm
#  4. tail -f slurm-<jobname>-<JOBID>.err   # tqdm often here; see HPC_SLURM_PIPELINE_GUIDE_beau.md
#  5. chmod +x …/track_slurm_beau.sh && ./…/track_slurm_beau.sh <JOBID>
#
# PROJECT ROOT
# ------------
# Script cd’s to project root before papermill. By default it walks upward from
# your sbatch directory until it finds .git . If your tree has no .git, set
# BEAU_PROJECT_ROOT in the ## EDIT block to an absolute path.
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

# ## EDIT — Optional: absolute project root if .git cannot be found walking up from sbatch cwd.
# Example: BEAU_PROJECT_ROOT="/sfs/gpfs/tardis/home/you/myproject"
BEAU_PROJECT_ROOT="${BEAU_PROJECT_ROOT:-}"

_find_repo_root_from_submit_dir() {
  local d
  d="$(cd "${SLURM_SUBMIT_DIR}" && pwd)"
  while [[ "$d" != "/" ]]; do
    if [[ -e "$d/.git" ]]; then
      printf '%s\n' "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

if [[ -n "${BEAU_PROJECT_ROOT}" ]]; then
  REPO_ROOT="$(cd "${BEAU_PROJECT_ROOT}" && pwd)"
else
  REPO_ROOT="$(_find_repo_root_from_submit_dir)" || {
    echo "ERROR: No .git found walking up from ${SLURM_SUBMIT_DIR}. Set BEAU_PROJECT_ROOT in pipe_job_beau.slurm ." >&2
    exit 1
  }
fi

cd "${REPO_ROOT}"

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

# ## EDIT — Your main notebook path, RELATIVE to project root (must exist after cd above).
# Examples:  "notebooks/analysis.ipynb"  or  "my_workflow.ipynb"
NB_IN="YOUR_NOTEBOOK.ipynb"

# Executed notebook output (written under REPO_ROOT).
NB_OUT="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}-output.ipynb"

command -v conda >/dev/null || { echo "ERROR: conda not on PATH after module load." >&2; exit 1; }
conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}" \
  || { echo "ERROR: conda env '${ENV_NAME}' not found. Create it interactively." >&2; exit 1; }

test -f "${NB_IN}" || { echo "ERROR: ${NB_IN} not found under ${REPO_ROOT} — fix NB_IN in pipe_job_beau.slurm" >&2; exit 1; }

OUT_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
ERR_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo "==> Project root: ${REPO_ROOT}"
echo "==> Notebook    : ${REPO_ROOT}/${NB_IN}"
echo "==> Output nb   : ${REPO_ROOT}/${NB_OUT}"
echo "==> Submit from  : ${SLURM_SUBMIT_DIR}  (logs .out/.err land here)"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${OUT_FILE}"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${ERR_FILE}"
echo ""
echo "==> Lines in code cells starting with RUN_CELL (optional; for skip/reload notebooks):"
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
