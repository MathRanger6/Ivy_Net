#!/usr/bin/env python3
"""Build PD22 item 2 raw panel minutes distribution AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_raw_minutes_distribution_slide.py --slides-only
  python sports/scripts/build_pd22_raw_minutes_distribution_slide.py

Output:
  slides/auto/CHAR_PD22_raw_minutes_distribution_AUTO.pptx

Copy into HAND: Change Picture + bullets from AUTO deck.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD22_RAW_MINUTES_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mpct

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_raw_minutes_distribution"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

DIST_SCRIPT = SCRIPTS / "pd22_raw_minutes_distribution.py"

CLAIM = (
    r"Claim (PD22): Minutes floor must be grounded in the raw roster distribution — "
    r"not an arbitrary cut — before we defend min 20 min for $\rho$ / ASSIGN panels."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_RAW_MINUTES_DECK)


def _refresh_distribution(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(DIST_SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    print(
        "Running raw minutes distribution ..."
        if not plot_only
        else "Refreshing minutes distribution PNG ..."
    )
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    n_all = int(s.get("n_player_seasons", 0))
    n_draft = int(s.get("n_drafted_player_seasons", 0))
    med = s.get("minutes_median")
    p90 = s.get("minutes_p90")
    med_fmt = m(float(med), decimals=0) if med is not None else "?"
    p90_fmt = m(float(p90), decimals=0) if p90 is not None else "?"

    return [
        r"PD22 item 2: season-minutes on box-QC panel (min\_minutes=0 rebuild).",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · {m(n_all)} player-seasons · {m(n_draft)} ever-draft rows.",
        rf"Median minutes = {med_fmt}; 90th percentile = {p90_fmt}.",
        rf"Zero-minute rows: {m(int(s.get('n_zero_minutes', 0)))} "
        rf"({mpct(float(s.get('pct_zero_minutes', 0)))} of panel).",
        rf"Below {m(10)} min: {mpct(float(s.get('pct_below_10', 0)))}; "
        rf"below {m(20)} min: {mpct(float(s.get('pct_below_20', 0)))} (hero lock).",
        rf"Ever-draft below {m(20)} min: {mpct(float(s.get('drafted_pct_below_20', 0)))} "
        rf"(median drafted = {m(float(s.get('drafted_minutes_median', 0)), decimals=0)} min).",
        rf"Left: empirical cumulative distribution function (ECDF) — all vs ever-draft; teal = {m(10)} min, red = {m(20)} min.",
        rf"Right: histogram zoom {m(0)}–{m(150)} min — low-minute mass driving floor choice.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 raw minutes distribution AUTO slide.")
    parser.add_argument(
        "--slides-only",
        action="store_true",
        help="Use existing PNG + JSON (no distribution rerun)",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from CSV only, then build slide",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh_distribution(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing distribution JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    subtitle = (
        rf"PD22 · raw panel minutes · {seasons} · "
        rf"median = {m(float(s.get('minutes_median', 0)), decimals=0)} min · "
        rf"{mpct(float(s.get('pct_below_20', 0)))} below {m(20)} min"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Raw panel season-minutes distribution",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
