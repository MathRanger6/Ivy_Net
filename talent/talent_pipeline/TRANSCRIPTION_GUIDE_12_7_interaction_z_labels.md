# Transcription guide: Cell 12.7 interaction plot z-score labels

Use this when applying the same changes in another notebook or after a revert. **Cell:** 12.7 (INTERACTION EFFECTS 3D PLOTS). All edits are in that one cell.

---

## 1. After the line `var_y_label = spec.get('var_y_label') or var_y`

**Add these lines** (before "# Per-plot distribution overrides"):

```python
                        # Optional: use z-score versions of the variables
                        if use_z:
                            var_x = f"{prefix}{var_x}"
                            var_y = f"{prefix}{var_y}"
                        # Detect z-scored for labels/titles (either use_z or var names already have z_ prefix from run profile)
                        is_z_scale = use_z or (str(var_x).startswith(prefix) if var_x else False) or (str(var_y).startswith(prefix) if var_y else False)
                        var_x_label_display = f"{var_x_label} (z-scored)" if is_z_scale else var_x_label
                        var_y_label_display = f"{var_y_label} (z-scored)" if is_z_scale else var_y_label
```

---

## 2. Remove the duplicate block

**Delete** this block (it appears later, right before "# Ensure variables exist and are in the model"):

```python
                        # Optional: use z-score versions of the variables
                        if use_z:
                            var_x = f"{prefix}{var_x}"
                            var_y = f"{prefix}{var_y}"
```

(Keep only the one you added in step 1.)

---

## 3. Marginal-effect plot labels

**Find:**

- `axm.set_title(f"Marginal effect of {var_x_label} across {var_y_label}")`
- `axm.set_xlabel(var_y_label)`
- `axm.set_ylabel(f"Marginal slope (b1 + b3*{var_y_label})")`

**Replace with:**

- `axm.set_title(f"Marginal effect of {var_x_label_display} across {var_y_label_display}")`
- `axm.set_xlabel(var_y_label_display)`
- `axm.set_ylabel(f"Marginal slope (b1 + b3*{var_y_label_display})")`

---

## 4. 3D surface plot labels and title

**Find:**

- `ax.set_xlabel(var_x_label, labelpad=10, ...)`
- `ax.set_ylabel(var_y_label, labelpad=10, ...)`
- `title = f"Interaction: {var_x_label} vs {var_y_label}"`
- `if use_z:`
- `title += "\n(Standardized with Z-Scores)"`

**Replace with:**

- `ax.set_xlabel(var_x_label_display, labelpad=10, ...)`  (same kwargs)
- `ax.set_ylabel(var_y_label_display, labelpad=10, ...)`  (same kwargs)
- `title = f"Interaction: {var_x_label_display} vs {var_y_label_display}"`
- `if is_z_scale:`
- `title += "\n(Standardized with Z-Scores)"`  (unchanged)

---

## 5. Contour plot labels and title

**Find:**

- `ax2.set_xlabel(var_x_label, fontsize=10, ...)`
- `ax2.set_ylabel(var_y_label, fontsize=10, ...)`
- `title2 = f"Interaction Contour: {var_x_label} vs {var_y_label}"`
- `if use_z:`
- `title2 += "\n(Standardized with Z-Scores)"`

**Replace with:**

- `ax2.set_xlabel(var_x_label_display, fontsize=10, ...)`  (same kwargs)
- `ax2.set_ylabel(var_y_label_display, fontsize=10, ...)`  (same kwargs)
- `title2 = f"Interaction Contour: {var_x_label_display} vs {var_y_label_display}"`
- `if is_z_scale:`
- `title2 += "\n(Standardized with Z-Scores)"`  (unchanged)

---

## 6. Distribution plot label suffix

**Find:**

- `label_suffix = " (standardized)" if use_z else ""`

**Replace with:**

- `label_suffix = " (standardized)" if is_z_scale else ""`

---

## Summary

- New variables: `is_z_scale`, `var_x_label_display`, `var_y_label_display` (defined in step 1).
- All axis labels and titles that used `var_x_label` / `var_y_label` now use `var_x_label_display` / `var_y_label_display` where the plot is shown to the user.
- All checks that used `use_z` for the subtitle or suffix now use `is_z_scale` so run-profile z_ variables (with `use_z: False` in the spec) still get “(z-scored)” and “(Standardized with Z-Scores)”.
