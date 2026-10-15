# Panel 8 peak-to-tail comparison

Original 2011-2021 top-7% own-performance band; all eligible player-team-season observations at colleges represented by an ever-drafted player. Leave-one-out teammate averages and all 11 original bin counts were reproduced. Historical bin assignment uses right-closed intervals, including the lowest endpoint.

Peak bin 7: 36/117 = 30.7692%. Final bins 10-11 pooled: 7/51 = 13.7255%. Decline: 17.0437 percentage points.

One-sided p-values from 9,999 centered Rademacher multiplier draws, seed 46:

- No grouping or peak correction: 0.0040.
- Grouping only: 0.0011.
- Nine-location peak correction only: 0.0242.
- Both: 0.0081.

The grouped standard error is 5.7094 percentage points, compared with 6.4389 under row independence. Grouping can increase or decrease variance of a difference. Both-adjustment simultaneous one-sided 95% lower bound is +3.3770 percentage points. These are approximate, exploratory results, conditional on the original population, bins, and fixed final-two-bin tail. They do not correct historical choices of panel, years, performance band, or binning, and do not establish causality or the whole inverted-U shape.

The tail has 51 records, 50 distinct people, seven drafted people and 21 connected college groups. Only seven colleges supply its drafted observations. Sparse outcome support can affect the bootstrap approximation. The final bin alone has nine records and one drafted observation.

Two player-seasons in the full population have records at different colleges. They are retained to reproduce the original curve and connected in the grouped analysis; their source identities remain for review. Neither duplicated player-season occurs in peak bin 7 or tail bins 10-11. Grouping OFF treats every source row as independent, even repeated observations of a person.

Notebook: Section 4C of PD46_Draft_Rate_Comparisons.ipynb. RUN_PANEL8_TEST controls reruns. No manuscript changes.
