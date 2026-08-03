#!/usr/bin/env python3
"""DEPRECATED shim — use pass_c_rho_ablation_bundle.py."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    target = Path(__file__).resolve().parent / "pass_c_rho_ablation_bundle.py"
    print(
        "Note: 540_rho_ablation_bundle.py is deprecated.\n"
        f"  Pass C → sports/scripts/{target.name}\n"
    )
    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
