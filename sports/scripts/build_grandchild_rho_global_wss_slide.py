#!/usr/bin/env python3
"""Build LG ρ → global WSS reference slide (Alex primary ASSIGN readout).

Runs 541 ρ sweep (unless --slides-only), then writes disposable AUTO deck.
Companion (scale-free): build_grandchild_rho_assortativity_slide.py (H_sort).

Run (repo root):
  python sports/scripts/build_grandchild_rho_global_wss_slide.py
  python sports/scripts/build_grandchild_rho_global_wss_slide.py --slides-only
  python sports/scripts/build_grandchild_rho_global_wss_slide.py --quick
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
from global_wss_readout import (
    global_wss_definition_bullet,
    global_wss_h_sort_link_bullet,
    global_wss_note_bullet,
)
from h_sort_readout import h_sort_note_bullet
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

SWEEP_SCRIPT = SCRIPTS / "541_grandchild_rho_sweep.py"
FIG = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_vs_global_wss.png"
META = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_sweep_meta.json"
CSV = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_sweep_summary.csv"
OUT_PPTX = SLIDES_AUTO / "CHAR_grandchild_rho_global_wss_AUTO.pptx"

CLAIM = (
    "Claim (Alex): global\\_wss is the within-team SS numerator on the assign partition — "
    r"$\rho \uparrow$ lowers global\_wss on the same 2015 LG league ($H_{sort}$ is the scale-free companion)."
)


def _regenerate(*, quick: bool) -> None:
    cmd = [sys.executable, str(SWEEP_SCRIPT)]
    if quick:
        cmd.append("--quick")
    print("Running LG ρ sweep ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    import pandas as pd

    bullets = [
        r"\rho = LG ASSIGN homophily knob in \exp(-\rho|\hat{A}_i - \mu_j|).",
        r"Each point: mean \pm 1 SD of global\_wss over stochastic LG realizations.",
        global_wss_definition_bullet(),
        global_wss_h_sort_link_bullet(),
    ]
    if CSV.is_file():
        summary = pd.read_csv(CSV)
        if len(summary) >= 2 and "global_wss_mean" in summary.columns:
            lo = summary.iloc[0]
            hi = summary.iloc[-1]
            bullets.append(
                rf"\rho={lo['rho']:g}: global\_wss \approx {lo['global_wss_mean']:.0f} "
                rf"\to \rho={hi['rho']:g}: global\_wss \approx {hi['global_wss_mean']:.0f}."
            )
    n_rep = meta.get("n_realizations")
    n_teams = meta.get("n_teams")
    season = meta.get("season", 2015)
    if n_rep and n_teams:
        bullets.append(
            rf"{season} empirical PPM z · J={n_teams} · C=15 · {n_rep} reps × "
            rf"{len(meta.get('rho_values', []))} \rho arms."
        )
    bullets.append(global_wss_note_bullet())
    bullets.append(
        r"Companion slide: $H_{sort} = 1 - \mathrm{global\_wss}/\mathrm{SS}_{total}$ "
        r"(scale-free assortativity on the same sweep)."
    )
    bullets.append(h_sort_note_bullet())
    return bullets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides-only", action="store_true")
    parser.add_argument("--quick", action="store_true", help="Smoke sweep (3 ρ arms, 8 reps)")
    args = parser.parse_args()

    ensure_hero_dirs()
    if not args.slides_only:
        _regenerate(quick=args.quick)

    meta = load_meta(META)
    season = meta.get("season", 2015)
    n_teams = meta.get("n_teams", 402)
    n_rep = meta.get("n_realizations", "?")
    rho_band = meta.get("rho_calibration_band", [0, 1])

    subtitle = (
        rf"LG ASSIGN · {season} PPM z · J={n_teams}, C=15 · "
        rf"\rho \in [{rho_band[0]:g}, {rho_band[1]:g}] · {n_rep} reps/arm"
    )

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT_PPTX,
        title=r"LG ASSIGN — global\_wss vs $\rho$",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {OUT_PPTX}")


if __name__ == "__main__":
    main()
