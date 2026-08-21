# SCOUT → COMPASS: Track C complete — OBPM/BPM Pass A robustness

**Date:** 2026-08-20  
**From:** SCOUT  
**To:** COMPASS  
**Trigger:** Charles relayed your Round 3 Track C brief after Alex meeting (2026-08-20). Alex endorsed comprehensive-data check (OBPM/BPM); Charles green-lit SCOUT execution same day.

**Round 3 status:** Track **C** executed (**`--quick`** slice). Tracks **A** (HAND / Alex) and **MLE γ-profile** advanced in parallel via Charles — not SCOUT-owned this session.

---

## 0. Executive summary (for COMPASS)

| Item | Result |
|------|--------|
| **Task** | POST-QC hero robustness with **OBPM** and **BPM** as `perf_metric` — parallel to **PPM canonical**, no overwrite |
| **Verdict** | **Does not restore inverted-U** under POST-QC. If anything, **stronger monotonic rise** into elite teammate-quality bins; **β₂ more positive** than PPM |
| **PPM canonical** | Unchanged — `pass_a/PASS_A_empirical_talent_vs_roster_side_by_side.png` |
| **Charles deck** | PNGs placed on HAND deck **`OLD vs NEW empirical`** (+ matching export folder; first-slide titles per Charles convention) |
| **Alex line** | PPM hero canonical; OBPM/BPM = sensitivity appendix; July dip = mg=0 / cameo QC, not “need more ESPN” |

---

## 1. Context — what Charles told Alex

Charles aligned with Alex on:

- **HERO wavetops:** POST-QC panel → middle rise, **flat elite tail**; July inverted-U = sensitivity / QC artifact (B5–B6 cameo story).
- **More ESPN coverage:** unlikely to move needle.
- **OBPM/BPM:** right next empirical check — matches Round 3 **Track C**.
- **Bernoulli MLE (fix γ, refit λ/t, move γ):** Alex delighted; Charles to explain later via `3-Master_Plan/MLE/MLE_basics.md` + `MLE_fit_explainer.md`.

Charles has **not** fully answered Round 3 question doc yet; implicit priority: **MLE conversation with Alex** may rank ahead of **PD14** — note when Round 4 starts.

---

## 2. What SCOUT built and ran

### 2.1 Code changes

| File | Change |
|------|--------|
| `sports/scripts/pass_a_empirical_bundle.py` | `--perf-metric` (ppm / obpm / bpm / …); non-PPM → `pass_a/sensitivity/`; tagged filenames |
| `sports/scripts/pass_a_hero_sensitivity_plots.py` | Same; separate JSON/CSV per perf; `--quick` = 3 POST-QC specs for obpm/bpm (8 for ppm incl. July replay) |
| `sports/scripts/pass_a_bpm_robustness.py` | **New driver** — bundle + sensitivity + comparison report |

**Data path (unchanged):** `bpm_player_season_matched.csv` (2011–2021) merged in `panel_rebuild.py` / `perf_metric.py`. No new scrape.

### 2.2 Command run (repo root)

```bash
python sports/scripts/pass_a_bpm_robustness.py --quick
```

Equivalent to OBPM + BPM bundle (2011–2021) + 3 sensitivity PNGs each.

### 2.3 Spec (POST-QC hero)

- mg ≥ 10, min_minutes = 20, seasons 2011–2021  
- 16 quantile bins, winsor 0.01–0.99  
- X = **poolq_loo** (LOO teammate quality); own ability on left panel of side-by-side  

---

## 3. Key numbers — canonical spec (poolq_loo, mg=10, 2011–2021, 16q)

| perf | n | drafts | peak bin | peak rate | tail Δ | β₂ | ≥2 post-peak declines |
|------|---|--------|----------|-----------|--------|-----|------------------------|
| **ppm** (canonical) | 46,306 | 1,133 | 15 | 3.25% | −0.03pp | +0.006 | **0** |
| **obpm** | 45,154 | 1,102 | 16 | 11.69% | 0.00pp | +0.064 | **0** |
| **bpm** | 45,154 | 1,102 | 16 | 12.93% | 0.00pp | +0.049 | **0** |

**SCOUT read (matches your Round 3 prediction):**

- **Inverted-U:** No spec under POST-QC with ≥2 declining bins after peak (quick grid: **0** hits for obpm/bpm).
- **“Opposite direction”:** OBPM/BPM show **steeper monotonic climb** and **larger positive β₂** — not concavity at the elite tail.
- **n drop (~1,150 PS):** BPM merge coverage (2011–2021 only on matched file), not scrape gap.

Full comparison: `pass_a/sensitivity/TRACK_C_bpm_obpm_vs_ppm_report.md`

---

## 4. Where to find artifacts

### 4.1 Source PNGs / CSV / JSON (repo)

| Kind | Path |
|------|------|
| **PPM canonical** side-by-side | `pass_a/PASS_A_empirical_talent_vs_roster_side_by_side.png` |
| **OBPM / BPM** side-by-side | `pass_a/sensitivity/PASS_A_empirical_talent_vs_roster_side_by_side_{obpm,bpm}_16quantile_winsor0199_min20.png` |
| Sensitivity bar charts (quick) | `pass_a/sensitivity/PASS_A_sensitivity_{obpm,bpm}_*.png` |
| PPM POST-QC reference bar | `pass_a/sensitivity/PASS_A_sensitivity_loo_mg10_2011_2021_b16q_w0199.png` |
| July replay (mg=0) | `pass_a/sensitivity/PASS_A_sensitivity_loo_mg0_*_july_replay_mg0.png` |
| JSON indices | `pass_a/PASS_A_hero_sensitivity_post_qc_{obpm,bpm}.json` (+ ppm in `..._post_qc.json`) |
| LPM coeffs / ventile CSVs | `pass_a/sensitivity/PASS_A_lpm_hero_coefficients_*`, `PASS_A_binned_draft_rate_*` |

### 4.2 Charles slide deck (visual audit for agents)

Charles follows the usual convention: **`.pptx` master** + **same-name folder** (minus extension) with exported **`SlideN.png`**, and **first-slide title names** for reference.

| Item | Path (expected) |
|------|-----------------|
| Deck | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/OLD_vs_NEW_empirical.pptx` |
| PNG exports | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/OLD_vs_NEW_empirical/SlideN.png` |

Charles placed **Track C PNGs** (PPM vs POST-QC OBPM/BPM side-by-sides and sensitivity bars) on this deck for Alex / HAND work. **Refer to slide titles** when Charles cites slides in chat.

*(Parallel example: `slides/OLD_vs_NEW_data_intervals.pptx` + `slides/OLD_vs_NEW_data_intervals/`.)*

---

## 5. Implications for COMPASS sequencing

| Topic | SCOUT recommendation |
|-------|------------------------|
| **Rung 1 / inverted-U** | **Closed** on POST-QC with honest limits. Do not reopen for BPM/OBPM promotion unless Charles asks after reading deck. |
| **Track C follow-up** | **`--quick` sufficient for Alex brief.** Full 39-spec grid optional — run `pass_a_bpm_robustness.py` without `--quick` only if Charles wants appendix depth. |
| **Track A (HAND)** | Charles may be updating **`OLD vs NEW empirical`** — COMPASS can draft talking points from §3 + July replay contrast. |
| **Track B (ρ→2025)** | Still optional; script exists (`scripts/regenerate_pd21_rho_hsort_13_25.sh`), not run this session. |
| **Bernoulli MLE** | **Not blocked** by Track C (PPM-based A in fit). Charles/Alex γ conversation = separate line. |
| **PD14** | Park until Charles confirms ordering post-Alex. |
| **Round 3 Charles answers** | Track C effectively **green-lit in spirit**. Still need explicit reply on A/B/D ordering + B6 table + back-scrape. |

---

## 6. Suggested COMPASS talking points (Alex / appendix)

1. **Canonical hero = PPM**, POST-QC locked (mg=10, min=20, 2011–2021).
2. **Robustness:** OBPM and BPM **confirm** middle rise; **do not** restore elite-tail dip.
3. **July shape:** documented under **mg=0** sensitivity — cameo/QC, not ability-measure gap.
4. **BPM/OBPM value:** stronger talent gradient + defensible “we checked comprehensive SR metrics” — not a new canonical hero.

---

## 7. Not done (explicit)

- Full (non-`--quick`) OBPM/BPM sensitivity grid  
- Round 4 hoopR draft-loader verification (SCOUT Round 3 § follow-up)  
- ρ/H_sort 2013–2025 regen run  
- COMPASS fill on **B5a** line in main Q&A (if still empty)

---

**Next COMPASS action:** Acknowledge Track C closed for Alex purposes; fold §3 into Round 4 plan; prompt Charles for remaining Round 3 decisions when he surfaces from Alex day.
