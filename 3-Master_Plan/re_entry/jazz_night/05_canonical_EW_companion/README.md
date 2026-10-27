# Equal-width companion to the locked naïve plot

**Last synced:** 27 October 2026.  
**Status:** JN-01 (Q16) accepted by Charles and locked. JN-01-EW version 1 is ready for review as an early explanation of binning.

![Same canonical population in 16 equal-width bins](naive_PPM_EW16_2009_2021.png)

This companion uses exactly the same 22,795 players, 615 ever-drafted outcomes and standardized PPM values as the locked 2009–2021/final-PS quantile starter. Only the bin assignments change. Sixteen intervals cover the full observed range −2.719 to 6.114; each is approximately 0.552 standardized PPM units wide. No data are clipped or discarded.

Quantile bins contain 1,424 or 1,425 players each. Equal-width bins contain between zero and 4,472 players. For example, EW bin 14 contains two drafted out of five, producing 40%; bin 15 is empty and has no rate; bin 16 contains one player and no draft. The EW display uses 0–50% so every observed rate is visible. Upward triangles flag intervals extending beyond 50%; complete intervals remain in the CSV. Bins with fewer than 30 observations are hatched.

The count strip explains why the two displays look different. A quantile bin number and an EW bin number do not denote the same performance interval. The final quantile bin spans roughly 1.717–6.114 standardized PPM and contains 1,424 players; the final EW bin spans 5.562–6.114 and contains one.

[Same-scale Q/EW comparison](naive_PPM_Q16_vs_EW16_same_scale.png) uses 0–50% on both panels, with unchanged Q counts and rates. The locked standalone Q figure retains its accepted 0–20% display; it has not been overwritten.

The PNG and SVG are the EW figure; the paired PNG supports comparison. Counts, memberships, source hash and validation are saved alongside them. Both figures retain pointwise Wilson intervals without college-clustering adjustment. No new model, filtering, or significance test was introduced.
