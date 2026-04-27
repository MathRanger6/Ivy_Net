# How the "Red Line" Is Built (Cell 11 Competing Risks)

This is the plain-English flow for how the "highest OPM bin" line (often the red line) is built in the current `520_pipeline_cox_working.ipynb` logic.

## 0) What a row means before plotting

- In `df_analysis`, each row is a person-time interval (roughly one snapshot period for one officer), with fields like `pid_pde`, `start_time`, `stop_time`, `event`, and OPM-style variables.

## 1) Start from the Cell 11 analysis dataframe

- Cell 11 passes `df_analysis` into `prepare_plot_data(...)` for each plot spec.

## 2) Collapse to one row per officer

- The code sorts by `pid_pde` and `stop_time`, then does `groupby('pid_pde').last()`.
- That keeps each officer's **last** interval row.
- So binning for the CR plot is based on final-row values for each officer.

## 3) Apply requested filters

- Depending on the plot spec, officers can be filtered out (for example, missing plotted variable, optional OER-related filters, optional group-by filters).

## 4) Read the plotted OPM/z variable

- The variable in `plot_spec['variable']` is read from that one-row-per-officer table.
- If `bin_continuous=True`, the code bins that variable (for example, into 4 bins).

## 5) Assign officers to bins (`plot_group`)

- Officers get a `plot_group` label (for example, lowest to highest OPM bin).
- The "highest bin" group is the one with the highest mean of that plotted variable.

## 6) Build the promotion CR curve for each group

- For each `plot_group`, the code takes only officers in that group.
- It sorts by `stop_time`.
- For each distinct time, it counts promotion events (`event == 1`) at that time.
- It accumulates those counts as a running proportion using a fixed denominator (`len(group_data)`).

## 7) Plot that cumulative series vs time

- X-axis: `stop_time` (days).
- Y-axis: cumulative promotion incidence from the notebook's `calculate_cif` implementation (cumulative, not instantaneous).

## 8) What the "red line at time t" means in this implementation

- It is the cumulative promotion curve for officers in the top OPM bin defined from the one-row-per-officer table used by `prepare_plot_data`.
- In current code, that binning step is based on each officer's final-row value (after filtering), not a separate "everyone at exactly day 1000" landmark construction.

---

## One-line summary

The red line is built by taking officers whose plotted OPM variable falls in the highest bin (from the one-row-per-officer final-row table), then plotting their cumulative promotion incidence over `stop_time`.
