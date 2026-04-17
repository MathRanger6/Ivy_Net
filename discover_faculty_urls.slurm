#!/bin/bash
# Automated faculty URL discovery — queries Wayback Machine CDX API for all
# low-quality schools and surfaces ranked candidate URLs to investigate.
#
# Algorithm: uses CDX matchType=domain (one query per university apex domain)
# to discover ALL subdomains at once, mirroring the manual "start at the
# university homepage, navigate to wherever CS lived that year" workflow.
#
# Reads  : tenure/tenure_pipeline/faculty_snapshots_strategy_audit.jsonl
#          tenure/tenure_pipeline/r1_cs_departments.csv
#          tenure/tenure_pipeline/faculty_snapshots_plan.jsonl  (optional)
#
# Writes : tenure/tenure_pipeline/faculty_url_suggestions.jsonl
#          tenure/tenure_pipeline/faculty_url_suggestions.csv
#          (also writes rich progress to the slurm .out log in real time)
#
# Submit from Ivy_Net repo root:
#   cd ~/Ivy_Net && sbatch discover_faculty_urls.slurm
#
# Monitor live:
#   ./scripts/track_slurm.sh          # auto-finds the most recent job
#   ./scripts/track_slurm.sh <JOBID>  # specific job
#   tail -f slurm-discover_urls-<JOBID>.out
#
# To enable live test-parse (downloads + HTML-parses one Wayback snapshot per
# candidate — adds real faculty record counts but ~3–5s extra per candidate):
#   TEST_PARSE=1 sbatch discover_faculty_urls.slurm
#
# Runtime notes:
#   - The CDX matchType=domain query for one large university can take 5–15s
#     because it returns tens of thousands of URLs across all subdomains.
#   - With 36 low-quality schools and polite CDX delays (1.5s between domains,
#     3s between schools), expect 2–3 hours total.
#   - The job is all network I/O — 1 CPU and 4GB RAM is plenty.
#   - If the CDX API is unreachable (e.g. Wayback is down), the preflight
#     check will fail fast and the job will exit cleanly with an error.
#   - Checkpoint/resume: each school's results are written to the JSONL output
#     file immediately as it finishes (same pattern as the OpenAlex cache builder).
#     If the job is cancelled mid-run, re-submit — it will skip schools already
#     in faculty_url_suggestions.jsonl and resume from where it left off.
#     To force a full re-run from scratch, delete faculty_url_suggestions.jsonl
#     before submitting.
#   - Time limit: 4h.  Typical runtime is 2–3h (no TEST_PARSE).

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1        # pure network I/O — 1 CPU is all we need
#SBATCH --time=04:00:00          # 4h limit; typical is 2–3h
#SBATCH --mem=4G                 # CDX results fit easily; 4G is generous
#SBATCH --partition=standard
#SBATCH --job-name=discover_urls
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

# Pass through TEST_PARSE if the caller set it (e.g. TEST_PARSE=1 sbatch ...)
export TEST_PARSE="${TEST_PARSE:-0}"

ENV_NAME="${ENV_NAME:-tenure_net}"
SCRIPT="tenure/tenure_pipeline/discover_faculty_urls.py"
CONDA_PYTHON="${HOME}/.conda/envs/${ENV_NAME}/bin/python"

# Line-buffer stdout/stderr so tail -f gives real-time output in the log
if command -v stdbuf >/dev/null 2>&1; then
    run() { stdbuf -oL -eL "$@"; }
else
    run() { "$@"; }
fi

# ── Pre-flight checks ─────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════════════"
echo "  Faculty URL Discovery — Slurm Job ${SLURM_JOB_ID}"
echo "  Node       : ${SLURMD_NODENAME:-unknown}"
echo "  Started    : $(date)"
echo "  Submit dir : ${SLURM_SUBMIT_DIR}"
echo "  Script     : ${SCRIPT}"
echo "  Python     : ${CONDA_PYTHON}"
echo "  TEST_PARSE : ${TEST_PARSE}  (1 = download+parse one snapshot per candidate)"
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

[[ -f "tenure/tenure_pipeline/faculty_snapshots_strategy_audit.jsonl" ]] || {
    echo "ERROR: faculty_snapshots_strategy_audit.jsonl not found." >&2
    echo "       Run Cell 4 in 540_tenure_pipeline.ipynb first." >&2
    exit 1
}

[[ -f "tenure/tenure_pipeline/r1_cs_departments.csv" ]] || {
    echo "ERROR: r1_cs_departments.csv not found." >&2
    exit 1
}

# ── Run ───────────────────────────────────────────────────────────────────────
run "${CONDA_PYTHON}" "${SCRIPT}"

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  Job complete: $(date)"
echo "  Output files written to:"
echo "    tenure/tenure_pipeline/faculty_url_suggestions.jsonl"
echo "    tenure/tenure_pipeline/faculty_url_suggestions.csv"
echo "════════════════════════════════════════════════════════════════════"
