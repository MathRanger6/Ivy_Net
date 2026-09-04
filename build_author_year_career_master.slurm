#!/bin/bash
# PD29 career master — lightweight derive from openalex_works_by_year.jsonl
#
# Submit from Ivy_Net repo root:
#   cd ~/Ivy_Net && sbatch build_author_year_career_master.slurm
#
# Mac (no Slurm):
#   python tenure/tenure_pipeline/build_author_year_career_master.py

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=01:00:00
#SBATCH --mem=8G
#SBATCH --partition=standard
#SBATCH --job-name=career_master
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge
cd "${SLURM_SUBMIT_DIR}"

export PYTHONUNBUFFERED=1
ENV_NAME="${ENV_NAME:-tenure_net}"
SCRIPT="tenure/tenure_pipeline/build_author_year_career_master.py"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"

[[ -x "${CONDA_PYTHON}" ]] || { echo "ERROR: ${CONDA_PYTHON} missing" >&2; exit 1; }
[[ -f "${SCRIPT}" ]] || { echo "ERROR: ${SCRIPT} missing" >&2; exit 1; }

echo "Career master build — job ${SLURM_JOB_ID} — $(date)"
"${CONDA_PYTHON}" "${SCRIPT}"
echo "Complete — $(date)"
