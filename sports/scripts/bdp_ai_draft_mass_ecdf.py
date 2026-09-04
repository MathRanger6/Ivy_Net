#!/usr/bin/env python3
"""BDP — Â draft-mass ECDF for choosing overlay percentile bands.

Dual empirical CDF on pooled PPM z (within season):
  • +DFT panel (F-HERO ecosystem)
  • drafted-only ($Y_{\\mathrm{draft}}=1$) on the same min-minutes filter

Horizontal grid = equal **draft-mass** slices (default 5%).
Vertical lines = **panel top-%** cuts (default F-HERO grid 7, 15, 25, 40).

Run (repo root):
  python sports/scripts/bdp_ai_draft_mass_ecdf.py
  python sports/scripts/bdp_ai_draft_mass_ecdf.py --draft-mass-step 10
  python sports/scripts/bdp_ai_draft_mass_ecdf.py --panel-top-cuts "7,15,25,40,60"
  python sports/scripts/bdp_ai_draft_mass_ecdf.py --bands "0:7,7:15,15:25,25:40"

Outputs (``basic_data_plots/``):
  ``BDP_Ai_draft_mass_ecdf_<spec>_<metric>.png``
  ``BDP_Ai_draft_mass_ecdf_<spec>_<metric>_cuts.csv``
  ``BDP_Ai_draft_mass_ecdf_<spec>_<metric>.json``
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from cct_p2b_ai_band_overlay import (
    DEFAULT_MIN_MINUTES,
    AiTopPctBand,
    apply_top_pct_band,
    parse_bands,
    _perf_cutoffs,
)
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs
from hero_plot_style import PLOT_DPI
from pass_a_congestion_conditional import CctSpec, _get_panel
from pd20_22_campaign_window import activate_from_args, add_window_args, current_window

DEFAULT_DRAFT_MASS_STEP = 5.0
DEFAULT_PANEL_TOP_CUTS = (7.0, 15.0, 25.0, 40.0)
DEFAULT_BANDS = "0:7,7:15,15:25,25:40"

PANEL_COLOR = "#2e75b6"
DRAFT_COLOR = "#ed7d31"
MASS_LINE_COLOR = "#c00000"
PANEL_CUT_COLOR = "#7030a0"


def _plot_ecdf(ax, values: np.ndarray, *, color: str, label: str, lw: float = 2.0) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=lw, label=label)


def _draft_mass_grid(drafted: np.ndarray, step_pct: float) -> pd.DataFrame:
    masses = np.arange(step_pct, 100.0, step_pct)
    rows = []
    for m in masses:
        q = float(np.quantile(drafted, m / 100.0))
        rows.append(
            {
                "row_type": "draft_mass",
                "draft_mass_pct": float(m),
                "z_cut": q,
                "n_drafted_at_or_below": int(np.sum(drafted <= q)),
                "n_drafted_total": int(drafted.size),
            }
        )
    return pd.DataFrame(rows)


def _panel_top_grid(panel_perf: np.ndarray, drafted: np.ndarray, tops: list[float]) -> pd.DataFrame:
    rows = []
    n_draft_total = int(drafted.size)
    for top in tops:
        z = float(np.quantile(panel_perf, 1.0 - top / 100.0))
        n_draft_below = int(np.sum(drafted <= z))
        rows.append(
            {
                "row_type": "panel_top_cut",
                "panel_top_pct": float(top),
                "panel_pct_floor": 100.0 - float(top),
                "z_cut": z,
                "draft_mass_below_pct": 100.0 * n_draft_below / n_draft_total if n_draft_total else float("nan"),
                "n_drafts_below": n_draft_below,
                "n_drafts_total": n_draft_total,
            }
        )
    return pd.DataFrame(rows)


def _band_table(
    panel: pd.DataFrame,
    drafted_total: int,
    bands: list[AiTopPctBand],
    cuts: dict[float, float],
) -> pd.DataFrame:
    rows = []
    for band in bands:
        sliced = apply_top_pct_band(panel, band, cuts)
        y = pd.to_numeric(sliced["Y_draft"], errors="coerce").fillna(0).astype(int)
        n_drafts = int(y.sum())
        rows.append(
            {
                "row_type": "overlay_band",
                "band": band.label,
                "top_lo": band.top_lo,
                "top_hi": band.top_hi,
                "z_cut_outer": cuts[float(band.top_hi)],
                "z_cut_inner": cuts[float(band.top_lo)] if band.top_lo > 0 else float("nan"),
                "band_n": int(len(sliced)),
                "band_drafts": n_drafts,
                "draft_share_of_total_pct": 100.0 * n_drafts / drafted_total if drafted_total else float("nan"),
                "band_draft_rate": n_drafts / len(sliced) if len(sliced) else float("nan"),
            }
        )
    return pd.DataFrame(rows)


def _base_spec(args) -> CctSpec:
    w = current_window()
    return CctSpec(
        season_min=w.season_min,
        season_max=w.season_max,
        min_minutes=float(args.min_minutes),
        min_team_season_games=int(args.min_team_games),
        winsor_lo=0.01,
        winsor_hi=0.99,
        n_bins=16,
        ai_lo=None,
        ai_hi=None,
        ai_top_pct=None,
        perf_metric=str(args.perf_metric).strip().lower(),
        dft=bool(args.dft),
    )


def _output_stem(base: CctSpec) -> str:
    seasons = f"{base.season_min % 100}_{base.season_max % 100}"
    dft = "dft" if base.dft else "full"
    return (
        f"BDP_Ai_draft_mass_ecdf_mg{base.min_team_season_games}_"
        f"min{int(base.min_minutes)}_{seasons}_{dft}_{base.perf_metric}"
    )


def build_figure(
    *,
    panel_perf: np.ndarray,
    drafted_perf: np.ndarray,
    draft_mass_df: pd.DataFrame,
    panel_top_df: pd.DataFrame,
    png: Path,
    spec_label: str,
    perf_metric: str,
    draft_mass_step: float,
    panel_pool_label: str | None = None,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, ax = plt.subplots(figsize=(10.5, 6.2))

    pool_label = panel_pool_label or rf"+DFT panel ($n={panel_perf.size:,}$)"
    _plot_ecdf(
        ax,
        panel_perf,
        color=PANEL_COLOR,
        lw=2.2,
        label=pool_label,
    )
    _plot_ecdf(
        ax,
        drafted_perf,
        color=DRAFT_COLOR,
        lw=2.0,
        label=rf"Drafted $Y_{{\mathrm{{draft}}}}=1$ ($n={drafted_perf.size:,}$)",
    )

    for _, row in draft_mass_df.iterrows():
        m = row["draft_mass_pct"]
        z = row["z_cut"]
        ax.axhline(m / 100.0, color=MASS_LINE_COLOR, ls=":", lw=0.9, alpha=0.55)
        ax.plot(z, m / 100.0, "o", color=MASS_LINE_COLOR, ms=4.5, zorder=5)
        if int(m) % max(int(draft_mass_step * 2), 10) == 0 or m == draft_mass_df["draft_mass_pct"].iloc[-1]:
            ax.annotate(
                f"{int(m)}%",
                xy=(z, m / 100.0),
                xytext=(4, 2),
                textcoords="offset points",
                fontsize=7,
                color=MASS_LINE_COLOR,
            )

    for _, row in panel_top_df.iterrows():
        z = row["z_cut"]
        top = row["panel_top_pct"]
        ax.axvline(z, color=PANEL_CUT_COLOR, ls="--", lw=1.4, alpha=0.85)
        ax.annotate(
            f"top {top:g}%",
            xy=(z, 0.02),
            xytext=(3, 8),
            textcoords="offset points",
            fontsize=7.5,
            color=PANEL_CUT_COLOR,
            rotation=90,
            va="bottom",
        )

    x_lo = float(min(panel_perf.min(), drafted_perf.min()))
    x_hi = float(max(panel_perf.max(), drafted_perf.max()))
    pad = 0.06 * (x_hi - x_lo) if x_hi > x_lo else 0.5
    ax.set_xlim(x_lo - pad, x_hi + pad)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(rf"{perf_metric.upper()} $z$ within season ($\hat{{A}}_i$)")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title(
        rf"BDP — $\hat{{A}}_i$ draft-mass ECDF · {spec_label} · "
        rf"draft grid {draft_mass_step:g}% · panel top cuts",
        fontsize=11,
        pad=10,
    )
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.95)

    note = (
        r"Red dots: equal draft-mass quantiles on $Y_{\mathrm{draft}}=1$. "
        r"Purple dashed: panel top-% cuts (overlay band edges). "
        r"Read orange curve $\rightarrow$ draft mass; blue $\rightarrow$ panel pool."
    )
    fig.text(0.5, 0.01, note, ha="center", va="bottom", fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png.relative_to(REPO)}")


# Reigning data-story panel 4 uses the standard F-HERO draft-mass grid (not band-lock edges).
REIGNING_ECDF_PANEL_TOP_CUTS = DEFAULT_PANEL_TOP_CUTS


def run_reigning_last_ps_ecdf(out_dir: Path) -> Path:
    """Reigning data-story panel 4 — last-ps ALLT with purple overlay band cuts."""
    from pass_a_congestion_conditional import CctSpec, _get_panel

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = "BDP_Ai_draft_mass_ecdf_mg10_min20_09_21_allt_ppm_last_ps"
    out_png = out_dir / f"{stem}.png"
    out_csv = out_dir / f"{stem}_cuts.csv"
    out_json = out_dir / f"{stem}.json"

    base = CctSpec(
        season_min=2009,
        season_max=2021,
        min_minutes=20.0,
        min_team_season_games=10,
        winsor_lo=0.01,
        winsor_hi=0.99,
        n_bins=16,
        ai_lo=None,
        ai_hi=None,
        perf_metric="ppm",
        dft=False,
        y_draft_mode="ever",
        panel_rows="last-ps",
    )
    use = _get_panel(base)
    panel = use.dropna(subset=["perf", "Y_draft"]).copy()
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    drafted = panel.loc[y == 1].copy()
    panel_perf = panel["perf"].to_numpy(dtype=float)
    drafted_perf = drafted["perf"].to_numpy(dtype=float)

    panel_top_cuts = list(REIGNING_ECDF_PANEL_TOP_CUTS)
    tops = {0.0, *panel_top_cuts}
    cuts = _perf_cutoffs(panel, tops)
    draft_mass_df = _draft_mass_grid(drafted_perf, 5.0)
    panel_top_df = _panel_top_grid(panel_perf, drafted_perf, panel_top_cuts)
    band_df = _band_table(panel, int(drafted_perf.size), parse_bands(DEFAULT_BANDS), cuts)
    cuts_df = pd.concat([draft_mass_df, panel_top_df, band_df], ignore_index=True, sort=False)

    build_figure(
        panel_perf=panel_perf,
        drafted_perf=drafted_perf,
        draft_mass_df=draft_mass_df,
        panel_top_df=panel_top_df,
        png=out_png,
        spec_label="mg10 min20 09_21 · ALLT · panel=last-ps · Y=ever",
        perf_metric="ppm",
        draft_mass_step=5.0,
        panel_pool_label=rf"Full panel ($n={panel_perf.size:,}$)",
    )
    cuts_df.to_csv(out_csv, index=False, float_format="%.6g")

    meta = {
        "diagnostic": "bdp_ai_draft_mass_ecdf",
        "date": date.today().isoformat(),
        "panel": "mg10 min20 09_21 · ALLT · panel=last-ps · Y=ever",
        "panel_top_cuts": panel_top_cuts,
        "n_panel": int(panel_perf.size),
        "n_drafted": int(drafted_perf.size),
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Â draft-mass ECDF for band picking.")
    parser.add_argument("--min-minutes", type=float, default=DEFAULT_MIN_MINUTES)
    parser.add_argument("--min-team-games", type=int, default=10, dest="min_team_games")
    parser.add_argument("--perf-metric", default="ppm", choices=("ppm", "bpm", "obpm", "dbpm"))
    parser.add_argument("--dft", action="store_true", default=True)
    parser.add_argument("--no-dft", action="store_false", dest="dft")
    parser.add_argument(
        "--draft-mass-step",
        type=float,
        default=DEFAULT_DRAFT_MASS_STEP,
        help="Draft-mass grid step in percent (default: 5).",
    )
    parser.add_argument(
        "--panel-top-cuts",
        default=",".join(str(x) for x in DEFAULT_PANEL_TOP_CUTS),
        help="Panel top-% cut lines (comma-separated).",
    )
    parser.add_argument(
        "--bands",
        default=DEFAULT_BANDS,
        help="Overlay-style bands for band_table CSV (top_lo:top_hi,...).",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    ensure_hero_dirs()
    base = _base_spec(args)
    panel_top_cuts = [float(x.strip()) for x in args.panel_top_cuts.split(",") if x.strip()]
    bands = parse_bands(args.bands)
    tops = {0.0}
    tops.update(panel_top_cuts)
    for b in bands:
        tops.add(b.top_lo)
        tops.add(b.top_hi)

    pop = "+DFT" if base.dft else "full panel"
    print(
        f"Building panel · mg{base.min_team_season_games} min{base.min_minutes:g} · {pop} · "
        f"{base.perf_metric} …",
        flush=True,
    )
    use = _get_panel(base)
    panel = use.dropna(subset=["perf", "Y_draft"]).copy()
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    drafted = panel.loc[y == 1].copy()
    panel_perf = panel["perf"].to_numpy(dtype=float)
    drafted_perf = drafted["perf"].to_numpy(dtype=float)
    n_drafts_total = int(drafted_perf.size)

    cuts = _perf_cutoffs(panel, tops)
    draft_mass_df = _draft_mass_grid(drafted_perf, float(args.draft_mass_step))
    panel_top_df = _panel_top_grid(panel_perf, drafted_perf, panel_top_cuts)
    band_df = _band_table(panel, n_drafts_total, bands, cuts)

    cuts_df = pd.concat([draft_mass_df, panel_top_df, band_df], ignore_index=True, sort=False)

    stem = _output_stem(base)
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_csv = BASIC_DATA_PLOTS / f"{stem}_cuts.csv"
    out_json = BASIC_DATA_PLOTS / f"{stem}.json"

    spec_label = (
        f"mg{base.min_team_season_games} min{base.min_minutes:g} "
        f"{base.season_min % 100}_{base.season_max % 100} · {pop}"
    )
    build_figure(
        panel_perf=panel_perf,
        drafted_perf=drafted_perf,
        draft_mass_df=draft_mass_df,
        panel_top_df=panel_top_df,
        png=out_png,
        spec_label=spec_label,
        perf_metric=base.perf_metric,
        draft_mass_step=float(args.draft_mass_step),
    )

    cuts_df.to_csv(out_csv, index=False, float_format="%.6g")
    print(f"Wrote {out_csv.relative_to(REPO)}")
    print("\nOverlay bands:")
    print(
        band_df[
            ["band", "band_n", "band_drafts", "draft_share_of_total_pct", "z_cut_outer", "z_cut_inner"]
        ].to_string(index=False)
    )
    print("\nPanel top cuts → draft mass below:")
    print(panel_top_df[["panel_top_pct", "z_cut", "draft_mass_below_pct"]].to_string(index=False))

    meta = {
        "diagnostic": "bdp_ai_draft_mass_ecdf",
        "date": date.today().isoformat(),
        "panel": spec_label,
        "perf_metric": base.perf_metric,
        "min_minutes": base.min_minutes,
        "dft": base.dft,
        "winsor": [base.winsor_lo, base.winsor_hi],
        "draft_mass_step_pct": float(args.draft_mass_step),
        "panel_top_cuts": panel_top_cuts,
        "bands": args.bands,
        "n_panel": int(panel_perf.size),
        "n_drafted": n_drafts_total,
        "K_over_N": n_drafts_total / panel_perf.size if panel_perf.size else float("nan"),
        "png": out_png.name,
        "cuts_csv": out_csv.name,
        "panel_cuts": panel_top_df.to_dict(orient="records"),
        "overlay_bands": band_df.to_dict(orient="records"),
    }
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print("Done.")


if __name__ == "__main__":
    main()
