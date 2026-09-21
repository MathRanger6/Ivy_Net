"""
OER assignment and pool metrics (forward/backward only).

This module provides:
- assign_oer_to_snapshots_fast(): build individual fwd/bwd cumulative metrics and ratios
- add_pool_means_and_sizes(): compute pool means/minus-means/sizes for fwd+bwd
- add_pool_ranks_pct_zscores(): compute pool rank/pct/z for fwd+bwd
"""

import pandas as pd
import numpy as np


def _normalize_date_col(df, col):
    if col in df.columns:
        # If duplicate column names exist, df[col] returns a DataFrame.
        if isinstance(df[col], pd.DataFrame):
            df[col] = df[col].iloc[:, 0]
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.normalize()
    return df


def assign_oer_to_snapshots_fast(
    df_snaps,
    df_oers,
    pid_col='pid_pde',
    snapshot_date_col='snpsht_dt',
    rated_officer_col='rated_ofcr',
    eval_strt_col='eval_strt_dt',
    eval_thru_col='eval_thru_dt',
    rater_col='rater',
    snr_rater_col='snr_rater',
    rtr_box_col='rater_box',
    snr_box_col='snr_rater_box',
    clean_oer_cols=False,
    tb_value=70,
    use_tqdm=True,
    create_legacy_bwd_diag=True,
    debug_bwd=True,
):
    """
    Fast OER-to-snapshot assignment with forward/backward modes.

    Forward (carry-forward): most recent eval_thru_dt <= snapshot.
    Backward (painted): eval_strt_dt <= snapshot <= eval_thru_dt.

    Returns snapshot frame with:
    - *_fwd and *_bwd columns for rater/snr rater + boxes + dates
    - cumulative counts: cum_*_fwd_* and cum_*_bwd_*
    - ratios: tb_ratio_fwd_* and tb_ratio_bwd_*
    """
    pbar = None
    if use_tqdm:
        try:
            # Force standard (text) tqdm to avoid broken widget rendering
            from tqdm.auto import tqdm
            # If tqdm.auto causes widget issues, fall back to:
            # from tqdm import tqdm
            pbar = tqdm(
                total=5,
                desc="assign_oer_to_snapshots_fast",
                dynamic_ncols=True,
                leave=False,
            )
        except Exception:
            pbar = None

    snaps = pd.DataFrame(df_snaps).copy()
    oers = pd.DataFrame(df_oers).copy()
    if clean_oer_cols:
        from functionsG import load_json
        var_dir = './running_vars'
        oer_cols_keep = load_json('oer_cols_keep', var_dir)
        oers = oers[[col for col in oers.columns if col in oer_cols_keep]]
        print(f"\n   • Cleaned OER columns using {var_dir}/oer_cols_keep.json")
    if pbar:
        pbar.update(1)

    _normalize_date_col(snaps, snapshot_date_col)
    _normalize_date_col(oers, eval_strt_col)
    _normalize_date_col(oers, eval_thru_col)
    if pbar:
        pbar.update(1)

    if rated_officer_col != pid_col and rated_officer_col in oers.columns:
        oers = oers.rename(columns={rated_officer_col: pid_col})
    
    # merge_asof requires global sort on the "on" keys (date), and with "by" we keep a
    # stable secondary sort on pid — here [snapshot_date_col, pid_col].
    snaps_sorted = snaps.sort_values([snapshot_date_col, pid_col]).reset_index(drop=True)
    oers_thru_sorted = oers.sort_values([eval_thru_col, pid_col]).reset_index(drop=True)
    # Precompute cumulative counts on eval_thru_dt (completed evals)
    # Only count evals where a box check exists for that rater type.
    rtr_has_box = oers_thru_sorted[rtr_box_col].notna()
    snr_has_box = oers_thru_sorted[snr_box_col].notna()
    rtr_eval_inc = rtr_has_box.astype(int)
    snr_eval_inc = snr_has_box.astype(int)
    rtr_tb_inc = ((oers_thru_sorted[rtr_box_col] == tb_value) & rtr_has_box).astype(int)
    snr_tb_inc = ((oers_thru_sorted[snr_box_col] == tb_value) & snr_has_box).astype(int)

    oers_thru_sorted['cum_evals_thru_rtr'] = rtr_eval_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
    oers_thru_sorted['cum_evals_thru_snr'] = snr_eval_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
    oers_thru_sorted['cum_tb_rtr_thru'] = rtr_tb_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
    oers_thru_sorted['cum_tb_snr_thru'] = snr_tb_inc.groupby(oers_thru_sorted[pid_col]).cumsum()

    df_fwd = pd.merge_asof(
        snaps_sorted,
        oers_thru_sorted,
        left_on=snapshot_date_col,
        right_on=eval_thru_col,
        by=pid_col,
        direction='backward',
    )
    
    fwd_cols = {
        rater_col: 'rtr_rater_fwd',
        snr_rater_col: 'snr_rater_fwd',
        rtr_box_col: 'rtr_rater_box_fwd',
        snr_box_col: 'snr_rater_box_fwd',
        'eval_id': 'eval_id_fwd',
        eval_strt_col: 'eval_strt_dt_fwd',
        eval_thru_col: 'eval_thru_dt_fwd',
    }

    df_fwd = df_fwd.rename(columns=fwd_cols)
    if pbar:
        pbar.update(1)

    df_bwd = pd.merge_asof(
        snaps_sorted,
        oers_thru_sorted,
        left_on=snapshot_date_col,
        right_on=eval_thru_col,
        by=pid_col,
        direction='forward',
    )

    mask_outside = df_bwd[snapshot_date_col] < df_bwd[eval_strt_col]
    for col in [rater_col, snr_rater_col, rtr_box_col, snr_box_col, 'eval_id', eval_strt_col, eval_thru_col]:
        df_bwd.loc[mask_outside, col] = pd.NA

    bwd_cols = {
        rater_col: 'rtr_rater_bwd',
        snr_rater_col: 'snr_rater_bwd',
        rtr_box_col: 'rtr_rater_box_bwd',
        snr_box_col: 'snr_rater_box_bwd',
        'eval_id': 'eval_id_bwd',
        eval_strt_col: 'eval_strt_dt_bwd',
        eval_thru_col: 'eval_thru_dt_bwd',
    }
    df_bwd = df_bwd.rename(columns=bwd_cols)
    if pbar:
        pbar.update(1)

    merge_cols = [pid_col, snapshot_date_col] + list(bwd_cols.values())
    df_tb = df_fwd.merge(df_bwd[merge_cols], on=[pid_col, snapshot_date_col], how='left')
    
    # Guard against duplicate column names (can happen from upstream mapping/renames)
    if df_tb.columns.duplicated().any():
        dupes = df_tb.columns[df_tb.columns.duplicated()].tolist()
        print(f"[WARN] Dropping duplicate columns after merge: {dupes}")
        df_tb = df_tb.loc[:, ~df_tb.columns.duplicated()]
    
    for col in ['eval_strt_dt_fwd', 'eval_thru_dt_fwd', 'eval_strt_dt_bwd', 'eval_thru_dt_bwd']:
        _normalize_date_col(df_tb, col)
    
    # Ensure box columns are numeric for TB comparison
    for col in ['rtr_rater_box_fwd', 'snr_rater_box_fwd', 'rtr_rater_box_bwd', 'snr_rater_box_bwd']:
        if col in df_tb.columns:
            df_tb[col] = pd.to_numeric(df_tb[col], errors='coerce')

    bwd_fill_cols = [
        'rtr_rater_bwd', 'snr_rater_bwd', 'rtr_rater_box_bwd', 'snr_rater_box_bwd',
        'eval_id_bwd', 'eval_strt_dt_bwd', 'eval_thru_dt_bwd'
    ]
    df_tb[bwd_fill_cols] = (
        df_tb.groupby([pid_col, 'eval_thru_dt_bwd'])[bwd_fill_cols]
        .transform('first')
    )
    if pbar:
        pbar.update(1)

    if debug_bwd:
        total_rows = len(df_tb)
        bwd_missing_eval = df_tb['eval_id_bwd'].isna().sum()
        bwd_missing_thru = df_tb['eval_thru_dt_bwd'].isna().sum()
        bwd_missing_strt = df_tb['eval_strt_dt_bwd'].isna().sum()
        print("\n[DEBUG BWD] Basic coverage")
        print(f"   rows: {total_rows:,}")
        print(f"   eval_id_bwd missing: {bwd_missing_eval:,} ({bwd_missing_eval/total_rows:.1%})")
        print(f"   eval_thru_dt_bwd missing: {bwd_missing_thru:,} ({bwd_missing_thru/total_rows:.1%})")
        print(f"   eval_strt_dt_bwd missing: {bwd_missing_strt:,} ({bwd_missing_strt/total_rows:.1%})")

        # Within-rating-window check (should be mostly true for bwd rows)
        in_window = (
            df_tb['eval_strt_dt_bwd'].notna()
            & df_tb['eval_thru_dt_bwd'].notna()
            & (df_tb[snapshot_date_col] >= df_tb['eval_strt_dt_bwd'])
            & (df_tb[snapshot_date_col] <= df_tb['eval_thru_dt_bwd'])
            
        )
        in_window_rate = in_window.mean() if total_rows > 0 else 0
        print(f" In-window rate: {in_window_rate:.1%}")
    
    # Forward cumulative counts: completed evals (eval_thru_dt <= snapshot)
    df_tb['cum_evals_fwd_rtr'] = df_tb['cum_evals_thru_rtr'].fillna(0).astype(int)
    df_tb['cum_evals_fwd_snr'] = df_tb['cum_evals_thru_snr'].fillna(0).astype(int)
    df_tb['cum_tb_fwd_rtr'] = df_tb['cum_tb_rtr_thru'].fillna(0).astype(int)
    df_tb['cum_tb_fwd_snr'] = df_tb['cum_tb_snr_thru'].fillna(0).astype(int)
 
    df_tb['tb_ratio_fwd_rtr'] = np.where(
        df_tb['cum_evals_fwd_rtr'] > 0,
        (df_tb['cum_tb_fwd_rtr'] / df_tb['cum_evals_fwd_rtr']),
        np.nan,
    )
    df_tb['tb_ratio_fwd_snr'] = np.where(
        df_tb['cum_evals_fwd_snr'] > 0,
        (df_tb['cum_tb_fwd_snr'] / df_tb['cum_evals_fwd_snr']),
        np.nan,
    )

    # Safety: ensure cumulative thru_* columns exist before backward merge
    required_cum = [
        'cum_evals_thru_rtr', 'cum_evals_thru_snr',
        'cum_tb_rtr_thru', 'cum_tb_snr_thru',
    ]
    missing_cum = [c for c in required_cum if c not in oers_thru_sorted.columns]
    if missing_cum:
        # Recompute cumulatives defensively if missing (e.g., column pruning or upstream issues)
        rtr_has_box = oers_thru_sorted[rtr_box_col].notna() if rtr_box_col in oers_thru_sorted.columns else pd.Series(False, index=oers_thru_sorted.index)
        snr_has_box = oers_thru_sorted[snr_box_col].notna() if snr_box_col in oers_thru_sorted.columns else pd.Series(False, index=oers_thru_sorted.index)
        rtr_eval_inc = rtr_has_box.astype(int)
        snr_eval_inc = snr_has_box.astype(int)
        rtr_tb_inc = ((oers_thru_sorted[rtr_box_col] == tb_value) & rtr_has_box).astype(int) if rtr_box_col in oers_thru_sorted.columns else pd.Series(0, index=oers_thru_sorted.index)
        snr_tb_inc = ((oers_thru_sorted[snr_box_col] == tb_value) & snr_has_box).astype(int) if snr_box_col in oers_thru_sorted.columns else pd.Series(0, index=oers_thru_sorted.index)
        oers_thru_sorted['cum_evals_thru_rtr'] = rtr_eval_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
        oers_thru_sorted['cum_evals_thru_snr'] = snr_eval_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
        oers_thru_sorted['cum_tb_rtr_thru'] = rtr_tb_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
        oers_thru_sorted['cum_tb_snr_thru'] = snr_tb_inc.groupby(oers_thru_sorted[pid_col]).cumsum()
    
    # Backward cumulative counts: use the NEXT eval_thru_dt (paint backward across rating period)
    # Drop cum_*_thru from left to avoid merge suffixes (_x,_y)
    df_next = df_tb.drop(columns=required_cum, errors='ignore').merge(
        oers_thru_sorted[[pid_col, eval_thru_col, 'cum_evals_thru_rtr', 'cum_evals_thru_snr', 'cum_tb_rtr_thru', 'cum_tb_snr_thru']],
        left_on=[pid_col, 'eval_thru_dt_bwd'],
        right_on=[pid_col, eval_thru_col],
                how='left',
    )
    df_tb['cum_evals_bwd_rtr'] = df_next['cum_evals_thru_rtr'].fillna(0).astype(int)
    df_tb['cum_evals_bwd_snr'] = df_next['cum_evals_thru_snr'].fillna(0).astype(int)
    df_tb['cum_tb_bwd_rtr'] = df_next['cum_tb_rtr_thru'].fillna(0).astype(int)
    df_tb['cum_tb_bwd_snr'] = df_next['cum_tb_snr_thru'].fillna(0).astype(int)
    
    df_next = df_next.drop(
        columns=[
            'cum_evals_thru_rtr', 'cum_evals_thru_snr',
            'cum_tb_rtr_thru', 'cum_tb_snr_thru',
        ],
        errors='ignore',
    )
    
    df_tb['tb_ratio_bwd_rtr'] = np.where(
        
        df_tb['cum_evals_bwd_rtr'] > 0,
        (df_tb['cum_tb_bwd_rtr'] / df_tb['cum_evals_bwd_rtr']),
        np.nan,
    )
    df_tb['tb_ratio_bwd_snr'] = np.where(
        df_tb['cum_evals_bwd_snr'] > 0,
        (df_tb['cum_tb_bwd_snr'] / df_tb['cum_evals_bwd_snr']),
        np.nan,
    )

    # Optional diagnostic: legacy backward ratios (pre-fix behavior)
    if create_legacy_bwd_diag:
        print("Creating legacy backward diagnostics columns")
        if 'cum_evals_thru_rtr' in df_tb.columns and 'cum_tb_rtr_thru' in df_tb.columns:
            df_tb['tb_ratio_bwd_rtr_legacy'] = np.where(
                df_tb['cum_evals_thru_rtr'] > 0,
                (df_tb['cum_tb_rtr_thru'] / df_tb['cum_evals_thru_rtr']),
                np.nan,
            )
        
        if 'cum_evals_thru_snr' in df_tb.columns and 'cum_tb_snr_thru' in df_tb.columns:
            df_tb['tb_ratio_bwd_snr_legacy'] = np.where(
                df_tb['cum_evals_thru_snr'] > 0,
                (df_tb['cum_tb_snr_thru'] / df_tb['cum_evals_thru_snr']),
                np.nan,
            )       
    # Drop helper cumulative columns after both fwd/bwd ratios are computed
    df_tb = df_tb.drop(
        columns=[
            'cum_evals_thru_rtr', 'cum_evals_thru_snr',
            'cum_tb_rtr_thru', 'cum_tb_snr_thru',
        ],
        errors='ignore',
    )
    if pbar:
        pbar.close()

    return df_tb

def _peer_value_for_pool(series, exclude_peer_tb_zero):
    """Pool aggregation values; optionally drop peers with exact tb_ratio == 0."""
    vals = pd.to_numeric(series, errors='coerce')
    if exclude_peer_tb_zero:
        vals = vals.mask(vals == 0)
    return vals


def _add_pool_mean_size(
    df,
    group_cols,
    value_col,
    prefix,
    suffix,
    pool_min_size,
    exclude_self,
    exclude_peer_tb_zero=False,
):
    pool_val = _peer_value_for_pool(df[value_col], exclude_peer_tb_zero)
    work = df.copy()
    work['_pool_val'] = pool_val
    count = work.groupby(group_cols, observed=True)['_pool_val'].transform('count')
    sum_vals = work.groupby(group_cols, observed=True)['_pool_val'].transform('sum')
    is_self = pool_val.notna().astype(int)

    if exclude_self:
        denom = count - is_self
        numer = sum_vals - pool_val.fillna(0)
    else:
        denom = count
        numer = sum_vals

    mean = np.where(denom > 0, numer / denom, np.nan)
    mean = np.where(denom >= pool_min_size, mean, np.nan)
    size = np.where(denom >= pool_min_size, denom, np.nan)

    df[f'pool_size_{prefix}_{suffix}'] = size
    df[f'pool_tb_ratio_mean_{prefix}_{suffix}'] = mean
    df[f'pool_minus_mean_{prefix}_{suffix}'] = df[value_col] - mean
    return df


def resolve_pool_group_cols(
    pool_grouping_mode,
    snapshot_date_col,
    rater_col,
    eval_strt_col='eval_strt_dt_bwd',
    eval_thru_col='eval_thru_dt_bwd',
):
    """Return groupby columns for pool metrics, or None for active-at-anchor modes."""
    mode = (pool_grouping_mode or 'legacy').strip().lower()
    if mode == 'legacy':
        return [snapshot_date_col, rater_col]
    if mode == 'rating_window':
        return [snapshot_date_col, rater_col, eval_strt_col, eval_thru_col]
    if mode in ('active_at_eval_thru', 'active_at_snapshot'):
        return None
    raise ValueError(
        f"Unknown pool_grouping_mode={pool_grouping_mode!r}. "
        "Expected legacy, rating_window, active_at_eval_thru, or active_at_snapshot."
    )


def _add_pool_mean_size_active_at_anchor(
    df,
    pid_col,
    rater_col,
    anchor_col,
    eval_strt_col,
    eval_thru_col,
    value_col,
    prefix,
    suffix,
    pool_min_size,
    exclude_self,
    exclude_peer_tb_zero=False,
):
    """
    LOO pool stats where peers = officers under the same rater whose OER window
    covers anchor_col (e.g. eval_thru_dt_bwd = moment SNR writes the OER).
    """
    out = df.copy()
    n = len(out)
    mean_arr = np.full(n, np.nan, dtype=float)
    size_arr = np.full(n, np.nan, dtype=float)

    use_cols = []
    for col in (pid_col, rater_col, anchor_col, eval_strt_col, eval_thru_col, value_col):
        if col not in use_cols:
            use_cols.append(col)
    work = out[use_cols].copy()
    for col in dict.fromkeys((anchor_col, eval_strt_col, eval_thru_col)):
        work[col] = pd.to_datetime(work[col], errors='coerce')

    valid_self = (
        work[rater_col].notna()
        & work[anchor_col].notna()
        & work[value_col].notna()
    )
    peers = work.dropna(subset=[rater_col, eval_strt_col, eval_thru_col, value_col])
    if exclude_peer_tb_zero:
        peer_tb = pd.to_numeric(peers[value_col], errors='coerce')
        peers = peers.loc[peer_tb != 0].copy()
    peers = peers.drop_duplicates(
        subset=[pid_col, rater_col, eval_strt_col, eval_thru_col],
        keep='last',
    )
    work['_ix'] = np.arange(n)

    left = work.loc[valid_self, ['_ix', pid_col, rater_col, anchor_col, value_col]]
    if not left.empty and not peers.empty:
        peer_g = peers.rename(
            columns={
                pid_col: '_peer_pid',
                eval_strt_col: '_peer_strt',
                eval_thru_col: '_peer_thru',
                value_col: '_peer_val',
            }
        )
        cross = left.merge(peer_g, on=rater_col, how='inner')
        cross = cross[
            (cross[anchor_col] >= cross['_peer_strt'])
            & (cross[anchor_col] <= cross['_peer_thru'])
        ]
        if exclude_self:
            cross = cross[cross[pid_col] != cross['_peer_pid']]
        if not cross.empty:
            agg = cross.groupby('_ix', sort=False).agg(
                pool_sum=('_peer_val', 'sum'),
                pool_cnt=('_peer_val', 'count'),
            )
            ok = agg['pool_cnt'] >= pool_min_size
            ix_ok = agg.index[ok].to_numpy(dtype=int, copy=False)
            cnt_ok = agg.loc[ok, 'pool_cnt'].to_numpy(dtype=float)
            mean_arr[ix_ok] = agg.loc[ok, 'pool_sum'].to_numpy() / cnt_ok
            size_arr[ix_ok] = cnt_ok

    out[f'pool_size_{prefix}_{suffix}'] = size_arr
    out[f'pool_tb_ratio_mean_{prefix}_{suffix}'] = mean_arr
    out[f'pool_minus_mean_{prefix}_{suffix}'] = out[value_col] - mean_arr
    return out


def _add_pool_mean_size_for_rater(
    df,
    pool_grouping_mode,
    snapshot_date_col,
    pid_col,
    rater_col,
    eval_strt_col,
    eval_thru_col,
    pool_anchor_col,
    value_col,
    prefix,
    suffix,
    pool_min_size,
    exclude_self,
    exclude_peer_tb_zero=False,
):
    group_cols = resolve_pool_group_cols(
        pool_grouping_mode,
        snapshot_date_col,
        rater_col,
        eval_strt_col=eval_strt_col,
        eval_thru_col=eval_thru_col,
    )
    mode = (pool_grouping_mode or 'legacy').strip().lower()
    if group_cols is not None:
        return _add_pool_mean_size(
            df=df,
            group_cols=group_cols,
            value_col=value_col,
            prefix=prefix,
            suffix=suffix,
            pool_min_size=pool_min_size,
            exclude_self=exclude_self,
            exclude_peer_tb_zero=exclude_peer_tb_zero,
        )
    anchor_col = (
        snapshot_date_col if mode == 'active_at_snapshot' else pool_anchor_col
    )
    return _add_pool_mean_size_active_at_anchor(
        df=df,
        pid_col=pid_col,
        rater_col=rater_col,
        anchor_col=anchor_col,
        eval_strt_col=eval_strt_col,
        eval_thru_col=eval_thru_col,
        value_col=value_col,
        prefix=prefix,
        suffix=suffix,
        pool_min_size=pool_min_size,
        exclude_self=exclude_self,
        exclude_peer_tb_zero=exclude_peer_tb_zero,
    )


def add_pool_means_and_sizes(
    df_in,
    snapshot_date_col,
    rtr_col,
    snr_col,
    ratio_rtr_fwd_col,
    ratio_snr_fwd_col,
    ratio_rtr_bwd_col,
    ratio_snr_bwd_col,
    pool_min_size=3,
    exclude_self=True,
    pool_grouping_mode='legacy',
    pid_col='pid_pde',
    eval_strt_col='eval_strt_dt_bwd',
    eval_thru_col='eval_thru_dt_bwd',
    pool_anchor_col='eval_thru_dt_bwd',
    exclude_peer_tb_zero=None,
):
    if exclude_peer_tb_zero is None:
        try:
            from pipeline_config import POOL_EXCLUDE_PEER_TB_ZERO  # noqa: WPS433

            exclude_peer_tb_zero = bool(POOL_EXCLUDE_PEER_TB_ZERO)
        except Exception:
            exclude_peer_tb_zero = False
    mode = (pool_grouping_mode or 'legacy').strip().lower()
    print(f"   • add_pool_means_and_sizes: POOL_GROUPING_MODE={mode}")
    if exclude_peer_tb_zero:
        print("   • add_pool_means_and_sizes: POOL_EXCLUDE_PEER_TB_ZERO=True (peers with tb_ratio==0 dropped from pools)")
    df = df_in.copy()
    pool_kw = dict(
        pool_grouping_mode=mode,
        snapshot_date_col=snapshot_date_col,
        pid_col=pid_col,
        eval_strt_col=eval_strt_col,
        eval_thru_col=eval_thru_col,
        pool_anchor_col=pool_anchor_col,
        pool_min_size=pool_min_size,
        exclude_self=exclude_self,
        exclude_peer_tb_zero=exclude_peer_tb_zero,
    )
    df = _add_pool_mean_size_for_rater(
        df=df,
        rater_col=rtr_col,
        value_col=ratio_rtr_fwd_col,
        prefix='rtr',
        suffix='fwd',
        **pool_kw,
    )
    df = _add_pool_mean_size_for_rater(
        df=df,
        rater_col=snr_col,
        value_col=ratio_snr_fwd_col,
        prefix='snr',
        suffix='fwd',
        **pool_kw,
    )
    df = _add_pool_mean_size_for_rater(
        df=df,
        rater_col=rtr_col,
        value_col=ratio_rtr_bwd_col,
        prefix='rtr',
        suffix='bwd',
        **pool_kw,
    )
    df = _add_pool_mean_size_for_rater(
        df=df,
        rater_col=snr_col,
        value_col=ratio_snr_bwd_col,
        prefix='snr',
        suffix='bwd',
        **pool_kw,
    )
    return df


def _add_pool_ranks(df, group_cols, value_col, prefix, suffix, pool_min_size, rank_method, rank_ascending, z_eps):
    rank = df.groupby(group_cols)[value_col].rank(ascending=rank_ascending, method=rank_method)
    rank_pct = df.groupby(group_cols)[value_col].rank(ascending=rank_ascending, method=rank_method, pct=True)
    std = df.groupby(group_cols)[value_col].transform('std')
    mean_col = f'pool_tb_ratio_mean_{prefix}_{suffix}'
    mean = df[mean_col] if mean_col in df.columns else df.groupby(group_cols)[value_col].transform('mean')

    size_col = f'pool_size_{prefix}_{suffix}'
    size = df[size_col] if size_col in df.columns else df.groupby(group_cols)[value_col].transform('count')
    valid = (size >= pool_min_size) & std.notna() & (std > z_eps)

    df[f'pool_tb_ratio_rank_{prefix}_{suffix}'] = np.where(valid, rank, np.nan)
    df[f'pool_tb_ratio_rank_pct_{prefix}_{suffix}'] = np.where(valid, rank_pct, np.nan)
    df[f'pool_tb_ratio_zpool_{prefix}_{suffix}'] = np.where(valid, (df[value_col] - mean) / std, np.nan)
    return df


def add_pool_ranks_pct_zscores(
    df_in,
    snapshot_date_col,
    rtr_col,
    snr_col,
    ratio_rtr_fwd_col,
    ratio_snr_fwd_col,
    ratio_rtr_bwd_col,
    ratio_snr_bwd_col,
    pool_min_size=3,
    rank_method='average',
    rank_ascending=False,
    z_eps=1e-9,
    pool_grouping_mode='legacy',
    eval_strt_col='eval_strt_dt_bwd',
    eval_thru_col='eval_thru_dt_bwd',
):
    mode = (pool_grouping_mode or 'legacy').strip().lower()
    if mode in ('active_at_eval_thru', 'active_at_snapshot'):
        raise NotImplementedError(
            f"add_pool_ranks_pct_zscores does not support POOL_GROUPING_MODE={mode!r}. "
            "Set CELL6_POOL_RANKS=False or use legacy/rating_window."
        )
    rtr_group = resolve_pool_group_cols(
        mode, snapshot_date_col, rtr_col, eval_strt_col, eval_thru_col
    )
    snr_group = resolve_pool_group_cols(
        mode, snapshot_date_col, snr_col, eval_strt_col, eval_thru_col
    )
    df = df_in.copy()
    df = _add_pool_ranks(
        df=df,
        group_cols=rtr_group,
        value_col=ratio_rtr_fwd_col,
        prefix='rtr',
        suffix='fwd',
        pool_min_size=pool_min_size,
        rank_method=rank_method,
        rank_ascending=rank_ascending,
        z_eps=z_eps,
    )
    df = _add_pool_ranks(
        df=df,
        group_cols=snr_group,
        value_col=ratio_snr_fwd_col,
        prefix='snr',
        suffix='fwd',
        pool_min_size=pool_min_size,
        rank_method=rank_method,
        rank_ascending=rank_ascending,
        z_eps=z_eps,
    )
    df = _add_pool_ranks(
        df=df,
        group_cols=rtr_group,
        value_col=ratio_rtr_bwd_col,
        prefix='rtr',
        suffix='bwd',
        pool_min_size=pool_min_size,
        rank_method=rank_method,
        rank_ascending=rank_ascending,
        z_eps=z_eps,
    )
    df = _add_pool_ranks(
        df=df,
        group_cols=snr_group,
        value_col=ratio_snr_bwd_col,
        prefix='snr',
        suffix='bwd',
        pool_min_size=pool_min_size,
        rank_method=rank_method,
        rank_ascending=rank_ascending,
        z_eps=z_eps,
    )
    return df
