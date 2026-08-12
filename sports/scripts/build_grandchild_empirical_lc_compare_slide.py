#!/usr/bin/env python3
"""Build empirical vs Grandchild team L_C comparison AUTO reference slide.

Runs grandchild_empirical_lc_compare.py (unless --slides-only), then writes disposable AUTO deck.

Run (repo root):
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_empirical_lc_compare_slide.py
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_empirical_lc_compare_slide.py --slides-only
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_empirical_lc_compare_slide.py --rho 0.5 --gamma 0.5
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

DIAG_SCRIPT = SCRIPTS / "grandchild_empirical_lc_compare.py"
FIG = GRANDCHILD_ASSIGN / "GRANDCHILD_empirical_lc_compare_2011_2021.png"
META = GRANDCHILD_ASSIGN / "GRANDCHILD_empirical_lc_compare_2011_2021_meta.json"
OUT_PPTX = SLIDES_AUTO / "CHAR_grandchild_empirical_lc_compare_AUTO.pptx"

CLAIM = (
    "Claim (PD17 / LG): Team smooth L_C on real rosters vs LG sim — "
    r"same $\sigma(\gamma(\hat{A}_j - \theta))$ formula; compare distribution shape before SCORE."
)


def _regenerate(*, rho: float, gamma: float | None) -> None:
    cmd = [sys.executable, str(DIAG_SCRIPT), "--rho", str(rho)]
    if gamma is not None:
        cmd.extend(["--gamma", str(gamma)])
    print("Running empirical vs LG L_C compare ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    sim = meta.get("sim", {})
    emp_lc = emp.get("L_C", {})
    sim_lc = sim.get("L_C", {})
    theta = meta.get("theta")
    gamma = meta.get("gamma")
    kn = meta.get("theta_K_over_N", {})
    rho = sim.get("rho", meta.get("rho", 0.5))
    seasons = meta.get("seasons", "2011-2021")

    bullets = [
        r"Team L_C = mean_{j} \sigma(\gamma(\hat{A}_{j} - \theta)) — team-smooth congestion.",
        r"Left panel: empirical NCAA (real rosters). Right: LG ASSIGN sim.",
        rf"Panel: MBB {seasons} · PPM z · min 20 min · poolq winsor 0.01–0.99.",
    ]
    if theta is not None and kn:
        bullets.append(
            rf"Shared \theta = F^{{-1}}_{{\hat{{A}}}}(1-K/N) = {theta:.3f} z "
            rf"(K/N={kn.get('K_over_N', 0):.4f})."
        )
    if gamma is not None:
        bullets.append(rf"\gamma = {gamma:g} (HAND17 slide-4 default; 539 placeholder).")
    if emp_lc and sim_lc:
        bullets.append(
            rf"Empirical: mean L_C={emp_lc.get('mean', 0):.3f}, "
            rf"sd={emp_lc.get('std', 0):.3f} ({emp_lc.get('n', 0):,} team-seasons)."
        )
        bullets.append(
            rf"LG (\rho={rho:g}): mean L_C={sim_lc.get('mean', 0):.3f}, "
            rf"sd={sim_lc.get('std', 0):.3f} ({sim_lc.get('n', 0):,} team-seasons)."
        )
    bullets.extend(
        [
            r"Sim: one LG league per season (J = N/15), stacked team-seasons.",
            r"ASSIGN shapes rosters; L_C is score-side input — computed after assign.",
            r"Overlay PNG: grandchild_assign/GRANDCHILD_empirical_lc_overlay_2011_2021.png",
            r"Normalized side-by-side: grandchild_assign/GRANDCHILD_empirical_lc_compare_normalized_2011_2021.png",
        ]
    )
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--rho", type=float, default=0.5)
    parser.add_argument("--gamma", type=float, default=None)
    args = parser.parse_args()

    ensure_hero_dirs()
    if not args.slides_only:
        _regenerate(rho=float(args.rho), gamma=args.gamma)

    meta = load_meta(META)
    seasons = meta.get("seasons", "2011-2021")
    theta = meta.get("theta")
    gamma = meta.get("gamma", 0.5)
    rho = meta.get("sim", {}).get("rho", args.rho)
    kn = meta.get("theta_K_over_N", {})
    k_over_n = kn.get("K_over_N")

    subtitle_parts = [
        rf"MBB {seasons} · team smooth L_C · LG \rho={rho:g}",
        rf"\gamma={gamma:g}",
    ]
    if theta is not None and k_over_n is not None:
        subtitle_parts.append(rf"\theta={theta:.3f} z (K/N={k_over_n:.4f})")

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT_PPTX,
        title=r"Empirical vs LG — team $L_C$ distribution",
        subtitle=" · ".join(subtitle_parts),
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )


if __name__ == "__main__":
    main()
