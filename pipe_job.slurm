#!/bin/bash
# Run 540_tenure_pipeline.ipynb with the RUN_CELL* flags as-set in CELL 0.
# Currently: RUN_CELL6A=True, RUN_CELL6B=True (OpenAlex author IDs + works by year).
#
# Submit from the Ivy_Net repo root:
#   cd /path/to/Ivy_Net && sbatch pipe_job.slurm
#
# Monitor live:
#   tail -f slurm-pipe_job-<JOBID>.out
#   tail -f slurm-pipe_job-<JOBID>.err

#SBATCH --time=6:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --partition=standard
#SBATCH --job-name=pipe_job
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge

cd "${SLURM_SUBMIT_DIR}"

export PYTHONUNBUFFERED=1

if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

ENV_NAME="${ENV_NAME:-tenure_net}"
NB_IN="540_tenure_pipeline.ipynb"
NB_OUT="slurm-pipe_job-${SLURM_JOB_ID}-output.ipynb"

command -v conda >/dev/null || { echo "ERROR: conda not on PATH after module load." >&2; exit 1; }
conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}" \
  || { echo "ERROR: conda env '${ENV_NAME}' not found. Run myjob.slurm first." >&2; exit 1; }

test -f "${NB_IN}" || { echo "ERROR: ${NB_IN} not found in ${PWD}" >&2; exit 1; }

OUT_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
ERR_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo "==> Notebook  : ${SLURM_SUBMIT_DIR}/${NB_IN}"
echo "==> Output nb : ${SLURM_SUBMIT_DIR}/${NB_OUT}   (executed copy with outputs)"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${OUT_FILE}"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${ERR_FILE}"
echo ""
echo "==> Active RUN_CELL flags (as set in CELL 0 of the notebook):"
grep "^RUN_CELL" "${NB_IN}" | grep -v '\\\\n' | python3 -c "
import sys, json
nb = json.load(open('${NB_IN}'))
for cell in nb['cells']:
    if cell.get('cell_type') != 'code': continue
    for line in cell.get('source', []):
        l = line.strip().rstrip(',')
        if l.startswith('RUN_CELL') and '=' in l:
            print('   ', l)
" 2>/dev/null || true
echo ""

# papermill gives per-cell progress + injects parameters if needed;
# fall back to nbconvert --execute if papermill is not installed.
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
