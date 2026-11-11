# Peer influence axes — cross-domain mismatch (B1 vs B2)

**Last synced:** 2026-11-10

**Audience:** Charles → COMPASS (all domains); backup for Ch.3 empirics alignment.

---

## Introduction — we think we have a problem

Across the dissertation we want the **same story in every domain** (Army, tenure, sports, etc.): first show how **your own performance** relates to the outcome, then show how **peer / group context** relates to the outcome. Charles has been treating those second plots as comparable “HERO” or “group talent” figures everywhere.

**We now believe the second plot does not use the same quantity on the horizontal axis in every domain.** On **Army Run 1**, the promotion bars and HERO script bin officers on **how far you sit above or below your peers** (your TB ratio **minus** the leave-one-out average TB in your peer pool). In **other domains**, Charles recalls binning promotion on **the strength of the peer group itself** (the pool average, or LOO pool mean)—**not** the gap between you and that average.

Those are different scientific questions:

- “**Was I rated in a strong or weak peer group?**” (pool level)
- “**Was I better or worse than the peers I was stacked against?**” (you minus pool)

We had already argued about **how to define the peer pool** (snapshot × senior rater vs rating-window rules). This memo is about a **separate** choice: whether the x-axis for the second figure is **pool level** or **individual minus pool**. Army’s current code and March export figures use **minus pool**; other mosaics may use **pool level only**. If we publish both without one rule, the cross-domain chapter reads as if the same label meant different things.

**What this memo does:** spells out the two options (B1 and B2 below), what the **Mac repo** says we *intend*, what the **March AWS export** actually ran, and the **fast checks** on Army data to see whether we can align everyone on pool level (B1) without losing the strong Army gradient—or whether we must rebalance other domains to minus-pool (B2).

**What we need from COMPASS:** After reading **Roster pressure (ideal target)**, **Fast Army checks**, and **Decision to lock**: (1) recommend **one** rule for the second figure in **all** domains for the **near-term** chapter (B1 vs B2); (2) advise whether **roster pressure (B3)** is the right **long-term** standard and what operational definition to use in Army, tenure, and sports; (3) say whether the Army March result is still an acceptable “hero” plot under the near-term rule.

**Notation (for the rest of the memo):** \(\hat{A}_i\) = own performance (e.g. forward SNR TB ratio); \(\hat{T}_j^{\mathrm{LOO}}\) = leave-one-out mean of peers’ TB in the same pool; **B1** = bin on \(\hat{T}_j^{\mathrm{LOO}}\); **B2** = bin on \(\hat{A}_i - \hat{T}_j^{\mathrm{LOO}}\); **B3** = bin on **roster pressure** (domain-specific operationalization below).

---

## Shared goal (all domains)

- **Figure A (naive):** \(P(Y_i{=}1)\) binned vs **own performance** \(\hat{A}_i\).
- **Figure B (“group talent” / HERO):** \(P(Y_i{=}1)\) binned vs **one** agreed pool construct — **not yet locked the same way across domains**.
- **Figure B (ideal, not yet unified):** **Ideally** Charles would **rerun every domain** with the **same conceptual x-axis — roster pressure** — because we **suspect** it best captures **negative peer-group effects** (competition for scarce advancement slots), not only “how good was the pool” (B1) or “how far above the pool mean am I” (B2). **That suspicion is not yet tested** domain-by-domain on a common definition.

---

## Three options for Figure B (near-term vs ideal)

| Option | Plain language | Typical operationalization | Question it answers |
|--------|----------------|---------------------------|---------------------|
| **B1 — Pool level** | Average strength of peers | LOO peer **mean** \(\hat{T}_j^{\mathrm{LOO}}\) (Army: `pool_tb_ratio_mean_snr_fwd`) | “How strong was my peer pool?” |
| **B2 — Relative standing** | You minus peer average | \(\hat{A}_i - \hat{T}_j^{\mathrm{LOO}}\) (Army: `pool_minus_mean_snr_fwd`; March HERO uses z-scored B2) | “How far above/below LOO peers am I?” |
| **B3 — Roster pressure (ideal)** | Congestion / how much rival quality competes for the same scarce slots | **Model-aligned:** congestion term \(C\) in \(S_i = A_i - \lambda C\) (Levine–Gates draft: credible competitors, crowding). **Sports (partial):** LOO **sum** of teammate quality (`congestion_crowding`, legacy `poolq_loo` paths) vs LOO **mean** (`congestion_quality`). **Army / tenure:** **not** a single shared column named `roster_pressure` in production pipelines yet — would need an explicit build (e.g. LOO sum of peer TB in SNR pool, or model-specified \(C\)). | “How **crowded** is the roster I’m competing on?” (emphasis on **selection pressure**, not prestige or relative rank alone) |

**Assuming** `POOL_EXCLUDE_SELF = True` on Army: \(\hat{T}_j\) in **`pool_tb_ratio_mean_*`** is the **LOO peer mean**, not a mean that includes self. “LOO vs \(\hat{T}_j\)” is **how the mean is built**, not a separate axis beside B1/B2/B3.

**Charles’s working hunch (tabled in intro writing, now reopened for empirics):** peer **mean** (B1) and **minus mean** (B2) were convenient reduced-form axes; **roster pressure (B3)** may be the construct that matches the **selection-channel** story (peers help development / hurt when they compete for the same promotion). **We need to see if that is true** — i.e. whether B3 bins produce a **clear, comparable** \(P(Y{=}1)\) pattern across Army, tenure, basketball, and other cases, and whether B3 **beats or complements** B1/B2 on the current Army March feather and on refits elsewhere.

---

## Roster pressure (ideal target) — what a full rerun would mean

**Goal:** One **named** second figure in every domain: \(P(Y{=}1)\) vs **roster pressure**, with a **written mapping** from domain data to the same idea (congestion / competitive thickness of the pool).

**Assuming** we adopt the model chapter’s congestion layer as the conceptual anchor: roster pressure is **not** identical to B1 (pool mean can rise from prestige without more direct competitors) and **not** identical to B2 (relative standing mixes own \(\hat{A}_i\) with pool level). B3 foregrounds **how much peer quality is in the assignment competing for the outcome**.

**Implementation status (repo snapshot, 2026-11-10):**

| Domain | Closest existing variables | Rerun “roster pressure” figure? |
|--------|----------------------------|-------------------------------|
| **Sports** | `congestion_crowding` (LOO **sum**), `congestion_quality` (LOO mean), `poolq_loo` | **Partially** — Tier 1 notebook path exists; must **choose** sum vs mean as B3 proxy and align binning with Army |
| **Army** | B1/B2 in `df_pipeline_11`; **no** standard `roster_pressure` column | **Needs build + 520 rerun** (e.g. LOO sum of `tb_ratio_fwd_snr` in SNR pool, or model \(C\) from sigmoid relevance — **definition TBD with COMPASS/Alex**) |
| **Tenure** | **Assuming** mosaic used pool-level LOO; roster-pressure analog **not** verified in this memo | **Needs audit + new variable** |
| **Other** | Case-by-case | Same pattern |

**Empirical test plan (ideal, cross-domain):**

1. Fix **one operational definition** of roster pressure per domain (document in one table).
2. Rerun **Figure A** (\(\hat{A}_i\)) unchanged.
3. Rerun **Figure B** as \(P(Y{=}1)\) vs **B3** (same binning rules: EW8, cohort filters, last-observation grain where applicable).
4. **Compare** B3 to B1 and B2 **on the same sample**: monotone promotion gradient? inverted-U? domain-specific shape?
5. **Only then** retire or demote B1/B2 in print, or keep B1/B2 as robustness panels.

**Assuming** time and PDE export constraints: **near-term** chapter may still ship B1 or B2 on some domains while B3 is validated; this memo asks COMPASS to say whether that is acceptable or misleading.

---

## What canonical Mac repo says (definition of record for *intent*)

**Paths:** `talent/talent_pipeline/`, `talent/re_entry/`, `pipeline_config.py`, `pipeline_config_17_1.py`

- **Figure A (Army):** `run1_cr_z_tb_ratio_fwd_snr` — **`z_tb_ratio_fwd_snr`** (`RUN_SCALE = 'z'`).
- **Figure B (Army):** `run1_cr_z_pool_minus_mean_snr_fwd` + **`army_hero_slide_plot.py`** default **`plot_var = "z_pool_minus_mean_snr_fwd"`** → **B2 (relative)**, not B1.
- **Minus-mean in Cell 5:** `pool_minus_mean = tb_ratio_fwd_snr - LOO peer mean` when `exclude_self=True`.
- **Pool membership (Cell 5):** **`POOL_GROUPING_MODE = 'active_at_eval_thru'`** in current `pipeline_config.py`, with `add_cum_oer_metrics_mod_working.py` that accepts `pool_grouping_mode` (peers under same SNR whose bwd OER window covers `eval_thru_dt_bwd`, **assuming** Cells 4–5 run through that code path).

**Assuming** Charles has **not** yet rerun 520 on PDE/Vantage with the **current** `talent/talent_pipeline/add_cum_oer_metrics_mod_working.py` + `active_at_eval_thru`, any **saved feather from an old AWS run does not automatically match** this pool definition.

---

## What downloaded export folders contain (what may have been actually plotted)

**Paths:** `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/`, `…20260421-0802/`

- **Run 1 plot *variable* (March screenshots / metadata):** still **B2** — `z_pool_minus_mean_snr_fwd`, same **17_1** logic as repo (EW8, `filter_zero_oer`, etc.). **Not** default B1 on \(\hat{T}_j\) alone.
- **Pool code inside those exports (checked in repo copies):** **`add_cum_oer_metrics_mod_working.py` without `POOL_GROUPING_MODE`** → Cell 5 uses **legacy** groups: **`snpsht_dt × snr_rater_bwd`** for forward SNR pools. **Assuming** March Run 1 was built from **20260320-1000**, the strong HERO bars are **B2 with legacy pools**, not B2 with `active_at_eval_thru`.
- **April export (`20260421-0802`):** **same legacy** `add_cum` pattern in the copy in git unless files were replaced on AWS and not synced to Mac — **assuming** no undocumented refresh, it does **not** by itself prove `active_at_eval_thru` was used for that run.

---

## Cross-domain crisis (other fields vs Army)

- **Assuming** other domains’ mosaics use **B1** (\(P(Y{=}1)\) vs **\(\hat{T}_j\)** or LOO mean **directly**), and Army Run 1 / HERO uses **B2**, the chapter mixes **“peer environment level”** vs **“peer-adjusted standing”** under one “group talent” label.
- That mismatch is **orthogonal** to legacy vs `active_at_eval_thru`: **B1 vs B2** confusion can persist even when pool definitions match.

---

## Fast Army checks (no full domain rebuild)

**Assuming** `df_pipeline_11_cox_analysis.feather` exists for March Run 1:

1. **B1 on Army:** bin promotion on **`pool_tb_ratio_mean_snr_fwd`** or **`z_pool_tb_ratio_mean_snr_fwd`** (same filters/grain as HERO: last interval per officer, EW8, min pool 3, `filter_zero_oer` unless deliberately relaxed).
2. **B2:** compare to existing **`z_pool_minus_mean_snr_fwd`** (current HERO / March bars).
3. **B3 (provisional):** **assuming** we adopt **LOO sum of peer `tb_ratio_fwd_snr`** in the same SNR pool as the first Army roster-pressure proxy, compute on the March feather (or one Cell 5 add-on) and bin the same way. **If that column does not exist yet**, this step is **blocked** until a short pipeline patch — still worth flagging for COMPASS as the intended Army B3.
4. **If B1 is still strongly monotone** → can **align other domains on B1** for a **temporary** fix (still relabel Army from B2 to B1).
5. **If only B2 stays strong** → **re-bin other domains on B2**, or **two labeled designs** in the dissertation.
6. **If B3 matches theory best** (e.g. clearest selection-pressure curve) → prioritize **full domain reruns on B3** even if B1/B2 were “good enough.”

**Assuming** a Cell 11 plot entry or `army_hero_slide_plot.py --plot-var …`, B1 and B2 can be tested in minutes on Mac from the March feather **without** rerunning 502–512; B3 may need a new computed column first.

---

## Pool-definition caveat (when rerunning matters)

| Source | Figure B variable | Pool peers for \(\hat{T}_j\) / minus-mean |
|--------|-------------------|------------------------------------------|
| March feather + export `add_cum` | B2 (as plotted) | **Legacy** `snpsht_dt × snr_rater_bwd` |
| Fresh run from **`talent/talent_pipeline/`** | B2 (config unchanged) | **`active_at_eval_thru`** (unless `POOL_GROUPING_MODE` is changed) |

**Assuming** a Vantage rerun with latest Mac code, **B1 and B2 values can both shift** vs March; the **B1 vs B2 policy choice** should be decided **on one frozen run** (export or one full 520 pass), then applied to all domains.

---

## Decision to lock (one row per domain)

| Figure | X-axis (pick and document) |
|--------|----------------------------|
| **A** | \(\hat{A}_i\) (own) — **already shared intent** |
| **B (near-term)** | **B1** \(\hat{T}_j^{\mathrm{LOO}}\) **or B2** \(\hat{A}_i - \hat{T}_j^{\mathrm{LOO}}\) — **Army repo + March plots currently B2**; **other domains, assuming Charles’s description, likely B1** |
| **B (ideal)** | **B3 roster pressure** — **same construct in all domains after operational definition + reruns**; **empirically unverified as of this memo** |

---

## One-liner for advisors / COMPASS

**Near-term crisis:** **Assuming** March Army matches `17_1`, promotion bars use **B2 (minus LOO mean)** while **assuming** other domains used **B1 (pool LOO mean)** — we need one **interim** rule and quick Army B1/B2 checks on `df_pipeline_11`.

**Ideal direction:** Charles wants to **rerun all domains** with **roster pressure (B3)** as the second-figure x-axis because it may best represent **negative peer / selection congestion**; **we need COMPASS’s advice on the operational definition and whether the data support B3 over B1/B2** before rewriting every mosaic.

---

## Related repo docs

- [`talent/documents/512_520_CELL_COLUMN_INVENTORY.md`](../../talent/documents/512_520_CELL_COLUMN_INVENTORY.md) — Cell 5 columns
- [`_DISPOSABLE_Ch3_data_empirics_thread.md`](_DISPOSABLE_Ch3_data_empirics_thread.md) — Ch.3 run-of-record
- [`ARMY_PLOT_PROVENANCE_AUDIT.md`](ARMY_PLOT_PROVENANCE_AUDIT.md) — plot file names
