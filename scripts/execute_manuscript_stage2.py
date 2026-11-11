#!/usr/bin/env python3
"""Execute 5-Manuscript stage 2 from 00_MOVE_MANIFEST_proposed.csv."""
from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "5-Manuscript/00_MOVE_MANIFEST_proposed.csv"
LOG = ROOT / "5-Manuscript/stage2_run_log.txt"


def log(msg: str, fh) -> None:
    fh.write(msg + "\n")
    fh.flush()
    print(msg)


def is_tracked(rel: str) -> bool:
    r = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        capture_output=True,
    )
    return r.returncode == 0


def merge_dir_into(src: Path, dst: Path, use_git: bool) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for child in sorted(src.iterdir()):
        target = dst / child.name
        if target.exists():
            continue
        relocate(child, target, use_git)


def relocate(src: Path, dst: Path, use_git: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.is_dir() and dst.is_dir():
            merge_dir_into(src, dst, use_git)
            if not any(src.iterdir()):
                src.rmdir()
            return
        raise FileExistsError(f"destination exists: {dst}")
    if use_git and is_tracked(str(src.relative_to(ROOT))):
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
    else:
        shutil.move(str(src), str(dst))


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    rel = dst.relative_to(ROOT)
    subprocess.run(["git", "add", "-f", str(rel)], cwd=ROOT, check=False)


def main() -> int:
    rows = []
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    append = "--resume" in sys.argv
    mode = "a" if append else "w"
    with LOG.open(mode, encoding="utf-8") as fh:
        log(f"Stage 2 {'resume' if append else 'started'} — root {ROOT}", fh)

        # 1. DELETE + JUNK (full run only)
        for row in ([] if append else rows):
            st = row["status"].strip()
            if st not in ("DELETE", "JUNK"):
                continue
            cur = row["current_path"].strip().rstrip("/")
            if not cur:
                continue
            p = ROOT / cur
            if not p.exists():
                log(f"SKIP {st} missing: {cur}", fh)
                continue
            if is_tracked(cur):
                subprocess.run(["git", "rm", "-f", cur], cwd=ROOT, check=True)
            else:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            log(f"{st}: {cur}", fh)

        # 2. Collect operations (defer MOVE_LAST)
        ops = []
        move_last = []
        for row in rows:
            st = row["status"].strip()
            cur = row["current_path"].strip()
            prop = (row.get("proposed_path") or "").strip()
            if st in ("STAYS", "EXPANDED"):
                continue
            if st in ("DELETE", "JUNK"):
                continue
            if not cur or not prop or " (stays)" in prop:
                continue
            if st == "MOVE_LAST":
                move_last.append(row)
                continue
            ops.append(row)

        # Sort: deeper paths first (directories before parents)
        def depth_key(r: dict) -> tuple:
            cur = r["current_path"].rstrip("/")
            return (-cur.count("/"), cur)

        ops.sort(key=depth_key)

        for row in ops:
            st = row["status"].strip()
            cur = row["current_path"].strip().rstrip("/")
            prop = row["proposed_path"].strip().rstrip("/")
            src = ROOT / cur
            dst = ROOT / prop
            if not src.exists():
                dst_check = ROOT / prop if prop else None
                if st in ("MOVE", "COPY", "DEDUPE", "SCRIPT", "MOVE_LAST") and dst_check and dst_check.exists():
                    log(f"SKIP {st} already at dest: {prop}", fh)
                else:
                    log(f"SKIP {st} missing: {cur}", fh)
                continue
            try:
                if st == "COPY":
                    if src.is_dir():
                        log(f"SKIP COPY dir: {cur}", fh)
                        continue
                    copy_file(src, dst)
                    log(f"COPY: {cur} -> {prop}", fh)
                elif st in ("MOVE", "DEDUPE", "SCRIPT"):
                    relocate(src, dst, use_git=True)
                    log(f"{st}: {cur} -> {prop}", fh)
                else:
                    log(f"SKIP unknown status {st}: {cur}", fh)
            except Exception as e:
                log(f"FAIL {st} {cur}: {e}", fh)
                return 1

        for row in move_last:
            cur = row["current_path"].strip().rstrip("/")
            prop = row["proposed_path"].strip()
            src = ROOT / cur
            dst = ROOT / prop
            if not src.exists():
                log(f"SKIP MOVE_LAST missing: {cur}", fh)
                continue
            try:
                relocate(src, dst, use_git=True)
                log(f"MOVE_LAST: {cur} -> {prop}", fh)
            except Exception as e:
                log(f"FAIL MOVE_LAST {cur}: {e}", fh)
                return 1

        # Stub README for emptied handoff folder
        handoff = ROOT / "3-Master_Plan/VECTOR_work/new_VECTOR_work/Introduction_Agent_Handoff_20261027"
        if handoff.exists():
            stub = handoff / "README_MOVED.txt"
            if not stub.exists():
                stub.write_text(
                    "Introduction/lit-review manuscript files moved to 5-Manuscript/ "
                    "(02_Literature_Review, 01_Introduction). See 5-Manuscript/README.md.\n",
                    encoding="utf-8",
                )
                subprocess.run(
                    ["git", "add", str(stub.relative_to(ROOT))],
                    cwd=ROOT,
                    check=False,
                )
            log("Wrote Introduction_Agent_Handoff stub README_MOVED.txt", fh)

        log("Stage 2 complete.", fh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
