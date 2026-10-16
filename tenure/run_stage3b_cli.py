#!/usr/bin/env python3
"""
Run Stage 3B (Wayback HTML download) from Terminal — same code as notebook cells 0 + 3B,
but in a normal Python process (not Cursor's Jupyter kernel). Use this when large HTML
writes fail under the notebook sandbox / Dropbox.

Usage (from any shell):
  cd "/path/to/Cursor Workspace PDE"    # repo root (parent of tenure/)
  conda activate tenure_net
  python3 tenure/run_stage3b_cli.py
  # or: python3 run_stage3b_cli.py   (if symlink at root points here)

Optional:
  python3 tenure/run_stage3b_cli.py --notebook /other/path/540_tenure_pipeline.ipynb
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _strip_notebook_magics(src: str) -> str:
    """Remove Jupyter/IPython-only lines (%matplotlib, !shell, etc.)."""
    out = []
    for line in src.splitlines(keepends=True):
        s = line.lstrip()
        if s.startswith("%") or s.startswith("!"):
            continue
        out.append(line)
    return "".join(out)


def _repo_root(script_path: Path) -> Path:
    """Workspace repo root: parent of tenure/ when this file lives under tenure/."""
    p = script_path.parent
    if p.name == "tenure":
        return p.parent
    return p


def _find_code_cell(cells: list, marker: str) -> int:
    """Return index of first code cell whose source contains ``marker``."""
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if marker in src:
            return i
    return -1


def main() -> None:
    ap = argparse.ArgumentParser(description="Run tenure pipeline CELL 0 + 3B outside Jupyter.")
    ap.add_argument(
        "--notebook",
        type=Path,
        default=None,
        help="Path to 540_tenure_pipeline.ipynb (default: tenure/540 or root symlink)",
    )
    args = ap.parse_args()

    script = Path(__file__).resolve()
    repo_root = _repo_root(script)
    os.chdir(repo_root)

    sys.path.insert(0, str(repo_root))
    tp = repo_root / "tenure" / "tenure_pipeline"
    if not tp.is_dir():
        tp = repo_root / "tenure_pipeline"
    if str(tp) not in sys.path:
        sys.path.insert(0, str(tp))

    nb_path = args.notebook
    if nb_path is None:
        nb_path = repo_root / "tenure" / "540_tenure_pipeline.ipynb"
    nb_path = nb_path.resolve()
    if not nb_path.is_file():
        print(f"ERROR: notebook not found: {nb_path}", file=sys.stderr)
        sys.exit(1)

    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    cells = nb["cells"]
    idx0 = _find_code_cell(cells, "=== CELL 0: IMPORTS & PATH SETUP ===")
    if idx0 < 0:
        print("ERROR: could not locate CELL 0 code cell by marker", file=sys.stderr)
        sys.exit(1)
    if cells[idx0].get("cell_type") != "code":
        print("ERROR: CELL 0 is not a code cell", file=sys.stderr)
        sys.exit(1)

    print(f"Using notebook CELL 0 = index {idx0}; Stage 3B via stage3b_download.py", flush=True)
    cell0 = _strip_notebook_magics("".join(cells[idx0].get("source", [])))
    prelude = "import matplotlib\nmatplotlib.use('Agg')\n\n"
    g: dict = {"__name__": "__main__", "__file__": str(script)}
    exec(compile(prelude + cell0, f"{nb_path}:cell0", "exec"), g, g)
    from stage3b_download import run_stage3b_from_globals

    run_stage3b_from_globals(g)


if __name__ == "__main__":
    main()
