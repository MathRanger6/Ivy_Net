


















from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any

# Canonical rank order (junior to senior).  OOO rows are inferred as LTC or above.
RANK_ORDER: List[str] = [
    "2LT", "1LT", "CPT", "MAJ", "LTC", "COL", "BG", "MG", "LTG", "GEN",
]
# NATO rank codes (OF = officer); used as the default mapping to cmd_lvl.
NATO_CMD_LVL = {
"2LT": "OF-00", "1LT": "OF-01", "CPT": "OF-02", "MAJ": "OF-03",
"LTC": "OF-04", "COL": "OF-05", "BG": "OF-06", "MG": "OF-07",
"LTG": "OF-08", "GEN": "OF-09",
}

SENIOR_RANKS: List[str] = ["LTC", "COL", "BG", "MG", "LTG", "GEN"]

def _ensure_datetime(ser: pd.Series) -> pd.Series:
	return pd.to_datetime(ser, errors='coerce')

def _build_dor_table(
    df: pd.DataFrame,
    pid_col: str,
    rank_col: str,
    dor_cpt_col: str,
    dor_maj_col: str,
    ppln_pgrd_col: str,
) -> pd.DataFrame:
    """
    Build a flat table (pid, dor_date, rank), one row per promotion, vectorized.
    Uses only dor_cpt and dor_maj as DoR columns; for OOO rows uses ppln_pgrd_col
    (no dor_ooo).  Used for merge_asof to infer rank at any snapshot date.
    """
    dor_dt = "dor_date"
    out_col = "NATO_rank"
    parts: List[pd.DataFrame] = []

    # CPT: one row per officer (use first no-null per pid)
    cpt = (
        df[[pid_col, dor_cpt_col]]
        .dropna(subset=[dor_cpt_col])
        .drop_duplicates(subset=[pid_col], keep="first")
    )
    cpt = cpt.rename(columns={dor_cpt_col: dor_dt})
    cpt[out_col] = "CPT"
    parts.append(cpt[[pid_col, dor_dt, out_col]])

    # MAJ
    maj = (
        df[[pid_col, dor_maj_col]]
        .dropna(subset=[dor_maj_col])
        .drop_duplicates(subset=[pid_col], keep="first")
    )
    maj = maj.rename(columns={dor_maj_col: dor_dt})
    maj[out_col] = "MAJ"
    parts.append(maj[[pid_col, dor_dt, out_col]])

    # OOO: one row per (pid, ppln_pgrd_eff_dt), rank = LTC, COL, ... by order
    ooo = (
        df.loc[df[rank_col] == "OOO", [pid_col, ppln_pgrd_col]]
        .dropna(subset=[ppln_pgrd_col])
        .drop_duplicates()
        .sort_values([pid_col, ppln_pgrd_col])
    )
    if len(ooo) > 0:
        ooo = ooo.rename(columns={ppln_pgrd_col: dor_dt})
        idx = ooo.groupby(pid_col, sort=False).cumcount()
        # Clamp idx so we never index past SENIOR_RANKS (officers with 6+ OOO dates cap at GEN)
        safe_idx = np.minimum(idx, len(SENIOR_RANKS) -1)
        ooo[out_col] = np.take(SENIOR_RANKS, safe_idx)
        parts.append(ooo[[pid_col, dor_dt, out_col]])
        
    dor_table = pd.concat(parts, axis=0, ignore_index=True)
    # Ensure date columns exists (concat can lack dor_dt if only OOO part had rows and used a different name)
    if dor_dt not in dor_table.columns:
        for src in [dor_cpt_col, dor_maj_col, ppln_pgrd_col]:
            if src in dor_table.columns:
                dor_table = dor_table.rename(columns={src: dor_dt})
                break
        else:
            raise KeyError(f"Expected column '{dor_dt}' after concat; got {list(dor_table.columns)}")
    dor_table[dor_dt] = pd.to_datetime(dor_table[dor_dt], errors="coerce")
    dor_table = dor_table.dropna(subset=[dor_dt]).sort_values([pid_col, dor_dt]).reset_index(drop=True)
    return dor_table

def add_cmd_lvl(
    df: pd.DataFrame,
    rank_col: str = "rank_pde",
    snapshot_date_col: str = "snpsht_dt",
    pid_col: str = "pid_pde",
    dor_cpt_col: str = "dor_cpt",
    dor_maj_col: str = "dor_maj",
    ppln_pgrd_col: str = "ppln_pgrd_eff_dt",
    cmd_lvl_col: str = "NATO_rank",
    rank_order: Optional[List[str]] = None,
    rank_to_cmd_lvl: Optional[Dict[str, str]] = None,
    inplace: bool = False,
    use_tqdm: bool = True,
) -> pd.DataFrame:
    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """
    if not inplace:
        df = df.copy()

    rank_to_cmd_lvl = rank_to_cmd_lvl if rank_to_cmd_lvl is not None else NATO_CMD_LVL
    
    pbar = None
    if use_tqdm:
        try:
            from tqdm.auto import tqdm
            pbar = tqdm(total=3, desc="add_cmd_lvl", dynamic_ncols=True, leave=False)
        except Exception as e:
            pbar = None; print(f"TQDM promblem: {e}!!")

    # 1) Vectorized: build flat DOR table (pid, dor_date, NATO_rank)
    dor_table = _build_dor_table(
        df, pid_col, rank_col, dor_cpt_col, dor_maj_col, ppln_pgrd_col
    )
    if pbar is not None:
        pbar.update(1)
    dor_dt_col = "dor_date"
    inferred_col = "NATO_rank"

    # Ensure dor_table has a column named dor_dt_col (in case _build_dor_table returned alternate name)
    if dor_dt_col not in dor_table.columns:
        for src in [dor_cpt_col, dor_maj_col, ppln_pgrd_col]:
            if src in dor_table.columns:
                dor_table = dor_table.rename(columns={src: dor_dt_col})
                break
        else:
            raise KeyError(
                f"dor_table missing date column '{dor_dt_col}'; has {list(dor_table.columns)}"
            )
            
    # 2) merge_asof: for each (pid, snpsht_dt) get latest DOR row where dor_date <= snpsht_dt
    left = df[[pid_col, snapshot_date_col]].copy()
    left[snapshot_date_col] = _ensure_datetime(left[snapshot_date_col])
    left = left.sort_values([snapshot_date_col, pid_col]).reset_index(drop=True)
    # Ensure right has dor_date as a column (not index) so merge_asof doesn't treat right_on as index level
    right = (
        dor_table[[pid_col, dor_dt_col, inferred_col]]
        .sort_values([dor_dt_col, pid_col])
        .reset_index(drop=True)
    )
    merged = pd.merge_asof(
        left,
        right,
        left_on=snapshot_date_col,
        right_on=dor_dt_col,
        by=pid_col,
        direction="backward",
    )
    # Attach NATO_rank back to df (merge preserves df row order)
    df = df.merge(
        merged[[pid_col, snapshot_date_col, inferred_col]],
        on=[pid_col, snapshot_date_col],
        how="left",
    )
    if pbar is not None:
        pbar.update(1)
        
    # 3) cmd_lvl: use rank_pde when not OOO, else use NATO_rank; map via NATO
    rank_vals = df[rank_col].astype(str).str.strip()
    is_ooo = rank_vals == "OOO"
    inferred = df[inferred_col]
    actual_rank = np.where(is_ooo, inferred, rank_vals)
    actual_rank = pd.Series(actual_rank, index=df.index)
    df[cmd_lvl_col] = actual_rank.map(rank_to_cmd_lvl).fillna("")
    # Only drop the temporary inferred-rank column if it's not the same as the output column
    if inferred_col != cmd_lvl_col:
        df.drop(columns=[inferred_col], inplace=True, errors="ignore")
    if pbar is not None:
        pbar.update(1)
        pbar.close()
    
    return df

if __name__ == "__main__":
    print("NATO_lvl: use add_cdm_lvl(df, ...) to add cmd_lvl (NATO rank) column.")























    
            