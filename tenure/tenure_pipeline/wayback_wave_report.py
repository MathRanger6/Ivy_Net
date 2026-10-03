"""
Post-wave URL quality report — plan snaps, HTML on disk, mean parse records per file.

Usage:
  python tenure/tenure_pipeline/wayback_wave_report.py
  python tenure/tenure_pipeline/wayback_wave_report.py --slugs arizona_state_university
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from wayback.paths import SnapshotPathContext, faculty_source_id, normalize_faculty_url, normalize_wayback_slug_filter, slugify


def _default_path_ctx(tp: Path) -> SnapshotPathContext:
    ws = tp.parent
    html = tp / "faculty_snapshots"
    return SnapshotPathContext(
        workspace_root=ws,
        tenure_pipeline_dir=tp,
        faculty_snapshots_write_root=html,
        stage3_html_dir=html,
    )


def _load_schools(tp: Path) -> list[dict]:
    schools_py = tp / "r1_schools_data.py"
    ns: dict = {}
    exec(compile(schools_py.read_text(encoding="utf-8"), str(schools_py), "exec"), ns)
    return ns["PILOT_SCHOOLS"]


def _plan_stats(plan_path: Path) -> tuple[dict[tuple[str, str], int], dict[str, set[str]]]:
    """(slug, norm_url) → plan snap count; (slug, norm_url) → set local_path."""
    counts: dict[tuple[str, str], int] = defaultdict(int)
    paths: dict[tuple[str, str], set[str]] = defaultdict(set)
    if not plan_path.is_file():
        return counts, paths
    with open(plan_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("plan_row_type") == "cdx_bookmark":
                continue
            if r.get("n_snaps", 1) <= 0:
                continue
            slug = r.get("uni_slug") or ""
            src = r.get("source_url") or ""
            lp = r.get("local_path") or ""
            if not slug or not src or not lp:
                continue
            key = (slug, normalize_faculty_url(src))
            if lp not in paths[key]:
                paths[key].add(lp)
                counts[key] += 1
    return counts, paths


def _audit_mean_recs(audit_path: Path) -> dict[tuple[str, str], float]:
    """(uni_slug, source_id) → mean n_records per audit row."""
    sums: dict[tuple[str, str], list[float]] = defaultdict(list)
    if not audit_path.is_file():
        return {}
    with open(audit_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            slug = r.get("uni_slug") or ""
            lp = r.get("local_path") or ""
            n = r.get("n_records")
            if not slug or n is None:
                continue
            parts = lp.replace("\\", "/").split("/")
            sid = ""
            for i, p in enumerate(parts):
                if p == slug and i + 1 < len(parts):
                    sid = parts[i + 1]
                    break
            if sid:
                sums[(slug, sid)].append(float(n))
    return {k: sum(v) / len(v) for k, v in sums.items() if v}


def _html_count(path_ctx: SnapshotPathContext, slug: str, source_id: str) -> int:
    for root in path_ctx.search_roots():
        d = root / slug / source_id
        if d.is_dir():
            return sum(1 for _ in d.rglob("*.html"))
    return 0


def print_wave_report(
    *,
    tenure_pipeline_dir: Path | None = None,
    wayback_slugs: set[str] | None = None,
) -> None:
    tp = tenure_pipeline_dir or Path(__file__).resolve().parent
    path_ctx = _default_path_ctx(tp)
    slug_filter = normalize_wayback_slug_filter(wayback_slugs)

    plan_counts, _ = _plan_stats(tp / "faculty_snapshots_plan.jsonl")
    audit_means = _audit_mean_recs(tp / "faculty_snapshots_strategy_audit.jsonl")
    schools = _load_schools(tp)

    print("\n  Wayback URL report (plan snaps | HTML on disk | mean recs/file from parse audit)")
    print(f"  {'University':<42} {'URL (truncated)':<38} {'Plan':>5} {'HTML':>5} {'AvgRec':>7}")
    print("  " + "-" * 102)

    shown = 0
    for school in schools:
        slug = slugify(school["university"])
        if slug_filter and slug not in slug_filter:
            continue
        for url in school.get("urls", []):
            nu = normalize_faculty_url(url)
            sid = faculty_source_id(url)
            plan_n = plan_counts.get((slug, nu), 0)
            html_n = _html_count(path_ctx, slug, sid)
            avg_rec = audit_means.get((slug, sid))
            avg_s = f"{avg_rec:.1f}" if avg_rec is not None else "—"
            u_show = url if len(url) <= 36 else url[:33] + "..."
            print(
                f"  {school['university'][:42]:<42} {u_show:<38} {plan_n:>5} {html_n:>5} {avg_s:>7}"
            )
            shown += 1

    if shown == 0:
        print("  (no rows — check --slugs or r1_schools_data.py)")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Report plan/HTML/parse stats per faculty URL.")
    ap.add_argument("--slugs", type=str, default="", help="Comma-separated uni_slug filter")
    args = ap.parse_args()
    slugs = None
    if args.slugs.strip():
        slugs = {s.strip() for s in args.slugs.split(",") if s.strip()}
    print_wave_report(wayback_slugs=slugs)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
