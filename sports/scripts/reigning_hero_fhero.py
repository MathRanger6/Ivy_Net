#!/usr/bin/env python3
"""Reigning hero (slide 12) — paired F-HERO on the same plot population.

Lock aperture (matches basic_data_plots + HERO):
  2009–2021 · last-ps · ever · ALLT · min20 · mg10 · winsor 1–99 · PPM z

F-HERO x-axis is T̂_j (team mean, incl. self) — not poolq_LOO. Pair with reigning HERO.

Outputs:
  ``3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/fhero/``

Run (repo root):
  python sports/scripts/reigning_hero_fhero.py
  python sports/scripts/reigning_hero_fhero.py --only ecdf single overlay
  python sports/scripts/reigning_hero_fhero.py --with-dft-overlay
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "sports/scripts"
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import REIGNING_HERO_FHERO, ensure_hero_dirs  # noqa: E402

OUT = REIGNING_HERO_FHERO
MANIFEST = OUT / "manifest.json"

SEASON_MIN = 2009
SEASON_MAX = 2021
COMMON = [
    "--season-min",
    str(SEASON_MIN),
    "--season-max",
    str(SEASON_MAX),
    "--panel-rows",
    "last-ps",
    "--y-draft-mode",
    "ever",
    "--min-minutes",
    "20",
    "--perf-metric",
    "ppm",
]
COMMON_MG10_ECDF = [*COMMON, "--min-team-games", "10"]
COMMON_MG10_CCT = [*COMMON, "--min-team-season-games", "10"]
COMMON_MG10_OVERLAY = [*COMMON, "--min-team-games", "10"]

REIGNING_LOCK = {
    "output_tag": "perm_loo_ever_lastps_ew16",
    "season_window": "09_21",
    "panel_rows": "last-ps",
    "y_draft_mode": "ever",
    "population": "ALLT",
    "filters": "min20 · mg10 · winsor 0.01–0.99 · PPM z",
    "hero_axis": "poolq_loo (EW16)",
    "hero_lpm_beta_sq_09_21": 0.00172,
    "fhero_axis": "T_j_hat (pw4p7 piecewise)",
    "fhero_ai_band": "top 7%",
}


def _out_flag() -> list[str]:
    return ["--out-dir", str(OUT.relative_to(REPO))]


def _run(cmd: list[str], *, label: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=REPO, check=True)


def run_ecdf() -> None:
    _run(
        [
            sys.executable,
            str(SCRIPTS / "bdp_ai_draft_mass_ecdf.py"),
            *COMMON_MG10_ECDF,
            *_out_flag(),
        ],
        label="ECDF — Â draft-mass (band picking)",
    )


def run_single_band() -> None:
    _run(
        [
            sys.executable,
            str(SCRIPTS / "pass_a_congestion_conditional.py"),
            "--plot",
            "fixed_ai_tj_knbins",
            "--p2b-single",
            *COMMON_MG10_CCT,
            "--ai-top-pct",
            "7",
            "--tj-n-low",
            "4",
            "--tj-n-high",
            "7",
            *_out_flag(),
        ],
        label="F-HERO single band (top 7% Â · pw4p7)",
    )


def run_overlay(*, dft: bool = False) -> None:
    cmd = [
        sys.executable,
        str(SCRIPTS / "cct_p2b_ai_band_overlay.py"),
        *COMMON_MG10_OVERLAY,
        "--bands",
        "0:7,7:15,15:25,25:40",
        "--hero-top",
        "0:7",
        "--tj-edge-mode",
        "shared_panel",
        "--tj-n-low",
        "4",
        "--tj-n-high",
        "7",
        *_out_flag(),
    ]
    if dft:
        cmd.append("--dft")
    _run(
        cmd,
        label="P2b overlay (+DFT panel)" if dft else "P2b overlay (ALLT · Slide-10 bands)",
    )


def _glob_one(pattern: str) -> Path | None:
    matches = sorted(OUT.glob(pattern))
    return matches[0] if matches else None


def _read_json(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _fhero_readout(meta: dict) -> dict:
    knee = meta.get("knee_summary") or meta.get("knee") or {}
    prov = meta.get("provenance") or {}
    return {
        "band_n": meta.get("band_n"),
        "total_drafts": meta.get("total_drafts"),
        "ai_top_pct": meta.get("ai_top_pct"),
        "alex_downturn_visible": knee.get("alex_downturn_visible"),
        "plateau_mean_draft_rate": knee.get("plateau_mean_draft_rate"),
        "tail_mean_draft_rate": knee.get("tail_mean_draft_rate"),
        "panel_rows": prov.get("panel_rows") or meta.get("provenance", {}).get("panel_rows"),
        "footer": meta.get("footer"),
    }


def _overlay_readout(meta: dict) -> dict:
    hero_band = next(
        (b for b in (meta.get("bands") or []) if b.get("top_lo") == 0.0 and b.get("top_hi") == 7.0),
        {},
    )
    knee = hero_band.get("knee") or {}
    return {
        "dft": meta.get("dft"),
        "hero_band_n": hero_band.get("band_n"),
        "hero_band_drafts": hero_band.get("total_drafts"),
        "alex_downturn_visible": knee.get("alex_downturn_visible"),
        "knee_tj": (hero_band.get("knee_peak") or {}).get("knee_tj"),
        "knee_rate": (hero_band.get("knee_peak") or {}).get("knee_rate"),
    }


def _build_manifest(*, with_dft: bool) -> dict:
    single_json = _glob_one("FHERO_pw4p7_allt_min20_mg10_top7_ppm_*_last_ps.json")
    overlay_allt = _glob_one("FHERO_pw4p7_overlay_lines_sharetj_allt_min20_mg10_ppm_*_last_ps.json")
    overlay_dft = _glob_one("FHERO_pw4p7_overlay_lines_sharetj_dft_min20_mg10_ppm_*_last_ps.json")
    ecdf_json = _glob_one("BDP_Ai_draft_mass_ecdf_mg10_min20_*_allt_ppm_last_ps.json")

    single_meta = _read_json(single_json)
    overlay_meta = _read_json(overlay_allt)

    artifacts = [
        {
            "key": "ecdf",
            "role": "Â draft-mass ECDF (overlay band reference)",
            "json": ecdf_json.name if ecdf_json else None,
            "png": _glob_one("BDP_Ai_draft_mass_ecdf_mg10_min20_*_allt_ppm_last_ps.png"),
        },
        {
            "key": "single",
            "role": "F-HERO knee (top 7% Â · pw4p7 T̂_j)",
            "json": single_json.name if single_json else None,
            "png": _glob_one("FHERO_pw4p7_allt_min20_mg10_top7_ppm_*_last_ps.png"),
            "readout": _fhero_readout(single_meta),
        },
        {
            "key": "overlay",
            "role": "P2b multi-band overlay (Slide 10 bands · ALLT)",
            "json": overlay_allt.name if overlay_allt else None,
            "png": _glob_one("FHERO_pw4p7_overlay_lines_sharetj_allt_min20_mg10_ppm_*_last_ps.png"),
            "readout": _overlay_readout(overlay_meta),
        },
    ]
    if with_dft and overlay_dft:
        artifacts.append(
            {
                "key": "overlay_dft",
                "role": "P2b overlay (+DFT panel · sensitivity)",
                "json": overlay_dft.name,
                "png": _glob_one("FHERO_pw4p7_overlay_lines_sharetj_dft_min20_mg10_ppm_*_last_ps.png"),
                "readout": _overlay_readout(_read_json(overlay_dft)),
            }
        )

    for a in artifacts:
        png = a.get("png")
        if isinstance(png, Path):
            a["png"] = png.name if png else None
            a["png_exists"] = bool(png and png.is_file())

    pairing = {
        "hero": "Flat LOO elite on poolq_LOO (β₂ ≈ +0.00172) — reigning HERO EW16.",
        "fhero": (
            "Concave/downturn on T̂_j within top-7% Â band — separate congestion axis; "
            "same last-ps · 09–21 · min20 · mg10 aperture."
        ),
        "alex_downturn_visible": (single_meta.get("knee_summary") or single_meta.get("knee") or {}).get(
            "alex_downturn_visible"
        ),
    }

    return {
        "created": datetime.now().isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "deck": "reigning_hero_fhero",
        "reigning_lock": REIGNING_LOCK,
        "population": {
            "seasons": f"{SEASON_MIN}–{SEASON_MAX}",
            "panel_rows": "last-ps",
            "y_draft_mode": "ever",
            "population_default": "ALLT",
            "min_minutes": 20,
            "min_team_games": 10,
            "winsor": [0.01, 0.99],
            "perf_metric": "ppm",
        },
        "pairing_note": pairing,
        "artifacts": artifacts,
        "commands": {
            "full": "python sports/scripts/reigning_hero_fhero.py",
            "ecdf": "python sports/scripts/reigning_hero_fhero.py --only ecdf",
            "single": "python sports/scripts/reigning_hero_fhero.py --only single",
            "overlay": "python sports/scripts/reigning_hero_fhero.py --only overlay",
        },
    }


PLOT_FNS = {
    "ecdf": run_ecdf,
    "single": run_single_band,
    "overlay": lambda: run_overlay(dft=False),
    "overlay_dft": lambda: run_overlay(dft=True),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Reigning hero paired F-HERO (slide 12 population).")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=tuple(PLOT_FNS.keys()),
        help="Run subset (default: ecdf + single + overlay).",
    )
    parser.add_argument(
        "--with-dft-overlay",
        action="store_true",
        help="Also run +DFT overlay (sensitivity; not reigning default).",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    OUT.mkdir(parents=True, exist_ok=True)

    default_keys = ["ecdf", "single", "overlay"]
    if args.with_dft_overlay:
        default_keys.append("overlay_dft")
    keys = args.only or default_keys

    print(f"Reigning hero F-HERO · {SEASON_MIN}–{SEASON_MAX} · last-ps · out={OUT.relative_to(REPO)}")
    for key in keys:
        PLOT_FNS[key]()

    manifest = _build_manifest(with_dft=args.with_dft_overlay or "overlay_dft" in keys)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {MANIFEST.relative_to(REPO)}", flush=True)

    readout = manifest.get("pairing_note") or {}
    downturn = readout.get("alex_downturn_visible")
    print(
        f"Pairing: HERO flat LOO · F-HERO alex_downturn_visible={downturn}",
        flush=True,
    )
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
