#!/usr/bin/env python3
"""Build PD21 ρ → H_sort calibration AUTO slide (Alex ASSIGN calibration).

AUTO text is authoritative — copy title, subtitle, bullets, and claim into HAND verbatim.

Run (repo root):
  python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py --slides-only
  python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py
  python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py --ppm-zero-below-minutes 20 --slides-only

Output:
  slides/auto/CHAR_PD21_rho_hsort_calibrate_AUTO.pptx              (HAND20 slide 14 — hero)
  slides/auto/CHAR_PD21_rho_hsort_calibrate_ppm0lt20_AUTO.pptx     (HAND20 slide 15 — contrast)

Figure: pd21_rho/PD21_rho_hsort_calibrate_2011_2021[_ppm0lt20]_bracket.png
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

from hero_gallery_paths import AUTO_PD21_RHO_DECK, PD21_RHO, ensure_hero_dirs
from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)
from h_sort_readout import h_sort_definition_bullet, h_sort_note_bullet
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta
from pd21_slide_common import (
    calibrate_claim,
    calibrate_role_bullet,
    calibrate_title,
    contrast_do_dont_bullets,
    hero_do_dont_bullets,
    inset_bullet,
    is_contrast_panel,
    jump_2014_2015_bullet,
    panel_bullet,
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
    fig = PD21_RHO / f"{stem}_bracket.png"
    fit = PD21_RHO / f"{stem}_fit_bracket.json"
    base_deck = AUTO_PD21_RHO_DECK
    if tag:
        base_deck = AUTO_PD21_RHO_DECK.with_name(
            AUTO_PD21_RHO_DECK.stem.replace("_AUTO", f"_{tag}_AUTO") + ".pptx"
        )
    out_pptx = auto_deck_path(base_deck)
    return fig, fit, out_pptx


def _refresh_plot(*, ppm_zero_below_minutes: float | None) -> None:
    cmd = [sys.executable, str(CALIBRATE_SCRIPT), "--plot-only", *window_cli_flags()]
    if ppm_zero_below_minutes is not None:
        cmd.extend(["--ppm-zero-below-minutes", str(float(ppm_zero_below_minutes))])
    print("Refreshing bracket PNG (plot-only) ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(fit: dict) -> list[str]:
    long = fit.get("longitudinal", {})
    rho_star = float(long.get("rho_star_longitudinal", float("nan")))
    err_star = float(long.get("mean_abs_err_at_star", float("nan")))
    err_ref = float(long.get("mean_abs_err_at_reference_rho", float("nan")))
    ref_rho = float(long.get("reference_rho", 0.5))
    n_seeds = int(fit.get("n_seeds", 50))
    bracket = fit.get("bracket", {})
    tol = bracket.get("tol", 0.001)

    per = fit.get("per_season", [])
    n_zero = sum(1 for row in per if float(row.get("rho_star", 1.0)) == 0.0)
    n_capped = sum(1 for row in per if row.get("rho_star_capped_at_max"))
    if n_capped == 0 and fit.get("bracket", {}).get("rho_max") is not None:
        rho_max_fit = float(fit["bracket"]["rho_max"])
        n_capped = sum(
            1
            for row in per
            if np.isclose(float(row.get("rho_star", -1.0)), rho_max_fit)
            and float(row.get("h_sort_abs_err", 0.0)) > 0.005
        )
    nonzero = [
        (int(row["season"]), float(row["rho_star"]))
        for row in per
        if float(row.get("rho_star", 0.0)) > 0.0
    ]
    nonzero_str = ", ".join(rf"{s}: \rho^* \approx {r:.3g}" for s, r in nonzero[:5])
    if len(nonzero) > 5:
        nonzero_str += ", …"

    err_star_s = f"{err_star:.2g}"
    err_ref_s = f"{err_ref:.3f}"
    rho_star_s = f"{rho_star:.4g}"
    h_sim = long.get("h_sort_sim_mean_at_star")
    h_emp = long.get("h_sort_empirical_mean_over_seasons")
    if h_sim is None:
        for row in long.get("curve", []):
            if abs(float(row["rho"]) - rho_star) < 1e-9:
                h_sim = row.get("h_sort_sim_mean_over_seasons")
                break
    if h_emp is None and fit.get("empirical_targets"):
        h_emp = float(np.mean([float(t["h_sort_empirical"]) for t in fit["empirical_targets"]]))
    h_sim_s = f"{float(h_sim):.3f}" if h_sim is not None else "?"
    h_emp_s = f"{float(h_emp):.3f}" if h_emp is not None else "?"

    bullets = [
        calibrate_role_bullet(fit),
        r"Alex (Aug 2026): calibrate ASSIGN $\rho$ so LG simulated $H_{\mathrm{sort}}$ "
        r"matches empirical NCAA; formal $\rho$ MLE parked.",
        panel_bullet(fit),
        f"Search: bracket + bisect (tol={tol:g}), {n_seeds} seeds/arm; "
        r"$H_{\mathrm{sort}}^{\mathrm{sim}}$ monotone in $\rho$.",
        h_sort_definition_bullet(),
        f"Longitudinal $\\rho^* \\approx {rho_star_s}$; "
        f"mean $H_{{\\mathrm{{sort}}}}^{{\\mathrm{{sim}}}}$ at $\\rho^*$ = {h_sim_s}; "
        f"mean $H_{{\\mathrm{{sort}}}}^{{\\mathrm{{emp}}}}$ = {h_emp_s}.",
        f"Per-season: {n_zero}/{len(per)} seasons at $\\rho^*=0$; "
        + (f"nonzero — {nonzero_str}" if nonzero_str else r"all at $\rho^*=0$.")
        + (f" · {n_capped} season(s) hit $\\rho_{{\\max}}$ cap." if n_capped else ""),
        f"Legacy reference $\\rho={ref_rho:g}$: mean $|error| \\approx {err_ref_s}$ "
        f"vs $\\approx {err_star_s}$ at $\\rho^*$.",
        inset_bullet(fit),
    ]
    jump = jump_2014_2015_bullet(fit)
    if jump:
        bullets.append(jump)
    if is_contrast_panel(fit):
        bullets.extend(contrast_do_dont_bullets())
    else:
        bullets.extend(hero_do_dont_bullets(fit))
    bullets.extend([
        h_sort_note_bullet(),
        r"Figure: small multiples — blue sim curve, red empirical line, green $\rho^*$ "
        r"(x-axis zoomed to evaluated bracket).",
    ])
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD21 ρ H_sort calibration AUTO slide.")
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

    n_seeds = int(fit.get("n_seeds", 50))
    seasons = fit.get("seasons", "2011-2021")
    tol = fit.get("bracket", {}).get("tol", 0.001)
    rho_star = float(fit.get("longitudinal", {}).get("rho_star_longitudinal", 0.0))
    role = "contrast ppm0lt20" if is_contrast_panel(fit) else "hero panel"

    subtitle = (
        rf"PD21 · LG ASSIGN calibration · {seasons} · {n_seeds} seeds · "
        rf"bracket tol={tol:g} · longitudinal $\rho^* \approx {rho_star:.3g}$ · {role}"
    )

    build_interval_overlap_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=calibrate_title(fit),
        subtitle=subtitle,
        bullets=_readout_bullets(fit),
        claim=calibrate_claim(fit),
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
