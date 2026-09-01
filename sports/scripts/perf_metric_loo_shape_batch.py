#!/usr/bin/env python3
"""Disposable batch — reigning LOO porch shape across perf metrics (COMPASS gate).

For each perf key: P(Y=1) vs poolq_LOO (EW16, last-ps) + quadratic LPM β₂ on the same
porch as ``reigning_hero/``. Flags monotone vs non-monotone; **ignore H_sort for promotion**.

Outputs under ``sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/loo_shape/``.

Run (repo root):
  export PYTHONPATH="sports"
  python3 sports/scripts/perf_metric_loo_shape_batch.py
  python3 sports/scripts/perf_metric_loo_shape_batch.py --metrics ppm bpm efg_pct
  python3 sports/scripts/perf_metric_loo_shape_batch.py --no-plots
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from bdp_ai_tj_distributions import BdpSpec, parse_bdp_spec
from bdp_reigning_loo_plots import (
    N_BINS_EW,
    WINSOR,
    _loo_ventile_table,
    _prepare_last_ps,
    _quadratic_lpm_coef,
    run_draft_rate_vs_loo,
)
from hero_gallery_paths import (
    PERF_METRIC_RHO_EDA,
    PERF_METRIC_RHO_EDA_H_SORT,
    PERF_METRIC_RHO_EDA_LOO,
    ensure_hero_dirs,
)
from sports_pipeline.perf_metric import resolve_perf_metric

REIGNING_SPEC = "mg10 min20 09_21"
DEFAULT_METRICS = (
    "ppm",
    "fg_pct",
    "efg_pct",
    "ts_pct_box",
    "per",
    "bpm",
    "tspct",
    "ws",
    "minutes",
)

LPM_CONCAVE_EPS = 0.005  # |β₂| below this ≈ flat (reigning PPM ~ +0.0017)
MONOTONE_EPS = 1e-4
TAIL_DROP_MIN = 0.005


def _bin_shape_label(tbl: pd.DataFrame) -> dict:
    """Classify draft-rate vs poolq_LOO bin curve (EW16 ventiles)."""
    y = tbl["draft_rate"].to_numpy(dtype=float)
    n = len(y)
    if n < 3:
        return {
            "bin_shape": "insufficient_bins",
            "strictly_monotone_increasing": False,
            "peak_bin": None,
            "tail_drop": False,
        }

    diffs = np.diff(y)
    strictly_up = bool(np.all(diffs >= -MONOTONE_EPS))
    peak_idx = int(np.argmax(y))
    left = float(y[0])
    right = float(y[-1])
    peak = float(y[peak_idx])
    peak_interior = 0 < peak_idx < n - 1
    endpoints_below_peak = peak > left + MONOTONE_EPS and peak > right + MONOTONE_EPS
    tail_drop = peak_idx < n - 1 and (peak - right) >= TAIL_DROP_MIN

    if peak_interior and endpoints_below_peak:
        bin_shape = "inverted_u_like"
    elif peak_idx == n - 1 and strictly_up:
        bin_shape = "monotone_increasing"
    elif peak_idx == 0:
        bin_shape = "monotone_decreasing"
    elif tail_drop:
        bin_shape = "tail_drop"
    else:
        bin_shape = "other"

    return {
        "bin_shape": bin_shape,
        "strictly_monotone_increasing": strictly_up,
        "peak_bin": peak_idx,
        "peak_rate": peak,
        "left_rate": left,
        "right_rate": right,
        "tail_drop": tail_drop,
    }


def _lpm_shape(b2: float) -> str:
    if b2 < -LPM_CONCAVE_EPS:
        return "concave"
    if b2 > LPM_CONCAVE_EPS:
        return "convex"
    return "flat"


def _promotion_verdict(
    *,
    bin_shape: str,
    strictly_monotone_increasing: bool,
    lpm_shape: str,
    lpm_beta2: float,
    tail_drop: bool,
) -> tuple[str, str]:
    """COMPASS gate: LPM concavity primary; bin geometry confirmatory."""
    lpm_concave = lpm_beta2 < -LPM_CONCAVE_EPS
    lpm_convex = lpm_beta2 > LPM_CONCAVE_EPS

    if strictly_monotone_increasing or lpm_convex:
        if strictly_monotone_increasing and lpm_convex:
            return "fail", "strictly monotone ↑ + convex LPM β₂"
        if strictly_monotone_increasing:
            return "fail", "strictly monotone ↑"
        return "fail", f"convex LPM β₂ ({lpm_beta2:+.5f})"

    if lpm_concave:
        extra = f"; bin={bin_shape}"
        if tail_drop:
            extra += " + tail drop"
        return "pass", f"concave LPM β₂{extra}"

    return "marginal", f"flat LPM β₂ ({lpm_beta2:+.5f}); bin={bin_shape} (non-monotone but not concave)"


def _ability_loo_corr(panel: pd.DataFrame) -> float | None:
    work = panel.dropna(subset=["perf", "poolq_loo"]).copy()
    if work.empty:
        return None
    a = pd.to_numeric(work["perf"], errors="coerce").to_numpy(dtype=float)
    q = pd.to_numeric(work["poolq_loo"], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(a) & np.isfinite(q)
    if mask.sum() < 3:
        return None
    return float(np.corrcoef(a[mask], q[mask])[0, 1])


def _load_h_sort_map() -> dict[str, float]:
    path = PERF_METRIC_RHO_EDA_H_SORT / "Hsort_ladder_summary_2009_2021.csv"
    if not path.is_file():
        return {}
    df = pd.read_csv(path)
    if "perf_metric" not in df.columns or "H_sort_pooled" not in df.columns:
        return {}
    return dict(zip(df["perf_metric"].astype(str), df["H_sort_pooled"].astype(float)))


def analyze_metric(
    spec: BdpSpec,
    perf_metric: str,
    *,
    h_sort_map: dict[str, float],
) -> dict:
    resolve_perf_metric(perf_metric)
    panel = _prepare_last_ps(spec, perf_metric)
    tbl = _loo_ventile_table(panel, n_bins=N_BINS_EW)
    coef = _quadratic_lpm_coef(panel)
    b2 = float(coef["beta_poolq_loo_sq"])
    b1 = float(coef["beta_poolq_loo"])
    shape = _bin_shape_label(tbl)
    lpm = _lpm_shape(b2)
    verdict, verdict_reason = _promotion_verdict(
        bin_shape=shape["bin_shape"],
        strictly_monotone_increasing=shape["strictly_monotone_increasing"],
        lpm_shape=lpm,
        lpm_beta2=b2,
        tail_drop=bool(shape["tail_drop"]),
    )
    corr = _ability_loo_corr(panel)
    h_sort = h_sort_map.get(perf_metric)

    return {
        "perf_metric": perf_metric,
        "n_panel_rows": int(len(panel)),
        "n_binned_rows": int(tbl["n"].sum()),
        "lpm_beta1": b1,
        "lpm_beta2": b2,
        "lpm_shape": lpm,
        "bin_shape": shape["bin_shape"],
        "strictly_monotone_increasing": shape["strictly_monotone_increasing"],
        "tail_drop": shape["tail_drop"],
        "peak_bin": shape["peak_bin"],
        "peak_rate": shape.get("peak_rate"),
        "left_rate": shape.get("left_rate"),
        "right_rate": shape.get("right_rate"),
        "ability_loo_corr": corr,
        "H_sort_pooled": h_sort,
        "promotion_verdict": verdict,
        "promotion_reason": verdict_reason,
        "panel": panel,
        "bins": tbl,
        "lpm_coef": coef,
    }


def write_loo_shape_report(df: pd.DataFrame, spec: BdpSpec, out: Path) -> None:
    lines = [
        "# LOO-shape batch — perf-metric promotion gate (disposable EDA)",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Porch:** reigning hero lock · `{REIGNING_SPEC}` · last-ps · EW{N_BINS_EW} · "
        f"winsor {int(WINSOR[0]*100)}–{int(WINSOR[1]*100)} on poolq_LOO",
        "",
        "**COMPASS rule:** do not promote on sorting index (H_sort) alone. "
        "**Pass** = concave LPM β₂ (< 0). **Fail** = strictly monotone ↑ or convex β₂. "
        "**Marginal** = flat β₂ (includes reigning PPM baseline).",
        "",
        "## Summary",
        "",
        "| Rank | Key | LPM β₂ | LPM | Bin shape | Monotone ↑? | Â–LOO r | H_sort | Verdict |",
        "|------|-----|--------|-----|-----------|-------------|---------|--------|---------|",
    ]
    verdict_order = {"pass": 0, "marginal": 1, "fail": 2}
    rank_df = df.assign(_v=df["promotion_verdict"].map(verdict_order)).sort_values(
        ["_v", "lpm_beta2"], ascending=[True, True]
    )
    for rank, row in enumerate(rank_df.itertuples(index=False), start=1):
        hs = f"{row.H_sort_pooled:.4f}" if row.H_sort_pooled == row.H_sort_pooled else "—"
        corr = f"{row.ability_loo_corr:.3f}" if row.ability_loo_corr == row.ability_loo_corr else "—"
        mono = "yes" if row.strictly_monotone_increasing else "no"
        lines.append(
            f"| {rank} | `{row.perf_metric}` | {row.lpm_beta2:+.5f} | {row.lpm_shape} | "
            f"{row.bin_shape} | {mono} | {corr} | {hs} | **{row.promotion_verdict}** |"
        )

    lines.extend(
        [
            "",
            "## Verdict key",
            "",
            "- **pass** — concave LPM β₂ (< 0); candidate to inspect (not auto-promote)",
            "- **marginal** — flat LPM β₂ ≈ 0 (reigning PPM lives here)",
            "- **fail** — strictly monotone ↑ and/or convex LPM β₂ (> 0)",
            "",
            "## Points per minute (PPM) baseline",
            "",
        ]
    )
    ppm = df.loc[df["perf_metric"] == "ppm"]
    if not ppm.empty:
        p = ppm.iloc[0]
        lines.append(
            f"- LPM β₂ = {p['lpm_beta2']:+.5f} ({p['lpm_shape']}); bin shape = {p['bin_shape']}; "
            f"verdict = **{p['promotion_verdict']}** ({p['promotion_reason']})."
        )
        lines.append("- Reigning lock reference: β₂ ≈ +0.00172, shape tags “robust tail drop.”")

    lines.extend(
        [
            "",
            "## Per-metric artifacts",
            "",
            "PNG + bin CSV under `loo_shape/{metric}/`.",
            "",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO)}", flush=True)


def run_batch(
    metrics: list[str],
    *,
    write_plots: bool = True,
    prefix: str = "DISPO",
) -> pd.DataFrame:
    ensure_hero_dirs()
    out_root = PERF_METRIC_RHO_EDA_LOO
    out_root.mkdir(parents=True, exist_ok=True)
    spec = parse_bdp_spec(REIGNING_SPEC)
    h_sort_map = _load_h_sort_map()

    rows: list[dict] = []
    for metric in metrics:
        print(f"\n=== LOO shape · {metric} ===", flush=True)
        result = analyze_metric(spec, metric, h_sort_map=h_sort_map)
        metric_dir = out_root / metric
        metric_dir.mkdir(parents=True, exist_ok=True)

        bins_path = metric_dir / f"bins_ew{N_BINS_EW}.csv"
        result["bins"].to_csv(bins_path, index=False)

        png_name = None
        if write_plots:
            run_draft_rate_vs_loo(
                spec,
                perf_metric=metric,
                out_png=metric_dir / "draft_rate_poolq_loo.png",
                out_meta_dir=metric_dir,
                out_meta_dir_csv=metric_dir,
                prefix=prefix,
                n_bins=N_BINS_EW,
            )
            png_name = next(metric_dir.glob(f"*{metric}_lastps.png"), None)
            png_name = png_name.name if png_name else None

        row = {k: v for k, v in result.items() if k not in {"panel", "bins", "lpm_coef"}}
        row["bins_csv"] = bins_path.name
        row["png"] = png_name
        rows.append(row)
        print(
            f"  n={row['n_panel_rows']:,} β₂={row['lpm_beta2']:+.5f} "
            f"bin={row['bin_shape']} verdict={row['promotion_verdict']}",
            flush=True,
        )

    df = pd.DataFrame(rows)
    summary_path = out_root / f"loo_shape_summary_{spec.season_min}_{spec.season_max}.csv"
    df.to_csv(summary_path, index=False)
    print(f"\nWrote {summary_path.relative_to(REPO)}", flush=True)

    report_path = out_root / "LOO_SHAPE_REPORT.md"
    write_loo_shape_report(df, spec, report_path)

    manifest = {
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "reigning_spec": REIGNING_SPEC,
        "panel_rows": "last-ps",
        "poolq_binning": "equal_width",
        "n_bins": N_BINS_EW,
        "poolq_winsor": list(WINSOR),
        "metrics": metrics,
        "write_plots": write_plots,
        "summary_csv": summary_path.name,
        "report_md": report_path.name,
    }
    manifest_path = out_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path.relative_to(REPO)}", flush=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="LOO-shape batch across perf metrics (disposable).")
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=list(DEFAULT_METRICS),
        help=f"Perf keys (default: {' '.join(DEFAULT_METRICS)})",
    )
    parser.add_argument("--no-plots", action="store_true", help="Summary CSV only (faster).")
    args = parser.parse_args()
    run_batch(args.metrics, write_plots=not args.no_plots)


if __name__ == "__main__":
    main()
