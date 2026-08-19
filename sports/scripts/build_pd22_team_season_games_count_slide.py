#!/usr/bin/env python3
"""Build PD22 team-season games-count backup AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_team_season_games_count_slide.py --slides-only

Output:
  slides/auto/CHAR_PD22_team_season_games_count_AUTO.pptx

Copy into HAND: Change Picture + bullets from AUTO deck.

Figure source: PD22_team_season_games_count_2011_2021.png (+ JSON/CSV in pd22_minutes/).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (
    AUTO_PD22_TEAM_SEASON_GAMES_DECK,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta

from pd22_slide_common import KEEP_MIN_TEAM_SEASON_GAMES, MIN_TEAM_SEASON_GAMES, m, mgeq, mgt, mleq, mpct, msim

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_team_season_games_count"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

DEFAULT_MIN_GAMES = MIN_TEAM_SEASON_GAMES
KEEP_MIN_GAMES = KEEP_MIN_TEAM_SEASON_GAMES

CLAIM = (
    rf"Claim (PD22 backup): Box panel mixes full D-I seasons ({msim(30)} games) with sparse "
    rf"one-game team-seasons — default min\_team\_season\_games={DEFAULT_MIN_GAMES} drops team-seasons "
    rf"with {mleq(DEFAULT_MIN_GAMES)} games (keep {mgeq(KEEP_MIN_GAMES)}) before player-season aggregation."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_TEAM_SEASON_GAMES_DECK)


def _readout_bullets(meta: dict) -> list[str]:
    n_ts = int(meta.get("n_team_seasons", 0))
    n1 = int(meta.get("n_with_1_game", 0))
    pct1 = 100.0 * float(meta.get("pct_with_1_game", 0))
    med = float(meta.get("games_n_median", 0))
    mean = float(meta.get("games_n_mean", 0))
    le_key = f"n_with_{DEFAULT_MIN_GAMES}_or_fewer"
    n_le = int(meta.get(le_key, 0))
    n_gt = max(n_ts - n_le, 0)
    pct_le = 100.0 * n_le / n_ts if n_ts else 0.0

    return [
        r"PD22 backup: distinct game\_ids per (team\_id, season) in raw box (2011–2021).",
        rf"Panel: {m(n_ts)} team-seasons · median = {m(med, decimals=0)} games · mean = {m(mean, decimals=1)} · max = {m(int(meta.get('games_n_max', 0)))}.",
        rf"Bimodal: {m(n1)} team-seasons ({mpct(pct1)}) with only {m(1)} game (red line) vs cluster near {m(30)}–{m(32)} (full seasons).",
        rf"{mleq(DEFAULT_MIN_GAMES)} games: {m(n_le)} ({mpct(pct_le)}); {mgt(DEFAULT_MIN_GAMES)} games: {m(n_gt)} — sparse tail is partial coverage / small-school noise.",
        rf"Default box QC (panel\_rebuild): min\_team\_season\_games={DEFAULT_MIN_GAMES} drops team-seasons with {mleq(DEFAULT_MIN_GAMES)} games (keep {mgeq(KEEP_MIN_GAMES)}).",
        r"Left: linear counts; right: log $y$ — gap between spikes is low-frequency partial seasons, not hero-panel mass.",
        r"Pairs with roster-size backup: low-game team-seasons often inflate per-game roster anomalies (SCOUT ESPN dash rows).",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 team-season games count AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    n1 = int(meta.get("n_with_1_game", 0))
    med = float(meta.get("games_n_median", 0))
    subtitle = (
        rf"PD22 · team-season games · {_w().season_min}–{_w().season_max} · "
        rf"{m(n1)} with {m(1)} game · median = {m(med, decimals=0)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Games per team-season in raw box data (before QC)",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
