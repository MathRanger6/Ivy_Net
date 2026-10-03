"""Reconcile four counties' saved 2001 gymnasium webpages with other saved reports.

Offline source audit only: no Wayback requests, HERO curve, or research outcome.
Names, scores, and raw HTML are read into memory but never written or printed.
The exported CSV contains county counts only. Matching printed name and score
is corroboration, not proof of unique student identity; CNP is source-masked.
"""

import argparse
import base64
import csv
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE, canonical_bytes, verified_page
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    family_status, placement_status, saved_rows, verified_program_rows,
)
from EDUCATION_20261001_romania_origin_school_name_audit import save_csv
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import PAGES

COUNTIES = ("AB", "CS", "GL", "TL")
ALBA_PAGES = Path.home() / "Desktop/VECTOR_temp/romania_alba_2001_differentiation_v1/school_reports"
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_four_county_source_pilot"
CSV = OUT / "full_gymnasium_reconciliation.csv"
REPORT = OUT / "full_gymnasium_reconciliation.md"
FIELDS = (
    "county", "directory_gymnasiums", "verified_gymnasium_pages", "gymnasium_applicant_rows",
    "gymnasium_rows_without_name_or_admission_score", "name_score_repeated_in_gymnasium_pages",
    "applicant_exact_same_county", "applicant_exact_other_county",
    "applicant_name_score_components_disagree", "applicant_name_score_ambiguous",
    "applicant_not_found_in_saved_county_lists", "applicant_not_found_but_outcome_located",
    "applicant_not_found_and_outcome_not_found", "applicant_ambiguous_gymnasium_key",
    "one_placement_report_same_county", "one_placement_report_other_county",
    "one_unassigned_report_same_county", "one_unassigned_report_other_county",
    "outcome_name_score_ambiguous", "outcome_not_found_in_saved_reports",
    "outcome_ambiguous_gymnasium_key", "county_applicant_pages_complete",
    "county_unassigned_pages_complete", "county_placement_source_status",
)


def number(value):
    """Compare numeric scores without treating 9,50 and 9.5 as different."""
    value = str(value or "").strip().replace(",", ".")
    try:
        return Decimal(value) if value else None
    except InvalidOperation:
        return None


def name_score(row, field="Medie Admitere"):
    name = " ".join(str(row.get("Nume", "")).split())
    score = number(row.get(field))
    return (name, score) if name and score is not None else None


def components(row):
    exam = number(row.get("Medie Capacitate"))
    school_grade = number(row.get("Medie Absolvire"))
    return (exam, school_grade) if exam is not None and school_grade is not None else None


def alba_school_page(code, relative):
    """Verify the original Alba checkpoint format, including both hashes."""
    path = ALBA_PAGES / f"school_{int(code):03d}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if (value.get("schema_version") != 1 or value.get("source_code") != code
            or value.get("candidate_report") != relative):
        raise ValueError(f"AB gymnasium {code}: saved source identity disagrees")
    rows = value.get("rows")
    if not isinstance(rows, list) or value.get("row_count") != len(rows):
        raise ValueError(f"AB gymnasium {code}: saved row count disagrees")
    if hashlib.sha256(canonical_bytes(rows)).hexdigest() != value.get("rows_sha256"):
        raise ValueError(f"AB gymnasium {code}: row hash disagrees")
    raw = base64.b64decode(value.get("raw_html_base64", ""), validate=True)
    if hashlib.sha256(raw).hexdigest() != value.get("raw_html_sha256"):
        raise ValueError(f"AB gymnasium {code}: raw-page hash disagrees")
    return value


def all_gymnasium_rows():
    """Verify every directory-listed school page before trusting its rows."""
    result = defaultdict(list)
    counts = {}
    for county in COUNTIES:
        directory = school_directory(county)
        for code, (_name, relative) in directory.items():
            if county == "AB":
                page = alba_school_page(code, relative)
            else:
                path = PAGES / f"{county}_{code}.json"
                kind = json.loads(path.read_text(encoding="utf-8"))["kind"]
                if kind not in {"sampled_origin_school_candidates", "origin_school_candidates"}:
                    raise ValueError(f"{county} gymnasium {code}: unexpected report kind")
                page = verified_page(path, relative=relative, kind=kind)
            for row in page["rows"]:
                result[county].append((code, name_score(row), components(row)))
        counts[county] = len(directory)
        print(f"VERIFIED {county}: {len(directory)} gymnasium pages, "
              f"{len(result[county])} applicant rows", flush=True)
    return result, counts


def saved_national_indexes():
    """Index saved county reports; never infer absence from an incomplete view."""
    applicants = defaultdict(list)
    placements = defaultdict(list)
    unassigned = defaultdict(list)
    coverage = {}
    progress = placement_status()
    paths = sorted((CACHE / "county_manifests").glob("*.json"))
    for position, path in enumerate(paths, 1):
        county = path.stem
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for row in saved_rows(manifest, "candidate_roster"):
            if key := name_score(row):
                applicants[key].append((county, components(row)))
        original = saved_rows(manifest, "admitted_placements")
        original_keys = Counter(key for row in original if (key := name_score(row)))
        state = progress.get(county, {}).get("state", "unresolved")
        placement_complete, placement_gaps = family_status(manifest, "admitted_placements")
        source_status = ("original_county_pages_complete" if placement_complete and not placement_gaps
                         else "recovered_program_views_reconciled" if state == "placement_views_reconciled"
                         else "placement_pages_unresolved")
        if state == "placement_views_reconciled":
            expected = int(progress[county]["verified_programs"])
            recovered = Counter(key for row in verified_program_rows(county, expected)
                                if (key := name_score(row)))
            original_keys += recovered - original_keys  # Same report row may appear in both views.
        for key, count in original_keys.items():
            placements[key].extend([county] * count)
        for row in saved_rows(manifest, "unassigned_applicants"):
            if key := name_score(row, "Media admitere"):
                unassigned[key].append(county)
        if county in COUNTIES:
            candidate_complete, candidate_gaps = family_status(manifest, "candidate_roster")
            unassigned_complete, unassigned_gaps = family_status(manifest, "unassigned_applicants")
            if candidate_gaps or unassigned_gaps:
                raise ValueError(f"{county}: county report has unresolved pages")
            coverage[county] = (candidate_complete, unassigned_complete, source_status)
        if position % 10 == 0 or position == len(paths):
            print(f"INDEXED {position}/{len(paths)} saved county report sets", flush=True)
    return applicants, placements, unassigned, coverage


def evaluate(gymnasiums, directories, applicants, placements, unassigned, coverage):
    all_keys = Counter(key for rows in gymnasiums.values() for _code, key, _comp in rows
                       if key is not None)
    output = []
    for county in COUNTIES:
        tally = Counter()
        for _code, key, comp in gymnasiums[county]:
            if key is None:
                tally["gymnasium_rows_without_name_or_admission_score"] += 1
                continue
            if all_keys[key] > 1:
                tally["name_score_repeated_in_gymnasium_pages"] += 1
                tally["applicant_ambiguous_gymnasium_key"] += 1
                tally["outcome_ambiguous_gymnasium_key"] += 1
                continue
            peers = applicants[key]
            if len(peers) == 0:
                tally["applicant_not_found_in_saved_county_lists"] += 1
            elif len(peers) > 1:
                tally["applicant_name_score_ambiguous"] += 1
            elif comp is None or peers[0][1] is None or comp != peers[0][1]:
                tally["applicant_name_score_components_disagree"] += 1
            else:
                where = "same_county" if peers[0][0] == county else "other_county"
                tally[f"applicant_exact_{where}"] += 1

            found_placement = placements[key]
            found_unassigned = unassigned[key]
            if not peers:
                category = ("applicant_not_found_but_outcome_located"
                            if len(found_placement) + len(found_unassigned) == 1
                            else "applicant_not_found_and_outcome_not_found")
                tally[category] += 1
            if len(found_placement) + len(found_unassigned) == 0:
                tally["outcome_not_found_in_saved_reports"] += 1
            elif len(found_placement) + len(found_unassigned) != 1:
                tally["outcome_name_score_ambiguous"] += 1
            elif found_placement:
                where = "same_county" if found_placement[0] == county else "other_county"
                tally[f"one_placement_report_{where}"] += 1
            else:
                where = "same_county" if found_unassigned[0] == county else "other_county"
                tally[f"one_unassigned_report_{where}"] += 1
        candidate_complete, unassigned_complete, placement_state = coverage[county]
        row = {field: tally[field] for field in FIELDS}
        row.update(county=county, directory_gymnasiums=directories[county],
                   verified_gymnasium_pages=directories[county],
                   gymnasium_applicant_rows=len(gymnasiums[county]),
                   county_applicant_pages_complete=candidate_complete,
                   county_unassigned_pages_complete=unassigned_complete,
                   county_placement_source_status=placement_state)
        counted = (tally["gymnasium_rows_without_name_or_admission_score"]
                   + tally["applicant_ambiguous_gymnasium_key"]
                   + tally["applicant_exact_same_county"] + tally["applicant_exact_other_county"]
                   + tally["applicant_name_score_components_disagree"]
                   + tally["applicant_name_score_ambiguous"]
                   + tally["applicant_not_found_in_saved_county_lists"])
        if counted != len(gymnasiums[county]):
            raise ValueError(f"{county}: applicant categories do not sum to school rows")
        output.append(row)
        print(f"RECONCILED {county}: {len(gymnasiums[county])} school rows; "
              f"{tally['applicant_exact_same_county']} exact in own county applicant list; "
              f"{tally['applicant_exact_other_county']} exact in another county; "
              f"{tally['applicant_not_found_in_saved_county_lists']} not located there", flush=True)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="write name-free aggregate report")
    args = parser.parse_args(argv)
    print("OFFLINE SOURCE AUDIT: no Wayback requests; no individual data exported", flush=True)
    gymnasiums, directories = all_gymnasium_rows()
    applicants, placements, unassigned, coverage = saved_national_indexes()
    rows = evaluate(gymnasiums, directories, applicants, placements, unassigned, coverage)
    if not args.run:
        print("PREVIEW ONLY: no report written; add --run to save aggregates", flush=True)
        return rows
    save_csv(CSV, FIELDS, rows)
    total = lambda field: sum(row[field] for row in rows)
    lines = [
        "# Romania 2001: four-county gymnasium source reconciliation", "",
        "## What we compared", "",
        "This is an **offline audit of saved Romanian Ministry admission webpages** for Alba (AB), Caraș-Severin (CS), Galați (GL), and Tulcea (TL). No webpages were requested during this run, and no HERO or peer-effect analysis was performed.", "",
        "- **Gymnasium Applicant View:** a webpage listing the admission-round applicants from one originating gymnasium. We verified all 632 such pages listed in the four counties' origin-school directories, containing 12,945 applicant rows. These are participating applicants, not necessarily every eighth grader at each school.",
        "- **County Applicant View:** a county-wide webpage listing admission-round applicants. We checked whether each gymnasium row appears in its own county's list or another county's saved list.",
        "- **Placement and Unassigned Views:** Ministry webpages recording either a high-school/program placement or an unassigned applicant in the admission round. We checked these saved views across all 41 county report sets.", "",
        "## What the saved sources show", "",
        f"Of {total('gymnasium_applicant_rows'):,} gymnasium applicant rows, {total('applicant_exact_same_county'):,} matched the County Applicant View in the same county and {total('applicant_exact_other_county'):,} matched in another county. {total('applicant_not_found_in_saved_county_lists'):,} did not appear in the saved county applicant views; {total('applicant_not_found_but_outcome_located'):,} of those nevertheless had one placement or unassigned report row. Thus, absence from a county applicant list is not evidence that the person did not participate or obtain a place.", "",
        f"The Placement and Unassigned Views contain one matching report row for {total('one_placement_report_same_county') + total('one_placement_report_other_county') + total('one_unassigned_report_same_county') + total('one_unassigned_report_other_county'):,} of the {total('gymnasium_applicant_rows'):,} gymnasium rows. The remaining {total('outcome_not_found_in_saved_reports'):,} row remains **unresolved**; it must not be coded as an unsuccessful placement.", "",
        "The archived `CNP` identifier is masked and cannot identify a student. A printed name plus admission score is only a provisional match; for the applicant-list comparison we also required the examination score and grades 5–8 average to agree. We exported only county counts, never names or individual scores.", "",
        "| County | Gymnasium rows | Exact in own county applicant list | Exact in another county | Not in saved county applicant lists | One placement-report row | One unassigned-report row | Outcome ambiguous | Outcome not located |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['county']} | {row['gymnasium_applicant_rows']:,} | "
                     f"{row['applicant_exact_same_county']:,} | {row['applicant_exact_other_county']:,} | "
                     f"{row['applicant_not_found_in_saved_county_lists']:,} | "
                     f"{row['one_placement_report_same_county'] + row['one_placement_report_other_county']:,} | "
                     f"{row['one_unassigned_report_same_county'] + row['one_unassigned_report_other_county']:,} | "
                     f"{row['outcome_name_score_ambiguous'] + row['outcome_ambiguous_gymnasium_key']:,} | "
                     f"{row['outcome_not_found_in_saved_reports']:,} |")
    lines += ["", "The four counties' own County Applicant and Unassigned webpage series were complete in the saved archive. Their placement sources were also complete: AB and TL through the original county webpages, CS and GL through the recovered program webpages. Some other counties' saved report series are incomplete. Duplicate rows shared by original and recovered placement views were counted only once.", "",
              "## What remains unresolved", "",
              "A complete admission-round webpage series does **not** establish that every eighth grader from a gymnasium applied in this round. Name-and-score agreement does not prove unique identity. The one school row with no saved outcome report is on Galați originating-gymnasium page 186. A targeted offline search found no row with the same printed name in the saved county applicant, placement, or unassigned reports. Its status stays unresolved; a missing row is not evidence of nonplacement.", "",
              "We should not build a HERO curve or infer congestion from these counts. First we must decide whether the participating-applicant gymnasium group is the defensible peer group, and verify the selective-program outcome definition and its denominator.", "",
              "The companion CSV gives every county count and source-status flag. It contains no student-level information.", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"SAVED {CSV} and {REPORT}", flush=True)
    return rows


if __name__ == "__main__":
    main()
