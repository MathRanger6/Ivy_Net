"""
503_hierarchies.py
Builds hierarchy lookups and a by-FY prestige UIC list for pipeline use.

This module is designed to be imported by Cell 7 in 520_pipeline_cox_working.ipynb.
It reads PRESTIGE_CONFIG from pipeline_config.py to determine which units
should be designated as prestige.
"""

from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd

from functionsG import load_feather, load_json, store_json
from pipeline_config import PRESTIGE_CONFIG, DIVISION_CONFIG, SOURCE_RANK


def _as_set_map(uics_by_fy: Dict) -> Dict[int, set]:
    """Convert {fy: [uics]} to {fy: set(uics)} with int FY keys."""
    out = {}
    for fy, uics in (uics_by_fy or {}).items():
        try:
            fy_int = int(fy)
        except Exception:
            continue
        out[fy_int] = set(uics or [])
    return out


def build_prestige_uics_by_fy(
    df_uic_div_lookup: pd.DataFrame,
    prestige_roots: Iterable[str],
    include_top_uics: bool = True,
) -> Dict[int, list]:
    """Return by-FY list of UICs under the given top UIC roots."""
    if df_uic_div_lookup is None or df_uic_div_lookup.empty:
        return {}
    if not prestige_roots:
        return {}

    prestige_roots = set(prestige_roots)
    needed_cols = {"uic", "top_uic", "fy"}
    missing = needed_cols - set(df_uic_div_lookup.columns)
    if missing:
        raise ValueError(f"Missing required columns in df_uic_div_lookup: {sorted(missing)}")

    df_prestige = df_uic_div_lookup[df_uic_div_lookup["top_uic"].isin(prestige_roots)].copy()
    if not include_top_uics:
        df_prestige = df_prestige[df_prestige["uic"] != df_prestige["top_uic"]]

    by_fy = (
        df_prestige.groupby("fy")["uic"]
        .apply(lambda s: sorted(set(s.dropna())))
        .to_dict()
    )
    return by_fy


def get_prestige_uics_by_fy(
    prestige_config: Optional[dict] = None,
    df_uic_div_lookup: Optional[pd.DataFrame] = None,
    save: bool = True,
    var_dir: str = "./running_vars",
) -> Dict[int, list]:
    """
    Build and optionally save prestige_uics_by_fy using PRESTIGE_CONFIG.
    Returns {fy: [uic, ...]}.
    """
    cfg = prestige_config or PRESTIGE_CONFIG
    prestige_roots = cfg.get("prestige_uic_roots", [])
    include_top = cfg.get("include_top_uics", True)
    out_name = cfg.get("prestige_list_name", "prestige_uics_by_fy")

    if df_uic_div_lookup is None:
        df_uic_div_lookup = load_feather("df_uic_div_lookup")

    by_fy = build_prestige_uics_by_fy(
        df_uic_div_lookup,
        prestige_roots=prestige_roots,
        include_top_uics=include_top,
    )

    # Optional backfill for early FYs (e.g., before UIC tables start)
    if by_fy and cfg.get("backfill_early_fy", False):
        min_fy = min(by_fy.keys())
        start_fy = cfg.get("backfill_start_fy", min_fy)
        if start_fy < min_fy:
            if cfg.get("backfill_use_union", True):
                union_uics = sorted({u for uics in by_fy.values() for u in (uics or [])})
                fill_list = union_uics
            else:
                fill_list = by_fy[min_fy]
            for fy in range(start_fy, min_fy):
                by_fy.setdefault(fy, fill_list)
    
    if save:
        store_json(by_fy, out_name, var_dir)
    return by_fy


def apply_prestige_unit(
    df_in: pd.DataFrame,
    prestige_uics_by_fy: Dict[int, list],
    fy_col: str = "fy",
    uic_col: str = "asg_uic_pde",
    out_col: str = "prestige_unit",
) -> pd.DataFrame:
    """
    Add/overwrite prestige_unit column based on a by-FY list of UICs.
    """
    df = df_in.copy()
    if fy_col not in df.columns or uic_col not in df.columns:
        df[out_col] = 0
        return df

    # Normalize FY to Int64 for clean merges
    df[fy_col] = pd.to_numeric(df[fy_col], errors="coerce").astype("Int64")

    # Build lookup DataFrame for merge
    rows = []
    for fy, uics in (prestige_uics_by_fy or {}).items():
        for uic in uics or []:
            rows.append({fy_col: fy, uic_col: uic})
    if not rows:
        df[out_col] = 0
        return df

    lookup = pd.DataFrame(rows).drop_duplicates()
    lookup[out_col] = 1

    df = df.merge(lookup, on=[fy_col, uic_col], how="left")
    df[out_col] = df[out_col].fillna(0).astype(int)
    return df


def load_prestige_uics_by_fy(
    prestige_config: Optional[dict] = None,
    var_dir: str = "./running_vars",
) -> Dict[int, list]:
    """Load prestige_uics_by_fy from JSON based on PRESTIGE_CONFIG."""
    cfg = prestige_config or PRESTIGE_CONFIG
    out_name = cfg.get("prestige_list_name", "prestige_uics_by_fy")
    try:
        return load_json(out_name, var_dir)
    except FileNotFoundError:
        return {}


def apply_division_name(
    df_in: pd.DataFrame,
    division_config: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Optionally add div_name by merging df_uic_hierarchy on UIC.
    """
    cfg = division_config or DIVISION_CONFIG
    print(f"####### number 1 (py)\n")
    if not cfg.get("enabled", False):
        print(" DIVISION CONFIG not enabled!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return df_in
    print(f"\n\n!!!!!!!!!!!! DIVISION_CONFIG (inside py_503): {DIVISION_CONFIG}")
    df = df_in.copy(); print(f"\n========= DIVISION_CONFIG  (cfg):    {cfg}\n==============================")
    print(f"####### number 2 (py)\n")
    print(f"\n\create_final_div_cpt  (py): {cfg.get('create_final_div_cpt')} ===================================")
    uic_file = cfg.get("uic_hierarchy_file", "df_uic_hierarchy");  print(f"uic_hierarchy_file  (py): {uic_file} ===================================")
    print(f"####### number 21 (py)\n")
    uic_col = cfg.get("uic_col", "asg_uic_pde"); print(f" uic_col (py) : {uic_col} ===================================")
    print(f"####### number 22 (py)\n")
    div_col = cfg.get("div_col", "div_name"); print(f" div_col  (py): {div_col} ===================================")
    fy_col = cfg.get("fy_col", "fy"); print(f" fy_col  (py): {fy_col} ===================================")
    use_fy_lookup = cfg.get("use_fy_lookup", False); print(f"use_fy_lookup   (py): {use_fy_lookup} ===================================")
    uic_div_lookup_file = cfg.get("uic_div_lookup_file", "df_uic_div_lookup"); print(f" uic_div_lookup_file  (py): {uic_div_lookup_file} ===================================")

    if div_col in df.columns:
        print("******** div_col is in df.columns!!!!")
        return df
    print(f"####### number 3 (py)\n")
    if use_fy_lookup and fy_col in df.columns:
        lookup_dir = cfg.get("uic_div_lookup_dir")
        try:
            if lookup_dir is not None:
                df_uic_lookup = load_feather(uic_div_lookup_file, load_dir=lookup_dir) 
            else:
                df_uic_lookup = load_feather(uic_div_lookup_file)
        except FileNotFoundError:
            df_uic_lookup = None; print("!!!!!!!!!!!!!!!!  NO df_uic_lookup !!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!!!!!!!!!!!!!!!   df_uic_lookup (py): {df_uic_lookup} !!!!!!!!!!!!!!!!!!!!!!!!!")
        if (
            df_uic_lookup is not None
            and div_col in df_uic_lookup.columns
            and uic_col in df_uic_lookup.columns
            and fy_col in df_uic_lookup.columns
        ):
            fy_vals = pd.to_numeric(df[fy_col], errors="coerce").astype("Int64")
            df[fy_col] = fy_vals

            if cfg.get("backfill_early_fy", False):
                backfill_fy = cfg.get("backfill_fy")
                if backfill_fy is not None:
                    df[fy_col] = df[fy_col].where(df[fy_col] >= backfill_fy, backfill_fy)

            # df = df.merge(
            #     df_uic_lookup[[uic_col, fy_col, div_col]].drop_duplicates(),
            #     on=[uic_col, fy_col],
            #     how="left",
            # )
            lk = df_uic_lookup[[uic_col, fy_col, div_col]].drop_duplicates().copy()
            lk[fy_col] = pd.to_numeric(lk[fy_col], errors="coerce").astype("Int64")

            df = df.merge(lk, on=[uic_col, fy_col], how="left")
            return df
    
    try:
        df_uic_hier = load_feather(uic_file)
    except FileNotFoundError:
        return df

    if div_col not in df_uic_hier.columns or uic_col not in df.columns:
        return df

    df = df.merge(
        df_uic_hier[[uic_col, div_col]].drop_duplicates(),
        on=uic_col,
        how="left",
    )
    return df


def add_division_metrics(
    df_in: pd.DataFrame,
    division_config: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Add division service metrics (cumulative time, ratio time, final_div_cpt),
    plus optional per-division cumulative/ratio metrics for a short list.
    """
    cfg = division_config or DIVISION_CONFIG
    if not cfg.get("enabled", False):
        return df_in

    df = df_in.copy()
    div_col = cfg.get("div_col", "div_name")
    pid_col = cfg.get("pid_col", "pid_pde")
    date_col = cfg.get("date_col", "snpsht_dt")
    rank_col = cfg.get("rank_col", "rank_pde")
    source_rank = cfg.get("source_rank", SOURCE_RANK)

    if div_col not in df.columns or pid_col not in df.columns or date_col not in df.columns:
        return df

    df = df.sort_values(by=[pid_col, date_col])
    seq = df.groupby(pid_col).cumcount() + 1

    if cfg.get("create_div_cum_time", True):
        df["div_cum_time"] = df[div_col].notna().groupby(df[pid_col]).cumsum().astype(int)

    if cfg.get("create_div_ratio_time", True):
        if "div_cum_time" not in df.columns:
            df["div_cum_time"] = df[div_col].notna().groupby(df[pid_col]).cumsum().astype(int)
        df["div_ratio_time"] = df["div_cum_time"] / seq

    if cfg.get("create_final_div_cpt", True) and rank_col in df.columns:
        rank_mask = df[rank_col] == source_rank
        last_div = (
            df[rank_mask]
            .groupby(pid_col)[div_col]
            .last()
            .to_dict()
        )
        df["final_div_cpt"] = df[pid_col].map(last_div)

    name_map = cfg.get("division_name_map", {}) or {}
    div_list = cfg.get("division_list", []) or []
    prefix = cfg.get("division_prefix", "div")

    if name_map and div_list:
        div_code = df[div_col].map(name_map)
        for code in div_list:
            code_safe = str(code).replace(" ", "").replace("/", "_")
            mask = (div_code == code).astype(int)
            cum_col = f"{prefix}_{code_safe}_cum_time"
            ratio_col = f"{prefix}_{code_safe}_ratio_time"
            df[cum_col] = mask.groupby(df[pid_col]).cumsum()
            df[ratio_col] = df[cum_col] / seq

    return df
