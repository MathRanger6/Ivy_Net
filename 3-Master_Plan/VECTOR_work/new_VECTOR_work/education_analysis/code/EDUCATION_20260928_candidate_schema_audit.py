#!/usr/bin/env python3
"""Inventory ELS:2002 and HSLS:09 public-use files for the education candidate gate.

This first-stage audit reads Stata metadata only.  It does not fit models, construct
analytic samples, or run the data-story pipeline.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from pandas.io.stata import StataReader


REPO = Path(__file__).resolve().parents[5]
OUT = (
    REPO
    / "3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/outputs"
    / "candidate_schema_audit_20260928"
)

FILES = {
    "els_student": REPO
    / "datasets/els2002/source_public_nces_20260928/extracted/els_02_12_byf3pststu_v1_0.dta",
    "els_school": REPO
    / "datasets/els2002/source_public_nces_20260928/extracted/els_02_12_byf1sch_v1_0.dta",
    "els_f2_institution": REPO
    / "datasets/els2002/source_public_nces_20260928/extracted/els_02_12_f2inst_v1_0.dta",
    "els_f3_institution": REPO
    / "datasets/els2002/source_public_nces_20260928/extracted/els_02_12_f3inst_v1_0.dta",
    "hsls_student": REPO
    / "datasets/hsls09/source_public_nces_20260928/extracted/hsls09_16_student_pets_pear_v1_0.dta",
    "hsls_school": REPO
    / "datasets/hsls09/source_public_nces_20260928/extracted/HSLS_09_SCHOOL_v1_0.dta",
}

CONCEPTS = {
    "identifiers_and_groups": r"student id|school id|institution id|sample school|psu|stratum",
    "prior_performance": r"math.*score|test.*score|assessment|irt|standardized|standardized.*test|gpa|grade point",
    "applications": r"appl(y|ied|ication)|number of schools.*appl",
    "admissions": r"admi(t|tted|ssion)|accept(ed|ance)",
    "college_destination": r"first known postsecondary|first postsecondary|institution attended|college attended|sector.*institution|selectiv",
    "enrollment": r"enroll|attendance|persistence",
    "completion": r"degree|credential|certificate|attain|complet|graduat",
    "weights": r"weight|replicate|brr|panel wt|student wt",
}


def inspect_file(name: str, path: Path) -> tuple[dict, list[dict]]:
    if not path.exists():
        return {"name": name, "path": str(path.relative_to(REPO)), "exists": False}, []
    reader = StataReader(path)
    labels = reader.variable_labels()
    summary = {
        "name": name,
        "path": str(path.relative_to(REPO)),
        "exists": True,
        "rows": int(reader._nobs),
        "columns": int(reader._nvar),
    }
    matches: list[dict] = []
    for concept, pattern in CONCEPTS.items():
        rx = re.compile(pattern, flags=re.IGNORECASE)
        for variable, label in labels.items():
            searchable = f"{variable} {label or ''}"
            if rx.search(searchable):
                matches.append(
                    {
                        "file": name,
                        "concept": concept,
                        "variable": variable,
                        "label": label,
                    }
                )
    return summary, matches


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries: list[dict] = []
    matches: list[dict] = []
    for name, path in FILES.items():
        summary, file_matches = inspect_file(name, path)
        summaries.append(summary)
        matches.extend(file_matches)
        print(
            f"{name}: exists={summary['exists']} "
            f"rows={summary.get('rows', 'NA'):,} columns={summary.get('columns', 'NA'):,} "
            f"candidate_matches={len(file_matches):,}"
            if summary["exists"]
            else f"{name}: MISSING"
        )

    (OUT / "file_inventory.json").write_text(json.dumps(summaries, indent=2) + "\n")
    with (OUT / "candidate_variable_inventory.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "concept", "variable", "label"])
        writer.writeheader()
        writer.writerows(matches)
    print(f"Wrote {OUT.relative_to(REPO)}/file_inventory.json")
    print(f"Wrote {OUT.relative_to(REPO)}/candidate_variable_inventory.csv")


if __name__ == "__main__":
    main()
