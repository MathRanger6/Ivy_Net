"""
503_hierarchies.py
Builds hierarchy lookups and a by-FY prestige UIC list for pipeline use.

This module is designed to be imported by Cell 7 in 520_pipeline_cox_working.ipynb.
It reads PRESTIGE_CONFIG from pipeline_config.py to determine which units
should be designated as prestige.
"""

from pathlib import Path
from typing import Callable, Dict, Iterable, Optional

import pandas as pd

from functionsG import load_feather, load_json, store_json
from pipeline_config import PRESTIGE_CONFIG, DIVISION_CONFIG, SOURCE_RANK


def _normalize_fy_for_merge(
    series: pd.Series,
    two_digit_pivot: int= 68,
) -> pd.Series:
    """
    Coerce fiscal year to nullable Int64 comparable across frames.
    
    - **Full years** (numeric ``>=100``), e.g. 1995 or 2015, are left unchanged.
    - **Two-digit** values (``>=100``) are expanded: if ``yy > two_digit_pivot``
    then ``1900 + yy``, else ``2000 + yy`` (smae idea as Y2K pivot: 95->1995,
    15->2015 when pivot is 68.
    
    ``two_digit_pivot`` defaults to 68 (69-99 -> 1969-1999, 00-68 -> 2000-2068).
    """
    v = pd.to_numeric(series, errors="coerce")
    short = v.notna() & (v < 100)
    mask_19 = short & (v > two_digit_pivot)
    mask_20 = short & (v <= two_digit_pivot)
    out =v.astype("float64")
    out = out.where(~mask_19, 1900 + v)
    out = out.where(~mask_20, 2000 + v)
    return out.astype("Int64")


def _normalize_fy_scalar(fy, two_digit_pivot: int = 68) -> Optional[int]:
    """Single FY value through the same rules as _normalize_fy_for_merge. """
    try:
        s = _normalize_fy_for_merge(pd.Series([fy]), two_digit_pivot=two_digit_pivot)
        v = s.iloc[0]
    except Exception:
        return None
    if pd.isna(v):
        return None
    return int(v)

    
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
    prestige_config: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Add/overwrite prestige_unit column based on a by-FY list of UICs.
    """
    cfg = prestige_config or PRESTIGE_CONFIG
    pivot = int(cfg.get("fy_tow_digit_pivot", 68))
    
    df = df_in.copy()
    if fy_col not in df.columns or uic_col not in df.columns:
        df[out_col] = 0
        return df

    df[fy_col] = _normalize_fy_for_merge(df[fy_col], two_digit_pivot=pivot)

    # Build lookup DataFrame for merge (FY keys may be two-digit from same 503 source as div lookup)
    rows = []
    for fy, uics in (prestige_uics_by_fy or {}).items():
        fy_i = _normalize_fy_scalar(fy, two_digit_pivot=pivot)
        if fy_i is None:
            continue
        for uic in uics or []:
            rows.append({fy_col: fy_i, uic_col: uic})
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


def ensure_prestige_metrics(
    df_in: pd.DataFrame,
    prestige_config: Optional[dict] = None,
    fy_col: str = "fy",
    uic_col: str = "asg_uic_pde",
    pid_col: str = "pid_pde",
    date_col: str = "snpsht_dt",
    unit_col: str = "prestige_unit",
    sum_col: str = "prestige_sum",
    mean_col: str = "prestige_mean",
    logger: Optional[Callable[[str], None]] = None,
):
    """
    Ensure prestige_unit and optional cumulative prestige metrics exist.

    Behavior is controlled by PRESTIGE_CONFIG keys:
    - enable_prestige_processing: master switch for this step (default True)
    - fy_two_digit_pivot: two-digit FY expansion (see _normalize_fy_for_merge)
    - create_prestige_sum: create cumulative sum column when missing (default True)
    - create_prestige_mean: create expanding mean column when missing (default False)
    """
    cfg = prestige_config or PRESTIGE_CONFIG
    log = logger or (lambda _msg: None)
    info = {
        "enabled": cfg.get("enable_prestige_processing", True),
        "created_unit": False,
        "created_sum": False,
        "created_mean": False,
    }
    df = df_in.copy()

    if not info["enabled"]:
        return df, info

    if unit_col not in df.columns:
        try:
            prestige_uics_by_fy = get_prestige_uics_by_fy(prestige_config=cfg)
            df = apply_prestige_unit(
                df,
                prestige_uics_by_fy,
                fy_col=fy_col,
                uic_col=uic_col,
                out_col=unit_col,
                prestige_config=cfg,
            )
            info["created_unit"] = True
        except Exception as exc:
            log(f"⚠️ Failed to create {unit_col}: {exc}")
            df[unit_col] = 0
            info["created_unit"] = True

    create_sum = cfg.get("create_prestige_sum", True)
    create_mean = cfg.get("create_prestige_mean", False)
    if unit_col in df.columns and (create_sum or create_mean):
        need_sum = create_sum and sum_col not in df.columns
        need_mean = create_mean and mean_col not in df.columns
        if need_sum or need_mean:
            df = df.sort_values(by=[pid_col, date_col])
            if need_sum:
                df[sum_col] = df.groupby(pid_col)[unit_col].cumsum()
                info["created_sum"] = True
            if need_mean:
                df[mean_col] = df.groupby(pid_col)[unit_col].transform(
                    lambda x: x.expanding().mean()
                )
                info["created_mean"] = True

    return df, info


def apply_division_name(
    df_in: pd.DataFrame,
    division_config: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Optionally add div_name by merging division lookup on (UIC, FY) or hierarchy on UIC.

    When using FY lookup, merge is left join: rows with no matching UICxFY keep
    NA in div_name (expected). Filtering/dropna in plots or analysis handles those.
    """
    cfg = division_config or DIVISION_CONFIG
    if not cfg.get("enabled", False):
        return df_in

    df = df_in.copy()
    uic_file = cfg.get("uic_hierarchy_file", "df_uic_hierarchy")
    uic_col = cfg.get("uic_col", "asg_uic_pde")
    div_col = cfg.get("div_col", "div_name")
    fy_col = cfg.get("fy_col", "fy")
    use_fy_lookup = cfg.get("use_fy_lookup", False)
    uic_div_lookup_file = cfg.get("uic_div_lookup_file", "df_uic_div_lookup")

    if div_col in df.columns:
        return df

    if use_fy_lookup and fy_col in df.columns:
        lookup_dir = cfg.get("uic_div_lookup_dir")
        debug_div = bool(cfg.get("debug_division", False));#print("DEBUG_DIV is GOOD")
        try:
            if lookup_dir is not None:
                df_uic_lookup = load_feather(uic_div_lookup_file, load_dir=lookup_dir)
            else:
                df_uic_lookup = load_feather(uic_div_lookup_file)
        except FileNotFoundError:
            df_uic_lookup = None

        if (
            df_uic_lookup is not None
            and div_col in df_uic_lookup.columns
            and uic_col in df_uic_lookup.columns
            and fy_col in df_uic_lookup.columns
        ):
            pivot = int(cfg.get("fy_two_digit_pivot", 68)); #print("PIVOT DEF  is GOOD")
            print(f"[DIV DEBUG] null fy values BEFORE _normalize...: {int(df[fy_col].isna().sum()):,}")
            df[fy_col] = _normalize_fy_for_merge(df[fy_col], two_digit_pivot=pivot); #print("NFFM  is GOOD")
            print(f"[DIV DEBUG] null fy values AFTER _normalize...: {int(df[fy_col].isna().sum()):,}")
            lk = df_uic_lookup[[uic_col, fy_col, div_col]].drop_duplicates().copy(); #print("LK DEF  is GOOD")
            lk[fy_col] = _normalize_fy_for_merge(lk[fy_col], two_digit_pivot=pivot); #print("LK NFFM  is GOOD")
            lk_fy_min = lk[fy_col].dropna().min() if not lk.empty else None;# print("LK_FY_MIN  is GOOD")
            
            if cfg.get("backfill_early_fy", False):
                backfill_fy = cfg.get("backfill_fy")
                if backfill_fy in (None, "lookup_min"):
                    bf = lk_fy_min
                else:
                    bf = _normalize_fy_scalar(backfill_fy, two_digit_pivot=pivot); print("NFS  is GOOD")
                    if bf is not None:
                        df[fy_col] = df[fy_col].where(df[fy_col] >= bf, bf)
                        if debug_div:
                            print(f"[DIV_DEBUG] Backfill FY floor applied at {bf} (lookup min FY={lk_fy_min})")
                            
            if debug_div:
                null_uic = int(df[uic_col].isna().sum()) if uic_col in df.columns else -1
                null_fy = int(df[fy_col].isna().sum()) if fy_col in df.columns else -1
                dup_keys = int(lk.duplicated([uic_col, fy_col]).sum())
                print(
                    f"[DIV_DEBUG] Pre-merge rows = {len(df):,}, null_{uic_col}={null_uic:,}, "
                    f"null{fy_col}={null_fy:,}, lookup_rows={len(lk):,}, dup_key_rows={dup_keys:,}"
                )
                if lk_fy_min is not None:
                    lk_fy_max = lk[fy_col].dropna().max()
                    print(f"[DIV_DEBUG] Lookup FY span: {int(lk_fy_min)} to {int(lk_fy_max)}") 
            
            df = df.merge(lk, on=[uic_col, fy_col], how="left", indicator=debug_div)
            if debug_div:
                merge_counts = df["_merge"].value_counts(dropna=False).to_dict()
                print(f"[DIV_DEBUG] Merge indicator counts: {merge_counts}")
                div_non_null = float(df[div_col].notna().mean())
                miss_n = int(df[div_col].isna().sum())
                print(f"[DIV_DEBUG] {div_col} non-null rate after merge: {div_non_null:.2%} ({len(df)-miss_n:,}/{len(df):,})")
                if miss_n > 0 and uic_col in df.columns:
                    print(f"[DIV_DEBUG] Top missing {uic_col} values:")
                    print(df.loc[df[div_col].isna(), uic_col].astype(str).value_counts().head(15))
                if miss_n > 0 and fy_col in df.columns:
                    print(f"[DIV_DEBUG] Top missing {fy_col} values:")
                    print(df.loc[df[div_col].isna(), fy_col].value_counts(dropna=False).head(15))
                df = df.drop(columns=["_merge"])
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
