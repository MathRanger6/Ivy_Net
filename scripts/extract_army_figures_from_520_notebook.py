#!/usr/bin/env python3
"""Extract Army G1 figures from a executed 520_pipeline_cox_working.ipynb into army_sandbox/.

Canonical names (used by build_flipbook_figure_deck.py auto-discovery)
----------------------------------------------------------------------
Flipbook slot          | Canonical filename (write this)              | Notebook source
-----------------------|----------------------------------------------|------------------
G1 hero porch          | ARMY_G1_pool_minus_mean_fwd_cif_b8.png       | Cell 11 — CIF bars on z_pool_minus_mean_snr_fwd, 8 bins
Own-TB baseline        | ARMY_own_tb_ratio_fwd_cif_b8.png             | Cell 11 — CIF bars on z_tb_ratio_fwd_snr, 8 bins
Cox partial effects    | ARMY_partial_effects_pool_minus_mean.png     | Cell 12.6 — partial_effects_plots_stdz.png

Optional extras (saved when --extras; not required for flipbook inventory):
  ARMY_star_pool_interaction_cif_b8.png       — Cell 11 interaction CIF bars
  ARMY_tb_by_division_cif_b1.png              — Cell 11 TB ratio by div_name
  ARMY_cox_competing_risks_analysis_stdz.png  — Cell 12.5
  ARMY_cox_model_comparison_stdz.png          — Cell 12.4
  ARMY_combined_effect_pool_minus_mean_stdz.png — Cell 12.6A (pool-minus-mean combined effect)

Cell 11 inline PNG order per plot (do not confuse):
  ~170KB  competing-risks curve figure (optional: *_CR_curves.png)
  ~20KB   Final CIF bar chart      ← canonical G1 / own-TB
  ~200KB  metadata card            ← never export for decks

AWS Run 1 cif_bars filenames (cross-check):
  cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png
  cr_z_tb_r_fwd_none_b8_ew_noOER_2002-2022_cif_bars.png

Usage:
  python scripts/extract_army_figures_from_520_notebook.py
  python scripts/extract_army_figures_from_520_notebook.py --notebook path/to/520.ipynb --extras
  python scripts/extract_army_figures_from_520_notebook.py --dry-run

Then regenerate decks:
  python scripts/build_flipbook_figure_deck.py
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_NOTEBOOK = (
    REPO
    / "talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb"
)
OUT_DIR = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox"

# Canonical flipbook trio — keys match build_flipbook_figure_deck.py slots
CANONICAL_EXPORTS: dict[str, dict[str, str]] = {
    "hero_cif": {
        "filename": "ARMY_G1_pool_minus_mean_fwd_cif_b8.png",
        "description": "G1 — 8-bin promotion CIF bars, z_pool_minus_mean_snr_fwd (Run 1)",
    },
    "own_tb_cif": {
        "filename": "ARMY_own_tb_ratio_fwd_cif_b8.png",
        "description": "Own TB ratio — monotone 8-bin promotion CIF bars (Run 1)",
    },
    "partial_effects": {
        "filename": "ARMY_partial_effects_pool_minus_mean.png",
        "description": "Cell 12.6A combined effect — z_pool_minus_mean_snr_fwd (+ sq), full model",
    },
}

# Optional CR curve figures (~170KB each) — full promotion/attrition CIF curves over time
OPTIONAL_CR_CURVES: dict[str, dict[str, str]] = {
    "hero_cr_curves": {
        "filename": "ARMY_G1_pool_minus_mean_fwd_CR_curves.png",
        "plot_create_pattern": r"run1_cr_z_pool_minus_mean",
    },
    "own_tb_cr_curves": {
        "filename": "ARMY_own_tb_ratio_fwd_CR_curves.png",
        "plot_create_pattern": r"run1_cr_z_tb_ratio",
    },
}

OPTIONAL_EXPORTS: list[dict[str, str]] = [
    {
        "filename": "ARMY_star_pool_interaction_cif_b8.png",
        "cell_index": "51",
        "plot_create": r"run1_cr_star_pool",
    },
    {
        "filename": "ARMY_tb_by_division_cif_b1.png",
        "cell_index": "51",
        "plot_create": r"run1_cr_tb_by_div",
    },
    {
        "filename": "ARMY_cox_competing_risks_analysis_stdz.png",
        "cell_index": "68",
        "match": r"competing_risks_analysis_stdz",
    },
    {
        "filename": "ARMY_cox_model_comparison_stdz.png",
        "cell_index": "66",
        "match": r"model_comparison_stdz",
    },
    {
        "filename": "ARMY_combined_effect_pool_minus_mean_stdz.png",
        "cell_index": "73",
        "match": r"combined_effect.*pool_minus_mean",
        "png_index": "0",
    },
]


def _cell_index(notebook: dict, marker: str) -> int | None:
    for i, cell in enumerate(notebook.get("cells", [])):
        src = "".join(cell.get("source", []))
        if marker in src and cell.get("cell_type") == "code":
            return i
    return None


def _png_bytes_from_output(output: dict) -> bytes | None:
    data = output.get("data") or {}
    b64 = data.get("image/png")
    if not b64:
        return None
    return base64.standard_b64decode(b64)


def _extract_cell11_cif_bars(cell: dict, plot_create_pattern: str) -> tuple[str, bytes] | None:
    """Extract the ~20KB CIF bar panel from a Cell 11 plot block.

    Each plot block in the saved notebook emits three inline PNGs:
      1. ~170KB — full competing-risks curve figure
      2. ~20KB  — Final CIF bar chart (promotion + attrition bars)  ← flipbook G1
      3. ~200KB — metadata card (never use for decks)

    The metadata PNG comes *after* the 'Saved metadata:' log line, so we must not
    pair 'Created CIF bar plot:' with the next large PNG.
    """
    rx_create = re.compile(plot_create_pattern, re.IGNORECASE)
    in_block = False
    block_pngs: list[bytes] = []
    cif_filename: str | None = None

    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            text = output.get("text", "")
            if isinstance(text, list):
                text = "".join(text)
            for line in text.split("\n"):
                if "Creating plot:" in line:
                    if rx_create.search(line):
                        in_block = True
                        block_pngs = []
                        cif_filename = None
                    elif in_block:
                        in_block = False
                elif in_block and "Created CIF bar plot:" in line:
                    m = re.search(r"Created CIF bar plot:\s*(\S+)", line)
                    if m:
                        cif_filename = m.group(1).rstrip(",")
                elif in_block and "Saved metadata:" in line and cif_filename:
                    cif_png = next((p for p in block_pngs if len(p) < 50_000), None)
                    if cif_png:
                        return cif_filename, cif_png
                    in_block = False
        elif output.get("output_type") == "display_data" and in_block:
            raw = _png_bytes_from_output(output)
            if raw:
                block_pngs.append(raw)
    return None


def _extract_cell11_cr_curves(cell: dict, plot_create_pattern: str) -> tuple[str, bytes] | None:
    """Optional: full CR curve figure (~170KB) — first large PNG in the plot block."""
    rx_create = re.compile(plot_create_pattern, re.IGNORECASE)
    in_block = False
    block_pngs: list[bytes] = []
    cr_filename: str | None = None

    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            text = output.get("text", "")
            if isinstance(text, list):
                text = "".join(text)
            for line in text.split("\n"):
                if "Creating plot:" in line:
                    if rx_create.search(line):
                        in_block = True
                        block_pngs = []
                        cr_filename = None
                    elif in_block:
                        in_block = False
                elif in_block and "Created competing risks plot:" in line:
                    m = re.search(r"Created competing risks plot:\s*(\S+)", line)
                    if m:
                        cr_filename = m.group(1).rstrip(",")
                elif in_block and "Saved metadata:" in line and block_pngs:
                    first_large = next((p for p in block_pngs if len(p) >= 50_000), None)
                    if first_large:
                        return (cr_filename or "cr_curves.png"), first_large
                    in_block = False
        elif output.get("output_type") == "display_data" and in_block:
            raw = _png_bytes_from_output(output)
            if raw:
                block_pngs.append(raw)
    return None


def _extract_first_png_after_stream(cell: dict, pattern: str, png_index: int = 0) -> bytes | None:
    """First PNG after a stream line matching pattern (for Cell 12 saves)."""
    seen_match = False
    png_i = 0
    rx = re.compile(pattern, re.IGNORECASE)
    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            text = output.get("text", "")
            if isinstance(text, list):
                text = "".join(text)
            if rx.search(text):
                seen_match = True
        elif seen_match and output.get("output_type") == "display_data":
            raw = _png_bytes_from_output(output)
            if raw:
                if png_i == png_index:
                    return raw
                png_i += 1
    # Cell 12.6: often one PNG with no matching stream in saved output — take first PNG
    if png_index == 0:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "display_data":
                raw = _png_bytes_from_output(output)
                if raw:
                    return raw
    return None


def _extract_126a_pool_combined(cell: dict) -> tuple[str, bytes] | None:
    """Cell 12.6A — first combined-effect panel for z_pool_minus_mean_snr_fwd (+ sq)."""
    in_pool = False
    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            text = output.get("text", "")
            if isinstance(text, list):
                text = "".join(text)
            if "Combined effect pair: z_pool_minus_mean" in text:
                in_pool = True
        elif in_pool and output.get("output_type") == "display_data":
            raw = _png_bytes_from_output(output)
            if raw:
                return ("combined_effect_z_pool_minus_mean_snr_fwd_stdz.png", raw)
    return None


def extract_core(notebook: dict) -> dict[str, tuple[str, bytes]]:
    cells = notebook["cells"]
    idx11 = _cell_index(notebook, "CELL 11: COX ANALYSIS & PLOTTING")
    idx126a = _cell_index(notebook, "12.6A. COMBINED EFFECT")
    if idx11 is None:
        raise SystemExit("Could not find Cell 11 in notebook.")
    if idx126a is None:
        raise SystemExit("Could not find Cell 12.6A in notebook.")

    cell11 = cells[idx11]
    found: dict[str, tuple[str, bytes]] = {}

    hero = _extract_cell11_cif_bars(cell11, r"run1_cr_z_pool_minus_mean")
    if hero:
        found["hero_cif"] = hero

    own_tb = _extract_cell11_cif_bars(cell11, r"run1_cr_z_tb_ratio")
    if own_tb:
        found["own_tb_cif"] = own_tb

    pe = _extract_126a_pool_combined(cells[idx126a])
    if pe:
        found["partial_effects"] = pe

    return found


def extract_optional(notebook: dict) -> list[tuple[str, str, bytes]]:
    cells = notebook["cells"]
    out: list[tuple[str, str, bytes]] = []
    for spec in OPTIONAL_EXPORTS:
        idx = int(spec["cell_index"])
        if idx >= len(cells):
            continue
        cell = cells[idx]
        png_index = int(spec.get("png_index", 0))
        if spec.get("cell_index") == "51" and spec.get("plot_create"):
            hit = _extract_cell11_cif_bars(cell, spec["plot_create"])
            if hit:
                aws_name, raw = hit
                out.append((spec["filename"], aws_name, raw))
        else:
            raw = _extract_first_png_after_stream(cell, spec["match"], png_index=png_index)
            if raw:
                out.append((spec["filename"], spec["match"], raw))
    return out


def write_png(path: Path, data: bytes, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path} ({len(data)//1024} KB)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"  wrote {path.relative_to(REPO)} ({len(data)//1024} KB)")


def print_canonical_table() -> None:
    print("Canonical filenames for flipbook / build_flipbook_figure_deck.py:\n")
    print(f"{'Slot':<18} {'Filename':<44} Description")
    print("-" * 100)
    for slot, meta in CANONICAL_EXPORTS.items():
        print(f"{slot:<18} {meta['filename']:<44} {meta['description']}")
    print("\nOptional (--extras):\n")
    for spec in OPTIONAL_EXPORTS:
        print(f"  {spec['filename']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK, help="Executed 520 notebook path")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR, help="Output directory (army_sandbox)")
    parser.add_argument("--extras", action="store_true", help="Also extract optional supporting figures")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    parser.add_argument("--list-names", action="store_true", help="Print canonical name table and exit")
    args = parser.parse_args()

    if args.list_names:
        print_canonical_table()
        return 0

    nb_path = args.notebook.resolve()
    if not nb_path.exists():
        print(f"Notebook not found: {nb_path}", file=sys.stderr)
        return 1

    notebook = json.loads(nb_path.read_text(encoding="utf-8"))
    print(f"Source: {nb_path.relative_to(REPO)}")
    print(f"Output: {args.out_dir.relative_to(REPO)}/\n")

    found = extract_core(notebook)
    missing = [k for k in CANONICAL_EXPORTS if k not in found]
    if missing:
        print("ERROR: Could not extract required slots:", ", ".join(missing), file=sys.stderr)
        print("Use an executed notebook (Mar 2026 AWS export with Cell 11+ outputs).", file=sys.stderr)
        return 1

    manifest_lines = [
        "# Army figure extract manifest (auto-generated)",
        f"# Source notebook: {nb_path.relative_to(REPO)}",
        "# Canonical names consumed by scripts/build_flipbook_figure_deck.py",
        "",
        "| Slot | Canonical file | AWS / notebook label |",
        "|------|----------------|----------------------|",
    ]

    for slot, (aws_name, raw) in found.items():
        canon = CANONICAL_EXPORTS[slot]["filename"]
        write_png(args.out_dir / canon, raw, args.dry_run)
        manifest_lines.append(f"| {slot} | `{canon}` | `{aws_name}` |")
        # Keep AWS-named copy for traceability
        aws_copy = args.out_dir / "aws_originals" / aws_name
        write_png(aws_copy, raw, args.dry_run)

    if args.extras:
        print("\nOptional extras:")
        cell11 = notebook["cells"][_cell_index(notebook, "CELL 11: COX ANALYSIS & PLOTTING")]
        for _slot, spec in OPTIONAL_CR_CURVES.items():
            hit = _extract_cell11_cr_curves(cell11, spec["plot_create_pattern"])
            if hit:
                aws_name, raw = hit
                write_png(args.out_dir / spec["filename"], raw, args.dry_run)
                manifest_lines.append(f"| extra | `{spec['filename']}` | `{aws_name}` |")
        for filename, label, raw in extract_optional(notebook):
            write_png(args.out_dir / filename, raw, args.dry_run)
            manifest_lines.append(f"| extra | `{filename}` | `{label}` |")

    if not args.dry_run:
        manifest_path = args.out_dir / "EXTRACT_MANIFEST.txt"
        manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
        print(f"\nManifest: {manifest_path.relative_to(REPO)}")

    print("\nRegenerate figure decks:")
    print("  python scripts/build_flipbook_figure_deck.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
