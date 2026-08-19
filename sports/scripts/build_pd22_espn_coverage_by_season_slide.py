#!/usr/bin/env python3
"""Build PD22 ESPN box coverage-by-season backup AUTO slide (SCOUT verify).

Run (repo root):
  python sports/scripts/build_pd22_espn_coverage_by_season_slide.py --slides-only
  python sports/scripts/build_pd22_espn_coverage_by_season_slide.py

Output:
  slides/auto/CHAR_PD22_espn_coverage_by_season_AUTO.pptx
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD22_ESPN_COVERAGE_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import m, mgeq, marrow, mpct

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_espn_coverage_by_season"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

DIST_SCRIPT = SCRIPTS / "pd22_espn_coverage_by_season.py"
HERO_LOCK = 20.0

CLAIM = (
    r"Claim (PD22 backup): 2013→2014 jump in raw player-season counts is ESPN box **depth** "
    r"(more players listed per game), not doubled games — hero min-20 panel is longitudinal-safe for $\rho$ / $H_{\mathrm{sort}}$."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_ESPN_COVERAGE_DECK)


def _refresh(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(DIST_SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    print("Running ESPN coverage diagnostic ..." if not plot_only else "Refreshing coverage PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    jump = meta.get("jump_2013_2014") or {}
    ov = meta.get("overlap_teams_2013_2014") or {}
    ps_raw = jump.get("player_seasons_raw_pct_change")
    ps_min20 = jump.get("player_seasons_min20_pct_change")
    games = jump.get("games_pct_change")
    roster = jump.get("median_roster_per_ts_pct_change")
    rpg = jump.get("mean_box_rows_per_game_team_pct_change")

    return [
        r"PD22 backup (SCOUT Aug 2026): frozen \texttt{mbb\_df\_player\_box.csv} — season coverage for $\rho$ timeseries jump.",
        r"Source: distinct player-season rows aggregated from ESPN box (2011–2021); CSV not rewritten on disk.",
        rf"2013→2014 raw player-seasons: {marrow(int(jump.get('player_seasons_raw_2013', 0)), int(jump.get('player_seasons_raw_2014', 0)))} "
        rf"({mpct(ps_raw) if ps_raw is not None else '?'}); "
        rf"games {mpct(games) if games is not None else '?'} only.",
        rf"Roster depth: median players/team-season {mpct(roster) if roster is not None else '?'}; "
        rf"mean box rows/game/team {mpct(rpg) if rpg is not None else '?'} — ESPN lists more bench lines from 2014.",
        rf"Overlap teams only ({m(int(ov.get('overlap_teams', 0)))} schools): player-seasons "
        rf"{marrow(int(ov.get('player_seasons_overlap_2013', 0)), int(ov.get('player_seasons_overlap_2014', 0)))} (+44\% on same team\_ids).",
        rf"Hero panel (box QC + min {mgeq(HERO_LOCK)}): {marrow(int(jump.get('player_seasons_min20_2013', 0)), int(jump.get('player_seasons_min20_2014', 0)))} "
        rf"({mpct(ps_min20) if ps_min20 is not None else '?'}).",
        rf"Left: raw aggregate jumps at 2014; orange min-{HERO_LOCK:g} line flat — use for PD21 $\rho$ calibration, not ppm0lt20.",
        r"Right: median roster size and rows/game/team — SCOUT verify against ESPN API sample games 2013 vs 2014.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 ESPN coverage backup AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    jump = meta.get("jump_2013_2014") or {}
    subtitle = (
        rf"PD22 · ESPN box coverage · {_w().season_min}–{_w().season_max} · "
        rf"2013→2014 raw +{mpct(jump.get('player_seasons_raw_pct_change', 0))} · "
        rf"min-{HERO_LOCK:g} +{mpct(jump.get('player_seasons_min20_pct_change', 0))}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — ESPN box coverage by season (2013→2014 depth break)",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
