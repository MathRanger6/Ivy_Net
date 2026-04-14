#!/usr/bin/env python3
"""
tenure_pipeline/legacy_flat_snapshots.py
──────────────────────────────────────────────────────────────────────────────
Housekeeping for Option B paths: under each school folder in faculty_snapshots/,
create ``legacy/`` (if needed) and move every *file* that sits directly under the
school folder into ``legacy/``. Subdirectories (e.g. ``<source_id>/``) are left
in place.

Example (before):
  faculty_snapshots/indiana_university/2002_spring.html
  faculty_snapshots/indiana_university/92afac56/2002_spring.html

After:
  faculty_snapshots/indiana_university/legacy/2002_spring.html
  faculty_snapshots/indiana_university/92afac56/2002_spring.html

Usage:
  python tenure_pipeline/legacy_flat_snapshots.py --dry-run
  python tenure_pipeline/legacy_flat_snapshots.py --force

Note: Paths in ``faculty_snapshots_plan.jsonl``, ``faculty_snapshots_index.jsonl``,
and ``faculty_snapshots_parsed.jsonl`` still point at the old locations unless you
rebuilt the plan or edit those files. After a clean rebuild + 3B + 4, this script is
safest for tidying leftover flat files. Otherwise expect to re-run Cell 4 or clear
parsed rows that reference moved paths.

After moving, Cell 4 and ``apply_url_updates.iter_school_html_files()`` treat
``legacy/`` like any other subfolder (same ``rglob('*.html')`` rule as ``<source_id>/``).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TP = Path(__file__).resolve().parent
DEFAULT_ROOT = TP / "faculty_snapshots"


def collect_moves(root: Path) -> list[tuple[Path, Path]]:
    out: list[tuple[Path, Path]] = []
    if not root.is_dir():
        return out
    for school in sorted(root.iterdir()):
        if not school.is_dir() or school.name.startswith("."):
            continue
        legacy = school / "legacy"
        for p in school.iterdir():
            if p.is_file():
                out.append((p, legacy / p.name))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Move top-level flat snapshot files into <slug>/legacy/ per school.",
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"faculty_snapshots directory (default: {DEFAULT_ROOT})",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="Skip YES confirmation.")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="If legacy/<name> exists, replace it (default: skip those files).",
    )

    args = ap.parse_args()
    root: Path = args.root.resolve()

    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2

    moves = collect_moves(root)
    skipped_dest = 0
    planned: list[tuple[Path, Path]] = []
    for src, dest in moves:
        if dest.exists() and not args.overwrite:
            skipped_dest += 1
            continue
        planned.append((src, dest))

    n_schools = len({p[0].parent for p in planned}) if planned else 0
    print(f"Root: {root}")
    print(f"Moves: {len(planned)} file(s) across {n_schools} school folder(s)")
    if skipped_dest:
        print(f"Skipped (destination exists): {skipped_dest}")

    if args.dry_run:
        for src, dest in planned[:200]:
            print(f"  {src.relative_to(root)}  ->  {dest.relative_to(root)}")
        if len(planned) > 200:
            print(f"  ... and {len(planned) - 200} more")
        print("\n  (--dry-run: no changes)")
        return 0

    if not planned:
        print("Nothing to do.")
        return 0

    if not args.force:
        try:
            ans = input("\nType YES to move files: ").strip()
        except EOFError:
            print("  No input; use --force.", file=sys.stderr)
            return 2
        if ans != "YES":
            print("Aborted.")
            return 1

    for src, dest in planned:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and args.overwrite:
            dest.unlink()
        shutil.move(str(src), str(dest))
        print(f"  moved: {src.relative_to(root)} -> {dest.relative_to(root)}")

    print(f"\nDone. {len(planned)} file(s) moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
