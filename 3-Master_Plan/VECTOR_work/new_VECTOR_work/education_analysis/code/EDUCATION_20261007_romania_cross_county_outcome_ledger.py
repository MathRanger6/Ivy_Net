"""Source audit and researcher-run local-versus-anywhere outcome comparison.

Only verified saved 2001 Ministry pages are read. Raw person-level records and
the optional ledger stay under ~/Desktop/VECTOR_temp. Repository output contains
name-free aggregate counts and plots only. No network request occurs here.

The archive masks personal IDs, so name + admission score + origin school is a
provisional source linkage. An unassigned result is not a rejection from any
particular program; preferences are not observed.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import EDUCATION_20261004_romania_four_county_pilot as pilot
import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    county_suffix, marked_unassigned, rows, school_code,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, name_score, saved_national_indexes,
)
from EDUCATION_20261003_romania_four_county_program_identity_gate import clean, source_programs
from EDUCATION_20261003_romania_four_county_program_identity_gate import local_placement_rows
from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path.home() / "Desktop/VECTOR_temp/romania_2001_outcome_ledger_v1"
OUT = ROOT / "outputs/romania_2001_seven_county_cross_county_comparison"
COUNTIES = ("AB", "CS", "GL", "TL", "AR", "SB", "B")


def _origin_results(county, source_state):
    """Index source outcomes by origin school and printed person key in memory."""
    pages, missing = rows(county, "school_results", source_state["school_results"])
    if missing or source_state["school_results"]["unresolved"]:
        raise ValueError(f"{county}: school-result source pages remain unresolved")
    result = defaultdict(list)
    for relative, page in pages:
        if relative.lower().startswith("raport_scoli_din_judet_tot"):
            continue
        code = school_code(relative)
        if not code:
            raise ValueError(f"{county}: school-result page lacks its school code")
        for row in page["rows"]:
            result[(code, name_score(row))].append(row)
    return result


def _destination_catalog(county):
    """Join destination program directory with occupancy and cutoff records."""
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    programs = source_programs(manifest, county)
    identity = defaultdict(list)
    for code, row, _places, _admitted, _vacancies, _cutoff in programs:
        identity[(clean(row["Liceu"]), clean(row["Profil"]),
                  clean(row["Specializare"]))].append(code)
    catalog = {code: {
        "code": code, "school": clean(row["Liceu"]),
        "category": clean(row["Specializare"]), "level": clean(row["Nivel"]),
        "places": places, "admitted": admitted, "vacancies": vacancies,
        "cutoff": float(cutoff) if cutoff is not None else None,
    } for code, row, places, admitted, vacancies, cutoff in programs}
    return catalog, identity


def _outcome_rows(settings):
    """Make a private in-memory ledger, preserving every unresolved source row."""
    if tuple(settings.counties) != COUNTIES:
        raise ValueError("This comparison is frozen to the seven audited origin counties")
    gyms, _directories = all_gymnasium_rows(COUNTIES)
    _applicants, national_placed, _unassigned, _coverage = saved_national_indexes(())
    source_state = views.load_status()["counties"]
    origin_pages = {county: _origin_results(county, source_state[county])
                    for county in COUNTIES}
    incoming_keys = {}
    for county in COUNTIES:
        pages, missing = rows(county, "incoming_admitted", source_state[county]["incoming_admitted"])
        if missing or source_state[county]["incoming_admitted"]["unresolved"]:
            raise ValueError(f"{county}: incoming-admitted source pages remain unresolved")
        incoming_keys[county] = Counter(name_score(row) for _url, page in pages for row in page["rows"])

    destinations = set(COUNTIES)
    for county in COUNTIES:
        for result_rows in origin_pages[county].values():
            for row in result_rows:
                destination = county_suffix(row.get("Liceu"))
                if destination and destination != county:
                    destinations.add(destination)
    catalogs = {}
    catalog_issues = {}
    for county in sorted(destinations):
        try:
            catalogs[county] = _destination_catalog(county)
        except (ValueError, KeyError) as exc:
            if county in COUNTIES:
                raise  # A failed origin-county catalog invalidates its own plot.
            catalog_issues[county] = str(exc)
    winner = {county: {tier: pilot._winner_codes(catalog, tier, settings)
                       for tier in (1, 2)}
              for county, (catalog, _identity) in catalogs.items()}
    # For students placed at home, the separately verified program-placement
    # reports often supply an exact code that the school-result page omits.
    # Reuse that source rather than treating same-label programs as mixed.
    progress = placement_status()
    home_reports = {}
    for origin in COUNTIES:
        manifest = json.loads((CACHE / "county_manifests" / f"{origin}.json").read_text())
        program_rows = source_programs(manifest, origin)
        local_rows = local_placement_rows(manifest, origin, progress, program_rows)
        by_key = defaultdict(list)
        for report in local_rows:
            by_key[name_score(report)].append(report)
        home_reports[origin] = by_key

    records = []
    audit = Counter()
    for origin in COUNTIES:
        group = gyms[origin]
        group_sizes = Counter(code for code, _key, _comp in group)
        group_sums = defaultdict(float)
        for code, _key, components in group:
            if components is None:
                raise ValueError(f"{origin}: applicant examination component absent")
            group_sums[code] += float(components[0])
        for code, key, components in group:
            source = origin_pages[origin].get((code, key), [])
            record = {"origin": origin, "gymnasium": code,
                      "exam": float(components[0]),
                      "school_grade": float(components[1]),
                      "peer_count": group_sizes[code] - 1,
                      "peer_mean_exam": ((group_sums[code] - float(components[0]))
                                         / (group_sizes[code] - 1)
                                         if group_sizes[code] > 1 else np.nan),
                      "destination": None, "program_code": None,
                      "match_status": "unresolved", "assignment": "unresolved",
                      "home_top1": np.nan, "home_top2": np.nan,
                      "any_top1": np.nan, "any_top2": np.nan}
            if not source:
                audit["missing_origin_result"] += 1
                records.append(record)
                continue
            placed = [row for row in source if not marked_unassigned(row)]
            unassigned = [row for row in source if marked_unassigned(row)]
            # One Bucharest page includes an extra unassigned line for an
            # independently verified local placement. Do not infer which line
            # belongs to the person without corroboration in the report set.
            if len(placed) == 1 and unassigned:
                destinations_seen = national_placed[key]
                if len(destinations_seen) != 1:
                    audit["conflicting_result_unresolved"] += 1
                    records.append(record)
                    continue
                audit["placement_corrob_extra_unassigned"] += 1
            elif len(placed) > 1 or (not placed and len(unassigned) != 1):
                audit["ambiguous_origin_result"] += 1
                records.append(record)
                continue
            if not placed:
                if national_placed[key]:
                    # A masked-ID name/score collision may represent another
                    # person; do not overwrite the school result or force it
                    # into the paired denominator.
                    audit["unassigned_national_key_ambiguity"] += 1
                    records.append(record)
                    continue
                record.update(assignment="unassigned", match_status="origin_result_verified",
                              home_top1=0, home_top2=0, any_top1=0, any_top2=0)
                audit["unassigned"] += 1
                records.append(record)
                continue

            row = placed[0]
            destination = county_suffix(row.get("Liceu")) or origin
            record["destination"] = destination
            record["assignment"] = "home_placed" if destination == origin else "away_placed"
            if destination != origin:
                # A placement outside the home county is definitely not a
                # placement in one of its home-county top programs.
                record["home_top1"] = 0
                record["home_top2"] = 0
            if destination not in catalogs:
                audit["destination_catalog_absent"] += 1
                records.append(record)
                continue
            if destination != origin:
                # A second, independent destination page is available for
                # movements between two of the seven fully acquired counties.
                if destination in incoming_keys and incoming_keys[destination][key] != 1:
                    audit["away_incoming_disagreement"] += 1
                    records.append(record)
                    continue
                if national_placed[key] != [destination]:
                    audit["away_national_placement_disagreement"] += 1
                    records.append(record)
                    continue
            school = clean(row.get("Liceu"))
            if destination != origin:
                school = school.rsplit(" / ", 1)[0]
            identity = (school, clean(row.get("Profil")), clean(row.get("Specializare")))
            catalog, by_identity = catalogs[destination]
            if destination == origin:
                reports = home_reports[origin][key]
                if len(reports) != 1:
                    audit["home_program_report_unresolved"] += 1
                    records.append(record)
                    continue
                options = pilot._destination_options(reports[0], origin,
                                                     catalog, by_identity)
                if not options or not set(options).issubset(set(by_identity.get(identity, []))):
                    audit["home_school_result_program_disagreement"] += 1
                    records.append(record)
                    continue
            else:
                options = by_identity.get(identity, [])
            if not options:
                audit["program_identity_unmatched"] += 1
                records.append(record)
                continue
            possible_top1 = {option in winner[destination][1] for option in options}
            possible_top2 = {option in winner[destination][2] for option in options}
            if len(possible_top1) != 1 or len(possible_top2) != 1:
                audit["program_rank_mixed"] += 1
                records.append(record)
                continue
            score = key[1]
            if not any(catalog[option]["cutoff"] is not None and
                       Decimal(str(catalog[option]["cutoff"])) <= score
                       for option in options):
                audit["program_cutoff_disagreement"] += 1
                records.append(record)
                continue
            record["program_code"] = options[0] if len(options) == 1 else None
            record["match_status"] = ("unique_program" if len(options) == 1
                                      else "rank_invariant_ambiguous_program")
            record["any_top1"] = int(next(iter(possible_top1)))
            record["any_top2"] = int(next(iter(possible_top2)))
            if destination == origin:
                record["home_top1"] = record["any_top1"]
                record["home_top2"] = record["any_top2"]
            audit[record["assignment"]] += 1
            if len(options) > 1:
                audit["rank_invariant_program_ambiguity"] += 1
            records.append(record)
    audit["origin_applicants"] = len(records)
    audit["destination_counties"] = len(destinations)
    audit["destination_catalogs_unverified"] = len(catalog_issues)
    audit["destination_catalog_county_codes_unverified"] = ",".join(sorted(catalog_issues))
    return pd.DataFrame(records), dict(audit)


def audit_sources(settings):
    """Source-only preview, no individual output and no outcome plots."""
    ledger, audit = _outcome_rows(settings)
    print("Source-only audit:", audit, flush=True)
    print("Records retained in memory:", len(ledger), flush=True)
    return audit


def _comparison_cells(ledger, settings, tier):
    """Paired rates use one common denominator, defined before looking at rates."""
    eligible = ledger.loc[(ledger["peer_count"] > 0)
                          & ledger[f"home_top{tier}"].notna()
                          & ledger[f"any_top{tier}"].notna()].copy()
    eligible["band"] = eligible["county_band"]
    cells = []
    for origin in (*COUNTIES, "ALL"):
        part = eligible if origin == "ALL" else eligible.loc[eligible["origin"] == origin]
        if part.empty:
            continue
        part = part.copy()
        part["peer_bin"] = pd.qcut(part["peer_mean_exam"], q=settings.peer_strength_bins,
                                   labels=False, duplicates="drop")
        for (band, bin_number), cell in part.groupby(["band", "peer_bin"]):
            if pd.isna(bin_number):
                continue
            cells.append({"origin": origin, "tier": tier, "band": band,
                          "peer_bin": int(bin_number) + 1,
                          "mean_peer_exam": cell["peer_mean_exam"].mean(),
                          "applicants": len(cell),
                          "gymnasiums": len(cell[["origin", "gymnasium"]].drop_duplicates()),
                          "counties": cell["origin"].nunique(),
                          "home_top_count": int(cell[f"home_top{tier}"].sum()),
                          "any_top_count": int(cell[f"any_top{tier}"].sum()),
                          "home_top_rate": cell[f"home_top{tier}"].mean(),
                          "any_top_rate": cell[f"any_top{tier}"].mean(),
                          "away_applicants": int((cell["assignment"] == "away_placed").sum())})
    return pd.DataFrame(cells), eligible


def _movement_summary(ledger, settings):
    """Show whether outward-bound applicants occupy different score ranges."""
    top_label = pilot._band_labels(settings)[3]
    output = []
    for (origin, assignment), group in ledger.groupby(["origin", "assignment"], sort=False):
        output.append({"origin": origin, "assignment": assignment,
                       "applicants": len(group),
                       "median_exam": group["exam"].median(),
                       "mean_exam": group["exam"].mean(),
                       "top_own_exam_band_count": int((group["county_band"] == top_label).sum()),
                       "top_own_exam_band_pct": (group["county_band"] == top_label).mean(),
                       "program_rank_unresolved": int(group["any_top1"].isna().sum())})
    return pd.DataFrame(output)


def _multistate_cells(eligible, tier, settings):
    """Four mutually exclusive observed states on the paired denominator."""
    data = eligible.copy()
    data["peer_bin"] = data.groupby("origin")["peer_mean_exam"].transform(
        lambda values: pd.qcut(values, q=settings.peer_strength_bins,
                               labels=False, duplicates="drop") + 1)
    data["state"] = np.select([
        data["assignment"] == "unassigned",
        data["any_top1"] == 1,
        data["any_top2"] == 1,
    ], ["unassigned", "top_one_anywhere", "top_two_only_anywhere"],
        default="other_placed_program")
    if tier == 1:
        # The four-state outcome is independent of which tier's paired curve
        # is displayed; record it once alongside the top-one comparison.
        return (data.groupby(["origin", "band", "peer_bin", "state"],
                             dropna=False).size().rename("applicants").reset_index())
    return pd.DataFrame()


def _paired_figure(cells, settings, tier, path, *, only_excellence):
    """Show home and anywhere rates at the same peer bins and denominator."""
    if only_excellence:
        locations = (*COUNTIES, "ALL")
        bands = [pilot._band_labels(settings)[2]]
        fig, axes = plt.subplots(4, 2, figsize=(17, 19), sharey=True)
        panels = [(origin, bands[0]) for origin in locations]
    else:
        bands = list(pilot._band_labels(settings))
        fig, axes = plt.subplots(2, 2, figsize=(17, 11), sharey=True)
        panels = [("ALL", band) for band in bands]
    for axis, (origin, band) in zip(axes.flat, panels):
        part = cells.loc[(cells["origin"] == origin) & (cells["band"] == band)
                         & (cells["applicants"] >= 20)].sort_values("mean_peer_exam")
        axis.plot(part["mean_peer_exam"], 100 * part["home_top_rate"],
                  "o-", color="#356c9b", label="Top program at home")
        axis.plot(part["mean_peer_exam"], 100 * part["any_top_rate"],
                  "o-", color="#a43d4c", label="Top program anywhere observed")
        for row in part.itertuples():
            axis.annotate(str(row.applicants), (row.mean_peer_exam,
                          100 * row.any_top_rate), xytext=(0, 6),
                          textcoords="offset points", ha="center", fontsize=7)
        axis.set_title(f"{origin} · {band}")
        axis.set_xlabel("Mean examination score of other gymnasium applicants")
        axis.set_ylabel("Placed in designated top program (%)")
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
    scope = "excellence band by origin county" if only_excellence else "pooled counties by own-score band"
    fig.suptitle(f"Romania 2001: home vs observed destination, top {tier}\n{scope}", fontsize=15)
    fig.text(.5, .01,
             "Same applicants in both lines; labels give applicants. Cells below 20 are in CSV but not plotted. "
             "Descriptive, with unknown preferences and masked personal IDs.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=[0, .03, 1, .95])
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _movement_figure(movement, path):
    """Compare movers with stayers on own scores, without labeling motive."""
    states = (("home_placed", "Placed at home", "#356c9b"),
              ("away_placed", "Placed elsewhere", "#a43d4c"),
              ("unassigned", "Unassigned", "#999999"))
    fig, axes = plt.subplots(1, 2, figsize=(17, 5))
    x = np.arange(len(COUNTIES))
    width = .25
    for offset, (state, label, color) in enumerate(states):
        series = movement.loc[movement["assignment"] == state].set_index("origin")
        median = [series.loc[c, "median_exam"] if c in series.index else np.nan for c in COUNTIES]
        top = [100 * series.loc[c, "top_own_exam_band_pct"]
               if c in series.index else np.nan for c in COUNTIES]
        axes[0].bar(x + (offset - 1) * width, median, width, label=label, color=color)
        axes[1].bar(x + (offset - 1) * width, top, width, label=label, color=color)
    axes[0].set_ylabel("Median own examination score")
    axes[1].set_ylabel("In county top own-score band (%)")
    for axis in axes:
        axis.set_xticks(x, COUNTIES)
        axis.set_xlabel("Origin county")
        axis.grid(axis="y", alpha=.2)
        axis.set_axisbelow(True)
        axis.legend(fontsize=8)
    fig.suptitle("Who leaves the origin county? Observed admissions routes, not motives")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _multistate_figure(cells, settings, path):
    """Pooled four-state mix across within-county peer-strength ranks."""
    band = pilot._band_labels(settings)[2]
    data = cells.loc[cells["band"] == band]
    pivot = data.pivot_table(index="peer_bin", columns="state", values="applicants",
                             aggfunc="sum", fill_value=0)
    order = (("unassigned", "Unassigned", "#777777"),
             ("other_placed_program", "Other program", "#73afd2"),
             ("top_two_only_anywhere", "Top two only", "#e58b25"),
             ("top_one_anywhere", "Top one", "#a43d4c"))
    totals = pivot.sum(axis=1)
    fig, axis = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(pivot))
    for key, label, color in order:
        values = (100 * pivot.get(key, pd.Series(0, index=pivot.index)) / totals).to_numpy()
        axis.bar(pivot.index.astype(int), values, bottom=bottom, color=color, label=label)
        bottom += values
    for position, total in totals.items():
        axis.annotate(f"n={int(total):,}", (position, 100),
                      xytext=(0, 4), textcoords="offset points", ha="center", fontsize=8)
    axis.set_ylim(0, 108)
    axis.set_xlabel("Peer-strength quantile within origin county (low to high)")
    axis.set_ylabel("Share of applicants in excellence own-score band (%)")
    axis.set_title("Four observed placement states across gymnasium peer strength")
    axis.legend(ncol=4, loc="upper center")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def run_comparison(settings, *, run=False, save_private_ledger=True):
    """Researcher-controlled execution; importing this file never runs it."""
    if not run:
        print("Comparison is off. Set RUN_CROSS_COUNTY_COMPARISON = True in the notebook.")
        return None
    if settings.top_tiers != (1, 2):
        raise ValueError("Keep the saved top-one and top-two tiers for this comparison")
    print("1/4 Verifying source pages and building the in-memory outcome ledger...", flush=True)
    ledger, audit = _outcome_rows(settings)
    # Reuse the previous notebook's exact county percentile boundaries.
    band_input = ledger.rename(columns={"origin": "county"}).copy()
    band_input["tier"] = settings.top_tiers[0]
    banded, boundaries = pilot._add_bands(band_input, settings)
    ledger["county_band"] = banded["county_band"].to_numpy()
    ledger["pooled_band"] = banded["pooled_band"].to_numpy()
    print("2/4 Auditing paired denominators and movement composition...", flush=True)
    movement = _movement_summary(ledger, settings)
    paired = []
    multistate = pd.DataFrame()
    denominator = {}
    for tier in settings.top_tiers:
        cells, eligible = _comparison_cells(ledger, settings, tier)
        paired.append(cells)
        denominator[tier] = len(eligible)
        if tier == 1:
            multistate = _multistate_cells(eligible, tier, settings)
    paired = pd.concat(paired, ignore_index=True)
    timestamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    folder = OUT / timestamp
    folder.mkdir(parents=True, exist_ok=False)
    print("3/4 Saving name-free aggregates and paired figures...", flush=True)
    pd.DataFrame([audit]).to_csv(folder / "source_audit.csv", index=False)
    boundaries.to_csv(folder / "score_band_boundaries.csv", index=False)
    movement.to_csv(folder / "movement_score_composition.csv", index=False)
    paired.to_csv(folder / "paired_home_anywhere_cells.csv", index=False)
    multistate.to_csv(folder / "multistate_cells.csv", index=False)
    for tier in settings.top_tiers:
        _paired_figure(paired, settings, tier, folder / f"paired_excellence_top{tier}.png",
                       only_excellence=True)
        _paired_figure(paired, settings, tier, folder / f"paired_pooled_bands_top{tier}.png",
                       only_excellence=False)
    _movement_figure(movement, folder / "movement_exam_by_status.png")
    _multistate_figure(multistate, settings, folder / "multistate_excellence.png")
    if save_private_ledger:
        PRIVATE.mkdir(parents=True, exist_ok=True)
        private_path = PRIVATE / f"{timestamp}_ledger.csv"
        private_data = ledger.copy()
        private_data.insert(0, "record_id", np.arange(1, len(private_data) + 1))
        private_data.to_csv(private_path, index=False)
    else:
        private_path = None
    report = ["# Seven-county local-versus-anywhere comparison", "",
              "The same observed gymnasium applicants enter both lines of each paired plot. "
              "Home means a top program in the originating county; anywhere means a top program "
              "in the actual destination county. Both program rankings use the saved notebook's "
              "top-one/top-two, full-program, subject-category settings. A placement outside the "
              "home county is a known zero for the home outcome but enters the anywhere outcome "
              "only after its destination program's rank is source-resolved.", "",
              f"Applicants in the source ledger: **{len(ledger):,}**. "
              f"Paired denominator after requiring a gymnasium peer and both rankings: "
              f"**{denominator[1]:,}** (top one), **{denominator[2]:,}** (top two). "
              "These are participating admissions-round applicants, not every eighth grader.", "",
              "## Source limits", "",
              f"Out-of-county placements with an unresolved destination-program rank: "
              f"**{int(((ledger.assignment == 'away_placed') & ledger.any_top1.isna()).sum())}**. "
              f"The unreconciled destination catalog county code(s): "
              f"**{audit['destination_catalog_county_codes_unverified'] or 'none'}**. "
              f"There are also **{audit.get('unassigned_national_key_ambiguity', 0)}** "
              "school-page unassigned applicants with a same-name-and-score placement "
              "elsewhere in the saved national reports; masked IDs prevent treating "
              "that as the same person. "
              "These rows remain unresolved and are excluded from both lines of the paired plot, "
              "rather than being called failures. Exact source-status counts are in `source_audit.csv`.", "",
              "The archived personal identifier is masked. Matches based on origin school plus "
              "printed name and admission score are provisional. The archive does not show "
              "student preference lists: unassigned does not mean rejected by a particular "
              "program, and an origin–destination county link does not explain why the student "
              "applied there. Examination score was measured after time in the gymnasium. "
              "These figures are descriptive, not causal evidence of congestion.", "",
              "`movement_score_composition.csv` compares own examination performance across "
              "home placed, elsewhere placed, and unassigned applicants. "
              "`multistate_cells.csv` splits the common denominator into unassigned, top-one, "
              "top-two-only, and other placed programs. All exports in this folder are name-free "
              "aggregates; the optional row-level ledger stays on the Desktop.", ""]
    (folder / "report.md").write_text("\n".join(report), encoding="utf-8")
    (folder / "run_manifest.json").write_text(json.dumps({
        "settings": asdict(settings), "source_audit": audit,
        "private_ledger_saved": bool(private_path),
        "private_ledger_path": str(private_path) if private_path else None,
        "scope": "Seven audited origin counties, Romania 2001 main admissions round",
    }, indent=2) + "\n", encoding="utf-8")
    print("4/4 Complete. Read:", folder / "report.md", flush=True)
    if private_path:
        print("Private row-level ledger:", private_path, flush=True)
    return folder, pd.DataFrame([audit]), movement
