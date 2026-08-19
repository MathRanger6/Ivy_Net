#!/usr/bin/env python3
"""Build PD22 item 8 bench-zero vs H_sort mechanism AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_ppm_zero_hsort_mechanism_slide.py --slides-only
  python sports/scripts/build_pd22_ppm_zero_hsort_mechanism_slide.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD22_PPM_ZERO_HSORT_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
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


STEM_PREFIX = "PD22_ppm_zero_hsort_mechanism"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

SCRIPT = SCRIPTS / "pd22_ppm_zero_hsort_mechanism.py"
HERO_LOCK = 20.0

CLAIM = (
    r"Claim (PD22): PPM-zero piles identical bench abilities on rosters — "
    r"check whether that mechanically inflates empirical $H_{\mathrm{sort}}$ vs drop-at-20."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_PPM_ZERO_HSORT_DECK)


def _refresh(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    print("Running PPM-zero H_sort mechanism ..." if not plot_only else "Refreshing PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")

    return [
        r"PD22 item 8: bench-zero share vs within-team dispersion; season $H_{\mathrm{sort}}$ drop vs PPM-zero.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · PPM-zero floor = {m(HERO_LOCK, decimals=0)} min.",
        rf"Team-season scatter: corr(zero fraction, within-team perf std) = "
        rf"{m(float(s.get('corr_zero_fraction_vs_perf_std', 0)), decimals=3)} "
        rf"({m(int(s.get('n_team_seasons', 0)))} team-seasons).",
        rf"Mean empirical $H_{{\mathrm{{sort}}}}$: drop = "
        rf"{m(float(s.get('h_sort_drop_mean', 0)), decimals=4)} vs PPM-zero = "
        rf"{m(float(s.get('h_sort_ppm_zero_mean', 0)), decimals=4)} "
        rf"($\Delta$ mean = {m(float(s.get('h_sort_delta_mean', 0)), decimals=4)}).",
        rf"Teams with $\geq$ half roster zeroed: {m(int(s.get('n_team_seasons_ge_half_zeroed', 0)))}.",
        r"Left: more bench zeros $\Rightarrow$ lower within-team dispersion (identical zeroed cohort). "
        r"Right: season $H_{\mathrm{sort}}$ under both panel policies.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 item 8 H_sort mechanism AUTO slide.")
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--plot-only", action="store_true")
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

    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    subtitle = (
        rf"PD22 item 8 · bench zeros vs $H_{{\mathrm{{sort}}}}$ · {seasons} · "
        rf"$\Delta$ mean = {m(float(s.get('h_sort_delta_mean', 0)), decimals=4)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — bench-zero clustering vs empirical sorting",
        subtitle=subtitle,
        bullets=[b for b in _readout_bullets(meta) if b],
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
