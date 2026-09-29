#!/usr/bin/env python3
"""Check whether Romania files 4-6 preserve nested student peer pools.

This is a structural/schema gate only. It does not fit a model or estimate an
association between peer context and outcomes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_DIR = (
    REPO_ROOT
    / "datasets"
    / "romania"
    / "source_public_openicpsr_20260928"
    / "extracted"
    / "data"
)
OUTPUT_DIR = (
    REPO_ROOT
    / "3-Master_Plan"
    / "VECTOR_work"
    / "new_VECTOR_work"
    / "education_analysis"
    / "outputs"
    / "romania_schema_audit_20260928"
)


def native(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def summarize(path: Path) -> dict[str, object]:
    columns = ["grade", "bcg", "bct", "year", "ua", "us", "us2", "ct", "survey"]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)

    school_track_to_school = frame.groupby("us2", dropna=False)["us"].nunique(dropna=False)
    school_track_to_town = frame.groupby("us2", dropna=False)["ua"].nunique(dropna=False)
    school_to_town = frame.groupby("us", dropna=False)["ua"].nunique(dropna=False)
    track_sizes = frame.groupby(["year", "us2"], dropna=False).size()
    school_sizes = frame.groupby(["year", "us"], dropna=False).size()

    def quantiles(series: pd.Series) -> dict[str, object]:
        return {
            str(q): native(series.quantile(q))
            for q in (0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)
        }

    return {
        "file": path.name,
        "rows": int(len(frame)),
        "years": [native(v) for v in sorted(frame["year"].dropna().unique())],
        "unique_towns_ua": int(frame["ua"].nunique(dropna=True)),
        "unique_schools_us": int(frame["us"].nunique(dropna=True)),
        "unique_school_tracks_us2": int(frame["us2"].nunique(dropna=True)),
        "us2_max_number_of_us_values": int(school_track_to_school.max()),
        "us2_max_number_of_ua_values": int(school_track_to_town.max()),
        "us_max_number_of_ua_values": int(school_to_town.max()),
        "track_group_size_quantiles": quantiles(track_sizes),
        "school_group_size_quantiles": quantiles(school_sizes),
        "track_cell_counts": {
            "total": int(len(track_sizes)),
            "size_1": int((track_sizes == 1).sum()),
            "size_below_5": int((track_sizes < 5).sum()),
            "size_below_10": int((track_sizes < 10).sum()),
        },
        "missing_counts": {column: int(frame[column].isna().sum()) for column in columns},
        "baccalaureate_structure": {
            "not_taken_rows": int((frame["bct"] == 0).sum()),
            "taken_rows": int((frame["bct"] == 1).sum()),
            "grade_missing_when_not_taken": int(
                ((frame["bct"] == 0) & frame["bcg"].isna()).sum()
            ),
            "grade_missing_when_taken": int(
                ((frame["bct"] == 1) & frame["bcg"].isna()).sum()
            ),
            "grade_present_when_not_taken": int(
                ((frame["bct"] == 0) & frame["bcg"].notna()).sum()
            ),
            "grade_present_when_taken": int(
                ((frame["bct"] == 1) & frame["bcg"].notna()).sum()
            ),
        },
        "ct_unique_values": [native(v) for v in sorted(frame["ct"].dropna().unique())],
        "bct_unique_values": [native(v) for v in sorted(frame["bct"].dropna().unique())],
        "survey_unique_values": [native(v) for v in sorted(frame["survey"].dropna().unique())],
        "example_us2_values": [str(v) for v in frame["us2"].dropna().drop_duplicates().head(10)],
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = [summarize(SOURCE_DIR / f"data-AER-{index}.dta") for index in (4, 5, 6)]
    output = OUTPUT_DIR / "pool_structure_gate.json"
    output.write_text(json.dumps(summaries, indent=2))
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
