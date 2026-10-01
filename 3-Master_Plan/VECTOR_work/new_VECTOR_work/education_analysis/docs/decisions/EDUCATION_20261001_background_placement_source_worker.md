# Romania 2001 placement-source worker: operating boundary

**Date:** October 1, 2026  
**Purpose:** Recover archived *placement source records* while dissertation model-chapter writing proceeds. This is source acquisition, not a national analysis.

## What the worker does

The [worker](../../code/EDUCATION_20261001_romania_background_placement_worker.py) reads the frozen county placement-gap inventory and the saved program-occupancy counts. For each incomplete county, it requests only destination-program reports whose lowest admitted score is at or below the last score on the saved county placement page. It stores the archived pages, URLs, row counts, and hashes in `~/Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1/alternate_report_pilot/`, outside Dropbox and Git. Verified pages are reused on the next run.

After each county, it writes only aggregate, name-free status to [placement_county_status.csv](../../outputs/romania_2001_national_source_recovery/placement_county_status.csv). A county earns **`placement_views_reconciled`** only when every targeted program report matches its independent occupancy count, there are no duplicate printed-name-plus-score signatures across those reports, and the distinct signatures absent from the saved county pages equal the independently measured placement gap. This status describes placement *source views only*. It does not establish applicant-roster completeness, complete origin-gymnasium cohorts, valid person linkage, or readiness for research analysis.

Every other case remains **`unresolved`**. HTTP 404 addresses are recorded in the private `alternate_report_pilot/unresolved_requests.json` and skipped on ordinary resumes, preserving them for alternative-capture or redundant-view searches. They are not declared unavailable. Other failures remain unresolved too. HTTP 429 stops the entire run rather than pressing the archive. Charles retains the decision on when a source path has been exhausted and when to authorize analysis.

## Run and monitor

**Recommended for Charles:** open the dedicated [source-recovery notebook](../../notebooks/EDUCATION_20261001_Romania_2001_background_placement_source_recovery.ipynb) in Cursor with the `sports_net` kernel. Cell 1 exposes the county, run limit, pacing, and retry settings. Cell 3 previews the queue without network access. Set `RUN_SOURCE_ACQUISITION = True` in Cell 1 and run Cell 4 to see every request, saved page, wait reason, county reconciliation, and unresolved item directly below that cell. Cell 5 displays the aggregate county status. You can keep this notebook running while working on the chapter elsewhere. Interrupting the cell preserves completed page checkpoints; the current county status may lag until the next county checkpoint.

The same worker can also run in a visible Cursor terminal. Press **Control-C once** to request a graceful stop; the worker finishes the current request or wait and writes the county status before exiting. A verified page is never discarded on resume.

```zsh
cd "3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/code"
/usr/bin/caffeinate -i /opt/anaconda3/envs/sports_net/bin/python -u EDUCATION_20261001_romania_background_placement_worker.py --run --counties NT --max-new-pages 40 --max-hours 2
```

Omit `--counties NT` after Neamț if you want the worker's small-county-first queue. It will reread and verify Neamț's saved pages before fetching anything new. The `--max-new-pages` and `--max-hours` bounds limit each run; neither means the data are unavailable.

The worker previews its county queue unless `--run` is supplied. The [launcher](../../code/start_romania_placement_worker.sh) starts a bounded run from a **Cursor terminal** and writes a private log and process ID under `~/Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1/background_worker/`. It asks macOS to prevent idle sleep while the worker runs; closing the laptop lid can still suspend it. The default run limit is 40 new pages or two hours, whichever comes first. Rerunning safely resumes from verified checkpoints. The next county after the Vaslui and Olt pilots is Neamț.

```zsh
cd "3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/code"
./start_romania_placement_worker.sh 40 2
```

The launcher prints the exact log path and process ID. Follow that log with `tail -f 'LOG_PATH_PRINTED_BY_LAUNCHER'`. Stop with `kill PID_PRINTED_BY_LAUNCHER`; verified source pages remain saved. To work on one county, append `--counties NT`. To deliberately retry a previously recorded 404, append `--retry-unresolved` after reviewing the address. The worker never runs a national outcome, sorting, HERO, or congestion calculation.

**Current bounded live check:** The first Neamț run fetched its program index and one program report, verified the report's 25 rows against occupancy, and stopped at the requested two-page limit. A longer bounded run saved and verified 11 further Neamț program reports. Charles then requested direct control of execution, so the agent-run session was stopped while another request was in progress. That interrupted request was not checkpointed; it can be retried on resume. No county was declared complete. The aggregate CSV still reflects the first two-page checkpoint until a resumed run finishes or stops at a county boundary; the private page checkpoints contain the later saved reports.

## Scientific stopping gate

Placement recovery is only one of the source gates. The national candidate-roster gaps, unassigned-applicant gap, duplicate signatures, source fields, cross-county linkage, and origin-gymnasium applicant coverage still require a separate audit. No recovered placement count turns an unknown outcome into a failure or a missing applicant into a nonapplicant. National analyses and figures require source readiness **and Charles's explicit authorization**.
