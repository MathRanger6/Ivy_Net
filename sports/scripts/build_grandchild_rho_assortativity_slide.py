#!/usr/bin/env python3
"""Build Grandchild ρ → assortativity reference slide (Alex ASSIGN validation).

Runs 541 ρ sweep (unless --slides-only), then writes disposable AUTO deck.

Run (repo root):
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_rho_assortativity_slide.py
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_rho_assortativity_slide.py --slides-only
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_rho_assortativity_slide.py --quick
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
from h_sort_readout import h_sort_definition_bullet, h_sort_note_bullet
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

SWEEP_SCRIPT = SCRIPTS / "541_grandchild_rho_sweep.py"
FIG = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_vs_assortativity.png"
META = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_sweep_meta.json"
CSV = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_sweep_summary.csv"
OUT_PPTX = SLIDES_AUTO / "CHAR_grandchild_rho_assortativity_AUTO.pptx"

CLAIM = (
    "Claim (Alex): Higher ASSIGN homophily \\rho should raise realized assortativity — "
    r"Grandchild one-shot league on 2015 PPM z shows monotonic H_{sort}(\rho)."
)


def _regenerate(*, quick: bool) -> None:
    cmd = [sys.executable, str(SWEEP_SCRIPT)]
    if quick:
        cmd.append("--quick")
    print("Running Grandchild ρ sweep ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _readout_bullets(meta: dict) -> list[str]:
    import pandas as pd

    bullets = [
        r"\rho = Grandchild ASSIGN homophily knob in \exp(-\rho|\hat{A}_i - \mu_j|).",
        r"Each point: mean \pm 1 SD of H_{sort} over stochastic Grandchild realizations.",
        h_sort_definition_bullet(),
        r"H_{sort} = realized assortativity on the assigned partition (0 none, 1 full).",
    ]
    if CSV.is_file():
        summary = pd.read_csv(CSV)
        if len(summary) >= 2:
            lo = summary.iloc[0]
            hi = summary.iloc[-1]
            bullets.append(
                rf"\rho={lo['rho']:g}: H_{{sort}} \approx {lo['H_mean']:.3f} "
                rf"\to \rho={hi['rho']:g}: H_{{sort}} \approx {hi['H_mean']:.3f}."
            )
    n_rep = meta.get("n_realizations")
    n_teams = meta.get("n_teams")
    season = meta.get("season", 2015)
    if n_rep and n_teams:
        bullets.append(
            rf"2015 empirical PPM z · J={n_teams} · C=15 · {n_rep} reps × "
            rf"{len(meta.get('rho_values', []))} \rho arms."
        )
    bullets.append(
        r"VECTOR lock: \rho is generative (ASSIGN); H_{sort} is measured sorting — not the same object."
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
        rf"Grandchild ASSIGN · {season} PPM z · J={n_teams}, C=15 · "
        rf"\rho \in [{rho_band[0]:g}, {rho_band[1]:g}] · {n_rep} reps/arm"
    )

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT_PPTX,
        title=r"Homophily $\rho$ vs realized assortativity $H_{sort}$ (Grandchild sim)",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )


if __name__ == "__main__":
    main()
