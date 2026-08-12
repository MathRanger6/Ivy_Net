#!/usr/bin/env python3
"""Rebuild PD17 ρ validation AUTO decks (global_wss + H_sort companion).

Alex primary: global_wss (within-team SS numerator on the assign partition).
Companion: H_sort scale-free readout on the same 541 ρ sweep.

Run (repo root):
  python sports/scripts/build_pd17_rho_validation_slides.py --slides-only
  python sports/scripts/build_pd17_rho_validation_slides.py   # reruns full ρ sweep first
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent

BUILD_GLOBAL_WSS = SCRIPTS / "build_grandchild_rho_global_wss_slide.py"
BUILD_H_SORT = SCRIPTS / "build_grandchild_rho_assortativity_slide.py"


def _run(script: Path, *, slides_only: bool, quick: bool) -> None:
    cmd = [sys.executable, str(script)]
    if slides_only:
        cmd.append("--slides-only")
    elif quick:
        cmd.append("--quick")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD17 ρ validation AUTO slides.")
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--quick", action="store_true", help="Smoke ρ sweep (both builders)")
    parser.add_argument("--global-wss-only", action="store_true")
    parser.add_argument("--h-sort-only", action="store_true")
    args = parser.parse_args()

    if args.global_wss_only and args.h_sort_only:
        parser.error("Choose at most one of --global-wss-only / --h-sort-only")

    print("=== PD17 ρ validation AUTO slides ===")
    if not args.h_sort_only:
        print("[1/2] global_wss (Alex primary) ...")
        _run(BUILD_GLOBAL_WSS, slides_only=args.slides_only, quick=args.quick)
    if not args.global_wss_only:
        print("[2/2] H_sort companion ...")
        _run(BUILD_H_SORT, slides_only=args.slides_only, quick=args.quick)

    print()
    print("Copy into CHAR_PD17_HAND.pptx (Change Picture + bullets):")
    print("  Primary:  slides/auto/CHAR_grandchild_rho_global_wss_AUTO.pptx")
    print("  Optional: slides/auto/CHAR_grandchild_rho_assortativity_AUTO.pptx")
    print("  Figures:  grandchild_assign/GRANDCHILD_rho_vs_global_wss.png")
    print("            grandchild_assign/GRANDCHILD_rho_vs_assortativity.png")


if __name__ == "__main__":
    main()
