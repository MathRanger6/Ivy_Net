#!/bin/bash
#SBATCH --job-name=537_merge_s1
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag
#
# Concatenate Stage 1 shard CSVs → rivanna_faithful_537/stage1_results.csv
# N_STAGE1_SHARDS must match rivanna_stage1_faithful_537.slurm array size.

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

echo "==> Job       : ${SLURM_JOB_NAME} ${SLURM_JOB_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> Python    : ${CONDA_PYTHON}"
echo "==> Stage1 shards: ${N_STAGE1_SHARDS}"
echo ""

run "${CONDA_PYTHON}" sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py \
  merge-stage1 \
  --n-shards "$N_STAGE1_SHARDS"
