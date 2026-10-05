"""Compare AR/SB county applicant lists with saved gymnasium applicant pages.

Offline source audit only. It reads private name/score rows to compare records,
but writes only aggregate counts. A name-and-score match is provisional; it is
not a unique student identifier. No Wayback requests or outcome analysis.
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20261001_romania_offline_county_source_readiness import family_status, saved_rows
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, components, name_score,
)
import EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation as school_audit
from EDUCATION_20261001_romania_origin_school_name_audit import save_csv


TARGET_COUNTIES = ("AR", "SB")
SAVED_SCHOOL_COUNTIES = ("AB", "CS", "GL", "TL", "AR", "SB")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_county_expansion_20261004"
FIELDS = (
    "county", "county_applicants", "exact_own_county_school_page",
    "exact_other_checked_county_school_page", "ambiguous_school_page_match",
    "same_name_and_admission_score_but_components_disagree",
    "not_found_on_six_counties_school_pages", "missing_comparison_fields",
    "not_found_with_printed_school_label", "not_found_without_printed_school_label",
    "not_found_label_says_own_county", "not_found_label_says_other_county",
    "not_found_label_county_unreadable",
)


def school_indexes():
    # The imported audit verifies source identity, row counts, and saved hashes.
    school_audit.COUNTIES = SAVED_SCHOOL_COUNTIES
    school_rows, _ = all_gymnasium_rows()
    exact = defaultdict(Counter)
    name_and_score = defaultdict(Counter)
    for county, rows in school_rows.items():
        for _code, identity, scores in rows:
            if identity is not None:
                name_and_score[identity][county] += 1
                if scores is not None:
                    exact[(identity, scores)][county] += 1
    return exact, name_and_score


def audit_county(county, exact, name_and_score):
    path = CACHE / "county_manifests" / f"{county}.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    complete, gaps = family_status(manifest, "candidate_roster")
    if not complete or gaps:
        raise ValueError(f"{county}: county applicant pages are not complete")
    applicants = saved_rows(manifest, "candidate_roster")
    tally = Counter()
    for row in applicants:
        identity, scores = name_score(row), components(row)
        if identity is None or scores is None:
            tally["missing_comparison_fields"] += 1
            continue
        locations = exact.get((identity, scores), Counter())
        matches = sum(locations.values())
        if matches > 1:
            tally["ambiguous_school_page_match"] += 1
        elif locations[county] == 1:
            tally["exact_own_county_school_page"] += 1
        elif matches == 1:
            tally["exact_other_checked_county_school_page"] += 1
        elif name_and_score.get(identity):
            tally["same_name_and_admission_score_but_components_disagree"] += 1
        else:
            tally["not_found_on_six_counties_school_pages"] += 1
            school_label = str(row.get("Şcoală", "")).strip()
            tally["not_found_with_printed_school_label" if school_label else "not_found_without_printed_school_label"] += 1
            # County applicant webpages print origin labels like "SCHOOL / AR".
            # This suffix is source evidence, not an inferred school-name match.
            suffix = re.search(r"/\s*([A-Z]{1,2})\s*$", school_label, re.I)
            if suffix is None:
                tally["not_found_label_county_unreadable"] += 1
            elif suffix.group(1).upper() == county:
                tally["not_found_label_says_own_county"] += 1
            else:
                tally["not_found_label_says_other_county"] += 1
    result = {field: tally[field] for field in FIELDS}
    result.update(county=county, county_applicants=len(applicants))
    main_categories = FIELDS[2:8]
    if sum(result[field] for field in main_categories) != len(applicants):
        raise ValueError(f"{county}: categories do not add to applicant count")
    if (result["not_found_label_says_own_county"] + result["not_found_label_says_other_county"]
            + result["not_found_label_county_unreadable"] != result["not_found_on_six_counties_school_pages"]):
        raise ValueError(f"{county}: school-label categories do not add up")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="save name-free CSV and plain-language report")
    args = parser.parse_args(argv)
    print("OFFLINE ONLY: verifying six counties' saved school pages; no network request", flush=True)
    exact, name_and_score = school_indexes()
    results = [audit_county(county, exact, name_and_score) for county in TARGET_COUNTIES]
    for row in results:
        print(f"{row['county']}: {row['county_applicants']} county-list applicants; "
              f"{row['exact_own_county_school_page']} on own-county school pages; "
              f"{row['exact_other_checked_county_school_page']} on another checked county's school pages; "
              f"{row['not_found_on_six_counties_school_pages']} not located on the six checked counties' school pages "
              f"({row['not_found_label_says_own_county']} labeled own-county origin, "
              f"{row['not_found_label_says_other_county']} labeled another-county origin)", flush=True)
    if args.save:
        OUT.mkdir(parents=True, exist_ok=True)
        csv_path = OUT / "reverse_applicant_school_page_check.csv"
        save_csv(csv_path, FIELDS, results)
        lines = [
            "# Arad and Sibiu: reverse applicant-list check", "",
            "This is an offline check of saved 2001 Romanian Ministry admissions webpages. It asks whether each person on an Arad or Sibiu **county-wide applicant webpage** also appears on a saved **originating-gymnasium applicant webpage**. We have school webpages for six counties: Alba, Caraș-Severin, Galați, Tulcea, Arad, and Sibiu. No new webpage was requested; no HERO or peer-effect analysis was run.", "",
            "A match requires the printed name, admission score, national-exam score, and grades 5–8 average to agree. The printed name is not a unique student identifier. Only county-level counts are saved here; no names or individual scores are exported.", "",
        ]
        for row in results:
            lines += [
                f"## {row['county']}", "",
                f"The county-wide applicant webpages list **{row['county_applicants']:,}** people. **{row['exact_own_county_school_page']:,}** have one exact match on a school webpage in this county; **{row['exact_other_checked_county_school_page']:,}** have one exact match on a school webpage in another of the six checked counties.", "",
                f"**{row['not_found_on_six_counties_school_pages']:,}** were not located on any of those six counties' school webpages. The county list prints a school label with an origin-county suffix (for example, `/ AR`). **{row['not_found_label_says_other_county']:,}** of the unmatched rows are labeled as originating in another county, whose school page may not be among the six counties collected. **{row['not_found_label_says_own_county']:,}** are labeled as originating in this county and require a closer source check. For **{row['not_found_label_county_unreadable']:,}**, the origin-county suffix could not be read. These labels are evidence supplied by the archived county list; we have not inferred a school code from the name.", "",
                f"Additional comparison limits: **{row['ambiguous_school_page_match']:,}** matched more than one school-page row; **{row['same_name_and_admission_score_but_components_disagree']:,}** shared a name and admission score but had different score components; **{row['missing_comparison_fields']:,}** lacked a field needed for this comparison.", "",
            ]
        lines += [
            "## What this check settles—and what it does not", "",
            "The county applicant lists and saved school pages overlap strongly, but they are not interchangeable inventories. A county-wide list can include applicants whose originating gymnasium is elsewhere. A school webpage contains this admissions round's participating applicants, not necessarily every eighth grader at the school. Before treating unmatched county rows as missing source data, inspect their printed school labels and whether their origin lies outside the six checked counties. Do not code an unmatched row as unsuccessful.", "",
        ]
        report = OUT / "reverse_applicant_school_page_check.md"
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"SAVED name-free counts: {csv_path}", flush=True)
        print(f"SAVED explanation: {report}", flush=True)
    return results


if __name__ == "__main__":
    main()
