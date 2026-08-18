#!/usr/bin/env python3
"""Build PD22 items 3–4 PPM distribution AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_ppm_distribution_slide.py --slides-only
  python sports/scripts/build_pd22_ppm_distribution_slide.py

Output:
  slides/auto/CHAR_PD22_ppm_distribution_AUTO.pptx

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

from hero_gallery_paths import AUTO_PD22_PPM_DISTRIBUTION_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mn, mgt, mlt, mpct

PPM_SCRIPT = SCRIPTS / "pd22_ppm_distribution.py"
SEASON_MIN = 2011
SEASON_MAX = 2021
STEM = f"PD22_ppm_distribution_{SEASON_MIN}_{SEASON_MAX}"
HERO_LOCK = 20.0

CLAIM = (
    r"Claim (PD22): Minutes floor guards against noisy PPM tails — "
    r"sub-20-min rows include extreme points-per-minute spikes; hero ASSIGN uses "
    r"PPM z-scored within season on the min-20 panel."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{STEM}.png"
    meta = PD22_MINUTES / f"{STEM}.json"
    return fig, meta, AUTO_PD22_PPM_DISTRIBUTION_DECK


def _refresh_ppm(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(PPM_SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    print("Running PPM distribution ..." if not plot_only else "Refreshing PPM PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    spec = meta.get("panel_spec") or {}

    return [
        r"PD22 items 3–4: points-per-minute (PPM) — filtered-out tail vs hero ASSIGN input.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · hero lock min = {m(HERO_LOCK, decimals=0)} min.",
        rf"Item 3 (left): {m(int(s.get('n_filtered_out_total', 0)))} rows with minutes {mlt(HERO_LOCK)} "
        rf"({m(int(s.get('n_filtered_out_zero_minutes', 0)))} at {m(0)} min excluded from PPM hist).",
        rf"Sub-{HERO_LOCK:g}-min with PPM {mgt(1.0)}: {m(int(s.get('n_filtered_out_ppm_gt_1', 0)))}; "
        rf"max raw PPM in tail: {m(float(s.get('filtered_out_ppm_max', 0)), decimals=2)}.",
        rf"Item 4 (right): hero panel {mn(int(s.get('n_hero_panel', 0)))} — raw PPM then "
        r"PPM z within season (PD21 ASSIGN ability; empirical roster caps are separate).",
        rf"Hero raw PPM median = {m(float(s.get('hero_raw_ppm_median', 0)), decimals=3)}; "
        rf"standardized ability median = {m(float(s.get('hero_perf_median', 0)), decimals=2)}.",
        r"Left: why minutes matter (garbage-time PPM spikes). "
        r"Right: what enters homophily calibration after the floor.",
        spec.get("assign_ability", ""),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 PPM distribution AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV only")
    args = parser.parse_args()

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh_ppm(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing PPM JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    subtitle = (
        rf"PD22 · PPM tails · {seasons} · "
        rf"{m(int(s.get('n_filtered_out_ppm_gt_1', 0)))} sub-{HERO_LOCK:g}-min rows with PPM {mgt(1)}"
    )

    bullets = [b for b in _readout_bullets(meta) if b]

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — PPM distribution: filtered-out tail vs hero ASSIGN input",
        subtitle=subtitle,
        bullets=bullets,
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
