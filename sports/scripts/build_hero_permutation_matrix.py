#!/usr/bin/env python3
"""Build slide × permutation choice matrix from hero_permutation_slides/manifest.json.

Each row = one deck slide (PPT slide number). Columns = orthogonal knob values;
``X`` marks which setting that slide uses (exactly one X per knob group).

Also writes shape readouts (β₂, peak bin) to spot trends while scanning.

Run (repo root):
  python sports/scripts/build_hero_permutation_matrix.py
  python sports/scripts/build_hero_permutation_matrix.py --manifest path/to/manifest.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SANDBOX = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox"
DEFAULT_MANIFEST = SANDBOX / "hero_permutation_slides/manifest.json"
DEFAULT_CSV = SANDBOX / "hero_permutation_slides/HERO_permutation_matrix.csv"
DEFAULT_MD = SANDBOX / "hero_permutation_slides/HERO_permutation_matrix.md"

# Column groups (one X per group per row). Order matches sweep axes left → right.
CHOICE_COLUMNS: tuple[tuple[str, str], ...] = (
    ("poolq_loo", "roster_x:poolq_loo"),
    ("poolq", "roster_x:poolq"),
    ("ever", "y:ever"),
    ("season-Y", "y:season"),
    ("all-ps", "panel:all-ps"),
    ("last-ps", "panel:last-ps"),
    ("ALLT", "pop:allt"),
    ("+DFT", "pop:dft"),
    ("q16", "bin:q16"),
    ("q20", "bin:q20"),
    ("ew16", "bin:ew16"),
    ("ew20", "bin:ew20"),
)

READOUT_COLUMNS: tuple[str, ...] = (
    "peak_vent",
    "peak_rate_pct",
    "bin0_rate_pct",
    "beta_sq",
    "bin0_peak",
)


def _spec_dict(run: dict) -> dict:
    spec = run.get("spec")
    if isinstance(spec, dict):
        return spec
    return run


def _bin_slug(spec: dict) -> str:
    mode = str(spec.get("poolq_binning", "quantile")).strip().lower()
    n = int(spec.get("n_bins", 16))
    if mode == "equal_width":
        return f"ew{n}"
    return f"q{n}"


def _active_choices(spec: dict) -> set[str]:
    """Return internal choice keys (one per knob group) that are active for this spec."""
    out: set[str] = set()
    rx = str(spec.get("roster_x", "poolq_loo"))
    out.add("roster_x:poolq_loo" if rx == "poolq_loo" else "roster_x:poolq")
    ym = str(spec.get("y_draft_mode", "ever"))
    out.add("y:ever" if ym == "ever" else "y:season")
    pr = str(spec.get("panel_rows", "all-ps"))
    out.add("panel:all-ps" if pr == "all-ps" else "panel:last-ps")
    out.add("pop:dft" if bool(spec.get("dft")) else "pop:allt")
    out.add(f"bin:{_bin_slug(spec)}")
    return out


def _shape_fields(run: dict) -> dict[str, str]:
    shape = run.get("shape") or {}
    peak_v = shape.get("peak_vent")
    peak_disp = str(int(peak_v) + 1) if peak_v is not None else ""
    return {
        "peak_vent": peak_disp,
        "peak_rate_pct": _fmt_num(shape.get("peak_rate_pct")),
        "bin0_rate_pct": _fmt_num(shape.get("bin0_rate_pct")),
        "beta_sq": _fmt_num(shape.get("beta_sq"), signed=True),
        "bin0_peak": "X" if shape.get("bin0_is_peak") else "",
    }


def _fmt_num(val, *, signed: bool = False) -> str:
    if val is None:
        return ""
    try:
        f = float(val)
    except (TypeError, ValueError):
        return ""
    if signed:
        return f"{f:+.4g}"
    return f"{f:.4g}"


def build_matrix_rows(manifest: dict) -> list[dict[str, str]]:
    runs = sorted(manifest.get("runs") or [], key=lambda r: int(r.get("slide_index") or 0))
    rows: list[dict[str, str]] = []
    for run in runs:
        spec = _spec_dict(run)
        active = _active_choices(spec)
        row: dict[str, str] = {
            "slide": str(run.get("slide_index", "")),
            "output_tag": str(run.get("output_tag", "")),
        }
        for col_label, choice_key in CHOICE_COLUMNS:
            row[col_label] = "X" if choice_key in active else ""
        row.update(_shape_fields(run))
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    headers = ["slide", "output_tag", *[c[0] for c in CHOICE_COLUMNS], *READOUT_COLUMNS, "PICK"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            out = {h: row.get(h, "") for h in headers}
            if not out.get("PICK"):
                out["PICK"] = ""
            w.writerow(out)


def write_markdown(path: Path, manifest: dict, rows: list[dict[str, str]]) -> None:
    tier = manifest.get("tier", "?")
    season = manifest.get("season_window") or manifest.get("season_windows", "?")
    date = manifest.get("date", "")
    choice_headers = [c[0] for c in CHOICE_COLUMNS]
    all_headers = ["slide", "output_tag", *choice_headers, *READOUT_COLUMNS, "PICK"]

    lines = [
        "# HERO permutation matrix",
        "",
        f"**Tier:** `{tier}` · **Season:** `{season}` · **Date:** {date}",
        "",
        "Each row = PowerPoint slide number. **X** = that knob setting applies (one X per group).",
        "Empty **PICK** column — mark slides you shortlist while reviewing the deck.",
        "",
        "| " + " | ".join(all_headers) + " |",
        "| " + " | ".join(["---"] * len(all_headers)) + " |",
    ]
    for row in rows:
        cells = [row.get(h, "") for h in all_headers]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append(
        "_Regenerate: `python sports/scripts/build_hero_permutation_matrix.py` "
        "(also runs automatically after `build_hero_permutation_slides.py`)._"
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_permutation_matrix(
    manifest: dict,
    *,
    csv_path: Path,
    md_path: Path,
) -> tuple[Path, Path]:
    rows = build_matrix_rows(manifest)
    write_csv(csv_path, rows)
    write_markdown(md_path, manifest, rows)
    return csv_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="HERO permutation matrix from manifest.json")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    manifest_path = args.manifest if args.manifest.is_absolute() else REPO / args.manifest
    if not manifest_path.is_file():
        raise SystemExit(f"Missing manifest {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = manifest.get("runs") or []
    if not runs:
        raise SystemExit("Manifest has no runs.")

    csv_path = args.csv if args.csv.is_absolute() else REPO / args.csv
    md_path = args.md if args.md.is_absolute() else REPO / args.md
    build_permutation_matrix(manifest, csv_path=csv_path, md_path=md_path)
    print(f"Wrote {csv_path.relative_to(REPO)} · {len(runs)} rows")
    print(f"Wrote {md_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
