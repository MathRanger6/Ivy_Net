#!/bin/bash
# Submit from this repo so paths resolve correctly:
#   cd /path/to/Ivy_Net && sbatch myjob.slurm
#
# Review #SBATCH lines below (account, partition, mail, time) before submitting.

#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=standard
#SBATCH --job-name=tenure_net_env_install
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge

# Directory you submitted from (recommended: Ivy_Net repo root).
cd "${SLURM_SUBMIT_DIR}"

# Slurm already writes this script's stdout/stderr to slurm-%x-%j.out — no need to run
# tail inside the job. These settings help the log file flush often so a login-node
#   tail -f slurm-<jobname>-<jobid>.out
# shows live progress instead of big silent gaps.
export PYTHONUNBUFFERED=1
export PIP_PROGRESS_BAR=on

# Line-buffer stdout/stderr when stdbuf exists (common on Linux).
if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

command -v conda >/dev/null || { echo "ERROR: conda not on PATH after module load." >&2; exit 1; }

# Override with:  sbatch --export=ALL,ENV_NAME=myenv,ENV_FILE=my.yml myjob.slurm
ENV_NAME="${ENV_NAME:-tenure_net}"
ENV_FILE="${ENV_FILE:-environment-tenure_net.yml}"
export ENV_NAME ENV_FILE SLURM_SUBMIT_DIR

test -f "${ENV_FILE}" || { echo "ERROR: missing ${ENV_FILE} in ${PWD}" >&2; exit 1; }

# Matches #SBATCH --output/--error slurm-%x-%j.{out,err}
OUT_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
ERR_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo "==> Watch this job live (from another terminal, same directory):"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${OUT_FILE}"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${ERR_FILE}"
echo ""

# Idempotent: create once, update on later runs (avoids "environment already exists").
if conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
  echo "==> Env ${ENV_NAME} exists; updating from ${ENV_FILE}"
  run conda env update -n "${ENV_NAME}" -f "${ENV_FILE}" --prune --verbose
else
  echo "==> Creating env from ${ENV_FILE} (name comes from YAML; expect ${ENV_NAME})"
  run conda env create -f "${ENV_FILE}" --verbose
fi

echo "==> Main env step finished. Activate with: conda activate ${ENV_NAME}"

# =============================================================================
# PUT YOUR CODE BELOW HERE  (runs in this job after env create/update)
# =============================================================================
# Uncomment and edit, or leave empty and use myjob.local.sh instead (sourced next).
#
# Example:
  conda run -n "${ENV_NAME}" pip install --no-input "pydantic==2.10.6" "pydantic-settings==2.6.1"
  conda run -n "${ENV_NAME}" python -c "import pydantic; print('pydantic OK', pydantic.__version__)"
#
# =============================================================================

# Optional extra commands (pins, one-off pip, etc.): copy myjob.local.sh.example → myjob.local.sh
LOCAL_HOOK="${SLURM_SUBMIT_DIR}/myjob.local.sh"
if [[ -f "${LOCAL_HOOK}" ]]; then
  echo "==> Sourcing ${LOCAL_HOOK}"
  # shellcheck source=/dev/null
  source "${LOCAL_HOOK}"
else
  echo "==> No myjob.local.sh (optional). Copy myjob.local.sh.example → myjob.local.sh to append steps."
fi

echo "==> Job complete."
