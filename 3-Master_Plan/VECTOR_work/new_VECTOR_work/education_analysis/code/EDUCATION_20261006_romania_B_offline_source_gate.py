"""Offline Bucharest 2001 source check; exports aggregates only.

This verifies saved Ministry pages and compares printed names and scores in
memory. A match is provisional because the archive masks the personal ID.
No network request, selection outcome, or peer-effect calculation occurs.
"""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    family_status, placement_status, saved_rows, verified_program_rows,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, components, name_score, saved_national_indexes,
)

COUNTY = "B"
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_bucharest_expansion_20261005"


def audit():
    # Each originating-school page is checked against its saved URL, row count,
    # and content hashes by the existing school-page verifier.
    school_by_county, directory_counts = all_gymnasium_rows([COUNTY])
    school_rows = school_by_county[COUNTY]
    manifest = json.loads((CACHE / "county_manifests/B.json").read_text())
    progress = placement_status()[COUNTY]

    family = {}
    for label in ("candidate_roster", "admitted_placements", "unassigned_applicants"):
        complete, unresolved = family_status(manifest, label)
        family[label] = {"complete": complete, "unresolved_pages": unresolved,
                         "saved_rows": len(saved_rows(manifest, label))}

    if progress["state"] != "placement_views_reconciled" or int(progress["unresolved_programs"]):
        raise ValueError("B program recovery has not passed its saved source check")
    # The recovered 297 reports cover the missing portion of Bucharest's
    # placement view. The county page and program page can contain the same
    # student, so take the larger multiplicity for each printed identity.
    program_rows = verified_program_rows(COUNTY, int(progress["verified_programs"]))
    original_rows = saved_rows(manifest, "admitted_placements")
    original = Counter(name_score(row) for row in original_rows if name_score(row))
    recovered = Counter(name_score(row) for row in program_rows if name_score(row))
    placement = original | recovered
    if sum(placement.values()) != int(progress["occupancy_admitted"]):
        raise ValueError("B combined placement rows differ from the published admitted total")

    school = Counter(key for _code, key, _comp in school_rows if key)
    county_candidate = saved_rows(manifest, "candidate_roster")
    candidate = Counter(name_score(row) for row in county_candidate if name_score(row))
    unassigned = Counter(name_score(row, "Media admitere")
                         for row in saved_rows(manifest, "unassigned_applicants")
                         if name_score(row, "Media admitere"))
    candidate_components = {name_score(row): components(row) for row in county_candidate
                            if candidate[name_score(row)] == 1}

    tally = Counter()
    for _code, key, comp in school_rows:
        if key is None:
            tally["school_rows_without_match_key"] += 1
            continue
        if school[key] != 1:
            tally["school_rows_with_repeated_key"] += 1
            continue
        if candidate[key] == 1 and comp is not None and comp == candidate_components.get(key):
            tally["exact_saved_county_candidate_matches"] += 1
        elif candidate[key] > 1:
            tally["ambiguous_saved_county_candidate_matches"] += 1
        elif candidate[key] == 1:
            tally["county_candidate_component_mismatches"] += 1
        else:
            tally["not_on_saved_county_candidate_pages"] += 1

        found = placement[key] + unassigned[key]
        if found == 1 and placement[key]:
            tally["one_saved_B_placement"] += 1
        elif found == 1:
            tally["one_saved_B_unassigned"] += 1
        elif found > 1:
            tally["multiple_saved_B_outcome_rows"] += 1
        else:
            tally["no_saved_B_outcome_row"] += 1

    comparable = (len(school_rows) - tally["school_rows_without_match_key"]
                  - tally["school_rows_with_repeated_key"])
    if sum(tally[k] for k in ("one_saved_B_placement", "one_saved_B_unassigned",
                              "multiple_saved_B_outcome_rows", "no_saved_B_outcome_row")) != comparable:
        raise ValueError("Outcome categories fail to account for comparable school rows")

    # Search the other 40 counties' saved applicant/placement/unassigned views.
    # This check does not assume their archived page families are complete.
    _applicants, national_placements, national_unassigned, _coverage = saved_national_indexes([])
    for _code, key, _comp in school_rows:
        if key is None or school[key] != 1 or placement[key] + unassigned[key]:
            continue
        other_placed = [county for county in national_placements[key] if county != COUNTY]
        other_unassigned = [county for county in national_unassigned[key] if county != COUNTY]
        if len(other_placed) == 1 and not other_unassigned:
            tally["one_saved_other_county_placement"] += 1
        elif len(other_unassigned) == 1 and not other_placed:
            tally["one_saved_other_county_unassigned"] += 1
        elif other_placed or other_unassigned:
            tally["multiple_saved_other_county_outcome_rows"] += 1
        else:
            tally["no_saved_outcome_in_41_counties"] += 1
    if sum(tally[k] for k in ("one_saved_other_county_placement",
                              "one_saved_other_county_unassigned",
                              "multiple_saved_other_county_outcome_rows",
                              "no_saved_outcome_in_41_counties")) != tally["no_saved_B_outcome_row"]:
        raise ValueError("Other-county outcome categories do not sum to unmatched B rows")

    return {
        "county": COUNTY, "verified_gymnasium_pages": directory_counts[COUNTY],
        "gymnasium_applicant_rows": len(school_rows),
        "recovered_program_reports": int(progress["verified_programs"]),
        "recovered_program_rows": len(program_rows),
        "county_placement_rows_saved": len(original_rows),
        "combined_B_placement_rows": sum(placement.values()),
        "published_B_admitted_total": int(progress["occupancy_admitted"]),
        **{f"{kind}_{field}": value for kind, state in family.items()
           for field, value in state.items()},
        **{key: tally[key] for key in (
            "school_rows_without_match_key", "school_rows_with_repeated_key",
            "exact_saved_county_candidate_matches", "ambiguous_saved_county_candidate_matches",
            "county_candidate_component_mismatches", "not_on_saved_county_candidate_pages",
            "one_saved_B_placement", "one_saved_B_unassigned",
            "multiple_saved_B_outcome_rows", "no_saved_B_outcome_row",
            "one_saved_other_county_placement", "one_saved_other_county_unassigned",
            "multiple_saved_other_county_outcome_rows", "no_saved_outcome_in_41_counties")},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="save aggregate CSV and report")
    args = parser.parse_args(argv)
    print("Checking saved Bucharest sources offline; no web requests.", flush=True)
    row = audit()
    print(f"Verified {row['verified_gymnasium_pages']} school pages with "
          f"{row['gymnasium_applicant_rows']:,} applicant rows.", flush=True)
    print(f"Saved Bucharest outcome rows: {row['one_saved_B_placement']:,} placed, "
          f"{row['one_saved_B_unassigned']:,} unassigned, "
          f"{row['no_saved_B_outcome_row']:,} not located here.", flush=True)
    print(f"Of those {row['no_saved_B_outcome_row']:,}: "
          f"{row['one_saved_other_county_placement']:,} placed in another county, "
          f"{row['one_saved_other_county_unassigned']:,} unassigned in another county, "
          f"{row['no_saved_outcome_in_41_counties']:,} not located in saved reports.", flush=True)
    if args.save:
        OUT.mkdir(parents=True, exist_ok=True)
        csv_path = OUT / "B_offline_source_gate.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(row))
            writer.writeheader()
            writer.writerow(row)
        report = OUT / "B_offline_source_gate.md"
        report.write_text(
            "# Bucharest 2001: saved admissions source check\n\n"
            "This check reads saved Romanian Ministry admissions webpages without making a web request. "
            "It saves aggregate counts only; printed names and scores remain in memory. "
            "A printed name and admission score are provisional evidence of a match because the archived personal identifier is masked.\n\n"
            f"The **Gymnasium Applicant View** has {row['verified_gymnasium_pages']:,} verified "
            f"originating-school webpages with {row['gymnasium_applicant_rows']:,} applicant rows. "
            "These describe participants in this admissions round, not necessarily every eighth grader at those schools.\n\n"
            f"The **Placement View** combines {row['county_placement_rows_saved']:,} rows on saved "
            f"county placement webpages with {row['recovered_program_rows']:,} rows from "
            f"{row['recovered_program_reports']:,} separately saved program placement webpages. "
            "Repeated records appearing in both views are counted once. The combined "
            f"{row['combined_B_placement_rows']:,} records equal the published admitted total "
            f"of {row['published_B_admitted_total']:,}. This verifies the Bucharest placement "
            "source at the aggregate level.\n\n"
            f"Among the school-page rows, {row['one_saved_B_placement']:,} have exactly one "
            f"matching Bucharest placement record; {row['one_saved_B_unassigned']:,} have exactly one "
            f"matching saved Bucharest unassigned record; {row['multiple_saved_B_outcome_rows']:,} "
            f"have multiple possible saved outcome rows; and {row['no_saved_B_outcome_row']:,} "
            "have no saved Bucharest outcome row. A person in the last group might have an "
            "out-of-county outcome or appear on an unresolved source webpage. Of those, "
            f"{row['one_saved_other_county_placement']:,} have one placement in another county, "
            f"{row['one_saved_other_county_unassigned']:,} have one other-county unassigned row, "
            f"{row['multiple_saved_other_county_outcome_rows']:,} have ambiguous other-county "
            f"reports, and {row['no_saved_outcome_in_41_counties']:,} have no outcome in any of "
            "the 41 saved county report sets. The latter remain unresolved and must not be "
            "counted as unsuccessful.\n\n"
            f"The saved **County Applicant View** contains {row['candidate_roster_saved_rows']:,} "
            f"rows, of which {row['exact_saved_county_candidate_matches']:,} match a school-page "
            "row on printed name, admission score, exam score, and grades 5–8 average. "
            f"{row['not_on_saved_county_candidate_pages']:,} school-page rows do not appear "
            "in the saved county applicant pages. This comparison is limited by the missing pages.\n\n"
            "## Open source questions\n\n"
            f"County applicant pages complete: **{row['candidate_roster_complete']}**; "
            f"unresolved pages: **{row['candidate_roster_unresolved_pages']}**. "
            f"Unassigned pages complete: **{row['unassigned_applicants_complete']}**; "
            f"unresolved pages: **{row['unassigned_applicants_unresolved_pages']}**. "
            "The original county placement page series also has an unresolved page, although "
            "the recovered program reports reconcile the combined placement records to the "
            "published admitted total. Recover or account for the missing county applicant and "
            "unassigned pages, then review applicants with no outcome in the saved county reports. "
            "Do not run a Bucharest HERO or congestion analysis from these counts.\n",
            encoding="utf-8",
        )
        print(f"Saved {csv_path} and {report}", flush=True)
    return row


if __name__ == "__main__":
    main()
