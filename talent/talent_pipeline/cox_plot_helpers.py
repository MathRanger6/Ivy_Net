"""
Helper functions for enhanced Cox regression plot generation.

This module provides utilities for:
- Generating descriptive plot filenames
- Creating plot metadata
- Formatting configuration text for display
- Adding configuration boxes to plots
- Enhancing legend labels with statistics
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Callable, Optional

import matplotlib.pyplot as plt
try:
    import seaborn as sns
    _SEABORN_AVAILABLE = True
except Exception:
    _SEABORN_AVAILABLE = False


def apply_unknown_group_by_filter(
    working_df: pd.DataFrame,
    plot_spec: dict,
    plot_config: dict,
    log: Optional[Callable[[str], None]] = None,
) -> pd.DataFrame:
    """
    If ``exclude_unknown_div_name`` is True (``plot_spec`` overrides ``plot_config`` when key is
    present), drop rows where ``plot_spec['group_by']`` is NaN or a placeholder label.

    The usual ``div_name`` placeholder from the merge is title-case **Unknown**. We normalize with
    ``strip`` + ``casefold`` and compare to ``"unknown"``, so **Unknown**, **UNKNOWN**, etc. are
    all treated the same.

    Also drops string placeholders ``nan`` / ``none`` and blank strings.

    Used by Cell 11 ``prepare_plot_data`` for competing-risks / KM grouping (e.g. ``div_name``).
    """
    _log = log or (lambda _m: None)
    excl = plot_spec.get("exclude_unknown_div_name")
    if excl is None:
        excl = plot_config.get("exclude_unknown_div_name", False)
    gb = plot_spec.get("group_by")
    if not excl or gb is None or gb not in working_df.columns:
        return working_df
    col = working_df[gb]
    strv = col.astype("string")
    # Merge placeholder is typically "Unknown"; casefold so any casing matches
    sl = strv.str.strip().str.casefold()
    is_bad = strv.isna() | sl.eq("unknown") | sl.eq("nan") | sl.eq("none") | (sl == "")
    before = len(working_df)
    out = working_df[~is_bad].copy()
    removed = before - len(out)
    if removed > 0:
        _log(
            f"  • Dropped {removed:,} officers with missing/Unknown/placeholder {gb!r} "
            f"(exclude_unknown_div_name=True)"
        )
        _log(f"  • Remaining officers: {len(out):,}")
    return out


def cr_discrete_group_colors(n_groups: int, mode: str = "husl") -> list:
    """
    Hex colors for competing-risks curves and matching CIF bar panels.

    ``mode``:
      - ``husl`` (default): evenly spaced hues; best when you have many groups and want
        colors that do not overlap visually.
      - ``tab20``: first use ``tab20``, then ``tab20b`` (up to 40 distinct base colors),
        then ``husl`` for any overflow.
      - ``set1``: legacy Set1 + Set2 + Set3 listed colors (up to ~29), then ``husl`` for overflow.
        Older code used modulo indexing, which repeated colors when *n* exceeded the palette.
      - ``glasbey``: categorical ``glasbey`` colormap when available (matplotlib ≥ 3.7); else ``husl``.

    Returns a list of length ``n_groups`` (may be shorter if ``n_groups`` is 0).
    """
    import matplotlib.colors as mcolors

    if n_groups <= 0:
        return []
    mode = (mode or "husl").strip().lower()

    def _husl(n: int) -> list:
        if _SEABORN_AVAILABLE:
            pal = sns.color_palette("husl", n_colors=n)
            return [mcolors.to_hex(tuple(c[:3])) for c in pal]
        return [
            mcolors.to_hex(mcolors.hsv_to_rgb((i / max(n, 1), 0.85, 0.9)))
            for i in range(n)
        ]

    if mode == "husl":
        return _husl(n_groups)

    if mode == "tab20":
        t20 = [mcolors.to_hex(c) for c in list(plt.cm.tab20.colors) + list(plt.cm.tab20b.colors)]
        if n_groups <= len(t20):
            return t20[:n_groups]
        return t20 + _husl(n_groups - len(t20))

    if mode == "set1":
        base = list(plt.cm.Set1.colors) + list(plt.cm.Set2.colors) + list(plt.cm.Set3.colors)
        hexes = [mcolors.to_hex(c) for c in base]
        if n_groups <= len(hexes):
            return hexes[:n_groups]
        return hexes + _husl(n_groups - len(hexes))

    if mode == "glasbey":
        try:
            gb = plt.colormaps["glasbey"]
            if hasattr(gb, "colors") and gb.colors is not None and len(gb.colors) >= n_groups:
                return [mcolors.to_hex(c) for c in gb.colors[:n_groups]]
            return [mcolors.to_hex(gb(i / max(n_groups - 1, 1))) for i in range(n_groups)]
        except Exception:
            pass
        return _husl(n_groups)

    # Unknown mode: behave like gradient / default plotting — use husl
    return _husl(n_groups)


def generate_plot_filename(plot_spec, df_stats=None):
    """
    Generate descriptive filename from plot specification.
    
    Creates filenames that include key configuration details for easy identification:
    Format: {plot_type}_{variable}_{group_by}_{bins}_{bin_method}_{filter}_{date_range}.png
    
    Args:
        plot_spec: Plot specification dictionary
        df_stats: Optional dictionary with data statistics (N officers, date range, etc.)
    
    Returns:
        str: Descriptive filename
    """
    # Extract plot type: 'km' for Kaplan-Meier, 'cr' for Competing Risks
    plot_type = 'km' if plot_spec['plot_type'] == 'kaplan_meier' else 'cr'
    
    # Get variable and group_by names (default to 'none' if not specified or None)
    variable = plot_spec.get('variable', 'none')
    group_by = plot_spec.get('group_by', 'none')
    if group_by is None:
        group_by = 'none'
    
    # Shorten variable names to keep filenames manageable
    # Remove common prefixes/suffixes and limit to 20 characters
    var_short = variable.replace('cum_', '').replace('_recvd', '').replace('_ratio', '_r')
    var_short = var_short.replace('_snr', '').replace('_rtr', '').replace('prestige_', 'prest_')
    var_short = var_short[:20]  # Limit length to prevent overly long filenames
    
    # Shorten group_by names similarly (remove underscores, limit to 10 chars)
    if group_by != 'none':
        group_short = group_by.replace('_', '')[:10]
    else:
        group_short = 'none'
    
    # Determine binning information for filename
    if plot_spec.get('bin_continuous', False):
        # Continuous variable was binned: include number of bins and method
        bins = f"b{plot_spec.get('n_bins', 3)}"  # e.g., "b3" for 3 bins
        bin_method = 'q' if plot_spec.get('bin_method') == 'quantile' else 'ew'  # 'q' = quantile, 'ew' = equal_width
    else:
        # Categorical variable (no binning needed)
        bins = 'cat'
        bin_method = 'na'  # Not applicable
    
    # Filter information: indicate if zero-OER officers were excluded
    filter_str = 'noOER' if plot_spec.get('filter_zero_oer', False) else 'all'
    
    # Extract date range from statistics if available
    # Format: "_2000-2022" (start year - end year)
    date_str = ''
    if df_stats and 'date_range' in df_stats and df_stats['date_range']:
        start_date = df_stats['date_range'].get('start', '')
        end_date = df_stats['date_range'].get('end', '')
        if start_date and end_date:
            # Extract first 4 characters (year) from date string
            try:
                start_year = str(start_date)[:4] if len(str(start_date)) >= 4 else ''
                end_year = str(end_date)[:4] if len(str(end_date)) >= 4 else ''
                if start_year and end_year:
                    date_str = f"_{start_year}-{end_year}"
            except:
                pass  # Skip date if extraction fails
    
    # Build the complete filename with all components
    filename = f"{plot_type}_{var_short}_{group_short}_{bins}_{bin_method}_{filter_str}{date_str}.png"
    
    # Clean up filename: remove special characters that might cause filesystem issues
    filename = filename.replace('/', '_').replace(' ', '_').replace('|', '_')
    filename = filename.replace('(', '').replace(')', '').replace('[', '').replace(']', '')
    
    # Ensure filename doesn't exceed reasonable length (100 characters)
    # If too long, truncate variable name more aggressively
    if len(filename) > 100:
        var_short = var_short[:10]  # Further truncate variable name
        filename = f"{plot_type}_{var_short}_{group_short}_{bins}_{bin_method}_{filter_str}{date_str}.png"
        # Final safety check: if still too long, hard limit to 100 chars
        # Remove .png extension before truncation to avoid .png.png
        if len(filename) > 100:
            if filename.endswith('.png'):
                filename = filename[:-4]  # Remove .png extension
            filename = filename[:100] + '.png'  # Truncate to 100 chars and re-add .png
    
    return filename


def get_plot_metadata(plot_spec, df, plot_df, filtering_params=None):
    """
    Generate metadata dictionary for a plot.
    
    Creates a comprehensive metadata dictionary that captures all configuration
    and data statistics for a plot. This metadata is saved as JSON alongside the plot
    for documentation and reproducibility.
    
    Args:
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
        df: Original dataframe (for date range, total intervals, etc.)
        plot_df: Prepared plot dataframe (officer-level, after filtering/binning)
        filtering_params: Optional filtering settings (from pipeline_config filtering_params)
    
    Returns:
        dict: Metadata including configuration, data stats, group sizes, etc.
    """
    # Extract date range from original dataframe if snapshot date column exists
    # This helps identify the time period covered by the analysis
    date_range = None
    if 'snpsht_dt' in df.columns:
        try:
            date_range = {
                'start': str(df['snpsht_dt'].min()),  # Earliest snapshot date
                'end': str(df['snpsht_dt'].max())     # Latest snapshot date
            }
        except:
            pass  # Skip if date extraction fails
    
    # Count number of officers in each plot group
    # Useful for understanding sample sizes per group
    group_sizes = {}
    if 'plot_group' in plot_df.columns:
        group_sizes = plot_df['plot_group'].value_counts().to_dict()
    
    # Calculate statistics for each group if variable was binned
    # Provides mean, min, max, median for each bin (helps interpret bin ranges)
    group_stats = {}
    if plot_spec.get('variable') and plot_spec.get('bin_continuous', False):
        var_name = plot_spec['variable']
        if var_name in plot_df.columns:
            # For each group, calculate descriptive statistics of the binned variable
            for group in plot_df['plot_group'].unique():
                group_data = plot_df[plot_df['plot_group'] == group][var_name]
                if len(group_data) > 0:
                    group_stats[group] = {
                        'mean': float(group_data.mean()),      # Average value in this bin
                        'min': float(group_data.min()),        # Minimum value in this bin
                        'max': float(group_data.max()),        # Maximum value in this bin
                        'median': float(group_data.median())   # Median value in this bin
                    }
    
    # Default filtering params from pipeline_config if not explicitly provided
    if filtering_params is None:
        try:
            from pipeline_config import filtering_params as _filtering_params
            filtering_params = _filtering_params
        except Exception:
            filtering_params = None

    # Load column/division config for traceability (optional)
    column_config = None
    division_config = None
    try:
        from pipeline_config import COLUMN_CONFIG as _column_config, DIVISION_CONFIG as _division_config
        column_config = _column_config
        division_config = _division_config
    except Exception:
        pass

    model_static_cols = None
    model_time_varying_cols = None
    dummy_cfg = None
    if column_config:
        model_static_cols = column_config.get("model_static_cols") or column_config.get("static_cols")
        model_time_varying_cols = column_config.get("model_time_varying_cols") or column_config.get("time_varying_cols")
        dummy_cfg = column_config.get("dummy_variables", {})

    div_cfg = None
    if division_config:
        div_cfg = {
            "enabled": division_config.get("enabled", False),
            "create_div_cum_time": division_config.get("create_div_cum_time", False),
            "create_div_ratio_time": division_config.get("create_div_ratio_time", False),
            "create_final_div_cpt": division_config.get("create_final_div_cpt", False),
            "division_list": division_config.get("division_list", []),
        }

    # Assemble complete metadata dictionary
    metadata = {
        # Basic plot identification
        'plot_name': plot_spec['name'],              # Original plot name from config
        'plot_type': plot_spec['plot_type'],         # 'kaplan_meier' or 'competing_risks'
        'variable': plot_spec.get('variable'),       # Variable being analyzed (or None)
        'group_by': plot_spec.get('group_by'),       # Grouping variable (or None)
        
        # Configuration settings (how the plot was created)
        'configuration': {
            'bin_continuous': plot_spec.get('bin_continuous', False),  # Was variable binned?
            'n_bins': plot_spec.get('n_bins'),                          # Number of bins (if binned)
            'bin_method': plot_spec.get('bin_method'),                  # 'quantile' or 'equal_width'
            'min_group_size': plot_spec.get('min_group_size'),          # Minimum officers per group
            'use_time_varying': plot_spec.get('use_time_varying', True), # Use time-varying values?
            'filter_zero_oer': plot_spec.get('filter_zero_oer', False),  # Exclude zero-OER officers?
            'filter_nan_variable': plot_spec.get('filter_nan_variable', False),  # Drop NaNs for plotted variable?
            'filtering_params': filtering_params,  # CELL 9 filtering settings (if provided)
            'model_static_cols': model_static_cols,
            'model_time_varying_cols': model_time_varying_cols,
            'dummy_create': dummy_cfg.get('create_dummies') if dummy_cfg is not None else None,
            'dummy_exclude_reference': dummy_cfg.get('exclude_reference') if dummy_cfg is not None else None,
            'division_config': div_cfg,
        },
        
        # Data statistics (sample sizes, date ranges)
        'data_stats': {
            'total_officers': int(plot_df['pid_pde'].nunique()) if 'pid_pde' in plot_df.columns else None,  # Number of unique officers
            'total_intervals': len(df) if 'pid_pde' in df.columns else None,  # Total intervals in original data
            'n_groups': int(plot_df['plot_group'].nunique()) if 'plot_group' in plot_df.columns else None,  # Number of groups in plot
            'date_range': date_range,  # Start and end dates (if available)
        },
        
        # Group-level information
        'group_sizes': group_sizes,      # Number of officers per group
        'group_stats': group_stats if group_stats else None,  # Statistics per group (if binned)
    }
    return metadata


def format_plot_config_text(plot_spec, metadata):
    """
    Format configuration information as text for plot subtitle or text box.
    
    Creates a multi-line text string that summarizes key plot configuration details.
    Used in the configuration box displayed on plots and in subtitles.
    
    Args:
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
        metadata: Metadata dictionary from get_plot_metadata()
    
    Returns:
        str: Formatted configuration text (newline-separated lines)
    """
    lines = []
    
    # Add variable and grouping information
    if plot_spec.get('variable'):
        lines.append(f"Variable: {plot_spec['variable']}")  # Variable being analyzed
    if plot_spec.get('group_by'):
        lines.append(f"Group by: {plot_spec['group_by']}")  # Grouping variable
    
    # Add binning information
    if plot_spec.get('bin_continuous', False):
        # Variable was binned: show number of bins and method
        bin_method = plot_spec.get('bin_method', 'quantile')
        bin_method_display = 'quantile' if bin_method == 'quantile' else 'equal width'
        lines.append(f"Bins: {plot_spec.get('n_bins', 3)} ({bin_method_display})")
    else:
        # Categorical variable (no binning)
        lines.append("Bins: Categorical")
    
    # Add filtering information
    if plot_spec.get('filter_zero_oer', False):
        lines.append("Filter: Exclude zero-OER officers")  # Officers with no OER data excluded
    else:
        lines.append("Filter: All officers")  # No filtering applied
    
    # Add data statistics (sample sizes)
    if metadata.get('data_stats'):
        stats = metadata['data_stats']
        if stats.get('total_officers'):
            lines.append(f"N officers: {stats['total_officers']:,}")  # Total number of officers
        if stats.get('n_groups'):
            lines.append(f"Groups: {stats['n_groups']}")  # Number of groups in plot

    if plot_spec.get("cr_tb_stratify_title_suffix"):
        lines.append(f"CR add-on: {plot_spec['cr_tb_stratify_title_suffix']}")
    
    # Join all lines with newlines for multi-line display
    return "\n".join(lines)


def format_plot_title(plot_spec):
    """
    Generate descriptive plot title from plot specification.
    
    Creates a human-readable title that describes what the plot shows,
    replacing technical variable names with more readable versions.
    
    Args:
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
    
    Returns:
        str: Descriptive title (e.g., "Kaplan-Meier: Cumulative TB Ratio (SNR) by Year Group")
    """
    # Determine plot type display name
    plot_type_display = "Kaplan-Meier" if plot_spec['plot_type'] == 'kaplan_meier' else "Competing Risks"
    
    # Convert variable name to readable format
    variable = plot_spec.get('variable', '')
    if variable:
        # Replace underscores with spaces, handle common abbreviations
        var_display = variable.replace('_', ' ').replace('cum ', 'Cumulative ').title()
        # Fix common abbreviations to proper case
        var_display = var_display.replace('Tb', 'TB').replace('Snr', 'SNR').replace('Rtr', 'RTR')
        var_display = var_display.replace('Oer', 'OER').replace('Evals', 'Evaluations')
    else:
        # No variable specified (plotting all officers)
        var_display = "All Officers"
    
    # Convert group_by name to readable format
    group_by = plot_spec.get('group_by', '')
    if group_by:
        group_display = group_by.replace('_', ' ').title()  # Replace underscores, title case
        group_display = group_display.replace('Yg', 'Year Group')  # Expand common abbreviations
    else:
        group_display = ""
    
    # Combine into final title
    if group_display:
        # Title with grouping: "Kaplan-Meier: Variable by Group"
        title = f"{plot_type_display}: {var_display}\nby {group_display}"
    else:
        # Title without grouping: "Kaplan-Meier: Variable"
        title = f"{plot_type_display}: {var_display}"

    # Cell 11 TB-stratify add-on: second line (own-TB stratum + quantile vs equal width)
    _tb_note = plot_spec.get("cr_tb_stratify_title_suffix")
    if _tb_note:
        title = f"{title}\n{_tb_note}"

    return title


def format_plot_subtitle(plot_spec, metadata):
    """
    Generate subtitle text with configuration details.
    
    Creates a concise subtitle that appears below the main title,
    summarizing key configuration parameters in a comma-separated format.
    
    Args:
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
        metadata: Metadata dictionary from get_plot_metadata()
    
    Returns:
        str: Formatted subtitle text (e.g., "3 bins (quantile), min_group=50, N=15,234 officers, filtered: all")
    """
    parts = []
    
    # Add binning information
    if plot_spec.get('bin_continuous', False):
        # Variable was binned: show number of bins and method
        bin_method = plot_spec.get('bin_method', 'quantile')
        bin_method_short = 'quantile' if bin_method == 'quantile' else 'equal_width'
        parts.append(f"{plot_spec.get('n_bins', 3)} bins ({bin_method_short})")
    else:
        # Categorical variable (no binning)
        parts.append("Categorical")
    
    # Add minimum group size requirement
    parts.append(f"min_group={plot_spec.get('min_group_size', 50)}")
    
    # Add sample size (number of officers)
    if metadata.get('data_stats') and metadata['data_stats'].get('total_officers'):
        parts.append(f"N={metadata['data_stats']['total_officers']:,} officers")
    
    # Add filter status
    if plot_spec.get('filter_zero_oer', False):
        parts.append("filtered: exclude zero-OER")  # Zero-OER officers excluded
    else:
        parts.append("filtered: all")  # All officers included
    
    # Join all parts with commas for compact display
    return ", ".join(parts)


def format_legend_label(plot_spec, group, plot_df, var_name=None):
    """
    Format legend label with statistics for a group.
    
    Enhances legend labels by adding statistical information:
    - For binned variables: average, range, and sample size
    - For competing risks: final cumulative incidence function (CIF)
    - Always includes sample size (N)
    
    Args:
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
        group: Group name/label (e.g., "High TB Ratio" or "Year Group 2000")
        plot_df: Plot dataframe (officer-level, after filtering/binning)
        var_name: Variable name (if binned, used to calculate group statistics)
    
    Returns:
        str: Enhanced legend label (e.g., "High TB Ratio (avg: 45.2%, range: 30.0-60.0, N=5,089)")
    """
    # Optional mapping for categorical labels (keep local to avoid notebook edits)
    legend_map = {
        'sex': {0: 'Female', 1: 'Male', '0': 'Female', '1': 'Male'},
        'married': {0: 'Unmarried', 1: 'Married', '0': 'Unmarried', '1': 'Married'},
        'prestige': {0: 'Without', 1: 'With', '0': 'Without', '1': 'With'},
    }

    def map_category_label(var_name, value):
        if not var_name:
            return str(value)
        mapping = legend_map.get(var_name)
        if not mapping:
            return str(value)
        if value in mapping:
            return mapping[value]
        # Try string key first
        if str(value) in mapping:
            return mapping[str(value)]
        # Try numeric normalization (e.g., "1.0" -> 1)
        try:
            num_val = float(value)
            if num_val.is_integer():
                int_val = int(num_val)
                if int_val in mapping:
                    return mapping[int_val]
                if str(int_val) in mapping:
                    return mapping[str(int_val)]
        except Exception:
            pass
        return str(value)

    # Get data for this specific group
    group_data = plot_df[plot_df['plot_group'] == group]
    n_officers = len(group_data)
    
    # Start with base group name, mapped for common categorical labels
    label = str(group)
    group_by = plot_spec.get('group_by')
    variable = plot_spec.get('variable')
    if isinstance(group, str) and " | " in group:
        first_part, second_part = group.split(" | ", 1)
        group_by_label = map_category_label(group_by, first_part)
        variable_label = map_category_label(variable, second_part)
        # Display variable first, then group_by (variable | group_by)
        label = f"{variable_label} | {group_by_label}"
    else:
        # Single grouping (either group_by or variable)
        if group_by:
            label = map_category_label(group_by, group)
        elif variable:
            label = map_category_label(variable, group)
    
    # Add statistics if variable was binned (shows actual value ranges for each bin)
    if var_name and var_name in plot_df.columns and plot_spec.get('bin_continuous', False):
        # Extract variable values for this group
        group_var_data = group_data[var_name].dropna()
        # if len(group_var_data) > 0:
        #     # Calculate descriptive statistics for this bin
        #     avg_val = group_var_data.mean()   # Average value in this bin
        #     min_val = group_var_data.min()    # Minimum value in this bin
        #     max_val = group_var_data.max()    # Maximum value in this bin
        #     # Add statistics to label (raw if 0-1 scale, else percent-style)
        #     if min_val >= 0 and max_val <= 1.5:
        #         label += f" (avg: {avg_val:.3f}, range: {min_val:.3f}-{max_val:.3f}, N={n_officers:,})"
        #     else:
        #         label += f" (avg: {avg_val:.1f}%, range: {min_val:.1f}-{max_val:.1f}, N={n_officers:,})"
        # else:
        #     # No data available, just show sample size
        #     label += f" (N={n_officers:,})"
        label += f" N={n_officers:,}"
    else:
        # Not binned or no variable: just show sample size
        label += f" N={n_officers:,}"
    
    # Optional legacy suffix for slides/diagnostics (disabled by default for paper output).
    if plot_spec.get('legend_show_final_cif', False):
        if plot_spec.get('plot_type') == 'competing_risks':
            if 'event' in plot_df.columns and 'event' in group_data.columns:
                n_promoted = (group_data['event'] == 1).sum()
                if n_officers > 0:
                    promo_rate = n_promoted / n_officers
                    label += f", final CIF: {promo_rate:.2f}"
    
    return label


def add_configuration_box(ax, plot_spec, metadata, font_size=8):
    """
    Add configuration text box to plot axis.
    
    Creates a text box in the bottom-right corner of the plot showing
    key configuration details. Uses semi-transparent background so it
    doesn't completely obscure the plot data.
    
    Args:
        ax: Matplotlib axis object (where to add the box)
        plot_spec: Plot specification dictionary (from PLOT_CONFIG)
        metadata: Metadata dictionary from get_plot_metadata()
        font_size: Font size for text box (default: 8, should be small to not obstruct plot)
    """
    # Generate formatted configuration text
    config_text = format_plot_config_text(plot_spec, metadata)
    
    # Split into lines (already newline-separated from format_plot_config_text)
    lines = config_text.split('\n')
    
    # Rejoin lines (in case we need to process them further)
    textstr = '\n'.join(lines)
    
    # Create text box properties: rounded corners, semi-transparent wheat background
    props = dict(
        boxstyle='round',      # Rounded corners
        facecolor='wheat',     # Light background color
        alpha=0.8,             # Semi-transparent (80% opacity)
        edgecolor='gray',      # Gray border
        linewidth=0.5          # Thin border
    )
    
    # Add text box to axis
    # Position: 0.98 = 98% from left (right side), 0.02 = 2% from bottom
    # transform=ax.transAxes means coordinates are relative to axis (0-1 range)
    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=font_size,
            verticalalignment='bottom',    # Align text to bottom of box
            horizontalalignment='right',   # Align text to right of box
            bbox=props,                    # Apply box styling
            family='monospace')            # Use monospace font for readability


def save_plot_metadata(metadata, plot_dir, filename_base):
    """
    Save plot metadata to JSON file alongside plot.
    
    Saves a JSON file with the same base name as the plot (with "_metadata.json" suffix)
    containing all configuration and data statistics. This allows for:
    - Reproducing plots with the same configuration
    - Understanding what data/parameters were used
    - Tracking plot generation history
    
    Args:
        metadata: Metadata dictionary from get_plot_metadata()
        plot_dir: Directory where plot is saved (e.g., './cox/cox_plots')
        filename_base: Base filename without extension (e.g., 'km_tb_ratio_by_yg_b3_q_all')
    
    Returns:
        str: Path to saved metadata file
    """
    # Create metadata filename: same as plot but with "_metadata.json" suffix
    metadata_path = os.path.join(plot_dir, f"{filename_base}_metadata.json")
    
    # Convert numpy types to native Python types for JSON serialization
    # JSON doesn't support numpy types, so we need to convert them
    def convert_to_serializable(obj):
        """Recursively convert numpy types to Python native types."""
        if isinstance(obj, np.integer):
            return int(obj)  # Convert numpy int to Python int
        elif isinstance(obj, np.floating):
            return float(obj)  # Convert numpy float to Python float
        elif isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert numpy array to Python list
        elif isinstance(obj, dict):
            # Recursively convert dictionary values
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively convert list items
            return [convert_to_serializable(item) for item in obj]
        elif pd.isna(obj):
            return None  # Convert pandas NaN to None (JSON null)
        return obj  # Return as-is if already serializable
    
    # Convert all numpy types in metadata to Python native types
    serializable_metadata = convert_to_serializable(metadata)
    
    # Add timestamp for tracking when plot was created
    serializable_metadata['created_at'] = datetime.now().isoformat()
    
    # Write metadata to JSON file with pretty formatting (indent=2)
    with open(metadata_path, 'w') as f:
        json.dump(serializable_metadata, f, indent=2)
    
    return metadata_path


def _format_list_short(items, max_items=19):
    """Format a list for compact display in metadata cards."""
    if not items:
        return "None"
    items = list(items)
    if len(items) <= max_items:
        return ", ".join([str(x) for x in items])
    return f"{len(items)} items"


def _build_metadata_card_lines(metadata):
    """Create a list of lines for a compact metadata card."""
    lines = []
    lines.append("PLOT")
    lines.append(f"  name: {metadata.get('plot_name')}")
    lines.append(f"  type: {metadata.get('plot_type')}")
    lines.append(f"  variable: {metadata.get('variable')}")
    lines.append(f"  group_by: {metadata.get('group_by')}")
    lines.append("")

    cfg = metadata.get("configuration", {})
    lines.append("CONFIG")
    lines.append(f"  bin_continuous: {cfg.get('bin_continuous')}")
    lines.append(f"  n_bins: {cfg.get('n_bins')}")
    lines.append(f"  bin_method: {cfg.get('bin_method')}")
    lines.append(f"  min_group_size: {cfg.get('min_group_size')}")
    lines.append(f"  use_time_varying: {cfg.get('use_time_varying')}")
    lines.append(f"  filter_zero_oer: {cfg.get('filter_zero_oer')}")
    lines.append(f"  filter_nan_variable: {cfg.get('filter_nan_variable')}")
    lines.append("")

    lines.append("MODEL")
    lines.append(f"  create_dummies: {cfg.get('dummy_create')}")
    lines.append(f"  exclude_reference: {cfg.get('dummy_exclude_reference')}")
    lines.append(f"  model_static_cols: {_format_list_short(cfg.get('model_static_cols'))}")
    lines.append(f"  model_time_varying_cols: {_format_list_short(cfg.get('model_time_varying_cols'))}")
    lines.append("")

    div_cfg = cfg.get("division_config") or {}
    lines.append("DIVISION")
    if not div_cfg or not div_cfg.get("enabled"):
        lines.append("  enabled: False")
    else:
        lines.append("  enabled: True")
        lines.append(f"  div_cum_time: {div_cfg.get('create_div_cum_time')}")
        lines.append(f"  div_ratio_time: {div_cfg.get('create_div_ratio_time')}")
        lines.append(f"  final_div_cpt: {div_cfg.get('create_final_div_cpt')}")
        lines.append(f"  division_list: {_format_list_short(div_cfg.get('division_list'))}")
    lines.append("")

    filtering = cfg.get("filtering_params")
    lines.append("FILTERS")
    if not filtering:
        lines.append("  (no filtering params)")
    else:
        # Dates
        dates = filtering.get("filter_dates", {})
        if dates.get("enabled"):
            lines.append(f"  dates: {dates.get('start_date')} to {dates.get('end_date')}")
        else:
            lines.append("  dates: all")

        # Job codes
        jobs = filtering.get("filter_job_codes", {})
        if jobs.get("enabled"):
            if jobs.get("exclude_problematic"):
                prob_codes = jobs.get("problematic_codes")
                lines.append(f"  job_codes: exclude problematic ({len(prob_codes or [])} codes)")
                lines.append(f"  excluded codes: {prob_codes}")
            if jobs.get("include_specific"):
                lines.append(f"  job_codes: include {_format_list_short(jobs.get('include_specific'))}")
                if jobs.get("include_only_specific"):
                    lines.append(f"  included only specific jobs")
        else:
            lines.append("  job_codes: all")

        # Gender
        gender = filtering.get("filter_gender", {})
        if gender.get("enabled"):
            inc = gender.get("include_gender") or "all"
            lines.append(f"  gender: {inc}, excl_dual={gender.get('exclude_dual_gender')}")
        else:
            lines.append("  gender: all")

        # Year groups
        ygs = filtering.get("filter_ygs", {})
        if ygs.get("enabled"):
            if ygs.get("include_specific"):
                lines.append(f"  ygs: include {_format_list_short(ygs.get('include_specific'))}")
            if ygs.get("exclude_specific"):
                lines.append(f"  ygs: exclude {_format_list_short(ygs.get('exclude_specific'))}")
        else:
            lines.append("  ygs: all")

        # Divisions
        divs = filtering.get("filter_divisions", {})
        if divs.get("enabled"):
            div_line = []
            if divs.get("gtw_only"):
                div_line.append("gtw_only")
            if divs.get("prestige_only"):
                div_line.append("prestige_only")
            if divs.get("include_divisions"):
                div_line.append(f"include {_format_list_short(divs.get('include_divisions'))}")
            if not div_line:
                div_line.append("custom")
            lines.append(f"  divisions: {', '.join(div_line)}")
        else:
            lines.append("  divisions: all")
    lines.append("")

    stats = metadata.get("data_stats", {})
    lines.append("DATA")
    lines.append(f"  total_officers: {stats.get('total_officers'):,}")
    lines.append(f"  total_intervals: {stats.get('total_intervals'):,}")
    lines.append(f"  n_groups: {stats.get('n_groups'):,}")
    date_range = stats.get("date_range")
    if date_range and isinstance(date_range, dict):
        lines.append(f"  date_range: {date_range.get('start')} to {date_range.get('end')}")
    else:
        lines.append("  date_range: n/a")
    lines.append("")

    group_sizes = metadata.get("group_sizes") or {}
    lines.append("GROUP SIZES")
    if group_sizes:
        # Sort by size desc and show top groups
        top_groups = sorted(group_sizes.items(), key=lambda x: x[1], reverse=True)
        for group, n in top_groups[:10]:
            lines.append(f"  {group}: {n:,}")
        if len(top_groups) > 10:
            lines.append(f"  ... ({len(top_groups)} groups)")
    else:
        lines.append("  n/a")

    return lines


def plot_var_distribution(
    series,
    label,
    bins='fd',
    min_bins=10,
    max_bins=60,
    color='steelblue',
    log_x=False,
    log_y=False,
    output_dir=None,
    filename=None,
    dpi=300,
):
    """
    Plot a professional histogram with summary stats.

    Args:
        series: Pandas Series or array-like
        label: Axis/title label
        bins: 'fd', 'scott', 'sturges', or int
        min_bins: Minimum number of bins when using a rule
        max_bins: Maximum number of bins when using a rule
        color: Histogram color
        log_x: If True, use log scale on x-axis (drops nonpositive values)
        log_y: If True, use log scale on y-axis
        output_dir: Optional directory to save the plot
        filename: Optional filename (without extension if you prefer)
        dpi: Image resolution when saving
    """
    if series is None:
        print(f"⚠️ No data for distribution: {label}")
        return

    s = pd.to_numeric(pd.Series(series), errors='coerce').dropna()
    if log_x:
        nonpos = (s <= 0).sum()
        if nonpos:
            print(f"⚠️ Dropping {nonpos:,} nonpositive values for log-x: {label}")
        s = s[s > 0]
    if s.empty:
        print(f"⚠️ No non-null values for distribution: {label}")
        return

    mean_val = s.mean()
    median_val = s.median()
    p05, p95 = np.percentile(s, [5, 95])
    # Determine bin edges
    if isinstance(bins, str):
        edges = np.histogram_bin_edges(s, bins=bins)
        n_bins = max(1, len(edges) - 1)
        if min_bins is not None:
            n_bins = max(n_bins, int(min_bins))
        if max_bins is not None:
            n_bins = min(n_bins, int(max_bins))
        edges = np.linspace(s.min(), s.max(), n_bins + 1)
        hist_bins = edges
    else:
        hist_bins = bins

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(s, bins=hist_bins, color=color, alpha=0.75, edgecolor='white', linewidth=0.8)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label='Mean')
    ax.axvline(median_val, color='black', linestyle=':', linewidth=1.5, label='Median')

    ax.set_title(f"Distribution: {label}", fontsize=12, fontweight='bold')
    ax.set_xlabel(label, fontsize=10, fontweight='bold')
    ax.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    if log_x:
        ax.set_xscale('log')
    if log_y:
        ax.set_yscale('log')
    
    stats_text = (
        f"n={len(s):,}\n"
        f"mean={mean_val:.3f}\n"
        f"median={median_val:.3f}\n"
        f"p05={p05:.3f}\n"
        f"p95={p95:.3f}"
    )
    ax.text(
        0.98, 0.98, stats_text,
        transform=ax.transAxes,
        ha='right', va='top',
        fontsize=8,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    )

    plt.tight_layout()

    output_path = None
    if output_dir:
        if filename is None:
            safe_label = (
                str(label)
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
            )
            filename = f"distribution_{safe_label}.png"
        elif not filename.endswith(".png"):
            filename = f"{filename}.png"

        output_path = os.path.join(output_dir, filename)
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        
    plt.show()
    plt.close(fig)
    return output_path


def plot_competing_risks_cif_bars(
    plot_df,
    plot_spec,
    metadata,
    output_dir=None,
    filename_base=None,
    dpi=400,
    figsize=(10, 9),
    tick_sz=None,
    legend_outside=True,
):
    """
    Plot bar charts of final CIF by bin for promotion and attrition.

    Bars are ordered by the mean of the plotted variable (ascending),
    which yields z-score ascending order when plotting z-scored variables.

    If ``plot_spec['cr_color_mode']`` is one of ``set1`` / ``tab20`` / ``husl`` / ``glasbey``,
    bar colors match the competing-risks curves (via ``cr_discrete_group_colors``). Otherwise
    the blue/orange gradient from ``cif_bar_palette*`` is used.

    ``plot_spec['cif_bar_xtick_labels']``: ``'group'`` (division names), ``'quantile'`` (Q1..Qn),
    or ``None`` for auto: group labels when ``group_only_curves`` and ``group_by`` are set.
    """
    if plot_df is None or plot_df.empty:
        print("⚠️ No data for CIF bar plots.")
        return None

    var_name = plot_spec.get("variable")
    group_col = "plot_group"
    if group_col not in plot_df.columns:
        print("⚠️ plot_group missing; cannot build CIF bars.")
        return None

    # Compute per-group stats
    group_stats = []
    for group, gdf in plot_df.groupby(group_col):
        # Match competing-risks filtering: require valid stop time
        if "stop_time" in gdf.columns:
            gdf = gdf[gdf["stop_time"].notna() & (gdf["stop_time"] > 0)].copy()
        n = len(gdf)
        if n == 0:
            continue
        promo_rate = (gdf["event"] == 1).sum() / n if "event" in gdf.columns else np.nan
        attr_rate = (gdf["event"] == 2).sum() / n if "event" in gdf.columns else np.nan
        if var_name and var_name in gdf.columns:
            mean_val = pd.to_numeric(gdf[var_name], errors="coerce").mean()
            min_val = pd.to_numeric(gdf[var_name], errors="coerce").min()
            max_val = pd.to_numeric(gdf[var_name], errors="coerce").max()
        else:
            mean_val = min_val = max_val = np.nan
        group_stats.append({
            "group": group,
            "n": n,
            "promo_rate": promo_rate,
            "attr_rate": attr_rate,
            "mean_val": mean_val,
            "min_val": min_val,
            "max_val": max_val,
        })

    if not group_stats:
        print("⚠️ No group stats for CIF bar plots.")
        return None

    # Sort by mean of variable (ascending). Fallback to group label order.
    if not all(np.isnan(gs["mean_val"]) for gs in group_stats):
        group_stats.sort(key=lambda x: (np.nan_to_num(x["mean_val"], nan=0.0)))
    else:
        group_stats.sort(key=lambda x: str(x["group"]))

    labels = []
    promo_vals = []
    attr_vals = []
    legend_labels = []
    footnote_lines = []
    for gs in group_stats:
        labels.append(str(gs["group"]))
        promo_vals.append(gs["promo_rate"])
        attr_vals.append(gs["attr_rate"])
        legend_labels.append(str(gs["group"]))
        if not np.isnan(gs["mean_val"]):
            footnote_lines.append(
                f"{gs['group']}: N={gs['n']:,}, avg={gs['mean_val']:.3f}, "
                f"range={gs['min_val']:.3f}-{gs['max_val']:.3f}"
            )
        else:
            footnote_lines.append(f"{gs['group']}: N={gs['n']:,}")
    footnote_lines = []
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=False)
    ax1, ax2 = axes
    x = np.arange(len(labels))
    ordered_groups = [gs["group"] for gs in group_stats]
    n_ord = len(ordered_groups)
    q_labels = [f"Q{i+1}" for i in range(n_ord)]

    xtick_mode = plot_spec.get("cif_bar_xtick_labels")
    if xtick_mode is None:
        xtick_mode = (
            "group" if (plot_spec.get("group_only_curves") and plot_spec.get("group_by")) else "quantile"
        )
    if xtick_mode == "group":
        bar_cats = [str(gs["group"]) for gs in group_stats]
    else:
        bar_cats = list(q_labels)

    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def _rgb_to_hex(rgb):
        return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in rgb)

    def _build_hex_gradient(hex_colors, n_colors):
        if not hex_colors:
            return None
        if len(hex_colors) == n_colors:
            return hex_colors
        if len(hex_colors) == 1:
            return [hex_colors[0]] * n_colors
        # Interpolate between first and last colors
        start = _hex_to_rgb(hex_colors[0])
        end = _hex_to_rgb(hex_colors[-1])
        gradient = []
        for i in range(n_colors):
            t = i / max(n_colors - 1, 1)
            rgb = (
                start[0] + (end[0] - start[0]) * t,
                start[1] + (end[1] - start[1]) * t,
                start[2] + (end[2] - start[2]) * t,
            )
            gradient.append(_rgb_to_hex(rgb))
        return gradient

    cmode = plot_spec.get("cr_color_mode")
    if cmode in ("set1", "tab20", "husl", "glasbey"):
        promo_palette = cr_discrete_group_colors(n_ord, cmode)
        attr_palette = list(promo_palette)
    else:
        promo_palette = plot_spec.get("cif_bar_palette_promo") or plot_spec.get("cif_bar_palette")
        attr_palette = plot_spec.get("cif_bar_palette_attr") or plot_spec.get("cif_bar_palette")
        promo_palette = _build_hex_gradient(promo_palette or ["#d7e6f5", "#1f5aa6"], n_ord)
        attr_palette = _build_hex_gradient(attr_palette or ["#fde2cf", "#c0581a"], n_ord)

    promo_color_map = {g: promo_palette[i] for i, g in enumerate(ordered_groups)}
    attr_color_map = {g: attr_palette[i] for i, g in enumerate(ordered_groups)}
    promo_colors = [promo_color_map.get(gs["group"], "#4c4c4c") for gs in group_stats]
    attr_colors = [attr_color_map.get(gs["group"], "#4c4c4c") for gs in group_stats]
    
    promo_df = pd.DataFrame({"bin": bar_cats, "cif": promo_vals})
    attr_df = pd.DataFrame({"bin": bar_cats, "cif": attr_vals})
    promo_df["bin"] = pd.Categorical(promo_df["bin"], categories=bar_cats, ordered=True)
    attr_df["bin"] = pd.Categorical(attr_df["bin"], categories=bar_cats, ordered=True)

    if _SEABORN_AVAILABLE:
        sns.barplot(x="bin", y="cif", data=promo_df, ax=ax1, palette=promo_colors)
    else:
        ax1.bar(x, promo_vals, color=promo_colors, alpha=0.95)
    var_label = f" ({var_name})" if var_name else ""
    show_titles = plot_spec.get("cif_bar_show_titles", False)
    show_xlabels = plot_spec.get("cif_bar_show_xlabels", False)
    if show_titles:
        ax1.set_title(f"Final CIF: Promotion{var_label}", fontweight="bold")
    ax1.set_ylabel("Final CIF")
    ax1.grid(axis="y", alpha=0.25)
    _xlab = None
    if show_xlabels:
        _xlab = plot_spec.get("group_by", "Group") if xtick_mode == "group" else "Bin"
    ax1.set_xlabel(_xlab)
    ax1.set_xticks(x)
    _rot = 45 if xtick_mode == "group" else 0
    _ha = "right" if _rot else "center"
    ax1.set_xticklabels(bar_cats, rotation=_rot, ha=_ha)
    ax1.tick_params(axis="x", labelbottom=True)
    if tick_sz is not None:
        ax1.tick_params(axis="both", which="major", labelsize=tick_sz)
    
    if _SEABORN_AVAILABLE:
        sns.barplot(x="bin", y="cif", data=attr_df, ax=ax2, palette=attr_colors)
    else:
        ax2.bar(x, attr_vals, color=attr_colors, alpha=0.95)
    if show_titles:
        ax2.set_title(f"Final CIF: Attrition{var_label}", fontweight="bold")
    ax2.set_ylabel("Final CIF")
    ax2.grid(axis="y", alpha=0.25)
    _xlab2 = None
    if show_xlabels:
        _xlab2 = plot_spec.get("group_by", "Group") if xtick_mode == "group" else "Bin"
    ax2.set_xlabel(_xlab2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(bar_cats, rotation=_rot, ha=_ha)
    if tick_sz is not None:
        ax2.tick_params(axis="both", which="major", labelsize=tick_sz)
        
    # Legend with bin labels (optional)
    show_legend = plot_spec.get("cif_bar_show_legend", False)
    handles = [plt.Line2D([0], [0], color="none") for _ in legend_labels]
    if show_legend:
        if legend_outside:
            fig.legend(
                handles,
                legend_labels,
                fontsize=8,
                loc="lower center",
                bbox_to_anchor=(0.5, -0.02),
                ncol=2,
                frameon=True,
            )
        else:
            ax1.legend(handles, legend_labels, fontsize=8, loc="upper right")

    # Footnote boxes under each subplot with bin metadata (two columns)
    footnote_text = ""
    if footnote_lines:
        mid = (len(footnote_lines) + 1) // 2
        left_col = footnote_lines[:mid]
        right_col = footnote_lines[mid:]
        pad = max(len(s) for s in left_col) + 3
        merged_lines = []
        for i in range(max(len(left_col), len(right_col))):
            left = left_col[i] if i < len(left_col) else ""
            right = right_col[i] if i < len(right_col) else ""
            merged_lines.append(left.ljust(pad) + right)
        footnote_text = "\n".join(merged_lines)
        


    if footnote_text:
        box_props = dict(boxstyle="round", facecolor="wheat", alpha=0.6, edgecolor="gray", linewidth=0.5)
        ax1.text(
            0.5,
            -0.25,
            footnote_text,
            transform=ax1.transAxes,
            ha="center",
            va="top",
            fontsize=8,
            bbox=box_props,
        )
        ax2.text(
            0.5,
            -0.25,
            footnote_text,
            transform=ax2.transAxes,
            ha="center",
            va="top",
            fontsize=8,
            bbox=box_props,
        )
        
    # Space between the two CIF bar chart panels (Promotion top, Attrition bottom).
    # Adjust via plot_spec['cif_bar_hspace'] or PLOT_CONFIG['cif_bar_hspace']  (e.g. 0.6 = more gap)
    hspace = plot_spec.get('cif_bar_hspace') or 0.6
    if legend_outside and show_legend:
        plt.tight_layout(rect=[0, 0.22, 1, 1])
        plt.subplots_adjust(hspace=hspace, bottom=0.28)
    elif legend_outside:
        plt.tight_layout(rect=[0, 0.18, 1, 1])
        plt.subplots_adjust(hspace=hspace, bottom=0.24)
    else:
        plt.tight_layout()
        plt.subplots_adjust(hspace=hspace, bottom=0.12)

    output_path = None
    if output_dir and filename_base:
        if filename_base.endswith(".png"):
            filename_base = filename_base[:-4]
        output_path = os.path.join(output_dir, f"{filename_base}_cif_bars.png")
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")

    plt.show()
    plt.close(fig)
    return output_path


def composite_cif_curve_and_bars(path_cr_plot, path_bar_plot, path_out, dpi=300):
    """
    Build a single image for slides: 2x2 layout from saved CIF curve plot and CIF bar plot.
    Left column: Promotion CIF curve (top), Promotion CIF bars (bottom).
    Right column: Attrition CIF curve (top), Attrition CIF bars (bottom).
    Both input PNGs are assumed to be two-panel figures (top=promo, bottom=attrition).
    """
    from matplotlib import image as mpl_image
    if not os.path.isfile(path_cr_plot) or not os.path.isfile(path_bar_plot):
        return None
    cr_img = mpl_image.imread(path_cr_plot)
    bar_img = mpl_image.imread(path_bar_plot)
    H_cr, W_cr = cr_img.shape[:2]
    H_bar, W_bar = bar_img.shape[:2]
    # Top half = promo, bottom half = attrition (both figures)
    promo_curve = cr_img[: H_cr // 2, :]
    attr_curve = cr_img[H_cr // 2 :, :]
    promo_bar = bar_img[: H_bar // 2, :]
    attr_bar = bar_img[H_bar // 2 :, :]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].imshow(promo_curve)
    axes[0, 0].set_title("Promotion (CIF curve)", fontsize=11, fontweight="bold")
    axes[0, 0].axis("off")
    axes[0, 1].imshow(attr_curve)
    axes[0, 1].set_title("Attrition (CIF curve)", fontsize=11, fontweight="bold")
    axes[0, 1].axis("off")
    axes[1, 0].imshow(promo_bar)
    axes[1, 0].set_title("Promotion (CIF bars)", fontsize=11, fontweight="bold")
    axes[1, 0].axis("off")
    axes[1, 1].imshow(attr_bar)
    axes[1, 1].set_title("Attrition (CIF bars)", fontsize=11, fontweight="bold")
    axes[1, 1].axis("off")
    plt.tight_layout()
    fig.savefig(path_out, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path_out

def save_plot_metadata_card(
    metadata,
    plot_dir,
    filename_base,
    figsize=(8, 5),
    dpi=200,
    wrap_width=48,
):
    """
    Save a compact, two-column metadata card as a PNG image.

    This is intended for pasting into slides next to a plot.
    """
    import textwrap
    import matplotlib.pyplot as plt

    # Build and wrap lines for a readable card
    raw_lines = _build_metadata_card_lines(metadata)
    wrapped_lines = []
    for line in raw_lines:
        if not line:
            wrapped_lines.append("")
            continue
        wrapped = textwrap.wrap(line, width=wrap_width, subsequent_indent="  ")
        wrapped_lines.extend(wrapped if wrapped else [""])

    # Split into two columns
    mid = (len(wrapped_lines) + 1) // 2
    left_text = "\n".join(wrapped_lines[:mid])
    right_text = "\n".join(wrapped_lines[mid:])

    # Draw card
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor("white")
    title = f"Metadata: {metadata.get('plot_name')}"
    fig.text(0.02, 0.98, title, ha="left", va="top", fontsize=11, fontweight="bold")
    fig.text(0.02, 0.92, left_text, ha="left", va="top", fontsize=9, family="monospace")
    fig.text(0.52, 0.92, right_text, ha="left", va="top", fontsize=9, family="monospace")

    # Save
    output_path = os.path.join(plot_dir, f"{filename_base}_metadata_card.png")
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return output_path
