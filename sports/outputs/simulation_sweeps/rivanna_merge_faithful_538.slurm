#!/bin/bash
#SBATCH --job-name=538_merge
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=00:30:00
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag
#
# Final merge + plots → rivanna_faithful_538/grouped_candidates.csv

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

N_SHARDS="${N_SHARDS:-64}"

echo "==> Job       : ${SLURM_JOB_NAME} ${SLURM_JOB_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> Python    : ${CONDA_PYTHON}"
echo "==> Env name  : ${ENV_NAME}"
echo "==> Matplotlib check:"
if ! "${CONDA_PYTHON}" -c "import sys; import matplotlib; print('    exe:', sys.executable); print('    matplotlib', matplotlib.__version__)"; then
  echo "" >&2
  echo "ERROR: matplotlib missing in ${CONDA_PYTHON}" >&2
  echo "  Fix: conda activate ${ENV_NAME} && python -m pip install matplotlib" >&2
  exit 1
fi

echo "==> N shards  : ${N_SHARDS}"
echo ""

run "${CONDA_PYTHON}" sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py merge --n-shards "$N_SHARDS"
