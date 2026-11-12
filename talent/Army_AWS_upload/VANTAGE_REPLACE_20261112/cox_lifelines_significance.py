"""
Cox model statistical significance via lifelines.

The 520 pipeline fits the Cox model with scikit-survival (CoxPHSurvivalAnalysis),
which does not provide p-values or standard errors. This module fits the same
model with lifelines (CoxPHFitter) to get Wald tests, p-values, and confidence
intervals for each coefficient.

Usage
-----
1) From the notebook (after Cell 12.3 has run):
    from cox_lifelines_significance import fit_and_test_significance
    summary_df, summary_str = fit_and_test_significance(
        df_full_model[final_model_vars].copy(),
        duration=full_time,
        event=full_event.astype(int),
        variables=final_model_vars,
        output_dir="./cox/cox_results",
        save_suffix="_stdz",
    )
    print(summary_str)

2) Standalone (after the notebook has saved full-model data):
    python cox_lifelines_significance.py

    Expects either:
    - cox/cox_results/full_model_for_lifelines.csv  (has columns: duration, event, + covariates)
    or
    - cox/cox_results/full_model_for_lifelines_stdz.csv  (when using z-scored run)

    The notebook Cell 12.3 saves this file after fitting the full model so you can
    run this script without re-running the whole pipeline.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple, Union

import pandas as pd
import numpy as np

try:
    from lifelines import CoxPHFitter
except ImportError:
    CoxPHFitter = None  # type: ignore


def fit_and_test_significance(
    df: pd.DataFrame,
    duration: Union[np.ndarray, pd.Series],
    event: Union[np.ndarray, pd.Series],
    variables: Optional[List[str]] = None,
    output_dir: str = "./cox/cox_results",
    save_suffix: str = "",
) -> Tuple[pd.DataFrame, str]:
    """
    Fit Cox model with lifelines and return summary with p-values and CIs.

    Parameters
    ----------
    df : pd.DataFrame
        Covariates only (same columns as used in sksurv fit). Must be aligned
        with duration and event (same length, same index if applicable).
    duration : array-like
        Time (e.g. interval length: stop_time - start_time). Same length as df.
    event : array-like
        1 if event (e.g. promotion), 0 if censored. Same length as df.
    variables : list of str, optional
        Column names to use. If None, uses all columns of df.
    output_dir : str
        Directory to save summary CSV. Created if missing.
    save_suffix : str
        Suffix for output filename (e.g. "_stdz" for z-scored run).

    Returns
    -------
    summary_df : pd.DataFrame
        lifelines summary table (coef, exp(coef), se, z, p, confidence intervals).
    summary_str : str
        Full summary as string (same as print(cph.summary)).
    """
    if CoxPHFitter is None:
        raise ImportError("lifelines is required. Install with: pip install lifelines")

    variables = variables or list(df.columns)
    # Build dataframe in lifelines format: duration, event + covariates
    out = df[variables].copy()
    out["duration"] = np.asarray(duration, dtype=float).ravel()
    out["event"] = np.asarray(event, dtype=int).ravel()

    if len(out) != len(df):
        raise ValueError("duration/event length must match df length")

    cph = CoxPHFitter()
    cph.fit(out, duration_col="duration", event_col="event")
    summary_df = cph.summary

    # Pretty-print summary
    summary_str = cph.summary.to_string()

    # Save summary table
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(
        output_dir,
        f"full_model_lifelines_significance{save_suffix}.csv",
    )
    summary_df.to_csv(out_path)
    summary_str += f"\n\n(Saved to {out_path})"

    return summary_df, summary_str


def run_from_saved_data(
    results_dir: str = "./cox/cox_results",
    filename: str = "full_model_for_lifelines",
    suffix: str = "",
) -> Tuple[pd.DataFrame, str]:
    """
    Load full-model data saved by the 520 notebook and run significance tests.

    Expects a CSV with columns: duration, event, and all covariate columns.
    Filename can be e.g. full_model_for_lifelines or full_model_for_lifelines_stdz.
    """
    base = f"{filename}{suffix}.csv"
    path = os.path.join(results_dir, base)
    if not os.path.isfile(path):
        alt = os.path.join(results_dir, filename + ".csv")
        if os.path.isfile(alt):
            path = alt
        else:
            raise FileNotFoundError(
                f"Full-model data not found at {path} or {alt}. "
                "Run the 520 notebook through Cell 12.3 so it saves full_model_for_lifelines*.csv"
            )

    df = pd.read_csv(path)
    if "duration" not in df.columns or "event" not in df.columns:
        raise ValueError(
            f"CSV must have 'duration' and 'event' columns. Found: {list(df.columns)}"
        )
    variables = [c for c in df.columns if c not in ("duration", "event")]
    duration = df["duration"].values
    event = df["event"].values
    df_cov = df[variables]

    return fit_and_test_significance(
        df_cov,
        duration=duration,
        event=event,
        variables=variables,
        output_dir=results_dir,
        save_suffix=suffix,
    )


if __name__ == "__main__":
    results_dir = "./cox/cox_results"
    # Match notebook suffix when using z-scored model
    suffix = "_stdz" if len(sys.argv) > 1 and sys.argv[1] == "stdz" else ""

    try:
        summary_df, summary_str = run_from_saved_data(
            results_dir=results_dir,
            filename="full_model_for_lifelines",
            suffix=suffix,
        )
        print("Cox model (lifelines) – statistical significance")
        print("=" * 60)
        print(summary_str)
    except FileNotFoundError as e:
        print(e)
        print("\nTo generate the data file, run the 520 notebook through Cell 12.3.")
        print("The notebook will save cox/cox_results/full_model_for_lifelines[suffix].csv")
        sys.exit(1)
