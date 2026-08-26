#!/usr/bin/env python3
"""Run HERO setting permutations for population_sandbox and write a manifest.

Orthogonal axes (default tier = core 2×2×2 = 8 runs per season window):
  --roster-x poolq_loo | poolq
  --y-draft-mode ever | season
  --panel-rows all-ps | last-ps

Season window: --season-window 11_21 (default) | 13_21 | both

Extended (--tier extended): × +DFT (16 per window).
Full (--tier full): extended × quantile q16 vs equal_width ew20 (32 per window).
real_full (--tier real_full): full grid × both season windows (64 runs).

Manifest → hero_permutation_slides/manifest.json (append after each run).

Run (repo root):
  python sports/scripts/hero_permutation_sweep.py --dry-run
  python sports/scripts/hero_permutation_sweep.py --tier core
  python sports/scripts/hero_permutation_sweep.py --tier core --season-window 13_21
  python sports/scripts/hero_permutation_sweep.py --tier core --season-window both
  python sports/scripts/hero_permutation_sweep.py --tier real_full
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from itertools import product
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "sports/scripts"
sys.path.insert(0, str(SCRIPTS))

from pd20_22_campaign_window import (  # noqa: E402
    FULL_PANEL_SEASON_MAX,
    FULL_PANEL_SEASON_MIN,
    PRIMARY_SEASON_MAX,
    PRIMARY_SEASON_MIN,
)
from plot_provenance import roster_x_slug  # noqa: E402

BUNDLE = SCRIPTS / "pass_a_empirical_bundle.py"
SANDBOX = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox"
HERO_OUT = SANDBOX / "hero"
SLIDES_DIR = SANDBOX / "hero_permutation_slides"
MANIFEST = SLIDES_DIR / "manifest.json"

SEASON_WINDOWS: dict[str, tuple[int, int]] = {
    "11_21": (FULL_PANEL_SEASON_MIN, FULL_PANEL_SEASON_MAX),
    "13_21": (PRIMARY_SEASON_MIN, PRIMARY_SEASON_MAX),
}

BASELINE = {
    "y_draft_mode": "ever",
    "panel_rows": "all-ps",
    "roster_x": "poolq_loo",
    "n_bins": 16,
    "poolq_binning": "quantile",
    "dft": False,
    "season_window": "11_21",
    "output_tag": "FIXED_HERO",
    "label": "FIXED HERO — canonical deck",
}


@dataclass(frozen=True)
class HeroPermSpec:
    y_draft_mode: str
    panel_rows: str
    roster_x: str
    n_bins: int
    poolq_binning: str
    dft: bool
    season_min: int
    season_max: int
    season_window: str
    output_tag: str
    label: str

    def diff_from_baseline(self) -> list[str]:
        diffs: list[str] = []
        if self.season_window != BASELINE["season_window"]:
            diffs.append(f"season_window: {BASELINE['season_window']} → {self.season_window}")
        for key in ("roster_x", "y_draft_mode", "panel_rows", "poolq_binning", "n_bins", "dft"):
            cur = getattr(self, key)
            base = BASELINE[key]
            if cur != base:
                diffs.append(f"{key}: {base} → {cur}")
        return diffs

    def command(self) -> str:
        parts = [
            "python sports/scripts/pass_a_empirical_bundle.py",
            f"--season-min {self.season_min}",
            f"--season-max {self.season_max}",
            f"--y-draft-mode {self.y_draft_mode}",
            f"--panel-rows {self.panel_rows}",
            f"--roster-x {self.roster_x}",
            f"--n-bins {self.n_bins}",
            f"--poolq-binning {self.poolq_binning}",
            f"--output-tag {self.output_tag}",
            f"--output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero",
        ]
        if self.dft:
            parts.append("--dft")
        return " \\\n  ".join(parts)

    def command_one_line(self) -> str:
        return self.command().replace(" \\\n  ", " ")


def _tag(
    *,
    roster_x: str,
    y_draft_mode: str,
    panel_rows: str,
    poolq_binning: str,
    dft: bool,
) -> str:
    rx = "loo" if roster_x == "poolq_loo" else "poolq"
    y = "ever" if y_draft_mode == "ever" else "seasony"
    pr = "allps" if panel_rows == "all-ps" else "lastps"
    bin_slug = "q16" if poolq_binning == "quantile" else "ew20"
    dft_slug = "_dft" if dft else ""
    return f"perm_{rx}_{y}_{pr}_{bin_slug}{dft_slug}"


def _label(
    *,
    roster_x: str,
    y_draft_mode: str,
    panel_rows: str,
    poolq_binning: str,
    dft: bool,
    season_window: str,
) -> str:
    rx = "LOO poolq_loo" if roster_x == "poolq_loo" else "team poolq (incl. self)"
    y = "ever-draft" if y_draft_mode == "ever" else "season-Y label"
    pr = "all PS rows" if panel_rows == "all-ps" else "last PS only (cross-section)"
    bins = "QTL16" if poolq_binning == "quantile" else "EW20"
    dft_s = " +DFT" if dft else " ALLT"
    seasons = season_window.replace("_", "–")
    return f"{seasons} · {rx} · {y} · {pr} · {bins}{dft_s}"


def _iter_base_specs(*, tier: str) -> list[HeroPermSpec]:
    """One season window — baseline + factorial grid."""
    roster_opts = ("poolq_loo", "poolq")
    y_opts = ("ever", "season")
    panel_opts = ("all-ps", "last-ps")
    dft_opts = (False,) if tier == "core" else (False, True)
    bin_opts = (
        (("quantile", 16), ("equal_width", 20))
        if tier == "full"
        else (("quantile", 16),)
    )

    specs: list[HeroPermSpec] = []
    seen_tags: set[str] = set()

    def _append(spec: HeroPermSpec) -> None:
        if spec.output_tag in seen_tags:
            return
        seen_tags.add(spec.output_tag)
        specs.append(spec)

    _append(
        HeroPermSpec(
            y_draft_mode=BASELINE["y_draft_mode"],
            panel_rows=BASELINE["panel_rows"],
            roster_x=BASELINE["roster_x"],
            n_bins=BASELINE["n_bins"],
            poolq_binning=BASELINE["poolq_binning"],
            dft=BASELINE["dft"],
            season_min=0,
            season_max=0,
            season_window="",
            output_tag=BASELINE["output_tag"],
            label=BASELINE["label"],
        )
    )

    for roster_x, y_mode, panel_rows, dft, (binning, n_bins) in product(
        roster_opts, y_opts, panel_opts, dft_opts, bin_opts
    ):
        tag = _tag(
            roster_x=roster_x,
            y_draft_mode=y_mode,
            panel_rows=panel_rows,
            poolq_binning=binning,
            dft=dft,
        )
        if tag in seen_tags or (
            roster_x == BASELINE["roster_x"]
            and y_mode == BASELINE["y_draft_mode"]
            and panel_rows == BASELINE["panel_rows"]
            and binning == BASELINE["poolq_binning"]
            and dft == BASELINE["dft"]
        ):
            continue
        _append(
            HeroPermSpec(
                y_draft_mode=y_mode,
                panel_rows=panel_rows,
                roster_x=roster_x,
                n_bins=n_bins,
                poolq_binning=binning,
                dft=dft,
                season_min=0,
                season_max=0,
                season_window="",
                output_tag=tag,
                label="",
            )
        )
    return specs


def iter_specs(*, tier: str, season_windows: list[str]) -> list[HeroPermSpec]:
    base = _iter_base_specs(tier=tier)
    out: list[HeroPermSpec] = []
    for win in season_windows:
        smin, smax = SEASON_WINDOWS[win]
        for spec in base:
            label = spec.label
            if not label:
                label = _label(
                    roster_x=spec.roster_x,
                    y_draft_mode=spec.y_draft_mode,
                    panel_rows=spec.panel_rows,
                    poolq_binning=spec.poolq_binning,
                    dft=spec.dft,
                    season_window=win,
                )
            elif spec.output_tag == BASELINE["output_tag"]:
                label = f"{label} ({win.replace('_', '–')})"
            else:
                label = _label(
                    roster_x=spec.roster_x,
                    y_draft_mode=spec.y_draft_mode,
                    panel_rows=spec.panel_rows,
                    poolq_binning=spec.poolq_binning,
                    dft=spec.dft,
                    season_window=win,
                )
            out.append(
                HeroPermSpec(
                    y_draft_mode=spec.y_draft_mode,
                    panel_rows=spec.panel_rows,
                    roster_x=spec.roster_x,
                    n_bins=spec.n_bins,
                    poolq_binning=spec.poolq_binning,
                    dft=spec.dft,
                    season_min=smin,
                    season_max=smax,
                    season_window=win,
                    output_tag=spec.output_tag,
                    label=label,
                )
            )
    return out


def _season_slug(season_min: int, season_max: int) -> str:
    return f"{int(season_min) % 100}_{int(season_max) % 100}"


def _find_hero_png(tag: str, season_slug: str) -> Path | None:
    matches = sorted(HERO_OUT.glob(f"HERO_*_{season_slug}_{tag}.png"))
    if not matches:
        matches = sorted(HERO_OUT.glob(f"HERO_*{season_slug}*{tag}.png"))
    return matches[0] if matches else None


def _find_roster_csv(spec: HeroPermSpec, tag: str, season_slug: str) -> Path | None:
    """Hero-panel binned draft rate CSV for ``spec.roster_x`` (never ability ventiles)."""
    xslug = roster_x_slug(spec.roster_x)
    if xslug == "poolq":
        # Filename: PASS_A_binned_draft_rate_poolq_poolq_{core} (poolq inserted twice).
        patterns = [
            f"PASS_A_binned_draft_rate_poolq_poolq_*_{season_slug}_{tag}.csv",
            f"PASS_A_binned_draft_rate_poolq_poolq_*{season_slug}*{tag}.csv",
        ]
    else:
        patterns = [
            f"PASS_A_binned_draft_rate_{xslug}_*_{season_slug}_{tag}.csv",
            f"PASS_A_binned_draft_rate_{xslug}_*{season_slug}*{tag}.csv",
        ]
    for pat in patterns:
        matches = [p for p in sorted(HERO_OUT.glob(pat)) if "ability" not in p.name]
        if matches:
            return matches[0]
    fallback = [
        p
        for p in sorted(HERO_OUT.glob(f"PASS_A_binned_draft_rate_*_{season_slug}_{tag}.csv"))
        if "ability" not in p.name and (xslug != "poolq" or "poolq_poolq" in p.name)
        and (xslug != "poolq_loo" or "poolq_loo" in p.name)
    ]
    return fallback[0] if fallback else None


def _find_lpm_txt(tag: str, season_slug: str) -> Path | None:
    matches = sorted(HERO_OUT.glob(f"PASS_A_lpm_hero_coefficients_*_{season_slug}_{tag}.txt"))
    if not matches:
        matches = sorted(HERO_OUT.glob(f"PASS_A_lpm_hero_coefficients_*{season_slug}*{tag}.txt"))
    return matches[0] if matches else None


def _shape_summary(csv_path: Path | None, *, lpm_path: Path | None = None) -> dict:
    if csv_path is None or not csv_path.is_file():
        return {}
    if "ability" in csv_path.name:
        print(
            f"WARNING: shape summary skipped — CSV is ability ventiles, not roster-x: {csv_path.name}",
            flush=True,
        )
        return {}
    df = pd.read_csv(csv_path)
    if df.empty or "draft_rate" not in df.columns:
        return {}
    peak_idx = int(df["draft_rate"].idxmax())
    peak = df.loc[peak_idx]
    bin0 = df.loc[df["vent"].idxmin()] if "vent" in df.columns else df.iloc[0]
    last = df.iloc[-1]
    b2_path = lpm_path
    if b2_path is None and csv_path is not None:
        core = csv_path.name.removeprefix("PASS_A_binned_draft_rate_")
        for prefix in ("poolq_loo_", "poolq_", "poolq_loo", "poolq"):
            if core.startswith(prefix):
                core = core[len(prefix) :]
                break
        b2_path = csv_path.parent / f"PASS_A_lpm_hero_coefficients_{core.replace('.csv', '.txt')}"
    beta_sq = None
    if b2_path is not None and b2_path.is_file():
        for line in b2_path.read_text(encoding="utf-8").splitlines():
            if "_sq" in line and not line.startswith("#"):
                try:
                    beta_sq = float(line.split()[-1])
                except ValueError:
                    pass
    return {
        "peak_vent": int(peak.get("vent", peak_idx)),
        "peak_rate_pct": round(100 * float(peak["draft_rate"]), 3),
        "bin0_rate_pct": round(100 * float(bin0["draft_rate"]), 3),
        "last_bin_rate_pct": round(100 * float(last["draft_rate"]), 3),
        "bin0_is_peak": bool(int(peak.get("vent", peak_idx)) == int(bin0.get("vent", 0))),
        "beta_sq": beta_sq,
    }


def _manifest_entry(spec: HeroPermSpec, *, png: Path | None, csv_path: Path | None, prov: Path | None) -> dict:
    slug = _season_slug(spec.season_min, spec.season_max)
    lpm_path = _find_lpm_txt(spec.output_tag, slug)
    return {
        "output_tag": spec.output_tag,
        "season_window": spec.season_window,
        "season_min": spec.season_min,
        "season_max": spec.season_max,
        "label": spec.label,
        "spec": asdict(spec),
        "diff_from_baseline": spec.diff_from_baseline(),
        "command": spec.command(),
        "command_one_line": spec.command_one_line(),
        "hero_png": str(png.relative_to(REPO)) if png else None,
        "roster_csv": str(csv_path.relative_to(REPO)) if csv_path else None,
        "roster_csv_xslug": roster_x_slug(spec.roster_x),
        "provenance_json": str(prov.relative_to(REPO)) if prov else None,
        "shape": _shape_summary(csv_path, lpm_path=lpm_path),
    }


def _entry_from_disk(spec: HeroPermSpec) -> dict:
    slug = _season_slug(spec.season_min, spec.season_max)
    png = _find_hero_png(spec.output_tag, slug)
    csv_path = _find_roster_csv(spec, spec.output_tag, slug)
    prov_glob = list(HERO_OUT.glob(f"HERO_*_{slug}_{spec.output_tag}_provenance.json"))
    if not prov_glob:
        prov_glob = list(HERO_OUT.glob(f"HERO_*{slug}*{spec.output_tag}_provenance.json"))
    prov = prov_glob[0] if prov_glob else None
    if png:
        print(f"INDEX · {spec.season_window} · {spec.output_tag} · {png.name}", flush=True)
    else:
        print(f"MISSING PNG · {spec.season_window} · {spec.output_tag}", flush=True)
    return _manifest_entry(spec, png=png, csv_path=csv_path, prov=prov)


def _run_one(spec: HeroPermSpec, *, force: bool) -> dict:
    slug = _season_slug(spec.season_min, spec.season_max)
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
            str(HERO_OUT.relative_to(REPO)),
        ]
        if spec.dft:
            cmd.append("--dft")
        print(f"RUN · {spec.season_window} · {spec.output_tag}", flush=True)
        subprocess.run(cmd, cwd=REPO, check=True)
        png = _find_hero_png(spec.output_tag, slug)

    csv_path = _find_roster_csv(spec, spec.output_tag, slug)
    prov_glob = list(HERO_OUT.glob(f"HERO_*_{slug}_{spec.output_tag}_provenance.json"))
    if not prov_glob:
        prov_glob = list(HERO_OUT.glob(f"HERO_*{slug}*{spec.output_tag}_provenance.json"))
    prov = prov_glob[0] if prov_glob else None
    return _manifest_entry(spec, png=png, csv_path=csv_path, prov=prov)


def _resolve_season_windows(raw: str) -> list[str]:
    key = str(raw).strip().lower()
    if key == "both":
        return ["11_21", "13_21"]
    if key not in SEASON_WINDOWS:
        raise SystemExit(
            f"season-window must be one of {sorted(SEASON_WINDOWS)} or both, got {raw!r}"
        )
    return [key]


def _sync_manifest_counts(manifest: dict) -> None:
    """Keep n_runs / n_specs / complete aligned with runs[] (safe after interrupt)."""
    runs = manifest.get("runs") or []
    n_runs = len(runs)
    n_planned = manifest.get("n_planned")
    if n_planned is None:
        legacy = manifest.get("n_specs")
        n_planned = int(legacy) if legacy is not None else n_runs
    manifest["n_planned"] = int(n_planned)
    manifest["n_runs"] = n_runs
    manifest["n_specs"] = n_runs
    manifest["complete"] = n_runs >= manifest["n_planned"]


def _write_manifest(manifest: dict) -> None:
    _sync_manifest_counts(manifest)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _resolve_run_config(tier: str, season_window_arg: str) -> tuple[str, list[str], str, str]:
    """Return (grid_tier, season_windows, manifest_tier, effective_season_window)."""
    if tier == "real_full":
        if season_window_arg != "11_21":
            print(
                f"Note: --tier real_full forces season-window both (ignoring {season_window_arg!r})",
                flush=True,
            )
        return "full", ["11_21", "13_21"], "real_full", "both"
    return tier, _resolve_season_windows(season_window_arg), tier, season_window_arg


def main() -> None:
    parser = argparse.ArgumentParser(description="HERO permutation sweep → manifest.json")
    parser.add_argument(
        "--tier",
        choices=("core", "extended", "full", "real_full"),
        default="core",
        help=(
            "core=8 (2×2×2); extended=+DFT (16); full=+EW20 (32); "
            "real_full=full×both seasons (64). Baseline always first."
        ),
    )
    parser.add_argument(
        "--season-window",
        choices=("11_21", "13_21", "both"),
        default="11_21",
        help="Season range per run (default 11_21). both = run 11_21 then 13_21 (doubles count).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print specs only; do not run.")
    parser.add_argument("--force", action="store_true", help="Re-run even if PNG exists.")
    parser.add_argument(
        "--repair-manifest",
        action="store_true",
        help="Rebuild manifest from on-disk PNGs/CSVs only (fixes shape/roster_csv; no pass_a).",
    )
    args = parser.parse_args()

    grid_tier, season_windows, manifest_tier, season_window_effective = _resolve_run_config(
        str(args.tier), str(args.season_window)
    )
    specs = iter_specs(tier=grid_tier, season_windows=season_windows)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    HERO_OUT.mkdir(parents=True, exist_ok=True)

    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "tier": manifest_tier,
        "grid_tier": grid_tier,
        "season_window": season_window_effective,
        "season_windows": season_windows,
        "baseline": BASELINE,
        "n_planned": len(specs),
        "n_runs": 0,
        "n_specs": 0,
        "complete": False,
        "runs": [],
    }

    print(
        f"HERO permutation sweep · tier={manifest_tier} · season={season_window_effective} · "
        f"planned={len(specs)}",
        flush=True,
    )
    for i, spec in enumerate(specs, start=1):
        print(f"\n--- [{i}/{len(specs)}] {spec.season_window} · {spec.output_tag} ---", flush=True)
        print(spec.command(), flush=True)
        if args.dry_run:
            continue
        if args.repair_manifest:
            entry = _entry_from_disk(spec)
        else:
            entry = _run_one(spec, force=bool(args.force))
        entry["slide_index"] = i
        manifest["runs"].append(entry)
        _write_manifest(manifest)

    if args.dry_run:
        manifest["runs"] = [
            {
                "slide_index": i + 1,
                "output_tag": s.output_tag,
                "season_window": s.season_window,
                "label": s.label,
                "spec": asdict(s),
                "diff_from_baseline": s.diff_from_baseline(),
                "command": s.command(),
            }
            for i, s in enumerate(specs)
        ]
        _write_manifest(manifest)
        print(f"\nDry-run manifest → {MANIFEST.relative_to(REPO)}", flush=True)
    else:
        _sync_manifest_counts(manifest)
        print(
            f"\nDone · {manifest['n_runs']}/{manifest['n_planned']} runs · "
            f"complete={manifest['complete']} · manifest → {MANIFEST.relative_to(REPO)}",
            flush=True,
        )
        if not manifest["complete"]:
            print(
                "WARNING: sweep interrupted or incomplete — re-run the same tier/season to resume "
                "(existing PNGs are skipped).",
                flush=True,
            )
        print("Build deck: python sports/scripts/build_hero_permutation_slides.py", flush=True)


if __name__ == "__main__":
    main()
