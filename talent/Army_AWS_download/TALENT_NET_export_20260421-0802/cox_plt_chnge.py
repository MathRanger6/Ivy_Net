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
        title = f"{plot_type_display}: {var_display} by {group_display}"
    else:
        # Title without grouping: "Kaplan-Meier: Variable"
        title = f"{plot_type_display}: {var_display}"
    
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
        if len(group_var_data) > 0:
            # Calculate descriptive statistics for this bin
            avg_val = group_var_data.mean()   # Average value in this bin
            min_val = group_var_data.min()    # Minimum value in this bin
            max_val = group_var_data.max()    # Maximum value in this bin
            # Add statistics to label (assumes percentage values, adjust format if needed)
            label += f" (avg: {avg_val:.1f}%, range: {min_val:.1f}-{max_val:.1f}, N={n_officers:,})"
        else:
            # No data available, just show sample size
            label += f" (N={n_officers:,})"
    else:
        # Not binned or no variable: just show sample size
        label += f" (N={n_officers:,})"
    
    # For competing risks plots, add final cumulative incidence function (CIF)
    # This shows the final promotion/attrition rate for the group
    # Check both plot_df and group_data to ensure 'event' column exists
    if plot_spec['plot_type'] == 'competing_risks':
        if 'event' in plot_df.columns and 'event' in group_data.columns:
            # Calculate final promotion rate (proportion promoted by end of observation)
            n_promoted = (group_data['event'] == 1).sum()
            if n_officers > 0:
                promo_rate = n_promoted / n_officers
                label += f", final CIF: {promo_rate:.2f}"  # Add CIF to label
        # If 'event' column doesn't exist, silently skip CIF addition (not a critical error)
    
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


def _format_list_short(items, max_items=6):
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
                n_prob = len(jobs.get("problematic_codes") or [])
                lines.append(f"  job_codes: exclude problematic ({n_prob} codes)")
            if jobs.get("include_specific"):
                lines.append(f"  job_codes: include {_format_list_short(jobs.get('include_specific'))}")
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
    lines.append(f"  total_officers: {stats.get('total_officers')}")
    lines.append(f"  total_intervals: {stats.get('total_intervals')}")
    lines.append(f"  n_groups: {stats.get('n_groups')}")
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
        for group, n in top_groups[:8]:
            lines.append(f"  {group}: {n:,}")
        if len(top_groups) > 8:
            lines.append(f"  ... ({len(top_groups)} groups)")
    else:
        lines.append("  n/a")

    return lines


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