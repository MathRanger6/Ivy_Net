"""
Stage 4 — HTML faculty parse (extracted from 540 Cell 4).
"""
from __future__ import annotations

import json
import time as _time
from collections import Counter
from pathlib import Path

import html_parser

from wayback.paths import SnapshotPathContext, normalize_wayback_slug_filter


def run_stage4_parse(
    *,
    path_ctx: SnapshotPathContext,
    stage3_plan: Path,
    stage4_out: Path,
    stage4_strat_out: Path,
    wayback_slugs: set[str] | None = None,
    parse_schools: list[str] | None = None,
    parse_despite_plan_sentinel: set[str] | None = None,
    condemn_on_failure: bool = False,
    min_faculty_per_file: int = 2,
) -> None:
    parse_despite_plan_sentinel = parse_despite_plan_sentinel or set()
    slug_filter = normalize_wayback_slug_filter(wayback_slugs)

    all_slugs = path_ctx.iter_slugs_with_html()
    if slug_filter:
        all_slugs = [s for s in all_slugs if s in slug_filter]
        print(f"  WAYBACK_SLUGS filter : {len(slug_filter)} slug(s) for parse")
    target_schools = parse_schools if parse_schools else all_slugs
    if slug_filter:
        target_schools = [s for s in target_schools if s in slug_filter]
    print(f"  Schools with HTML : {len(all_slugs)}")

    done_files: set[str] = set()
    parsed_slugs: set[str] = set()
    if stage4_out.exists():
        with open(stage4_out, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    lp = r.get("local_path", "")
                    if lp:
                        done_files.add(lp)
                    parsed_slugs.add(r.get("uni_slug", ""))
                except Exception:
                    pass
    print(
        f"  Checkpoint loaded  : {len(parsed_slugs):,} school(s) with existing records  "
        f"({len(done_files):,} files already parsed)"
    )

    cell4_skip_slug: dict[str, bool] = {}
    if stage3_plan.exists():
        with open(stage3_plan, encoding="utf-8") as pf:
            for line in pf:
                if not line.strip():
                    continue
                try:
                    pr = json.loads(line)
                except Exception:
                    continue
                us = pr.get("uni_slug")
                if not us:
                    continue
                real = (
                    pr.get("local_path")
                    and pr.get("year") is not None
                    and pr.get("season")
                    and pr.get("n_snaps", 1) != -1
                )
                if real:
                    cell4_skip_slug[us] = False
                elif pr.get("n_snaps") == -1 and ("Cell 4 auto-condemned" in (pr.get("reason") or "")):
                    cell4_skip_slug[us] = True

    new_schools = []
    for s in target_schools:
        school_dir = path_ctx.school_html_dir(s)
        html_files = sorted(school_dir.rglob("*.html")) if school_dir and school_dir.exists() else []
        new_html = [f for f in html_files if path_ctx.disk_html_to_plan_local_path(f) not in done_files]
        if new_html:
            new_schools.append(s)

    plan_skip_list = [
        s for s in new_schools if cell4_skip_slug.get(s, False) and s not in parse_despite_plan_sentinel
    ]
    new_schools = [
        s for s in new_schools if (not cell4_skip_slug.get(s, False)) or s in parse_despite_plan_sentinel
    ]
    if plan_skip_list:
        shown = ", ".join(plan_skip_list[:6])
        more = f" (+{len(plan_skip_list) - 6} more)" if len(plan_skip_list) > 6 else ""
        print(
            f"  Skipped (plan)     : {len(plan_skip_list)} school(s) — Cell 4 condemn sentinel: {shown}{more}"
        )

    n_new = len(new_schools)
    est_files = sum(
        len(
            [
                f
                for f in (path_ctx.school_html_dir(s) or Path()).rglob("*.html")
                if path_ctx.disk_html_to_plan_local_path(f) not in done_files
            ]
        )
        for s in new_schools
        if path_ctx.school_html_dir(s)
    )
    print(f"  Schools to parse   : {n_new}  (~{est_files:,} HTML files)")
    print(f"  {'─'*58}")

    stage4_out.parent.mkdir(parents=True, exist_ok=True)

    def _hms(s):
        s = max(0, int(s))
        h, r = divmod(s, 3600)
        m, sec = divmod(r, 60)
        return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"

    t_start = _time.time()
    total_records = 0
    total_files = 0
    school_summary = []

    with open(stage4_out, "a", encoding="utf-8") as out, open(stage4_strat_out, "a", encoding="utf-8") as strat:
        for s_idx, slug in enumerate(new_schools, 1):
            school_dir = path_ctx.school_html_dir(slug)
            if not school_dir or not school_dir.exists():
                continue
            html_files = sorted(school_dir.rglob("*.html"))
            if not html_files:
                continue

            n_files = 0
            uni_display = slug.replace("_", " ").title()
            elapsed = _time.time() - t_start
            rate_s = s_idx / elapsed if elapsed > 0 else 0
            remain = (n_new - s_idx) / rate_s if rate_s > 0 else 0
            pct = s_idx / n_new * 100 if n_new else 0
            eta_str = f"  ETA {_hms(remain)}" if elapsed > 5 else ""
            print(
                f"\n  [{s_idx:>3}/{n_new}] {pct:4.0f}%  ── {uni_display}"
                f"  ({len(html_files)} files)"
                f"  elapsed {_hms(elapsed)}{eta_str}"
                f"  │  {total_records:,} recs so far",
                flush=True,
            )

            school_recs = []
            last_meta = {"winner": "n/a"}
            new_html_files = [
                f for f in html_files if path_ctx.disk_html_to_plan_local_path(f) not in done_files
            ]
            is_first_parse = slug not in parsed_slugs

            for html_file in new_html_files:
                parts = html_file.stem.split("_")
                if len(parts) < 2:
                    continue
                try:
                    year = int(parts[0])
                except ValueError:
                    continue
                season = parts[1]

                recs, meta = html_parser.extract_faculty(html_file, slug, return_meta=True)
                if len(recs) < min_faculty_per_file:
                    continue
                last_meta = meta
                lp = path_ctx.disk_html_to_plan_local_path(html_file)
                strat_rec = {
                    "uni_slug": slug,
                    "year": year,
                    "season": season,
                    "local_path": lp,
                    "winner": meta["winner"],
                    "n_records": len(recs),
                    "strategy_counts": meta["counts"],
                }
                for r in recs:
                    record = {
                        "university": uni_display,
                        "uni_slug": slug,
                        "year": year,
                        "season": season,
                        "name": r["name"],
                        "rank": r["rank"],
                        "rank_raw": r.get("rank_raw", ""),
                        "parse_strategy": r.get("parse_strategy", ""),
                        "local_path": lp,
                    }
                    school_recs.append((record, strat_rec))
                n_files += 1

            bad_reason = None
            n_recs = len(school_recs)
            if n_recs == 0:
                bad_reason = "zero_records_after_filter"
            else:
                name_counts = Counter(rec["name"] for rec, _ in school_recs)
                top_name, top_n = name_counts.most_common(1)[0]
                n_unique = len(name_counts)
                if top_n / n_recs > 0.40 and n_unique < 8:
                    bad_reason = (
                        f"profile_page_trap — '{top_name}' appears {top_n}/{n_recs} times "
                        f"({top_n/n_recs:.0%}), only {n_unique} unique names"
                    )

            if bad_reason and not is_first_parse:
                bad_reason = None

            if bad_reason:
                if condemn_on_failure:
                    import shutil

                    sentinel = {
                        "university": uni_display,
                        "uni_slug": slug,
                        "n_snaps": -1,
                        "tried_primary_url": "",
                        "tried_urls": [],
                        "queried_at": _time.strftime("%Y-%m-%d"),
                        "reason": f"Cell 4 auto-condemned: {bad_reason}",
                    }
                    with open(stage3_plan, "a", encoding="utf-8") as pf:
                        pf.write(json.dumps(sentinel) + "\n")
                    shutil.rmtree(school_dir, ignore_errors=True)
                    print(f"     ⚠  CONDEMNED — {bad_reason}", flush=True)
                else:
                    print(f"     ⚠  Quality check failed — {bad_reason}", flush=True)
                    print("        No records written; HTML preserved  (CELL4_CONDEMN_ON_FAILURE=False)", flush=True)
                school_summary.append((slug, n_files, 0, 0.0))
                continue

            written_strats = set()
            for record, strat_rec in school_recs:
                out.write(json.dumps(record) + "\n")
                strat_key = (
                    strat_rec["uni_slug"],
                    strat_rec["year"],
                    strat_rec["season"],
                    strat_rec["local_path"],
                )
                if strat_key not in written_strats:
                    strat.write(json.dumps(strat_rec) + "\n")
                    written_strats.add(strat_key)

            out.flush()
            strat.flush()
            avg = n_recs / max(n_files, 1)
            total_records += n_recs
            total_files += n_files
            school_summary.append((slug, n_files, n_recs, avg))
            print(
                f"     → {n_files} files  │  {n_recs:,} records  │  avg {avg:.1f}/file  │  "
                f"winner: {last_meta['winner']}",
                flush=True,
            )

    print(f"\n{'School':<48} {'Files':>6} {'Records':>8} {'Avg/file':>9}")
    print("-" * 80)
    for slug, nf, nr, avg in sorted(school_summary):
        flag = "✅" if avg >= 10 else ("⚠️ " if avg >= 3 else "❌")
        print(f"  {flag} {slug:<46} {nf:6d} {nr:8,} {avg:9.1f}")

    print(f"\n  Total records written : {total_records:,}")
    print(f"  Total files parsed    : {total_files:,}")
    print(f"  Output                : {stage4_out.name}")
    print(f"  Strategy audit        : {stage4_strat_out.name}")


def run_stage4_from_globals(g: dict) -> None:
    if not g.get("RUN_CELL4"):
        return
    from wayback.paths import snapshot_path_context_from_globals

    g["reload_py_files"]()
    import html_parser  # noqa: F401 — reload side effect

    path_ctx = snapshot_path_context_from_globals(g)
    clk = g["time_start"]("Stage 4 — HTML Faculty Parse (all schools, all ranks)")
    run_stage4_parse(
        path_ctx=path_ctx,
        stage3_plan=Path(g["STAGE3_PLAN"]),
        stage4_out=Path(g["STAGE4_OUT"]),
        stage4_strat_out=Path(g["STAGE4_STRAT_OUT"]),
        wayback_slugs=g.get("WAYBACK_SLUGS"),
        parse_schools=g.get("PARSE_SCHOOLS"),
        parse_despite_plan_sentinel=set(g.get("CELL4_PARSE_DESPITE_PLAN_SENTINEL") or []),
        condemn_on_failure=bool(g.get("CELL4_CONDEMN_ON_FAILURE", False)),
        min_faculty_per_file=int(g.get("MIN_FACULTY_PER_FILE", 2)),
    )
    g["time_stop"](clk)
