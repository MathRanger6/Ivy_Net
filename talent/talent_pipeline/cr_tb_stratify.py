"""
TB-ratio stratification for Cell 11 competing-risks / CIF bar outputs.

When enabled (``CR_TB_STRATIFY_CONFIG`` in ``pipeline_config``), 520 repeats each
**competing_risks** spec for officers in **low / med / high** tertiles of **own** TB
ratio (from the **last** interval per ``pid_pde``). Pool binning, time scale, and
``plot_spec`` (except ``name``) match the main run; only the **officer set** changes.

Does **not** automatically run Kaplan–Meier specs (only ``plot_type == 'competing_risks'``).
"""

from __future__ import annotations

import os
import warnings
from typing import Any, Callable, Optional, Tuple

import pandas as pd


def add_cr_tb_stratum_column(
    df: pd.DataFrame,
    tb_col: str,
    pid_col: str = "pid_pde",
    time_col: str = "stop_time",
    n_strata: int = 3,
    labels: Tuple[str, ...] = ("low_tb", "med_tb", "high_tb"),
    new_col: str = "_cr_tb_stratum",
) -> pd.DataFrame:
    """
    Assign each officer to a tertile of **own** ``tb_col`` (value from last row by
    ``stop_time``), then map that label to **all** intervals for that officer.
    """
    if tb_col not in df.columns:
        raise KeyError(f"tb_stratify column {tb_col!r} not in dataframe")
    if len(labels) != n_strata:
        raise ValueError("len(labels) must equal n_strata")
    if pid_col not in df.columns or time_col not in df.columns:
        raise KeyError("df must contain pid_col and time_col")

    out = df.copy()
    o = out.sort_values([pid_col, time_col]).groupby(pid_col, observed=True).last(numeric_only=False)
    tb = pd.to_numeric(o[tb_col], errors="coerce")
    valid = tb.notna()
    n_miss = int((~valid).sum())
    if n_miss:
        warnings.warn(
            f"add_cr_tb_stratum_column: {n_miss} officers with NaN {tb_col} after last(); "
            "they will not appear in any stratum."
        )
    tb_ok = tb[valid]
    if len(tb_ok) < n_strata:
        raise ValueError(
            f"Not enough officers with non-NaN {tb_col} for {n_strata} strata: n={len(tb_ok)}"
        )
    try:
        strata = pd.qcut(tb_ok, q=n_strata, labels=list(labels), duplicates="drop")
    except Exception as e:
        warnings.warn(f"pd.qcut failed ({e!r}); falling back to rank-based qcut.")
        rk = tb_ok.rank(method="first")
        strata = pd.qcut(rk, q=n_strata, labels=list(labels), duplicates="drop")
    m = strata.to_dict()
    out[new_col] = out[pid_col].map(m)
    return out


def run_tb_stratified_cr_after_main(
    df_analysis: pd.DataFrame,
    PLOT_CONFIG: dict,
    CR_TB_STRATIFY_CONFIG: dict,
    print_v: Callable[[str], None],
    prepare_plot_data: Callable,
    get_plot_metadata: Callable,
    generate_plot_filename: Callable,
    save_plot_metadata_card: Callable,
    plot_competing_risks: Callable,
    plot_competing_risks_cif_bars: Callable,
    tick_sz: float,
    filtering_params: Optional[dict],
    os_module: Any = os,
) -> Tuple[int, int]:
    """
    After the main Cell 11 loop: repeat each **competing_risks** plot for each TB stratum.
    Returns (created, skipped) counts.
    """
    if not CR_TB_STRATIFY_CONFIG.get("enabled"):
        return (0, 0)

    tb_col = str(CR_TB_STRATIFY_CONFIG.get("tb_stratify_col", "z_tb_ratio_fwd_snr"))
    n_strata = int(CR_TB_STRATIFY_CONFIG.get("n_strata", 3))
    labels = tuple(CR_TB_STRATIFY_CONFIG.get("stratum_labels", ("low_tb", "med_tb", "high_tb")))
    scol = str(CR_TB_STRATIFY_CONFIG.get("stratum_col", "_cr_tb_stratum"))
    only_cr = bool(CR_TB_STRATIFY_CONFIG.get("only_competing_risks", True))
    if len(labels) != n_strata:
        print_v("⚠️ CR_TB_STRATIFY: stratum_labels length != n_strata; abort TB stratify.")
        return (0, 0)

    try:
        df_tagged = add_cr_tb_stratum_column(
            df_analysis, tb_col=tb_col, n_strata=n_strata, labels=labels, new_col=scol
        )
    except Exception as e:
        print_v(f"❌ TB stratify: add_cr_tb_stratum_column failed: {e}")
        return (0, 0)

    fp = filtering_params or {}
    jobs = []
    try:
        jobs = fp.get("filter_job_codes", {}).get("include_specific") or []
    except Exception:
        pass

    try:
        from IPython.display import Image, display
    except Exception:
        display = None
        Image = None

    created = 0
    skipped = 0
    for stratum in labels:
        for plot_spec in PLOT_CONFIG.get("plots", []):
            if only_cr and plot_spec.get("plot_type") != "competing_risks":
                continue
            if plot_spec.get("plot_type") != "competing_risks":
                continue
            ps = {**plot_spec, "name": f"{plot_spec['name']}_{stratum}"}
            df_in = df_tagged[df_tagged[scol] == stratum].copy()
            if len(df_in) == 0:
                print_v(f"  ⚠️ TB stratum {stratum}: no rows, skip {ps['name']}")
                skipped += 1
                continue
            print_v(
                f"\n  🔄 [TB stratum={stratum}] CR plot: {ps['name']}  (rows={len(df_in):,})"
            )
            plot_df = prepare_plot_data(df_in, ps)
            if plot_df is None or len(plot_df) == 0:
                print_v(f"  ❌ Skipped (no plot_df): {ps['name']}")
                skipped += 1
                continue
            metadata = get_plot_metadata(ps, df_in, plot_df)
            filename_base = generate_plot_filename(ps, metadata["data_stats"])
            save_path = os_module.path.join(PLOT_CONFIG["plot_dir"], filename_base)
            plot_competing_risks(plot_df, ps, save_path, metadata)
            created += 1
            if ps.get("plot_cif_bars", False) or PLOT_CONFIG.get("plot_cif_bars", False):
                _cif_figsize = (PLOT_CONFIG["figsize"][0], PLOT_CONFIG["figsize"][1])
                plot_competing_risks_cif_bars(
                    plot_df,
                    ps,
                    metadata,
                    output_dir=PLOT_CONFIG["plot_dir"],
                    filename_base=filename_base,
                    dpi=PLOT_CONFIG.get("dpi", 400),
                    figsize=_cif_figsize,
                    tick_sz=tick_sz,
                    legend_outside=PLOT_CONFIG.get("cif_bar_legend_outside", True),
                )
                n_bins = ps.get("n_bins", "")
                bmeth = ps.get("bin_method", "")
                print_v(
                    f"  ✅ [TB {stratum}] CIF bar plot: {filename_base.replace('.png', '')}_cif_bars.png, "
                    f"{n_bins} bins, {bmeth}, jobs: {jobs}"
                )
            try:
                metadata_path = save_plot_metadata_card(
                    metadata, PLOT_CONFIG["plot_dir"], filename_base.replace(".png", "")
                )
                print_v(f"  ✅ Saved metadata: {os_module.path.basename(metadata_path)}")
                if PLOT_CONFIG.get("show_metadata_cards", False) and display and Image:
                    display(Image(metadata_path))
            except Exception as e:
                print_v(f"  ⚠️ Could not save metadata: {e}")
    return (created, skipped)
