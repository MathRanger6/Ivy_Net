#!/usr/bin/env python3
"""Tenure Act II — conditional tenure-rate plots (fixed Â, vary dept LOO).

Ports MBB CCT matched-pond + elite-pond LOO twin to PD29 decision cohort.

Run (repo root):
  python tenure/scripts/tenure_pass_a_congestion.py --plot cct \\
    --ai-z-lo 1.0 --ai-z-hi 2.0 --loo-n-bins 8

  python tenure/scripts/tenure_pass_a_congestion.py --plot elite_pond \\
    --ai-top-pct 20 --loo-n-low 3 --loo-n-high 5

  python tenure/scripts/tenure_pass_a_congestion.py --plot all_probes
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
TENURE_PIPELINE = REPO / "tenure" / "tenure_pipeline"
SPORTS_SCRIPTS = REPO / "sports" / "scripts"
SCRIPTS_DIR = REPO / "tenure" / "scripts"
DEFAULT_OUT = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "tenure_sandbox"
    / "act2"
)

sys.path.insert(0, str(TENURE_PIPELINE))
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SPORTS_SCRIPTS))

from decision_hero_prep import prepare_decision_hero_persons  # noqa: E402
from tenure_grain_labels import DECISION, stamp_window_badge  # noqa: E402

SQUID_VENT_16 = (5, 6, 7)
JACKAL_VENT_16 = (13, 14, 15)
SQUID_COLOR = "#2ecc71"
JACKAL_COLOR = "#e67e22"
OTHER_COLOR = "#95a5a6"
TAIL_COLOR = "#e67e22"
MIN_CELL_N_WARN = 5


@dataclass
class TenureAct2Spec:
    ai_lo: float | None = None
    ai_hi: float | None = None
    ai_top_pct: float | None = None
    n_bins: int = 8
    poolq_binning: str = "quantile"

    @property
    def ai_band_label(self) -> str:
        if self.ai_top_pct is not None:
            pct = float(self.ai_top_pct)
            if abs(pct - round(pct)) < 1e-9:
                return f"top {int(round(pct))}%"
            return f"top {pct:g}%"
        if self.ai_lo is None or self.ai_hi is None:
            return "full panel"
        return f"[{self.ai_lo:g}, {self.ai_hi:g}]"

    def apply_ai_band(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.ai_top_pct is not None:
            pct = float(self.ai_top_pct)
            cut = float(df["perf"].quantile(1.0 - pct / 100.0))
            return df.loc[pd.to_numeric(df["perf"], errors="coerce") >= cut].copy()
        if self.ai_lo is None or self.ai_hi is None:
            return df.copy()
        return df.loc[(df["perf"] >= self.ai_lo) & (df["perf"] <= self.ai_hi)].copy()


def _wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return float("nan"), float("nan")
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    margin = z * math.sqrt((p * (1.0 - p) / n + z2 / (4.0 * n * n))) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def _asymmetric_yerr(rate, ci_lo, ci_hi) -> tuple[np.ndarray, np.ndarray]:
    y = np.asarray(rate, dtype=float)
    lo = np.asarray(ci_lo, dtype=float)
    hi = np.asarray(ci_hi, dtype=float)
    return np.maximum(0.0, y - lo), np.maximum(0.0, hi - y)


def _z_slug(z: float) -> str:
    return f"{z:g}".replace(".", "p").replace("-", "m")


def _ai_band_slug(spec: TenureAct2Spec) -> str:
    if spec.ai_top_pct is not None:
        pct = float(spec.ai_top_pct)
        if abs(pct - round(pct)) < 1e-9:
            return f"top{int(round(pct))}"
        return f"top{_z_slug(pct)}"
    if spec.ai_lo is not None and spec.ai_hi is not None:
        return f"z{_z_slug(spec.ai_lo)}_{_z_slug(spec.ai_hi)}"
    return "all"


def _proxy_ventiles(n_bins: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    n = int(n_bins)

    def map_region(lo16: int, hi16: int) -> tuple[int, ...]:
        lo = int(math.floor(lo16 * n / 16))
        hi = int(math.ceil((hi16 + 1) * n / 16)) - 1
        hi = min(hi, n - 1)
        if lo > hi:
            lo = hi
        return tuple(range(lo, hi + 1))

    return map_region(SQUID_VENT_16[0], SQUID_VENT_16[-1]), map_region(
        JACKAL_VENT_16[0], JACKAL_VENT_16[-1]
    )


def _assign_quantile_bins(values: pd.Series, n_bins: int) -> pd.Series:
    s = pd.to_numeric(values, errors="coerce")
    ranks = s.rank(method="first")
    try:
        out = pd.qcut(ranks, q=int(n_bins), labels=False, duplicates="drop")
    except ValueError:
        out = pd.Series(np.nan, index=s.index)
    return out.astype("Int64")


def _equal_width_edges(values: pd.Series, n_bins: int) -> np.ndarray:
    s = pd.to_numeric(values, errors="coerce").dropna()
    if s.empty:
        return np.linspace(0.0, 1.0, int(n_bins) + 1)
    lo, hi = float(s.min()), float(s.max())
    if hi <= lo:
        hi = lo + 1e-6
    return np.linspace(lo, hi, int(n_bins) + 1)


def _piecewise_tail_edges(
    values: pd.Series,
    *,
    n_low: int,
    n_high: int,
    split_q: float = 0.75,
) -> tuple[np.ndarray, float]:
    s = pd.to_numeric(values, errors="coerce").dropna()
    if s.empty:
        edges = np.linspace(0.0, 1.0, int(n_low) + int(n_high) + 1)
        return edges, 0.5
    split = float(s.quantile(float(split_q)))
    lo, hi = float(s.min()), float(s.max())
    if split <= lo:
        split = lo + (hi - lo) * 0.5
    if split >= hi:
        split = lo + (hi - lo) * 0.5
    low_edges = np.linspace(lo, split, int(n_low) + 1)
    high_edges = np.linspace(split, hi, int(n_high) + 1)[1:]
    return np.concatenate([low_edges, high_edges]), split


def _assign_bin_labels(values: pd.Series, edges: np.ndarray) -> pd.Series:
    cut = pd.cut(
        pd.to_numeric(values, errors="coerce"),
        bins=edges,
        labels=False,
        include_lowest=True,
    )
    return pd.Series(cut, index=values.index, dtype="Int64")


def load_tenure_panel(panel_path: Path, career_path: Path) -> tuple[pd.DataFrame, dict]:
    persons, stats = prepare_decision_hero_persons(panel_path, career_path)
    df = pd.DataFrame(persons)
    df = df.dropna(subset=["own_career_rate", "dept_loo_career_rate"]).copy()
    if df.empty:
        raise SystemExit("No persons with both own career rate and dept LOO.")

    def _z(s: pd.Series) -> pd.Series:
        mu = float(s.mean())
        sd = float(s.std())
        if sd <= 0:
            return pd.Series(0.0, index=s.index)
        return (s - mu) / sd

    df["perf"] = df.groupby("decision_year", observed=True)["own_career_rate"].transform(_z)
    df["dept_loo"] = pd.to_numeric(df["dept_loo_career_rate"], errors="coerce")
    df["Y_tenure"] = df["tenure"].astype(int)
    return df, stats


def _outcome_table(band: pd.DataFrame, *, vent_col: str = "vent") -> pd.DataFrame:
    rows = []
    for vent, grp in band.dropna(subset=[vent_col]).groupby(vent_col, observed=True):
        n = int(len(grp))
        events = int(pd.to_numeric(grp["Y_tenure"], errors="coerce").fillna(0).sum())
        rate = events / n if n else float("nan")
        lo, hi = _wilson_ci(events, n)
        rows.append(
            {
                "vent": int(vent),
                "bin_display": int(vent) + 1,
                "n": n,
                "tenured": events,
                "tenure_rate": rate,
                "ci_lo": lo,
                "ci_hi": hi,
                "dept_loo_mean": float(grp["dept_loo"].mean()),
                "dept_loo_median": float(grp["dept_loo"].median()),
                "perf_mean": float(grp["perf"].mean()),
                "thin_cell": n < MIN_CELL_N_WARN,
            }
        )
    return pd.DataFrame(rows).sort_values("vent").reset_index(drop=True)


def _matched_pond_table(df: pd.DataFrame, spec: TenureAct2Spec) -> tuple[pd.DataFrame, pd.DataFrame]:
    band = df.dropna(subset=["perf", "dept_loo", "Y_tenure"]).copy()
    band = spec.apply_ai_band(band)
    band["vent"] = _assign_quantile_bins(band["dept_loo"], spec.n_bins)
    tbl = _outcome_table(band)
    return band, tbl


def _pool_summary(tbl: pd.DataFrame, vents: tuple[int, ...], label: str) -> dict:
    sub = tbl.loc[tbl["vent"].isin(vents)]
    n = int(sub["n"].sum())
    events = int(sub["tenured"].sum())
    rate = events / n if n else float("nan")
    lo, hi = _wilson_ci(events, n)
    return {
        "label": label,
        "ventiles_0idx": list(vents),
        "bins_1idx": [v + 1 for v in vents],
        "n": n,
        "tenured": events,
        "tenure_rate": rate,
        "ci_lo": lo,
        "ci_hi": hi,
    }


def _knee_summary(tbl: pd.DataFrame, *, binning_meta: dict | None = None) -> dict:
    if tbl.empty:
        return {"alex_downturn_visible": False}
    meta = binning_meta or {}
    n = len(tbl)
    if meta.get("mode") == "piecewise_tail":
        n_low = max(1, int(meta.get("n_low_bins", n // 2)))
        plateau = tbl.iloc[:n_low]
        tail = tbl.iloc[-3:]
    else:
        n_plateau = max(1, n // 2)
        plateau = tbl.iloc[:n_plateau]
        tail = tbl.iloc[max(0, n - 3) :]
    plateau_rate = float(plateau["tenure_rate"].mean())
    tail_rate = float(tail["tenure_rate"].mean())
    last_rate = float(tbl.iloc[-1]["tenure_rate"])
    last_n = int(tbl.iloc[-1]["n"])
    return {
        "plateau_mean_tenure_rate": plateau_rate,
        "tail_mean_tenure_rate": tail_rate,
        "last_bin_tenure_rate": last_rate,
        "last_bin_n": last_n,
        "alex_downturn_visible": bool(tail_rate < plateau_rate or last_rate < plateau_rate),
    }


def _loo_knbins_table(
    df: pd.DataFrame,
    spec: TenureAct2Spec,
    *,
    axis_binning: str,
    n_bins: int,
    n_low: int,
    n_high: int,
    tail_split_q: float,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, dict]:
    band = df.dropna(subset=["perf", "dept_loo", "Y_tenure"]).copy()
    band = spec.apply_ai_band(band)
    mode = str(axis_binning).strip().lower()
    if mode == "piecewise_tail":
        edges, split_loo = _piecewise_tail_edges(
            band["dept_loo"],
            n_low=int(n_low),
            n_high=int(n_high),
            split_q=float(tail_split_q),
        )
        binning_meta = {
            "mode": "piecewise_tail",
            "n_low_bins": int(n_low),
            "n_high_bins": int(n_high),
            "tail_split_quantile": float(tail_split_q),
            "tail_split_dept_loo": split_loo,
        }
    else:
        edges = _equal_width_edges(band["dept_loo"], int(n_bins))
        split_loo = float("nan")
        binning_meta = {"mode": "equal_width", "n_bins": int(n_bins)}

    band["vent"] = _assign_bin_labels(band["dept_loo"], edges)
    n_low_bins = int(n_low) if mode == "piecewise_tail" else None
    rows = []
    for vent, grp in band.dropna(subset=["vent"]).groupby("vent", observed=True):
        v = int(vent)
        n = int(len(grp))
        events = int(grp["Y_tenure"].sum())
        rate = events / n if n else float("nan")
        lo, hi = _wilson_ci(events, n)
        elo, ehi = float(edges[v]), float(edges[v + 1])
        is_tail = v >= n_low_bins if n_low_bins is not None else False
        rows.append(
            {
                "vent": v,
                "bin_display": v + 1,
                "n": n,
                "tenured": events,
                "tenure_rate": rate,
                "ci_lo": lo,
                "ci_hi": hi,
                "edge_lo": elo,
                "edge_hi": ehi,
                "dept_loo_mean": float(grp["dept_loo"].mean()),
                "high_loo_tail": is_tail,
                "thin_cell": n < MIN_CELL_N_WARN,
            }
        )
    tbl = pd.DataFrame(rows).sort_values("vent").reset_index(drop=True)
    binning_meta["dept_loo_range"] = {"lo": float(edges[0]), "hi": float(edges[-1])}
    return band, tbl, edges, binning_meta


def _configure_mathtext() -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()


def plot_cct_matched_pond(
    spec: TenureAct2Spec,
    tbl: pd.DataFrame,
    band: pd.DataFrame,
    out_png: Path,
) -> dict:
    from hero_plot_style import PLOT_DPI, annotate_bar_n, finalize_bar_figure, set_wrapped_ax_title
    from plot_provenance import hero_bin_label

    _configure_mathtext()
    squid_vents, jackal_vents = _proxy_ventiles(spec.n_bins)
    squid = _pool_summary(tbl, squid_vents, "Squid proxy (mid pond)")
    jackal = _pool_summary(tbl, jackal_vents, "Jackal proxy (top pond)")
    cct_holds = squid["tenure_rate"] > jackal["tenure_rate"]

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    x = tbl["bin_display"].to_numpy(dtype=float)
    y = tbl["tenure_rate"].to_numpy(dtype=float)
    yerr_lo, yerr_hi = _asymmetric_yerr(y, tbl["ci_lo"], tbl["ci_hi"])
    counts = tbl["n"].to_numpy(dtype=int)
    colors = [
        SQUID_COLOR if int(v) in squid_vents else JACKAL_COLOR if int(v) in jackal_vents else OTHER_COLOR
        for v in tbl["vent"]
    ]
    ax.bar(x, y, color=colors, edgecolor="white", alpha=0.92, width=0.85)
    ax.errorbar(x, y, yerr=[yerr_lo, yerr_hi], fmt="none", ecolor="0.25", capsize=2, linewidth=0.8)
    annotate_bar_n(ax, x, y, counts, colors)

    bin_badge = hero_bin_label(poolq_binning=spec.poolq_binning, n_bins=spec.n_bins)
    ax.set_xlabel(rf"Dept pond LOO bin · {bin_badge} ($1$ = lowest pond)", fontsize=10, labelpad=4)
    ax.set_ylabel(r"Mean $Y_{\mathrm{tenure}}$ (resolved)", fontsize=10)
    ax.set_xticks(x)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    stamp_window_badge(ax, DECISION, corner="upper_right")

    compare = (
        f"Squid: {100*squid['tenure_rate']:.1f}% (n={squid['n']:,})\n"
        f"Jackal: {100*jackal['tenure_rate']:.1f}% (n={jackal['n']:,})\n"
        f"CCT: {'YES' if cct_holds else 'NO'}"
    )
    ax.text(0.02, 0.98, compare, transform=ax.transAxes, fontsize=8, va="top", family="monospace")
    ax.legend(
        handles=[
            mpatches.Patch(facecolor=SQUID_COLOR, edgecolor="white", label="Squid (mid pond)"),
            mpatches.Patch(facecolor=JACKAL_COLOR, edgecolor="white", label="Jackal (top pond)"),
            mpatches.Patch(facecolor=OTHER_COLOR, edgecolor="white", label="Other bins"),
        ],
        loc="upper right",
        fontsize=8,
        framealpha=0.92,
    )

    set_wrapped_ax_title(
        ax,
        [
            r"CCT — tenure rate at fixed Alex $\hat{A}$ · PD29 decision cohort",
            rf"Â z band {spec.ai_band_label} · {bin_badge} on dept pond LOO",
        ],
    )
    finalize_bar_figure(
        fig,
        [
            f"Band n={len(band):,} · tenured={int(band['Y_tenure'].sum()):,} · Wilson CIs · bar labels = n",
            f"Within-year z on pubs_per_career_year · {date.today().isoformat()}",
        ],
    )
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=PLOT_DPI, facecolor="white")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    return {"squid": squid, "jackal": jackal, "cct": cct_holds}


def plot_elite_pond_loo(
    spec: TenureAct2Spec,
    tbl: pd.DataFrame,
    band: pd.DataFrame,
    out_png: Path,
    *,
    binning_meta: dict,
    knee: dict,
) -> None:
    from hero_plot_style import PLOT_DPI, annotate_bar_n, finalize_bar_figure, set_wrapped_ax_title
    from plot_provenance import fhero_bin_label

    _configure_mathtext()
    n_low = int(binning_meta.get("n_low_bins", 3))
    n_high = int(binning_meta.get("n_high_bins", 5))
    bin_badge = fhero_bin_label(
        tj_binning=binning_meta.get("mode", "piecewise_tail"),
        tj_n_low=n_low,
        tj_n_high=n_high,
        axis="dept LOO",
    )

    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    x = tbl["bin_display"].to_numpy(dtype=float)
    y = tbl["tenure_rate"].to_numpy(dtype=float)
    yerr_lo, yerr_hi = _asymmetric_yerr(y, tbl["ci_lo"], tbl["ci_hi"])
    counts = tbl["n"].to_numpy(dtype=int)
    colors = [TAIL_COLOR if bool(r["high_loo_tail"]) else OTHER_COLOR for _, r in tbl.iterrows()]

    ax.bar(x, y, color=colors, edgecolor="white", alpha=0.92, width=0.85)
    ax.errorbar(x, y, yerr=[yerr_lo, yerr_hi], fmt="none", ecolor="0.25", capsize=2, linewidth=0.8)
    annotate_bar_n(ax, x, y, counts, colors)
    ax.set_xlabel(rf"Dept pond LOO bin · {bin_badge}", fontsize=10, labelpad=4)
    ax.set_ylabel(r"Mean $Y_{\mathrm{tenure}}$ (resolved)", fontsize=10)
    ax.set_xticks(x)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    stamp_window_badge(ax, DECISION, corner="upper_right")

    compare = (
        f"Plateau (low/mid): {100*knee['plateau_mean_tenure_rate']:.1f}%\n"
        f"Tail (last 3 bins): {100*knee['tail_mean_tenure_rate']:.1f}%\n"
        f"Last bin: {100*knee['last_bin_tenure_rate']:.1f}% (n={knee['last_bin_n']:,})\n"
        f"Downturn: {'YES' if knee['alex_downturn_visible'] else 'NO'}"
    )
    ax.text(0.02, 0.98, compare, transform=ax.transAxes, fontsize=8, va="top", family="monospace")
    ax.legend(
        handles=[
            mpatches.Patch(facecolor=OTHER_COLOR, edgecolor="white", label="Coarse dept LOO bins"),
            mpatches.Patch(facecolor=TAIL_COLOR, edgecolor="white", label="Fine tail dept LOO bins"),
        ],
        loc="upper right",
        fontsize=8,
        framealpha=0.92,
    )

    set_wrapped_ax_title(
        ax,
        [
            r"Elite pond LOO — tenure rate at fixed $\hat{A}_i$ · PD29",
            rf"Â gate {spec.ai_band_label} · {bin_badge}",
        ],
    )
    loo_rng = binning_meta.get("dept_loo_range", {})
    finalize_bar_figure(
        fig,
        [
            (
                f"Band n={len(band):,} · tenured={int(band['Y_tenure'].sum()):,} · "
                f"dept LOO [{loo_rng.get('lo', 0):.3g}, {loo_rng.get('hi', 0):.3g}]"
            ),
            f"Within-year z on pubs_per_career_year · {date.today().isoformat()}",
        ],
    )
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=PLOT_DPI, facecolor="white")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")


def run_cct(
    df: pd.DataFrame,
    spec: TenureAct2Spec,
    out_dir: Path,
) -> Path:
    if spec.ai_lo is None or spec.ai_hi is None:
        raise SystemExit("CCT requires --ai-z-lo and --ai-z-hi.")
    stem = (
        f"CCT_tenure_rate_ai_band_dept_loo_pd29_{_ai_band_slug(spec)}_"
        f"q{spec.n_bins}"
    )
    out_png = out_dir / f"{stem}.png"
    out_json = out_dir / f"{stem}.json"
    out_csv = out_dir / f"{stem}_dept_loo_bins.csv"

    band, tbl = _matched_pond_table(df, spec)
    if tbl.empty:
        raise SystemExit("No rows in matched Â band for CCT.")

    summary = plot_cct_matched_pond(spec, tbl, band, out_png)
    tbl.to_csv(out_csv, index=False, float_format="%.6g")
    print(f"Wrote {out_csv.relative_to(REPO)}")

    meta = {
        "diagnostic": "tenure_cct_matched_pond_pd29",
        "date": date.today().isoformat(),
        "plot": "cct",
        "ai_lo": spec.ai_lo,
        "ai_hi": spec.ai_hi,
        "ai_band_label": spec.ai_band_label,
        "n_bins": spec.n_bins,
        "band_n": int(len(band)),
        "band_tenured": int(band["Y_tenure"].sum()),
        "squid_proxy": summary["squid"],
        "jackal_proxy": summary["jackal"],
        "cct_signature_squid_gt_jackal": bool(summary["cct"]),
        "bins": tbl.to_dict(orient="records"),
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print(
        f"  Squid {100*summary['squid']['tenure_rate']:.1f}% vs "
        f"Jackal {100*summary['jackal']['tenure_rate']:.1f}% · "
        f"CCT={'YES' if summary['cct'] else 'NO'}"
    )
    return out_png


def run_elite_pond(
    df: pd.DataFrame,
    spec: TenureAct2Spec,
    out_dir: Path,
    *,
    axis_binning: str = "piecewise_tail",
    n_bins: int = 24,
    n_low: int = 3,
    n_high: int = 5,
    tail_split_q: float = 0.75,
) -> Path:
    if spec.ai_top_pct is None:
        raise SystemExit("Elite pond requires --ai-top-pct.")
    from plot_provenance import fhero_bin_slug

    bin_slug = fhero_bin_slug(tj_binning=axis_binning, tj_n_low=n_low, tj_n_high=n_high, tj_n_bins=n_bins)
    stem = f"ELITE_pond_loo_{bin_slug}_pd29_{_ai_band_slug(spec)}"
    out_png = out_dir / f"{stem}.png"
    out_json = out_dir / f"{stem}.json"
    out_csv = out_dir / f"{stem}_dept_loo_bins.csv"

    band, tbl, edges, binning_meta = _loo_knbins_table(
        df,
        spec,
        axis_binning=axis_binning,
        n_bins=n_bins,
        n_low=n_low,
        n_high=n_high,
        tail_split_q=tail_split_q,
    )
    if tbl.empty:
        raise SystemExit("No rows in elite Â band for LOO twin.")

    knee = _knee_summary(tbl, binning_meta=binning_meta)
    plot_elite_pond_loo(spec, tbl, band, out_png, binning_meta=binning_meta, knee=knee)
    tbl.to_csv(out_csv, index=False, float_format="%.6g")
    print(f"Wrote {out_csv.relative_to(REPO)}")

    meta = {
        "diagnostic": "tenure_elite_pond_loo_pd29",
        "date": date.today().isoformat(),
        "plot": "elite_pond",
        "ai_top_pct": spec.ai_top_pct,
        "ai_band_label": spec.ai_band_label,
        "binning": binning_meta,
        "bin_edges": [float(e) for e in edges],
        "band_n": int(len(band)),
        "band_tenured": int(band["Y_tenure"].sum()),
        "knee": knee,
        "bins": tbl.to_dict(orient="records"),
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print(
        f"  Plateau {100*knee['plateau_mean_tenure_rate']:.1f}% → "
        f"tail {100*knee['tail_mean_tenure_rate']:.1f}% · "
        f"downturn={'YES' if knee['alex_downturn_visible'] else 'NO'}"
    )
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Tenure Act II conditional plots (PD29)")
    parser.add_argument("--input", type=Path, default=TENURE_PIPELINE / "faculty_panel_with_pools.jsonl")
    parser.add_argument("--career", type=Path, default=TENURE_PIPELINE / "author_year_career_master.jsonl")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--plot",
        choices=("cct", "elite_pond", "all_probes"),
        required=True,
    )
    parser.add_argument("--ai-z-lo", type=float, default=None)
    parser.add_argument("--ai-z-hi", type=float, default=None)
    parser.add_argument("--ai-top-pct", type=float, default=None)
    parser.add_argument("--loo-n-bins", type=int, default=8)
    parser.add_argument("--loo-n-low", type=int, default=3)
    parser.add_argument("--loo-n-high", type=int, default=5)
    parser.add_argument("--tail-split-q", type=float, default=0.75)
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    if not args.career.is_file():
        raise SystemExit(f"Career master not found: {args.career}")

    df, prep_stats = load_tenure_panel(args.input, args.career)
    print(
        f"Panel: {len(df):,} with Â + dept LOO · "
        f"tenured={int(df['Y_tenure'].sum()):,} · "
        f"cohort resolved={prep_stats.get('n_cohort')}"
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.plot in ("cct", "all_probes"):
        z_lo = args.ai_z_lo if args.ai_z_lo is not None else 1.0
        z_hi = args.ai_z_hi if args.ai_z_hi is not None else 2.0
        run_cct(
            df,
            TenureAct2Spec(ai_lo=z_lo, ai_hi=z_hi, n_bins=args.loo_n_bins),
            args.out_dir,
        )

    if args.plot in ("elite_pond", "all_probes"):
        top = args.ai_top_pct if args.ai_top_pct is not None else 20.0
        run_elite_pond(
            df,
            TenureAct2Spec(ai_top_pct=top),
            args.out_dir,
            n_low=args.loo_n_low,
            n_high=args.loo_n_high,
            tail_split_q=args.tail_split_q,
        )

    print("Done.")


if __name__ == "__main__":
    main()
