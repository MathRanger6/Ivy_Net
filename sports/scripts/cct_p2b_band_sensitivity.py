#!/usr/bin/env python3
"""Run P2b overlay band schemes side-by-side + one summary figure for humans.

Writes per-scheme overlay PNG + sweep CSV under ``band_sensitivity/<scheme>/``,
then ``band_sensitivity/BAND_SENSITIVITY_summary.png`` (2×2 overlays + readout bars).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "sports/scripts/cct_p2b_ai_band_overlay.py"
DEFAULT_OUT = (
    REPO
    / "3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_archive/band_sensitivity_2026-08"
)


@dataclass(frozen=True)
class Scheme:
    slug: str
    title: str
    subtitle: str
    extra_args: list[str]


SCHEMES: tuple[Scheme, ...] = (
    Scheme(
        "dm30",
        "A — 30% draft-mass tiers",
        "Equal ~127 drafts per line · current default",
        [],  # uses --draft-mass-tiers 30 in _run_scheme
    ),
    Scheme(
        "slide10",
        "B — Slide-10 percentiles",
        "0:7 · 7:15 · 15:25 · 25:40 (Alex prose)",
        ["--bands", "0:7,7:15,15:25,25:40", "--hero-top", "0:7", "--no-draft-mass-tiers"],
    ),
    Scheme(
        "two_band",
        "C — 2-band compromise",
        "Elite top 7% vs rest 7–20%",
        ["--bands", "0:7,7:20", "--hero-top", "0:7", "--no-draft-mass-tiers"],
    ),
    Scheme(
        "suggest10",
        "D — Data-driven (10% steps)",
        "Auto bands until min n / drafts fail",
        [
            "--suggest-width",
            "10",
            "--min-band-n",
            "150",
            "--min-drafts",
            "40",
            "--no-draft-mass-tiers",
        ],
    ),
)


def _run_scheme(scheme: Scheme, out_root: Path, *, skip_rerun: bool) -> Path:
    scheme_dir = out_root / scheme.slug
    scheme_dir.mkdir(parents=True, exist_ok=True)
    stem_glob = list(scheme_dir.glob("FHERO_pw4p7_overlay_lines_sharetj_*_sweep.csv"))
    if skip_rerun and stem_glob:
        return stem_glob[0]

    args = [
        sys.executable,
        str(SCRIPT),
        "--season-min",
        "2013",
        "--season-max",
        "2021",
        "--panel-rows",
        "last-ps",
        "--y-draft-mode",
        "ever",
        "--no-dft",
        "--tj-n-low",
        "4",
        "--tj-n-high",
        "7",
        "--tj-edge-mode",
        "shared_panel",
        "--out-dir",
        str(scheme_dir),
    ]
    if scheme.slug == "dm30":
        args.extend(["--draft-mass-tiers", "30"])
    else:
        args.extend(scheme.extra_args)

    print(f"\n=== {scheme.title} ===", flush=True)
    subprocess.run(args, check=True, cwd=REPO)
    stem_glob = list(scheme_dir.glob("FHERO_pw4p7_overlay_lines_sharetj_*_sweep.csv"))
    if not stem_glob:
        raise FileNotFoundError(f"No sweep CSV in {scheme_dir}")
    return stem_glob[0]


def _hero_row(sweep: pd.DataFrame) -> pd.Series:
    """Top / elite band: smallest top_hi (F-HERO)."""
    s = sweep.copy()
    s["_hi"] = pd.to_numeric(s["top_hi"], errors="coerce")
    return s.loc[s["_hi"].idxmin()]


def _build_summary(out_root: Path, schemes: tuple[Scheme, ...], sweeps: dict[str, pd.DataFrame]) -> Path:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.05, 1.05, 0.75], hspace=0.28, wspace=0.12)

    for i, scheme in enumerate(schemes):
        row, col = divmod(i, 2)
        ax = fig.add_subplot(gs[row, col])
        pngs = list((out_root / scheme.slug).glob("FHERO_pw4p7_overlay_lines_sharetj_*.png"))
        if pngs:
            ax.imshow(mpimg.imread(pngs[0]))
        ax.set_title(f"{scheme.title}\n{scheme.subtitle}", fontsize=10, pad=6)
        ax.axis("off")

    # Bottom readout: top-tier power metrics
    ax_bar = fig.add_subplot(gs[2, :])
    labels = []
    min_bins = []
    drafts = []
    downturns = []
    knees = []
    for scheme in schemes:
        sw = sweeps[scheme.slug]
        hero = _hero_row(sw)
        labels.append(scheme.slug.upper())
        min_bins.append(float(hero.get("min_bin_n", 0) or 0))
        drafts.append(float(hero.get("total_drafts", 0) or 0))
        downturns.append(1.0 if str(hero.get("downturn_visible", False)).lower() in ("true", "1") else 0.0)
        knees.append(float(hero.get("knee_tj_peak", np.nan)))

    x = np.arange(len(labels))
    w = 0.22
    ax_bar.bar(x - 1.5 * w, min_bins, width=w, label="Top-tier min bin n", color="#1565c0")
    ax_bar.bar(x - 0.5 * w, drafts, width=w, label="Top-tier drafts K", color="#2e7d32")
    ax_bar.bar(x + 0.5 * w, np.array(downturns) * 100, width=w, label="Downturn visible (0/100)", color="#c62828")
    ax2 = ax_bar.twinx()
    ax2.plot(x, knees, "D-", color="#6a1b9a", ms=8, lw=2, label="Top-tier knee T̂_j")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.set_ylabel("Count / flag (×100 for downturn)")
    ax2.set_ylabel("Knee T̂_j (top tier)")
    ax_bar.set_title(
        "Top Â band only — power & knee readout (compare schemes at a glance)",
        fontsize=11,
        pad=10,
    )
    ax_bar.legend(loc="upper left", fontsize=9)
    ax2.legend(loc="upper right", fontsize=9)
    ax_bar.set_ylim(0, max(max(min_bins), max(drafts), 100) * 1.15)

    fig.suptitle(
        "P2b band sensitivity · MBB 2013–21 · last-ps · ALLT · mg10 min20 · shared T̂_j grid",
        fontsize=12,
        y=0.98,
    )
    out_png = out_root / "BAND_SENSITIVITY_summary.png"
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_png


def _write_readout_md(out_root: Path, schemes: tuple[Scheme, ...], sweeps: dict[str, pd.DataFrame]) -> Path:
    lines = [
        "# P2b band sensitivity readout",
        "",
        "**Spec:** 2013–21 · last-ps · ALLT · mg10 min20 · shared T̂_j 4+7",
        "",
        "## Top tier (F-HERO / elite band) — what matters for the knee",
        "",
        "| Scheme | Band | n | Drafts | min bin n | Downturn? | Knee T̂_j | Peak rate |",
        "|--------|------|---|--------|-----------|-----------|----------|-----------|",
    ]
    for scheme in schemes:
        sw = sweeps[scheme.slug]
        hero = _hero_row(sw)
        lines.append(
            f"| **{scheme.slug}** | {hero['band']} | {int(hero['band_n']):,} | "
            f"{int(hero['total_drafts']):,} | {int(hero.get('min_bin_n', 0))} | "
            f"{'Yes' if hero.get('downturn_visible') else 'No'} | "
            f"{float(hero.get('knee_tj_peak', float('nan'))):.2f} | "
            f"{100 * float(hero.get('knee_rate_peak', 0)):.1f}% |"
        )
    lines.extend(["", "## All bands per scheme", ""])
    for scheme in schemes:
        lines.append(f"### {scheme.title}")
        lines.append("")
        sw = sweeps[scheme.slug]
        cols = ["band", "band_n", "total_drafts", "min_bin_n", "downturn_visible", "knee_tj_peak"]
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "---|" * len(cols))
        for _, r in sw.iterrows():
            lines.append(
                "| "
                + " | ".join(
                    str(r[c]) if c != "downturn_visible" else ("Yes" if r[c] else "No")
                    for c in cols
                )
                + " |"
            )
        lines.append("")
    out_md = out_root / "BAND_SENSITIVITY_readout.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_md


def main() -> None:
    parser = argparse.ArgumentParser(description="P2b band sensitivity sweep + summary figure.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--skip-rerun", action="store_true", help="Use existing scheme CSVs if present.")
    args = parser.parse_args()
    out_root = args.out_dir if args.out_dir.is_absolute() else REPO / args.out_dir
    out_root.mkdir(parents=True, exist_ok=True)

    sweeps: dict[str, pd.DataFrame] = {}
    for scheme in SCHEMES:
        csv_path = _run_scheme(scheme, out_root, skip_rerun=args.skip_rerun)
        sweeps[scheme.slug] = pd.read_csv(csv_path)

    summary_png = _build_summary(out_root, SCHEMES, sweeps)
    readout_md = _write_readout_md(out_root, SCHEMES, sweeps)
    meta = {
        "schemes": [s.slug for s in SCHEMES],
        "summary_png": summary_png.name,
        "readout_md": readout_md.name,
    }
    (out_root / "BAND_SENSITIVITY_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"\nWrote {summary_png.relative_to(REPO)}")
    print(f"Wrote {readout_md.relative_to(REPO)}")


if __name__ == "__main__":
    main()
