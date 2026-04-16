#!/usr/bin/env python3
"""
Assign consistent cell metadata["name"] on Jupyter notebooks for editor outlines.

Convention: ``{notebook_stem} · Cell {N} — {title}`` when a banner matches
``# CELL N:`` or ``NOTEBOOK CELL N: …``; otherwise ``S{order:02d}`` (sequence index)
+ markdown heading or first meaningful comment line.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _clean_title(s: str, max_len: int = 90) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


def _skip_banner_line(raw: str) -> bool:
    raw = raw.strip()
    if not raw or raw.startswith("=") and set(raw.replace(" ", "")) <= {"=", "#"}:
        return True
    if re.match(r"^#?\s*=+\s*$", raw):
        return True
    return False


def _polish_fallback_title(title: str) -> str:
    title = re.sub(r"^SDV_SECOND\s*[—\-]\s*", "", title, flags=re.I)
    title = re.sub(r"^BPM_\w+\s*[—\-]\s*", "", title, flags=re.I)
    title = title.strip()
    return _clean_title(title)


def derive_cell_name(stem: str, idx: int, cell: dict) -> str:
    src = cell.get("source", [])
    if isinstance(src, list):
        src = "".join(src)
    elif not isinstance(src, str):
        src = str(src)

    order = idx + 1
    head = src[:6000]

    m = re.search(
        r"NOTEBOOK\s+CELL\s+(\d+)(?:\s*\([^)]*\))?\s*:\s*([^\n]+)",
        head,
        re.IGNORECASE,
    )
    if m:
        title = _clean_title(m.group(2).strip())
        return f"{stem} · Cell {m.group(1)} — {title}"

    m = re.search(
        r"^\s*#\s*(?:[\w.]+\s*[—\-]\s*)?CELL\s+(\d+)(?:\s*\([^)]*\))?\s*:\s*(.+)$",
        src,
        re.MULTILINE | re.IGNORECASE,
    )
    if m:
        title = _clean_title(m.group(2))
        return f"{stem} · Cell {m.group(1)} — {title}"

    m = re.search(r"^\s*#\s*CELL\s+(\d+)\s*:\s*(.+)$", src, re.MULTILINE | re.IGNORECASE)
    if m:
        title = _clean_title(m.group(2))
        return f"{stem} · Cell {m.group(1)} — {title}"

    m = re.search(r"^\s*#\s*CELL\s+(\d+)\s*[—\-:\s]\s*(.+)$", src, re.MULTILINE | re.IGNORECASE)
    if m:
        title = _clean_title(m.group(2))
        return f"{stem} · Cell {m.group(1)} — {title}"

    if cell.get("cell_type") == "markdown":
        for line in src.splitlines():
            s = line.strip()
            if s.startswith("#"):
                title = _clean_title(s.lstrip("#").strip())
                if title:
                    return f"{stem} · S{order:02d} — {title}"
        plain = src.strip().split("\n", 1)[0].strip()
        if plain and not plain.startswith("#"):
            return f"{stem} · S{order:02d} — {_polish_fallback_title(plain[:100])}"

    if cell.get("cell_type") == "code":
        for line in src.splitlines():
            s = line.strip()
            if not s.startswith("#"):
                continue
            raw = s.lstrip("#").strip()
            if _skip_banner_line(raw):
                continue
            if "NOTEBOOK" in raw.upper() and "CELL" in raw.upper() and re.search(r"\d", raw):
                continue
            title = _polish_fallback_title(raw[:200])
            if title:
                return f"{stem} · S{order:02d} — {title}"

    return f"{stem} · S{order:02d} — ({cell.get('cell_type', 'unknown')})"


def name_cells_in_notebook(path: Path, dry_run: bool = False) -> int:
    path = path.resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    cells = data.get("cells", [])
    stem = path.stem
    n = 0
    for i, cell in enumerate(cells):
        name = derive_cell_name(stem, i, cell)
        meta = cell.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
        old = meta.get("name")
        if old == name:
            continue
        if dry_run:
            print(f"{path.name}[{i}]: {old!r} -> {name!r}")
            n += 1
            continue
        meta["name"] = name
        cell["metadata"] = meta
        n += 1
    if not dry_run and n:
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    paths = [a for a in argv[1:] if not a.startswith("-")]
    if not paths:
        root = Path(__file__).resolve().parent.parent
        paths = sorted(str(p) for p in root.glob("*.ipynb"))
    total_files = 0
    for p in paths:
        n = name_cells_in_notebook(Path(p), dry_run=dry)
        if n:
            print(f"{'[dry] ' if dry else ''}{p}: updated {n} cell name(s)")
            total_files += 1
    if not paths:
        print("No notebooks found.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
