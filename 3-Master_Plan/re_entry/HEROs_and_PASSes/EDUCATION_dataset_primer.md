# Education Big Fish datasets — primer for researchers

**Last synced:** 2026-09-22

**Audience:** Charles (and Alex) — dissertation HERO / assortativity work, no NCES survey background required.

**Purpose:** Enough context to read Alex’s **NELS:88** and **HS&B:80** Big Fish panels, run porch screens, and talk honestly about **assortativity**, **peer context**, and **what education can (and cannot) test** in our model.

**Standalone:** One document; paths below are repo-relative from project root.

**PDF:** Charles converts locally: `./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/HEROs_and_PASSes/EDUCATION_dataset_primer.md`

---

## 1. What these datasets are (plain English)

Both files are **Alex-built “Big Fish” panels** on classic **U.S. national education longitudinal surveys**. They are **not** raw NCES microdata you have to construct from scratch — peer leave-one-out (LOO) means, unit sizes, and analytic flags are **already computed**.

| Dataset | Full name | Cohort | Pond (unit) | Outcome horizon |
|---------|-----------|--------|-------------|-----------------|
| **NELS:88** | National Education Longitudinal Study | 1988 **8th-grade** cohort, peer snapshot at **10th grade** | **High school** (10th-grade classmates in sample) | Degree attainment by **2000** (~age 26) |
| **HS&B:80** | High School & Beyond | **1980** high-school **Sophomore** and **Senior** samples (separate) | **School × cohort wave** | Degree attainment by **1986** (~age 22–24) |

**Alex’s intent (Sep 2026):** Education is **“gold for the community”** — public, familiar domain to show **peer ponds**, **sorting (assortativity)**, and **peer context vs long-run outcomes** without sports framing.

**Repo paths:**

| Panel CSV |
|-----------|
| `datasets/nels88/nels88_big_fish_panel.csv` |
| `datasets/hsb80/hsb80_big_fish_panel.csv` |

**Status in repo:** **NELS:88** + **HS&B:80 (Soph + Senior, separate decks)** wired in `big_fish_data_story.py` → [`education_sandbox/`](education_sandbox/nels88/README.md) (`nels88`, `hsb80_soph`, `hsb80_senior`).

---

## 2. One row = what?

Each row is **one sampled student** in the analytic file.

- **Not** a full school census — only students **in the NCES sample** for that school appear as peers.
- **`peer_n`** ≈ 13 and **`unit_n`** ≈ 14 (NELS, min-10 sample) means roughly **14 sampled kids from that school**, not “everyone in the building.”
- Peer LOO is: *mean test score of the **other sampled students** in my school cell*, excluding self.

**Time structure:** Peer context is a **single high-school snapshot** (baseline tests). Outcome is **attainment many years later**. You are not watching within-year competition; you are asking whether **early peer composition** lines up with **later degree completion**.

---

## 3. Map to our HERO / Big Fish frame

Binding rule: **environment ≠ advancement**; **score ≠ select**. Education stress-tests the **sorting** and **peer context** legs more than **scarce top-K selection**.

| Our term | NELS / HSB column(s) | Note |
|----------|----------------------|------|
| **Unit / student** | `student_id` | One person |
| **Pond** | `school_id`, `unit_id` | School (NELS: 10th-grade high school; HSB: school × Soph/Senior wave) |
| **Own ability (Â)** | `own_performance_raw`, `own_performance_z` | Baseline **test composite** (reading + history standardized scores) |
| **Peer context (LOO)** | `peer_mean_loo`, `peer_mean_z_loo` | Mean peer test score / z, excl. self (~97–100% fill) |
| **Team mean (T̂_j analog)** | `unit_mean_including_self` | School mean including self |
| **Relative standing** | `relative_performance_z`, `within_unit_percentile_loo` | Own vs peers |
| **Congestion-ish proxies** | `n_peers_above`, `share_peers_above`, `n_top_decile_peers_loo`, `gap_to_unit_top` | “How many strong peers in my sampled pond?” — not sports usage |
| **Y (outcome)** | NELS: `bachelors_or_higher_by_2000` · HSB: `bachelors_or_higher_by_1986` | **Binary degree attainment**, not draft/tenure |
| **Sample gates** | `analytic_sample_min5`, `analytic_sample_min10`, `cell_at_least_*` | Minimum peers for stable LOO |
| **Survey weights** | NELS: `followup_weight_2000` · HSB: `followup_weight_1986`, `base_year_weight` | Use for population-style rates in serious tables |

**What is missing vs sports panels:** No Alex **`own_performance_index`** composite, no season-by-season panel, no explicit **top-K winner rule** in the data.

---

## 4. Key numbers (analytic samples)

| Panel | Filter | N | P(BA or higher) | Median peers |
|-------|--------|---|-----------------|--------------|
| **NELS:88** | `analytic_sample_min10 == 1` | **7,238** | **~36%** | ~13 peers |
| **HS&B Sophomore** | `analytic_sample_min5 == 1` | **12,184** | **~6.7%** | (see CSV) |
| **HS&B Senior** | `analytic_sample_min5 == 1` | **9,874** | **~17%** | (see CSV) |

**HSB rule (Alex):** Analyze **Sophomore and Senior separately** — different samples and questionnaires; **do not pool** into one HERO without justification.

**Why HSB BA rates differ:** 1986 follow-up is **early** for a BA (many still in college). NELS 2000 is a more mature attainment window.

**Other Y columns (secondary):** `associate_or_higher`, `any_postsecondary`, `high_school_diploma` — useful for robustness, not primary dissertation porch.

---

## 5. How to interpret — three Alex asks

Alex’s Sep 2026 guidance: screen for **(1) congestion**, **(2) assortativity**, **(3) effect** (does peer context move the outcome porch?).

### 5.1 Assortativity (sorting index $H_{\mathrm{sort}}$)

**Question:** Are students **sorted into schools** by baseline test ability?

- Compute **$H_{\mathrm{sort}}$** on **`own_performance_z`** with pools = **school** (same recipe as MBB overlap / Army — `541_grandchild_homophily_assign.realized_sorting_index_H_sort`).
- **Expectation:** Education should show **higher $H_{\mathrm{sort}}$ than MBB PPM (~0.06)** and plausibly in the **tenure (~0.17) or Army (~0.27)** ballpark — school quality and tracking sort peers.
- **Panel:** Team/school **interval overlap** (same machinery as Army panel 5).

**Read:** High $H_{\mathrm{sort}}$ means **ASSIGN / homophily matters for pool formation** (“why am I in this school?”). It does **not** by itself prove congestion-in-score ($\lambda$).

### 5.2 Peer context / “effect” (HERO-style porch)

**Question:** Does **peer LOO** predict **P(BA+)**?

- **X:** `peer_mean_z_loo` (or quantile bins thereof).
- **Y:** `bachelors_or_higher_by_*`.
- **Plot:** P(BA+) by peer LOO ventile — same **Layer A** grammar as Army/MBB HERO.

**Literature baseline:** “Big fish in a small pond” — often **monotonic** (weaker peers → higher attainment or self-concept), not necessarily MBB-style **inverted-U**.

**Do not over-claim:** This is **attainment**, not **one scarce slot per school**. ~36% BA in NELS is a **population rate**, not NBA draft odds.

### 5.3 Congestion (sports sense)

**Question:** Is there a **scarce-resource / spotlight** story?

- **Weak direct analog** in education vs football **usage LOO**.
- Closest panel columns: **`share_top_decile_peers_loo`**, **`n_peers_above`**, **`gap_to_unit_top`** — “how crowded is the top of my sampled pond?”
- **Pass A ($\lambda$ knockout)** is **not in the CSV** — education does not observe a ranking equation.

**Honest framing:** Education is strongest on **sorting + peer composition → long-run outcome**, not on **congestion in a score that ranks candidates for one slot**.

---

## 6. What to claim vs not claim

| OK to say | Avoid |
|-----------|--------|
| Schools **sort** students by measured ability ($H_{\mathrm{sort}} > 0$). | “Education confirms MBB-style inverted-U hero” without seeing the curve. |
| Peer LOO at baseline **predicts** (or doesn’t) BA+ many years later. | “Peer LOO **causes** degree completion.” |
| Education extends the framework to **public, non-sports** data. | “Same **selection** mechanism as NFL draft / tenure vote.” |
| Sampled-classmate LOO is **explicitly partial** peers. | “Full school roster LOO.” |
| HSB Soph vs Senior are **different cohorts**. | One pooled “HSB HERO” without split. |

---

## 7. Relation to homophily ($\rho$) and MBB “works anyway”

Three objects — keep separate:

| Object | Role |
|--------|------|
| **$H_{\mathrm{sort}}$** | **Empirical** sorting — variance in ability explained by pond assignment |
| **$\rho$ (homophily)** | **Simulated ASSIGN** knob calibrated to match $H_{\mathrm{sort}}$ (PD21) |
| **$\lambda$ (congestion in score)** | **Scoring** in $S_i = A_i - \lambda L_C$ — Pass A knockout |

**2a — Can we get congestion effects without assortativity?**  
**Yes in the sim:** fixed rosters, toggle $\lambda$, same top-K select. Congestion-in-score does **not** require homophily.

**2b — MBB boundary case:** MBB has **very low $H_{\mathrm{sort}}$ (~0.06)** and **tiny K/N** (few draft slots per huge roster). Hero-ish curves may appear even when **$\rho^* \approx 0$**. **Army ($H_{\mathrm{sort}} \approx 0.27$)** is the opposite regime — **real sorting into units**.

**Education’s role in that debate:** Likely **high $H_{\mathrm{sort}}$**, **non–top-K Y** — separates **“sorted ponds”** from **“scarce selective advancement.”** Even a flat HERO porch would be informative: *assortativity without draft-like selection*.

---

## 8. Suggested screening sequence (when you build)

1. **NELS:88 first** (smaller, cleaner outcome window by 2000).
   - Overlap + **$H_{\mathrm{sort}}$** on school partition.
   - HERO: P(BA+) vs `peer_mean_z_loo` (Q16 ventiles); use **`followup_weight_2000`** for weighted rates if reporting population-style numbers.
   - Gate: `analytic_sample_min10 == 1`.
2. **HS&B:80** — **Soph** and **Senior** as **two decks**.
   - Same panels; note lower BA rate by 1986, especially Sophomores.
3. **One-page synthesis table** for Alex:

   | Domain | $H_{\mathrm{sort}}$ | HERO shape? | Congestion proxy? | Selection-like Y? |
   |--------|---------------------|-------------|-------------------|-----------------|
   | NELS | ~0.25 | steep monotonic | weak (HS pond) | No (~36% BA) |
   | HSB Soph | ~0.28 | steep monotonic | weak | No (~7% BA) |
   | HSB Senior | ~0.32 | steep monotonic | weak | No (~17% BA) |

**Not in this primer but same portfolio:** Football (position + usage congestion), LoL (dev→top-tier promotion). See `HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md`.

---

## 9. Column cheat sheet (both panels)

Shared Big Fish columns (names align across NELS and HSB):

| Column | Meaning |
|--------|---------|
| `own_performance_raw` | Baseline test composite (level) |
| `own_performance_z` | Student z-score (global or as documented in Alex build) |
| `peer_mean_loo` | Mean peer raw score, excl. self |
| `peer_mean_z_loo` | Mean peer z, excl. self — **primary HERO X** |
| `peer_sd_loo` | Dispersion of peers |
| `unit_n` | Sample size in school cell (incl. self) |
| `peer_n` | Peers used for LOO (= unit_n − 1) |
| `within_unit_percentile_loo` | Percentile within school sample |
| `n_peers_above` / `share_peers_above` | Count / share of peers with higher raw score |
| `n_top_decile_peers_loo` | Count of global top-decile peers in pond |
| `unit_mean_including_self` | School mean including self |
| `gap_to_unit_top` | Distance to top scorer in cell |
| `global_top_decile_cutoff` / `own_global_top_decile` | Global high-ability flags |
| `base_year_ses` | SES control |
| `sex_label` / `race_label` (NELS) or `sex` / `race` (HSB) | Demographics |

HSB-only extras: `gpa10`, `gpa12`, `school_type_label`, `school_region`, `SOQFLAG` / `SRQFLAG` (questionnaire flags).

---

## 10. One-sentence talk tracks

**For Alex (education value):**  
“NELS and HS&B let us show **sorted school ponds** and **peer LOO vs long-run attainment** on public data — high assortativity without pretending every domain is NFL draft selection.”

**For the dissertation boundary:**  
“Education is our **assortativity and peer-composition** leg; Army/MBB/tenure remain the **scarce advancement** legs.”

**For methods footnote:**  
“Peer LOO is over **sampled classmates**, not full rosters; weights matter for population rates.”

---

## 11. Related repo docs

| Doc | Role |
|-----|------|
| `HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md` | Portfolio verdict + sequencing |
| `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | Environment vs advancement; score vs select |
| `HEROs_and_PASSes/legends_sandbox/LEGENDS_LoL_primer_for_researchers.md` | Parallel primer format (sports domain) |
| `scripts/big_fish_data_story.py` | Football + LoL mosaics today — **education not wired yet** |

---

*End of primer.*
