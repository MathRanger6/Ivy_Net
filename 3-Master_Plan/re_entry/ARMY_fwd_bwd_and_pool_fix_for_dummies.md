# Army OER forward vs backward — and why pool sizes look wrong

**Last synced:** 2026-09-20

**Audience:** Charles (re-entry after ~1 year away from the 520 pipeline code)

**Standalone:** Explains what `_fwd` and `_bwd` mean in the talent pipeline, which mode is used for own performance vs senior-rater pools in Run 1, why panel 6 pool sizes can exceed ~50, and a recommended fix — without opening the notebooks.

---

## 0. One-sentence version

**Forward (`_fwd`)** = “what OER history is **known by** this snapshot date.” **Backward (`_bwd`)** = “which OER **rating window is active** on this snapshot date.” Run 1 uses **forward for the officer’s own top-block ratio and for pool comparisons**, but uses **backward to pick *who* is in the senior-rater pool** — and then groups poolmates on **calendar snapshot day**, which is too coarse and inflates pool size.

---

## 1. The two clocks you are always juggling

Every officer row in the pipeline is tied to two different timelines:

| Timeline | What it is | Example column |
|----------|------------|----------------|
| **HRC snapshot date** | A fixed day on the personnel system clock (`snpsht_dt`) | 2018-03-31 |
| **OER rating period** | Start and end of one evaluation (`eval_strt_dt` … `eval_thru_dt`) | 2017-10-01 … 2018-09-30 |

An OER row in the raw file always has a **senior rater** (`snr_rater`) — that person is the SNR for **that evaluation period**, not necessarily “everyone this general ever rated.”

Cell 4 (`assign_oer_to_snapshots_fast`) stamps **both** forward and backward OER information onto every snapshot row. Cell 5–6 build **pools** from those stamps. Run 1 Cox/HERO mostly use the **`_fwd`** performance columns, but pool **membership** keys off **`snr_rater_bwd`**.

---

## 2. Forward vs backward — plain English

Think of one captain and one snapshot date **S**.

### Forward (`_fwd`) — “last completed OER as of S”

**Rule:** Find the most recent OER whose **through date** (`eval_thru_dt`) is **on or before** S.

**Intuition:** “As of this snapshot, what is the **latest finished** evaluation the Army has on file?”

**Simple example**

| Snapshot S | Last completed OER thru date | What `_fwd` sees |
|------------|------------------------------|------------------|
| 2018-03-31 | 2017-09-30 (done) | That OER’s rater, SNR, boxes |
| 2018-03-31 | *(none yet)* | Missing — officer not yet evaluated |

**Used for:** cumulative top-block counts and **`tb_ratio_fwd_snr`** — the officer’s **own** performance track record **as known at** S.

**Code:** `merge_asof` with `direction='backward'` on `eval_thru_dt` → columns like `snr_rater_fwd`, `eval_thru_dt_fwd`, `tb_ratio_fwd_snr`.

---

### Backward (`_bwd`) — “OER window that covers S”

**Rule:** Find an OER where **start ≤ S ≤ through** (snapshot falls **inside** the rating period). If S is before the period starts, fields are cleared.

**Intuition:** “On this snapshot date, which **active rating cycle** am I in?”

**Simple example**

| Snapshot S | OER window | What `_bwd` sees |
|------------|------------|------------------|
| 2018-03-31 | 2017-10-01 – 2018-09-30 | SNR and rater **for that cycle** |
| 2018-03-31 | 2018-10-01 – 2019-09-30 *(not started yet)* | Missing (S before `eval_strt_dt`) |
| 2018-03-31 | 2016-10-01 – 2017-09-30 *(already closed)* | Not this window — forward might still use it |

**Used for:** **`snr_rater_bwd`**, **`eval_strt_dt_bwd`**, **`eval_thru_dt_bwd`** — *who is rating me in the cycle that covers today?*

**Code:** `merge_asof` with `direction='forward'` on `eval_thru_dt`, then mask to the window → columns like `snr_rater_bwd`, `eval_thru_dt_bwd`.

---

### Naming trap (read this twice)

In **`pipeline_config.py`**, the words “forward” and “backward” describe **two different merge strategies**. They do **not** mean “forward = future” in everyday speech.

| Config label | Column suffix | Merge idea |
|--------------|---------------|------------|
| `TB_ASSIGNMENT_MODE = 'forward'` | `_fwd` | Last **completed** eval through S |
| “backward assignment” in code comments | `_bwd` | Eval **window covering** S |

You remembered correctly: **one mode for “my OER history” and another for “which rating pool am I in.”**

---

## 3. What Run 1 actually uses (today)

Defaults in `pipeline_config.py` + `pipeline_config_17_1.py` (Run 1):

```text
TB_ASSIGNMENT_MODE_SELF  = 'forward'   →  tb_ratio_fwd_snr, z_tb_ratio_fwd_snr
TB_ASSIGNMENT_MODE_POOL  = 'forward'   →  pool_minus_mean_snr_fwd, z_pool_minus_mean_snr_fwd
```

So in **Run 1**:

| Concept | Forward or backward? | Column(s) |
|---------|----------------------|-----------|
| **Own performance (Â)** | **Forward** | `tb_ratio_fwd_snr` → `z_tb_ratio_fwd_snr` |
| **Pool comparison (LOO)** | **Forward** (peer ratios) | `pool_minus_mean_snr_fwd` → `z_pool_minus_mean_snr_fwd` |
| **Who is my senior rater for pooling?** | **Backward ID** | `snr_rater_bwd` |
| **Pool size on BDP panel 6** | Forward suffix, backward key | `pool_size_snr_fwd` grouped by `(snpsht_dt, snr_rater_bwd)` |

That last row is the subtle part you half-remembered:

- **Peer performance** in the pool mean is **`tb_ratio_fwd_snr`** (forward).
- **Pool roster key** is **`snr_rater_bwd`** (backward SNR person ID).
- **Pool roster also requires same `snpsht_dt`** — every officer in the cohort on that **calendar snapshot day** who shares that SNR ID.

Cell 5 calls this explicitly:

```python
add_pool_means_and_sizes(
    ...
    rtr_col='rtr_rater_bwd',
    snr_col='snr_rater_bwd',           # ← pool membership key (backward)
    ratio_snr_fwd_col='tb_ratio_fwd_snr',  # ← value averaged in pool (forward)
    ...
)
```

**512 OER ingest** still drops rows with no `snr_rater` — that part is fine. The pool-size issue is **not** “we forgot to drop null SNRs”; it is **how we define “same pool” after that.**

---

## 4. Tiny story — three officers, one general

General **G** is senior rater on several OERs. Captains **A**, **B**, **C** all have `snr_rater_bwd = G` on snapshot **2018-03-31**, but:

- **A**’s active window: FY17 cycle (thru 2017-09-30) — backward match might be FY18 cycle depending on dates  
- **B** and **C** share the **same** FY18 window (thru 2018-09-30)

Under **current code**, if all three rows show `snr_rater_bwd = G` on **2018-03-31**, they land in **one pool**:

```text
Pool key = (snpsht_dt = 2018-03-31, snr_rater_bwd = G)
Pool size = count of officers with valid tb_ratio_fwd_snr in that bucket
```

Army reality: G’s **FY18 rating pool** might be ~15 officers in one chain — not every captain in the entire dataset who ever shows G on a March snapshot.

That is why **`pool_size_snr_fwd` can be 100+** while HRM’s `snr_rater_rates_this_grd` on the OER row is often ~12–25.

---

## 5. What your probe just showed (2026-09-20 AWS)

| Measure | Median | 95th pct | Max | Share > 50 |
|---------|--------|----------|-----|------------|
| **Computed** `pool_size_snr_fwd` (last snapshot) | 23 | 79 | 264 | 19.1% |
| **Official** `snr_rater_rates_this_grd` (OER rows) | 12 | 56 | *(bad sentinel)* | 6.4% |
| **Alt** count by `(snr_rater_bwd × eval_thru_dt_bwd)` | 4 | 33 | 766 | 2.7% |

**How to read this**

1. **Official field** — Your “pools aren’t bigger than ~50” instinct matches **p95 = 56** on real OER rows. Median **12** is plausible. Ignore absurd max (7e9) until filtered — data quality issue, not your code.

2. **Computed pool** — **Too fat.** Median 23 and long tail above 50 = snapshot×SNR grouping is **not** the Army rating pool.

3. **Alt grouping** — Adding **`eval_thru_dt_bwd`** to the pool key shrinks counts toward Army-like scale (median 4, p95 33). Still some monsters (766) — next refinement may need **`eval_strt_dt_bwd`** too, or UIC — but direction is clear.

**Conclusion:** Not a transcription bug; a **pool definition** bug. LOO and Cox pool context built on the fat pools are **methodologically soft** until re-keyed.

---

## 6. What each pipeline stage uses (cheat sheet)

| Stage | Forward? | Backward? | Notes |
|-------|----------|-----------|-------|
| **512** OER clean | — | — | Drop null `snr_rater`; raw OER rows |
| **Cell 4** merge | Builds **both** `_fwd` and `_bwd` columns | Same | Every snapshot gets both stamps |
| **Cell 5** pool mean/size | **`tb_ratio_fwd_snr`** in pool mean | **`snr_rater_bwd`** + **`snpsht_dt`** for group | Mixed — this is the design choice |
| **Cell 6** pool ranks/z | Same as Cell 5 | Same | |
| **Run 1 Cox** | **`z_tb_ratio_fwd_snr`**, **`z_pool_minus_mean_snr_fwd`** | `snr_rater_bwd` exported for overlap plots only | Model does not include SNR ID as covariate |
| **HERO / BDP panel 6** | `pool_size_snr_fwd` | Overlap uses `snr_rater_bwd` | Panel 6 histogram = forward size, backward key |

---

## 7. Alex slide — pool at OER write time

**Your theory (correct):** When COL Baker writes CPT Gates’s OER, he compares Gates to **every captain he is senior-rating at that moment** — not alumni, not everyone who ever shared his SNR ID on a quarterly HRC snapshot.

### Slide cast (2-101 Brigade)

| Person | Role | Pool relevance |
|--------|------|----------------|
| COL Baker → COL Garrett | Senior rater | Pool identity changes at SNR turnover |
| CPT Prince, Gates | Same battalion captains | Usually in pool together while both under Baker/Garrett |
| CPT Girvan | Different battalion, same brigade SNR | In pool until he leaves (Sept 2020) |
| CPT Strogatz | Replaces Girvan | In pool from Sept 2020 onward |

### Gates’s 2nd OER (June 2021, SNR change)

| Captain | In pool for Gates? | Why |
|---------|-------------------|-----|
| Prince | Yes | Still in command |
| Gates | Yes (self → LOO excludes) | Ratee |
| Girvan | **No** | Left Sept 2020 — superstar should **not** affect this OER |
| Strogatz | Yes | Current peer under Garrett |

**Anchor time T** = end of Gates’s rating period (`eval_thru_dt`) ≈ June 2021.  
**Peer rule:** same SNR **and** officer *j*’s OER window **covers T**.

Current code uses **HRC snapshot day** instead of **T**, and groups too coarsely — that is the gap between your slide and Cell 5 today.

---

## 8. Recommended fix — now implemented as a toggle

**One line in `pipeline_config.py`** — no code surgery to revert:

```python
POOL_GROUPING_MODE = 'legacy'              # original pipeline
# POOL_GROUPING_MODE = 'active_at_eval_thru'  # Alex slide / OER write time
```

### Modes

| Mode | Pool membership rule | When to use |
|------|---------------------|-------------|
| **`legacy`** | `snpsht_dt × snr_rater_bwd` | Default; reproduces all prior runs |
| **`rating_window`** | `snpsht_dt × snr_rater_bwd × eval_strt_bwd × eval_thru_bwd` | Intermediate; splits staggered windows on same snapshot |
| **`active_at_eval_thru`** | Peers whose window **covers `eval_thru_dt_bwd`** (same SNR) | **Matches your slide** — pool at OER completion |
| **`active_at_snapshot`** | Peers whose window **covers `snpsht_dt`** | Panel-time “who SNR rates now” each snapshot |

**Unchanged in all modes:** own performance and pool comparison values still use **`tb_ratio_fwd_snr`** (forward).

### How to test / revert

1. Edit `talent/talent_pipeline/pipeline_config.py` → set `POOL_GROUPING_MODE`.
2. Re-run **520 Cell 5 → 11** (feather), then BDP / HERO / Cox.
3. Run `python -u talent/re_entry/army_pool_size_probe.py` — prints active mode + pool-size stats.
4. Something breaks? Set back to `'legacy'` and re-run Cell 5 onward.

**Note:** `CELL6_POOL_RANKS` must stay **False** when using `active_at_*` modes (ranks not implemented for those yet; Run 1 does not need them).

---

## 9. Option A (rating_window) — intermediate step

**Change in Cell 5** (`add_pool_means_and_sizes` — now `POOL_GROUPING_MODE='rating_window'`):

```text
OLD pool key:  (snpsht_dt, snr_rater_bwd)
NEW pool key:  (snpsht_dt, snr_rater_bwd, eval_strt_dt_bwd, eval_thru_dt_bwd)
```

**Keep unchanged (for Run 1):**

- Own performance: **`tb_ratio_fwd_snr`** / `z_tb_ratio_fwd_snr`
- Pool comparison values: still average peers’ **`tb_ratio_fwd_snr`** (forward ratios in the same true rating pool)
- Pool membership ID: still **`snr_rater_bwd`** (backward SNR — correct for “who is rating this cycle”)

**Why this is the right first fix**

- Probe already shows p95 drops from **79 → 33** with only `eval_thru_dt_bwd` added.
- Minimal conceptual change: “pool = SNR’s officers in **this** OER cycle,” not “everyone on March 31 with the same SNR person somewhere in their file.”
- Matches Army `snr_rater_rates_this_grd` scale much better.

**Simple before/after example**

| Officer | snpsht_dt | snr_rater_bwd | eval_thru_dt_bwd | OLD poolmates | NEW poolmates |
|---------|-----------|---------------|------------------|---------------|---------------|
| A | 2018-03-31 | G | 2018-09-30 | All {A,B,C,…} on 2018-03-31 with G | Officers with G **and** thru 2018-09-30 |
| D | 2018-03-31 | G | 2017-09-30 | Same huge bucket as A | **Different, smaller** bucket |

---

### Option B (config-only experiment): Set `TB_ASSIGNMENT_MODE_POOL = 'backward'`

This switches pool **column names** to `pool_minus_mean_snr_bwd` etc., averaging **`tb_ratio_bwd_snr`** within pools. That is a **different scientific question** (“LOO within active-window ratios”), not the same as fixing pool **membership**. **Do not confuse with Option A.** Option A fixes *who is in the pool*; Option B changes *which performance number is compared*.

---

### Option C (later): Add UIC or rating unit to the pool key

If Option A still leaves tails (max 766 in probe), add `oer_uic_pde` or `snr_rater_asg_uic_pde` from OER. Army pools are often “SNR + unit + cycle.” Defer until Option A is implemented and re-probed.

---

## 10. Implementation checklist (after flipping the toggle)

1. Set `POOL_GROUPING_MODE` in `pipeline_config.py`.
2. Re-run **520 Cell 5 → 11**; then BDP / HERO / overlap scripts.
3. Run `army_pool_size_probe.py` — compare computed vs official vs simulated `active_at_eval_thru`.
4. Spot-check a known SNR cohort (e.g. brigade slide example) at one `eval_thru_dt`.

**Do not** need to re-run 512 unless OER clean rules change.

---

## 11. What you can tell Alex (one paragraph)

“We model pool standing the way senior raters actually work: at OER write time, compare the ratee to captains they are senior-rating then — not everyone who ever shared their SNR on a quarterly snapshot. Forward top-block ratio is the performance measure; backward SNR identifies the rater chain. We added a config toggle (`POOL_GROUPING_MODE`) so we can switch from legacy snapshot×SNR pools to event-anchored peers at `eval_thru_dt` and revert instantly if downstream models misbehave.”

---

## 12. Files to keep handy

| File | Role |
|------|------|
| `talent/talent_pipeline/add_cum_oer_metrics_mod_working.py` | Forward/backward merge + `add_pool_means_and_sizes` |
| `talent/talent_pipeline/pipeline_config.py` | `TB_ASSIGNMENT_MODE_SELF` / `_POOL` |
| `talent/talent_pipeline/520_pipeline_cox_working.ipynb` | Cells 4–6 |
| `talent/re_entry/army_pool_size_probe.py` | Before/after probe |
| `talent/re_entry/army_basic_plots.py` | Panel 6 pool size histogram |

---

## 13. Parked until after fix

- Pool interval overlap panel (`snpsht_dt × snr_rater_bwd`) — update grain to match new pool key.
- HERO / Cox Run 1 — re-estimate after new LOO; coefficients may shift.
- Official `snr_rater_rates_this_grd` — add filter (e.g. 1–200) before validation plots.

---

*Thread log: 2026-09-20 — probe diagnosis; Alex slide section + `POOL_GROUPING_MODE` toggle in Cell 5.*
