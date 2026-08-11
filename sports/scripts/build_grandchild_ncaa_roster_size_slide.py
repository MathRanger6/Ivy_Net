#!/usr/bin/env python3
"""Build NCAA vs LG roster-size input comparison AUTO reference slide.

Runs grandchild_ncaa_roster_size_distribution.py (unless --slides-only), then writes
disposable AUTO deck for HAND17 Change Picture workflow.

Run (repo root):
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_ncaa_roster_size_slide.py
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_ncaa_roster_size_slide.py --slides-only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

DIAG_SCRIPT = SCRIPTS / "grandchild_ncaa_roster_size_distribution.py"
FIG = GRANDCHILD_ASSIGN / "GRANDCHILD_ncaa_vs_lg_roster_size_compare_2011_2021.png"
META = GRANDCHILD_ASSIGN / "GRANDCHILD_ncaa_roster_size_distribution_2011_2021_meta.json"
OUT_PPTX = SLIDES_AUTO / "CHAR_grandchild_ncaa_roster_size_compare_AUTO.pptx"

CLAIM = (
    "Claim (PD17 / LG): The minutes floor defines who counts as a roster peer — "
    "NCAA empirical team-units are thinner and variable; LG repacks the same ability "
    "pool into fixed C=15 synthetic leagues."
)


def _regenerate(*, season_min: int, season_max: int) -> None:
    cmd = [
        sys.executable,
        str(DIAG_SCRIPT),
        "--season-min",
        str(season_min),
        "--season-max",
        str(season_max),
    ]
    print("Running NCAA vs LG roster-size diagnostics ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    ncaa = meta.get("team_season_summary", {})
    lg = meta.get("lg_team_season_summary", {})
    seasons = meta.get("seasons_label", "2011-2021")
    c = meta.get("lg_roster_size_reference", 15)
    ncaa_mean = ncaa.get("mean", 0.0)
    ncaa_n = ncaa.get("n", 0)
    lg_n = lg.get("n", 0)

    return [
        r"Players per team-season after \geq 20 ESPN box minutes (same panel as PD17 hero).",
        rf"Left: NCAA real (team_id, season) units — $n={ncaa_n:,}$, mean={ncaa_mean:.1f}, "
        rf"median={ncaa.get('median', 0):.0f}.",
        rf"Right: LG synthetic leagues — $n={lg_n:,}$, every roster $C={c:g}$ "
        r"(J = N/15 per season, stacked).",
        r"Red dotted: NCAA mean. Orange dashed: LG fixed capacity.",
        rf"Only {100 * ncaa.get('share_eq_15', 0):.1f}\% of NCAA team-seasons have exactly "
        rf"{c:g} qualifying players; LG always uses {c:g}.",
        r"Same ~62k player-season ability pool; different team-unit structure fed to LOO / L_C.",
        r"Estimand: rotation-peer pools (not full roster sheets; not a minutes simulator).",
        r"Companion: grandchild_assign/GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--season-min", type=int, default=2011)
    parser.add_argument("--season-max", type=int, default=2021)
    args = parser.parse_args()

    ensure_hero_dirs()
    if not args.slides_only:
        _regenerate(season_min=args.season_min, season_max=args.season_max)

    meta = load_meta(META)
    seasons = meta.get("seasons_label", "2011-2021")
    ncaa = meta.get("team_season_summary", {})
    lg = meta.get("lg_team_season_summary", {})
    c = meta.get("lg_roster_size_reference", 15)

    subtitle = (
        rf"MBB {seasons} · min 20 min · NCAA mean={ncaa.get('mean', 0):.1f} vs LG "
        rf"$C={c:g}$ · {ncaa.get('n', 0):,} vs {lg.get('n', 0):,} team-seasons"
    )

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT_PPTX,
        title=r"NCAA vs LG — roster sizes fed into the pipeline",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {OUT_PPTX}")


if __name__ == "__main__":
    main()
