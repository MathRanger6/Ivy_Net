#!/usr/bin/env python3
"""Build PD22 single-season interval overlap AUTO slide (items 10–11).

Run (repo root):
  python sports/scripts/build_pd22_interval_overlap_season_slide.py --season 2012 --slides-only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import PD22_MINUTES, SLIDES_AUTO, ensure_hero_dirs
from interval_overlap_readouts import empirical_overlap_bullets
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()

SCRIPT = SCRIPTS / "pd22_interval_overlap_season.py"
DEFAULT_SEASON = 2012


def _artifact_paths(season: int) -> tuple[Path, Path, Path]:
    stem = f"PD22_interval_overlap_season_{season}"
    fig = PD22_MINUTES / f"{stem}.png"
    meta = PD22_MINUTES / f"{stem}.json"
    deck = auto_deck_path(SLIDES_AUTO / f"CHAR_PD22_interval_overlap_season_{season}_AUTO.pptx")
    return fig, meta, deck


def _refresh(*, season: int, plot_only: bool) -> None:
    cmd = [sys.executable, str(SCRIPT), "--season", str(season)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict, *, season: int) -> list[str]:
    rho = meta.get("rho_star_drop_bracket")
    item = meta.get("pd22_item") or (10 if season == 2012 else 11)
    rho_s = m(float(rho), decimals=3) if rho is not None else r"$?$"

    bullets = [
        rf"PD22 item {item}: single-season interval overlap — season {m(season)} only (not pooled).",
        BOX_QC_PANEL_NOTE,
        rf"Bracket $\rho^*$ (drop-at-20): {rho_s} · "
        rf"$H_{{\mathrm{{sort}}}}$ = {m(float(meta.get('H_sort', 0)), decimals=4)}.",
        r"Each team-season: talent window $[\min \hat{A}_i, \max \hat{A}_i]$ on PPM $z$.",
        r"Top-left: coverage along spectrum; crimson dashed = disjoint sort-and-chop benchmark.",
        r"Bottom: roster intervals sorted by $\hat{T}_j$ — stacking = overlap.",
    ]
    if rho is not None and abs(float(rho)) < 0.01:
        bullets.append(
            r"$\rho^* \approx 0$ but overlap structure remains — bracket fit $\neq$ visual absence of sorting."
        )
    bullets.extend(empirical_overlap_bullets(meta, paired_compare=True)[-2:])
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 interval overlap season slide.")
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON)
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--plot-only", action="store_true")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    season = int(args.season)
    fig, meta_path, out_pptx = _artifact_paths(season)
    ensure_hero_dirs()
    out_pptx.parent.mkdir(parents=True, exist_ok=True)

    if not args.slides_only:
        _refresh(season=season, plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta or not fig.is_file():
        raise SystemExit(f"Missing artifacts for season {season}")

    rho = meta.get("rho_star_drop_bracket")
    item = meta.get("pd22_item") or (10 if season == 2012 else 11)
    h_sort = meta.get("H_sort")
    n_ts = meta.get("n_team_seasons")

    claim = (
        r"Claim (PD22): Single-season overlap diagnostic — does talent-window stacking "
        r"persist when bracket $\rho^* \approx 0$?"
        if rho is not None and abs(float(rho)) < 0.01
        else r"Claim (PD22): Single-season talent-window overlap vs bracket $\rho^*$."
    )

    subtitle_parts = [
        rf"PD22 item {item} · season {season} · min 20 min drop panel",
    ]
    if n_ts:
        subtitle_parts.append(rf"{n_ts:,} team-seasons")
    if h_sort is not None:
        subtitle_parts.append(rf"$H_{{\mathrm{{sort}}}}={float(h_sort):.3f}$")
    if rho is not None:
        subtitle_parts.append(rf"$\rho^*={float(rho):g}$")

    build_interval_overlap_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=rf"PD22 — team interval overlap · season {season}",
        subtitle=" · ".join(subtitle_parts),
        bullets=_readout_bullets(meta, season=season),
        claim=claim,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
