#!/usr/bin/env python3
"""
tenure_pipeline/rebuild_plan.py
──────────────────────────────────────────────────────────────────────────────
Clean reset of the Wayback **plan** (and optionally the download **index**) so
Cell 3A will treat every URL in r1_schools_data.py as **unqueried** and run a
full CDX pass. Use this after Option B (per-source_id paths) when you want a
consistent plan without hand-editing JSONL.

Does **not** delete HTML under faculty_snapshots/ or parsed output — do that
manually if you need a full wipe.

Typical workflow
----------------
  python tenure_pipeline/rebuild_plan.py --force

Then in the notebook (kernel restarted if needed):
  Cell 0 → Cell 2 → Cell 3A (RUN_CELL3_CDX=True) → 3B → 4

Options
-------
  (default)            Backup and truncate plan + faculty_snapshots_index.jsonl.
  --plan-only          Truncate only the plan; keep the download index (3B may
                       still skip files that match old index + on-disk HTML).
  --clear-retry-queue  Also backup and empty cdx_retry_queue.jsonl.
  --dry-run            Print actions only.
  --force              Skip the confirmation prompt (for scripts / CI).

Backups are written under:
  tenure_pipeline/backups/plan_rebuild_<timestamp>/
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

TP = Path(__file__).resolve().parent
WORKSPACE = TP.parent

PLAN = TP / "faculty_snapshots_plan.jsonl"
INDEX = TP / "faculty_snapshots_index.jsonl"
RETRY_QUEUE = TP / "cdx_retry_queue.jsonl"


def _backup(src: Path, dest_dir: Path) -> Path | None:
    if not src.exists() or src.stat().st_size == 0:
        return None
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    return dest


def _truncate(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Backup and truncate Wayback plan/index so Cell 3A re-queries all school URLs.",
    )
    p.add_argument(
        "--plan-only",
        action="store_true",
        help="Truncate only the plan file; keep faculty_snapshots_index.jsonl.",
    )
    p.add_argument(
        "--clear-retry-queue",
        action="store_true",
        help="Also backup and empty cdx_retry_queue.jsonl.",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="Skip confirmation.")

    args = p.parse_args()
    full = not args.plan_only

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = TP / "backups" / f"plan_rebuild_{ts}"

    targets: list[tuple[str, Path]] = [("plan", PLAN)]
    if full:
        targets.append(("index", INDEX))
    if args.clear_retry_queue:
        targets.append(("retry queue", RETRY_QUEUE))

    print("Rebuild plan — will backup then truncate:")
    for label, path in targets:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        print(f"  • {label}: {path}  ({'empty' if not exists or size == 0 else f'{size:,} bytes'})")
    print(f"  • backup folder: {backup_root}")

    if args.dry_run:
        print("\n  (--dry-run: no changes made)")
        return 0

    if not args.force:
        try:
            ans = input("\nType YES to continue: ").strip()
        except EOFError:
            print("  No input; use --force to run non-interactively.", file=sys.stderr)
            return 2
        if ans != "YES":
            print("  Aborted.")
            return 1

    backup_root.mkdir(parents=True, exist_ok=True)
    backed = 0
    for _label, path in targets:
        b = _backup(path, backup_root)
        if b:
            backed += 1
            print(f"  backed up: {b.name}")
        elif path.exists() and path.stat().st_size == 0:
            print(f"  skip backup (empty): {path.name}")

    for _label, path in targets:
        _truncate(path)
        print(f"  truncated: {path.name}")

    print(f"\n  Done. {backed} file(s) copied to {backup_root}")
    print("  Next: run Cell 2 → Cell 3A → 3B → 4 in 540_tenure_pipeline.ipynb.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
