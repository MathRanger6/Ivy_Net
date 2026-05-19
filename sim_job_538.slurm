#!/bin/bash
# Faithful 538 generative parameter sweep — full pipeline in one submission.
# Submits: Stage 1 array → Merge Stage 1 → Stage 2 array → final merge (grouped CSV + plots).
#
# Submit from the Ivy_Net repo root:
#   cd /path/to/Ivy_Net && sbatch sim_job_538.slurm
#
# Pilot grid (~96 Stage-1 scenarios):
#   PILOT=1 sbatch sim_job_538.slurm
#
# Wipe prior outputs:
#   ./scripts/clean_rivanna_faithful_538_sweep.sh --dry-run
#   ./scripts/clean_rivanna_faithful_538_sweep.sh --yes
#
# Prerequisite on Rivanna: sports/datasets/mbb/empirical_perf_fit.json (530 CELL 5b).
#
# Optional overrides:
#   N_STAGE1_SHARDS=64   — match rivanna_stage1_faithful_538.slurm --array
#   N_SHARDS=64          — Stage 2 array + final merge
#   ENV_NAME=sports_net
#   PILOT=1              — pilot grid instead of full ~51k Stage-1 scenarios

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --partition=standard
#SBATCH --job-name=sim_job_538
#SBATCH --output=slurm_out/slurm-%x-%j.out
#SBATCH --error=slurm_out/slurm-%x-%j.err
#SBATCH --mail-user=dzk3ja@virginia.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --constraint=rivanna
#SBATCH --account=sds_ag

set -euo pipefail

module load miniforge

cd "${SLURM_SUBMIT_DIR}"

export PYTHONUNBUFFERED=1

export N_STAGE1_SHARDS="${N_STAGE1_SHARDS:-64}"
export N_SHARDS="${N_SHARDS:-64}"
export ENV_NAME="${ENV_NAME:-sports_net}"
export PILOT="${PILOT:-0}"

if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

SWEEP="sports/outputs/simulation_sweeps"
WORKER="${SWEEP}/faithful_538_sweep_rivanna_worker.py"
STAGE1="${SWEEP}/rivanna_stage1_faithful_538.slurm"
MERGE1="${SWEEP}/rivanna_merge_stage1_faithful_538.slurm"
STAGE2="${SWEEP}/rivanna_stage2_array_faithful_538.slurm"
MERGE2="${SWEEP}/rivanna_merge_faithful_538.slurm"
FIT="sports/datasets/mbb/empirical_perf_fit.json"

for f in "$WORKER" "$STAGE1" "$MERGE1" "$STAGE2" "$MERGE2"; do
  test -f "$f" || {
    echo "ERROR: missing $f (cwd=${PWD})" >&2
    exit 1
  }
done

if [[ ! -f "$FIT" ]]; then
  echo "WARNING: missing ${FIT} — empirical_530 scenarios will fail." >&2
  echo "  Run 530 CELL 5b on Mac and push: ./scripts/rsync_push_to_hpc.sh sweep538-deps" >&2
fi

echo "==> Driver    : sim_job_538 ${SLURM_JOB_ID}"
echo "==> Work dir  : ${PWD}"
echo "==> N_STAGE1_SHARDS=${N_STAGE1_SHARDS}  N_SHARDS=${N_SHARDS}  ENV_NAME=${ENV_NAME}  PILOT=${PILOT}"
echo ""

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

echo "==> All 538 sweep stages complete."
echo "==> Results   : ${SWEEP}/rivanna_faithful_538/grouped_candidates.csv"
