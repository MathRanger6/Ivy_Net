#!/bin/bash
# =============================================================================
# pipe_job_beau.slurm — Rivanna starter batch script for Beau
# Lives in: Ivy_Net/5-Manuscript/Beau_guide/
# =============================================================================
#
# OVERVIEW (read this block once)
# -------------------------------
# This submits ONE Slurm job that runs your Jupyter notebook from top to bottom
# on a compute node (not the login node).  The notebook itself decides what to
# execute using RUN_CELL* booleans in Cell 0 — same pattern as Charles's pipeline.
#
# You maintain ONE notebook file; edit Cell 0 before submitting to choose stages.
#
# STEP-BY-STEP — FIRST TIME ON RIVANNA
# --------------------------------------
#  1. SSH to Rivanna (FastX/Open OnDemand as usual).
#  2. Clone or copy the Ivy_Net repo into the path YOU want (example below).
#  3. Create a conda env with notebook deps (pandas, jupyter, papermill, …).
#       module load miniforge
#       conda create -n tenure_net python=3.11  # name must match ENV_NAME below or override at sbatch time
#       conda activate tenure_net
#       pip install papermill jupyter pandas …   # match Charles's env / pyproject / requirements if provided
#  4. EDIT THE PLACEHOLDERS in this file (search for "YOUR_" and "## EDIT").
#  5. Submit (recommended — logs land in Ivy_Net repo root next to tenure/):
#       cd /your/path/to/Ivy_Net
#       sbatch 5-Manuscript/Beau_guide/pipe_job_beau.slurm
#     The script walks upward from your submit directory to find functionsG_working.py
#     and cds there before running papermill — NB_IN paths stay correct even though
#     this .slurm file lives under 5-Manuscript/Beau_guide/.
#  6. Watch logs (JOBID = number Slurm prints after sbatch; logs follow SLURM_SUBMIT_DIR):
#       tail -f slurm-<job_name>-<JOBID>.out    # stdout — prints & echoes
#       tail -f slurm-<job_name>-<JOBID>.err    # stderr — tqdm/progress often HERE (see guide)
#       chmod +x 5-Manuscript/Beau_guide/track_slurm_beau.sh    # once
#       ./5-Manuscript/Beau_guide/track_slurm_beau.sh <JOBID>    # tail -f on the right .err
#
# STEP-BY-STEP — EVERY RUN AFTER THAT
# ------------------------------------
#  • Open 5-Manuscript/Beau_guide/540_tenure_pipeline_beau.ipynb (format example)
#    OR tenure/540_tenure_pipeline.ipynb — match NB_IN below.
#  • Set RUN_CELL* flags in Cell 0.
#  • Save.
#  • cd /your/path/to/Ivy_Net && sbatch 5-Manuscript/Beau_guide/pipe_job_beau.slurm
#
# OUTPUT FILES — Slurm writes these relative to WHERE YOU RAN SBATCH (--output/--error).
# Recommended: submit from Ivy_Net root so logs match Charles's layout:
# ------------------------------------------------------------------------
#   slurm-<job_name>-<JOBID>.out   ← stdout (normal prints).  Watch live:
#       tail -f slurm-<job_name>-<JOBID>.out
#       (“tail” = show end of file; “-f” = keep streaming new lines as Slurm writes them.)
#   slurm-<job_name>-<JOBID>.err   ← stderr (NOT “errors only”: tqdm bars & warnings land here).
#       Often feels more active than .out — same tail -f pattern as above.
#   slurm-<job_name>-<JOBID>-output.ipynb ← executed notebook WITH outputs (written under Ivy_Net root after cd)
#
# =============================================================================

# -----------------------------------------------------------------------------
# ## EDIT — Slurm resources (Rivanna)
# Insert walltime you need; job dies when limit hits (--time).
# -----------------------------------------------------------------------------
#SBATCH --time=6:00:00

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

# ## EDIT — CPUs you want visible inside Python (numpy/pandas threads).
#SBATCH --cpus-per-task=8

# ## EDIT — RAM for the whole notebook process (pandas spikes — round up).
#SBATCH --mem=64G

# ## EDIT — Partition: Rivanna commonly uses standard / parallel / gpu ; pick yours from docs/sacctmgr.
#SBATCH --partition=standard

# ## EDIT — Short label for logs and squeue (letters/numbers/underscore OK).
#SBATCH --job-name=pipe_job_beau

# Log filenames become slurm-<job-name>-<JOBID>.{out,err} (relative to sbatch cwd).
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err

# ## EDIT — Slurm emails when job ends or fails (UVA NetID email).
#SBATCH --mail-user=YOUR_NETID@virginia.edu
#SBATCH --mail-type=END,FAIL

# Rivanna hardware pool — keep unless RC tells you otherwise.
#SBATCH --constraint=rivanna

# ## EDIT — Billing group / PI allocation string (required on Rivanna).
#     Find yours: https://www.rc.virginia.edu/userinfo/rivanna/slurm/ or run `accounts` / ask PI.
#SBATCH --account=YOUR_SLURM_ALLOCATION

set -euo pipefail

# Resolve Ivy_Net repo root (directory containing functionsG_working.py) so NB_IN works
# regardless of whether this script lives under 5-Manuscript/Beau_guide/.
_find_ivy_net_root_from() {
  local d
  d="$(cd "${SLURM_SUBMIT_DIR}" && pwd)"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/functionsG_working.py" ]]; then
      printf '%s\n' "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

IVY_NET_ROOT="$(_find_ivy_net_root_from)" || {
  echo "ERROR: Cannot find Ivy_Net repo root (expected functionsG_working.py walking up from ${SLURM_SUBMIT_DIR})." >&2
  exit 1
}

cd "${IVY_NET_ROOT}"

# ## EDIT — Module that provides conda on Rivanna (usually miniforge).
module load miniforge

export PYTHONUNBUFFERED=1

if command -v stdbuf >/dev/null 2>&1; then
  run() { stdbuf -oL -eL "$@"; }
else
  run() { "$@"; }
fi

# ## EDIT — Conda environment NAME you created for this project.
ENV_NAME="${ENV_NAME:-tenure_net}"

# ## EDIT — Notebook path RELATIVE to Ivy_Net root after cd (papermill executes this file).
# Default is the Beau_guide COPY showing Cell 0 + RUN_CELL* layout — swap for Charles production notebook:
#   NB_IN="tenure/540_tenure_pipeline.ipynb"
NB_IN="5-Manuscript/Beau_guide/540_tenure_pipeline_beau.ipynb"

# Executed notebook — names match Slurm job name + job ID so runs never overwrite.
NB_OUT="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}-output.ipynb"

command -v conda >/dev/null || { echo "ERROR: conda not on PATH after module load." >&2; exit 1; }
conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}" \
  || { echo "ERROR: conda env '${ENV_NAME}' not found. Create it once interactively." >&2; exit 1; }

test -f "${NB_IN}" || { echo "ERROR: ${NB_IN} not found in ${PWD}" >&2; exit 1; }

OUT_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.out"
ERR_FILE="slurm-${SLURM_JOB_NAME}-${SLURM_JOB_ID}.err"
echo "==> Repo root : ${IVY_NET_ROOT}"
echo "==> Notebook  : ${IVY_NET_ROOT}/${NB_IN}"
echo "==> Output nb : ${IVY_NET_ROOT}/${NB_OUT}   (executed copy with outputs)"
echo "==> Slurm logs (.out/.err) go next to sbatch cwd — usually repo root if you:"
echo "      cd ${IVY_NET_ROOT} && sbatch 5-Manuscript/Beau_guide/pipe_job_beau.slurm"
echo "==> Watch live (tail -f streams new lines as the job writes logs — Ctrl+C stops watching only):"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${OUT_FILE}"
echo "    tail -f ${SLURM_SUBMIT_DIR}/${ERR_FILE}"
echo ""
echo "==> Active RUN_CELL flags (parsed from CELL 0 of the notebook):"
python3 -c "
import json
nb = json.load(open('${NB_IN}', encoding='utf-8'))
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    for line in cell.get('source', []):
        l = line.strip().rstrip(',')
        if l.startswith('RUN_CELL') and '=' in l:
            print('   ', l)
" 2>/dev/null || true
echo ""

# ## EDIT — Only if conda installs envs somewhere non-default on Rivanna:
# CONDA_PREFIX_OVERRIDE="${HOME}/.conda/envs/${ENV_NAME}"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"
CONDA_PAPERMILL="${HOME}/.conda/envs/${ENV_NAME}/bin/papermill"
CONDA_NBCONVERT="${HOME}/.conda/envs/${ENV_NAME}/bin/jupyter"

if "${CONDA_PYTHON}" -c "import papermill" 2>/dev/null && [[ -x "${CONDA_PAPERMILL}" ]]; then
  echo "==> Executing via papermill …"
  run "${CONDA_PAPERMILL}" \
      --no-progress-bar \
      --log-output \
      --execution-timeout -1 \
      "${NB_IN}" "${NB_OUT}"
else
  echo "==> papermill not found — falling back to jupyter nbconvert …"
  run "${CONDA_NBCONVERT}" nbconvert \
      --to notebook \
      --execute \
      --ExecutePreprocessor.timeout=-1 \
      --output "${NB_OUT}" \
      "${NB_IN}"
fi

echo ""
echo "==> Job complete. Executed notebook saved to: ${NB_OUT}"
