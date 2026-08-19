#!/usr/bin/env python3
"""Build PD22 item 9 panel policy compare AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_panel_policy_compare_slide.py --slides-only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD22_PANEL_POLICY_COMPARE_DECK, PD22_MINUTES, ensure_hero_dirs
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


STEM_PREFIX = "PD22_panel_policy_compare"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

SCRIPT = SCRIPTS / "pd22_panel_policy_compare.py"
HERO_LOCK = 20.0

CLAIM = (
    r"Claim (PD22): At min 20, drop vs PPM-zero — bracket $\rho^*$ and empirical "
    r"$H_{\mathrm{sort}}$ decide which panel policy enters PD21 calibration."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_PANEL_POLICY_COMPARE_DECK)


def _refresh(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")

    return [
        r"PD22 item 9: panel policy compare at min 20 — drop (PD21 default) vs PPM-zero.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · floor = {m(HERO_LOCK, decimals=0)} min.",
        rf"Longitudinal bracket $\rho^*$: drop = {m(float(s.get('rho_star_longitudinal_drop', 0)), decimals=3)} "
        rf"vs PPM-zero = {m(float(s.get('rho_star_longitudinal_ppm_zero', 0)), decimals=3)} "
        + (
            r"(legacy JSON — pre-box-QC $H_{\mathrm{sort}}$ target)."
            if s.get("rho_star_longitudinal_ppm_zero_stale")
            else "."
        ),
        rf"Empirical $H_{{\mathrm{{sort}}}}$ mean (current panel, item 8): drop = "
        rf"{m(float(s.get('h_sort_emp_mean_drop', 0)), decimals=4)} vs PPM-zero = "
        rf"{m(float(s.get('h_sort_emp_mean_ppm_zero', 0)), decimals=4)} "
        rf"($\Delta$ = {m(float(s.get('h_sort_emp_mean_delta', 0)), decimals=4)}).",
        rf"Seasons with $\rho^* = 0$: drop {m(int(s.get('n_seasons_rho_zero_drop', 0)))} / "
        rf"{m(int(_w().season_max - _w().season_min + 1))} vs PPM-zero "
        rf"{m(int(s.get('n_seasons_rho_zero_ppm_zero', 0)))}.",
        rf"Recommendation: **{s.get('recommended_policy', 'drop')}** — "
        r"PPM-zero inflates $\rho^*$ without proportional $H_{\mathrm{sort}}$ gain; "
        r"partial shrinkage not pursued.",
        r"Top: per-season $\rho^*$. Bottom: empirical $H_{\mathrm{sort}}$ (items 6–8 context).",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 item 9 policy compare AUTO slide.")
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
    if not meta or not fig.is_file():
        raise SystemExit(f"Missing artifacts: {meta_path} / {fig}")

    s = meta.get("summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    subtitle = (
        rf"PD22 item 9 · policy compare · {seasons} · "
        rf"$\rho^*$ drop {m(float(s.get('rho_star_longitudinal_drop', 0)), decimals=3)} "
        rf"vs PPM-zero {m(float(s.get('rho_star_longitudinal_ppm_zero', 0)), decimals=3)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — panel policy: drop vs PPM-zero at min 20",
        subtitle=subtitle,
        bullets=[b for b in _readout_bullets(meta) if b],
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
