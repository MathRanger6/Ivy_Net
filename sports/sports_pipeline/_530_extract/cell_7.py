# =============================================================================
# CELL 7: Draft indicator Y_draft + optional SR merge + construction of `perf`
# =============================================================================
# After this cell:
#   - agg["Y_draft"] ∈ {0,1}: ever drafted (any appearance in lookup file).
#   - agg may gain SR columns (BPM, OBPM, DBPM, ...) if matched file exists.
#   - agg["perf"] is the performance measure for LOO teammate pool + LPM (PERF_METRIC).


def _resolve_perf_metric(m):
    """Map user-facing PERF_METRIC string → (canonical_label, sr_column_or_None).

    Returns:
        (str, str | None): e.g. ("opm", "OBPM") for SR metrics, ("ppm", None) for box-only.
    """
    k = str(m).strip().lower()
    if k in ("obpm", "opm"):
        return "opm", "OBPM"
    if k in ("dbpm", "dpm"):
        return "dpm", "DBPM"
    if k == "bpm":
        return "bpm", "BPM"
    if k == "ppm":
        return "ppm", None
    if k in ("minutes", "min"):
        return "minutes", None
    raise ValueError(
        'PERF_METRIC must be "ppm", "minutes", "bpm", "opm", or "dpm" '
        f'(aliases obpm, dbpm, min), got {m!r}'
    )


_perf_label, _sr_col = _resolve_perf_metric(PERF_METRIC)
# If True, PERF_METRIC requires columns from Sports-Reference merge file.
_needs_sr = _sr_col is not None

# --- Draft outcome (v0): row-level "ever in draft lookup" ---
# Lookup is produced by sdv_second export; integer athlete_id set membership.
lu = pd.read_csv(DRAFT_LOOKUP_PATH)
drafted = set(lu["athlete_id"].dropna().astype(int))
agg["Y_draft"] = agg["athlete_id"].astype(int).isin(drafted).astype(int)
print("Drafted players in panel (any season row):", agg["Y_draft"].sum(), "/", len(agg), "rows")
print(f"Row-wise draft rate: {agg['Y_draft'].mean():.4f}")

# --- Optional left-merge of SR advanced stats (bpm_merge_to_530 output) ---
# Merge is on (athlete_id, season, team_id): same grain as agg after groupby above.
if os.path.isfile(BPM_MATCHED_PATH):
    mb = pd.read_csv(BPM_MATCHED_PATH, low_memory=False)
    key = ["athlete_id", "season", "team_id"]
    # Normalize join keys to numeric so merge doesn't miss on int vs float string issues.
    for c in key:
        agg[c] = pd.to_numeric(agg[c], errors="coerce")
        mb[c] = pd.to_numeric(mb[c], errors="coerce")
    # One row per key on SR side (merge notebook should already dedupe; safe if re-run).
    mb = mb.drop_duplicates(subset=key)
    # Bring over all non-key columns except internal flag has_bpm (redundant once BPM present).
    stat_cols = [c for c in mb.columns if c not in key and c != "has_bpm"]
    agg = agg.merge(mb[key + stat_cols], on=key, how="left")
    # Quick coverage diagnostics for the three headline SR metrics.
    for lab, col in (("BPM", "BPM"), ("OBPM", "OBPM"), ("DBPM", "DBPM")):
        if col in agg.columns:
            print(f"Merged SR from {BPM_MATCHED_PATH} — non-null {lab}: {int(agg[col].notna().sum()):,}")
elif _needs_sr:
    # Fail fast: cannot construct SR-based perf without merge output (see config two-pass note).
    raise FileNotFoundError(
        f"{BPM_MATCHED_PATH} not found but PERF_METRIC={PERF_METRIC!r} needs SR columns. "
        "For a first run through export: set PERF_METRIC to 'ppm' or 'minutes', export "
        "`player_season_panel_530.csv`, then bpm_merge (scrape jobs only) → scrape_bpm "
        "(until raw CSV exists) → bpm_merge (Match); then switch PERF_METRIC to bpm/opm/dpm."
    )
else:
    # Box-only perf (ppm/minutes): merge file is optional; LOO uses ESPN-derived columns.
    print(f"No {BPM_MATCHED_PATH} (not needed for PERF_METRIC={PERF_METRIC!r}).")

# --- Single column `perf` for all downstream cells (LOO, LPM, plots) ---
if _perf_label == "ppm":
    agg["perf"] = agg["ppm"]
elif _perf_label == "minutes":
    agg["perf"] = agg["minutes"]
else:
    # SR path: perf is the chosen advanced stat; NaN where merge did not match a player-season.
    if _sr_col not in agg.columns:
        raise KeyError(
            f"PERF_METRIC={PERF_METRIC!r} needs column {_sr_col!r} from {BPM_MATCHED_PATH}. "
            "Re-run bpm_merge_to_530 or choose ppm/minutes."
        )
    agg["perf"] = agg[_sr_col]

print(
    f"perf ← {_perf_label}"
    + (f" (SR column {_sr_col})" if _needs_sr else " (box)")
)