#!/bin/bash
# Faithful 537 parameter sweep — full pipeline in one submission.
# Submits: Stage 1 array → Merge Stage 1 → Stage 2 array → final merge (grouped CSV + plots).
#
# Submit from the Ivy_Net repo root (same as pipe_job.slurm):
#   cd /path/to/Ivy_Net && sbatch sim_job.slurm
#
# This driver job stays RUNNING until all child jobs finish (--wait), so give it a wall
# time that covers the slowest Stage 1/2 shards plus merges (see #SBATCH --time below).
#
# Optional overrides (export before sbatch):
#   N_STAGE1_SHARDS=64   — must match #SBATCH --array in rivanna_stage1_faithful_537.slurm
#   N_SHARDS=64         — must match Stage 2 array + rivanna_merge_faithful_537.slurm
#   ENV_NAME=sports_net — Python conda env for worker scripts
#
# Monitor driver logs (under repo slurm_out/):
#   tail -f slurm_out/slurm-sim_job-<JOBID>.out
#   tail -f slurm_out/slurm-sim_job-<JOBID>.err
#
# Child jobs (sbatch from this driver) use the same submit directory — logs are also under slurm_out/.

#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --partition=standard
#SBATCH --job-name=sim_job
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge
SLURM_SUBMIT_DIR = "~/Ivy_Net"
cd "${SLURM_SUBMIT_DIR}"

export PYTHONUNBUFFERED=1

export N_STAGE1_SHARDS="${N_STAGE1_SHARDS:-64}"
export N_SHARDS="${N_SHARDS:-64}"
export ENV_NAME="${ENV_NAME:-sports_net}"

if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

SWEEP="sports/outputs/simulation_sweeps"
WORKER="${SWEEP}/faithful_537_sweep_rivanna_worker.py"
STAGE1="${SWEEP}/rivanna_stage1_faithful_537.slurm"
MERGE1="${SWEEP}/rivanna_merge_stage1_faithful_537.slurm"
STAGE2="${SWEEP}/rivanna_stage2_array_faithful_537.slurm"
MERGE2="${SWEEP}/rivanna_merge_faithful_537.slurm"

for f in "$WORKER" "$STAGE1" "$MERGE1" "$STAGE2" "$MERGE2"; do
  test -f "$f" || {
    echo "ERROR: missing $f (cwd=${PWD})" >&2
    exit 1
  }
done

echo "==> Driver    : sim_job ${SLURM_JOB_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> N_STAGE1_SHARDS=${N_STAGE1_SHARDS}  N_SHARDS=${N_SHARDS}  ENV_NAME=${ENV_NAME}"
echo ""
echo "==> Pipeline  : Stage1 array → merge-stage1 → Stage2 array → merge (plots)"
echo ""

# --export=ALL forwards this job's environment (incl. N_STAGE1_SHARDS, N_SHARDS, ENV_NAME)
# to child sbatch jobs so their Slurm scripts see the same shard counts.
submit_wait() {
  local label="$1"
  local script="$2"
  echo "--------------------------------------------------------------------"
  echo "==> ${label}: sbatch --wait ${script}"
  local jid
  jid="$(sbatch --parsable --wait --export=ALL "$script")"
  echo "==> ${label} finished (job ${jid})"
  echo ""
}

submit_wait "Stage 1 array" "$STAGE1"
submit_wait "Merge Stage 1" "$MERGE1"
submit_wait "Stage 2 array" "$STAGE2"
submit_wait "Final merge" "$MERGE2"

echo "==> All sweep stages complete."
echo "==> Results   : ${SWEEP}/rivanna_faithful_537/grouped_candidates.csv"
