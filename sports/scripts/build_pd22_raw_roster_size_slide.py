#!/usr/bin/env python3
"""Legacy alias — builds AFTER box QC roster-size AUTO slide.

Prefer:
  build_pd22_raw_roster_size_before_qc_slide.py  (motivation, HAND first)
  build_pd22_raw_roster_size_after_qc_slide.py   (post-QC panel)
"""

from __future__ import annotations

from build_pd22_raw_roster_size_after_qc_slide import main

if __name__ == "__main__":
    main()
