#!/bin/bash
#SBATCH --job-name=lambda_sweep
#SBATCH --partition=standard
#SBATCH --account=sds_ag
#SBATCH --constraint=rivanna
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
set -euo pipefail
module load miniforge
ENV_NAME="${ENV_NAME:-sports_net}"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"
if [[ ! -x "${CONDA_PYTHON}" ]]; then
  CONDA_PYTHON="$(command -v python)"
fi
cd "${SLURM_SUBMIT_DIR}"
export PYTHONUNBUFFERED=1
"${CONDA_PYTHON}" sports/scripts/grandchild_lambda_select_sweep.py --lambda 1.25 1.5 1.75 2 3 4
