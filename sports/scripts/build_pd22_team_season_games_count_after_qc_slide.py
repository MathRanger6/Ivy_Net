#!/usr/bin/env python3
"""Build PD22 team-season games count AUTO slide — after box QC.

Run (repo root):
  python sports/scripts/build_pd22_team_season_games_count_after_qc_slide.py --slides-only
  python sports/scripts/build_pd22_team_season_games_count_after_qc_slide.py

Output:
  slides/auto/CHAR_PD22_team_season_games_count_after_qc_AUTO.pptx

Pair with raw motivation slide: CHAR_PD22_team_season_games_count_AUTO.pptx
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (
    AUTO_PD22_TEAM_SEASON_GAMES_AFTER_QC_DECK,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, MIN_TEAM_SEASON_GAMES, KEEP_MIN_TEAM_SEASON_GAMES, m, mgeq, mleq

DIST_SCRIPT = SCRIPTS / "pd22_team_season_games_count.py"
SEASON_MIN = 2011
SEASON_MAX = 2021
STEM = f"PD22_team_season_games_count_after_qc_{SEASON_MIN}_{SEASON_MAX}"
DEFAULT_MIN_GAMES = MIN_TEAM_SEASON_GAMES
KEEP_MIN_GAMES = KEEP_MIN_TEAM_SEASON_GAMES

CLAIM = (
    rf"Claim (PD22 backup): After box QC, team-season game counts are full-season D-I coverage "
    rf"({mgeq(KEEP_MIN_GAMES)} games) — low-game tail ({mleq(DEFAULT_MIN_GAMES)} games) removed before panel build."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{STEM}.png"
    meta = PD22_MINUTES / f"{STEM}.json"
    return fig, meta, AUTO_PD22_TEAM_SEASON_GAMES_AFTER_QC_DECK


def _refresh(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(DIST_SCRIPT), "--after-qc-only"]
    if plot_only:
        cmd.append("--plot-only")
    print("Running after-QC games count ..." if not plot_only else "Refreshing after-QC PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    n_ts = int(meta.get("n_team_seasons", 0))
    med = float(meta.get("games_n_median", 0))
    mean = float(meta.get("games_n_mean", 0))
    qc = meta.get("box_qc_report") or {}
    dropped_ts = int(qc.get("team_seasons_dropped_low_games", 0))

    return [
        rf"PD22 backup (after filter): distinct game\_ids per (team\_id, season) surviving box QC.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {m(n_ts)} team-seasons kept · median = {m(med, decimals=0)} games · mean = {m(mean, decimals=1)} · "
        rf"min = {m(int(meta.get('games_n_min', 0)))} (all {mgeq(KEEP_MIN_GAMES)}).",
        rf"Removed by min\_team\_season\_games={DEFAULT_MIN_GAMES}: {m(dropped_ts)} team-seasons "
        rf"with {mleq(DEFAULT_MIN_GAMES)} games (see raw games-count slide).",
        rf"Dropped dash rows: {m(int(qc.get('dash_rows_dropped', 0)))} game rows before game-count tally.",
        rf"No one-game spike — bulk mass sits near {m(28)}–{m(32)} games (normal D-I seasons).",
        r"Left: linear counts; right: log $y$ — post-QC panel is what roster-size and minutes diagnostics use.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 after-QC games count AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG only")
    args = parser.parse_args()

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    med = float(meta.get("games_n_median", 0))
    n_ts = int(meta.get("n_team_seasons", 0))
    subtitle = (
        rf"PD22 · games after box QC · {SEASON_MIN}–{SEASON_MAX} · "
        rf"{m(n_ts)} team-seasons · median = {m(med, decimals=0)} · min {mgeq(KEEP_MIN_GAMES)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Games per team-season after box QC",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
