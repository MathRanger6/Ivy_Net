#!/usr/bin/env python3
"""Rebuild PD17 interval-overlap **reference** decks (never touches HAND master).

Slide 3 — full NCAA panel 2011-2021:
  auto/CHAR_empirical_team_interval_overlap_AUTO.pptx

Slide 4 — NCAA compare window (default 2015-2019):
  auto/CHAR_empirical_team_interval_overlap_2015_2019_AUTO.pptx

Slide 5 — Grandchild sim same window:
  auto/CHAR_grandchild_league_interval_overlap_2015_2019_AUTO.pptx

Run (repo root):
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/rebuild_pd17_interval_reference_slides.py
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/rebuild_pd17_interval_reference_slides.py --slides-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_EMPIRICAL_OVERLAP_DECK, ensure_hero_dirs
from interval_overlap_paths import (
    DEFAULT_WINDOW_SEASON_MAX,
    DEFAULT_WINDOW_SEASON_MIN,
    empirical_overlap_paths,
    grandchild_overlap_paths,
)

BUILD_EMPIRICAL = SCRIPTS / "build_empirical_team_interval_overlap_slide.py"
BUILD_GRANDCHILD = SCRIPTS / "build_grandchild_league_analysis_slide.py"


def _load_json(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _run(script: Path, *extra: str) -> None:
    subprocess.run([sys.executable, str(script), *extra], cwd=str(REPO), check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild PD17 slides 3–5 interval reference decks (never HAND)."
    )
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--season-min", type=int, default=DEFAULT_WINDOW_SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=DEFAULT_WINDOW_SEASON_MAX)
    parser.add_argument("--rho", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=5412015)
    parser.add_argument("--skip-full-panel", action="store_true", help="Only rebuild window slides 4–5")
    args = parser.parse_args()

    ensure_hero_dirs()
    slide_flags = ["--slides-only"] if args.slides_only else []

    paths_full = empirical_overlap_paths()
    paths_ncaa = empirical_overlap_paths(season_min=args.season_min, season_max=args.season_max)
    paths_sim = grandchild_overlap_paths(
        season_min=args.season_min,
        season_max=args.season_max,
        single_season_legacy=False,
    )

    if not args.skip_full_panel:
        print("Slide 3 reference — full NCAA 2011-2021 ...")
        _run(BUILD_EMPIRICAL, *slide_flags)

    print(f"Slide 4 reference — NCAA {args.season_min}-{args.season_max} ...")
    _run(
        BUILD_EMPIRICAL,
        *slide_flags,
        "--season-min",
        str(args.season_min),
        "--season-max",
        str(args.season_max),
    )

    print(f"Slide 5 reference — Grandchild sim {args.season_min}-{args.season_max} ...")
    gc_flags = [
        *slide_flags,
        "--season-min",
        str(args.season_min),
        "--season-max",
        str(args.season_max),
        "--rho",
        str(args.rho),
        "--seed",
        str(args.seed),
    ]
    _run(BUILD_GRANDCHILD, *gc_flags)

    meta_full = _load_json(paths_full["meta"])
    meta_ncaa = _load_json(paths_ncaa["meta"])
    meta_sim = _load_json(paths_sim["meta"])

    print()
    print("Reference decks (update HAND manually — never CHAR_PD17_HAND.pptx):")
    if not args.skip_full_panel:
        print(f"  Slide 3 (full panel): {AUTO_EMPIRICAL_OVERLAP_DECK}")
        print(f"    H_sort={meta_full.get('H_sort')}  max cov={meta_full.get('coverage_max')}")
    print(f"  Slide 4 (NCAA window):  {paths_ncaa['deck']}")
    print(f"    H_sort={meta_ncaa.get('H_sort')}  max cov={meta_ncaa.get('coverage_max')}  "
          f"norm={meta_ncaa.get('coverage_max_normalized')}")
    print(f"  Slide 5 (sim window):   {paths_sim['deck']}")
    assign = meta_sim.get("assignment", {})
    print(f"    H_sort={meta_sim.get('H_sort')}  max cov={meta_sim.get('coverage_max')}  "
          f"norm={meta_sim.get('coverage_max_normalized')}  rho={assign.get('rho', args.rho)}")
    print()
    print("HAND: Change Picture → copy bullets → keep equation formatting.")


if __name__ == "__main__":
    main()
