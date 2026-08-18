#!/usr/bin/env python3
"""PD22 item 9 — compare panel policies (drop vs PPM-zero) at min 20.

Side-by-side empirical H_sort and bracket rho* from PD21 calibration JSONs.
Default: load existing full 2011-2021 bracket fits (no simulation).

Run (repo root):
  python sports/scripts/pd22_panel_policy_compare.py
  python sports/scripts/pd22_panel_policy_compare.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_panel_policy_compare_2011_2021.csv
  PD22_panel_policy_compare_summary_2011_2021.csv
  PD22_panel_policy_compare_2011_2021.json
  PD22_panel_policy_compare_2011_2021.png
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import PD21_RHO, PD22_MINUTES, ensure_hero_dirs
from interval_overlap_paths import seasons_label

OUT = PD22_MINUTES
SEASON_MIN = 2011
SEASON_MAX = 2021
HERO_LOCK = 20.0
STEM = f"PD22_panel_policy_compare_{SEASON_MIN}_{SEASON_MAX}"
CALIBRATE_SCRIPT = SCRIPTS / "pd21_rho_hsort_calibrate.py"
MECHANISM_SEASON_CSV = OUT / f"PD22_ppm_zero_hsort_mechanism_season_{SEASON_MIN}_{SEASON_MAX}.csv"

DROP_JSON = PD21_RHO / f"PD21_rho_hsort_calibrate_{SEASON_MIN}_{SEASON_MAX}_fit_bracket.json"
PPM0_JSON = PD21_RHO / f"PD21_rho_hsort_calibrate_{SEASON_MIN}_{SEASON_MAX}_ppm0lt{int(HERO_LOCK)}_fit_bracket.json"
HSORT_STALE_TOLERANCE = 0.01


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{STEM}.csv",
        "summary_csv": OUT / f"{STEM.replace('_compare_', '_compare_summary_')}.csv",
        "json": OUT / f"{STEM}.json",
        "png": OUT / f"{STEM}.png",
    }


def _load_fit(path: Path, *, policy: str) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Missing bracket JSON for {policy}: {path}")
    meta = json.loads(path.read_text(encoding="utf-8"))
    meta["_policy"] = policy
    meta["_path"] = str(path)
    return meta


def _empirical_targets(fit: dict) -> dict[int, dict]:
    rows = fit.get("empirical_targets") or fit.get("season_data") or []
    return {int(r["season"]): r for r in rows}


def _load_hsort_current_panel() -> pd.DataFrame:
    if not MECHANISM_SEASON_CSV.is_file():
        raise FileNotFoundError(
            f"Missing item 8 season CSV — run pd22_ppm_zero_hsort_mechanism.py first: {MECHANISM_SEASON_CSV}"
        )
    df = pd.read_csv(MECHANISM_SEASON_CSV)
    return df.rename(
        columns={
            "h_sort_drop": "h_sort_emp_drop_current",
            "h_sort_ppm_zero": "h_sort_emp_ppm_zero_current",
            "h_sort_delta_ppm_zero_minus_drop": "h_sort_emp_delta_current",
        }
    )


def _season_table(drop: dict, ppm0: dict, hsort_current: pd.DataFrame) -> pd.DataFrame:
    dps = {int(r["season"]): r for r in drop.get("per_season", [])}
    pps = {int(r["season"]): r for r in ppm0.get("per_season", [])}
    dsd = _empirical_targets(drop)
    psd = _empirical_targets(ppm0)
    seasons = sorted(set(dps) | set(pps) | set(hsort_current["season"].astype(int)))
    hmap = hsort_current.set_index("season")
    rows = []
    for season in seasons:
        dr = dps.get(season, {})
        pr = pps.get(season, {})
        hc = hmap.loc[season] if season in hmap.index else {}
        rows.append(
            {
                "season": season,
                "rho_star_drop": dr.get("rho_star"),
                "rho_star_ppm_zero": pr.get("rho_star"),
                "rho_star_delta": (
                    float(pr["rho_star"]) - float(dr["rho_star"])
                    if dr.get("rho_star") is not None and pr.get("rho_star") is not None
                    else float("nan")
                ),
                "h_sort_emp_drop": hc.get("h_sort_emp_drop_current", dr.get("h_sort_empirical")),
                "h_sort_emp_ppm_zero": hc.get("h_sort_emp_ppm_zero_current", pr.get("h_sort_empirical")),
                "h_sort_emp_delta": hc.get("h_sort_emp_delta_current"),
                "h_sort_emp_ppm_zero_bracket_json": pr.get("h_sort_empirical"),
                "n_players_drop": dsd.get(season, {}).get("n_players"),
                "n_players_ppm_zero": psd.get(season, {}).get("n_players"),
            }
        )
    return pd.DataFrame(rows)


def _policy_summary(drop: dict, ppm0: dict, season_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for policy, fit in (("drop", drop), ("ppm_zero", ppm0)):
        long = fit.get("longitudinal", {})
        ps = fit.get("per_season", [])
        sd = _empirical_targets(fit)
        n_zero_rho = sum(1 for r in ps if float(r.get("rho_star", -1)) == 0.0)
        if policy == "drop":
            h_mean = float(season_df["h_sort_emp_drop"].mean())
        else:
            h_mean = float(season_df["h_sort_emp_ppm_zero"].mean())
        rows.append(
            {
                "policy": policy,
                "panel_mode": fit.get("panel", {}).get("panel_mode", ""),
                "description": fit.get("panel", {}).get("description", ""),
                "rho_star_longitudinal": long.get("rho_star_longitudinal"),
                "h_sort_emp_mean": h_mean,
                "h_sort_emp_mean_bracket_json": long.get("h_sort_empirical_mean_over_seasons"),
                "h_sort_sim_mean_at_star": long.get("h_sort_sim_mean_at_star"),
                "mean_abs_err_at_star": long.get("mean_abs_err_at_star"),
                "n_seasons": len(ps),
                "n_seasons_rho_star_zero": n_zero_rho,
                "n_players_mean": float(np.mean([r.get("n_players", float("nan")) for r in sd.values()]))
                if sd
                else float("nan"),
                "source_json": fit.get("_path", ""),
            }
        )
    return pd.DataFrame(rows)


def _ppm_zero_stale(ppm0: dict, season_df: pd.DataFrame) -> tuple[bool, float]:
    json_hs = season_df["h_sort_emp_ppm_zero_bracket_json"].dropna()
    cur_hs = season_df["h_sort_emp_ppm_zero"].dropna()
    if len(json_hs) == 0 or len(cur_hs) == 0:
        return True, float("nan")
    merged = season_df.dropna(subset=["h_sort_emp_ppm_zero_bracket_json", "h_sort_emp_ppm_zero"])
    diff = (merged["h_sort_emp_ppm_zero_bracket_json"] - merged["h_sort_emp_ppm_zero"]).abs()
    return bool(diff.mean() > HSORT_STALE_TOLERANCE), float(diff.mean())


def _summary(season_df: pd.DataFrame, policy_df: pd.DataFrame, *, ppm0_stale: bool, ppm0_hsort_drift: float) -> dict:
    drop = policy_df.loc[policy_df["policy"] == "drop"].iloc[0]
    pz = policy_df.loc[policy_df["policy"] == "ppm_zero"].iloc[0]
    h_delta = float(season_df["h_sort_emp_delta"].mean())
    note = (
        "Drop-at-20 on current box-QC panel: rho*≈0, H_sort stable. "
        "PPM-zero legacy bracket JSON targets pre-QC H_sort (~0.17) — rho*~0.57 not valid on current panel; "
        "item 8 shows H_sort delta ~0.001 only."
        if ppm0_stale
        else "Drop-at-20 recommended; PPM-zero inflates rho* without proportional H_sort gain."
    )
    return {
        "hero_lock_min_minutes": HERO_LOCK,
        "rho_star_longitudinal_drop": float(drop["rho_star_longitudinal"]),
        "rho_star_longitudinal_ppm_zero": float(pz["rho_star_longitudinal"]),
        "rho_star_longitudinal_ppm_zero_stale": ppm0_stale,
        "rho_star_longitudinal_delta": float(pz["rho_star_longitudinal"]) - float(drop["rho_star_longitudinal"]),
        "h_sort_emp_mean_drop": float(drop["h_sort_emp_mean"]),
        "h_sort_emp_mean_ppm_zero": float(pz["h_sort_emp_mean"]),
        "h_sort_emp_mean_delta": h_delta,
        "ppm_zero_bracket_hsort_drift": ppm0_hsort_drift,
        "n_seasons_rho_zero_drop": int(drop["n_seasons_rho_star_zero"]),
        "n_seasons_rho_zero_ppm_zero": int(pz["n_seasons_rho_star_zero"]),
        "recommended_policy": "drop",
        "recommendation_note": note,
    }


def _plot(season_df: pd.DataFrame, summary: dict, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    xs = season_df["season"].to_numpy(dtype=int)

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.0), sharex=True)

    ax = axes[0]
    ax.plot(xs, season_df["rho_star_drop"], "o-", color="darkorange", lw=2, ms=5, label="Drop (min 20)")
    ax.plot(xs, season_df["rho_star_ppm_zero"], "s--", color="steelblue", lw=1.8, ms=5, label="PPM-zero (legacy bracket JSON)")
    if summary.get("rho_star_longitudinal_ppm_zero_stale"):
        ax.text(
            0.02,
            0.02,
            "PPM-zero ρ* from pre-box-QC panel\n(current H_sort ≈ drop — item 8)",
            transform=ax.transAxes,
            fontsize=7.5,
            va="bottom",
            bbox=dict(boxstyle="round", facecolor=(1.0, 0.95, 0.88), alpha=0.92),
        )
    ax.axhline(summary["rho_star_longitudinal_drop"], color="darkorange", ls=":", lw=1.2, alpha=0.7)
    ax.axhline(summary["rho_star_longitudinal_ppm_zero"], color="steelblue", ls=":", lw=1.2, alpha=0.7)
    ax.set_ylabel(r"Bracket $\rho^*$")
    ax.set_title(
        rf"Per-season $\rho^*$ · longitudinal drop = {summary['rho_star_longitudinal_drop']:.3g} "
        rf"vs PPM-zero = {summary['rho_star_longitudinal_ppm_zero']:.3g}"
    )
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25, linewidth=0.5)

    ax = axes[1]
    ax.plot(xs, season_df["h_sort_emp_drop"], "o-", color="darkorange", lw=2, ms=5, label="Drop")
    ax.plot(xs, season_df["h_sort_emp_ppm_zero"], "s-", color="steelblue", lw=2, ms=5, label="PPM-zero")
    ax.set_xlabel("Season")
    ax.set_ylabel(r"Empirical $H_{\mathrm{sort}}$")
    ax.set_title(rf"$H_{{\mathrm{{sort}}}}$ empirical · $\Delta$ mean = {summary['h_sort_emp_mean_delta']:+.4f}")
    ax.legend(fontsize=8, loc="best")
    ax.grid(alpha=0.25, linewidth=0.5)

    fig.suptitle(rf"PD22 item 9 — panel policy compare · {seasons} · floor = {HERO_LOCK:g} min", fontsize=11, y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _maybe_run_calibration(*, quick: bool) -> None:
    missing = [p for p in (DROP_JSON, PPM0_JSON) if not p.is_file()]
    if not missing:
        return
    cmd_base = [sys.executable, str(CALIBRATE_SCRIPT), "--fresh"]
    if quick:
        cmd_base.append("--quick")
    if not DROP_JSON.is_file():
        print("Running drop bracket calibration ...", flush=True)
        subprocess.run(cmd_base + ["--min-minutes", str(HERO_LOCK)], cwd=str(REPO), check=True)
    if not PPM0_JSON.is_file():
        print("Running PPM-zero bracket calibration ...", flush=True)
        subprocess.run(
            cmd_base + ["--ppm-zero-below-minutes", str(HERO_LOCK)],
            cwd=str(REPO),
            check=True,
        )


def run(*, refresh_calibration: bool, quick_calibration: bool) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    if refresh_calibration:
        for p in (DROP_JSON, PPM0_JSON):
            if p.is_file():
                p.unlink()
    _maybe_run_calibration(quick=quick_calibration)

    drop = _load_fit(DROP_JSON, policy="drop")
    ppm0 = _load_fit(PPM0_JSON, policy="ppm_zero")
    hsort_current = _load_hsort_current_panel()
    season_df = _season_table(drop, ppm0, hsort_current)
    ppm0_stale, ppm0_drift = _ppm_zero_stale(ppm0, season_df)
    policy_df = _policy_summary(drop, ppm0, season_df)
    summary = _summary(season_df, policy_df, ppm0_stale=ppm0_stale, ppm0_hsort_drift=ppm0_drift)
    _plot(season_df, summary, paths["png"])

    season_df.to_csv(paths["csv"], index=False, float_format="%.12g")
    policy_df.to_csv(paths["summary_csv"], index=False, float_format="%.12g")

    meta = {
        "diagnostic": "pd22_panel_policy_compare",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "sources": {
            "drop": str(DROP_JSON.relative_to(REPO)),
            "ppm_zero": str(PPM0_JSON.relative_to(REPO)),
        },
        "summary": summary,
        "policy_table": policy_df.to_dict(orient="records"),
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nLongitudinal rho*: drop={summary['rho_star_longitudinal_drop']:.4g}, "
          f"ppm-zero={summary['rho_star_longitudinal_ppm_zero']:.4g}", flush=True)
    print(f"H_sort emp mean: drop={summary['h_sort_emp_mean_drop']:.4f}, "
          f"ppm-zero={summary['h_sort_emp_mean_ppm_zero']:.4f} "
          f"(delta={summary['h_sort_emp_mean_delta']:+.4f})", flush=True)
    print(f"Recommended: {summary['recommended_policy']}", flush=True)
    print(f"\nWrote {paths['png']}", flush=True)
    print(f"Wrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['summary_csv']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full compare first: {paths['csv']}")
    season_df = pd.read_csv(paths["csv"])
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    summary = meta.get("summary") or {}
    if not summary:
        drop = _load_fit(DROP_JSON, policy="drop")
        ppm0 = _load_fit(PPM0_JSON, policy="ppm_zero")
        hsort_current = _load_hsort_current_panel()
        season_df = pd.read_csv(paths["csv"])
        ppm0_stale, ppm0_drift = _ppm_zero_stale(ppm0, season_df)
        summary = _summary(season_df, _policy_summary(drop, ppm0, season_df), ppm0_stale=ppm0_stale, ppm0_hsort_drift=ppm0_drift)
    _plot(season_df, summary, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV")
    parser.add_argument(
        "--refresh-calibration",
        action="store_true",
        help="Delete existing bracket JSON and rerun calibration (slow unless --quick)",
    )
    parser.add_argument(
        "--quick-calibration",
        action="store_true",
        help="If calibration needed, use pd21 --quick (2015 only)",
    )
    args = parser.parse_args()
    if args.plot_only:
        plot_only()
    else:
        run(refresh_calibration=args.refresh_calibration, quick_calibration=args.quick_calibration)


if __name__ == "__main__":
    main()
