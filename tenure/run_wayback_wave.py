#!/usr/bin/env python3
"""
Daily Wayback enrichment — optional CLI front door (same stages as 540 Cells 2, 3A, 3B, 4).

Usage (from repo root):
  python3 tenure/run_wayback_wave.py --slugs arizona_state_university --steps apply,cell2,cdx,download,parse
  python3 tenure/run_wayback_wave.py --steps download,parse   # global queue, no slug filter

Steps:
  apply    — run apply_url_updates.py (worksheet new_url → r1_schools_data.py)
  cell2    — rebuild r1_cs_departments.csv from PILOT_SCHOOLS
  cdx      — Stage 3A CDX discovery
  download — Stage 3B HTML download
  parse    — Stage 4 HTML parse
  report   — post-wave table (plan snaps | HTML on disk | mean parse recs)

After ``parse``, ``report`` runs automatically unless ``--no-post-report``.

Notebook users: set WAYBACK_SLUGS and RUN_CELL* in Cell 0 instead; this script shares the same .py modules.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def _strip_notebook_magics(src: str) -> str:
    out = []
    for line in src.splitlines(keepends=True):
        s = line.lstrip()
        if s.startswith("%") or s.startswith("!"):
            continue
        out.append(line)
    return "".join(out)


def _repo_root(script: Path) -> Path:
    p = script.parent
    return p.parent if p.name == "tenure" else p


def _find_code_cell(cells: list, marker: str) -> int:
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        if marker in "".join(cell.get("source", [])):
            return i
    return -1


def _load_cell0_globals(repo_root: Path) -> dict:
    nb_path = repo_root / "tenure" / "540_tenure_pipeline.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    idx0 = _find_code_cell(nb["cells"], "=== CELL 0: IMPORTS & PATH SETUP ===")
    if idx0 < 0:
        raise SystemExit("ERROR: Cell 0 not found in 540_tenure_pipeline.ipynb")
    code = _strip_notebook_magics("".join(nb["cells"][idx0]["source"]))
    prelude = "import matplotlib\nmatplotlib.use('Agg')\n\n"
    g: dict = {"__name__": "__main__", "__file__": str(nb_path)}
    exec(compile(prelude + code, f"{nb_path}:cell0", "exec"), g, g)
    return g


def _run_cell2(g: dict) -> None:
    import json as _json

    import pandas as pd

    import r1_schools_data

    rows = []
    for school in r1_schools_data.PILOT_SCHOOLS:
        rows.append(
            {
                "university": school["university"],
                "dept_name": school.get("dept_name", ""),
                "urls": _json.dumps(school.get("urls", [])),
                "notes": school.get("notes", ""),
                "pilot": True,
            }
        )
    df = pd.DataFrame(rows)
    out = Path(g["STAGE2_OUT"])
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"  Cell 2 CSV written: {out} ({len(df)} schools)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Run Wayback enrichment steps (Cells 2, 3A, 3B, 4).")
    ap.add_argument(
        "--slugs",
        type=str,
        default="",
        help="Comma-separated uni_slug values (e.g. arizona_state_university). Empty = all schools.",
    )
    ap.add_argument(
        "--steps",
        type=str,
        default="apply,cell2,cdx,download,parse",
        help="Comma-separated: apply, cell2, cdx, download, parse, report",
    )
    ap.add_argument(
        "--no-post-report",
        action="store_true",
        help="Do not run report automatically after parse.",
    )
    args = ap.parse_args()

    script = Path(__file__).resolve()
    repo_root = _repo_root(script)
    os.chdir(repo_root)
    sys.path.insert(0, str(repo_root))
    tp = repo_root / "tenure" / "tenure_pipeline"
    sys.path.insert(0, str(tp))

    steps = [s.strip().lower() for s in args.steps.split(",") if s.strip()]
    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()] if args.slugs.strip() else None

    if "apply" in steps:
        apply_py = tp / "apply_url_updates.py"
        print("\n── Step: apply (worksheet → r1_schools_data.py)")
        subprocess.run([sys.executable, str(apply_py)], check=True)

    g = _load_cell0_globals(repo_root)
    if slugs is not None:
        g["WAYBACK_SLUGS"] = slugs
        print(f"\n  WAYBACK_SLUGS set for this run: {slugs}")

    if "cell2" in steps:
        print("\n── Step: cell2 (rebuild r1_cs_departments.csv)")
        _run_cell2(g)

    if "cdx" in steps:
        print("\n── Step: cdx (Stage 3A)")
        g["RUN_CELL3_CDX"] = True
        from stage3a_cdx import run_stage3a_from_globals

        run_stage3a_from_globals(g)

    if "download" in steps:
        print("\n── Step: download (Stage 3B)")
        g["RUN_CELL3_DOWNLOAD"] = True
        from stage3b_download import run_stage3b_from_globals

        run_stage3b_from_globals(g)

    if "parse" in steps:
        print("\n── Step: parse (Stage 4)")
        g["RUN_CELL4"] = True
        from stage4_parse import run_stage4_from_globals

        run_stage4_from_globals(g)

    run_report = "report" in steps or ("parse" in steps and not args.no_post_report)
    if run_report:
        print("\n── Step: report (wayback URL quality)")
        from wayback_wave_report import print_wave_report

        slug_set = set(slugs) if slugs else None
        print_wave_report(tenure_pipeline_dir=tp, wayback_slugs=slug_set)

    print("\n── Wayback wave complete.")


if __name__ == "__main__":
    main()
