# Story starter: canonical naïve PPM plot, reproduced

**Last synced:** 27 October 2026  
**Role:** Figure JN-01 version 1 in the standalone manuscript progression. **LOCKED by Charles on 27 October 2026.** Data reproduction verified; accepted image unchanged. The EW companion is stored separately in `../05_canonical_EW_companion/`.

![Canonical own-performance result in the Jazz night format](canonical_naive_PPM_Q16_2009_2021.png)

## What this reproduces

The saved Pass A own-performance plot uses 2009–2021, all eligible colleges, PPM standardized within season, final eligible observed records, and 16 equal-count quantile bins. The population contains 22,795 unique players, 615 ever drafted. We reproduced every original bin count, draft rate, mean performance and median performance from the frozen player-level source, matching the saved canonical CSV to numerical tolerance 1e-12. The highest bin contains 228 drafted players out of 1,424 (16.01%).

The new presentation uses a 0–20% vertical scale, percentage labels, player/draft counts, and pointwise 95% Wilson intervals. The original plot had no displayed intervals. These are additions to the display, not changes to the original bar heights. The inherited incorrect teammate-axis footer has been replaced with own-performance metadata. PPM is not clipped; no exponential or other model is fitted.

This step intentionally returns to the canonical 2009–2021/Q16 result after the earlier Jazz 2011–2021/Q8 experiments. It changes both window and bin count to recover the chosen historical anchor; it is not a one-variable sensitivity comparison.

## Format we can reuse

Keep the title and metadata hierarchy, observed-data color, percentage axis, count strip, and explanatory footer. `plot_style.json` holds display settings separately from the verified data. The PNG is high resolution; the SVG is a scalable alternative. Both describe the same result.

Future model predictions can be summarized in these saved bins and compared with the observed rates. Shared figures should use common numerical definitions and axis scales when compared directly. If later results require a different scale, binning, or layout, record the reason and revise the affected figure set consistently. The current 20% ceiling is not a constraint on future model predictions, which may require a larger range. Never silently hide model values to preserve the display.

## Exact records

`source_canonical_ability_bins.csv` preserves the original saved summary. `canonical_bin_counts.csv` adds integer draft counts, performance ranges, and intervals. `canonical_player_membership.csv.gz` records every player and bin. `provenance.json` records source hashes, settings, and the reproduction check. `validation.txt` summarizes the checks. The script is local and reproducible; it does not change the sources or manuscript.

See [JN_progression.md](../JN_progression.md) for the intended story and lock status, and [the running walkthrough](../Jazz_Night_Experimental_Walkthrough.md) for the exploration history.
