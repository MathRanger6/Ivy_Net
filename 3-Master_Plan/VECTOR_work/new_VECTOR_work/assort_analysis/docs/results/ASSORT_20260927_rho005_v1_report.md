# Lowering assignment preference: rho one versus 0.05

**Last synced:** 2026-09-27  
**Status:** Authorized comparison completed at 50% selection and lambda four.

## What we changed and why

After the 50% selection sweep, Charles chose lambda four and asked us to lower rho to 0.05. We held the performance data, team capacities, congestion formula, penalty coefficient, and fraction selected fixed. We changed only the assignment preference parameter.

Unlike merely changing the number selected, this required forming new teams. We generated 100 assignments per season at rho 0.05 using the same incoming-player order and uniform random draws used for each corresponding rho-one assignment. This makes the comparison paired. Congestion and peer quality were then recomputed from the new teams; those changes are consequences of assignment, not additional parameter changes.

The score remained $S_i=A_i-4C_j$, followed by deterministic selection of the highest 50%. The three populations and exact slot counts remained unchanged.

## What happened

**The broad rise-and-fall profile largely gives way to a nearly flat selection profile around 50%, with a modest upper-end decline.** This appears across the three seasons. The populated central EW bins are nearly level, and the quantile charts make the broad flattening particularly clear.

In 2015 at rho 0.05, the first fifteen quantile groups have selection rates between approximately 49.7% and 50.9%; the highest group is about 46.4%. Thus the result is not perfect flatness or zero congestion effect. It is a substantial change from the strongly rising, then declining EW profile at rho one.

The realized sorting index also changes. Its mean falls from about 0.366 to 0.089 in 2014, 0.362 to 0.088 in 2015, and 0.366 to 0.087 in 2016. Rho is a preference parameter, not the sorting index itself: rho 0.05 neither means 5% sorting nor guarantees zero realized sorting. These are descriptive sorting values, not significance tests against random assignment.

## The changing range of environments is part of the answer

With little similarity preference, players spread more evenly across teams. Most team environments concentrate near the middle of the previous peer-quality range. The extremely strong and weak environments present under rho one become rare or absent.

We preserved exactly the previous EW edges in all three seasons; no extension was required. Consequently empty high-end bins are visible rather than hidden by stretching the new distribution across the whole horizontal axis. Crosses mark empty bins; they do not mean zero selection.

In 2015 at rho 0.05, EW bins 14–16 contain no players across all 100 assignments. Bin 13 contains only one player-assignment observation. At the other extreme, the 100% bar in bin 2 also represents just one observation. Neither should drive scientific interpretation.

The two central EW bins 7 and 8 instead average about 1,412 and 1,331 players per assignment. Their selection rates are approximately 50.1% and 50.5%. The main mass of the data supports the near-flat description.

The quantile bins remain similarly populated, but their numerical peer-quality boundaries change with assignment. They compare relative standing within each assignment, not identical numerical environments across rho values. The EW view is necessary here to see how the range of represented environments has narrowed.

## What this means for our question

This experiment supports assignment preference being a strong shaper of the outcome profile in this tested configuration. It changes both the mixture of individual performance across environments and the environments themselves.

It does not prove that assortativity is universally necessary for a downturn. We tested two preference settings, with the same penalty and selection fraction, and a small upper-end decline remains at the lower preference. Nor did we compare fixed individual performance bands across environments; band-of-excellence plots remain separate later work.

This was not a low-selection boundary test: selection was held near 50%. The earlier scarcity result remains distinct. Together they say that our fixed-lambda scarcity comparison retained a relative EW downturn at rho one, while reducing assignment preference at 50% strongly flattened the overall profile. They do not yet establish the interaction across every combination of rho and scarcity.

## The results

![2015 rho comparison](../../outputs/rho005_v1/2015_rho_comparison.png){width=100%}

The first two rows compare selection rates. The bottom two show player counts for each preference setting. Count panels have individually scaled vertical axes; use their numerical tick labels when comparing concentration.

- [2014 comparison](../../outputs/rho005_v1/2014_rho_comparison.png)
- [2016 comparison](../../outputs/rho005_v1/2016_rho_comparison.png)

## Verification and filing

The assignment run completed in sports_net. The first rho-one assignment in each season was reconstructed exactly as a check on seed coupling and the unchanged assignment implementation. Every new assignment preserved exact team capacities and consumed the matched ordering and uniform random inputs. Independent ranking agreed with the selected identities, and both binning methods preserved all player and winner counts. Source hashes were unchanged. All three figures were visually inspected.

- [Specification](../decisions/ASSORT_20260927_rho005_v1_specification.md)
- [Code](../../code/rho005_v1/ASSORT_20260927_rho005_v1.py)
- [Rates, counts, and occupancy](../../outputs/rho005_v1/bar_summary.csv)
- [Sorting summary](../../outputs/rho005_v1/sorting_summary.csv)
- [Run record](../run_records/ASSORT_20260927_rho005_v1_run_record.json)

**Stopping point:** No additional preference values, penalties, scarcity settings, empirical claims, or PDF regeneration followed.

