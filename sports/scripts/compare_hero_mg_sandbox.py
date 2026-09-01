#!/usr/bin/env python3
"""Run HERO mg=0 vs existing mg10 in sports_sandbox/hero and print ventile diff.

Run (repo root):
  python sports/scripts/compare_hero_mg_sandbox.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SANDBOX = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero"
MG0_CSV = SANDBOX / "PASS_A_binned_draft_rate_poolq_loo_q16_allt_min20_mg0_11_21.csv"
MG10_CSV = SANDBOX / "PASS_A_binned_draft_rate_poolq_loo_q16_allt_min20_mg10_11_21.csv"
MG0_PROV = SANDBOX / "HERO_q16_allt_min20_mg0_11_21_provenance.json"


def main() -> None:
    bundle = REPO / "sports/scripts/pass_a_empirical_bundle.py"
    if not MG10_CSV.exists():
        raise SystemExit(
            "Missing mg10 CSV — run canonical first:\n"
            "  python sports/scripts/pass_a_empirical_bundle.py "
            "--output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero"
        )
    if not MG0_CSV.exists():
        cmd = [
            sys.executable,
            str(bundle),
            "--min-team-season-games",
            "0",
            "--output-root",
            str(SANDBOX.relative_to(REPO)),
        ]
        print("Running:", " ".join(cmd), flush=True)
        subprocess.run(cmd, cwd=REPO, check=True)

    if not MG0_CSV.exists() or not MG10_CSV.exists():
        raise SystemExit(f"Missing CSV — mg0={MG0_CSV.exists()} mg10={MG10_CSV.exists()}")

    if MG0_PROV.exists():
        prov10_path = SANDBOX / "HERO_q16_allt_min20_mg10_11_21_provenance.json"
        n0 = int(MG0_PROV.read_text(encoding="utf-8").split('"n_rows": ')[1].split(",")[0])
        print("\n=== mg0 provenance ===")
        print(MG0_PROV.read_text(encoding="utf-8"))
        if prov10_path.exists():
            n10 = int(prov10_path.read_text(encoding="utf-8").split('"n_rows": ')[1].split(",")[0])
            print(f"\nCanonical mg=10: n={n10:,} | mg=0 sensitivity: n={n0:,} | delta={n0 - n10:+,}")
            print("mg=0 inverted-U is pre-QC replay — do NOT lock as population. See sandbox README.")

    d0 = pd.read_csv(MG0_CSV)
    d10 = pd.read_csv(MG10_CSV)
    m = d0[["vent", "n", "draft_rate"]].merge(
        d10[["vent", "n", "draft_rate"]],
        on="vent",
        suffixes=("_mg0", "_mg10"),
    )
    m["rate_delta"] = m["draft_rate_mg0"] - m["draft_rate_mg10"]
    m["n_delta"] = m["n_mg0"] - m["n_mg10"]

    n0 = int(MG0_PROV.read_text(encoding="utf-8").split('"n_rows": ')[1].split(",")[0]) if MG0_PROV.exists() else None
    print("\n=== ventile comparison (mg0 − mg10) ===")
    print(m.to_string(index=False, float_format=lambda x: f"{x:.6g}"))
    print(f"\nmax |Δ draft_rate| = {m['rate_delta'].abs().max():.6g}")
    print(f"mean |Δ draft_rate| = {m['rate_delta'].abs().mean():.6g}")
    if n0 is not None:
        prov10 = SANDBOX / "HERO_q16_allt_min20_mg10_11_21_provenance.json"
        n10 = int(prov10.read_text(encoding="utf-8").split('"n_rows": ')[1].split(",")[0])
        print(f"n_rows: mg0={n0:,} mg10={n10:,} delta={n0 - n10:+,}")


if __name__ == "__main__":
    main()
