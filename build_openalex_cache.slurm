#!/bin/bash
# Build the OpenAlex snapshot cache — one-time run, estimated 3–5 hours.
#
# Reads  : tenure/tenure_pipeline/openalex_author_ids.jsonl
#          ~/cdh/OpenAlex1125/publicationauthoraffiliation/*.csv.gz
#          ~/cdh/OpenAlex1125/pub2year.csv.gz
#
# Writes : tenure/tenure_pipeline/openalex_snapshot_cache.jsonl  (incremental, safe to interrupt)
#          tenure/tenure_pipeline/openalex_works_by_year.jsonl   (incremental, safe to interrupt)
#
# Submit from Ivy_Net repo root:
#   cd ~/Ivy_Net && sbatch build_openalex_cache.slurm
#
# Monitor live:
#   ./scripts/track_slurm.sh          # auto-finds the most recent job
#   ./scripts/track_slurm.sh <JOBID>  # specific job
#
# Notes:
#   - If the job is cancelled mid-run, re-submit — it will resume from where
#     it left off (authors already in the cache are skipped automatically).
#   - Time limit is 12h to be safe; typical runtime is 3–5h.
#   - 32G RAM needed to hold the PAA hit table in memory during the scan phase.

#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --partition=standard
#SBATCH --job-name=oa_cache
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge

cd "${SLURM_SUBMIT_DIR}"

export PYTHONUNBUFFERED=1
# Optional: override snapshot root if it ever moves
# export OPENALEX_SNAPSHOT_ROOT=~/cdh/OpenAlex1125

ENV_NAME="${ENV_NAME:-tenure_net}"
SCRIPT="tenure/tenure_pipeline/build_openalex_cache.py"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"

# Line-buffer stdout/stderr so tail -f gives real-time output
if command -v stdbuf >/dev/null 2>&1; then
    run() { stdbuf -oL -eL "$@"; }
else
    run() { "$@"; }
fi

# ── Pre-flight checks ─────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════════════"
echo "  OpenAlex Cache Builder — Slurm Job ${SLURM_JOB_ID}"
echo "  Node      : ${SLURMD_NODENAME:-unknown}"
echo "  Started   : $(date)"
echo "  Submit dir: ${SLURM_SUBMIT_DIR}"
echo "  Script    : ${SCRIPT}"
echo "  Python    : ${CONDA_PYTHON}"
echo "════════════════════════════════════════════════════════════════════"
echo ""

[[ -x "${CONDA_PYTHON}" ]] || {
    echo "ERROR: Python not found at ${CONDA_PYTHON}" >&2
    echo "       Is the '${ENV_NAME}' conda env installed?" >&2
    exit 1
}

[[ -f "${SCRIPT}" ]] || {
    echo "ERROR: Script not found: ${SLURM_SUBMIT_DIR}/${SCRIPT}" >&2
    exit 1
}

# ── Run ───────────────────────────────────────────────────────────────────────
run "${CONDA_PYTHON}" "${SCRIPT}"

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  Job complete: $(date)"
echo "════════════════════════════════════════════════════════════════════"
