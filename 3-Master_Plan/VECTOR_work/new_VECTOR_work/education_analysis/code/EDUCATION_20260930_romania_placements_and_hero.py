"""Researcher-run Alba 2001 placement acquisition and descriptive HERO.

Importing this module neither fetches pages nor calculates a research result.
Names and original HTML stay in Charles's Desktop cache. Permanent outputs use
generated row identifiers, school codes, scores, and destination program codes.
See the September 30 program-ranking decision record for the scientific rules.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import EDUCATION_20260930_romania_cache_workflow as source
from romania_archive_retrieval import RetrievalStopped

BASE = Path(__file__).resolve().parents[1]
CACHE = source.CACHE / "placements_v1"
PROGRAMS = BASE / "outputs/romania_alba_2001_program_cutoffs_20260930/program_cutoffs.json"
OUTPUTS = BASE / "outputs/romania_alba_2001_hero_v1"
DECISION = BASE / "docs/decisions/EDUCATION_20260930_Romania_program_ranking_and_HERO_decisions.md"
FROZEN_SCORES = source.OUT / f"{source.STEM}_name_free_applicant_scores.csv.gz"
CATEGORIES = (
    "Matematica-Informatica", "Stiinte ale Naturii", "Stiinte Sociale",
    "Filologie", "Spec.Tehnologica", "Profesional",
)
SCHEMA = 1
BINS = 16
COMBINED_CATEGORIES = {
    "Matematica-Informatica": "Mathematics / sciences",
    "Stiinte ale Naturii": "Mathematics / sciences",
    "Stiinte Sociale": "Social sciences / philology",
    "Filologie": "Social sciences / philology",
    "Spec.Tehnologica": "Technology / vocational",
    "Profesional": "Technology / vocational",
}


def digest(value):
    return hashlib.sha256(source.canonical_bytes(value)).hexdigest()


def write_json(path, value):
    source.atomic_json(Path(path), value)


def placement_relative(school):
    original = school["candidate_report"]
    if "raport_candidati_per_scoala" not in original:
        raise ValueError("Unexpected candidate report path; no guessed placement address")
    return original.replace("raport_candidati_per_scoala", "raport_total_per_scoala", 1)


def checkpoint_path(code):
    if not str(code).isdigit():
        raise ValueError("Origin school code must be numeric")
    return CACHE / "school_reports" / f"school_{int(code):03d}.json"


def placement_coverage(candidate_rows, placement_rows):
    """Count exact coverage without returning names or enlarging the cohort.

    A placement report can be a genuine superset of the frozen candidate
    report. All frozen candidates must still have one unique name match and
    the same admission composite before that longer report is accepted.
    """
    candidate_names = Counter(r.get("Nume", "") for r in candidate_rows)
    by_name = defaultdict(list)
    for row in placement_rows:
        by_name[row.get("Nume", "")].append(row)
    matched = missing = ambiguous = disagreements = 0
    for row in candidate_rows:
        name = row.get("Nume", "")
        matches = by_name.get(name, [])
        if not name or candidate_names[name] != 1 or len(matches) > 1:
            ambiguous += 1
        elif not matches:
            missing += 1
        else:
            a, b = number(row.get("Medie Admitere")), number(matches[0].get("Medie Admitere"))
            if not (np.isfinite(a) and np.isfinite(b) and abs(a-b) < 1e-9):
                disagreements += 1
            else:
                matched += 1
    return {
        "frozen_candidate_rows": len(candidate_rows),
        "placement_report_rows": len(placement_rows),
        "unique_name_and_composite_matches": matched,
        "missing_candidates": missing, "ambiguous_candidates": ambiguous,
        "composite_disagreements": disagreements,
        "extra_report_rows_outside_frozen_population": sum(
            r.get("Nume", "") not in candidate_names for r in placement_rows),
        "candidate_rows_sha256": digest(candidate_rows),
    }


def validate_placement_count(school, expected_rows, rows):
    """Retain old equal-count checkpoints; verify strict coverage for extras."""
    if len(rows) < expected_rows:
        raise ValueError(f"Returned {len(rows)} rows; expected at least {expected_rows}. Not accepted.")
    if len(rows) == expected_rows:
        return None  # Person matching remains a separate analysis check.
    cached = source.verified_cache_record(school, {"candidate_rows": expected_rows})
    if cached is None:
        raise ValueError("Cannot verify a longer placement report without the frozen candidate cache.")
    audit = placement_coverage(cached["rows"], rows)
    if audit["unique_name_and_composite_matches"] != expected_rows:
        raise ValueError(
            f"Longer placement report is not a verified superset: {audit['missing_candidates']} missing, "
            f"{audit['ambiguous_candidates']} ambiguous, "
            f"{audit['composite_disagreements']} composite disagreements. Not accepted.")
    return audit


def verify_checkpoint(school, expected_rows):
    """A saved file is reusable only when identity, counts and hashes agree."""
    path = checkpoint_path(school["code"])
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    if (payload["schema"] != SCHEMA or payload["source_code"] != school["code"]
            or payload["relative_url"] != placement_relative(school)):
        raise ValueError(f"Placement checkpoint identity changed: school {school['code']}")
    rows = payload["rows"]
    if payload["rows_sha256"] != digest(rows):
        raise ValueError(f"Placement checkpoint count/hash changed: school {school['code']}")
    coverage = validate_placement_count(school, expected_rows, rows)
    if coverage is not None and payload.get("candidate_coverage_audit") != coverage:
        raise ValueError(f"Longer placement report lacks its verified coverage audit: school {school['code']}")
    if payload["kind"] == "source_verified_empty_origin":
        if expected_rows != 0:
            raise ValueError("An empty-origin checkpoint cannot substitute for a roster")
    elif payload["kind"] == "retrieved_placement_report":
        raw = base64.b64decode(payload["raw_html_base64"], validate=True)
        if hashlib.sha256(raw).hexdigest() != payload["raw_html_sha256"]:
            raise ValueError("Placement raw HTML checksum changed")
        if set(("Nume", "Liceu", "Profil", "Specializare", "Medie Admitere")) - set(payload["headers"]):
            raise ValueError("Placement headers changed")
    else:
        raise ValueError("Unknown checkpoint kind")
    return payload


def placement_status():
    """Read-only: no network request and no output files."""
    directory, checks = source.read_completed_checkpoint()
    complete, pending = [], []
    for school in directory:
        ok = verify_checkpoint(school, int(checks[school["code"]]["candidate_rows"]))
        (complete if ok is not None else pending).append(school["code"])
    return {"total_codes": len(directory), "complete_codes": len(complete),
            "remaining_codes": pending, "cache": str(CACHE)}


def _save_queue(directory, checks, errors):
    pending = []
    for school in directory:
        if verify_checkpoint(school, int(checks[school["code"]]["candidate_rows"])) is None:
            pending.append({"source_code": school["code"],
                            "relative_url": placement_relative(school),
                            "last_error": errors.get(school["code"], "not yet attempted")})
    write_json(CACHE / "unresolved_addresses.json", pending)
    return pending


def _event(event):
    """Technical details on disk; brief, legible progress in the notebook."""
    with (CACHE / "retrieval_events.jsonl").open("a") as stream:
        stream.write(json.dumps({"utc": source.now_utc(), **event}, ensure_ascii=False) + "\n")
        stream.flush()
    if event.get("kind") == "adaptive_pace":
        print(f"  Request spacing now {event['new_seconds']:.2f} seconds.", flush=True)
    elif event.get("kind") == "retrieval_wait" and event.get("seconds", 0) >= 10:
        print(f"  Waiting {event['seconds']:.0f} seconds: {event.get('reason', 'archive pacing')}.", flush=True)


def acquire_placements(*, live=False, initial_interval_seconds=2.0,
                       minimum_interval_seconds=1.2, maximum_interval_seconds=60.0,
                       max_runtime_hours=6.0, retry_passes=3,
                       retry_cooldown_seconds=180.0):
    """Checkpoint each school; retry only unresolved reports, sequentially.

    Existing candidate files are inputs and are never overwritten. The seven
    source-verified empty origin groups need no placement request. A failed
    or truncated placement page is queued, never accepted as an empty roster.
    """
    if not live:
        print("Preview only. No placement downloads.", flush=True)
        return placement_status()
    if retry_passes < 1 or retry_cooldown_seconds < 0:
        raise ValueError("Require at least one pass and a nonnegative cooldown")
    # First verify the existing complete acquisition, before any new requests.
    source._read_all_cached_reports()
    directory, checks = source.read_completed_checkpoint()
    CACHE.mkdir(parents=True, exist_ok=True, mode=0o700)
    errors = {}
    queue_path = CACHE / "unresolved_addresses.json"
    if queue_path.exists():
        errors = {r["source_code"]: r.get("last_error", "") for r in json.loads(queue_path.read_text())}
    for school in directory:
        code = school["code"]
        expected = int(checks[code]["candidate_rows"])
        if expected == 0 and verify_checkpoint(school, expected) is None:
            write_json(checkpoint_path(code), {
                "schema": SCHEMA, "source_code": code,
                "relative_url": placement_relative(school),
                "kind": "source_verified_empty_origin", "rows": [],
                "rows_sha256": digest([]), "saved_utc": source.now_utc(),
                "reason": "Verified candidate cache contains zero applicants; no placement page requested.",
            })
    pending = _save_queue(directory, checks, errors)
    if not pending:
        print("All placement checkpoints are already present. No network requests.", flush=True)
        return placement_status()
    structural = source.load_structural_module()
    structural.OUT = CACHE
    structural.emit = _event
    structural.configure_retrieval(
        True, initial_interval_seconds=initial_interval_seconds,
        minimum_interval_seconds=minimum_interval_seconds,
        maximum_interval_seconds=maximum_interval_seconds,
        max_runtime_hours=max_runtime_hours,
    )
    from tqdm.auto import tqdm

    started = time.monotonic()
    print(f"Placement acquisition running: {len(pending)} school reports needed.", flush=True)
    try:
        for pass_number in range(1, retry_passes + 1):
            codes = {r["source_code"] for r in pending}
            if not codes:
                break
            if pass_number > 1:
                structural.CLIENT.wait_between_passes(retry_cooldown_seconds, pass_number)
            schools = [s for s in directory if s["code"] in codes]
            with tqdm(schools, desc=f"Placement pass {pass_number}/{retry_passes}", unit="school") as bar:
                for school in bar:
                    code = school["code"]
                    expected = int(checks[code]["candidate_rows"])
                    page = structural.fetch(placement_relative(school), f"placement_origin_{code}", include_raw=True)
                    if page is None:
                        errors[code] = "Request or table parsing unresolved; see local event log."
                    elif set(("Nume", "Liceu", "Profil", "Specializare", "Medie Admitere")) - set(page[0]):
                        errors[code] = "Required placement columns missing. Not accepted."
                    else:
                        headers, rows, cells, meta, raw = page
                        try:
                            coverage = validate_placement_count(school, expected, rows)
                        except ValueError as exc:
                            errors[code] = str(exc)
                        else:
                            write_json(checkpoint_path(code), {
                                "schema": SCHEMA, "source_code": code,
                                "relative_url": placement_relative(school),
                                "kind": "retrieved_placement_report",
                                "headers": headers, "rows": rows, "rows_sha256": digest(rows),
                                "source_page": meta, "raw_html_base64": base64.b64encode(raw).decode(),
                                "raw_html_sha256": hashlib.sha256(raw).hexdigest(),
                                "candidate_coverage_audit": coverage,
                                "saved_utc": source.now_utc(),
                            })
                            if coverage is not None:
                                print(f"  Verified all {expected} frozen applicants; preserving "
                                      f"{coverage['extra_report_rows_outside_frozen_population']} extra "
                                      "placement row(s) as source evidence only. Population unchanged.", flush=True)
                            errors.pop(code, None)
                    # Flush the queue after every school, including every failure.
                    pending = _save_queue(directory, checks, errors)
                    bar.set_postfix(saved=len(directory)-len(pending), remaining=len(pending),
                                    wait=f"{structural.CLIENT.interval:.1f}s")
                    print(f"  School {code}: {'saved and checked' if code not in errors else errors[code]} "
                          f"| {len(directory)-len(pending)}/{len(directory)} complete "
                          f"| elapsed {(time.monotonic()-started)/60:.1f} min", flush=True)
    except (KeyboardInterrupt, RetrievalStopped) as exc:
        print(f"Stopped safely ({type(exc).__name__}). Saved schools will be skipped on restart.", flush=True)
    finally:
        pending = _save_queue(directory, checks, errors)
    print(f"Acquisition finished: {len(directory)-len(pending)}/{len(directory)} complete; "
          f"{len(pending)} unresolved. Queue: {queue_path}", flush=True)
    return placement_status()


def load_programs():
    programs = json.loads(PROGRAMS.read_text())
    if len({p["program_code"] for p in programs}) != len(programs):
        raise ValueError("Duplicate program identifiers")
    if set(p["specialization"] for p in programs) != set(CATEGORIES):
        raise ValueError("Program categories differ from the agreed six")
    for p in programs:
        if p["admitted"] + p["vacancies"] != p["places"]:
            raise ValueError("Program capacity balance failed")
        if p["filled"] != (p["places"] > 0 and p["vacancies"] == 0):
            raise ValueError("Program filled flag disagrees with counts")
    return programs


def winning_programs(programs, top_program_tiers=1, *, require_full_programs=True,
                     combine_program_categories=False):
    """Rank within six original subjects or three combined groups, with ties.

    Turning off the fullness requirement permits nonempty, partially occupied
    programs. Their observed minimum is not necessarily a binding capacity
    cutoff. Empty programs and missing minima never acquire an invented rank.
    """
    if type(top_program_tiers) is not int or top_program_tiers < 1:
        raise ValueError("top_program_tiers must be a positive integer")
    if type(require_full_programs) is not bool or type(combine_program_categories) is not bool:
        raise ValueError("Program eligibility and category switches must be True or False")
    def group(p):
        return COMBINED_CATEGORIES[p["specialization"]] if combine_program_categories else p["specialization"]
    groups = tuple(dict.fromkeys(COMBINED_CATEGORIES.values())) if combine_program_categories else CATEGORIES
    winners = []
    for category in groups:
        qualifying = [p for p in programs if group(p) == category
                      and p["places"] > 0 and p["admitted"] > 0
                      and p["lowest_admitted_score"] is not None
                      and np.isfinite(p["lowest_admitted_score"])
                      and (not require_full_programs or
                           (p["admitted"] == p["places"] and p["vacancies"] == 0))]
        if qualifying:
            cutoffs = sorted({p["lowest_admitted_score"] for p in qualifying}, reverse=True)
            selected = set(cutoffs[:top_program_tiers])
            winners.extend({**p, "ranking_group": category,
                            "cutoff_tier": cutoffs.index(p["lowest_admitted_score"])+1}
                           for p in qualifying if p["lowest_admitted_score"] in selected)
    return winners


def text(value):
    """Whitespace normalization only: no approximate names or inferred codes."""
    return " ".join(str(value).split())


def number(value):
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return np.nan


def classify_destination(row, programs, winners):
    """Only confirmed placement identifies success; a high score does not."""
    destination = text(row.get("Liceu", ""))
    if destination == "----- NEREPARTIZAT -----":
        return {"placement_status": "confirmed_unassigned", "program_code": "",
                "vocational": False, "success": 0.0}
    # Foreign county codes are explicit in the placement report, not inferred
    # from the candidate's county, which would misclassify an unassigned case.
    suffix = re.fullmatch(r"(.*?)\s*/\s*([A-Z]{1,2})", destination)
    if suffix and suffix.group(2) != "AB":
        return {"placement_status": "confirmed_outside_Alba", "program_code": "",
                "vocational": False, "success": np.nan}
    school = text(suffix.group(1)) if suffix else destination
    candidates = [p for p in programs
                  if text(p["school_name"]) == school
                  and text(p["profile"]) == text(row.get("Profil", ""))
                  and text(p["specialization"]) == text(row.get("Specializare", ""))]
    if len(candidates) != 1:
        return {"placement_status": "ambiguous_program" if candidates else "unmatched_program",
                "program_code": "", "vocational": False, "success": np.nan}
    p = candidates[0]
    # Similar labels with different language or attendance forms cannot be
    # resolved by guessing. Such duplicate triples stay ambiguous above.
    return {"placement_status": "confirmed_Alba_program", "program_code": p["program_code"],
            "vocational": p["level"] == "Profesional" or p["specialization"] == "Profesional",
            "success": float(p["program_code"] in winners)}


def attach_placements(frame, candidates, placements, programs, top_program_tiers=1, *,
                      require_full_programs=True, combine_program_categories=False):
    """Exact unique printed name WITHIN source code, checked against composite.

    Masked CNP is not a usable identifier. No name, CNP, or name hash is added
    to the returned DataFrame. The generated analytic_row preserves the frozen
    candidate order, allowing us to audit exclusions without publishing names.
    """
    winners = {p["program_code"] for p in winning_programs(programs, top_program_tiers,
               require_full_programs=require_full_programs, combine_program_categories=combine_program_categories)}
    result = []
    for code in sorted(candidates, key=int):
        candidate_rows = candidates[code]
        candidate_names = Counter(r.get("Nume", "") for r in candidate_rows)
        placement_names = defaultdict(list)
        for row in placements[code]:
            placement_names[row.get("Nume", "")].append(row)
        for ordinal, candidate in enumerate(candidate_rows, 1):
            name = candidate.get("Nume", "")
            matches = placement_names.get(name, [])
            label = {"placement_status": "unmatched_person", "program_code": "",
                     "vocational": False, "success": np.nan}
            if not name or candidate_names[name] > 1 or len(matches) > 1:
                label["placement_status"] = "ambiguous_person"
            elif len(matches) == 1:
                a = number(candidate.get("Medie Admitere"))
                b = number(matches[0].get("Medie Admitere"))
                if not (np.isfinite(a) and np.isfinite(b) and abs(a-b) < 1e-9):
                    label["placement_status"] = "composite_disagreement"
                else:
                    label = classify_destination(matches[0], programs, winners)
            result.append({"source_code": code, "analytic_row": ordinal, **label})
    labels = pd.DataFrame(result)
    merged = frame.merge(labels, on=["source_code", "analytic_row"],
                         how="left", validate="one_to_one", sort=False)
    if len(merged) != len(frame) or merged["placement_status"].isna().any():
        raise ValueError("Placement join lost candidate records")
    return merged


def add_peer_axis(frame):
    """Compute once using ALL recovered applicants, before outcome exclusions."""
    frame = frame.copy()
    group = frame.groupby("source_code")["A_z"]
    frame["peer_count"] = group.transform("size") - 1
    frame["peer_mean_A_z"] = (group.transform("sum") - frame["A_z"]) / frame["peer_count"].replace(0, np.nan)
    return frame


def outcome_population(frame, include_vocational=True):
    """One mutually exclusive exclusion reason per applicant; peers unchanged."""
    frame = frame.copy()
    frame["outcome_exclusion"] = "included"
    # Apply in reverse order of reporting precedence. Singletons may overlap
    # with unresolved/outside placements; the final reason counts only once.
    if not include_vocational:
        frame.loc[frame["vocational"], "outcome_exclusion"] = "vocational_denominator_exclusion"
    frame.loc[frame["success"].isna(), "outcome_exclusion"] = "unknown_placement_or_program"
    frame.loc[frame["placement_status"] == "confirmed_outside_Alba",
              "outcome_exclusion"] = "outside_Alba_destination"
    frame.loc[frame["peer_mean_A_z"].isna(), "outcome_exclusion"] = "no_observed_peer"
    frame["included_in_outcome"] = frame["outcome_exclusion"].eq("included")
    return frame


def frozen_edges(values, kind, n_bins=BINS):
    values = np.asarray(values, dtype=float)
    if not len(values) or not np.isfinite(values).all() or values.min() == values.max():
        raise ValueError("Outcome population needs a varying, finite peer axis")
    if kind == "equal_width":
        return np.linspace(values.min(), values.max(), n_bins + 1)
    if kind == "quantile":
        # Drop duplicate boundaries. Never divide identical peer values by
        # arbitrary row order just to enforce sixteen equal-sized groups.
        return np.unique(np.quantile(values, np.linspace(0, 1, n_bins + 1)))
    raise ValueError("Unknown binning")


def bin_table(frame, edges):
    kept = frame.loc[frame["included_in_outcome"]].copy()
    assignments = pd.cut(kept["peer_mean_A_z"], bins=edges, labels=False,
                         include_lowest=True, right=True)
    if assignments.isna().any():
        raise ValueError("An included applicant lies outside the frozen bin boundaries")
    kept["bin"] = assignments.astype(int)
    rows = []
    for b, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        data = kept.loc[kept["bin"] == b]
        n, successes = len(data), int(data["success"].sum())
        rows.append({"bin": b+1, "lower": float(lo), "upper": float(hi),
                     "N": n, "successes": successes,
                     "success_rate": successes/n if n else np.nan,
                     "mean_peer_A_z": float(data["peer_mean_A_z"].mean()) if n else np.nan})
    table = pd.DataFrame(rows)
    if int(table["N"].sum()) != len(kept):
        raise ValueError("Binned denominator does not reconcile")
    return table


def draw_hero(tables, rate, title, output):
    """Descriptive counts and rates only; no fitted curve or causal interval."""
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.2), sharey=True)
    highest = max(float(t['success_rate'].max()) for t in tables.values()) * 100
    upper = min(118, max(15, highest * 1.25 + 5))
    for ax, (kind, table) in zip(axes, tables.items()):
        x = table["bin"].to_numpy()
        y = table["success_rate"].to_numpy()*100
        ax.bar(x, y, color="#9f3e4e", width=.85)
        ax.axhline(rate*100, color="black", ls=":", label=f"Overall observed success: {rate:.2%}")
        for row in table.itertuples():
            if row.N:
                ax.annotate(f"{row.successes}/{row.N}", (row.bin, row.success_rate*100),
                            xytext=(0, 5), textcoords="offset points", ha="center",
                            fontsize=8, rotation=60)
            else:
                ax.text(row.bin, 1, "no estimate", rotation=90, ha="center", fontsize=8)
        ax.set_title(f"{'Equal-width' if kind == 'equal_width' else 'Quantile'} bins ({len(table)})")
        ax.set_xticks(x)
        ax.set_xlabel("Peer-performance bin, ordered from low to high\n"
                      "(mean standardized examination score of other gymnasium applicants)")
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, upper)
    axes[0].set_ylabel("Placed in a designated top program (%)")
    fig.suptitle(title, fontsize=14)
    fig.text(.5, .015, "Labels = successful placements / applicants. Actual main-round placements; "
             "outside-Alba destinations excluded.\n"
             "Peers retain the complete recovered applicant population. This descriptive view does not identify congestion.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0,.085,1,.94))
    paths = [output/"HERO.png", output/"HERO.pdf"]
    for path in paths:
        fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return paths


def prepare_analysis(top_program_tiers=1, *, require_full_programs=True, combine_program_categories=False):
    """Offline reconciliation. Returns name-free data; writes nothing."""
    reports, candidate_manifest = source._read_all_cached_reports()
    directory, checks = source.read_completed_checkpoint()
    placements, hashes, coverage_audits = {}, {}, {}
    for school in directory:
        payload = verify_checkpoint(school, int(checks[school["code"]]["candidate_rows"]))
        if payload is None:
            raise RuntimeError(f"Placement acquisition incomplete (school {school['code']}). Resume first.")
        placements[school["code"]] = payload["rows"]
        if payload.get("candidate_coverage_audit") is not None:
            coverage_audits[school["code"]] = payload["candidate_coverage_audit"]
        hashes[school["code"]] = source.sha256(checkpoint_path(school["code"]))
    structural = source.load_structural_module()
    if source.count_cross_code_exact_duplicates(structural, reports):
        raise ValueError("Repeated exact name-and-score signature across origin codes; inspect before HERO")
    frame, construction = source.build_name_free_frame(structural, reports)
    frame.insert(1, "analytic_row", frame.groupby("source_code", sort=False).cumcount()+1)
    frozen = pd.read_csv(FROZEN_SCORES, dtype={"source_code": str})
    if not frame[["source_code","analytic_row"]].equals(frozen[["source_code","analytic_row"]]):
        raise ValueError("Candidate order/population differs from the completed differentiation analysis")
    for column in ("exam_score","grades_5_8_average","admission_composite","A_z"):
        if not np.allclose(frame[column], frozen[column], rtol=0, atol=1e-10):
            raise ValueError(f"Frozen score comparison failed: {column}")
    programs = load_programs()
    frame = add_peer_axis(attach_placements(frame, reports, placements, programs, top_program_tiers,
        require_full_programs=require_full_programs, combine_program_categories=combine_program_categories))
    baseline = outcome_population(frame)
    audit = {
        "top_program_tiers": top_program_tiers,
        "require_full_programs": require_full_programs,
        "combine_program_categories": combine_program_categories,
        "source_population": int(len(frame)), "origin_codes": len(directory),
        "nonempty_origin_codes": int(frame["source_code"].nunique()),
        "placement_status_counts": {str(k): int(v) for k,v in frame["placement_status"].value_counts().items()},
        "baseline_reconciled_flow": {str(k): int(v) for k,v in baseline["outcome_exclusion"].value_counts().items()},
        "construction_checks": construction,
        "longer_placement_report_coverage": coverage_audits,
    }
    print("Offline reconciliation complete. Counts below overlap only in placement_status versus flow;\n"
          "the baseline_reconciled_flow itself counts each applicant once.", flush=True)
    print(json.dumps(audit, indent=2), flush=True)
    return frame, programs, audit, {
        "candidate_manifest_sha256": source.sha256(source.CACHE/"completed_manifest.json"),
        "placement_file_sha256": hashes, "program_table_sha256": source.sha256(PROGRAMS),
        "frozen_scores_sha256": source.sha256(FROZEN_SCORES),
    }


def reference_bin_edges(reference_run, baseline, proposed_edges):
    """Reuse a saved run's bins only after verifying the unchanged population.

    Success is deliberately excluded from the equality check: this is the
    one variable the tier comparison is supposed to change.
    """
    reference_run = Path(reference_run)
    record = json.loads((reference_run/"run_record.json").read_text())
    names = ("fixed_bin_edges.json", "baseline_include_vocational/name_free_applicant_outcome_audit.csv.gz")
    for name in names:
        if source.sha256(reference_run/name) != record["output_hashes"][name]:
            raise ValueError(f"Reference result checksum changed: {name}")
    previous = pd.read_csv(reference_run/names[1], dtype={"source_code":str,"program_code":str})
    columns = ["source_code", "analytic_row", "exam_score", "grades_5_8_average",
               "admission_composite", "A_z", "peer_count", "peer_mean_A_z",
               "placement_status", "program_code", "vocational", "outcome_exclusion", "included_in_outcome"]
    keys = ["source_code", "analytic_row"]
    old = previous[columns].sort_values(keys).reset_index(drop=True).replace({"":np.nan})
    new = baseline[columns].sort_values(keys).reset_index(drop=True).replace({"":np.nan})
    pd.testing.assert_frame_equal(old, new, check_dtype=False, check_exact=False, rtol=0, atol=1e-10)
    edges = {k:np.asarray(v,dtype=float) for k,v in json.loads((reference_run/names[0]).read_text()).items()}
    for kind, values in proposed_edges.items():
        np.testing.assert_allclose(edges[kind], values, rtol=0, atol=1e-12)
    return edges


def run_hero(*, run=False, include_vocational=True, top_program_tiers=1, reference_run=None,
             require_full_programs=True, combine_program_categories=False):
    """Offline only. Always preserve baseline; optional second denominator view."""
    settings = {"top_program_tiers": top_program_tiers, "require_full_programs": require_full_programs,
                "combine_program_categories": combine_program_categories}
    if not run:
        print("Preview only. No HERO calculation or network requests.", flush=True)
        return {"status": "not_run", "output_folder": str(OUTPUTS), **settings}
    print("HERO code running: 1/3 — checking caches and exact placement correspondence.", flush=True)
    frame, programs, audit, provenance = prepare_analysis(**settings)
    winners = winning_programs(programs, **settings)
    capacity_label = "fully occupied programs" if require_full_programs else "nonempty programs, including partially filled"
    category_label = "3 combined groups" if combine_program_categories else "6 original subjects"
    configuration_label = f"top {top_program_tiers} cutoff tier(s); {capacity_label}; {category_label}"
    baseline = outcome_population(frame, True)
    baseline_kept = baseline.loc[baseline["included_in_outcome"]]
    if baseline_kept.empty:
        raise ValueError("No confirmed outcome population. No HERO can be produced.")
    edges = {kind: frozen_edges(baseline_kept["peer_mean_A_z"], kind)
             for kind in ("equal_width", "quantile")}
    if reference_run is not None:
        edges = reference_bin_edges(reference_run, baseline, edges)
        print("  Reference population, placements, peer averages and bin boundaries verified unchanged.", flush=True)
    # Every execution gets its own folder. A comparison or later rerun cannot
    # overwrite the original baseline or silently change its bin boundaries.
    run_dir = OUTPUTS / (datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%S_%fZ")
                        + f"_top{top_program_tiers}_tiers_"
                        + ("full" if require_full_programs else "nonempty")
                        + ("_3groups" if combine_program_categories else "_6groups"))
    run_dir.mkdir(parents=True, exist_ok=False)
    write_json(run_dir/"RUNNING.json", {"started_utc":source.now_utc(), "phase":"writing name-free results"})
    write_json(run_dir/"matching_audit.json", audit)
    write_json(run_dir/"selected_programs.json", winners)
    write_json(run_dir/"fixed_bin_edges.json", {k:v.tolist() for k,v in edges.items()})
    variants = {"baseline_include_vocational": baseline}
    if not include_vocational:
        variants["comparison_exclude_vocational"] = outcome_population(frame, False)
    print("HERO code running: 2/3 — writing counts and drawing both binning views.", flush=True)
    results = {}
    for name, population in variants.items():
        folder = run_dir/name
        folder.mkdir()
        population.to_csv(folder/"name_free_applicant_outcome_audit.csv.gz", index=False, compression="gzip")
        kept = population.loc[population["included_in_outcome"]]
        if kept.empty:
            raise ValueError("No applicants remain in the requested comparison")
        tables = {kind: bin_table(population, limits) for kind, limits in edges.items()}
        n, k = len(kept), int(kept["success"].sum())
        removed_successes = removed_applicants = 0
        if name != "baseline_include_vocational":
            removed = baseline.loc[baseline["included_in_outcome"] & baseline["vocational"]].copy()
            removed_successes, removed_applicants = int(removed["success"].sum()), len(removed)
            if k != results["baseline_include_vocational"]["successes"] - removed_successes:
                raise ValueError("Vocational exclusion changed more than the removed applicants' outcomes")
            for kind, table in tables.items():
                reference = bin_table(baseline, edges[kind])
                removed_table = bin_table(removed, edges[kind])
                if not table["successes"].equals(reference["successes"] - removed_table["successes"]):
                    raise ValueError("Successful placements moved across fixed bins")
        for kind, table in tables.items():
            table.to_csv(folder/f"HERO_{kind}_bins.csv", index=False)
        figures = draw_hero(tables, k/n,
                            f"Alba 2001 • top {top_program_tiers} cutoff tier(s) within {category_label}\n{capacity_label}\n"
                            + ("Vocational placements included" if name.startswith("baseline") else
                               "Vocational placements excluded from denominator only"), folder)
        results[name] = {"N": n, "successes": k, "observed_success_fraction": k/n,
                         "vocational_applicants_removed": removed_applicants,
                         "vocational_successes_removed": removed_successes,
                         "reconciled_flow": {str(k):int(v) for k,v in population["outcome_exclusion"].value_counts().items()},
                         "actual_bin_counts": {k:len(t) for k,t in tables.items()},
                         "figures": [str(p) for p in figures]}
        print(f"  {name}: {k:,} successes / {n:,} applicants = {k/n:.2%}", flush=True)
    print("HERO code running: 3/3 — saving the explanatory report and reproducibility record.", flush=True)
    summary = {"status": "completed", "completed_utc": source.now_utc(),
               **settings,
               "reference_run": str(reference_run) if reference_run is not None else None,
               "scope": "Alba 2001 main-allocation descriptive HERO", "audit": audit,
               "variants": results, "selection_is_observed_placement": True,
               "requested_bins": BINS, "unknown_outcomes_are_not_failures": True}
    write_json(run_dir/"summary.json", summary)
    report = [
        f"# Alba 2001: descriptive placement HERO — {configuration_label}", "",
        "## What we did and why", "",
        "We already knew each recovered applicant's national-examination score and originating gymnasium. "
        "We next attached the companion report of actual placement, using an exact unique name within the "
        "source-coded gymnasium and checking the admission composite. This tells us where the applicant "
        "was placed; a score above a cutoff alone never counts as success.", "",
        f"We defined success as actual placement into the top {top_program_tiers} distinct cutoff tier(s) "
        f"among {capacity_label}, ranked within {category_label}, including every tie. "
        "With two tiers this retains the original highest tier and adds the next distinct cutoff. "
        "Empty programs and programs lacking a reported minimum are never ranked. "
        "Cutoffs are reported admission-composite minima in this allocation, not examination-only scores "
        "or measures of teaching quality.", "",
        ("The combined groups are mathematics/sciences, social sciences/philology, and technology/vocational. "
         "Programs are reranked inside each combined group; this can reduce the successful destination set."
         if combine_program_categories else "The six source specializations remain separately ranked."), "",
        ("The full-capacity requirement is active. No recovered vocational program qualifies as full."
         if require_full_programs else "The full-capacity requirement is OFF. A partially filled program's "
         "minimum admitted score may reflect its small intake rather than binding competition for places. "
         "Selection into the designated set in this run must not be described as proven capacity scarcity."), "",
        (f"Comparison reference: {reference_run}. The saved applicant population, placements, peer "
         "averages and outcome eligibility were verified unchanged, and the exact reference bin boundaries "
         "were reused. The earlier result remains intact."
         if reference_run is not None else "No earlier run was supplied as a comparison reference."), "",
        "We held the complete recovered applicant population fixed for score standardization and mean "
        "performance of other gymnasium applicants. Only the outcome denominator changes when we exclude "
        "outside-Alba destinations, unknown outcomes, applicants with no observed peer, or (optionally) "
        "vocational placements. The baseline retains confirmed unassigned applicants as unsuccessful.", "",
        "## Source accounting", "",
        f"- Recovered applicant records: **{len(frame):,}**.",
        "- Placement-status counts: " + json.dumps(audit["placement_status_counts"]) + ".",
        "- Baseline mutually exclusive flow: " + json.dumps(audit["baseline_reconciled_flow"]) + ".", "",
        "- Verified longer placement reports (extra rows retained only in source cache): "
        + json.dumps(audit.get("longer_placement_report_coverage", {})) + ".", "",
        "## Descriptive results", "",
    ]
    for name, info in results.items():
        report.extend([f"### {name.replace('_',' ')}", "",
                       f"- **{info['successes']:,} successful placements among {info['N']:,} applicants "
                       f"({info['observed_success_fraction']:.2%}).**",
                       f"- Actual bin counts: {info['actual_bin_counts']}.",
                       f"- Vocational exclusion removed {info['vocational_applicants_removed']} applicants, "
                       f"including {info['vocational_successes_removed']} designated successes.",
                       f"![Equal-width and quantile HERO]({name}/HERO.png)", ""])
    report.extend([
        "## What these plots do and do not establish", "",
        "The bars describe how realized placement rates vary with observed gymnasium peer examination "
        "performance. Labels show successes divided by applicants in each bin; an empty bin has no estimate. "
        "Quantile boundaries that coincide are collapsed, so tied peer values are never separated by row order. "
        "Both kinds of bin boundaries come from the baseline and remain fixed for any denominator comparison.", "",
        "These are participating-applicant peer groups, not verified complete graduating classes. "
        "Examination performance was measured after time in the gymnasium; it is not a pre-gymnasium ability "
        "measure. The admission composite also contains this examination score. The cutoffs and outcomes "
        "come from the same allocation. This descriptive HERO does not separate prior sorting, peer "
        "development, preferences, and competitive congestion or identify a causal effect.", "",
        "The observed success fraction is not capacity divided by a known true competitor pool: applications "
        "and preferences remain unobserved. Broadening the designated set changes our definition of success, "
        "not the historical allocation or institutional capacity. No automatic search over tiers, model replay, "
        "fitted curve, significance test, or new geographic coverage was run. Only the explicitly recorded "
        "category and occupancy settings were used.", "",
        "Review the plots and their per-bin counts before deciding whether any next analysis is warranted. "
        "An absent downturn is a result, not a reason to search automatically for a more favorable definition.", "",
        "## Reproducibility", "",
        "The companion run record hashes the candidate manifest, every placement checkpoint, frozen scores, "
        "program table, implementation, decision record, and generated outputs. Raw personal records remain "
        "in the separate Desktop cache; the saved row audit contains generated row numbers rather than names.", "",
    ])
    (run_dir/"report.md").write_text("\n".join(report), encoding="utf-8")
    provenance.update({"code_sha256": source.sha256(Path(__file__)),
                       **settings,
                       "reference_run": str(reference_run) if reference_run is not None else None,
                       "reference_run_record_sha256": source.sha256(Path(reference_run)/"run_record.json") if reference_run is not None else None,
                       "decision_sha256": source.sha256(DECISION),
                       "supporting_code_sha256": {name: source.sha256(BASE/"code"/name) for name in (
                           "EDUCATION_20260930_romania_cache_workflow.py",
                           "EDUCATION_20260929_romania_gymnasium_differentiation_v1.py",
                           "EDUCATION_20260929_alba_2001_structural_audit.py",
                           "romania_archive_retrieval.py")},
                       "notebook_sha256": source.sha256(BASE/"notebooks"/"EDUCATION_20260930_Romania_2001_placements_and_HERO.ipynb"),
                       "completed_utc": source.now_utc(), "include_vocational": include_vocational,
                       "python": __import__("sys").version, "pandas": pd.__version__, "numpy": np.__version__,
                       "output_hashes": {str(p.relative_to(run_dir)):source.sha256(p)
                           for p in run_dir.rglob("*") if p.is_file() and p.name != "RUNNING.json"}})
    write_json(run_dir/"run_record.json", provenance)
    (run_dir/"RUNNING.json").unlink()
    print(f"Finished. Read: {run_dir/'report.md'}", flush=True)
    return {"status":"completed", "run_directory":str(run_dir), "variants":results}
