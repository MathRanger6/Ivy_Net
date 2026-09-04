# Tenure hero pipeline — MBB mirror (use existing panel first)

**Last synced:** 2026-09-02

**Audience:** Charles + COMPASS (Mac analysis).

**Standalone:** Step-by-step map from rsync’d `faculty_panel_with_pools.jsonl` to tenure HERO plots, mirroring MBB post–re-entry work without re-scraping.

**MBB analogue doc:** [`../MBB_empirical_roster_select_replay.md`](../MBB_empirical_roster_select_replay.md)

---

## Side-by-side ladder

| Rung | MBB (done or in progress) | Tenure (this campaign) |
|------|----------------------------|-------------------------|
| **Data spine** | MBB panel CSV / exports | `faculty_panel_with_pools.jsonl` |
| **Pass A HERO** | `pass_a_empirical_bundle.py` → `sports_sandbox/hero/` | `tenure_pass_a_hero.py` → `tenure_sandbox/hero/` |
| **Pass A F-HERO** | `pass_a_congestion_conditional.py` → `fhero/` | **Act II** — T̂_j at fixed Â (pending lock) |
| **ρ / H_sort** | Reigning hero calibration; ρ* ≈ 0 → park for MBB | **Act III** — run diagnostic; park only if flat |
| **Generative replay** | `reigning_hero_sim_hero.py` | **Act IV** — after Alex lock |
| **Scrape / expand** | Box QC, min20, mg10 | **Parallel** — PEER on Rivanna when scheduled |

---

## PD29 delta (Sep 2, 2026) — Alex locks vs v0

**Source:** [`transcripts/PD29_notes.md`](../../../../transcripts/PD29_notes.md) — Charles showed **dirty porch** same call; Alex approved assortment direction, then tightened tenure mechanics.

| Dimension | **v0 (this doc, Sep 1)** | **PD29 lock (exploratory → next build)** |
|-----------|----------------------------|------------------------------------------|
| **Unit of analysis (HERO row)** | One row per **person** (ASST-PS mean peer LOO) or **last assistant year** on some runs | One row per **decision event** (~assistant **year 5–6** with tenure or out signal) |
| **Own Â** | ASST-PS mean **pubs/year** over assistant years; LAST-PS **cum** on some exploratory HERO runs | **ALL-PS · mean · own pubs at decision year** = `pubs_per_career_year` (cum ÷ publishing-years since first pub) |
| **Pond / peer pool** | Uni×year **assistant** peer pools; LOO over assistant person-years | **Whole department** in **decision year** (all faculty ranks for peer norm); not every historical dept×year |
| **Outcome frame** | Option A: censored out of **rates**, in **quantile rank**; scrape-window censor | **Up-or-out** in decision year (army-like); cumulative productivity “until that point” |
| **Data spine** | `faculty_panel_with_pools.jsonl` person–year | **Master author×year pubs table** → precompute running cum / rates; slice for decision years |
| **Porch (Sep 2)** | BDP + HERO deck on **existing** panel | Alex: overlap **H_sort high** ✓; censored = missing scrape; **promoted-with-zero annual rate** = wrong metric → supports T3 |

**COMPASS sequencing:** Keep v0 porch/HERO as **Act I exploratory** (Alex saw it Sep 2). **Do not** treat v0 LAST-PS / ASST-PS bars as paper-final without PD29 spine or explicit sensitivity. Next engineering tranche = **T5 master table** + **T1–T4 decision-year slice**.

**Open (PD29, not locked):** Homophily on all faculty vs assistant-only pond; exact early/late window around year 6; survival analysis deferred.

---

## Grain naming (Charles lock — Sep 2)

Aligned with MBB **ALL-PS / LAST-PS** vocabulary; tenure adds **ASST-PS** because assistant-only person-years are the main v0 panel.

### Windows (person-years)

| Token | Label | Meaning |
|-------|-------|---------|
| `all_ps` | **ALL-PS** | All person-years in panel (any rank) |
| `asst_ps` | **ASST-PS** | Assistant-rank person-years only |
| `last_ps` | **LAST-PS** | Final assistant person-year (exit cross-section) |

### Stats

| Token | Label | Meaning |
|-------|-------|---------|
| `mean` | **mean** | Average over the window (person collapse for ASST-PS) |
| `cum` | **cum** | Stock through end of window |
| `annum` | **annum** | Single person-year value (replaces legacy “annual”) |

Retired everywhere: **spell-mean**, `spell_mean`, `grain=…` in favor of **`--window` / `--stat`**.

### Canonical combinations (v0 + PD29)

| Use | Window · stat · metric | Code / field |
|-----|------------------------|--------------|
| v0 HERO peer X | **ASST-PS · mean · peer LOO (annum)** | `--window asst_ps --stat annum` (default) |
| LAST-PS HERO peer X | **LAST-PS · cum · peer LOO** | `--window last_ps --stat cum` |
| LAST-PS ability slice | **LAST-PS · cum · own pubs** | `--window last_ps --x-metric own_cum` |
| Alex Â (PD29) | **ALL-PS · mean · own pubs at decision year** | `pubs_per_career_year` in `author_year_career_master.jsonl` |

**Decision year** = cohort filter / which calendar year we **read** the metric — not a separate window token.

**Code:** `tenure/scripts/tenure_grain_labels.py` · CLI `tenure/scripts/tenure_pass_a_hero.py --window` / `--stat`

---

## Step 0 — Confirm Mac has panel (once per session)

```bash
./scripts/rsync_pull_recent_hpc.sh tenure   # if unsure
ls -lh tenure/tenure_pipeline/faculty_panel_with_pools.jsonl
```

See [`20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md`](../../20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md).

---

## Step 1 — Inference filter (strict v0)

From person–year rows, keep rows where:

- `match_confidence` ∈ **{HIGH, MEDIUM}**
- `poolq_loo_mean` is not null (on assistant rows used for LOO)
- `ever_assistant` is true

**Do not** hero-plot raw 106K without understanding OpenAlex NONE tier (62K person–years).

---

## Step 2 — Collapse to person-level (HERO window)

Same logic as `tenure/tenure_pipeline/stage9_analysis.py`:

1. One record per `faculty_id`
2. **`loo_mean`** = mean of `poolq_loo_mean` over **assistant** years with non-null LOO (**ASST-PS · mean · peer annum**)
3. Drop persons with no computable LOO assistant years
4. Person flags: `tenure_event`, `attrition`, `censored`

---

## Step 3 — Outcomes (Option A — locked for v0)

**Resolved** = tenure OR attrition (known ending).

| Rate | Numerator | Denominator |
|------|-----------|-------------|
| Tenure rate | `tenure_event` | resolved in bin |
| Attrition rate | `attrition` | resolved in bin |

**Censored:** report `n_censored` per bin; **exclude** from rate denominator. Survival / Cox later.

### Two separate decisions (do not conflate)

| Decision | v0 lock | What it controls |
|----------|---------|------------------|
| **A — Rate denominator (Option A)** | Censored **out** of tenure/attrition rate | Bar height = tenured ÷ (tenured + attrition) in bin |
| **B — Quantile assignment** | Censored **in** when ranking on LOO | Who lands in ventile 1…K (`n_all` ≈ equal); slide label `resolved/all` |

Option A is about **Y** (outcome unknown → no rate). Decision B is about **X** (peer context known → still get a bin).

See **[§ Censored in quantile bins — pros/cons for Alex](#censored-in-quantile-bins--proscons-for-alex)** below.

---

## Censored in quantile bins — pros/cons for Alex

**Question for Alex:** Should **right-censored** faculty (still assistant near end of scrape window, ~2022–2024 last-asst years; no observed tenure or attrition yet) **stay in the pool used to define quantile cutpoints**, while remaining **excluded from the rate denominator** (current v0)?

**What censored means here (not survival analysis yet):**

- **Tenured** — promoted associate/full within `gap_tolerance` (2 yr) of last assistant year  
- **Attrition** — last assistant year **before** window tail, never promoted  
- **Censored** — never promoted **and** still assistant near **max_year** (2024) → outcome not yet observed  

On the last-ps cum LOO panel (N=732): **408 censored (56%)**, **324 resolved**. Censorship is **not** uniform across LOO (middle ventiles can be `4/37` resolved vs `26/37` elsewhere).

### Pros — keep censored **in** quantile assignment (current)

1. **X reflects the full inference panel.** LOO is defined for censored people; their peer context is real. Dropping them before binning changes who defines “ventile 10.”
2. **Avoids selection bias in cutpoints.** Censored correlate with LOO and career stage (recent hires still in the pipeline). Excluding them before ranking shifts ventile boundaries — especially if high-LOO or mid-LOO assistants are disproportionately still active.
3. **Parallel to MBB HERO.** Everyone with computable roster X gets a ventile; draft **Y** is only measured where the outcome exists. Same split: known X, partial Y.
4. **Equal `n_all` is interpretable.** “This ventile is the bottom 5% of the **sample by LOO**” includes people still on the job market clock — which matches “who faces this peer environment in our data?”
5. **Transparent accounting.** CSV + slides report `n_censored`, `n_resolved`, and `resolved/all` per bin; compositional skew is visible rather than hidden by pre-filtering.

### Cons — keep censored **in** quantile assignment

1. **Unequal resolved N despite equal `n_all`.** Quantile guarantees ~equal people per bin, **not** equal resolved counts → noisy Wilson CIs where censorship piles up (e.g. bin 11: `4/37`).
2. **Harder slide read without training.** Looks like “broken quantile” if you only see resolved counts (fixed in slides with `resolved/all` + footnote).
3. **Compositional confound in rates.** A low tenure rate might mix “true lower promotion among leavers” with “this ventile is mostly young / still assistant” — not separable in binned Wilson plots alone.
4. **Not the only defensible choice.** Alternatives are easy to run as sensitivity (see below).

### Main alternatives (sensitivity, not v0)

| Variant | Bin assignment | Rate denominator | Tradeoff |
|---------|----------------|------------------|----------|
| **v0 (current)** | All with LOO | Resolved only | Full X panel; variable resolved n |
| **Resolved-only quantile** | Re-rank LOO on resolved only | Resolved | ~Equal resolved per bin; cutpoints ignore censored LOO → shifted ventiles |
| **Resolved-only panel** | Quantile on LOO | Resolved | Drops ~56% (last-ps); different population (“careers already ended”) |
| **Option B rates** | All with LOO (or any) | All incl. censored | Treat censored as non-tenure → **not** recommended without survival frame |

**COMPASS view:** v0 is coherent for **exploratory HERO** (shape of tenure vs peer context among cases with known endings, indexed to the full LOO spectrum). For **paper claims**, Alex should sign off on (i) whether resolved-only quantile sensitivity is required, and (ii) whether last-ps HERO needs a **cohort aperture** that reduces censorship (e.g. last-asst year cap) before debating bin mechanics.

**Code:** `stage9_analysis._bin_rows` ranks **all** persons with LOO; `_aggregate_bins` applies Option A rates. Flags from `panel_builder.py` (`censored` if `last_asst >= max_year - gap_tolerance` and no tenure event).

---

## Step 4 — Bin and plot

| Knob | v0 |
|------|-----|
| X | Person-level `loo_mean` |
| Method | Quantile — equal **`n_all`** per bin (censored **included** in rank; see § censored pros/cons) |
| Count | **16** |
| CI | Wilson on resolved counts |
| Outputs | PNG + CSV + provenance JSON → `tenure_sandbox/hero/` |

**Stage 9** (`stage9_inverted_u.png`, Apr 2026) used 18 bins on a **broader** population — useful sanity check, **not** the v0 deliverable.

---

## Step 5 — Act II+ (later)

| Act | Action |
|-----|--------|
| **II F-HERO** | Bin department mean pubs at fixed Â slice |
| **III ρ** | Department-level H_sort bracket (compare to MBB reigning hero ρ folder) |
| **IV Sim** | Frozen departments → fit score knobs → sim tenure flags → replay HERO |

**ρ policy:** Do **not** assume ρ ≈ 0 on tenure. Run Act III before parking ASSIGN like MBB.

---

## Code map

| File | Role |
|------|------|
| `tenure/tenure_pipeline/stage9_analysis.py` | Reference implementation (collapse + bin + plot) |
| `tenure/tenure_pipeline/build_faculty_panel_inference_v1.py` | Inference tier filter reference |
| `tenure/scripts/tenure_grain_labels.py` | Window + stat labels (ALL-PS / ASST-PS / LAST-PS · mean / cum / annum) |
| `tenure/scripts/tenure_pass_a_hero.py` | v0 CLI → `tenure_sandbox/hero/` |
| `sports/scripts/pass_a_empirical_bundle.py` | MBB template for provenance + filenames |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | Initial pipeline map; v0 locks from Charles + Alex direction. |
| 2026-09-01 | § censored in quantile bins — pros/cons for Alex (Option A rates + include censored in rank). |
| 2026-09-02 | § Grain naming lock — ASST-PS / LAST-PS / ALL-PS + mean / cum / annum; retire spell-mean; fix Alex Â = ALL-PS mean at decision year. |
