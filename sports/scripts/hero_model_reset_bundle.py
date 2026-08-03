#!/usr/bin/env python3
"""DEPRECATED shim — use pass_a_empirical_bundle.py and pass_b_generative_knockout_bundle.py.

This file runs Pass A then Pass B for backward compatibility with older notebook paths.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def main() -> None:
    print(
        "Note: hero_model_reset_bundle.py is deprecated.\n"
        "  Pass A → sports/scripts/pass_a_empirical_bundle.py\n"
        "  Pass B → sports/scripts/pass_b_generative_knockout_bundle.py\n"
    )
    for name in ("pass_a_empirical_bundle.py", "pass_b_generative_knockout_bundle.py"):
        path = SCRIPTS / name
        print(f"\n=== Running {name} ===")
        rc = subprocess.call([sys.executable, str(path)])
        if rc != 0:
            raise SystemExit(rc)
    print("\nDone (legacy shim: Pass A + Pass B).")


if __name__ == "__main__":
    main()
