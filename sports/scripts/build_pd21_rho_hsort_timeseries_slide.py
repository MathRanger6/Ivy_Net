#!/usr/bin/env python3
"""Build PD21 dual-axis rho* / H_sort timeseries AUTO slide.

AUTO text is authoritative — copy title, subtitle, bullets, and claim into HAND verbatim.

Run (repo root):
  python sports/scripts/build_pd21_rho_hsort_timeseries_slide.py --slides-only
  python sports/scripts/build_pd21_rho_hsort_timeseries_slide.py --ppm-zero-below-minutes 20 --slides-only

Output:
  slides/auto/CHAR_PD21_rho_hsort_timeseries_AUTO.pptx              (hero — optional)
  slides/auto/CHAR_PD21_rho_hsort_timeseries_ppm0lt20_AUTO.pptx   (HAND20 slide 16 — contrast)

Figure: pd21_rho/PD21_rho_hsort_calibrate_2011_2021[_ppm0lt20]_bracket_rho_hsort_timeseries.png
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import AUTO_PD21_RHO_TIMESERIES_DECK, PD21_RHO, ensure_hero_dirs
from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)
from h_sort_readout import h_sort_definition_bullet
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd21_slide_common import (
    calibrate_role_bullet,
    is_contrast_panel,
    jump_2014_2015_bullet,
    panel_bullet,
    timeseries_claim,
    timeseries_title,
)

CALIBRATE_SCRIPT = SCRIPTS / "pd21_rho_hsort_calibrate.py"


def _w():
    return current_window()


def _panel_tag(*, ppm_zero_below_minutes: float | None) -> str | None:
    if ppm_zero_below_minutes is None:
        return None
    thr = float(ppm_zero_below_minutes)
    tag_mm = int(thr) if float(thr).is_integer() else thr
    return f"ppm0lt{tag_mm}"


def _artifact_paths(*, ppm_zero_below_minutes: float | None) -> tuple[Path, Path, Path]:
    tag = _panel_tag(ppm_zero_below_minutes=ppm_zero_below_minutes)
    stem = f"PD21_rho_hsort_calibrate_{_w().tag}"
    if tag:
        stem = f"{stem}_{tag}"
    fig = PD21_RHO / f"{stem}_bracket_rho_hsort_timeseries.png"
    fit = PD21_RHO / f"{stem}_fit_bracket.json"
    base_deck = AUTO_PD21_RHO_TIMESERIES_DECK
    if tag:
        base_deck = AUTO_PD21_RHO_TIMESERIES_DECK.with_name(
            AUTO_PD21_RHO_TIMESERIES_DECK.stem.replace("_AUTO", f"_{tag}_AUTO") + ".pptx"
        )
    out_pptx = auto_deck_path(base_deck)
    return fig, fit, out_pptx


def _refresh_plot(*, ppm_zero_below_minutes: float | None) -> None:
    cmd = [sys.executable, str(CALIBRATE_SCRIPT), "--plot-only", *window_cli_flags()]
    if ppm_zero_below_minutes is not None:
        cmd.extend(["--ppm-zero-below-minutes", str(float(ppm_zero_below_minutes))])
    print("Refreshing timeseries PNG (plot-only) ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(fit: dict) -> list[str]:
    long = fit.get("longitudinal", {})
    per = fit.get("per_season", [])
    mean_rho = float(np.mean([float(r["rho_star"]) for r in per])) if per else float("nan")
    h_emp_mean = long.get("h_sort_empirical_mean_over_seasons")
    if h_emp_mean is None and per:
        h_emp_mean = float(np.mean([float(r["h_sort_empirical"]) for r in per]))
    n_capped = sum(1 for row in per if row.get("rho_star_capped_at_max"))
    if n_capped == 0 and fit.get("bracket", {}).get("rho_max") is not None:
        rho_max_fit = float(fit["bracket"]["rho_max"])
        n_capped = sum(
            1
            for row in per
            if np.isclose(float(row.get("rho_star", -1.0)), rho_max_fit)
            and float(row.get("h_sort_abs_err", 0.0)) > 0.005
        )

    bullets = [
        calibrate_role_bullet(fit),
        panel_bullet(fit),
        r"Red (left): per-season calibrated $\rho^*$; dotted red = mean $\rho^*$ "
        rf"($\approx {mean_rho:.3g}$). Open circles = hit $\rho_{{\max}}$ cap.",
        r"Blue (right): empirical $H_{\mathrm{sort}}$ by season; dotted blue = "
        rf"longitudinal mean $H_{{\mathrm{{sort}}}}^{{\mathrm{{emp}}}}$ "
        rf"($\approx {float(h_emp_mean):.3f}$)." if h_emp_mean is not None else
        r"Blue (right): empirical $H_{\mathrm{sort}}$ by season; dotted blue = longitudinal mean.",
        h_sort_definition_bullet(),
    ]
    jump = jump_2014_2015_bullet(fit)
    if jump:
        bullets.append(jump)
    if n_capped:
        bullets.append(
            f"{n_capped} season(s) at bracket cap — sim $H_{{\\mathrm{{sort}}}}$ still below "
            r"empirical at $\rho_{\max}$."
        )
    if is_contrast_panel(fit):
        bullets.append(
            r"Pair with PD22 ESPN coverage (HAND20 slide 9) — roster-depth context for ppm0lt20; "
            r"mid-decade $\rho^*$ spike is not the locked calibration estimand."
        )
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD21 rho/H_sort timeseries AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + fit JSON")
    parser.add_argument(
        "--ppm-zero-below-minutes",
        type=float,
        default=None,
        metavar="M",
        help="Build contrast AUTO deck (_ppm0ltM suffix)",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    fig, fit_path, out_pptx = _artifact_paths(ppm_zero_below_minutes=args.ppm_zero_below_minutes)

    ensure_hero_dirs()
    if not args.slides_only:
        _refresh_plot(ppm_zero_below_minutes=args.ppm_zero_below_minutes)

    fit = load_meta(fit_path)
    if not fit:
        raise SystemExit(f"Missing fit JSON: {fit_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    seasons = fit.get("seasons", "2011-2021")
    role = "contrast ppm0lt20" if is_contrast_panel(fit) else "hero panel"

    subtitle = (
        rf"PD21 · per-season $\rho^*$ vs empirical $H_{{\mathrm{{sort}}}}$ · {seasons} · {role}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=timeseries_title(fit),
        subtitle=subtitle,
        bullets=_readout_bullets(fit),
        claim=timeseries_claim(fit),
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
