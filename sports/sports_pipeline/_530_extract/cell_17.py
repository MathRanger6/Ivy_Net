# =============================================================================
# CELL 17: Export modeling table for downstream notebooks (BPM merge, etc.)
# =============================================================================
# Writes the post-LOO frame `g` (perf, poolq_loo, poolq_sq, Y_draft, identifiers, …).
# bpm_merge_to_530 expects athlete_display_name on the panel: that column must exist in `g`
# (it flows through from agg if it was present after the aggregation cell).

out_path = os.path.join(OUT_DIR, "player_season_panel_530.csv")
if "g" in dir():
    g.to_csv(out_path, index=False)
    print("Wrote:", out_path)
else:
    print("Run panel cells first.")