#!/usr/bin/env python3
"""Reigning hero star sweep — EW bin count × season window (20 runs).

Fixed lock (slide 12 family): poolq_loo · ever · last-ps · ALLT · equal_width ·
min20 · mg10 · winsor 0.01–0.99.

Varied:
  n_bins ∈ {8, 10, 12, 20, 24}
  season_window ∈ {09_21, 11_21, 13_21, 09_19}

Output tags: ``star_ew{N}_{season_window}`` → ``reigning_hero/hero_star_sweeps/``

Run (repo root):
  python sports/scripts/reigning_hero_star_sweep.py --dry-run
  python sports/scripts/reigning_hero_star_sweep.py
  python sports/scripts/reigning_hero_star_sweep.py --force
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import date, datetime
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "sports/scripts"
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import REIGNING_HERO_STAR_SWEEPS, ensure_hero_dirs  # noqa: E402
from hero_permutation_sweep import (  # noqa: E402
    BUNDLE,
    HeroPermSpec,
    _shape_summary,
)
from pd20_22_campaign_window import (  # noqa: E402
    FULL_PANEL_SEASON_MAX,
    FULL_PANEL_SEASON_MIN,
    PRIMARY_SEASON_MAX,
    PRIMARY_SEASON_MIN,
)
from plot_provenance import roster_x_slug, season_slug  # noqa: E402

STAR_OUT = REIGNING_HERO_STAR_SWEEPS
MANIFEST = STAR_OUT / "manifest.json"

SEASON_WINDOWS: dict[str, tuple[int, int]] = {
    "09_21": (2009, 2021),
    "11_21": (FULL_PANEL_SEASON_MIN, FULL_PANEL_SEASON_MAX),
    "13_21": (PRIMARY_SEASON_MIN, PRIMARY_SEASON_MAX),
    "09_19": (2009, 2019),
}

N_BINS_GRID = (8, 10, 12, 20, 24)

REIGNING_LOCK = {
    "roster_x": "poolq_loo",
    "y_draft_mode": "ever",
    "panel_rows": "last-ps",
    "poolq_binning": "equal_width",
    "n_bins": 16,
    "season_window": "09_21",
    "dft": False,
}


def iter_star_specs() -> list[HeroPermSpec]:
    specs: list[HeroPermSpec] = []
    for n_bins, win in product(N_BINS_GRID, SEASON_WINDOWS):
        smin, smax = SEASON_WINDOWS[win]
        tag = f"star_ew{n_bins}_{win}"
        label = (
            f"Star EW{n_bins} · {win.replace('_', '–')} · last-ps · LOO · ever · ALLT"
        )
        specs.append(
            HeroPermSpec(
                y_draft_mode="ever",
                panel_rows="last-ps",
                roster_x="poolq_loo",
                n_bins=int(n_bins),
                poolq_binning="equal_width",
                dft=False,
                season_min=smin,
                season_max=smax,
                season_window=win,
                output_tag=tag,
                label=label,
            )
        )
    return specs


def _find_hero_png(tag: str, season_slug_str: str) -> Path | None:
    matches = sorted(STAR_OUT.glob(f"HERO_*_{season_slug_str}_{tag}.png"))
    if not matches:
        matches = sorted(STAR_OUT.glob(f"HERO_*{season_slug_str}*{tag}.png"))
    return matches[0] if matches else None


def _find_roster_csv(spec: HeroPermSpec, tag: str, slug: str) -> Path | None:
    xslug = roster_x_slug(spec.roster_x)
    if xslug == "poolq":
        patterns = [
            f"PASS_A_binned_draft_rate_poolq_poolq_*_{slug}_{tag}.csv",
            f"PASS_A_binned_draft_rate_poolq_poolq_*{slug}*{tag}.csv",
        ]
    else:
        patterns = [
            f"PASS_A_binned_draft_rate_{xslug}_*_{slug}_{tag}.csv",
            f"PASS_A_binned_draft_rate_{xslug}_*{slug}*{tag}.csv",
        ]
    for pat in patterns:
        matches = [p for p in sorted(STAR_OUT.glob(pat)) if "ability" not in p.name]
        if matches:
            return matches[0]
    fallback = [
        p
        for p in sorted(STAR_OUT.glob(f"PASS_A_binned_draft_rate_*_{slug}_{tag}.csv"))
        if "ability" not in p.name
        and (xslug != "poolq" or "poolq_poolq" in p.name)
        and (xslug != "poolq_loo" or "poolq_loo" in p.name)
    ]
    return fallback[0] if fallback else None


def _find_lpm_txt(tag: str, slug: str) -> Path | None:
    matches = sorted(STAR_OUT.glob(f"PASS_A_lpm_hero_coefficients_*_{slug}_{tag}.txt"))
    if not matches:
        matches = sorted(STAR_OUT.glob(f"PASS_A_lpm_hero_coefficients_*{slug}*{tag}.txt"))
    return matches[0] if matches else None


def _manifest_entry(
    spec: HeroPermSpec,
    *,
    png: Path | None,
    csv_path: Path | None,
    prov: Path | None,
) -> dict:
    slug = season_slug(spec.season_min, spec.season_max)
    lpm_path = _find_lpm_txt(spec.output_tag, slug)
    return {
        "output_tag": spec.output_tag,
        "season_window": spec.season_window,
        "season_min": spec.season_min,
        "season_max": spec.season_max,
        "n_bins": spec.n_bins,
        "label": spec.label,
        "spec": asdict(spec),
        "command": spec.command(),
        "command_one_line": spec.command_one_line(),
        "hero_png": str(png.relative_to(REPO)) if png else None,
        "roster_csv": str(csv_path.relative_to(REPO)) if csv_path else None,
        "roster_csv_xslug": roster_x_slug(spec.roster_x),
        "provenance_json": str(prov.relative_to(REPO)) if prov else None,
        "shape": _shape_summary(csv_path, lpm_path=lpm_path),
    }


def _run_one(spec: HeroPermSpec, *, force: bool) -> dict:
    slug = season_slug(spec.season_min, spec.season_max)
    png = _find_hero_png(spec.output_tag, slug)
    if png and not force:
        print(f"SKIP (exists) · {spec.season_window} · {spec.output_tag} · {png.name}", flush=True)
    else:
        cmd = [
            sys.executable,
            str(BUNDLE),
            "--season-min",
            str(spec.season_min),
            "--season-max",
            str(spec.season_max),
            "--y-draft-mode",
            spec.y_draft_mode,
            "--panel-rows",
            spec.panel_rows,
            "--roster-x",
            spec.roster_x,
            "--n-bins",
            str(spec.n_bins),
            "--poolq-binning",
            spec.poolq_binning,
            "--output-tag",
            spec.output_tag,
            "--output-root",
            str(STAR_OUT.relative_to(REPO)),
        ]
        print(f"RUN · {spec.season_window} · ew{spec.n_bins} · {spec.output_tag}", flush=True)
        subprocess.run(cmd, cwd=REPO, check=True)
        png = _find_hero_png(spec.output_tag, slug)

    csv_path = _find_roster_csv(spec, spec.output_tag, slug)
    prov_glob = list(STAR_OUT.glob(f"HERO_*_{slug}_{spec.output_tag}_provenance.json"))
    if not prov_glob:
        prov_glob = list(STAR_OUT.glob(f"HERO_*{slug}*{spec.output_tag}_provenance.json"))
    prov = prov_glob[0] if prov_glob else None
    return _manifest_entry(spec, png=png, csv_path=csv_path, prov=prov)


def _write_manifest(manifest: dict) -> None:
    runs = manifest.get("runs") or []
    n_runs = len(runs)
    n_planned = int(manifest.get("n_planned", n_runs))
    manifest["n_planned"] = n_planned
    manifest["n_runs"] = n_runs
    manifest["complete"] = n_runs >= n_planned
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reigning hero star sweep (20 EW × season runs).")
    parser.add_argument("--dry-run", action="store_true", help="Print specs only; do not run.")
    parser.add_argument("--force", action="store_true", help="Re-run even if PNG exists.")
    args = parser.parse_args()

    ensure_hero_dirs()
    STAR_OUT.mkdir(parents=True, exist_ok=True)
    specs = iter_star_specs()

    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "sweep": "reigning_hero_star",
        "reigning_lock": REIGNING_LOCK,
        "n_bins_grid": list(N_BINS_GRID),
        "season_windows": list(SEASON_WINDOWS.keys()),
        "n_planned": len(specs),
        "n_runs": 0,
        "complete": False,
        "runs": [],
    }

    print(
        f"Reigning hero star sweep · planned={len(specs)} · out={STAR_OUT.relative_to(REPO)}",
        flush=True,
    )
    for i, spec in enumerate(specs, start=1):
        print(f"\n--- [{i}/{len(specs)}] {spec.output_tag} ---", flush=True)
        print(spec.command(), flush=True)
        if args.dry_run:
            continue
        entry = _run_one(spec, force=bool(args.force))
        entry["run_index"] = i
        manifest["runs"].append(entry)
        _write_manifest(manifest)

    if args.dry_run:
        manifest["runs"] = [
            {
                "run_index": i,
                "output_tag": s.output_tag,
                "season_window": s.season_window,
                "n_bins": s.n_bins,
                "label": s.label,
                "spec": asdict(s),
                "command": s.command(),
            }
            for i, s in enumerate(specs, start=1)
        ]
        _write_manifest(manifest)
        print(f"\nDry-run manifest → {MANIFEST.relative_to(REPO)}", flush=True)
    else:
        print(
            f"\nDone · {manifest['n_runs']}/{manifest['n_planned']} runs · "
            f"complete={manifest['complete']} · manifest → {MANIFEST.relative_to(REPO)}",
            flush=True,
        )


if __name__ == "__main__":
    main()
