"""
Live sandbox for FY-aware UIC hierarchy testing with WDARFF files.

Reads:
    ./hierarchy_data/FMS_Web/WDARFF_15-26/WDARFF_YYYY.txt

Builds:
    - parent->children graph for each FY
    - subordinate expansion for supplied root UICs
    - lookup DataFrame: [fy, top_uic, asg_uic]
    - fake snapshot test + assignment diagnostics

Example:
    python3 uic_hierarchy_live_sandbox.py --roots WDARFF,W0ZUFF
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, Iterable, Set

import pandas as pd


DEFAULT_DATA_DIR = (
    "./hierarchy_data/FMS_Web/WDARFF_15-26"
)


def parse_fy_from_filename(path: Path) -> int:
    m = re.search(r"WDARFF_(\d{4})\.txt$", path.name)
    if not m:
        raise ValueError(f"Could not parse FY from filename: {path.name}")
    return int(m.group(1))


def load_wdarff_tables(data_dir: str) -> Dict[int, pd.DataFrame]:
    base = Path(data_dir)
    files = sorted(base.glob("WDARFF_*.txt"))
    if not files:
        raise FileNotFoundError(f"No WDARFF_*.txt files found in: {base}")

    by_fy: Dict[int, pd.DataFrame] = {}
    for fp in files:
        fy = parse_fy_from_filename(fp)
        df = pd.read_csv(fp, sep="\t", dtype=str, keep_default_na=False)
        need = {"UIC", "PARENTUIC"}
        missing = need - set(df.columns)
        if missing:
            raise ValueError(f"{fp.name} missing required columns: {sorted(missing)}")
        df["UIC"] = df["UIC"].str.strip()
        df["PARENTUIC"] = df["PARENTUIC"].str.strip()
        by_fy[fy] = df
    return by_fy


def build_parent_children(df: pd.DataFrame) -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = defaultdict(set)
    for _, r in df.iterrows():
        parent = (r.get("PARENTUIC") or "").strip()
        child = (r.get("UIC") or "").strip()
        if parent and child:
            out[parent].add(child)
    return out


def get_all_subordinates(
    parent_children: Dict[str, Set[str]],
    root_uic: str,
    include_root: bool = True,
    max_depth: int | None = None,
) -> Set[str]:
    visited = set()
    found = set([root_uic]) if include_root else set()
    q = deque([(root_uic, 0)])

    while q:
        cur, depth = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        if max_depth is not None and depth >= max_depth:
            continue
        for child in parent_children.get(cur, set()):
            if child not in found:
                found.add(child)
            q.append((child, depth + 1))
    return found


def build_lookup_for_roots(
    by_fy_tables: Dict[int, pd.DataFrame],
    roots: Iterable[str],
    include_root: bool = True,
) -> pd.DataFrame:
    rows = []
    roots = [r.strip() for r in roots if str(r).strip()]
    for fy, df in sorted(by_fy_tables.items()):
        pc = build_parent_children(df)
        for root in roots:
            members = get_all_subordinates(pc, root, include_root=include_root)
            for asg_uic in members:
                rows.append({"fy": fy, "top_uic": root, "asg_uic": asg_uic})
    out = pd.DataFrame(rows).drop_duplicates()
    return out


def make_fake_snapshots_from_lookup(df_lookup: pd.DataFrame, n_per_fy: int = 12) -> pd.DataFrame:
    work = df_lookup.sort_values(["fy", "asg_uic"]).copy()
    work = work.groupby("fy").head(n_per_fy).reset_index(drop=True)
    work["pid_pde"] = range(1, len(work) + 1)
    work["asg_uic_pde"] = work["asg_uic"]
    work["snpsht_dt"] = pd.to_datetime(work["fy"].astype(str) + "-03-31")
    return work[["pid_pde", "fy", "asg_uic_pde", "snpsht_dt"]]


def assign_from_lookup(
    df_snapshots: pd.DataFrame,
    df_lookup: pd.DataFrame,
    *,
    fy_col: str = "fy",
    uic_col_left: str = "asg_uic_pde",
    uic_col_right: str = "asg_uic",
    out_col: str = "div_name",
) -> pd.DataFrame:
    left = df_snapshots.copy()
    right = df_lookup[[fy_col, uic_col_right, "top_uic"]].drop_duplicates().copy()
    right = right.rename(columns={uic_col_right: uic_col_left, "top_uic": out_col})
    left[fy_col] = pd.to_numeric(left[fy_col], errors="coerce").astype("Int64")
    right[fy_col] = pd.to_numeric(right[fy_col], errors="coerce").astype("Int64")
    out = left.merge(right, on=[fy_col, uic_col_left], how="left")
    return out


def run(args: argparse.Namespace) -> None:
    roots = [r.strip() for r in args.roots.split(",") if r.strip()]
    if not roots:
        raise ValueError("Provide at least one root via --roots")

    by_fy = load_wdarff_tables(args.data_dir)
    print(f"Loaded FY tables: {sorted(by_fy)}")
    lookup = build_lookup_for_roots(by_fy, roots=roots, include_root=True)
    print(f"Lookup rows: {len(lookup):,}")
    print("Lookup sample:")
    print(lookup.head(12))

    fake = make_fake_snapshots_from_lookup(lookup, n_per_fy=args.n_per_fy)
    assigned = assign_from_lookup(fake, lookup)

    unknown_rate = assigned["div_name"].isna().mean() if len(assigned) else 0.0
    print(f"\nFake assignment rows: {len(assigned):,}")
    print(f"Unknown rate: {unknown_rate:.3%}")
    print("Assigned sample:")
    print(assigned.head(20))

    if args.save_lookup:
        out_path = Path(args.save_lookup)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        lookup.to_csv(out_path, index=False)
        print(f"Saved lookup CSV: {out_path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Live FY-aware UIC hierarchy sandbox")
    p.add_argument("--data-dir", default=DEFAULT_DATA_DIR, help="Directory of WDARFF_YYYY.txt files")
    p.add_argument(
        "--roots",
        default="WDARFF",
        help="Comma-separated root UICs to expand (example: WDARFF,W0ZUFF)",
    )
    p.add_argument("--n-per-fy", type=int, default=12, help="Fake rows per FY for assignment test")
    p.add_argument("--save-lookup", default="", help="Optional path to save built lookup as CSV")
    return p


if __name__ == "__main__":
    parser = build_parser()
    run(parser.parse_args())
