# Bounded 2015 performance-measure audit: scope and reasons

**Date:** September 27, 2026  
**Authorization:** Charles approved VECTOR's proposed bounded audit with “Yessir.” That authorization covers a small predetermined identity check and a descriptive comparison of three measures on the same accepted 2015 players. It does not reopen simulation, model fitting, draft curves, source refresh, or the broader metric search.

## Question and sequence

We first checked whether existing advanced measures were available on the accepted 2015 population. Coverage was nearly complete, but the saved matching file did not have an exact construction record. SCOUT confirmed the coverage and identified the missing-record distinction. Next we will check a small sample against the existing raw Sports-Reference table, then compare season points per minute (PPM), Player Efficiency Rating (PER), and Box Plus/Minus (BPM) on exactly the same players. This tells us whether the measures describe player differences and team clustering differently. It does not identify latent talent or establish which measure best predicts selection.

The fixed starting population has 4,267 accepted players on 351 teams. Its checksum must match the saved rotation-audit execution record. Common-sample membership requires a finite PER and a finite BPM; no value is imputed and no player is removed because of an unattractive performance value. Expected common size is 4,161. Compare the full and common-sample PPM sorting index to show the effect of the sample restriction itself.

## Predetermined identity check

Select 24 players from 24 teams before calculating metric results. Rank common-sample players by the hexadecimal SHA-256 hash of the literal string `metric-identity-2015-20260927|athlete_id`, retain the first player from each distinct team, and take the first 24. This reproducible selection uses identifiers, not measured performance, minutes, draft status, or desired results.

For each, compare the accepted ESPN name and team with the saved crosswalk school slug and the normalized-name/school/2015 key in the raw Sports-Reference table. Use the documented highest-minutes rule for duplicate source keys. Preserve raw candidate counts, displayed names, school slugs, source URLs, scrape dates, source minutes, and saved versus raw PER/BPM values in the sample export. Stop before the metric comparison if a raw key is absent or either value disagrees beyond an absolute tolerance of $10^{-10}$. VECTOR will also read the displayed sample for obvious name/school problems.

This is a consistency check between saved sources. It cannot independently establish that the original website identities are correct, estimate an error rate over all 4,161 matches, or recover the exact historical matching run. Agreement with the same name-normalization procedure is not independent validation of that procedure.

## Descriptive calculations

Within the common 2015 population, standardize each measure $x$ using its own population mean and population standard deviation:

$$
z_i=\frac{x_i-\bar{x}}{\sqrt{N^{-1}\sum_i(x_i-\bar{x})^2}}.
$$

These transformations provide comparable scale units, not estimates of portable ability. Calculate raw distributions, Spearman rank correlations (correlations between player ranks), team minimum-to-maximum intervals on the standardized scale, and the sorting index ($H_{\mathrm{sort}}$):

$$
H_{\mathrm{sort}}=\frac{\sum_j n_j(\bar{x}_j-\bar{x})^2}{\sum_i(x_i-\bar{x})^2}.
$$

Every player receives equal weight in the sorting index. The reported mean interval width gives each team equal weight. Cross-check the index against one minus the within-team share of total variation and verify invariance to the common affine standardization. No random-assignment reference is run; these are descriptive indices, not excess sorting estimates or significance tests. The same players, team assignments, eligibility rules, and year are held fixed; the performance measure changes.

## Interpretation and stop rule

Higher measured sorting for PER than PPM would show that broader box production clusters differently from scoring rate among these same players. It would not prove PER is purer talent or that assortative recruiting caused the clustering. Higher sorting for BPM must be interpreted alongside its embedded team-performance adjustment. Similar sorting across measures would narrow this particular measurement explanation, without ruling out latent talent sorting. No measure wins by producing a larger sorting index or a preferred draft-outcome curve.

All new code, exports, execution records, and the narrated report stay under `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/`. Read the accepted audit, matched table, raw table, and crosswalk without modifying them. Record input/code/output hashes and verify that inputs did not change during execution. Do not overwrite older outputs. Sources, panels, pipeline code, model parameters, and older research artifacts remain intact.

One narrated report will record what we did, what it established, what it did not establish, and the smallest next decision. Further analysis requires another explicit authorization.
