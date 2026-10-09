"""Offline Bucharest source gate for the existing descriptive plots.

This reads verified private Ministry checkpoints and returns only in-memory
person keys plus name-free counts. It makes no web requests or research plots.
The printed name and admission score are provisional matching keys because
the public archive masks the personal identifier.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    county_suffix, marked_unassigned, rows, school_code,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import name_score

OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_bucharest_expansion_20261005"
GATE = OUT / "B_school_result_plot_source_gate.json"


def verify_bucharest(gym_rows, local_reports, national_placements):
    """Reconcile each B applicant with their own school's result and placements.

    Returns a private, in-memory outcome map and aggregate audit counts. The
    extra result-only rows are kept outside the gymnasium applicant cohort.
    """
    state = views.load_status()["counties"]["B"]
    result_pages, missing = rows("B", "school_results", state["school_results"])
    if missing or state["school_results"]["unresolved"]:
        raise ValueError("B school-result webpages remain unresolved")
    by_school = defaultdict(list)
    directory = 0
    for relative, page in result_pages:
        if relative.lower().startswith("raport_scoli_din_judet_tot"):
            directory += 1
            continue
        code = school_code(relative)
        if not code:
            raise ValueError("B school-result webpage has no source school code")
        for row in page["rows"]:
            by_school[(code, name_score(row))].append(row)
    # Fourteen directory schools have no applicants in the score-bearing view.
    # Their result pages remain part of the source audit but not the cohort.
    if directory != 1 or not {code for code, *_ in gym_rows}.issubset(
            {code for code, _ in by_school}):
        raise ValueError("B school-result pages do not cover applicant schools")

    local = Counter(name_score(row) for row in local_reports)
    incoming_pages, missing = rows("B", "incoming_admitted", state["incoming_admitted"])
    if missing or state["incoming_admitted"]["unresolved"]:
        raise ValueError("B incoming-admitted webpages remain unresolved")
    incoming = Counter(name_score(row) for _, page in incoming_pages for row in page["rows"])
    if any(n != 1 or local[key] != 1 for key, n in incoming.items()):
        raise ValueError("B incoming admissions do not link uniquely to local placement reports")

    applicant_keys = Counter(key for _, key, _ in gym_rows)
    if None in applicant_keys or any(n != 1 for n in applicant_keys.values()):
        raise ValueError("B applicant matching key is missing or repeated")
    if local.keys() & incoming.keys() & applicant_keys.keys():
        raise ValueError("B incoming admission also appears as a B-origin applicant")
    outcome = {}
    tally = Counter()
    for code, key, _ in gym_rows:
        found = by_school[(code, key)]
        if not found:
            raise ValueError("B applicant has no result on their own school's webpage")
        statuses = set()
        for row in found:
            if marked_unassigned(row):
                statuses.add("unassigned")
            elif destination := county_suffix(row.get("Liceu")):
                if destination == "B":
                    raise ValueError("B result has an external suffix naming B")
                statuses.add("external")
            else:
                statuses.add("local")
        if local[key] == 1:
            if "local" not in statuses or "external" in statuses:
                raise ValueError("B local placement contradicts the school-result webpage")
            status = "local"
            if "unassigned" in statuses:
                tally["local_with_extra_unassigned_result"] += 1
        elif local[key] == 0 and len(statuses) == 1:
            status = next(iter(statuses))
            if status == "local":
                raise ValueError("B school-result local placement missing from program reports")
            if status == "unassigned" and national_placements[key]:
                raise ValueError("B unassigned school result contradicts a national placement")
            if status == "external" and not any(c != "B" for c in national_placements[key]):
                raise ValueError("B external placement absent from national destination reports")
        else:
            raise ValueError("B applicant has ambiguous placement/result evidence")
        outcome[key] = status
        tally[status] += 1
    if tally["local"] + tally["unassigned"] + tally["external"] != len(gym_rows):
        raise ValueError("B applicant outcomes do not add to the school-page cohort")
    if tally["local"] + sum(incoming.values()) != len(local_reports):
        raise ValueError("B own-origin and incoming admissions do not add to occupancy")
    tally["origin_applicants"] = len(gym_rows)
    tally["local_placement_reports"] = len(local_reports)
    tally["incoming_admitted"] = sum(incoming.values())
    tally["school_result_only_rows"] = sum(map(len, by_school.values())) - len(gym_rows)
    return outcome, dict(tally)


def save_aggregate_gate(tally):
    """Write only counts; no names, scores, or row-level data leave memory."""
    OUT.mkdir(parents=True, exist_ok=True)
    GATE.write_text(json.dumps(tally, indent=2, sort_keys=True) + "\n", encoding="utf-8")
