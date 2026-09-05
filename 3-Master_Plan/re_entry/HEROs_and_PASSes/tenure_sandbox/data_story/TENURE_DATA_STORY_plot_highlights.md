# Tenure data story — plot highlights (talk track)

**Deck:** `TENURE_DATA_STORY_pd29_3x3.png` · read **top-left → bottom-right**  
**Reigning HERO lock:** decision cohort (PD29) · dept pond LOO · Alex Â (`pubs_per_career_year`) · Q16 · infHM all resolved

Use one sentence per panel when screening a domain; two if Alex asks “why is this here?”

---

## Row 1 — Who is in the pond?

### 1 · Cohort

**Highlight:** This is the **decision universe** — one row per resolved assistant exit at decision calendar year, inference tiers, and the outcome we care about (tenured vs attrition).

**Say:** “N = 391 resolved, 280 with Alex career rate, 389 with dept LOO — everything below is whether **peer context at decision** predicts tenure beyond **own cumulative productivity**.”

---

### 2 · Â_i and T̂_j

**Highlight:** Separates **individual cumulative productivity** (Alex Â at decision year) from **department mean career rate** (T̂_j, whole dept includes focal).

**Say:** “Own Â is right-skewed; dept talent has its own spread. HERO’s environment axis is **LOO dept pond**, not raw T̂_j — this panel sets up *who* vs *where*.”

**Numbers (PD29):** n = 280 with Â · n = 389 with T̂_j · med Â ≈ 4.9 · med T̂_j ≈ 4.8 (see `TENURE_BDP_Ai_Tj_pd29_meta.json`).

---

### 3 · dept pond LOO distribution (3a histogram · 3b ECDF)

**Highlight:** Shows the **support** of the peer-context variable — where dept LOO career rate lives, and how tenured vs attrition ECDFs differ.

**3a (histogram):** Raw LOO support on `pubs_per_career_year` at decision year (green).

**3b (ECDF):** Gray dotted = all resolved; **blue solid** = tenured; **red dashed** = attrition. Lines track closely in the mid-pond — separation is subtle, not MBB-draft-level shift.

**Value:** Before any binning story, LOO must be **non-degenerate** (median LOO peer count ≈ 27). This is descriptive **input** side, not the HERO curve.

**Say:** “Left: where dept LOO mass lives. Right: outcome ECDFs are similar through the median — tenure is not driven by a massive pond shift at the population level; conditional zooms (panels 7–8) matter more.”

**Not:** An outcome curve — descriptive distribution only.

---

## Row 2 — Geometry and who carries tenure mass

### 4 · Tenure mass vs Â (ECDF)

**Highlight:** **Where tenured cases come from in ability space** — cumulative share of all tenured faculty by Alex Â.

**Value:** Justifies **fixing Â bands** later (CCT / elite pond): tenure mass concentrates in the upper productivity tail (red tenure-mass grid + purple top-% cuts mirror MBB panel 4).

**Say:** “Most tenured faculty sit in the upper Â tail — when we **hold ability fixed** in panels 7–8, we zoom where the **marginal tenure decision** happens, not the whole cohort.”

**Pairs with:** Panel 2 (marginal Â) but Panel 4 answers **tenure-weighted** importance, not headcount.

**Numbers:** n = 280 with rate · n = 146 tenured with rate (among resolved with Â).

---

### 5 · Dept interval overlap

**Highlight:** **Sorting overlap** — how much dept-year talent windows stack on the same calendar-year roster (assortment geometry on career rate z within year).

**Say:** “Departments aren’t isolated talent bins — intervals overlap. That’s why LOO (peers excl. self) matters more than ‘my dept’s average’ alone.”

**Numbers:** 2000–2024 dept-year pools · H_sort on career-rate z (see overlap meta JSON).

---

### 6 · Dept roster size |T_j|

**Highlight:** **Pond size** — how many faculty define each decision-year dept LOO pool.

**Say:** “LOO is computed over ~100-person departments on average (median |T_j| ≈ 97). Peer context is a **real dept roster**, not a league average.”

---

## Row 3 — Conditional stories (LOO-axis; panels 7–8 TBD)

### 7 · CCT — fixed Â z ∈ [1, 2] · Q8 · dept LOO

**Highlight:** **Squid vs Jackal within a matched ability band** — mid-LOO vs top-LOO quantile bins, holding **within-year z ∈ [1, 2]** on Alex Â (scaled from MBB’s z ∈ [2, 3]).

| Knob | Panel 7 (tenure probe) |
|------|------------------------|
| Who | **z ∈ [1, 2]** on pubs_per_career_year (within decision year) |
| Share | **n = 33** with Â + LOO (279 eligible) |
| Binning | **Q8** quantile on dept pond LOO within band |
| Question | Mid-LOO vs top-LOO tenure rates — CCT signature? |
| **Sep 2026 read** | Squid **50%** (n=8) vs Jackal **50%** (n=8) → **CCT = NO** |

**Say:** “Panel 7 is the tenure CCT probe on a **wider z band** than MBB — cells are thin (n≈4/bin). No Squid–Jackal separation on this spec; full HERO concavity lives in panel 9.”

**Script:** `tenure/scripts/tenure_pass_a_congestion.py --plot cct --ai-z-lo 1 --ai-z-hi 2 --loo-n-bins 8`

---

### 8 · Elite pond LOO — top 20% Â · PW 3+5 · dept LOO

**Highlight:** **High-Â faculty only** — tenure rate vs dept LOO with **piecewise tail** binning (scaled from MBB top 7% → **top 20%** for N).

| Knob | Panel 8 (tenure probe) |
|------|------------------------|
| Who | **Top 20% Â** (within-year z on career rate) |
| Share | **n = 56** · 39 tenured |
| Binning | **PW 3+5** on dept pond LOO |
| Question | Plateau → **downturn** in highest LOO tail? |
| **Sep 2026 read** | Plateau **69.8%** → tail **83.3%** · last bin n=2 → **downturn = NO** |

**Say:** “Panel 8 is the elite-pond probe — tail bins are **very thin** (n=2–3). No MBB-style elite LOO dip here; panel 9 bin 14 still hints at a full-panel high-LOO drop.”

**Script:** `tenure/scripts/tenure_pass_a_congestion.py --plot elite_pond --ai-top-pct 20 --loo-n-low 3 --loo-n-high 5`

**Both probes:** `python tenure/scripts/tenure_pass_a_congestion.py --plot all_probes`

---

### 7 vs 8 — one-liner contrast (tenure probes, Sep 2026)

**Panel 7:** Among **matched-Â** faculty (**z ∈ [1, 2]**, n=33), do **middle** LOO bins beat **top** LOO bins? → **CCT = NO** on this spec.  
**Panel 8:** Among **high-Â** faculty (**top 20%**, n=56), extreme high-LOO tail downturn? → **NO** (thin tail bins; plateau 70% → tail 83%).

Same **dept LOO** x-axis as panel 9; **scaled Â gates** vs MBB (see footnotes).

| Â gate | Definition | Tenure PD29 probe |
|--------|------------|-------------------|
| Panel 7 | z ∈ **[1, 2]** | n = 33 · Q8 LOO |
| Panel 8 | **Top 20%** Â | n = 56 · PW 3+5 LOO |

---

### 9 · HERO (Pass A · dept LOO) — finale

**Highlight:** **Full-panel environment curve** — tenure rate vs dept LOO for everyone with computable pond (not Â-fixed).

**Say:** “Panel 9 is the **reigning tenure HERO** — middle rise, **concave** on LOO (LPM β₂ ≈ −0.017); highest LOO ventile drops (bin 14). Panels 7–8 zoom **where** in Â-space that conditional shape might live.”

**Numbers:** n = 389 · Q16 quantile bins · peak vent 5–6 (~79% tenure) · last high-LOO ventile weak.

---

## 30-second domain screen (Alex)

1. **Population sane?** → 1, 2, 6  
2. **Environment variable sane?** → 3  
3. **Tenure mass justifies zoom bands?** → 4  
4. **Assortment / overlap?** → 5  
5. **Act II congestion (CCT)?** → 7 *(probe: CCT=NO)*  
6. **Elite tail on LOO?** → 8 *(probe: downturn=NO; thin N)*  
7. **HERO shape?** → 9  

**Verdict strip (Sep 2026 probes):** HERO concave on full panel (panel 9); CCT band **no** Squid–Jackal split; elite top-20% **no** tail downturn — tail bins n≈2–3.

---

## Path to panels 7 & 8 — engineering checklist

**Status: first probes shipped** (`tenure_sandbox/act2/`, Sep 2026).

| Piece | Status |
|-------|--------|
| `tenure/scripts/tenure_pass_a_congestion.py` | ✓ |
| Panel 7 CCT z[1,2] Q8 | ✓ `CCT_tenure_rate_ai_band_dept_loo_pd29_z1_2_q8.png` |
| Panel 8 elite top20% PW3+5 | ✓ `ELITE_pond_loo_pw3p5_pd29_top20.png` |
| Manifest wired | ✓ `tenure_pd29_3x3_manifest.json` |

**Regen both probes + mosaic:**

```bash
python tenure/scripts/tenure_pass_a_congestion.py --plot all_probes
python sports/scripts/build_data_story_mosaic.py \
  --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json
```

**Next sensitivity (optional):** top 15% vs 25%; z ∈ [1, 3]; Q6 instead of Q8 — only if Alex wants a grid. Do **not** run MBB top-7% / z∈[2,3] without acknowledging empty cells.

---

## Perf metric story (`TENURE_PERF_METRIC_STORY.png`)

Six HERO rows per page (3 metrics × Q/EW): **career rate** · **cum pubs** · **annum pubs** (`pubs_year` at decision year), each with **dept LOO** peer X.

| Page | File | Bins |
|------|------|------|
| 1 | `TENURE_PERF_METRIC_STORY.png` | Q16 + EW16 |
| 2 | `TENURE_PERF_METRIC_STORY_p2.png` | Q10 + EW10 |

**Row 3 (plots 5–6 on each page):** **annum pubs** — single-calendar-year work count (not a career rate); LOO mean of colleagues' `pubs_year` at decision year.

```bash
python tenure/scripts/tenure_perf_metric_story.py --no-footer --page-size letter
```

---

## Footnotes for honest slides

- All BDP panels use **PD29 decision cohort** · `pubs_per_career_year` · whole-dept LOO at decision year.  
- Panel 9 uses **all 389** with LOO; panels 4 and Â-gated plots use **280** with career rate where noted.  
- Panels **7–8:** scaled Act II probes (z∈[1,2] Q8; top-20% PW3+5) — **not** MBB top-7%/z∈[2,3]. See `tenure_sandbox/act2/*.json`.  
- Full-panel HERO β₂ (dept LOO) ≈ **−0.017** — concave; **not** the same test as panel 7 Squid–Jackal.  
- v0 infHM BDP (ASST-PS poolq) remains in `basic_data_plots/*_infHM*` for porch history; **not** in this 3×3 deck.

---

## Rebuild commands

```bash
# All PD29 BDP
python tenure/scripts/tenure_basic_plots.py --mode pd29

# HERO (panel 9)
python tenure/scripts/tenure_pass_a_decision_hero.py

# Mosaic
python sports/scripts/build_data_story_mosaic.py \
  --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json
```
