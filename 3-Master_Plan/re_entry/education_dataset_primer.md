# Education Big Fish datasets — print primer

**For:** Charles · read before NELS / HSB screens · **2026-09-22**  
**Context:** Alex guidance (post-Army mosaics) — start with **education** for assortativity, peer context, and community-facing evidence; then football / LoL.  
**Binding frame:** Environment (`L_net = B − D`) ≠ advancement. Advancement = **score** then **select**. Hero = Layer A **outcomes**, not the scoring equation.

**Repo paths:**

| Dataset | Panel CSV |
|---------|-----------|
| NELS:88 | `datasets/nels88/nels88_big_fish_panel.csv` |
| HS&B:80 | `datasets/hsb80/hsb80_big_fish_panel.csv` |
| Assessment memo | `3-Master_Plan/re_entry/HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md` |

**Not wired yet:** no `education_sandbox/` or `big_fish_data_story.py --domain nels88` — CSV + this primer only.

---

## 1. What these datasets are (one paragraph each)

### NELS:88 (National Education Longitudinal Study)

Alex shipped a **Big Fish panel** on the **1988 eighth-grade cohort**, with peer context measured around **10th grade**. Each row is a **sampled student**. The **pond** is the **10th-grade high school** (`school_id` / `F1SCH_ID`). **Own ability** is a baseline **test composite** (`own_performance_raw`, `own_performance_z`). **Peer context** is leave-one-out mean test performance among **other sampled students in the same school** (`peer_mean_loo`, `peer_mean_z_loo`). **Outcome** is **degree attainment by 2000** — mainly `bachelors_or_higher_by_2000` (~**36%** in the min-10-peer analytic sample).

### HS&B:80 (High School & Beyond)

Same Big Fish logic on the **1980** cohort, but **two base-year samples**: **Sophomore** and **Senior** (separate rows — **do not pool** without thinking). Pond = **school × cohort wave**. Outcome = attainment by **1986** (`bachelors_or_higher_by_1986`, ~**11%** in min-5 analytic — cohort still young at follow-up). Richer covariates (SES, school type, region, GPA).

### Why Alex calls education “gold for the community”

Sports drafts and tenure are niche gates. **School × peer × long-run attainment** is public-data, policy-relevant, and connects to decades of **school effects / small-pond** literature — without pretending every domain is the NBA draft.

---

## 2. Column map (HERO / pond language)

| Our term | NELS / HSB column | Note |
|----------|-------------------|------|
| **Unit** | `student_id` | One student |
| **Pond** | `unit_id`, `school_id` | School (NELS: 10th-grade cell; HSB: school × Soph/Senior) |
| **Â (own ability)** | `own_performance_raw`, `own_performance_z` | Baseline test composite; **z** is the usual porch axis for own ability |
| **Peer LOO** | `peer_mean_loo`, `peer_mean_z_loo` | Mean test score of **other sampled students** in the pond |
| **Relative standing** | `relative_performance_z`, `within_unit_percentile_loo` | Own vs peers |
| **Congestion-ish proxies** | `n_peers_above`, `share_peers_above`, `n_top_decile_peers_loo`, `gap_to_unit_top` | “How many strong peers in my sampled pond?” — not usage/touches |
| **Pond size** | `unit_n`, `peer_n` | Sampled N in cell (not full school enrollment) |
| **Analytic filters** | `analytic_sample_min5`, `analytic_sample_min10`, `cell_at_least_*` | Require enough peers for stable LOO |
| **Y (outcome)** | NELS: `bachelors_or_higher_by_2000` · HSB: `bachelors_or_higher_by_1986` | Binary attainment |
| **Weights** | NELS: `followup_weight_2000` · HSB: `followup_weight_1986`, `base_year_weight` | Use for population-style rates if you report means |

**Not in panel:** teammate LOO on a composite index like football’s `own_performance_index`; no draft slot, no λ knockout, no Grandchild ρ precomputed.

---

## 3. Sample sizes (quick reference)

| | NELS:88 | HS&B:80 |
|---|---------|---------|
| Total rows | ~10,545 | ~22,889 (Soph ~12.6k · Senior ~10.3k) |
| Analytic (≥10 peers, NELS) | ~7,238 | — |
| Analytic (≥5 peers, HSB) | — | ~22,058 |
| **Y rate (BA+)** | ~**36%** (min-10) | ~**11%** (min-5; 1986 follow-up) |

---

## 4. How to interpret (your model)

### 4.1 Assortativity — **primary education win**

Compute **H_sort** on the school partition: share of cross-student variance in `own_performance_z` explained by **which school** you’re in (same recipe as Army/MBB overlap: `541_grandchild_homophily_assign.realized_sorting_index_H_sort`).

**Expectation:** H_sort **well above MBB PPM (~0.06)**, plausibly in the **tenure (~0.17) or Army (~0.27)** ballpark — students are sorted into schools by ability and SES.

**Read:** “How sorted are ponds?” — **ASSIGN / homophily** relevance for *why you face these peers*.

### 4.2 HERO porch — **peer LOO vs attainment**

Plot **P(BA+ | peer LOO ventiles)** (Q16), optionally **survey-weighted**.

**This is valid Layer A** — conditional outcome vs peer context.

**It is not** the same object as MBB draft HERO:

| MBB / Army / Tenure | Education |
|---------------------|-----------|
| **Scarce top-K** slot (draft, promotion, tenure line) | **Population attainment** (~36% / ~11%) |
| Often inverted-U / tail softening | May be **monotonic** (small-pond) or flat |
| Same-season or near-term Y | **10+ year lag** (HS test → 2000/1986 degree) |

**Do not say:** “congestion in the score” or “draft rate” without translation.

**Do say:** “Peer context in high school vs later BA completion” / “school sorting (H_sort) + peer gradient on attainment.”

### 4.3 Congestion (sports sense)

**Usage / spotlight / top-K peers** do not map cleanly. Closest panel fields: **`share_peers_above`**, **`n_top_decile_peers_loo`**, **`gap_to_unit_top`**. Treat as **exploratory**, not reigning spec.

### 4.4 Homophily (ρ) vs H_sort vs λ

| Object | Role in education screen |
|--------|-------------------------|
| **H_sort** | Empirical sorting into schools — **measure this** |
| **ρ (Grandchild ASSIGN)** | Sim knob to *generate* sorting — calibrate **after** H_sort if needed |
| **λ (congestion in score)** | **Not in data** — Pass A sim only |

**Key insight (Alex 2a/2b):** Congestion effects in the **sim** can appear **without** homophily (λ knockout, fixed rosters). MBB may “work anyway” because **H_sort is tiny** and **K/N is tiny**. Education is the **high-sorting, non-top-K** regime — tests whether **assortativity** and **peer effects** show up **without** NFL-style selection.

---

## 5. Design caveats (read before any slide)

1. **Sampled classmates, not full schools.** `peer_n ≈ 13` means ~14 surveyed students in that school cell — LOO is over **NELS/HSB sample peers**, not every student in the building.

2. **Frozen peer snapshot → distant outcome.** Peer context = ~10th grade tests; Y = degree by 2000/1986. Mechanism is long-run, not in-season advancement.

3. **Attainment ≠ selection.** High BA rate ≠ “one winner per school.” Hero **shape** may differ from sports; **assortativity** may still be strong.

4. **HSB: Soph vs Senior.** Alex: analyze **separately**. Different `unit_id` (`HSB_*_sophomore` vs senior). Pooling blurs cohort design.

5. **Weights.** For published-style rates, use follow-up (and base-year where appropriate) weights; unweighted porches are fine for **screening**.

6. **No sandbox yet.** Screening = new script or extend `big_fish_data_story.py` — not a one-liner today.

---

## 6. What “success” looks like for Alex (screen checklist)

| Signal | What to build | Success | Weak / fail |
|--------|---------------|---------|-------------|
| **Assortativity** | Overlap panel + **H_sort** on school | H_sort reported; overlap shows stacking | Low H_sort (unlikely) |
| **Peer effect** | HERO: P(BA+ \| `peer_mean_z_loo`) | Clear gradient or documented flat | — |
| **Congestion** | `share_peers_above` / top-decile peer counts vs Y | Optional nugget | No sports-style usage story expected |
| **Community** | One honest paragraph + one mosaic | Non-sports domain in portfolio | Forcing inverted-U / draft language |

**Suggested order:** **NELS88 first** (smaller, faster) → **HSB Soph** → **HSB Senior** → synthesis table vs Army / MBB / tenure H_sort.

---

## 7. Contrast table (where education sits)

| Domain | Pond | Y | Selection? | H_sort (empirical) | HERO role |
|--------|------|---|------------|--------------------|-----------|
| **Army** | Unit pool | Promotion | Strong | **~0.27** (Charles) | Anchor |
| **MBB** | Team LOO | Draft | Strong | **~0.06** | Anchor |
| **Tenure** | Dept LOO | Tenure | Strong | **~0.17** | Anchor |
| **NELS / HSB** | School LOO | BA+ | **Weak** | **TBD (expect high)** | Assortativity + peer |
| **Football** | Team / position LOO | Draft | Strong | DB ~0.15 | Usage congestion |
| **LoL** | Dev team LOO | Top-tier promo | Strong | TBD | Background screen |

---

## 8. Commands / next repo step (when ready)

```bash
# Not implemented yet — target deliverable:
#   3-Master_Plan/re_entry/HEROs_and_PASSes/nels88_sandbox/data_story/NELS_DATA_STORY_3x3.png
#   .../FOOTBALL_team_interval_overlap_meta.json-style H_sort sidecar
```

Until then: read CSV in pandas; filter `analytic_sample_min10` (NELS) or `analytic_sample_min5` (HSB); split HSB by `cohort`.

---

## 9. One-sentence talk track for Alex

> “Education gives us **high school sorting (H_sort)** and **peer LOO vs long-run attainment** without a draft gate — so we can show assortativity and peer context matter in a **community domain**, and separate that from **scarce top-K selection** where MBB and Army live.”

---

*Print: `./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/education_dataset_primer.md` (Charles runs locally per project convention).*
