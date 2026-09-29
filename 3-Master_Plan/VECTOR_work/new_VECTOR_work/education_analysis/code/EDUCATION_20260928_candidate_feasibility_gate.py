#!/usr/bin/env python3
"""Test whether public ELS:2002 and HSLS:09 can support the peer-pool design.

The gate reads only decisive columns.  It reports availability; it does not fit
models, infer effects, or generate a data-story mosaic.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


REPO = Path(__file__).resolve().parents[5]
OUT = (
    REPO
    / "3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/outputs"
    / "candidate_feasibility_gate_20260928"
)

SPECS = {
    "ELS:2002": {
        "path": REPO
        / "datasets/els2002/source_public_nces_20260928/extracted/els_02_12_byf3pststu_v1_0.dta",
        "columns": {
            "student_id": "STU_ID",
            "school_id": "SCH_ID",
            "prior_math": "BYTXMSTD",
            "prior_composite": "BYTXCSTD",
            "applications": "F2NAPP1P",
            "acceptances": "F2NACC1P",
            "application_selectivity": "F2PSAPSL",
            "acceptance_selectivity": "F2PSACSL",
            "first_attended_selectivity_2006": "F2PS1SLC",
            "first_known_selectivity_transcript": "F3TZPS1SLC",
            "highest_degree_2013": "F3TZHIGHDEG",
            "base_weight": "BYSTUWT",
        },
    },
    "HSLS:09": {
        "path": REPO
        / "datasets/hsls09/source_public_nces_20260928/extracted/hsls09_16_student_pets_pear_v1_0.dta",
        "columns": {
            "student_id": "STU_ID",
            "school_id": "SCH_ID",
            "prior_math": "X1TXMTSCOR",
            "applications": "X4CLGAPPNUM",
            "first_attended_selectivity_2016": "X4PS1SELECT",
            "first_known_selectivity_2021": "X6PS1SLC",
            "highest_degree_2021": "X6HIGHDEG",
            "bachelors_count_2021": "X6BACCRED",
        },
    },
}


def nonnegative_code(series: pd.Series) -> pd.Series:
    """Flag nonnegative codes; negative NCES codes require variable-specific interpretation."""
    return pd.to_numeric(series, errors="coerce").ge(0)


def summarize_study(name: str, spec: dict) -> tuple[dict, list[dict]]:
    raw_columns = list(spec["columns"].values())
    frame = pd.read_stata(
        spec["path"], columns=raw_columns, convert_categoricals=False
    ).rename(columns={raw: role for role, raw in spec["columns"].items()})
    details: list[dict] = []
    for role in spec["columns"]:
        values = frame[role]
        nonnegative = nonnegative_code(values)
        details.append(
            {
                "study": name,
                "role": role,
                "source_variable": spec["columns"][role],
                "rows": int(len(values)),
                "nonnegative_public_rows": int(nonnegative.sum()),
                "nonnegative_public_share": float(nonnegative.mean()),
                "unique_nonnegative_values": int(values.loc[nonnegative].nunique(dropna=True)),
                "most_common_values": {
                    str(k): int(v)
                    for k, v in values.value_counts(dropna=False).head(5).items()
                },
            }
        )

    school = next(item for item in details if item["role"] == "school_id")
    summary = {
        "study": name,
        "rows": int(len(frame)),
        "public_school_id_nonnegative_rows": school["nonnegative_public_rows"],
        "public_school_id_unique_nonnegative_values": school["unique_nonnegative_values"],
        "public_peer_pool_reconstructable": bool(
            school["nonnegative_public_rows"] > 0
            and school["unique_nonnegative_values"] > 1
        ),
        "mosaic_gate": "PASS"
        if school["nonnegative_public_rows"] > 0
        and school["unique_nonnegative_values"] > 1
        else "FAIL — common student-to-school identifier suppressed in public file",
    }
    return summary, details


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries: list[dict] = []
    details: list[dict] = []
    for name, spec in SPECS.items():
        summary, study_details = summarize_study(name, spec)
        summaries.append(summary)
        details.extend(study_details)
        print(
            f"{name}: rows={summary['rows']:,}; "
            f"nonnegative school IDs={summary['public_school_id_nonnegative_rows']:,}; "
            f"mosaic gate={summary['mosaic_gate']}"
        )
    (OUT / "candidate_gate_summary.json").write_text(
        json.dumps(summaries, indent=2) + "\n"
    )
    pd.DataFrame(details).to_csv(OUT / "candidate_field_counts.csv", index=False)
    print(f"Wrote {OUT.relative_to(REPO)}/candidate_gate_summary.json")
    print(f"Wrote {OUT.relative_to(REPO)}/candidate_field_counts.csv")


if __name__ == "__main__":
    main()
