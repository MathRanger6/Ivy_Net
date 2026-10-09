"""Reconcile saved 2001 source views for CT, PH, TM, and CJ, without network access.

Only county-level counts leave this process. Printed name plus admission score
is a provisional comparison key because the archived personal ID is masked.
This is a source audit, not an outcome or peer-effects analysis.
"""

import csv
from collections import Counter
from pathlib import Path

import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    count, county_suffix, marked_unassigned, multiset, rows, school_code,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import name_score


COUNTIES = ("CT", "PH", "TM", "CJ")
ALL_SAVED_COUNTIES = ("B", "AB", "CS", "GL", "TL", "AR", "SB", *COUNTIES)
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_four_new_county_source_reconciliation_20261008"
FIELDS = (
    "county", "school_result_pages", "school_result_directory_schools",
    "school_result_rows", "school_result_rows_without_name_score",
    "resident_pages_saved", "resident_pages_projected", "resident_rows_saved",
    "resident_rows_projected", "resident_source_complete",
    "resident_rows_matching_school_results", "resident_rows_absent_from_school_results",
    "school_result_rows_absent_from_saved_resident_list",
    "extra_school_results_marked_unassigned", "extra_school_results_other_status",
    "incoming_candidate_rows", "incoming_admitted_rows", "incoming_rejected_rows",
    "incoming_candidate_rows_without_outcome", "incoming_outcome_rows_without_candidate",
    "outgoing_admitted_with_destination_county",
)


def checked_rows(county, family, status):
    state = status[county][family]
    pages, missing = rows(county, family, state)
    if missing or state["unresolved"] or len(pages) != state["saved_pages"]:
        raise ValueError(f"{county}: {family} has a missing or unresolved saved page")
    if family != "resident_candidates" and len(pages) != state.get("projected_pages"):
        raise ValueError(f"{county}: {family} has fewer pages than the source projects")
    return pages


def run():
    status = views.load_status()["counties"]
    records = []
    outgoing = Counter()
    incoming_by_pair = Counter()
    incoming_without_origin = Counter()

    # Gather outgoing and incoming admissions for all eleven cached counties.
    # This comparison uses two independent Ministry views, not individual linkage.
    for county in ALL_SAVED_COUNTIES:
        result_pages = checked_rows(county, "school_results", status)
        for relative, page in result_pages:
            if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
                continue
            for row in page["rows"]:
                destination = county_suffix(row.get("Liceu"))
                if destination and destination != county:
                    outgoing[(county, destination)] += 1
        admitted_pages = checked_rows(county, "incoming_admitted", status)
        for _relative, page in admitted_pages:
            for row in page["rows"]:
                origin = county_suffix(row.get("Scoală provenienţă"))
                if origin and origin != county:
                    incoming_by_pair[(origin, county)] += 1
                else:
                    incoming_without_origin[county] += 1

    for county in COUNTIES:
        source = status[county]
        result_pages = checked_rows(county, "school_results", status)
        directory = [page for relative, page in result_pages
                     if relative.lower().startswith("raport_scoli_din_judet_tot.asp")]
        school_pages = [(relative, page) for relative, page in result_pages
                        if not relative.lower().startswith("raport_scoli_din_judet_tot.asp")]
        codes = [school_code(relative) for relative, _page in school_pages]
        if (len(directory) != 1 or None in codes or len(codes) != len(set(codes))
                or len(codes) != directory[0]["row_count"]):
            raise ValueError(f"{county}: school-result directory and school pages disagree")
        result_rows = [row for _relative, page in school_pages for row in page["rows"]]
        result = multiset(result_rows)
        no_key = len(result_rows) - count(result)

        resident_state = source["resident_candidates"]
        resident_pages, missing = rows(county, "resident_candidates", resident_state)
        resident = multiset(row for _relative, page in resident_pages for row in page["rows"])
        resident_complete = (not missing and not resident_state["unresolved"]
                             and len(resident_pages) == resident_state.get("projected_pages")
                             and count(resident) == resident_state.get("projected_records"))
        extras = result - resident
        # When the resident list is incomplete, these are merely unmatched in
        # the saved subset; their outcome status cannot be characterized here.
        extra_status = Counter()
        if resident_complete:
            remaining = extras.copy()
            for row in result_rows:
                key = name_score(row)
                if key and remaining[key]:
                    extra_status["unassigned" if marked_unassigned(row) else "other"] += 1
                    remaining[key] -= 1

        incoming = {}
        for family in ("incoming_candidates", "incoming_admitted", "incoming_rejected"):
            pages = checked_rows(county, family, status)
            incoming[family] = multiset(row for _relative, page in pages for row in page["rows"])
        outcomes = incoming["incoming_admitted"] + incoming["incoming_rejected"]
        record = {
            "county": county,
            "school_result_pages": len(school_pages),
            "school_result_directory_schools": directory[0]["row_count"],
            "school_result_rows": len(result_rows),
            "school_result_rows_without_name_score": no_key,
            "resident_pages_saved": len(resident_pages),
            "resident_pages_projected": resident_state.get("projected_pages", ""),
            "resident_rows_saved": count(resident),
            "resident_rows_projected": resident_state.get("projected_records", ""),
            "resident_source_complete": resident_complete,
            "resident_rows_matching_school_results": count(resident & result),
            "resident_rows_absent_from_school_results": count(resident - result),
            "school_result_rows_absent_from_saved_resident_list": count(extras),
            "extra_school_results_marked_unassigned": extra_status["unassigned"] if resident_complete else "",
            "extra_school_results_other_status": extra_status["other"] if resident_complete else "",
            "incoming_candidate_rows": count(incoming["incoming_candidates"]),
            "incoming_admitted_rows": count(incoming["incoming_admitted"]),
            "incoming_rejected_rows": count(incoming["incoming_rejected"]),
            "incoming_candidate_rows_without_outcome": count(incoming["incoming_candidates"] - outcomes),
            "incoming_outcome_rows_without_candidate": count(outcomes - incoming["incoming_candidates"]),
            "outgoing_admitted_with_destination_county": sum(n for (origin, _), n in outgoing.items() if origin == county),
        }
        records.append(record)
        print(f"{county}: {len(school_pages)} school-result pages, {len(result_rows):,} rows; "
              f"resident list {len(resident_pages)}/{resident_state.get('projected_pages')} pages; "
              f"incoming {record['incoming_candidate_rows']} candidates = "
              f"{record['incoming_admitted_rows']} admitted + "
              f"{record['incoming_rejected_rows']} rejected", flush=True)

    overlap = sorted((origin, destination, outgoing[(origin, destination)], incoming_by_pair[(origin, destination)])
                     for origin, destination in (set(outgoing) | set(incoming_by_pair))
                     if origin in ALL_SAVED_COUNTIES and destination in ALL_SAVED_COUNTIES
                     and (origin in COUNTIES or destination in COUNTIES))
    mismatches = [pair for pair in overlap if pair[2] != pair[3]]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "county_source_counts.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(records)
    with (OUT / "cross_county_flow_check.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("origin_county", "destination_county", "origin_result_admissions", "destination_incoming_admissions", "counts_agree"))
        writer.writerows((*pair, pair[2] == pair[3]) for pair in overlap)

    total = lambda field: sum(int(row[field]) for row in records)
    lines = [
        "# Romania 2001: four newly downloaded counties — offline source reconciliation", "",
        "This check reads saved, hash-verified Ministry webpages only. It made no archive requests. "
        "The exported files contain county counts, never names or individual scores. "
        "A printed name-and-admission-score match is provisional because the archived personal identifier is masked.", "",
        f"The four counties have **{total('school_result_pages'):,} school-result reports** containing "
        f"**{total('school_result_rows'):,} printed rows**. Every report listed by its saved school directory is present.", "",
        f"The incoming-candidate lists contain **{total('incoming_candidate_rows'):,} rows**: "
        f"**{total('incoming_admitted_rows'):,} admitted** and "
        f"**{total('incoming_rejected_rows'):,} rejected/unassigned** in their separate outcome lists. "
        f"Candidate rows lacking a matching incoming-outcome row: "
        f"**{total('incoming_candidate_rows_without_outcome')}**; outcome rows lacking an "
        f"incoming-candidate row: **{total('incoming_outcome_rows_without_candidate')}**. "
        "This compares printed name and admission score with multiplicity, not certified person identifiers.", "",
        "The county-wide resident-candidate lists are complete by their source-printed totals in "
        "PH and CJ. CT and TM still have missing archived pages; their saved rows are only a subset "
        "of their projected lists. The separate gymnasium score-component reports are checked "
        "against these school-result reports in the companion "
        "`gymnasium_result_reconciliation.md` audit. This source-view audit alone does not certify peer pools.", "",
        "## County details", "",
    ]
    for row in records:
        complete_detail = (
            f" The {row['school_result_rows_absent_from_saved_resident_list']} additional "
            f"school-result rows are marked unassigned."
            if row["resident_source_complete"]
            and row["extra_school_results_other_status"] == 0
            and row["extra_school_results_marked_unassigned"]
               == row["school_result_rows_absent_from_saved_resident_list"]
            else ""
        )
        lines.append(
            f"- **{row['county']}:** {row['school_result_pages']} school-result reports and "
            f"{row['school_result_rows']:,} rows; resident-candidate pages "
            f"{row['resident_pages_saved']}/{row['resident_pages_projected']}; "
            f"{row['resident_rows_matching_school_results']:,} saved resident rows match a "
            f"school-result row, {row['resident_rows_absent_from_school_results']} do not. "
            f"Incoming {row['incoming_candidate_rows']} = {row['incoming_admitted_rows']} "
            f"admitted + {row['incoming_rejected_rows']} rejected/unassigned."
            f"{complete_detail}"
        )
    lines += [
        "", "## Cross-county source check", "",
        f"For **{len(overlap)}** origin–destination county pairs involving at least one of these "
        f"four counties and with both counties in the eleven-county cache, "
        f"**{len(overlap) - len(mismatches)}** have equal counts in the originating county's "
        "school-result report and the destination county's incoming-admitted list. "
        f"**{len(mismatches)}** pairs differ. These are aggregate source counts, not a student-level match.", "",
        f"Incoming-admitted rows whose printed origin-school label could not be read as an external "
        f"county: **{sum(incoming_without_origin.values())}** across all eleven cached destinations.", "",
        "## What remains open", "",
        "1. Recover the missing CT and TM resident-candidate pages or retain their URL addresses as unresolved.",
        "2. Consult the companion gymnasium-to-result audit and retry any gymnasium report "
        "still listed there as unresolved before certifying complete peer pools.",
        *( ["3. Inspect the mismatching county-pair counts before treating the flows as reconciled."]
           if mismatches else [] ),
        "", "No scientific outcome, HERO plot, program ranking, or congestion analysis was run.", "",
    ]
    (OUT / "source_reconciliation.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved name-free audit: {OUT / 'source_reconciliation.md'}", flush=True)
    return records


if __name__ == "__main__":
    run()
