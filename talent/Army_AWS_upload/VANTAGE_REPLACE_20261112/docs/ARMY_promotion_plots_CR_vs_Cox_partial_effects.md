# Army promotion visuals — competing-risks CIF vs Cox partial effects

**For:** Vantage agents + Charles re-entry  
**Pairs with:** Cell 11 (`plot_competing_risks`) and Cell 12.6 / 12.6A (`partial_effects_plots`)

---

## Two layers, one dissertation story

| Layer | Where in 520 | Question | Peer pressure “when”? |
|--------|----------------|----------|------------------------|
| **A. Competing-risks CIF** | Cell **11** | Among officers grouped by **terminal** peer context, *when* and *how fully* does **promotion** accumulate from CPT? | **Last kept CPT quarter-end** (one x per officer) |
| **B. Partial effects (TV Cox)** | Cell **12.3** fit → **12.6 / 12.6A** plot | Holding other modeled covariates at typical values, how does **instantaneous promotion hazard** change with **quarterly** pool-relative standing? | **Every interval row** in the likelihood |

**Do not conflate:** A is **descriptive cumulative share** by fixed bin; B is **model-adjusted hazard vs level** of pool-minus-mean (often z-scored).

**Ch.3 bridge sentence:** *CIF stratifies officers by where peer context **ended**; partial effects summarize how peer context **during the CPT spell** aligns with modeled promotion hazard when it changes quarter to quarter.*

---

## Data both use (Cell 10)

- **Many rows per officer** — one per kept **quarter-end snapshot** while CPT (plus survival fields).
- Each row: own performance, **B2/B3** pool metrics, `start_time` / `stop_time`, `event` only on **last** row.
- **Open OER at quarter-end** sets SNR/RTR/pool on that row (`active_at_eval_thru` in config).

Cell 11 **collapses** to **last row** for plotting. Cell 12 **uses all rows** for the full model.

---

## Reading the CR promotion plot (Cell 11)

1. **Bin once:** last-row `z_pool_minus_mean_snr_fwd` (or configured variable) → color (e.g. 10 bins, N in legend).
2. **X:** days from **CPT DOR** (`stop_time` scale).
3. **Y at day t:** (officers in bin who promoted with `stop_time ≤ t`) / **original bin N** — step function at promotion times, **not** daily re-binning.
4. **Attrition / censor:** stay in denominator; do not add promotion steps → curves plateau below 1.

**Dissertation one-liner (B3 terminal):** *Cumulative promotion incidence from CPT, stratified on terminal-captain B3 peer relative standing (LOO SNR pool at last quarter-end), with attrition/censoring as competing risks.*

**Weakness (say it plainly):** Officers who **leave hard ponds** (e.g. division → easy unit before board) show **easy terminal peer context** but may have lived under **high** congestion earlier. CIF alone cannot recover that path.

---

## Reading partial effects (Cell 12.6)

1. **Not** time on x-axis. **X** = covariate (e.g. `z_pool_minus_mean_snr_fwd`); **Y** = **hazard ratio** vs **median** reference (line at 1 = no effect).
2. Built from **`cph_full`** after Cell **12.3** (static + **time-varying** cols).
3. **12.6A:** combined **linear + quadratic** for pool (curved joint effect).

**Not in repo as a plot:** quarterly **re-bin** CIF (each quarter new color, freeze on promote). TV Cox already uses quarterly x **inside the model**; use **12.6** for the “instantaneous peer” picture.

---

## Axis labels (B1 / B2 / B3) — `PEER_INFLUENCE_AXES_MISMATCH.md`

| Label | Column intuition (SNR forward, LOO) |
|-------|-------------------------------------|
| **B1** | Full-group mean \(T_j\) — **not stored**; reconstruct if needed |
| **B2** | `pool_tb_ratio_mean_snr_fwd` (LOO mean) |
| **B3** | `pool_minus_mean_snr_fwd` (own minus LOO mean) |

Align CR and partial-effect **plot_spec** with the axis you are claiming.

---

## Suggested figure pair for Alex

1. **CR promotion CIF** — terminal B2 or B3 (match memo choice), full sample.  
2. **12.6A combined effect** — same pool construct in the Cox model.

Same frozen feather; same `POOL_GROUPING_MODE = 'active_at_eval_thru'`.

---

## What partial effects are *not*

- Not the hand-drawn **600 officers, 120/600 by year 4** sketch **per bin** (that is CIF logic).  
- Not proof of causality; sorting and reassignment are confounds.  
- Not a substitute for **path summaries** (mean/max B3 over spell) if the story is “years in the 101st.”

---

## Code pointers (520 root)

| Artifact | Path |
|----------|------|
| Collapse + bin + CIF | `520` Cell 11 `prepare_plot_data`, `calculate_cif`, `plot_competing_risks` |
| TV Cox + partial effects | Cell 12.3 `cph_full`, Cell 12.6 / 12.6A |
| Pool grain | `pipeline_config.py` → `POOL_GROUPING_MODE` |
| Panel overlap (all snapshots) | `talent/re_entry/army_basic_plots.py` |

---

## Charles + Alex alignment (2026-11-12)

Shared understanding after CR / partial-effects pedagogy. **Not** a change to B1–B4 definitions in [`PEER_INFLUENCE_AXES_MISMATCH.md`](PEER_INFLUENCE_AXES_MISMATCH.md).

### Competing-risks CIF (Cell 11)

| Point | Agreement |
|-------|-----------|
| **Story A** | Curves show **early promotion** vs **eventual lower cumulative promotion** across terminal-peer bins (e.g. hard ponds that accelerate timing but cap attainment). |
| **Story B** | CIF logic **feeds** the cross-domain **promoted yes/no histograms** (HERO / binned promotion rates) — that layer is the **main comparative story** across Army, basketball, tenure. |
| **Limit** | **Binning on final peer pressure only** drops most of the multi-quarter path (101st → easy unit before board). **Acknowledged by both** — not dismissed, but labeled. |

**Role:** Keep CR + HERO on the **terminal B1–B3** campaign; prose states the limitation.

### Partial effects + interaction surfaces (Cell 12.6 / 12.7)

| Point | Agreement |
|-------|-----------|
| **What they show** | **Instantaneous** modeled promotion **hazard** vs **current** peer standing (quarterly x in the TV Cox fit), holding other modeled inputs at typical values. |
| **Verdict** | **Strong step in the right direction** — can **stand alone** in the dissertation. |
| **Priority** | Alex: **produce if time allows** (December bandwidth). |

### Stretch goal — cumulative peer pressure × hazard (Charles + Alex)

**Idea:** Plot **instantaneous promotion risk** against a **running cumulative peer-pressure statistic** built from **all quarters up to then** — **parallel to cumulative TB ratio** (forward cumulative own performance), but for **peer context** (B2 or B3 path-aggregate, definitional work needed).

| | |
|--|--|
| **Why** | Bridges “final bin only” CIF and “current quarter only” partial effect — honors **path** without re-binning CIF every quarter. |
| **Status** | **Not implemented** in 520 today. **Ideal if December time allows** — both judge it **high impact** for Ch.3. |
| **Engineering** | Likely new column(s) per officer-quarter (cumulative mean/max of LOO pool or minus-mean) + new plot spec or exported series for hazard overlay — **spec before code**. |

---

## Revision log

| Date | Note |
|------|------|
| 2026-11-12 | Authored from Charles + CODA thread (CIF pedagogy, 101st sorting, ship-shape bundle) |
| 2026-11-12 | Charles + Alex alignment: CR/HERO role, partial effects priority, cumulative peer-pressure × hazard stretch goal |
