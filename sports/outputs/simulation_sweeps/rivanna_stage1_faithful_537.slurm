#!/bin/bash
#SBATCH --job-name=537_stage1
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --job-name=537_stage1
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

ENV_NAME="${ENV_NAME:-sports_net}"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"
if [[ ! -x "${CONDA_PYTHON}" ]]; then
  CONDA_PYTHON="$(command -v python)"
fi

echo "==> Job       : ${SLURM_JOB_NAME} ${SLURM_JOB_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> Python    : ${CONDA_PYTHON}"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo ""

run "${CONDA_PYTHON}" sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py stage1 --reset
