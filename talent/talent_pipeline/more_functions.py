"""
Utility functions for Army personnel data analysis pipeline.
This module provides functions for database connections, data I/O, timing, and logging.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_fy(date_in):
    """
    Returns the fiscal year (int) for a given date.
    Accepts:
    - pd.Timestamp
    - str (ISO format: 'YYYY-MM-DD', etc.)
    - datetime / datetime64
    """
    try:
        # Convert input to pd.Timestamp
        date_ts = pd.to_datetime(date_in)

        # Fiscal year: if month >= Oct, FY = year + 1; else, FY = year
        fy = date_ts.year + 1 if date_ts.month >= 10 else date_ts.year

        return fy
    except Exception as e:
        return f"Error processing {date_in}: {e}"

import pandas as pd

def add_fy_col(df_input, date_column='snpsht_dt'):
    """
    Adds a 'fy' column to the DataFrame that represents the DoD fiscal year.
    
    Parameters:
        df_input (pd.DataFrame): The input DataFrame with a datetime column.
        date_column (str): The name of the datetime column to convert to fiscal year.
    
    Returns:
        pd.DataFrame: a new df with the added 'fy' column.
    """
    df_out = df_input.copy()
    
    # Convert column to datetime64 if it's not already
    df_out[date_column] = pd.to_datetime(df_out[date_column], errors='coerce')

    # Apply fiscal year calculation
    df_out['fy'] = df_out[date_column].apply(
        lambda x: x.year + 1 if pd.notnull(x) and x.month >= 10 else (x.year if pd.notnull(x) else None)
    ).astype('Int64')  # Use nullable integer type if needed
    
    return df_out


def get_division_colors(divisions, palette='Set3'):
    """
    Given a list of 5-15 division names, returns a dictionary mapping each division to a unique color.
    Uses seaborn's color_palette for color consistency.
    
    Parameters:
        divisions (list of str): List of 5-15 division names.
        palette (str): Name of seaborn color palette to use (default 'Set3').
    Returns:
        dict: {division_name: color}
    """
    n = len(divisions)
    if not (5 <= n <= 15):
        raise ValueError("Number of divisions must be between 5 and 15.")
    colors = sns.color_palette(palette, n)
    return {div: colors[i] for i, div in enumerate(divisions)}

def move_column_after(df, column_name, after_column):
    """
    Move a column in a DataFrame after another specified column.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to modify.
        column_name (str): The name of the column to move.
        after_column (str): The name of the column after which to move the specified column.

    Returns:
        pd.DataFrame: The modified DataFrame with the specified column moved after the specified column.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    if after_column not in df.columns:
        raise ValueError(f"Column '{after_column}' not found in DataFrame.")

    # Get the index of the columns
    column_index = df.columns.get_loc(column_name)
    after_index = df.columns.get_loc(after_column)

    # Move the column after the specified column
    # Convert to lists to avoid pandas Index concatenation issues
    cols = df.columns.tolist()
    
    # Remove the column from its current position
    cols.pop(column_index)
    
    # Insert the column after the specified column
    # Adjust after_index if the removed column was before it
    if column_index < after_index:
        after_index -= 1
    
    cols.insert(after_index + 1, column_name)
    
    df = df.reindex(columns=cols)
    return df




def main(argv):
	
	
	return

if __name__ == '__main__':
	import sys
	main(sys.argv)	