import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, Iterable, Optional, Tuple


def get_fy(date_in) -> Optional[int]:
    try:
        date_ts = pd.to_datetime(date_in)
        fy = date_ts.year + 1 if date_ts.month >= 10 else date_ts.year
        return int(fy)
    except Exception:
        return np.nan


def cut_pids(df_in: pd.DataFrame, cut_pid_list: Iterable) -> pd.DataFrame:
    return df_in[~df_in["pid_pde"].isin(cut_pid_list)]


def id_pids_dup_apnt_dt(
    df_in: pd.DataFrame,
    while_rank: Optional[str] = None,
    compo_filter: Optional[str] = "R",
    verbose: bool = True,
) -> list:
    df_w = df_in.copy()
    if compo_filter and "compo" in df_w.columns:
        df_w = df_w[df_w["compo"] == compo_filter]
    if while_rank:
        df_w = df_w[df_w["rank_pde"] == while_rank]
        if verbose:
            print(f"df_w unique rank_pde values: {df_w.rank_pde.unique()}.")

    null_apnt_dt_pids_list = df_w[df_w["ofcr_apnt_dt"].isna()]["pid_pde"].unique().tolist()
    if verbose:
        print(
            f"There are {len(null_apnt_dt_pids_list):,} pids with any null "
            f"'ofcr_apnt_dt' values while {while_rank + ' and ' if while_rank else ''}RA."
        )

    df_w = df_w.dropna(subset=["ofcr_apnt_dt"])

    if verbose:
        null_apnt_dt_pids_list = df_w[df_w["ofcr_apnt_dt"].isna()]["pid_pde"].unique().tolist()
        print(
            f"There are {len(null_apnt_dt_pids_list):,} pids with any null "
            f"'ofcr_apnt_dt' values while {while_rank + ' and ' if while_rank else ''}RA."
        )
        data = df_w["ofcr_apnt_dt"].tolist()
        print("df pids", Counter([type(dd) for dd in data]))

    countr_dict = Counter(list(df_w[["pid_pde", "ofcr_apnt_dt"]].drop_duplicates().pid_pde))
    dup_list_apnt_dt_no_nulls = [p for p, v in countr_dict.items() if v > 1]
    if verbose:
        print(f"There are {len(dup_list_apnt_dt_no_nulls):,} pids with duplicate dates after dropna.")
    return dup_list_apnt_dt_no_nulls


def get_mode_dict_small_pids(
    pid_list: Iterable,
    rank: str,
    col: str,
    base_df: pd.DataFrame,
    verbose: bool = True,
) -> Dict:
    df = base_df[base_df.pid_pde.isin(pid_list)]
    df = df[df.rank_pde == rank]
    mode_result = df.groupby("pid_pde")[col].agg(lambda x: x.mode().iloc[0])
    mode_dict = mode_result.to_dict()
    if verbose:
        print(f" after mode_result, mode_result has {len(mode_result):,} pids")
        print(f" after mode_dict, mode_dict has {len(mode_dict):,} pids")
    return mode_dict


def get_mode_dict_for_col(
    df_in: pd.DataFrame,
    col: str,
    rank: Optional[str] = None,
    verbose: bool = True,
) -> Dict:
    df_w = df_in.copy()
    if rank:
        df_w = df_w[df_w.rank_pde == rank]
    elif col == "ppln_pgrd_eff_dt":
        raise ValueError(f"A rank argument is required for a {col} mode")

    df_w = df_w.dropna(subset=[col])
    if verbose:
        print("Getting mode_dict...")
        print(f" after {col} dropna df_w has {df_w.pid_pde.nunique():,} pids")

    if col == "ofcr_apnt_dt":
        df_w[col] = df_w[col].apply(get_fy)
        df_w = df_w.dropna(subset=[col])
        df_w[col] = df_w[col].astype(int)
        if verbose:
            print(f" after apply(get_fy) df_w has {df_w.pid_pde.nunique():,} pids")
            print(f" after apply(get_fy) df_w has {df_w[col].nunique():,} {col}'s")
            print("Null test: ", [val for val in df_w[col].unique().tolist() if val != val])

    if verbose:
        print("Generating mode_result...")
    mode_result = df_w.groupby("pid_pde")[col].agg(lambda x: x.mode().iloc[0])
    mode_dict = mode_result.to_dict()
    if verbose:
        print(f" after mode_result, mode_result has {len(mode_result):,} pids")
        print(f" after mode_dict, mode_dict has {len(mode_dict):,} pids")
        print(f" after mode_dict, mode_dict has {df_w[col].nunique():,} unique values for '{col}'")
        print("Null test: ", [val for val in mode_dict.values() if val != val])
    return mode_dict


def get_new_col(pos_dup_val_col: str, rank: str) -> str:
    if pos_dup_val_col == "ofcr_apnt_dt":
        return "yg"
    if pos_dup_val_col == "ppln_pgrd_eff_dt":
        return f"dor_{rank.lower()}"
    raise ValueError(f"Unknown input column {pos_dup_val_col}")


def remove_dup_pids_and_set_new_column(
    df_in: pd.DataFrame,
    rank: str,
    dup_list: Iterable,
    pos_dup_val_col: str = "ofcr_apnt_dt",
    verbose: bool = True,
) -> Tuple[pd.DataFrame, Dict]:
    new_col = get_new_col(pos_dup_val_col, rank)
    df = df_in.copy()

    if verbose:
        print(f"The new column will be '{new_col}'.")
        print(f"df_in has {df_in.pid_pde.nunique():,} unique_pids")
        print(f"df_in has {len(df_in):,} rows")
        print(f"There are {len(list(dup_list)):,} pids in the duplicate list")

    pre_cut_pids_num = df.pid_pde.nunique()
    df = cut_pids(df, dup_list)
    post_cut_pids_num = df.pid_pde.nunique()

    if verbose:
        print(f"df after cutting duplicate list has {df.pid_pde.nunique():,} unique_pids")
        print(f"df after cutting duplicate list has {len(df):,} rows")
        print(
            f"The DataFrame had {len(list(dup_list)):,} pids eliminated for duplicate "
            f"{pos_dup_val_col} values"
        )

    df = df.dropna(subset=[pos_dup_val_col], axis=0)

    if pos_dup_val_col == "ofcr_apnt_dt":
        if verbose:
            print(f"Filtering OUT rows that are not rank_pde == {rank}.")
        df = df[df.rank_pde == rank]

        df_6 = df[["pid_pde", pos_dup_val_col]].drop_duplicates()
        duplicate_pids = df_6.duplicated(subset=["pid_pde"], keep=False)
        duplicate_rows = df_6[duplicate_pids]
        if not duplicate_rows.empty:
            raise ValueError(f"There are still duplicate values for {pos_dup_val_col}")

        df_6[new_col] = df_6[pos_dup_val_col].apply(get_fy)
        df_6 = df_6.dropna(subset=[new_col])
        df_6[new_col] = df_6[new_col].astype(int)
        col_dict = dict(zip(df_6["pid_pde"], df_6[new_col]))
    elif pos_dup_val_col == "ppln_pgrd_eff_dt":
        df_6 = df[df.rank_pde == rank]
        df_6 = df_6.dropna(subset=[pos_dup_val_col], axis=0)
        df_6 = df_6[["pid_pde", pos_dup_val_col]].drop_duplicates()
        duplicate_pids = df_6.duplicated(subset=["pid_pde"], keep=False)
        duplicate_rows = df_6[duplicate_pids]
        if not duplicate_rows.empty:
            raise ValueError(f"There are still duplicate values for {pos_dup_val_col}")
        col_dict = dict(zip(df_6["pid_pde"], df_6[pos_dup_val_col]))
    else:
        raise ValueError(f"Unknown input column {pos_dup_val_col}")

    df[new_col] = df["pid_pde"].map(col_dict)
    return df, col_dict


def build_yg_dict_501(
    df_base: pd.DataFrame,
    rank: str = "CPT",
    salvage_from_rank: str = "MAJ",
    compo_filter: Optional[str] = "R",
    verbose: bool = True,
) -> Dict:
    pos_dup_val_col = "ofcr_apnt_dt"

    dup_list = id_pids_dup_apnt_dt(
        df_base,
        while_rank=rank,
        compo_filter=compo_filter,
        verbose=verbose,
    )

    df_gf, df_yg_dict = remove_dup_pids_and_set_new_column(
        df_base, rank=rank, dup_list=dup_list, pos_dup_val_col=pos_dup_val_col, verbose=verbose
    )

    no_match = [pid for pid in df_gf.pid_pde.unique().tolist() if pid not in df_yg_dict]
    if rank == "CPT" and no_match:
        no_match_and_rank = df_base[
            (df_base.pid_pde.isin(no_match)) & (df_base.rank_pde == rank)
        ].pid_pde.unique().tolist()
        df_check = df_base.dropna(subset=[pos_dup_val_col])
        no_match_and_salvage_checked = df_check[
            (df_check.pid_pde.isin(no_match)) & (df_check.rank_pde == salvage_from_rank)
        ].pid_pde.unique().tolist()
        no_match_rank_without_salvage = [
            pid for pid in no_match_and_rank if pid not in no_match_and_salvage_checked
        ]

        if verbose:
            print(
                f"There are {len(no_match_and_rank):,} pids whose only {rank} "
                f"{pos_dup_val_col} row is NaT"
            )
            print(
                f"But {len(no_match_and_salvage_checked):,} of them DO have "
                f"'{salvage_from_rank}' {pos_dup_val_col} rows not NaT"
            )
            print(
                f"So {len(no_match_and_salvage_checked):,} pids are salvageable"
            )

        df_gf2 = cut_pids(df_gf.dropna(subset=[pos_dup_val_col]), no_match)
        df_yg_dict2 = get_mode_dict_for_col(
            df_gf2, pos_dup_val_col, rank=rank, verbose=verbose
        )
        df_yg_dict_salvage = get_mode_dict_small_pids(
            no_match_and_salvage_checked,
            salvage_from_rank,
            pos_dup_val_col,
            base_df=df_base,
            verbose=verbose,
        )
        df_yg_dict2.update(df_yg_dict_salvage)
        df_yg_dict = df_yg_dict2

        if verbose:
            print(f"df_yg_dict has {len(df_yg_dict)} pid_pde's after salvage")

    return df_yg_dict


def apply_yg_dict(
    df_in: pd.DataFrame,
    yg_dict: Dict,
    col_name: str = "yg",
    dtype: str = "Int64",
) -> pd.DataFrame:
    df_out = df_in.copy()
    df_out[col_name] = df_out["pid_pde"].map(yg_dict)
    if dtype:
        df_out[col_name] = df_out[col_name].astype(dtype)
    return df_out

