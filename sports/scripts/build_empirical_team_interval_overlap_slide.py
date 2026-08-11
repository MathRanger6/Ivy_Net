#!/usr/bin/env python3
"""Build PD17 empirical team interval overlap reference slide.

Full panel (HAND slide 3):
  python sports/scripts/build_empirical_team_interval_overlap_slide.py

Compare window (HAND slide 4, default 2015-2019):
  python sports/scripts/build_empirical_team_interval_overlap_slide.py --compare-window
  python sports/scripts/build_empirical_team_interval_overlap_slide.py --season-min 2015 --season-max 2019
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import ensure_hero_dirs
from interval_overlap_paths import DEFAULT_WINDOW_SEASON_MAX, DEFAULT_WINDOW_SEASON_MIN, empirical_overlap_paths
from interval_overlap_readouts import empirical_overlap_bullets
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

DIAG_SCRIPT = SCRIPTS / "empirical_team_interval_overlap.py"

CLAIM_FULL = (
    "Claim (PD17): Real NCAA rosters leave massively overlapping team talent windows — "
    r"full 2011–2021 panel target for \rho characterization (530 CELL 8)."
)
CLAIM_WINDOW = (
    "Claim: NCAA interval overlap on a fixed season window — "
    r"paired compare to Grandchild ASSIGN sim on the same window."
)


def _regenerate(*, season_min: int | None, season_max: int | None) -> None:
    cmd = [sys.executable, str(DIAG_SCRIPT)]
    if season_min is not None and season_max is not None:
        cmd += ["--season-min", str(season_min), "--season-max", str(season_max)]
    print("Regenerating empirical interval overlap figure ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument(
        "--compare-window",
        action="store_true",
        help=f"Use default compare window {DEFAULT_WINDOW_SEASON_MIN}-{DEFAULT_WINDOW_SEASON_MAX}",
    )
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    args = parser.parse_args()

    if args.compare_window:
        season_min, season_max = DEFAULT_WINDOW_SEASON_MIN, DEFAULT_WINDOW_SEASON_MAX
    elif args.season_min is not None or args.season_max is not None:
        if args.season_min is None or args.season_max is None:
            parser.error("--season-min and --season-max must be supplied together")
        season_min, season_max = args.season_min, args.season_max
    else:
        season_min = season_max = None

    paths = empirical_overlap_paths(season_min=season_min, season_max=season_max)
    paired = season_min is not None

    ensure_hero_dirs()
    if not args.slides_only:
        _regenerate(season_min=season_min, season_max=season_max)

    meta = load_meta(paths["meta"])
    seasons = meta.get("seasons", paths["seasons"])
    n_ts = meta.get("n_team_seasons")
    h_sort = meta.get("H_sort")

    if paired:
        title = rf"PD17 — NCAA team \hat{{A}}_{{i}} interval overlap ({seasons})"
        claim = CLAIM_WINDOW
    else:
        title = r"PD17 — Empirical team \hat{A}_{i} interval overlap (\rho diagnostic)"
        claim = CLAIM_FULL

    sub_parts = [
        rf"MBB {seasons} · PPM z within season · min 20 min · poolq winsor 0.01–0.99",
    ]
    if n_ts:
        sub_parts.append(rf"{n_ts:,} team-seasons (530 CELL 8 port)")
    if h_sort is not None:
        sub_parts.append(rf"H_{{sort}}={float(h_sort):.3f}")

    build_interval_overlap_slide(
        fig_path=paths["png"],
        out_pptx=paths["deck"],
        title=title,
        subtitle=" · ".join(sub_parts),
        bullets=empirical_overlap_bullets(meta, paired_compare=paired),
        claim=claim,
    )


if __name__ == "__main__":
    main()
