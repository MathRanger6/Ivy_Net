#!/usr/bin/env bash
# Remove faithful-538 Rivanna sweep outputs and related Slurm logs so a new
# sim_job_538.slurm run starts from an empty rivanna_faithful_538/ tree.
#
# Deletes:
#   sports/outputs/simulation_sweeps/rivanna_faithful_538/
#   slurm_out/slurm-538_*.{out,err}
#   slurm_out/slurm-sim_job_538-*.{out,err}
#   Legacy repo-root slurm-538_* and slurm-sim_job_538-* (if present)
#
# Does NOT delete 537 sweep outputs or other jobs' logs under slurm_out/.
#
# Usage (from repo root):
#   ./scripts/clean_rivanna_faithful_538_sweep.sh --dry-run
#   ./scripts/clean_rivanna_faithful_538_sweep.sh --yes
# Optional:
#   ./scripts/clean_rivanna_faithful_538_sweep.sh --yes --slurm-all

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
      sed -n '1,25p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (use --help)" >&2
      exit 2
      ;;
  esac
done

MARKER="${REPO_ROOT}/sports/outputs/simulation_sweeps/faithful_538_sweep_rivanna_worker.py"
if [[ ! -f "$MARKER" ]]; then
  echo "ERROR: expected Ivy_Net repo (missing ${MARKER})" >&2
  exit 1
fi

if [[ "$DRY" == 0 && "$YES" != 1 ]]; then
  echo "ERROR: refusing to delete without --yes (preview with --dry-run)" >&2
  exit 1
fi

SWEEP_OUT="${REPO_ROOT}/sports/outputs/simulation_sweeps/rivanna_faithful_538"

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
  "${REPO_ROOT}/slurm_out/slurm-538_"*.out
  "${REPO_ROOT}/slurm_out/slurm-538_"*.err
  "${REPO_ROOT}/slurm_out/slurm-sim_job_538-"*.out
  "${REPO_ROOT}/slurm_out/slurm-sim_job_538-"*.err
  "${REPO_ROOT}/slurm-538_"*.out
  "${REPO_ROOT}/slurm-538_"*.err
  "${REPO_ROOT}/slurm-sim_job_538-"*.out
  "${REPO_ROOT}/slurm-sim_job_538-"*.err
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
  echo "Done. You can submit: sbatch sim_job_538.slurm"
fi
