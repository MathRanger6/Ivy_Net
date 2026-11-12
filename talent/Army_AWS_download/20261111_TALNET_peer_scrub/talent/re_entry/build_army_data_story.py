#!/usr/bin/env python3
"""Build Army 3×3 data-story mosaic from manifest (Layer 3 wrapper).

Delegates to sports/scripts/build_data_story_mosaic.py.

Run (AWS 520 root — no PYTHONPATH needed):
  ./talent/re_entry/build_army_data_story.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import army_gallery_paths  # noqa: F401 — bootstraps sys.path

from army_gallery_paths import ARMY_RE_ENTRY, MANIFEST_RUN1, resolve_repo  # noqa: E402

DEFAULT_MANIFEST = MANIFEST_RUN1


def _refresh_cohort_text(manifest_path: Path) -> None:
    """If BDP manifest.json exists, patch panel-1 N counts in 3×3 manifest."""
    bdp_manifest = ARMY_RE_ENTRY / "output" / "basic_data_plots" / "manifest.json"
    if not bdp_manifest.is_file():
        return
    cohort = json.loads(bdp_manifest.read_text(encoding="utf-8")).get("cohort", {})
    if not cohort:
        return
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    grid = data.get("grid", [])
    if not grid or grid[0].get("type") != "text":
        return
    lines = grid[0].get("lines", [])
    new_lines = []
    for line in lines:
        if line.startswith("N = "):
            new_lines.append(f"N = {cohort.get('n_officers', '?'):,} officers (last snapshot)")
        elif line.startswith("Promoted / attrition"):
            new_lines.append(
                f"Promoted / attrition / censored = "
                f"{cohort.get('n_promoted', '?')} / "
                f"{cohort.get('n_attrition', '?')} / "
                f"{cohort.get('n_censored', '?')}"
            )
        elif line.startswith("Median pool size"):
            med = cohort.get("median_pool_size")
            new_lines.append(
                f"Median pool size = {med:.0f}" if med is not None else line
            )
        else:
            new_lines.append(line)
    grid[0]["lines"] = new_lines
    repo = resolve_repo()
    manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated cohort text in {manifest_path.relative_to(repo)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Army 3×3 data-story PNG")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--page-size",
        default="letter-landscape",
        choices=("screen", "letter", "letter-landscape", "tabloid", "tabloid-landscape"),
    )
    parser.add_argument("--no-footer", action="store_true")
    parser.add_argument("--skip-refresh-cohort", action="store_true")
    args = parser.parse_args()

    repo = resolve_repo()
    manifest_path = args.manifest.resolve()
    mosaic_script = repo / "sports" / "scripts" / "build_data_story_mosaic.py"

    if not manifest_path.is_file():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    if not mosaic_script.is_file():
        raise SystemExit(f"Compositor not found: {mosaic_script}")

    if not args.skip_refresh_cohort:
        _refresh_cohort_text(manifest_path)

    cmd = [
        sys.executable,
        str(mosaic_script),
        "--manifest",
        str(manifest_path),
        "--page-size",
        args.page_size,
    ]
    if args.no_footer:
        cmd.append("--no-footer")
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(repo))


if __name__ == "__main__":
    main()
