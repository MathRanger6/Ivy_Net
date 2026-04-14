"""
Function to join Officer Evaluation Report (OER) data to snapshot data
based on officer ID and overlapping date intervals.

This performs an interval overlap join where:
- df_mpb.pid_pde == df_oer.rated_ofcr
- df_mpb.snpsht_dt falls within [df_oer.eval_strt_dt, df_oer.eval_thru_dt]

Updated with complete implementation from 512_oer_int_working.ipynb CELL 4:
- Pool metrics creation
- OER deduplication
- High overlap reporting
- oer_source and n_oers_overlapping columns
- Primary recent strategy with comprehensive diagnostics
"""

import pandas as pd
import numpy as np


def join_oer_to_snapshots(df_mpb_in=None, df_oer_in=None,
                          dfbm=None, df_oer=None,  # Legacy parameter names for backward compatibility
                          pid_col='pid_pde', 
                          snapshot_date_col='snpsht_dt',
                          rated_officer_col='rated_ofcr',
                          start_date_col='eval_strt_dt',
                          thru_date_col='eval_thru_dt',
                          how='left',
                          keep_all_matches=True,
                          strategy=None,  # 'primary_recent' or 'overlap_all'
                          snr_rater_col='snr_rater',
                          rater_col='rater',
                          rater_box_col='rater_box',
                          snr_rater_box_col='snr_rater_box',
                          create_pool_metrics=False,
                          deduplicate_oers_for_count=True,
                          report_high_overlaps=True,
                          high_overlap_threshold=5):
    """
    Join OER evaluation data to snapshot data based on overlapping date intervals.
    
    Parameters:
    -----------
    df_mpb_in : pandas.DataFrame, optional
        Snapshot dataframe with pid_pde and snpsht_dt columns (new parameter name)
    df_oer_in : pandas.DataFrame, optional
        OER dataframe with rated_ofcr, eval_strt_dt, and eval_thru_dt columns (new parameter name)
    dfbm : pandas.DataFrame, optional
        Snapshot dataframe (legacy parameter name, used if df_mpb_in not provided)
    df_oer : pandas.DataFrame, optional
        OER dataframe (legacy parameter name, used if df_oer_in not provided)
    pid_col : str, default 'pid_pde'
        Column name for officer ID in df_mpb
    snapshot_date_col : str, default 'snpsht_dt'
        Column name for snapshot date in df_mpb
    rated_officer_col : str, default 'rated_ofcr'
        Column name for officer ID in df_oer
    start_date_col : str, default 'eval_strt_dt'
        Column name for evaluation start date in df_oer
    thru_date_col : str, default 'eval_thru_dt'
        Column name for evaluation end date in df_oer
    how : str, default 'left'
        Type of join: 'left', 'inner', 'right', or 'outer'
        - 'left': Keep all snapshots (default, matches your requirement)
        - 'inner': Keep only snapshots with matching evaluations
        - 'right': Keep all evaluations
        - 'outer': Keep all snapshots and evaluations
    keep_all_matches : bool, default True
        If strategy='overlap_all': keeps all matching evaluations (may create duplicates)
        If strategy='primary_recent': ignored (always one row per snapshot)
    strategy : str, optional
        Strategy for handling multiple overlapping OERs:
        - 'primary_recent': Select the OER whose period contains snapshot date,
          prioritizing the one with the most recent thru date (captures recency bias).
          If no containing OER, leaves as NaN (unrated time).
        - 'overlap_all': Original behavior - keep all overlapping OERs
        If None, uses keep_all_matches to determine behavior
    snr_rater_col : str, default 'snr_rater'
        Column name for senior rater pid_pde in df_oer
    rater_col : str, default 'rater'
        Column name for rater pid_pde in df_oer
    rater_box_col : str, default 'rater_box'
        Column name for rater's evaluation box score in df_oer
    snr_rater_box_col : str, default 'snr_rater_box'
        Column name for senior rater's evaluation box score in df_oer
    create_pool_metrics : bool, default False
        If True creates senior rater pool metrics:
        - 'snr_rater_pool_snr_rater_box_mean': Mean of snr_rater_box for all officers
          rated by the same senior rater at the same snapshot date
    deduplicate_oers_for_count : bool, default True
        If True, deduplicates OERs (based on eval_id or rated_officer + dates)
        before counting overlaps. This prevents duplicate OERs from inflating 
        the n_oers_overlapping count. Recommended if your df_oer may contain duplicates.
    report_high_overlaps : bool, default True
        If True, reports diagnostic information about snapshots with unusually
        high numbers of overlapping OERs (>= high_overlap_threshold).
    high_overlap_threshold : int, default 5
        Threshold for reporting high overlap cases. Snapshots with n_oers_overlapping
        >= this value will be included in diagnostic reports.
    
    Returns:
    --------
    pandas.DataFrame
        Joined dataframe with all df_mpb columns plus all df_oer columns.
        Snapshots without matching evaluations will have NaN for OER columns
        (unless how='inner').
        Added columns when strategy='primary_recent':
        - 'oer_source': 'active' (OER period contains snapshot), 'unrated_time', or NaN
        - 'n_oers_overlapping': Count of OERs that overlapped (for diagnostics)
        - If create_pool_metrics=True: 'snr_rater_pool_snr_rater_box_mean'
    
    Notes:
    ------
    - Ensures date columns are datetime type
    - 'primary_recent' strategy preserves one-row-per-snapshot structure
    - 'primary_recent' prioritizes recency bias (most recent evaluation context)
    - Handles unrated time as NaN (no backward/forward fill)
    - Pre-filters OERs to officers in master for optimization
    """
    
    # Handle parameter name aliases (support both new and legacy names)
    if df_mpb_in is not None:
        df_mpb = df_mpb_in
    elif dfbm is not None:
        df_mpb = dfbm
    else:
        raise ValueError("Either df_mpb_in or dfbm must be provided")
    
    if df_oer_in is not None:
        df_oer = df_oer_in
    elif df_oer is None:
        raise ValueError("Either df_oer_in or df_oer must be provided")
    
    # Handle strategy parameter (default to 'overlap_all' if not specified)
    if strategy is None:
        if keep_all_matches:
            strategy = 'overlap_all'
        else:
            strategy = 'primary_recent'
    elif strategy == 'primary_recent':
        keep_all_matches = False  # Always one row per snapshot for primary_recent
    elif strategy == 'overlap_all':
        # keep_all_matches is already set by user
        pass
    else:
        raise ValueError(f"Unknown strategy: {strategy}. Use 'primary_recent' or 'overlap_all'")
    
    # Make copies to avoid modifying originals
    df_mpb = df_mpb.copy()
    df_oer = df_oer.copy()
    
    # Add a unique identifier for each row in df_mpb to track them through the merge
    # This ensures we can preserve ALL df_mpb rows in a left join
    df_mpb['_df_mpb_row_id'] = range(len(df_mpb))
    
    # Ensure date columns are datetime
    date_cols_bm = [snapshot_date_col]
    date_cols_oer = [start_date_col, thru_date_col]
    
    for col in date_cols_bm:
        if col in df_mpb.columns:
            df_mpb[col] = pd.to_datetime(df_mpb[col], errors='coerce')
    
    for col in date_cols_oer:
        if col in df_oer.columns:
            df_oer[col] = pd.to_datetime(df_oer[col], errors='coerce')
    
    # Remove any rows with missing dates (can't join these)
    df_oer_clean = df_oer[
        df_oer[start_date_col].notna() & 
        df_oer[thru_date_col].notna()
    ].copy()
    
    print(f"📊 OER data: {len(df_oer):,} total evaluations, {len(df_oer_clean):,} with valid dates")
    
    # Check for duplicate OERs
    if deduplicate_oers_for_count:
        n_before_dedup = len(df_oer_clean)
        # Prefer eval_id if available (true unique identifier), otherwise use officer + dates
        if 'eval_id' in df_oer_clean.columns:
            # Use eval_id as the unique OER identifier
            dedup_subset = ['eval_id']
            dedup_desc = 'eval_id'
        else:
            # Fall back to officer + dates if eval_id not available
            dedup_subset = [rated_officer_col, start_date_col, thru_date_col]
            dedup_desc = 'officer/start/thru dates'

        df_oer_clean = df_oer_clean.drop_duplicates(
            subset=dedup_subset,
            keep='first'
        ).copy()
        n_after_dedup = len(df_oer_clean)
        if n_before_dedup > n_after_dedup:
            print(f"  ⚠️ Removed: {n_before_dedup - n_after_dedup:,} duplicate OERs (based on {dedup_desc})")
               
    # Pre-filter OERs to only officers present in df_mpb (optimization for merge speed)
    n_before_filter = len(df_oer_clean)
    officers_in_master = df_mpb[pid_col].unique().tolist()
    df_oer_clean = df_oer_clean[df_oer_clean[rated_officer_col].isin(officers_in_master)].copy()
    n_after_filter = len(df_oer_clean)
    if n_before_filter > n_after_filter:
        print(f"     !! Filtered to officers in master: {n_before_filter:,} -> {n_after_filter:,} OERs ({n_before_filter - n_after_filter:,} removed)")
        
    # First, merge on officer ID only
    # This creates a cartesian product for each officer, which we'll filter
    merged = df_mpb.merge(
        df_oer_clean,
        left_on=pid_col,
        right_on=rated_officer_col,
        how=how,
        suffixes=('', '_oer')
    )
    
    print(f"📊 After merge on officer ID: {len(merged):,} rows")
    
    # Filter to only rows where snapshot date falls within evaluation period
    # Condition: start_date <= snpsht_dt <= thru_date
    overlap_mask = (
        merged[snapshot_date_col].notna() &
        merged[start_date_col].notna() &
        merged[thru_date_col].notna() &
        (merged[start_date_col] <= merged[snapshot_date_col]) &
        (merged[snapshot_date_col] <= merged[thru_date_col])
    )
    
    # Apply strategy-specific filtering
    # Store rows_with_overlap for diagnostics (needed later)
    rows_with_overlap_for_diagnostics = None
    
    if strategy == 'primary_recent':
        # Primary recent strategy: Select one OER per snapshot with most recent thru date
        if how == 'left':
            # Step 1: Get all rows where OER period contains snapshot date
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            rows_with_overlap = merged[overlap_mask]
            # Only keep diagnostics copy if actually needed (saves memory)
            rows_with_overlap_for_diagnostics = rows_with_overlap if report_high_overlaps else None
            if len(rows_with_overlap) > 0:
                # For each snapshot, select the OER with most recent thru_date (captures recency bias)
                # Sort by snapshot_date, then by thru_date descending (most recent first)
                rows_with_overlap = rows_with_overlap.sort_values(
                    by=[snapshot_date_col, thru_date_col],
                    ascending=[True, False])

                # Keep only the first (most recent thru date per snapshot)
                # drop_duplicates() already returns new DataFrame, no need for .copy()
                primary_oers = rows_with_overlap.drop_duplicates(
                    subset=['_df_mpb_row_id'],
                    keep='first'
                )
                
                # Add metadata columns
                primary_oers['oer_source'] = 'active'
    
                # Count how many OERs overlapped (for diagnostics)
                # If deduplicate_oers_for_count, deduplicated based on OER identity before counting
                if deduplicate_oers_for_count:
                    # Deduplicate rows_with_overlap based on OER identity
                    # Prefer eval_id if available (true unique identifier), otherwise use officer + dates
                    if 'eval_id' in rows_with_overlap.columns:
                        # Use eval_id as the unique OER identifier
                        dedup_subset = ['_df_mpb_row_id', 'eval_id']
                    else:
                        # Fall back to officer + dates if eval_id not available
                        dedup_subset = ['_df_mpb_row_id', rated_officer_col, start_date_col, thru_date_col]

                    # This ensures each unique OER is only counted once per snapshot
                    rows_for_counting = rows_with_overlap.drop_duplicates(
                        subset=dedup_subset,
                        keep='first'
                    )
                else:
                    rows_for_counting = rows_with_overlap
                
                overlap_counts = rows_for_counting.groupby('_df_mpb_row_id').size().reset_index(name='n_oers_overlapping')
                primary_oers = primary_oers.merge(overlap_counts, on='_df_mpb_row_id', how='left')
            else:
                # No overlaps - create empty DataFrame with same columns as merged
                primary_oers = pd.DataFrame(columns=list(merged.columns) + ['oer_source', 'n_oers_overlapping'])

            # Step 2: Get df_mpb rows with no officer match (already have NaN OER columns)
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            rows_no_officer_match = merged[merged[start_date_col].isna()]
            rows_no_officer_match['oer_source'] = np.nan
            rows_no_officer_match['n_oers_overlapping'] = 0
    
            # Step 3: Find the df_mpb rows that matched an officer but no OER period contained snapshot
            df_mpb_rows_with_oer = set(primary_oers['_df_mpb_row_id'].unique()) if len(primary_oers) > 0 else set()
            df_mpb_rows_no_officer = set(rows_no_officer_match['_df_mpb_row_id'].unique())
            all_df_mpb_rows = set(df_mpb['_df_mpb_row_id'])
            missing_df_mpb_rows = all_df_mpb_rows - df_mpb_rows_with_oer - df_mpb_rows_no_officer
    
            # Step 4: For missing rows (officer matched but snapshot not in any OER period = unrated time)
            result_parts = [primary_oers, rows_no_officer_match]

            if len(missing_df_mpb_rows) > 0:
                # Get one representative row per missing df_mpb row
                # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
                missing_rows_data = merged[merged['_df_mpb_row_id'].isin(missing_df_mpb_rows)]
                # drop_duplicates() already returns new DataFrame, no need for .copy()
                missing_rows_representative = missing_rows_data.drop_duplicates(
                    subset=['_df_mpb_row_id'],
                    keep='first'
                )
    
                # Set OER columns to NaN and mark as 'unrated_time'
                oer_cols = [col for col in df_oer_clean.columns if col != rated_officer_col]
                for col in oer_cols:
                    missing_rows_representative[col] = np.nan
    
                missing_rows_representative['oer_source'] = 'unrated_time'
                missing_rows_representative['n_oers_overlapping'] = 0
    
                result_parts.append(missing_rows_representative)

            # Combine all parts
            result = pd.concat(result_parts, ignore_index=True)

        else:
            # For non-left joins with primary_recent, use the same logic but filter differently
            if how == 'inner':
                # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
                rows_with_overlap = merged[overlap_mask]
                if len(rows_with_overlap) > 0:
                    rows_with_overlap = rows_with_overlap.sort_values(
                        by=[snapshot_date_col, thru_date_col],
                        ascending=[True, False])
                    # drop_duplicates() already returns new DataFrame, no need for .copy()
                    result = rows_with_overlap.drop_duplicates(
                        subset=['_df_mpb_row_id'],
                        keep='first'
                    )
                    result['oer_source'] = 'active'
                    overlap_counts = rows_with_overlap.groupby('_df_mpb_row_id').size().reset_index(name='n_oers_overlapping')
                    result = result.merge(overlap_counts, on='_df_mpb_row_id', how='left')
                else:
                    result = pd.DataFrame(columns=merged.columns)
            else:
                # for right/outer, fall back to overlap_all logic
                strategy = 'overlap_all'

    # Original overlap_all strategy
    if strategy == 'overlap_all':
        if how == 'left':
            # For left join, keep ALL df_mpb rows
            # Strategy:
            # 1. Keep rows with date overlap (overlap_mask = True)
            # 2. Keep rows with no officer match (start_date_col is NaN from merge)
            # 3. For rows with officer match but no date overlap: keep ONE row per df_mpb row, set OER cols to NaN

            # Step 1: Get rows with valid date overlap
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            result_with_overlap = merged[overlap_mask]
    
            # Step 2: Get df_mpb rows with no officer match (these already have NaN OER columns)
            # drop_duplicates() already returns new DataFrame, no need for .copy()
            rows_no_officer_match = merged[merged[start_date_col].isna()]
    
            # Step 3: Find the df_mpb rows that are NOT yet represented (officer matched but dates didn't overlap)
            df_mpb_rows_with_overlap = set(result_with_overlap['_df_mpb_row_id'].unique())
            df_mpb_rows_no_match = set(rows_no_officer_match['_df_mpb_row_id'].unique())
            all_df_mpb_rows = set(df_mpb['_df_mpb_row_id'])
            missing_df_mpb_rows = all_df_mpb_rows - df_mpb_rows_with_overlap - df_mpb_rows_no_match
    
            # Step 4: For missing rows (officer match but no date overlap), get ONE representative row
            # and set OER columns to NaN
            result_parts = [result_with_overlap, rows_no_officer_match]
    
            if len(missing_df_mpb_rows) > 0:
                # Get merge results for these rows (they have officer match but dates don't overlap)
                # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
                missing_rows_data = merged[merged['_df_mpb_row_id'].isin(missing_df_mpb_rows)]
                # Take first row per missing df_mpb row
                # drop_duplicates() already returns new DataFrame, no need for .copy()
                missing_rows_representative = missing_rows_data.drop_duplicates(
                    subset=['_df_mpb_row_id'],
                    keep='first'
                )
    
                # Set OER columns to NaN for these non-overlapping rows
                oer_cols = [col for col in df_oer_clean.columns if col != rated_officer_col]
                for col in oer_cols:
                    missing_rows_representative[col] = np.nan

                result_parts.append(missing_rows_representative)
    
            # Combine all parts
            result = pd.concat(result_parts, ignore_index=True)

        elif how == 'inner':
            # For inner join, only keep matches
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            result = merged[overlap_mask]
        elif how == 'right':
            # For right join, keep all df_oer rows
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            result = merged[overlap_mask | merged[snapshot_date_col].isna()]
        else:  # outer
            # Boolean indexing already creates new DataFrame, no need for .copy() (saves memory)
            result = merged[overlap_mask | 
                (merged[snapshot_date_col].isna() & merged[start_date_col].notna()) | 
                (merged[start_date_col].isna() & merged[snapshot_date_col].notna())]

    print(f"📊 After filtering for date overlap: {len(result):,} rows")
    
    # Remove the temporary tracking column
    if '_df_mpb_row_id' in result.columns:
        result = result.drop(columns=['_df_mpb_row_id'])
                             
    # Handle multiple matches per snapshot (only for overlap_all strategy)
    if strategy == 'overlap_all' and not keep_all_matches:
        # Keep only the first match per snapshot
        # Prioritize by evaluation date (most recent evaluation for that snapshot)
        result = result.sort_values(
            by=[snapshot_date_col, start_date_col], 
            ascending=[True, False]
        ).drop_duplicates(
            subset=[pid_col, snapshot_date_col],
            keep='first'
        )
        print(f"📊 After keeping only first match per snapshot: {len(result):,} rows")
        
    # Create senior rater pool metrics (for primary recent strategy)
    if strategy == 'primary_recent' and create_pool_metrics and snr_rater_col in result.columns and snr_rater_box_col in result.columns:
        print(f"\n🔧 Creating senior rater pool metrics...")

        # Group by senior rater and snapshot date, calculate mean of snr_rater_box
        # This captures the "talent pool" context - officers being rated together
        pool_metrics = result[
            result[snr_rater_col].notna() &
            result[snr_rater_box_col].notna()
        ].groupby([snr_rater_col, snapshot_date_col])[snr_rater_box_col].mean().reset_index()
        pool_metrics.columns = [snr_rater_col, snapshot_date_col, 'snr_rater_pool_snr_rater_box_mean']

        # Merge back to result
        result = result.merge(
            pool_metrics,
            on=[snr_rater_col, snapshot_date_col],
            how='left'
        )

        n_pools = pool_metrics[[snr_rater_col, snapshot_date_col]].drop_duplicates().shape[0]
        print(f"✅ Created pool metrics for {n_pools:,} unique senior rater snapshot combinations")
    
    # Report statistics
    n_snapshots_with_eval = result[result[start_date_col].notna()].shape[0]
    n_unique_snapshots_with_eval = result[result[start_date_col].notna()][
        [pid_col, snapshot_date_col]
    ].drop_duplicates().shape[0]
    n_unique_snapshots_total = result[[pid_col, snapshot_date_col]].drop_duplicates().shape[0]
    n_unique_snapshots_no_eval = n_unique_snapshots_total - n_unique_snapshots_with_eval
    
    print(f"\n📊 Join Summary:")
    print(f"  • Total original snapshots: {len(df_mpb):,}")
    print(f"  • Snapshots in result: {n_unique_snapshots_total:,}")
    if n_unique_snapshots_total == len(df_mpb):
        print(f"✅ All original snapshots preserved (true to left join)")
    else:
        print(f"⚠️ Row count mismatch: {len(df_mpb):,} original vs {n_unique_snapshots_total:,} result")
    print(f"  • Snapshots with at least one evaluation: {n_unique_snapshots_with_eval:,} ({n_unique_snapshots_with_eval/n_unique_snapshots_total*100:.1f}%)")
    print(f"  • Snapshots without evaluation: {n_unique_snapshots_no_eval:,} ({n_unique_snapshots_no_eval/n_unique_snapshots_total*100:.1f}%)")
    print(f"  • Total snapshot-evaluation pairs: {n_snapshots_with_eval:,}")
    
    # Additional stats for primary_recent strategy
    if strategy == 'primary_recent' and 'oer_source' in result.columns:
        oer_source_counts = result['oer_source'].value_counts()
        print(f"\n📊 OER Source Breakdown:")
        for source, count in oer_source_counts.items():
            pct = count / n_unique_snapshots_total * 100
            print(f"  • {source}: {count:,} snapshots ({pct:.1f}%)")
    
    if 'n_oers_overlapping' in result.columns:
        active_rows = result[result['oer_source'] == 'active']
        if len(active_rows) > 0:
            overlapping_stats = active_rows['n_oers_overlapping'].describe()
            print(f"\n📊 Multiple OER Overlaps (where active):")
            print(f"  • Mean overlapping OERs: {overlapping_stats['mean']:.2f}")
            print(f"  • Median overlapping OERs: {overlapping_stats['50%']:.0f}")
            print(f"  • Max overlapping OERs: {overlapping_stats['max']:.0f}")
        
            # Report high overlap cases
            if report_high_overlaps:
                high_overlap_rows = active_rows[active_rows['n_oers_overlapping'] >= high_overlap_threshold]
                if len(high_overlap_rows) > 0:
                    print(f"\n!! High Overlap Cases (n_oers_overlapping >= {high_overlap_threshold:,}):")
                    print(f"  • Count: {len(high_overlap_rows):,} snapshots {len(high_overlap_rows)/len(active_rows)*100:.2f}% of active)")
                    print(f"  • Overlap range: {high_overlap_rows['n_oers_overlapping'].min():.0f} to {high_overlap_rows['n_oers_overlapping'].max():.0f} ")

                    # Show distribution of high overlap values
                    high_overlap_dist = high_overlap_rows['n_oers_overlapping'].value_counts().sort_index()
                    print(f"  • Distribution:")
                    for n_overlaps, count in high_overlap_dist.head(10).items():
                        print(f"    {n_overlaps:.0f} overlaps: {count:,} snapshots")
                    if len(high_overlap_dist) > 10:
                        print(f"   ... ({len(high_overlap_dist) - 10} more values)")
                    
                    # Sample a few high overlap cases for inspection
                    if len(high_overlap_rows) > 0:
                        sample_cols = [pid_col, snapshot_date_col, 'n_oers_overlapping', start_date_col, thru_date_col]
                        available_cols = [col for col in sample_cols if col in high_overlap_rows.columns]
                        sample_cases = high_overlap_rows.nlargest(5, 'n_oers_overlapping')[available_cols]
                        print(f"\n  • Sample cases (top 5 by overlap count):")
                        
                        # Pre-index rows_with_overlap_for_diagnostics for faster lookups (if available)
                        if rows_with_overlap_for_diagnostics is not None and len(rows_with_overlap_for_diagnostics) > 0:
                            # Create a multi-index for faster filtering
                            rows_with_overlap_for_diagnostics['_lookup_key'] = (
                                rows_with_overlap_for_diagnostics[pid_col].astype(str) + '|' +
                                rows_with_overlap_for_diagnostics[snapshot_date_col].astype(str)
                            )

                        # Get the original rows_with_overlap to show details
                        for idx, row in sample_cases.iterrows():
                            officer_id = row[pid_col]
                            snapshot_dt = row[snapshot_date_col]
                            n_overlaps = int(row['n_oers_overlapping'])
                            
                            print(f"\n   Officer {officer_id}, Snapshot {snapshot_dt}: {n_overlaps:,} overlapping OERs")
                            if start_date_col in row and thru_date_col in row:
                                print(f"   Selected OER: {row[start_date_col]} to {row[thru_date_col]}")

                            # Show details of overlapping OERs for this case
                            if rows_with_overlap_for_diagnostics is not None and 'eval_id' in rows_with_overlap_for_diagnostics.columns:
                                # Use pre-computed lookup key for faster filtering
                                lookup_key = str(officer_id) + '|' + str(snapshot_dt)
                                overlapping_oers = rows_with_overlap_for_diagnostics[
                                    (rows_with_overlap_for_diagnostics['_lookup_key'] == lookup_key) &
                                    rows_with_overlap_for_diagnostics[start_date_col].notna() &
                                    rows_with_overlap_for_diagnostics[thru_date_col].notna() 
                                ]

                                # Deduplicate by eval_id to show unique OERs
                                if len(overlapping_oers) > 0:
                                    unique_oers = overlapping_oers.drop_duplicates(subset=['eval_id'], keep='first') if 'eval_id' in overlapping_oers.columns else overlapping_oers.drop_duplicates(subset=[start_date_col, thru_date_col], keep='first')
                                    n_unique = len(unique_oers)
                                    print(f"  Unique eval_ids overlapping: {n_unique:,}")

                                    if n_unique <= 10:  # Only show details if not too many
                                        print(f"  Overlapping OER date ranges:")
                                        # Fully vectorized formatting - prepare all strings at once
                                        if 'eval_id' in unique_oers.columns:
                                            eval_ids = unique_oers['eval_id'].fillna('no_eval_id').astype(str)
                                            eval_id_strs = 'eval_id=' + eval_ids
                                        else:
                                            eval_id_strs = pd.Series(['no_eval_id'] * len(unique_oers), index=unique_oers.index)
                                        
                                        start_vals = unique_oers[start_date_col].astype(str)
                                        thru_vals = unique_oers[thru_date_col].astype(str)
                                        
                                        # Vectorized string formatting - create all formatted lines at once
                                        formatted_lines = '          ' + eval_id_strs + ': ' + start_vals + ' to ' + thru_vals
                                        
                                        # Print all lines (still need to iterate for print, but formatting is vectorized)
                                        for line in formatted_lines:
                                            print(line)
                                    else:
                                        print(f"         (Too many to display - {n_unique:,} unique OERs)")

                                    # Check if OERs overlap with each other (data quality issue)
                                    if n_unique > 1:
                                        oer_dates = unique_oers[[start_date_col, thru_date_col]].sort_values(start_date_col)
                                        # Use vectorized comparison instead of loop
                                        oer_dates_sorted = oer_dates.sort_values(start_date_col).values
                                        if len(oer_dates_sorted) > 1:
                                            overlaps = oer_dates_sorted[:-1, 1] >= oer_dates_sorted[1:, 0]  # thru_date[i] >= start_date[i+1]
                                            overlapping_pairs = overlaps.sum()
                                            if overlapping_pairs > 0:
                                                print(f"        ⚠️ WARNING: {overlapping_pairs:,} pairs of OERs have overlapping date ranges (data quality issue!)")
                                            else:
                                                print(f"        ✓ OERs are sequential (no overlapping date ranges)")
                                        
                        # Clean up temporary lookup columns
                        if rows_with_overlap_for_diagnostics is not None and '_lookup_key' in rows_with_overlap_for_diagnostics.columns:
                            rows_with_overlap_for_diagnostics = rows_with_overlap_for_diagnostics.drop(columns=['_lookup_key'])
                                                               
    if strategy == 'overlap_all' and keep_all_matches and n_unique_snapshots_with_eval > 0:
        avg_matches = n_snapshots_with_eval / n_unique_snapshots_with_eval
        print(f"  • Average evaluations per snapshot (where matched): {avg_matches:.2f}")
    
    return result


# Example usage:
if __name__ == "__main__":
    # Example data
    dfbm_example = pd.DataFrame({
        'pid_pde': ['O1', 'O1', 'O2', 'O2', 'O3'],
        'snpsht_dt': pd.to_datetime(['2018-01-01', '2018-04-01', '2018-02-15', '2018-05-01', '2018-03-01']),
        'other_col': ['A', 'B', 'C', 'D', 'E']
    })
    
    df_oer_example = pd.DataFrame({
        'rated_ofcr': ['O1', 'O1', 'O2'],
        'eval_strt_dt': pd.to_datetime(['2017-10-01', '2018-03-01', '2018-01-01']),
        'eval_thru_dt': pd.to_datetime(['2018-03-31', '2018-06-30', '2018-04-30']),
        'rating': [5, 4, 5]
    })
    
    # Join with all matches
    result = join_oer_to_snapshots(df_mpb_in=dfbm_example, df_oer_in=df_oer_example, 
                                   strategy='overlap_all', keep_all_matches=True)
    print("\nResult with all matches:")
    print(result[['pid_pde', 'snpsht_dt', 'eval_strt_dt', 'eval_thru_dt', 'rating']])
    
    # Join with primary_recent strategy
    result_primary = join_oer_to_snapshots(df_mpb_in=dfbm_example, df_oer_in=df_oer_example, 
                                         strategy='primary_recent')
    print("\nResult with primary_recent strategy:")
    print(result_primary[['pid_pde', 'snpsht_dt', 'eval_strt_dt', 'eval_thru_dt', 'rating', 'oer_source', 'n_oers_overlapping']])
