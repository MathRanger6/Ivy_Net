"""
Function to add date of rank (DOR) columns to a master dataframe.

This function adds columns like dor_cpt, dor_maj, etc. based on the first
occurrence of each rank in the ppln_pgrd_eff_dt column.
"""

import pandas as pd
import time


def time_start(process: str, nest: int = 0) -> float:
    """Start timing a process (simplified version)."""
    indent = '    ' * nest
    print(f"{indent}▶️  {process}...", end='', flush=True)
    return time.time()


def time_stop(start: float, nest: int = 0) -> None:
    """Stop timing a process and report duration (simplified version)."""
    indent = '    ' * nest
    elapsed = time.time() - start
    print(f" done. ({elapsed:.2f} sec)")


def add_dor_col(df_in, nest=0, rank_list=['CPT', 'MAJ']):
    """
    Add date of rank (DOR) columns to a master dataframe.
    
    For each rank in rank_list, finds the first occurrence of that rank
    (based on ppln_pgrd_eff_dt) for each officer and adds a dor_{rank.lower()}
    column to the dataframe.
    
    Parameters:
    -----------
    df_in : pandas.DataFrame
        Input dataframe with columns: pid_pde, snpsht_dt, rank_pde, ppln_pgrd_eff_dt
    nest : int, default 0
        Nesting level for indentation in timing messages
    rank_list : list, default ['CPT', 'MAJ']
        List of ranks to process (e.g., ['CPT', 'MAJ'])
    
    Returns:
    --------
    pandas.DataFrame
        Input dataframe with new DOR columns added (dor_cpt, dor_maj, etc.)
    """
    t0 = time_start(f"Add date of rank (dor) for {rank_list}", nest)
    
    # Make a copy of the FULL dataframe to avoid modifying original
    df = df_in.copy()
    
    # Extract only the columns we need for finding DOR dates
    dfw = df[['pid_pde', 'snpsht_dt', 'rank_pde', 'ppln_pgrd_eff_dt']].copy()
    
    # Sort by officer and snapshot date to ensure we get the first occurrence
    dfw = dfw.sort_values(by=["pid_pde", "snpsht_dt"])
    
    # Process each rank
    for rank in rank_list:
        dor_col = f"dor_{rank.lower()}"
        
        if dor_col not in df.columns:
            t1 = time_start(f"Adding {dor_col}...", nest=nest+1)
            
            # Find the first occurrence of this rank for each officer
            # Filter to rows with this rank, group by officer, take first occurrence
            rank_dates = (
                dfw[dfw["rank_pde"] == rank]
                .groupby("pid_pde")
                .first()["ppln_pgrd_eff_dt"]
            )
            
            # Add the DOR column to the FULL dataframe by mapping
            df[dor_col] = df["pid_pde"].map(rank_dates)
            
            time_stop(t1, nest=nest+1)
        else:
            print(f"Date of rank column {dor_col} is already in DataFrame")
    
    time_stop(t0, nest=nest)
    
    # Return the FULL dataframe with all original columns plus new DOR columns
    return df


# Example usage:
if __name__ == "__main__":
    # Create example data
    df_example = pd.DataFrame({
        'pid_pde': ['01', '01', '01', '01', '02', '02', '02'],
        'snpsht_dt': pd.to_datetime([
            '2017-03-31', '2017-06-30', '2017-09-30', '2017-12-31',
            '2017-06-30', '2017-09-30', '2017-12-31'
        ]),
        'rank_pde': ['CPT', 'CPT', 'MAJ', 'MAJ', 'CPT', 'CPT', 'MAJ'],
        'ppln_pgrd_eff_dt': pd.to_datetime([
            '2016-06-01', '2016-06-01', '2019-06-01', '2019-06-01',
            '2017-01-01', '2017-01-01', '2020-01-01'
        ]),
        'other_col': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    })
    
    print("Original dataframe:")
    print(df_example)
    print("\n" + "="*80 + "\n")
    
    result = add_dor_col(df_example, rank_list=['CPT', 'MAJ'])
    
    print("\n" + "="*80 + "\n")
    print("Dataframe with DOR columns:")
    print(result[['pid_pde', 'snpsht_dt', 'rank_pde', 'ppln_pgrd_eff_dt', 
                  'dor_cpt', 'dor_maj', 'other_col']])

