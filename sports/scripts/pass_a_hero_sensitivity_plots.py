#!/usr/bin/env python3
"""Pass A hero sensitivity — labeled PNG gallery (POST-QC tail-drop search).

Generates one bar chart per spec with an on-figure caption explaining what we tried.
Companion JSON/CSV written alongside PNGs.

Run (repo root):
  python sports/scripts/pass_a_hero_sensitivity_plots.py
  python sports/scripts/pass_a_hero_sensitivity_plots.py --quick   # 8 key specs only

Outputs:
  3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/sensitivity/
    PASS_A_sensitivity_<slug>.png
    PASS_A_hero_sensitivity_post_qc.json
    PASS_A_hero_sensitivity_index.csv
    README.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import PASS_A, ensure_hero_dirs
from pd22_slide_common import MIN_TEAM_SEASON_GAMES

from sports_pipeline import paths
from sports_pipeline.config import PipelineConfig
from sports_pipeline import panel_build, panel_rebuild
from sports_pipeline.panel_build import assign_poolq_bin_labels

SENS_DIR = PASS_A / "sensitivity"
JSON_OUT = PASS_A / "PASS_A_hero_sensitivity_post_qc.json"
CSV_OUT = PASS_A / "PASS_A_hero_sensitivity_index.csv"
README_OUT = SENS_DIR / "README.txt"


def _load_ts_games() -> pd.DataFrame:
    box = pd.read_csv(
        paths.player_box_csv(),
        usecols=["game_id", "team_id", "season", "athlete_display_name"],
        low_memory=False,
    )
    box = box[box["athlete_display_name"].astype(str).str.strip() != "-"]
    return (
        box.groupby(["team_id", "season"], observed=True)["game_id"]
        .nunique()
        .rename("ts_games")
        .reset_index()
    )


def tail_metrics(roster: pd.DataFrame) -> dict:
    r = roster.sort_values("vent")
    peak_i = int(r["draft_rate"].idxmax())
    peak_v = int(r.loc[peak_i, "vent"])
    peak_rate = float(r.loc[peak_i, "draft_rate"])
    top_rate = float(r.iloc[-1]["draft_rate"])
    post = r[r.vent > peak_v].sort_values("vent")
    declines = 0
    if len(post) >= 2:
        pr = post["draft_rate"].tolist()
        for i in range(len(pr) - 1):
            if pr[i + 1] < pr[i] - 1e-9:
                declines += 1
    consec = 0
    prev = peak_rate
    for _, row in post.iterrows():
        if float(row.draft_rate) < prev - 1e-9:
            consec += 1
            prev = float(row.draft_rate)
        else:
            break
    return {
        "peak_bin": peak_v + 1,
        "peak_rate": peak_rate,
        "bin_last_rate": top_rate,
        "tail_drop": top_rate - peak_rate,
        "decline_bins_after_peak": declines,
        "consec_declines_from_peak": consec,
        "rates": [round(float(x), 5) for x in r["draft_rate"].tolist()],
    }


def spec_description(rec: dict) -> str:
    x = rec["x"]
    perf = str(rec.get("perf_metric", "ppm")).upper()
    x_label = "poolq_loo (LOO teammate perf)" if x == "poolq_loo" else "pool_mean (team-season avg perf)"
    mg = int(rec["mg"])
    qc = (
        f"POST-QC: drop team-seasons with ≤{MIN_TEAM_SEASON_GAMES} ESPN games"
        if mg >= 10
        else "PRE-QC (July replay): no min-team-games filter — includes exhibition cameos"
    )
    lines = [
        "What we tried:",
        f"  perf_metric: {perf} (own ability + LOO teammate quality)",
        f"  X-axis: {x_label}",
        f"  Panel: {qc}",
        f"  Seasons: {rec['seasons']} · min_minutes={rec['min_minutes']:g}",
        f"  Bins: {rec['n_bins']} {rec['binning']} · winsor {rec['winsor'][0]}–{rec['winsor'][1]}",
    ]
    if rec.get("subsample"):
        sub = rec["subsample"]
        if sub == "draft_teams":
            lines.append("  Extra filter: teams with ≥1 ever-draftee only")
        elif sub == "ts25+":
            lines.append("  Extra filter: team-seasons with ≥25 distinct games")
        elif sub == "draft_teams+ts25":
            lines.append("  Extra filter: draft-team + ≥25 games")
        elif sub == "july_replay_mg0":
            lines.append("  Reference: exact July 2026 hero panel (mg=0)")
        else:
            lines.append(f"  Extra filter: {sub}")
    lines.extend(
        [
            f"  n={rec['n']:,} · drafts={rec['drafts']:,}",
            f"  Peak bin {rec['peak_bin']} @ {100*rec['peak_rate']:.2f}%",
            f"  Last bin @ {100*rec['bin_last_rate']:.2f}% · tail Δ={100*rec['tail_drop']:+.2f}pp",
            f"  Declining bins after peak: {rec['decline_bins_after_peak']} "
            f"(consecutive from peak: {rec['consec_declines_from_peak']})",
            f"  LPM β₂={rec['beta_sq']:+.4f} "
            f"({'concave' if rec['beta_sq'] < 0 else 'not concave'})",
        ]
    )
    return "\n".join(lines)


def spec_slug(rec: dict) -> str:
    parts = []
    perf = str(rec.get("perf_metric", "ppm")).lower()
    if perf != "ppm":
        parts.append(perf)
    parts.append(rec["x"].replace("poolq_loo", "loo").replace("pool_mean", "poolmean"))
    parts.append(f"mg{rec['mg']}")
    parts.append(rec["seasons"].replace("-", "_"))
    parts.append(f"b{rec['n_bins']}{'q' if rec['binning'] == 'quantile' else 'ew'}")
    wlo, whi = rec["winsor"]
    parts.append(f"w{int(wlo*100):02d}{int(whi*100):02d}")
    if rec.get("subsample"):
        parts.append(rec["subsample"].replace("+", "_"))
    slug = "_".join(parts)
    slug = re.sub(r"[^A-Za-z0-9_]+", "_", slug)
    return slug[:120]


def run_spec(
    ts_games: pd.DataFrame,
    *,
    xcol: str,
    mg: int,
    smin: int,
    smax: int,
    n_bins: int,
    binning: str,
    winsor=(0.01, 0.99),
    min_minutes=20.0,
    draft_relevant_only=False,
    ts_min_games: int | None = None,
    subsample: str | None = None,
    perf_metric: str = "ppm",
) -> dict | None:
    perf = str(perf_metric).strip().lower()
    cfg = PipelineConfig(
        perf_metric=[perf],
        perf_zscore_within_season=True,
        ventiles=n_bins,
        poolq_binning=binning,
        poolq_winsor_quantiles=winsor,
        min_minutes=min_minutes,
        min_team_season_games=mg,
        drop_dash_placeholder_names=True,
        restrict_teams_by_draftees=False,
        panel_season_min=smin,
        panel_season_max=smax,
    )
    panel = panel_rebuild.build_from_box(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf,
        poolq_winsor_quantiles=winsor,
        zscore_perf_within_season=True,
    )
    panel["pool_mean"] = panel.groupby(["team_id", "season"])["perf"].transform("mean")
    use = panel_build.filter_panel(panel, cfg).merge(ts_games, on=["team_id", "season"], how="left")
    if draft_relevant_only:
        use = use[use.team_id.isin(set(use.loc[use.Y_draft == 1, "team_id"]))]
    if ts_min_games is not None:
        use = use[use.ts_games >= ts_min_games]
    if len(use) < 500:
        return None
    use = use.copy()
    use["x"] = use[xcol]
    use["vent"] = assign_poolq_bin_labels(use["x"], n_bins, binning)
    roster = (
        use.groupby("vent", observed=True)
        .agg(n=("Y_draft", "size"), draft_rate=("Y_draft", "mean"))
        .reset_index()
    )
    if len(roster) < n_bins:
        return None
    tm = tail_metrics(roster)
    tmp = use.copy()
    tmp["poolq_loo"] = tmp["x"]
    tmp["poolq_sq"] = tmp["x"] ** 2
    b2 = float(panel_build.draft_poolq_quadratic_coeffs(tmp)["poolq_sq"])
    rec = {
        "perf_metric": perf,
        "x": xcol,
        "mg": mg,
        "seasons": f"{smin}-{smax}",
        "n_bins": n_bins,
        "binning": binning,
        "winsor": list(winsor),
        "min_minutes": min_minutes,
        "draft_relevant_only": draft_relevant_only,
        "ts_min_games": ts_min_games,
        "subsample": subsample,
        "n": int(len(use)),
        "drafts": int(use.Y_draft.sum()),
        "beta_sq": b2,
        **tm,
    }
    rec["slug"] = spec_slug(rec)
    rec["description"] = spec_description(rec)
    rec["png"] = f"PASS_A_sensitivity_{rec['slug']}.png"
    return rec


def all_specs(quick: bool, *, perf_metric: str = "ppm") -> list[dict]:
    ts_games = _load_ts_games()
    rows: list[dict] = []
    grid: list[tuple] = []
    if quick:
        if str(perf_metric).lower() == "ppm":
            grid = [
                ("poolq_loo", 10, 2011, 2021, 16, "quantile", (0.01, 0.99)),
                ("poolq_loo", 10, 2013, 2021, 16, "quantile", (0.01, 0.99)),
                ("poolq_loo", 10, 2013, 2021, 20, "equal_width", (0.01, 0.99)),
                ("poolq_loo", 10, 2013, 2021, 20, "equal_width", (0.02, 0.98)),
                ("pool_mean", 10, 2011, 2021, 16, "quantile", (0.01, 0.99)),
                ("pool_mean", 10, 2011, 2021, 20, "equal_width", (0.01, 0.99)),
                ("poolq_loo", 0, 2011, 2021, 16, "quantile", (0.01, 0.99)),
                ("poolq_loo", 10, 2011, 2021, 16, "quantile", (0.01, 0.99)),
            ]
        else:
            grid = [
                ("poolq_loo", 10, 2011, 2021, 16, "quantile", (0.01, 0.99)),
                ("poolq_loo", 10, 2013, 2021, 16, "quantile", (0.01, 0.99)),
                ("pool_mean", 10, 2011, 2021, 16, "quantile", (0.01, 0.99)),
            ]
        for xcol, mg, smin, smax, nb, binning, winsor in grid:
            r = run_spec(
                ts_games,
                xcol=xcol,
                mg=mg,
                smin=smin,
                smax=smax,
                n_bins=nb,
                binning=binning,
                winsor=winsor,
                subsample="july_replay_mg0" if mg == 0 else None,
                perf_metric=perf_metric,
            )
            if r:
                rows.append(r)
        return rows

    for xcol in ("poolq_loo", "pool_mean"):
        for smin, smax in ((2011, 2021), (2013, 2021)):
            for n_bins in (16, 20):
                for binning in ("quantile", "equal_width"):
                    for winsor in ((0.01, 0.99), (0.02, 0.98)):
                        r = run_spec(
                            ts_games,
                            xcol=xcol,
                            mg=10,
                            smin=smin,
                            smax=smax,
                            n_bins=n_bins,
                            binning=binning,
                            winsor=winsor,
                            perf_metric=perf_metric,
                        )
                        if r:
                            rows.append(r)

    for xcol in ("poolq_loo", "pool_mean"):
        for label, kw in [
            ("draft_teams", {"draft_relevant_only": True}),
            ("ts25+", {"ts_min_games": 25}),
            ("draft_teams+ts25", {"draft_relevant_only": True, "ts_min_games": 25}),
        ]:
            r = run_spec(
                ts_games,
                xcol=xcol,
                mg=10,
                smin=2011,
                smax=2021,
                n_bins=16,
                binning="quantile",
                subsample=label,
                perf_metric=perf_metric,
                **kw,
            )
            if r:
                rows.append(r)

    if str(perf_metric).lower() == "ppm":
        r0 = run_spec(
            ts_games,
            xcol="poolq_loo",
            mg=0,
            smin=2011,
            smax=2021,
            n_bins=16,
            binning="quantile",
            subsample="july_replay_mg0",
            perf_metric="ppm",
        )
        if r0:
            rows.append(r0)
    return rows


def plot_spec(rec: dict, out_dir: Path) -> Path:
    configure_matplotlib_mathtext()
    n_bins = int(rec["n_bins"])
    rates = rec["rates"]
    x = list(range(1, len(rates) + 1))

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    ax.bar(x, [100 * r for r in rates], color="steelblue", edgecolor="white", alpha=0.92)
    ax.set_xlabel("Bin (1 = lowest roster-pressure ventile)")
    ax.set_ylabel("Mean NBA draft rate (%)")
    xname = "LOO poolq" if rec["x"] == "poolq_loo" else "pool_mean"
    perf = str(rec.get("perf_metric", "ppm")).upper()
    ax.set_title(
        f"Pass A sensitivity — {perf} · {xname} · {rec['seasons']} · mg={rec['mg']}\n"
        f"{rec['n_bins']} {rec['binning']} · n={rec['n']:,} · drafts={rec['drafts']:,}",
        fontsize=11,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    peak = int(rec["peak_bin"])
    ax.axvline(peak, color="darkorange", ls="--", lw=1.2, alpha=0.8, label=f"peak bin {peak}")
    ax.legend(loc="upper left", fontsize=8)

    fig.text(
        0.02,
        0.02,
        rec["description"],
        transform=fig.transFigure,
        fontsize=7.5,
        va="bottom",
        ha="left",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.92, edgecolor="gray"),
    )
    fig.subplots_adjust(bottom=0.34)
    out = out_dir / rec["png"]
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def write_readme(rows: list[dict]) -> None:
    lines = [
        "Pass A hero sensitivity gallery",
        f"Generated: {date.today().isoformat()}",
        "",
        "Each PNG is mean Y_draft by roster-context bin with an on-figure caption.",
        "Goal: find POST-QC (mg=10) specs with ≥2 declining bins after peak (July had this only at mg=0).",
        "",
        "Files:",
    ]
    for rec in sorted(rows, key=lambda r: r["slug"]):
        flag = ""
        if rec.get("mg") == 0:
            flag = " [JULY REPLAY]"
        elif rec["decline_bins_after_peak"] >= 2:
            flag = " [≥2 POST-PEAK DROPS]"
        lines.append(f"  {rec['png']}{flag}")
        lines.append(f"    tail Δ={100*rec['tail_drop']:+.2f}pp · β₂={rec['beta_sq']:+.4f}")
    README_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _artifact_paths(perf_metric: str) -> tuple[Path, Path, Path]:
    perf = str(perf_metric).strip().lower()
    if perf == "ppm":
        return JSON_OUT, CSV_OUT, README_OUT
    tag = perf
    return (
        PASS_A / f"PASS_A_hero_sensitivity_post_qc_{tag}.json",
        PASS_A / f"PASS_A_hero_sensitivity_index_{tag}.csv",
        SENS_DIR / f"README_{tag}.txt",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Pass A hero sensitivity labeled PNG gallery.")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Plot key POST-QC specs only (3 per perf; faster smoke test).",
    )
    parser.add_argument(
        "--perf-metric",
        type=str,
        default="ppm",
        choices=("ppm", "obpm", "opm", "bpm", "dbpm", "dpm"),
        help="Own-ability + LOO perf (default ppm). Use obpm/bpm for Track C robustness.",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    SENS_DIR.mkdir(parents=True, exist_ok=True)
    perf = str(args.perf_metric).strip().lower()
    json_out, csv_out, readme_out = _artifact_paths(perf)

    print(f"Building sensitivity specs perf={perf} (quick={args.quick})...", flush=True)
    rows = all_specs(quick=args.quick, perf_metric=perf)
    print(f"  {len(rows)} specs computed", flush=True)

    for i, rec in enumerate(rows, 1):
        path = plot_spec(rec, SENS_DIR)
        print(f"  [{i}/{len(rows)}] {path.name}", flush=True)

    json_out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    pd.DataFrame(rows).to_csv(csv_out, index=False)
    global README_OUT
    README_OUT = readme_out
    write_readme(rows)

    post = [r for r in rows if r.get("mg") == 10 and not r.get("subsample")]
    hits = [r for r in post if r["decline_bins_after_peak"] >= 2]
    print(f"\nWrote {len(rows)} PNGs under {SENS_DIR}")
    print(f"  JSON: {json_out}")
    print(f"  CSV:  {csv_out}")
    print(f"  README: {readme_out}")
    print(f"  POST-QC grid specs with ≥2 decline bins after peak: {len(hits)}")
    for h in hits:
        print(f"    · {h['png']}")


if __name__ == "__main__":
    main()
