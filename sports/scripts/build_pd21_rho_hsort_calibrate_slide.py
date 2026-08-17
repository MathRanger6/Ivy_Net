#!/usr/bin/env python3
"""Build PD21 ρ → H_sort calibration AUTO slide (Alex ASSIGN calibration).

Run (repo root):
  python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py --slides-only
  python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py

Output:
  slides/auto/CHAR_PD21_rho_hsort_calibrate_AUTO.pptx

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

from hero_gallery_paths import AUTO_PD21_RHO_DECK, PD21_RHO, ensure_hero_dirs
from h_sort_readout import h_sort_definition_bullet, h_sort_note_bullet
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

CALIBRATE_SCRIPT = SCRIPTS / "pd21_rho_hsort_calibrate.py"
FIG = PD21_RHO / "PD21_rho_hsort_calibrate_2011_2021_bracket.png"
FIT = PD21_RHO / "PD21_rho_hsort_calibrate_2011_2021_fit_bracket.json"
OUT_PPTX = AUTO_PD21_RHO_DECK

CLAIM = (
    r"Claim (Alex): Near-zero ASSIGN homophily $\rho$ matches empirical "
    r"$H_{\mathrm{sort}}$ on the hero panel — legacy $\rho=0.5$ overshoots "
    r"simulated sorting by $\sim 0.10$."
)


def _refresh_plot() -> None:
    cmd = [
        sys.executable,
        str(CALIBRATE_SCRIPT),
        "--plot-only",
        "--plot-xmax",
        "0.1",
    ]
    print("Refreshing bracket PNG (plot-only, x-axis 0–0.1) ...")
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
        import numpy as np
        h_emp = float(np.mean([float(t["h_sort_empirical"]) for t in fit["empirical_targets"]]))
    h_sim_s = f"{float(h_sim):.3f}" if h_sim is not None else "?"
    h_emp_s = f"{float(h_emp):.3f}" if h_emp is not None else "?"

    bullets = [
        r"Alex (Aug 2026): calibrate ASSIGN $\rho$ so LG simulated $H_{\mathrm{sort}}$ "
        r"matches empirical NCAA; formal $\rho$ MLE parked.",
        r"Panel: 2011–2021 hero MBB · min 20 min · empirical roster caps · PPM z within season.",
        f"Search: bracket + bisect (tol={tol:g}), {n_seeds} seeds/arm; "
        r"$H_{\mathrm{sort}}^{\mathrm{sim}}$ monotone in $\rho$.",
        h_sort_definition_bullet(),
        f"Longitudinal $\\rho^* \\approx {rho_star_s}$; "
        + f"mean $H_{{\\mathrm{{sort}}}}^{{\\mathrm{{sim}}}}$ at $\\rho^*$ = {h_sim_s}; "
        + f"mean $H_{{\\mathrm{{sort}}}}^{{\\mathrm{{emp}}}}$ = {h_emp_s}.",
        f"Per-season: {n_zero}/{len(per)} seasons at $\\rho^*=0$; "
        + (f"nonzero — {nonzero_str}" if nonzero_str else r"all at $\rho^*=0$."),
        f"Legacy reference $\\rho={ref_rho:g}$: mean $|error| \\approx {err_ref_s}$ "
        f"vs $\\approx {err_star_s}$ at $\\rho^*$.",
        h_sort_note_bullet(),
        r"Figure: small multiples — blue sim curve, red empirical line, green $\rho^*$ "
        r"(x-axis zoomed to evaluated bracket; reference $\rho$ excluded from axis).",
    ]
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD21 ρ H_sort calibration AUTO slide.")
    parser.add_argument(
        "--slides-only",
        action="store_true",
        help="Use existing PNG + fit JSON (no plot refresh)",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    if not args.slides_only:
        _refresh_plot()

    fit = load_meta(FIT)
    if not fit:
        raise SystemExit(f"Missing fit JSON: {FIT}")

    n_seeds = int(fit.get("n_seeds", 50))
    seasons = fit.get("seasons", "2011-2021")
    tol = fit.get("bracket", {}).get("tol", 0.001)
    rho_star = float(fit.get("longitudinal", {}).get("rho_star_longitudinal", 0.0))

    subtitle = (
        rf"PD21 · LG ASSIGN calibration · {seasons} · {n_seeds} seeds · "
        rf"bracket tol={tol:g} · longitudinal $\rho^* \approx {rho_star:.3g}$"
    )

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT_PPTX,
        title=r"PD21 — Calibrate homophily $\rho$ to empirical sorting index $H_{\mathrm{sort}}$",
        subtitle=subtitle,
        bullets=_readout_bullets(fit),
        claim=CLAIM,
    )


if __name__ == "__main__":
    main()
