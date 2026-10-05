"""Offline AR/SB program-source check under the frozen four-county rule.

No Wayback requests and no HERO or peer-effect calculations. Saved names and
scores are compared in memory only; outputs contain county-level counts.
"""

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation as school_audit
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status
from EDUCATION_20261003_romania_four_county_program_identity_gate import clean, local_placement_rows
from EDUCATION_20261004_romania_four_county_pilot import (
    Settings, _destination_options, _program_catalog, _winner_codes,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import name_score


COUNTIES = ("AR", "SB")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_county_expansion_20261004"
FIELDS = (
    "county", "top_cutoff_tiers", "gymnasium_applicants", "local_placements",
    "programs", "fully_occupied_programs", "all_program_places", "all_program_admitted",
    "placement_rows", "winning_programs", "winning_program_places",
    "unique_program_placements", "multiple_possible_programs",
    "multiple_programs_certain_success", "multiple_programs_certain_nonsuccess",
    "multiple_programs_success_uncertain", "program_identity_not_found",
)


def audit():
    school_audit.COUNTIES = COUNTIES
    gymnasiums, _ = school_audit.all_gymnasium_rows()
    progress = placement_status()
    results = []
    for county in COUNTIES:
        manifest, programs, catalog = _program_catalog(county)
        reports = local_placement_rows(manifest, county, progress, programs)
        if len(reports) != sum(p["admitted"] for p in catalog.values()):
            raise ValueError(f"{county}: placement rows disagree with admitted totals")
        by_person = defaultdict(list)
        for report in reports:
            key = name_score(report)
            if key is None:
                raise ValueError(f"{county}: blank placement name or admission score")
            by_person[key].append(report)
        by_identity = defaultdict(list)
        for code, program, *_ in programs:
            key = tuple(clean(program[field]) for field in ("Liceu", "Profil", "Specializare"))
            by_identity[key].append(code)
        placements = []
        for _school_code, key, _scores in gymnasiums[county]:
            if len(by_person[key]) == 1:
                placements.append(by_person[key][0])
            elif len(by_person[key]) > 1:
                raise ValueError(f"{county}: ambiguous person-to-placement link")
        for tier in (1, 2):
            winners = _winner_codes(catalog, tier, Settings())
            tally = Counter()
            for report in placements:
                options = _destination_options(report, county, catalog, by_identity)
                if not options:
                    tally["program_identity_not_found"] += 1
                elif len(options) == 1:
                    tally["unique_program_placements"] += 1
                else:
                    tally["multiple_possible_programs"] += 1
                    possible = {code in winners for code in options}
                    category = ("multiple_programs_success_uncertain" if len(possible) == 2
                                else "multiple_programs_certain_success" if True in possible
                                else "multiple_programs_certain_nonsuccess")
                    tally[category] += 1
            if (tally["unique_program_placements"] + tally["multiple_possible_programs"]
                    + tally["program_identity_not_found"] != len(placements)):
                raise ValueError(f"{county}: placement categories do not add up")
            if (tally["multiple_programs_certain_success"]
                    + tally["multiple_programs_certain_nonsuccess"]
                    + tally["multiple_programs_success_uncertain"]
                    != tally["multiple_possible_programs"]):
                raise ValueError(f"{county}: ambiguous-program categories do not add up")
            result = {field: tally[field] for field in FIELDS}
            result.update(county=county, top_cutoff_tiers=tier,
                          gymnasium_applicants=len(gymnasiums[county]),
                          local_placements=len(placements), programs=len(catalog),
                          fully_occupied_programs=sum(p["places"] > 0 and p["vacancies"] == 0
                                                       for p in catalog.values()),
                          all_program_places=sum(p["places"] for p in catalog.values()),
                          all_program_admitted=sum(p["admitted"] for p in catalog.values()),
                          placement_rows=len(reports), winning_programs=len(winners),
                          winning_program_places=sum(catalog[code]["places"] for code in winners))
            results.append(result)
            print(f"{county} top {tier}: {len(winners)} qualifying programs; "
                  f"{tally['multiple_possible_programs']} placements have multiple possible codes "
                  f"({tally['multiple_programs_certain_success']} certain success, "
                  f"{tally['multiple_programs_certain_nonsuccess']} certain nonsuccess, "
                  f"{tally['multiple_programs_success_uncertain']} uncertain)", flush=True)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="save name-free counts and explanation")
    args = parser.parse_args(argv)
    print("OFFLINE PROGRAM GATE: no Wayback request, HERO plot, or peer-effect calculation", flush=True)
    rows = audit()
    if args.save:
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / "AR_SB_program_outcome_gate.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        lines = [
            "# Arad and Sibiu: program outcome source check", "",
            "This offline audit applies the four-county pilot's frozen definition: the highest one or two **distinct cutoff tiers** within each of the original six program subjects, considering only programs with every seat filled. A tie can put multiple programs in a tier. Actual recorded placement is required. The applicant's program preference list is unavailable, so these counts do not measure the institution's applicant-to-seat ratio.", "",
            "The archived Program Directory identifies programs; the Program Occupancy webpage gives seats, admitted students, vacancies, and the last admitted score. Both counties' program tables balance (seats = admitted + vacancies), and saved local placement rows equal the admitted totals. When a placement row names several possible programs, we compare the top-program yes/no result under *every* possible program code. We never guess a code.", "",
        ]
        for row in rows:
            lines += [
                f"## {row['county']}: top {row['top_cutoff_tiers']} cutoff tier(s)", "",
                f"There are **{row['programs']}** listed programs, including **{row['fully_occupied_programs']}** fully occupied programs. **{row['winning_programs']}** programs qualify for the specified top tier(s), containing **{row['winning_program_places']:,}** seats. All programs together list **{row['all_program_places']:,}** seats and **{row['all_program_admitted']:,}** admitted students; the saved local Placement View contains exactly **{row['placement_rows']:,}** rows.", "",
                f"Among **{row['local_placements']:,}** locally placed applicants from the recovered gymnasium pages, **{row['unique_program_placements']:,}** connect to one program code. **{row['multiple_possible_programs']:,}** connect to several possible codes: **{row['multiple_programs_certain_success']:,}** are top-program successes under every possible code, **{row['multiple_programs_certain_nonsuccess']:,}** are nonsuccesses under every possible code, and **{row['multiple_programs_success_uncertain']:,}** could switch yes/no depending on the code. **{row['program_identity_not_found']:,}** placements matched no program identity.", "",
            ]
        lines += [
            "## Interpretation", "",
            "The program and placement source structures support the same *definition* used in the four-county pilot. Any applicants whose possible program codes disagree on the top-program label must remain outside a definite yes/no outcome until resolved or be handled with explicit uncertainty bounds. Capacity is an observed feature of each program, but the number who sought that program is not observed; do not call the observed success fraction the institution's K/N. No HERO curve or causal congestion estimate was produced here.", "",
            "## Why targeted recovery was needed (before program-page reconciliation)", "",
            "In **Arad**, the county-wide Placement View prints the same school, technical profile, and technological subject for two programs at Colegiul Economic Arad. The Program Directory distinguishes a **day program** (code `x70`, 125 admitted, cutoff 8.25) from an **evening program** (code `x69`, 25 admitted, cutoff 7.09). The former qualifies for both top-one and top-two under the frozen full-program rule; the latter does not. Before targeted program-page recovery, the missing program code left 149 originating-Arad applicants' labels uncertain. The counts above report the current saved-source result.", "",
            "In **Sibiu**, three technological programs at Şcoala Naţională de Gaz Mediaş share the Placement View's school, technical profile, and subject. The Program Directory distinguishes **Romanian** (code `x95`, 75 admitted, cutoff 7.84), **German** (code `x93`, 25 admitted, cutoff 6.22), and **Hungarian** (code `x94`, 20 admitted with five vacancies, cutoff 5.91). None qualifies for top one, so the original program ambiguity did not change that outcome. For top two, the Romanian program qualifies while the others do not; before targeted recovery, 114 applicants had uncertain labels. The counts above report the current saved-source result.", "",
            "The narrow source-recovery target is the archived **program-specific admitted-student webpage** for these five codes. A recovered page must carry the correct source URL code and its student-row count must equal the Program Occupancy admitted count. Only then may we link its printed names and admission scores to the county-wide Placement View. We must not assign a person to a program merely because their score exceeds a cutoff.", "",
        ]
        lines += ["## Current closeout result", ""]
        for row in rows:
            remaining = row["multiple_programs_success_uncertain"] + row["program_identity_not_found"]
            lines.append(f"- {row['county']}, top {row['top_cutoff_tiers']}: **{remaining} local placement labels still unresolved** under this definition.")
        lines += ["", "Zero unresolved labels closes this particular local-program labeling issue. It does not establish complete eighth-grade cohorts, program preferences, causal identification, or authorize a new outcome analysis.", ""]
        report = OUT / "AR_SB_program_outcome_gate.md"
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"SAVED {path} and {report}", flush=True)
    return rows


if __name__ == "__main__":
    main()
