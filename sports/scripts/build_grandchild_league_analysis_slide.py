#!/usr/bin/env python3
"""Build Grandchild interval overlap reference slide.

Legacy single-season 2015:
  python sports/scripts/build_grandchild_league_analysis_slide.py

Compare window (HAND slide 5, default 2015-2019):
  python sports/scripts/build_grandchild_league_analysis_slide.py --compare-window
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
from interval_overlap_paths import DEFAULT_WINDOW_SEASON_MAX, DEFAULT_WINDOW_SEASON_MIN, grandchild_overlap_paths
from interval_overlap_readouts import grandchild_overlap_bullets
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

DIAG_SCRIPT = SCRIPTS / "grandchild_league_interval_diagnostic.py"

CLAIM_LEGACY = (
    "Claim: Grandchild ASSIGN (endogenous centroids, no T_{j^*}) on 2015 PPM z — "
    r"legacy single-season diagnostic."
)
CLAIM_WINDOW = (
    "Claim: Grandchild ASSIGN on the same season window as paired NCAA slide — "
    r"one realization per season, stacked team-seasons."
)


def _regenerate(*, season_min: int, season_max: int, rho: float, seed: int, legacy: bool) -> None:
    cmd = [sys.executable, str(DIAG_SCRIPT), "--rho", str(rho), "--seed", str(seed)]
    if legacy:
        cmd += ["--season", str(season_min)]
    else:
        cmd += ["--season-min", str(season_min), "--season-max", str(season_max)]
    print("Regenerating Grandchild interval overlap figure ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--compare-window", action="store_true")
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    parser.add_argument("--season", type=int, default=None, help="Legacy single season (2015)")
    parser.add_argument("--rho", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=5412015)
    args = parser.parse_args()

    if args.compare_window:
        season_min, season_max = DEFAULT_WINDOW_SEASON_MIN, DEFAULT_WINDOW_SEASON_MAX
        legacy = False
    elif args.season_min is not None or args.season_max is not None:
        if args.season_min is None or args.season_max is None:
            parser.error("--season-min and --season-max must be supplied together")
        season_min, season_max = args.season_min, args.season_max
        legacy = False
    else:
        season_min = season_max = args.season if args.season is not None else 2015
        legacy = args.season is None and not args.compare_window

    paths = grandchild_overlap_paths(
        season_min=season_min,
        season_max=season_max,
        single_season_legacy=legacy,
    )
    paired = not legacy or season_max > season_min

    ensure_hero_dirs()
    if not args.slides_only:
        _regenerate(
            season_min=season_min,
            season_max=season_max,
            rho=args.rho,
            seed=args.seed,
            legacy=legacy,
        )

    meta = load_meta(paths["meta"])
    assign = meta.get("assignment", {})
    seasons = meta.get("seasons") or paths["seasons"]
    rho = assign.get("rho", args.rho)
    n_units = meta.get("n_team_seasons") or meta.get("n_teams")
    n_players = meta.get("n_players")
    c = assign.get("roster_size", 15)
    h_sort = meta.get("H_sort") or assign.get("sorting_index_h")

    if paired and not legacy:
        title = rf"Grandchild sim — team \hat{{A}}_{{i}} interval overlap ({seasons})"
        claim = CLAIM_WINDOW
    else:
        title = r"Grandchild sim — team \hat{A}_{i} interval overlap (\rho diagnostic)"
        claim = CLAIM_LEGACY

    sub_parts = [
        rf"MBB {seasons} · Grandchild ASSIGN · \rho={rho:g} · C={c}",
    ]
    if n_players and n_units:
        sub_parts.append(rf"N={n_players:,}, {n_units:,} team-seasons")
    elif n_units:
        sub_parts.append(rf"{n_units:,} teams")
    if h_sort is not None:
        sub_parts.append(rf"H_{{sort}}={float(h_sort):.3f}")

    build_interval_overlap_slide(
        fig_path=paths["png"],
        out_pptx=paths["deck"],
        title=title,
        subtitle=" · ".join(sub_parts),
        bullets=grandchild_overlap_bullets(meta, paired_compare=paired and not legacy),
        claim=claim,
    )


if __name__ == "__main__":
    main()
