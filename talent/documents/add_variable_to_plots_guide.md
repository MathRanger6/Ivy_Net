# Adding Variables to CR Plots, PE Plots, and/or Cox Analysis

This guide explains how the pipeline decides which variables are in the model and in the data, and how to add a variable (e.g. **div_name**, **yg**) to competing-risks (CR) plotting, partial-effects (PE) plots, and/or the Cox model.

---

## 1. Static vs time-varying

- **Static** (e.g. **yg**, final_job_code): One value per officer for the whole follow-up. Cell 10 takes them from officer-level data and repeats that value for every interval. They belong in **static** config (`model_static_cols` or an extra-static list), **not** in time-varying lists.
- **Time-varying** (e.g. **div_name**): Can change from snapshot to snapshot (e.g. officer moves divisions). Cell 10 takes them from each snapshot, so each interval gets the value at that time. They belong in **time-varying** config (`EXTRA_TIME_VARYING_COLS` → `model_time_varying_cols`).

**Impact:** Static vars give “effect of being in group X” (constant for the officer). Time-varying vars give “effect of currently being in X” and have within-officer variation, which helps identify effects. Use the correct list so the pipeline builds the right structure.

---

## 2. What actually puts a variable in the model and in the data

### 2.1 Single source of truth for “in the pipeline and in the model”

- **Time-varying:**  
  **`EXTRA_TIME_VARYING_COLS`** (in your override, e.g. `pipeline_config_17_1.py`) is appended to **`model_time_varying_cols`**.  
  Then **`time_varying_cols`** is set to:  
  `base + oer + prestige + model_time_varying_cols`.  
  So anything in `model_time_varying_cols` is automatically carried into Cell 10 (survival data → `df_cox`) and into the Cox model variable list in Cell 12. No need to add the same variable to a second list.

- **Static:**  
  Use **`model_static_cols`** (or an **EXTRA_STATIC_COLS** list you append to it). That controls which static variables are in the model. Static columns must also be present in the data that feeds Cell 10 (e.g. in officer_info / the frame that has one row per officer).

### 2.2 Dummy creation: who creates dummies?

- **`COLUMN_CONFIG['dummy_variables']['categorical_cols']`** (in base `pipeline_config.py`):  
  Cell 11 **only** creates dummies for columns that are (a) listed in **`categorical_cols`** and (b) present in `df_analysis`. So if a column isn’t in the pipeline (e.g. you removed it from `EXTRA_TIME_VARYING_COLS`), Cell 11 skips it and it never enters the model.

- **Cell 12** has **hardcoded** logic for **yg**, **final_job_code**, and **div_name**. For those three, Cell 12 can create dummies itself (when `create_dummies` is True) if they’re in the model list and still in the dataframe. So for div_name you can leave it out of `categorical_cols` and Cell 12 will still create div dummies; adding div_name to `categorical_cols` just means Cell 11 creates them instead.

### 2.3 “I don’t want this variable to confound the model right now”

- **Remove it from the list that puts it in the model.**  
  For time-varying: remove it from **`EXTRA_TIME_VARYING_COLS`**.  
  For static: remove it from **`model_static_cols`** (or your EXTRA_STATIC_COLS).

- You can **leave** it in **`categorical_cols`**. When the variable isn’t in the pipeline, it won’t be in `df_cox`/`df_analysis`, so Cell 11 will skip it (“column not found”). It will not be in the model, so no confounding or extra collinearity.

---

## 3. How to add a variable: step-by-step

### 3.1 Add a **time-varying** variable (e.g. **div_name**) to Cox analysis and/or plots

**Goal:** Variable is in the survival data, in the Cox model (as dummies), and available for CR/PE plotting.

1. **Create the column earlier in the pipeline** (e.g. Cell 7 for `div_name` when `DIVISION_CONFIG['enabled'] = True`). Ensure it exists on the snapshot frame that feeds Cell 10.

2. **In your override (e.g. `pipeline_config_17_1.py`):**
   - Add the column name to **`EXTRA_TIME_VARYING_COLS`**:
     ```python
     EXTRA_TIME_VARYING_COLS = [
         'div_name',   # add others as needed
     ]
     COLUMN_CONFIG['model_time_varying_cols'] = list(COLUMN_CONFIG.get('model_time_varying_cols', [])) + EXTRA_TIME_VARYING_COLS
     ```
   - Ensure **`create_dummies`** is True if the variable is categorical:
     ```python
     COLUMN_CONFIG['dummy_variables']['create_dummies'] = True
     ```

3. **Optional:** Add it to **`categorical_cols`** in base `pipeline_config.py` (uncomment or add an entry) if you want Cell 11 to create the dummies; otherwise Cell 12 will create them for div_name.

4. **`time_varying_cols`** is already built from `model_time_varying_cols` in the override, so the variable is carried into Cell 10 and Cell 11 automatically. No extra step.

5. **Re-run** from Cell 7 (if you added a new column) and Cell 10 onward so `df_cox` and the model include the variable.

**CR plot with this variable (e.g. group by div_name):**  
Set **`USE_OVERRIDE_CR_PLOTS = True`** and add a plot that uses the variable (e.g. `group_by='div_name'`, and optionally `variable=...`, `n_bins=1`). The variable must be in `df_cox` (so it must be in `EXTRA_TIME_VARYING_COLS` / `model_time_varying_cols` as above).

**PE plots:**  
Time-varying variables that are in the model will appear in the set of variables considered for partial-effects plots (Cell 12.6). Division dummies (e.g. `div_82ABN`) can appear as categorical bars in 12.6 if they’re in the key-vars list; 12.6A is for combined linear+quadratic terms.

---

### 3.2 Add a **static** variable (e.g. **yg**) to Cox analysis and/or plots

**Goal:** Variable is in the Cox model (as dummies) and available for plotting, without putting it in time-varying lists.

1. **Ensure the column exists** in the data that feeds Cell 10 (e.g. officer-level frame with one row per officer; yg is usually already there from Cell 3 or 502).

2. **In your override:**
   - Append it to **`model_static_cols`** (or use an **EXTRA_STATIC_COLS** list):
     ```python
     EXTRA_STATIC_COLS = ['yg']   # or [] when you don't want it
     COLUMN_CONFIG['model_static_cols'] = list(COLUMN_CONFIG.get('model_static_cols', [])) + EXTRA_STATIC_COLS
     ```
   - Ensure **`create_dummies`** is True if it’s categorical.
   - **Do not** add it to `EXTRA_TIME_VARYING_COLS` (that’s for time-varying only).

3. **Optional:** Add **yg** (or the column) to **`categorical_cols`** in base config if you want Cell 11 to create dummies; otherwise Cell 12 will create yg dummies via its hardcoded yg block.

4. **Re-run** from Cell 10 (or earlier if the static column is built earlier) so the static variable is in the model.

**CR plot:**  
Use the variable as `group_by` in an override CR plot (e.g. `group_by='yg'`). It must be in the data and in the model for the plot to use it.

---

### 3.3 Add a variable **only** to CR plotting (not to the Cox model)

**Goal:** Stratify or group CR plots by a variable without including it in the Cox model (to avoid confounding).

1. **Get the variable into the pipeline data only** (so it’s in `df_cox` for plotting), but **not** into **`model_time_varying_cols`** or **`model_static_cols`**.
   - For a **time-varying** column: you’d need it in **`time_varying_cols`** but **not** in `model_time_varying_cols`. Currently we set `time_varying_cols = base + oer + prestige + model_time_varying_cols`, so every model time-varying column is in the pipeline. To have a column in the pipeline but not in the model you’d add it to the base/oer/prestige part of `time_varying_cols` only (e.g. in base config or a separate “plot-only” list that gets merged into `time_varying_cols` but not into `model_time_varying_cols`). Implementation depends on your config layout.
   - For a **static** column: it would need to be in the officer-level data and in whatever column list Cell 10 uses for static columns, but not in `model_static_cols`.

2. **CR plot:** Set **`USE_OVERRIDE_CR_PLOTS = True`** and add a plot with the desired `variable` and/or `group_by`. The variable must exist in the data used for the CR plot (usually `df_cox` or the same analysis dataframe).

---

## 4. Quick reference

| Goal | Time-varying (e.g. div_name) | Static (e.g. yg) |
|------|-------------------------------|-------------------|
| In Cox model | Add to **EXTRA_TIME_VARYING_COLS** (in override) | Add to **model_static_cols** or **EXTRA_STATIC_COLS** |
| In pipeline data (Cell 10) | Automatic once in model_time_varying_cols | Must be in officer-level data and in static column list |
| Dummies | create_dummies=True; optional: add to categorical_cols | Same |
| CR plot by this variable | USE_OVERRIDE_CR_PLOTS=True, add plot with group_by='div_name' (and variable/n_bins as needed) | Same idea with group_by='yg' |
| Don’t want in model | Remove from EXTRA_TIME_VARYING_COLS | Remove from model_static_cols / EXTRA_STATIC_COLS |

---

## 5. Legacy note (run overrides and CR defaults)

- **RUN_PROFILE** and **expand_run_profile()** set the main time-varying model columns (tv_vars, quadratics, interaction) and the default CR plot set. CR options (bins, etc.) go in **RUN_CR_PLOT_DEFAULTS** and `'cr_plot_defaults'` in RUN_PROFILE.
- To customize CR plots per plot (e.g. one plot with `n_bins=1`, `group_by='div_name'`), set **USE_OVERRIDE_CR_PLOTS = True** and define the full **PLOT_CONFIG['plots']** list in the override (see commented example in `pipeline_config_17_1.py`).
