#!/usr/bin/env bash
# Clear stuck KAC/RNF agent review state for Ivy_Net / Cursor Workspace PDE.
# Does NOT change repo files — only Cursor globalStorage (state.vscdb).
#
# Usage:
#   1. Cmd+Q Cursor (fully quit).
#   2. bash scripts/clear_cursor_stale_inline_diffs_pde.sh
#      (Use bash — Dropbox often strips the executable bit on ./scripts/…)
#   3. Reopen the project.

set -euo pipefail

DB="${HOME}/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
BACKUP_DIR="${HOME}/Desktop/cursor-state-backup-$(date +%Y%m%d_%H%M%S)"
PDE_MARKER="Cursor Workspace PDE"

# Workspace folder IDs used when opening Ivy_Net.code-workspace or PDE.code-workspace
WS_IDS=(
  bfed3a4f2453313cc2cfe74174ac3c0c
  01d95967f78aa1d64ab7f191f7bf05ea
  7a28434a41bdc33dd6a1ad05df3e4ef7
  77c302e1c9b985f31805a63e9efab271
)

if [[ ! -f "$DB" ]]; then
  echo "No state.vscdb at: $DB"
  exit 1
fi

if pgrep -x "Cursor" >/dev/null 2>&1 || pgrep -f "/Applications/Cursor.app" >/dev/null 2>&1; then
  echo "Cursor is still running. Cmd+Q Cursor, then run this script again."
  exit 1
fi

mkdir -p "$BACKUP_DIR"
cp "$DB" "$BACKUP_DIR/state.vscdb"
[[ -f "${DB}.backup" ]] && cp "${DB}.backup" "$BACKUP_DIR/state.vscdb.backup"
echo "Backup: $BACKUP_DIR"

before="$(sqlite3 "$DB" "SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'inlineDiff:%' AND value LIKE '%${PDE_MARKER}%';")"
echo "Pending inlineDiff rows for ${PDE_MARKER}: ${before}"

sqlite3 "$DB" <<SQL
BEGIN;
DELETE FROM cursorDiskKV
WHERE key LIKE 'inlineDiff:%' AND value LIKE '%${PDE_MARKER}%';
SQL

for ws in "${WS_IDS[@]}"; do
  sqlite3 "$DB" <<SQL
DELETE FROM cursorDiskKV WHERE key LIKE 'inlineDiff:${ws}:%';
DELETE FROM cursorDiskKV WHERE key LIKE 'inlineDiffUndoRedo:${ws}:%';
DELETE FROM cursorDiskKV WHERE key LIKE 'patch-graph:${ws}:%';
DELETE FROM cursorDiskKV WHERE key LIKE 'expectedContent-v1-${ws}-%';
SQL
done

after="$(sqlite3 "$DB" "SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'inlineDiff:%' AND value LIKE '%${PDE_MARKER}%';")"
echo "After cleanup: ${after} (was ${before})"
echo "Relaunch Cursor and open a .py file — KAC/RNF should be gone."
