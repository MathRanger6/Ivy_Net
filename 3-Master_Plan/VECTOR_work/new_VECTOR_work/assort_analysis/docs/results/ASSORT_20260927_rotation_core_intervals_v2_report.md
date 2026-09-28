# High-minute rotation intervals — version two (2015)

**Status:** Executed September 27, 2026 per [mission follow-up](../scientific_questions/ASSORT_20260927_SCOUT_mission_high_minute_rotation_intervals.md). Version one preserved unchanged.

## What stayed fixed

- Accepted input: [rotation audit players](../../outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz) (SHA-256 verified).
- **4,267** players, **351** teams, saved `ability_standardized` and team labels — no re-standardization, no eligibility change.
- Top-ten rule: $k_j=\min(10,|P_j|)$ by descending season minutes; ties → ascending `athlete_id`.
- **100** within-team random-$k_j$ draws, seed **20260927**, `numpy.random.default_rng`.

## What version two corrected

1. **One random membership per draw** drives team widths, coverage curve, and $H_{\mathrm{sort}}$ for that draw (v1 used independent random streams for widths vs coverage).
2. **Headline random width:** mean of **100 draw-level mean team widths** = **3.096** (not the v1-style **3.241** mean of team medians — reported separately).
3. **Headline random coverage:** mean of **100 draw-level means over the fixed grid** = **146.67** (secondary: mean of pointwise median curve = **146.87**).

## Interval results (matched basis)

| Case | Mean team interval width | Mean coverage over fixed grid |
|------|-------------------------:|------------------------------:|
| All eligible | **3.280** | **155.40** |
| Fixed top 10 by minutes | **2.855** | **135.22** |
| Random 10 (mean of draw aggregates) | **3.096** | **146.67** |

Central overlap remains large (max coverage still **351** on the grid). Top-ten intervals are nested in all-player intervals.

**High-minute vs random-10 width:** **2.855** vs **3.096** — minutes-based selection narrows **more** than a typical random ten on the same rosters. **High-minute vs random-10 coverage:** **135.22** vs **146.67** — same direction.

## Sorting index $H_{\mathrm{sort}}$ (overall, one value per case)

Formula: player-weighted share of variance explained by team means on saved standardized season points per minute (`ability_standardized`). Cross-checked against `realized_sorting_index_H_sort` (Grandchild) and raw `points_per_minute` (affine invariance).

| Case | $N$ | $H_{\mathrm{sort}}$ | Assignment-reallocation context $(J-1)/(N-1)$ | Observed minus context |
|------|----:|--------------------:|---------------------------------------------:|------------------------:|
| **All eligible** | 4,267 | **0.06194** | 0.08204 | −0.02010 |
| **Fixed top 10 minutes** | 3,501 | **0.06742** | 0.10000 | −0.03258 |
| **Random 10 (100 draws)** | 3,501 each | mean **0.07936** (median 0.07898; range 0.0698–0.0936) | 0.10000 | — |

Full-population index matches the [sorting sensitivity report](ASSORT_20260927_sorting_sensitivity_v1_report.md) reference **0.06194** within tolerance.

**Joint read on measured PPM (not latent talent):** Fixed top-ten raises $H_{\mathrm{sort}}$ slightly above the full **0.06194**, but **random within-team tens** land **higher still** (mean **~0.079**) — and **all 100** of those draw-level indices remain below the **0.1000** analytical expectation under random *reassignment across teams* with the same 3,501-player size and team capacities (saved range approximately **0.06984–0.09359**; none reaches 0.1000). The 100 draws select players *within* observed teams; the 0.1000 value is a different operation. Neither comparison establishes a significance level or latent-talent sorting. Minutes-based selection **does not** increase sorting index relative to random ten-player subsets on the same teams; interval widths still narrow **more** than random tens because endpoints move, not only because $N$ shrinks.

## What this does not establish

- Latent talent assortativity, draft selection, congestion in the score, or that PPM equals talent.
- Significance from the 100 descriptive draws (conditional on observed rosters).

## Artifacts (v2 only)

| Role | Path |
|------|------|
| Driver | [`code/ASSORT_20260927_rotation_core_intervals_v2.py`](../../code/ASSORT_20260927_rotation_core_intervals_v2.py) |
| Figure | [`outputs/.../ASSORT_20260927_rotation_core_intervals_v2_comparison.png`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_comparison.png) |
| $H_{\mathrm{sort}}$ JSON | [`..._sorting_index_summary.json`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_sorting_index_summary.json) |
| Random membership | [`..._random_membership.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_random_membership.csv) |
| Per-draw table | [`..._random_repetitions.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_random_repetitions.csv) |
| Run record | [`docs/run_records/ASSORT_20260927_rotation_core_intervals_v2_run_record.json`](../run_records/ASSORT_20260927_rotation_core_intervals_v2_run_record.json) |

Version one: [`ASSORT_20260927_rotation_core_intervals_v1_report.md`](ASSORT_20260927_rotation_core_intervals_v1_report.md).
