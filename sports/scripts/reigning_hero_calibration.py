#!/usr/bin/env python3
"""Reigning hero — PD28 calibration rerun (ρ*, γ*, λ*, t*, temperature).

Population lock: 2009–2021 · all-ps · min20 · mg10 · PPM z · winsor 1–99.
(Same filter chain as PD21 campaign; season window extended to reigning hero.)

Run (repo root):
  python sports/scripts/reigning_hero_calibration.py
  python sports/scripts/reigning_hero_calibration.py --only rho mle
  python sports/scripts/reigning_hero_calibration.py --quick   # smoke (2015 only, few seeds)

Outputs:
  ``3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/``
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (  # noqa: E402
    HERO_ROOT,
    PD21_MLE,
    PD21_RHO,
    REIGNING_HERO_CALIBRATION,
    REIGNING_HERO_CALIBRATION_MLE,
    REIGNING_HERO_CALIBRATION_RHO,
    REIGNING_HERO_CALIBRATION_TEMPERATURE,
    ensure_hero_dirs,
)

SEASON_MIN = 2009
SEASON_MAX = 2021
SLUG = "mg10_min20_09_21"
STEM_RHO = f"REIGNING_PD21_rho_hsort_calibrate_{SEASON_MIN}_{SEASON_MAX}_{SLUG}"
STEM_MLE = f"REIGNING_PD21_draft_bernoulli_mle_{SEASON_MIN}_{SEASON_MAX}_{SLUG}"
STEM_TEMP = f"REIGNING_GRANDCHILD_temperature_select_sweep_{SEASON_MIN}_{SEASON_MAX}_{SLUG}"

CAMPAIGN_RHO_FIT = PD21_RHO / "PD21_rho_hsort_calibrate_2011_2021_fit_bracket.json"
CAMPAIGN_MLE_JSON = PD21_MLE / "PD21_draft_bernoulli_mle_2013_2021.json"


def _py(script: str, *args: str) -> None:
    cmd = [sys.executable, str(SCRIPTS / script), *args]
    print(f"\n>>> {' '.join(cmd)}\n", flush=True)
    subprocess.run(cmd, cwd=REPO, check=True)


def run_rho(*, quick: bool, n_seeds: int, n_jobs: int, fresh: bool) -> Path:
    args = [
        "--season-min",
        str(SEASON_MIN),
        "--season-max",
        str(SEASON_MAX),
        "--method",
        "bracket",
        "--out-dir",
        str(REIGNING_HERO_CALIBRATION_RHO),
        "--output-stem",
        STEM_RHO,
        "--n-seeds",
        str(n_seeds),
        "--n-jobs",
        str(n_jobs),
    ]
    if quick:
        args.append("--quick")
    if fresh:
        args.append("--fresh")
    _py("pd21_rho_hsort_calibrate.py", *args)
    return REIGNING_HERO_CALIBRATION_RHO / f"{STEM_RHO}_fit_bracket.json"


def run_mle(*, quick: bool) -> Path:
    args = [
        "--season-min",
        str(SEASON_MIN),
        "--season-max",
        str(SEASON_MAX),
        "--out-dir",
        str(REIGNING_HERO_CALIBRATION_MLE),
        "--output-stem",
        STEM_MLE,
    ]
    if quick:
        args.append("--quick")
    _py("pd21_draft_bernoulli_mle.py", *args)
    return REIGNING_HERO_CALIBRATION_MLE / f"{STEM_MLE}.json"


def _read_rho_star(fit_path: Path) -> float:
    fit = json.loads(fit_path.read_text(encoding="utf-8"))
    lon = fit.get("longitudinal") or {}
    if "rho_star_longitudinal" in lon:
        return float(lon["rho_star_longitudinal"])
    # per-season median fallback
    per = fit.get("per_season") or []
    stars = [float(r["rho_star"]) for r in per if r.get("rho_star") is not None]
    if stars:
        return float(sorted(stars)[len(stars) // 2])
    return 0.0


def run_temperature(*, rho: float, quick: bool) -> Path:
    args = [
        "--season-min",
        str(SEASON_MIN),
        "--season-max",
        str(SEASON_MAX),
        "--rho",
        str(rho),
        "--out-dir",
        str(REIGNING_HERO_CALIBRATION_TEMPERATURE),
        "--output-stem",
        STEM_TEMP,
    ]
    if quick:
        args.append("--quick")
    _py("grandchild_temperature_select_sweep.py", *args)
    return REIGNING_HERO_CALIBRATION_TEMPERATURE / f"{STEM_TEMP}_meta.json"


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_compare_memo(
    *,
    rho_fit: Path | None,
    mle_json: Path | None,
    temp_meta: Path | None,
) -> Path:
    reigning_rho = _load_json(rho_fit) if rho_fit else {}
    reigning_mle = _load_json(mle_json) if mle_json else {}
    campaign_rho = _load_json(CAMPAIGN_RHO_FIT)
    campaign_mle = _load_json(CAMPAIGN_MLE_JSON)

    r_rho = (reigning_rho.get("longitudinal") or {}).get("rho_star_longitudinal")
    c_rho = (campaign_rho.get("longitudinal") or {}).get("rho_star_longitudinal")

    lines = [
        "# Reigning hero calibration vs PD21 campaign",
        "",
        f"**Generated:** {date.today().isoformat()}  ",
        f"**Reigning lock:** {SEASON_MIN}–{SEASON_MAX} · all-ps · min20 · mg10 · PPM z",
        "",
        "## Headline numbers (Alex PD28)",
        "",
        "| Parameter | Reigning 09–21 | Campaign baseline | Notes |",
        "|-----------|----------------|-------------------|-------|",
    ]

    def _cell(v) -> str:
        if v is None:
            return "—"
        if isinstance(v, float):
            return f"{v:.6g}"
        return str(v)

    lines.append(
        f"| **ρ\\*** (H_sort bracket) | {_cell(r_rho)} | {_cell(c_rho)} | "
        f"Campaign: 2011–21 [`pd21_rho/`](../../../../pd21_rho/) |"
    )
    lines.append(
        f"| **γ\\*** | {_cell(reigning_mle.get('gamma_hat'))} | "
        f"{_cell(campaign_mle.get('gamma_hat'))} | Campaign MLE: 2013–21 |"
    )
    lines.append(
        f"| **λ\\*** | {_cell(reigning_mle.get('lambda_hat'))} | "
        f"{_cell(campaign_mle.get('lambda_hat'))} | Bernoulli softmax MLE |"
    )
    lines.append(
        f"| **t\\*** (temperature in score) | {_cell(reigning_mle.get('t_hat'))} | "
        f"{_cell(campaign_mle.get('t_hat'))} | Not Gibbs SELECT t |"
    )
    lines.append(
        f"| **log L** | {_cell(reigning_mle.get('loglik_hat'))} | "
        f"{_cell(campaign_mle.get('loglik_hat'))} | |"
    )
    lines.append(
        f"| **n player-seasons** | {_cell(reigning_mle.get('n_player_seasons'))} | "
        f"{_cell(campaign_mle.get('n_player_seasons'))} | |"
    )

    # temperature summary
    if temp_meta and temp_meta.is_file():
        tmeta = _load_json(temp_meta)
        runs = tmeta.get("runs") or []
        if runs:
            lines.extend(["", "## Gibbs SELECT temperature sweep", ""])
            lines.append("| λ | log10(t) | LOO shape | pool-mean shape |")
            lines.append("|---|----------|-----------|-----------------|")
            for row in runs[:20]:
                curv_loo = (row.get("curvature_loo") or {}).get("shape", "?")
                curv_mean = (row.get("curvature_pool_mean") or {}).get("shape", "?")
                lines.append(
                    f"| {row.get('lambda', '?')} | {row.get('log10_t', '?')} | "
                    f"{curv_loo} | {curv_mean} |"
                )
            if len(runs) > 20:
                lines.append(f"| … | … | *({len(runs)} total runs)* | |")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- ρ: `{rho_fit.relative_to(REPO) if rho_fit else '—'}`",
            f"- MLE: `{mle_json.relative_to(REPO) if mle_json else '—'}`",
            f"- Temperature: `{temp_meta.relative_to(REPO) if temp_meta else '—'}`",
            "",
            "## Read for Alex",
            "",
            "Re-run the **same PD21 calibration chain** on the **09–21 reigning panel**. "
            "ρ* answers ASSIGN (homophily vs empirical H_sort); γ*/λ*/t* answer SCORE on fixed rosters; "
            "temperature sweep confirms inverted-U survives Gibbs SELECT at reigning ρ*.",
            "",
        ]
    )

    out = REIGNING_HERO_CALIBRATION / "CAMPAIGN_COMPARE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def write_manifest(
    *,
    rho_fit: Path | None,
    mle_json: Path | None,
    temp_meta: Path | None,
) -> None:
    manifest = {
        "date": date.today().isoformat(),
        "population": {
            "season_min": SEASON_MIN,
            "season_max": SEASON_MAX,
            "slug": SLUG,
            "panel_rows": "all-ps",
            "filters": "min20 · mg10 · winsor 0.01–0.99 · PPM z",
        },
        "pd28_source": "transcripts/20260828_Paper_Directions_28_otter_ai_transcript.docx",
        "steps": {
            "rho": {
                "stem": STEM_RHO,
                "fit_json": rho_fit.name if rho_fit and rho_fit.is_file() else None,
                "complete": bool(rho_fit and rho_fit.is_file()),
            },
            "mle": {
                "stem": STEM_MLE,
                "json": mle_json.name if mle_json and mle_json.is_file() else None,
                "complete": bool(mle_json and mle_json.is_file()),
            },
            "temperature": {
                "stem": STEM_TEMP,
                "meta_json": temp_meta.name if temp_meta and temp_meta.is_file() else None,
                "complete": bool(temp_meta and temp_meta.is_file()),
            },
        },
        "compare_memo": "CAMPAIGN_COMPARE.md",
    }
    out = REIGNING_HERO_CALIBRATION / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reigning hero PD28 calibration chain.")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=("rho", "mle", "temperature"),
        help="Run subset (default: all three in order).",
    )
    parser.add_argument("--quick", action="store_true", help="Smoke mode (short seasons/seeds).")
    parser.add_argument("--n-seeds", type=int, default=50, help="ρ calibration seeds per eval.")
    parser.add_argument("--n-jobs", type=int, default=8, help="Parallel workers for ρ sims.")
    parser.add_argument("--fresh", action="store_true", help="Ignore ρ JSONL checkpoint.")
    parser.add_argument(
        "--rho",
        type=float,
        default=None,
        help="Override ρ for temperature sweep (default: read from reigning fit).",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    REIGNING_HERO_CALIBRATION.mkdir(parents=True, exist_ok=True)

    keys = args.only or ("rho", "mle", "temperature")
    rho_fit: Path | None = REIGNING_HERO_CALIBRATION_RHO / f"{STEM_RHO}_fit_bracket.json"
    mle_json: Path | None = REIGNING_HERO_CALIBRATION_MLE / f"{STEM_MLE}.json"
    temp_meta: Path | None = REIGNING_HERO_CALIBRATION_TEMPERATURE / f"{STEM_TEMP}_meta.json"

    if "rho" in keys:
        rho_fit = run_rho(
            quick=args.quick,
            n_seeds=4 if args.quick else args.n_seeds,
            n_jobs=args.n_jobs,
            fresh=args.fresh,
        )

    if "mle" in keys:
        mle_json = run_mle(quick=args.quick)

    if "temperature" in keys:
        rho_val = args.rho
        if rho_val is None:
            if not rho_fit.is_file():
                raise SystemExit(
                    f"Missing {rho_fit} — run --only rho first or pass --rho explicitly."
                )
            rho_val = _read_rho_star(rho_fit)
            print(f"Using reigning ρ* = {rho_val:g} for temperature sweep", flush=True)
        temp_meta = run_temperature(rho=float(rho_val), quick=args.quick)

    write_compare_memo(rho_fit=rho_fit, mle_json=mle_json, temp_meta=temp_meta)
    write_manifest(rho_fit=rho_fit, mle_json=mle_json, temp_meta=temp_meta)
    print("\nDone.")


if __name__ == "__main__":
    main()
