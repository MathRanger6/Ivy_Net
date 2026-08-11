#!/usr/bin/env python3
"""Deprecated alias — use rebuild_pd17_interval_reference_slides.py.

Rebuilds PD17 interval overlap reference decks (slides 3–5). Never touches HAND.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve().parent / "rebuild_pd17_interval_reference_slides.py"

if __name__ == "__main__":
    cmd = [sys.executable, str(SCRIPT), *sys.argv[1:]]
    raise SystemExit(subprocess.call(cmd, cwd=str(REPO)))
