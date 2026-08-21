#!/usr/bin/env python3
"""Track C — OBPM/BPM hero robustness (POST-QC, parallel to PPM canonical).

Runs side-by-side Pass A + sensitivity bar charts for SR-backed perf metrics.
Does **not** overwrite canonical PPM PNGs in pass_a/ root.

Run (repo root):
  python sports/scripts/pass_a_bpm_robustness.py --quick
  python sports/scripts/pass_a_bpm_robustness.py
  python sports/scripts/pass_a_bpm_robustness.py --perf obpm --season-min 2013 --season-max 2021

Outputs: pass_a/sensitivity/ with _obpm_ / _bpm_ tags.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "sports" / "scripts"
PASS_A = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a"
SENS = PASS_A / "sensitivity"
PY = sys.executable


def _run(cmd: list[str]) -> None:
    print("\n===", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _load_ppm_canonical() -> dict | None:
    p = PASS_A / "PASS_A_hero_sensitivity_post_qc.json"
    if not p.is_file():
        return None
    rows = json.loads(p.read_text(encoding="utf-8"))
    for r in rows:
        if (
            r.get("perf_metric", "ppm") == "ppm"
            and r.get("x") == "poolq_loo"
            and r.get("mg") == 10
            and r.get("seasons") == "2011-2021"
            and r.get("n_bins") == 16
            and not r.get("subsample")
        ):
            return r
    return None


def _compare_report(perfs: list[str]) -> Path:
    ppm_ref = _load_ppm_canonical()
    lines = [
        f"# Track C — OBPM/BPM vs PPM canonical ({date.today().isoformat()})",
        "",
        "POST-QC hero (mg=10, min=20, 16 quantile poolq_loo, winsor 0.01–0.99).",
        "Robustness only — PPM canonical PNGs in pass_a/ root unchanged.",
        "",
    ]
    if ppm_ref:
        lines.extend(
            [
                "## PPM canonical reference (2011–2021 poolq_loo)",
                f"- n={ppm_ref['n']:,} drafts={ppm_ref['drafts']:,}",
                f"- peak bin {ppm_ref['peak_bin']} @ {100*ppm_ref['peak_rate']:.2f}%",
                f"- last bin @ {100*ppm_ref['bin_last_rate']:.2f}% · tail Δ={100*ppm_ref['tail_drop']:+.2f}pp",
                f"- β₂={ppm_ref['beta_sq']:+.4f} · decline bins after peak={ppm_ref['decline_bins_after_peak']}",
                "",
            ]
        )
    for perf in perfs:
        jp = PASS_A / f"PASS_A_hero_sensitivity_post_qc_{perf}.json"
        if not jp.is_file():
            lines.append(f"## {perf.upper()} — missing {jp.name}")
            continue
        rows = json.loads(jp.read_text(encoding="utf-8"))
        hit = next(
            (
                r
                for r in rows
                if r.get("x") == "poolq_loo"
                and r.get("mg") == 10
                and r.get("seasons") == "2011-2021"
                and r.get("n_bins") == 16
                and not r.get("subsample")
            ),
            None,
        )
        lines.append(f"## {perf.upper()} (2011–2021 poolq_loo)")
        if not hit:
            lines.append("- No matching spec row in sensitivity JSON.")
            lines.append("")
            continue
        lines.extend(
            [
                f"- n={hit['n']:,} drafts={hit['drafts']:,}",
                f"- peak bin {hit['peak_bin']} @ {100*hit['peak_rate']:.2f}%",
                f"- last bin @ {100*hit['bin_last_rate']:.2f}% · tail Δ={100*hit['tail_drop']:+.2f}pp",
                f"- β₂={hit['beta_sq']:+.4f} · decline bins after peak={hit['decline_bins_after_peak']}",
            ]
        )
        if ppm_ref:
            d_peak = hit["peak_bin"] - ppm_ref["peak_bin"]
            d_tail = hit["tail_drop"] - ppm_ref["tail_drop"]
            d_b2 = hit["beta_sq"] - ppm_ref["beta_sq"]
            lines.append(
                f"- vs PPM: Δpeak_bin={d_peak:+d} · Δtail={100*d_tail:+.2f}pp · Δβ₂={d_b2:+.4f}"
            )
        inv = hit["decline_bins_after_peak"] >= 2
        lines.append(
            f"- Inverted-U tail under POST-QC? **{'YES (≥2 post-peak drops)' if inv else 'NO (flat/rising tail)'}**"
        )
        lines.append("")
    out = SENS / "TRACK_C_bpm_obpm_vs_ppm_report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out.relative_to(REPO)}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Track C OBPM/BPM Pass A robustness.")
    parser.add_argument(
        "--perf",
        action="append",
        dest="perfs",
        choices=("obpm", "bpm"),
        help="Perf metric(s) to run (default: both obpm and bpm).",
    )
    parser.add_argument("--season-min", type=int, default=2011)
    parser.add_argument("--season-max", type=int, default=2021)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Sensitivity: 3 POST-QC specs per perf (faster).",
    )
    parser.add_argument(
        "--sensitivity-only",
        action="store_true",
        help="Skip side-by-side empirical bundle; run sensitivity bar charts only.",
    )
    args = parser.parse_args()
    perfs = args.perfs or ["obpm", "bpm"]
    win = ["--season-min", str(args.season_min), "--season-max", str(args.season_max)]

    for perf in perfs:
        if not args.sensitivity_only:
            _run(
                [
                    PY,
                    str(SCRIPTS / "pass_a_empirical_bundle.py"),
                    *win,
                    "--perf-metric",
                    perf,
                ]
            )
        sens_cmd = [
            PY,
            str(SCRIPTS / "pass_a_hero_sensitivity_plots.py"),
            "--perf-metric",
            perf,
        ]
        if args.quick:
            sens_cmd.append("--quick")
        _run(sens_cmd)

    _compare_report(perfs)
    print("\nTrack C done. Review pass_a/sensitivity/ — canonical PPM untouched.")


if __name__ == "__main__":
    main()
