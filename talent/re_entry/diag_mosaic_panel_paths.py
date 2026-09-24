#!/usr/bin/env python3
"""Print which PNG paths the 3×3 mosaic compositor will load (AWS 520 root).

Run from Network_1P_shell:
  python talent/re_entry/diag_mosaic_panel_paths.py

Flags duplicate filenames under talent/re_entry/output/ — the usual cause of
“individual panels look right but mosaic does not.”
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

MANIFEST = Path("talent/re_entry/manifests/army_run1_3x3_manifest.json")
BDP_MANIFEST = Path("talent/re_entry/output/basic_data_plots/manifest.json")
MOSAIC_OUT = Path("talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png")
OUTPUT_ROOT = Path("talent/re_entry/output")


def repo_root() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd / "talent" / "re_entry").is_dir() and (cwd / "sports" / "scripts").is_dir():
        return cwd
    here = Path(__file__).resolve().parent
    return here.parents[1]


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_mtime(path: Path) -> str:
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def find_same_basenames(root: Path, basename: str) -> list[Path]:
    hits: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        if basename in filenames:
            hits.append((Path(dirpath) / basename).resolve())
    return sorted(hits)


def main() -> None:
    repo = repo_root()
    print(f"REPO (mosaic CWD should be this): {repo}")
    print(f"cwd: {Path.cwd().resolve()}")
    if Path.cwd().resolve() != repo:
        print("WARNING: cwd != REPO — cd to 520 root before build_army_data_story.py")
    print()

    if BDP_MANIFEST.is_file():
        cohort = json.loads(BDP_MANIFEST.read_text(encoding="utf-8")).get("cohort", {})
        print(
            f"BDP manifest.json cohort: N={cohort.get('n_officers')} "
            f"med_pool={cohort.get('median_pool_size')}"
        )
    else:
        print(f"MISSING: {BDP_MANIFEST}")
    print()

    mpath = repo / MANIFEST
    data = json.loads(mpath.read_text(encoding="utf-8"))
    panel1_n = next(
        (ln for ln in data["grid"][0].get("lines", []) if ln.startswith("N = ")),
        "(no N line)",
    )
    print(f"3x3 manifest panel-1 text: {panel1_n}")
    print()

    print("Panels the compositor loads (REPO / manifest path):")
    print("-" * 72)
    for cell in data["grid"]:
        title = cell.get("title", "?")
        if cell.get("type") != "image":
            continue
        rel = cell["path"]
        resolved = (repo / rel).resolve()
        exists = resolved.is_file()
        line = f"  {title}\n    -> {resolved}"
        if exists:
            st = resolved.stat()
            line += f"\n    mtime={fmt_mtime(resolved)}  bytes={st.st_size}  md5={md5(resolved)[:12]}"
        else:
            line += "\n    *** FILE MISSING — mosaic build would fail ***"
        print(line)

        base = resolved.name
        dupes = find_same_basenames(repo / OUTPUT_ROOT, base)
        if len(dupes) > 1:
            print(f"    DUPLICATES ({len(dupes)} copies under {OUTPUT_ROOT}):")
            for p in dupes:
                tag = "CANONICAL" if p == resolved else "other"
                print(
                    f"      [{tag}] {p}\n"
                    f"              mtime={fmt_mtime(p)}  md5={md5(p)[:12]}"
                )
        print()

    out = (repo / MOSAIC_OUT).resolve()
    if out.is_file():
        print(f"Mosaic output: {out}")
        print(f"  mtime={fmt_mtime(out)}  bytes={out.stat().st_size}  md5={md5(out)[:12]}")
    else:
        print(f"Mosaic output MISSING: {out}")

    print()
    print("If you open individuals from a backup subfolder (run1_legacy, run2_thrudate,")
    print("etc.), they will NOT match — mosaic always reads top-level paths above.")


if __name__ == "__main__":
    main()
