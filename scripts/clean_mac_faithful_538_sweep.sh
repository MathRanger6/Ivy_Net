#!/usr/bin/env bash
# Remove local (Mac) faithful-538 sweep outputs so rsync_pull starts fresh.
#
# Deletes under sports/outputs/simulation_sweeps/:
#   rivanna_faithful_538/          (pulled HPC tree: shards, CSVs, plots)
#   faithful_538_candidate_plots/  (local plot_top output)
#   faithful_538_sweep_results.jsonl
#   faithful_538_sweep_stage*_results.csv
#   faithful_538_sweep_grouped_candidates.csv
#   faithful_538_sweep_README.md
#
# Optional: slurm_out/slurm-538_* and slurm-sim_job_538-* (from rsync_pull logs)
#
# Does NOT delete sweep source code (.py, .slurm) or 537 outputs.
#
# Usage (from repo root):
#   ./scripts/clean_mac_faithful_538_sweep.sh --dry-run
#   ./scripts/clean_mac_faithful_538_sweep.sh --yes
#   ./scripts/clean_mac_faithful_538_sweep.sh --yes --slurm-logs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

YES=0
DRY=0
SLURM_LOGS=0
for arg in "$@"; do
  case "$arg" in
    --yes) YES=1 ;;
    --dry-run) DRY=1 ;;
    --slurm-logs) SLURM_LOGS=1 ;;
    -h|--help)
      sed -n '1,22p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (use --help)" >&2
      exit 2
      ;;
  esac
done

MARKER="${REPO_ROOT}/sports/outputs/simulation_sweeps/faithful_538_sweep.py"
if [[ ! -f "$MARKER" ]]; then
  echo "ERROR: expected Ivy_Net repo (missing ${MARKER})" >&2
  exit 1
fi

if [[ "$DRY" == 0 && "$YES" != 1 ]]; then
  echo "ERROR: refusing to delete without --yes (preview with --dry-run)" >&2
  exit 1
fi

SWEEP="${REPO_ROOT}/sports/outputs/simulation_sweeps"

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

rm_target "${SWEEP}/rivanna_faithful_538"
rm_target "${SWEEP}/faithful_538_candidate_plots"
rm_target "${SWEEP}/faithful_538_sweep_results.jsonl"
rm_target "${SWEEP}/faithful_538_sweep_README.md"
rm_target "${SWEEP}/faithful_538_sweep_grouped_candidates.csv"

shopt -s nullglob
for f in "${SWEEP}"/faithful_538_sweep_stage*_results.csv; do
  rm_target "$f"
done
shopt -u nullglob

if [[ "$SLURM_LOGS" == 1 ]]; then
  shopt -s nullglob
  hits=(
    "${REPO_ROOT}/slurm_out/slurm-538_"*.out
    "${REPO_ROOT}/slurm_out/slurm-538_"*.err
    "${REPO_ROOT}/slurm_out/slurm-sim_job_538-"*.out
    "${REPO_ROOT}/slurm_out/slurm-sim_job_538-"*.err
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
fi

if [[ "$DRY" == 1 ]]; then
  echo "[dry-run] done."
else
  echo "Done. After the HPC run finishes: ./scripts/rsync_pull_from_hpc.sh sweep"
fi
