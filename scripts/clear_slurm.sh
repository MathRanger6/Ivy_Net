#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
rm -f "$REPO_ROOT"/slurm_out/slurm-*.*
# Legacy: logs in repo root (older #SBATCH paths)
rm -f "$REPO_ROOT"/slurm-*.*
