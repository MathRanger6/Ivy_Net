#!/usr/bin/env bash
# SR re-scrape 2009–2021 + re-match. Safe alongside COMPASS PPM reruns.
set -euo pipefail
REPO="/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE"
LOG="$REPO/datasets/mbb/sr_rescrape_2009_21.log"
export PYTHONPATH="$REPO/sports"
cd "$REPO"
echo "=== SR rescrape 2009-21 started $(date '+%Y-%m-%d %H:%M:%S') ===" >>"$LOG"
python3 -u "$REPO/sports/scripts/sr_rescrape_2009_21_worker.py" >>"$LOG" 2>&1
echo "=== SR rescrape 2009-21 finished $(date '+%Y-%m-%d %H:%M:%S') ===" >>"$LOG"
