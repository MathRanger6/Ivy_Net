#!/usr/bin/env python3
"""Build PD22 item 6 PPM-zero vs drop ability AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_ppm_zero_ability_slide.py --slides-only
  python sports/scripts/build_pd22_ppm_zero_ability_slide.py

Output:
  slides/auto/CHAR_PD22_ppm_zero_ability_distribution_AUTO.pptx
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD22_PPM_ZERO_ABILITY_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mn, mlt, mpct

SCRIPT = SCRIPTS / "pd22_ppm_zero_ability_distribution.py"
SEASON_MIN = 2011
SEASON_MAX = 2021
STEM = f"PD22_ppm_zero_ability_distribution_{SEASON_MIN}_{SEASON_MAX}"
HERO_LOCK = 20.0

CLAIM = (
    r"Claim (PD22): PPM-zero keeps bench players on roster at forced PPM = 0 — "
    r"expect a zero-heavy ability distribution vs the min-20 drop panel; "
    r"may inflate homophily if identical zeros cluster on teams."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{STEM}.png"
    meta = PD22_MINUTES / f"{STEM}.json"
    return fig, meta, AUTO_PD22_PPM_ZERO_ABILITY_DECK


def _refresh(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    print("Running PPM-zero ability distribution ..." if not plot_only else "Refreshing PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    thr = float(s.get("ppm_zero_below_minutes", HERO_LOCK))

    return [
        r"PD22 item 6: PPM-zero vs drop — raw PPM and ASSIGN ability (PPM z within season).",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · floor = {m(thr, decimals=0)} min.",
        rf"Drop panel ({mn(int(s.get('n_drop_panel', 0)))}): sub-{HERO_LOCK:g} rows removed at rebuild.",
        rf"PPM-zero panel ({mn(int(s.get('n_ppm_zero_panel', 0)))}): "
        rf"{m(int(s.get('n_zeroed_by_policy', 0)))} rows ({mpct(float(s.get('pct_zeroed_by_policy', 0)))}) "
        rf"forced to PPM $= 0$ (min {mlt(thr)}).",
        rf"Raw PPM spike: {m(int(s.get('n_raw_ppm_eq_zero_ppm_zero', 0)))} rows at PPM $= 0$ under PPM-zero.",
        rf"ASSIGN below $-1$ z: drop {m(int(s.get('n_perf_below_minus1_drop', 0)))} vs "
        rf"PPM-zero {m(int(s.get('n_perf_below_minus1_ppm_zero', 0)))}; "
        rf"zeroed cohort median = {m(float(s.get('ppm_zero_perf_median_zeroed_cohort', 0)), decimals=2)}.",
        r"Left column = drop (PD21 default). Right column = PPM-zero alternative flagged for induced homophily.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 item 6 PPM-zero ability AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV only")
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

    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    subtitle = (
        rf"PD22 item 6 · PPM-zero vs drop · {seasons} · "
        rf"{m(int(s.get('n_zeroed_by_policy', 0)))} bench rows at PPM $= 0$"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — ability under PPM-zero vs drop policy",
        subtitle=subtitle,
        bullets=[b for b in _readout_bullets(meta) if b],
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
