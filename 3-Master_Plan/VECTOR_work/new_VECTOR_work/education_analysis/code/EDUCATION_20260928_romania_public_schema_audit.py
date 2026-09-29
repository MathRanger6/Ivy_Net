#!/usr/bin/env python3
"""Inventory the public Romania AER replication Stata files.

This script reads Stata headers only. It does not fit models, transform the
microdata, or produce substantive results.
"""

from __future__ import annotations

import csv
import hashlib
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE_DIR.glob("data-AER-*.dta"))
    if len(files) != 8:
        raise RuntimeError(f"Expected 8 Stata files, found {len(files)}")

    file_rows: list[dict[str, object]] = []
    variable_rows: list[dict[str, object]] = []

    for path in files:
        reader = pd.read_stata(path, iterator=True, convert_categoricals=False)
        labels = reader.variable_labels()
        variables = list(reader._varlist)
        formats = list(reader._fmtlist)
        storage_types = list(reader._dtyplist)

        file_rows.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "row_count": int(reader._nobs),
                "column_count": int(reader._nvar),
                "data_label": reader.data_label,
                "timestamp": str(reader.time_stamp),
            }
        )

        for position, variable in enumerate(variables, start=1):
            variable_rows.append(
                {
                    "file": path.name,
                    "position": position,
                    "variable": variable,
                    "label": labels.get(variable, ""),
                    "stata_format": formats[position - 1],
                    "storage_type": str(storage_types[position - 1]),
                }
            )

    with (OUTPUT_DIR / "file_inventory.json").open("w") as stream:
        json.dump(file_rows, stream, indent=2)

    with (OUTPUT_DIR / "variable_inventory.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(variable_rows[0]))
        writer.writeheader()
        writer.writerows(variable_rows)

    print(json.dumps(file_rows, indent=2))
    print(f"Wrote {len(variable_rows)} variable records to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
