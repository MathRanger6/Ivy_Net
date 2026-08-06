#!/usr/bin/env python3
"""PEER — build faculty_panel_inference_v1.csv after Charles C1–C2 locks.

Primary filter: match_confidence IN (HIGH, MEDIUM); exclude MULTI.
Output: tenure_pipeline/faculty_panel_inference_v1.csv + filter manifest JSON.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "tenure_pipeline" / "R1_tenure_data.csv"
OUT = REPO / "tenure_pipeline" / "faculty_panel_inference_v1.csv"
MANIFEST = REPO / "tenure_pipeline" / "faculty_panel_inference_v1_manifest.json"

PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})


def main() -> None:
    if not SRC.is_file():
        raise FileNotFoundError(f"Missing source panel: {SRC}")

    df = pd.read_csv(SRC, low_memory=False)
    n_src_rows = len(df)
    n_src_persons = df["faculty_id"].nunique() if "faculty_id" in df.columns else None
    n_src_depts = df["uni_slug"].nunique() if "uni_slug" in df.columns else None

    tier_counts = df["match_confidence"].value_counts(dropna=False).to_dict()
    filtered = df[df["match_confidence"].isin(PRIMARY_TIERS)].copy()

    # Inference rows need LOO pool quality for Setting 3 inverted-U readouts
    if "poolq_loo_mean" in filtered.columns:
        with_poolq = filtered["poolq_loo_mean"].notna()
        n_before = len(filtered)
        filtered = filtered[with_poolq]
        poolq_dropped = n_before - len(filtered)
    else:
        poolq_dropped = 0

    filtered.to_csv(OUT, index=False)

    n_inf_rows = len(filtered)
    n_inf_persons = filtered["faculty_id"].nunique()
    n_inf_depts = filtered["uni_slug"].nunique()
    asst = filtered[filtered["rank"] == "assistant"] if "rank" in filtered.columns else filtered
    n_asst_rows = len(asst)
    n_asst_persons = asst["faculty_id"].nunique()

    manifest = {
        "artifact": "faculty_panel_inference_v1.csv",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "charles_locks": "20260611_Charles_Tier1_locks.md",
        "filter": {
            "match_confidence": sorted(PRIMARY_TIERS),
            "exclude": ["MULTI", "LOW", "NONE"],
            "require_poolq_loo_mean": True,
        },
        "source": {
            "path": str(SRC.relative_to(REPO)),
            "rows": n_src_rows,
            "persons": n_src_persons,
            "departments": n_src_depts,
            "match_confidence_counts": tier_counts,
        },
        "inference_sample": {
            "rows": n_inf_rows,
            "persons": n_inf_persons,
            "departments": n_inf_depts,
            "assistant_person_years": n_asst_rows,
            "assistant_persons": n_asst_persons,
            "rows_dropped_missing_poolq": poolq_dropped,
        },
        "prose_guidance": {
            "roster_n": "168 R1 CS departments in data construction",
            "lead_with": "inference_sample persons/departments above",
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT} ({n_inf_rows} rows, {n_inf_persons} persons, {n_inf_depts} depts)")
    print(json.dumps(manifest["inference_sample"], indent=2))


if __name__ == "__main__":
    main()
