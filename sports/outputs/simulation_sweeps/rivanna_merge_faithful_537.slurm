#!/bin/bash
#SBATCH --job-name=537_merge
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=00:30:00
#SBATCH --job-name=537_merge
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag
#
# Final merge + plots. Submit from Ivy_Net repo root so logs land in slurm_out/.

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
echo "==> Env name  : ${ENV_NAME} (override with ENV_NAME=... sbatch ...)"
echo "==> Matplotlib check (same interpreter as merge + candidate_plots):"
if ! "${CONDA_PYTHON}" -c "import sys; import matplotlib; print('    exe:', sys.executable); print('    matplotlib', matplotlib.__version__)"; then
    echo "" >&2
    echo "ERROR: matplotlib is not available in the Python that runs this merge job." >&2
    echo "  interpreter: ${CONDA_PYTHON}" >&2
    echo "  Cursor Remote SSH may auto-activate a conda env; Slurm does not — it uses the path above." >&2
    echo "  Fix on Rivanna: conda activate ${ENV_NAME} && python -m pip install matplotlib" >&2
    echo "  Or pick another env: ENV_NAME=my_env sbatch ..." >&2
    exit 1
fi

echo "==> N shards  : ${N_SHARDS}"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm_out/slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm_out/slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo ""

run "${CONDA_PYTHON}" sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py merge --n-shards "$N_SHARDS"
