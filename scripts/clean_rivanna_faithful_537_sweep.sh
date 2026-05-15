#!/usr/bin/env bash
# Remove faithful-537 Rivanna sweep outputs and related Slurm logs so a new
# sim_job.slurm run starts from an empty rivanna_faithful_537/ tree.
#
# Deletes:
#   sports/outputs/simulation_sweeps/rivanna_faithful_537/
#   slurm_out/slurm-537_*.{out,err}  (Stage1 / merge_s1 / Stage2 / merge)
#   slurm_out/slurm-sim_job-*.{out,err}
#   Legacy repo-root slurm-537_* and slurm-sim_job-* (if present)
#
# Does NOT delete other jobs' logs under slurm_out/ (e.g. pipe_job). Use
#   ./scripts/clear_slurm.sh
# if you want every slurm-* log file removed.
#
# Usage (from repo root):
#   ./scripts/clean_rivanna_faithful_537_sweep.sh --dry-run
#   ./scripts/clean_rivanna_faithful_537_sweep.sh --yes
# Optional:
#   ./scripts/clean_rivanna_faithful_537_sweep.sh --yes --slurm-all
#     → also runs clear_slurm.sh (all slurm_out/* + root slurm-*)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

YES=0
DRY=0
SLURM_ALL=0
for arg in "$@"; do
  case "$arg" in
    --yes) YES=1 ;;
    --dry-run) DRY=1 ;;
    --slurm-all) SLURM_ALL=1 ;;
    -h|--help)
      sed -n '1,30p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (use --help)" >&2
      exit 2
      ;;
  esac
done

MARKER="${REPO_ROOT}/sports/outputs/simulation_sweeps/faithful_537_sweep_rivanna_worker.py"
if [[ ! -f "$MARKER" ]]; then
  echo "ERROR: expected Ivy_Net repo (missing ${MARKER})" >&2
  exit 1
fi

if [[ "$DRY" == 0 && "$YES" != 1 ]]; then
  echo "ERROR: refusing to delete without --yes (preview with --dry-run)" >&2
  exit 1
fi

SWEEP_OUT="${REPO_ROOT}/sports/outputs/simulation_sweeps/rivanna_faithful_537"

rm_target() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    return 0
  fi
  if [[ "$DRY" == 1 ]]; then
    echo "[dry-run] would remove: ${path}"
  else
    echo "Removing: ${path}"
    rm -rf "$path"
  fi
}

rm_target "$SWEEP_OUT"

shopt -s nullglob
hits=(
  "${REPO_ROOT}/slurm_out/slurm-537_"*.out
  "${REPO_ROOT}/slurm_out/slurm-537_"*.err
  "${REPO_ROOT}/slurm_out/slurm-sim_job-"*.out
  "${REPO_ROOT}/slurm_out/slurm-sim_job-"*.err
  "${REPO_ROOT}/slurm-537_"*.out
  "${REPO_ROOT}/slurm-537_"*.err
  "${REPO_ROOT}/slurm-sim_job-"*.out
  "${REPO_ROOT}/slurm-sim_job-"*.err
)
shopt -u nullglob

for f in "${hits[@]+"${hits[@]}"}"; do
  if [[ "$DRY" == 1 ]]; then
    echo "[dry-run] would remove file: ${f}"
  else
    echo "Removing: ${f}"
    rm -f "$f"
  fi
done

if [[ "$SLURM_ALL" == 1 ]]; then
  if [[ "$DRY" == 1 ]]; then
    echo "[dry-run] would also run: ${SCRIPT_DIR}/clear_slurm.sh"
  else
    echo "Running: ${SCRIPT_DIR}/clear_slurm.sh"
    bash "${SCRIPT_DIR}/clear_slurm.sh"
  fi
fi

if [[ "$DRY" == 1 ]]; then
  echo "[dry-run] done."
else
  echo "Done. You can submit: sbatch sim_job.slurm"
fi
