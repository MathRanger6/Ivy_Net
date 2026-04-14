"""
Local sandbox for testing FY-aware division assignment.

Usage:
    python3 uic_division_sandbox.py

Then swap fake data with your live tables once you share them in Cursor.
"""

import pandas as pd


def assign_div_name_from_lookup(
    df_snapshots: pd.DataFrame,
    df_uic_div_lookup: pd.DataFrame,
    *,
    uic_col: str = "asg_uic_pde",
    fy_col: str = "fy",
    div_col: str = "div_name",
) -> pd.DataFrame:
    """Assign `div_name` by (UIC, FY) join and print coverage diagnostics."""
    need_left = {uic_col, fy_col}
    need_right = {uic_col, fy_col, div_col}
    miss_left = sorted(need_left - set(df_snapshots.columns))
    miss_right = sorted(need_right - set(df_uic_div_lookup.columns))
    if miss_left or miss_right:
        raise ValueError(
            f"Missing columns. snapshots missing={miss_left}, lookup missing={miss_right}"
        )

    left = df_snapshots.copy()
    right = df_uic_div_lookup[[uic_col, fy_col, div_col]].drop_duplicates().copy()

    left[fy_col] = pd.to_numeric(left[fy_col], errors="coerce").astype("Int64")
    right[fy_col] = pd.to_numeric(right[fy_col], errors="coerce").astype("Int64")

    out = left.merge(right, on=[uic_col, fy_col], how="left")
    if div_col in out.columns:
        unknown_rate = out[div_col].isna().mean()
        print(f"match rate: {(1 - unknown_rate):.3%}")
        print(f"unknown rate: {unknown_rate:.3%}")
        print("unknown by fy:")
        print(out.assign(_unknown=out[div_col].isna()).groupby(fy_col)["_unknown"].mean())
    return out


def _build_fake_data():
    snapshots = pd.DataFrame(
        {
            "pid_pde": [1, 2, 3, 4, 5, 6],
            "fy": [2019, 2019, 2020, 2020, 2021, 2021],
            "asg_uic_pde": ["UIC_A", "UIC_B", "UIC_A", "UIC_C", "UIC_D", "UIC_MISSING"],
            "snpsht_dt": pd.to_datetime(
                ["2019-02-01", "2019-03-01", "2020-04-01", "2020-05-01", "2021-06-01", "2021-07-01"]
            ),
        }
    )
    lookup = pd.DataFrame(
        {
            "fy": [2019, 2019, 2020, 2020, 2021],
            "asg_uic_pde": ["UIC_A", "UIC_B", "UIC_A", "UIC_C", "UIC_D"],
            "div_name": ["1ID", "25ID", "1ID", "82ABN", "10MTN"],
        }
    )
    return snapshots, lookup


if __name__ == "__main__":
    df_snap, df_lookup = _build_fake_data()
    print("fake snapshots:")
    print(df_snap)
    print("\nfake lookup:")
    print(df_lookup)
    print("\nassigning division labels...\n")
    df_out = assign_div_name_from_lookup(df_snap, df_lookup)
    print("\nresult:")
    print(df_out[["pid_pde", "fy", "asg_uic_pde", "div_name"]])
