#!/bin/bash
#SBATCH --job-name=538_stage1
#SBATCH --partition=standard
#SBATCH --array=0-63
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=slurm_out/slurm-%x-%A_%a.out
#SBATCH --error=slurm_out/slurm-%x-%A_%a.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag
#
# Stage 1 broad screen (538 generative soft assign + selection), sharded (default 64).
# Submit from Ivy_Net repo root. Keep #SBATCH --array in sync with N_STAGE1_SHARDS.
# Pilot grid (~96 scenarios):  PILOT=1 sbatch ... (adds --pilot to worker).
# Requires sports/datasets/mbb/empirical_perf_fit.json when grid uses empirical_530.

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

N_STAGE1_SHARDS="${N_STAGE1_SHARDS:-64}"
PILOT_FLAG=()
if [[ "${PILOT:-0}" == "1" ]]; then
  PILOT_FLAG=(--pilot)
fi

echo "==> Job       : ${SLURM_JOB_NAME} ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> Python    : ${CONDA_PYTHON}"
echo "==> Shard     : ${SLURM_ARRAY_TASK_ID}/${N_STAGE1_SHARDS}  PILOT=${PILOT:-0}"
echo "==> Watch live:"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm_out/slurm-${SLURM_JOB_NAME}-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out"
echo "    tail -f ${SLURM_SUBMIT_DIR}/slurm_out/slurm-${SLURM_JOB_NAME}-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err"
echo ""

run "${CONDA_PYTHON}" sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py \
  stage1-shard \
  --shard-id "$SLURM_ARRAY_TASK_ID" \
  --n-shards "$N_STAGE1_SHARDS" \
  "${PILOT_FLAG[@]}" \
  --reset
