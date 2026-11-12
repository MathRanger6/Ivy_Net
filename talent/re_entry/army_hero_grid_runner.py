#!/usr/bin/env python3
"""Batch HERO histograms: B1/B2/B3 × fwd/bwd × z/raw × EW/Q bins × full/boe.

Run from 520 workspace root after Cell 11 (with Phase 2 z columns on feather):

  python talent/re_entry/army_hero_grid_runner.py --quick
  python talent/re_entry/army_hero_grid_runner.py --dry-run
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import army_gallery_paths  # noqa: F401
from army_gallery_paths import ensure_army_output_dirs, resolve_feather
from army_hero_slide_plot import build_hero_panel, load_feather_officers
from army_hero_axes import Axis, Band, Direction, Scale

DEFAULT_N_BINS = (8, 12, 16)
DEFAULT_BIN_METHODS = ("equal_width", "quantile")
DEFAULT_AXES: tuple[Axis, ...] = ("b1", "b2", "b3")
DEFAULT_DIRECTIONS: tuple[Direction, ...] = ("fwd", "bwd")
DEFAULT_SCALES: tuple[Scale, ...] = ("z",)
DEFAULT_BANDS: tuple[Band, ...] = ("full", "boe")

QUICK_GRID = (
    dict(axis="b2", direction="fwd", scale="z", n_bins=8, bin_method="equal_width", band="full"),
    dict(axis="b3", direction="fwd", scale="z", n_bins=8, bin_method="equal_width", band="full"),
    dict(axis="b2", direction="fwd", scale="z", n_bins=8, bin_method="equal_width", band="boe"),
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Army HERO grid runner (B1–B3 campaign)")
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--tag", default="run1")
    parser.add_argument("--quick", action="store_true", help="Small smoke grid (3 plots)")
    parser.add_argument("--dry-run", action="store_true", help="Print jobs only")
    parser.add_argument("--axes", nargs="+", choices=DEFAULT_AXES, default=list(DEFAULT_AXES))
    parser.add_argument("--directions", nargs="+", choices=DEFAULT_DIRECTIONS, default=list(DEFAULT_DIRECTIONS))
    parser.add_argument("--scales", nargs="+", choices=DEFAULT_SCALES, default=list(DEFAULT_SCALES))
    parser.add_argument("--bands", nargs="+", choices=DEFAULT_BANDS, default=list(DEFAULT_BANDS))
    parser.add_argument("--n-bins", nargs="+", type=int, default=list(DEFAULT_N_BINS))
    parser.add_argument(
        "--bin-methods",
        nargs="+",
        choices=DEFAULT_BIN_METHODS,
        default=list(DEFAULT_BIN_METHODS),
    )
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers = None if args.dry_run else load_feather_officers(feather)

    if args.quick:
        jobs = [dict(**spec, tag=args.tag) for spec in QUICK_GRID]
    else:
        jobs = [
            dict(
                axis=ax,
                direction=dr,
                scale=sc,
                n_bins=nb,
                bin_method=bm,
                band=bd,
                tag=args.tag,
            )
            for ax, dr, sc, nb, bm, bd in itertools.product(
                args.axes,
                args.directions,
                args.scales,
                args.n_bins,
                args.bin_methods,
                args.bands,
            )
        ]

    print(f"HERO grid: {len(jobs)} jobs · feather={feather}")
    ok, fail = 0, 0
    for job in jobs:
        line = (
            f"  {job['axis']} {job['direction']} {job['scale']} "
            f"{job['bin_method']} n={job['n_bins']} band={job['band']}"
        )
        if args.dry_run:
            print(line)
            continue
        print(line, end=" … ", flush=True)
        try:
            build_hero_panel(
                officers,
                axis=job["axis"],
                direction=job["direction"],
                scale=job["scale"],
                n_bins=job["n_bins"],
                bin_method=job["bin_method"],
                band=job["band"],
                tag=job["tag"],
            )
            ok += 1
            print("ok")
        except SystemExit as exc:
            fail += 1
            print(f"SKIP ({exc})")
        except Exception as exc:
            fail += 1
            print(f"FAIL ({exc})")

    if not args.dry_run:
        print(f"Done: {ok} written, {fail} skipped/failed.")


if __name__ == "__main__":
    main()
