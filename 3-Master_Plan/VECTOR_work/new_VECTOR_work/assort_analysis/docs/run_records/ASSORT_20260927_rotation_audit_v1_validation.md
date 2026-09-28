# Rotation audit version one: validation record

**Status:** Computationally verified within the available repository and saved source checks; September 27, 2026. This is validation of the bounded construction and arithmetic, not a causal validation or a complete independent audit of every ESPN game record.

The exact executed driver, frozen input, two source-recovery overlays, parameters, Python/library versions, and SHA-256 checksums are saved in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json`. All five listed output files were present and their checksums matched that run record. The two source-recovery overlay checksums also matched. No shared source or historical output file was written by the driver.

Independent checks performed on the saved player and team tables:

- All 4,267 eligible player identifiers are unique and belong to 351 teams; team roster counts sum to 4,267.
- The accepted points-per-minute standardization has numerical mean zero and population standard deviation one.
- The team table's below-five counts sum to 339, and qualifying plus nonqualifying eligible-minute shares sum to one for each team.
- Six focal rows, spread across the saved athlete ordering, had their full and restricted leave-one-out peer means recomputed directly from their team's player rows. Both saved values matched in every spot check.
- Every full peer count is at least eight, every restricted peer count is at least seven, and there are no zero- or one-peer cases.
- Eighteen eligible players have at least one agreed fallback row; their omitted source points sum to 33. Across all 2015 source rows, 22 fallback rows carry 42 points. The source recovery supplied positive minutes for the other 15 of the 37 originally anomalous rows.
- The canonical-team change file contains two candidate rows for each of four changed athletes, with old and new selections matching the incidence summary. Three of those four meet the twenty-minute player floor under the new choice.

The compressed player comparison contains two identical team-name columns, suffixed `_x` and `_y`, because the player and team summaries were joined. Their equality was checked across all rows. This is a display duplication only; team identifiers, calculations, and counts do not depend on either name column.

The computation did not estimate draft rates, redraw the empirical outcome curve, recalculate the sorting index, run an assignment simulation, or choose a higher playing-time threshold. Independent source boxes could not establish positive minutes for the 22 fallback rows, so the report explicitly states the accepted omission rather than presenting those minutes as observed zeros or imputed values.
