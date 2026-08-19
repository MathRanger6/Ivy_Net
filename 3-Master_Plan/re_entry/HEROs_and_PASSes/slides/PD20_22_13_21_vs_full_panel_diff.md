# PD20–22: 2013–2021 vs full panel (2011–2021) — side-by-side diff

**Purpose:** Compare AUTO outputs while `./scripts/regenerate_pd20_22_auto_13_21.sh` runs.

| Full panel (current) | 2013–2021 contrast |
|----------------------|-------------------|
| PNG/JSON `*_2011_2021.*` | PNG/JSON `*_2013_2021.*` |
| AUTO `*_AUTO.pptx` | AUTO `*_13_21_AUTO.pptx` |
| 11 seasons | **9 seasons** (drops **2011, 2012**) |

**Alex lock (PD23):** 2011–2012 = ESPN depth / data-quality; primary analysis **2013+** is defensible. This run tests whether the **story** survives the trim.

---

## How to compare

1. Open pairs from `slides/auto/` (same slide family, different suffix).
2. For figures, diff PNGs in `pd20_temperature/`, `pd21_rho/`, `pd22_minutes/`.
3. Read subtitles first — almost every pooled slide should say **2013–2021** not 2011–2021.
4. **Qualitative arc** matters more than 3rd decimal on H_sort.

Legend: **Δ** = expected visual/numeric change · **≈** = same story, maybe relabel · **●** = watch closely

---

## HAND deck (21 slides)

### Act I — PD20 Gibbs gate (1–4)

| Slide | Topic | Δ? | What to check |
|------:|-------|----|----------------|
| 1 | Gibbs SELECT intro | ≈ | Text slide — no panel window |
| 2 | Temperature sweep | **● HIGH** | Inverted-U counts are **per-season stacks** → 9 seasons not 11; curves at λ=1.5/2.0 may shift slightly; subtitle season count |
| 3 | Cold limit C vs D | **MED** | Same λ,t point — shape should match; meta window label |
| 4 | PD20 takeaways | ≈ | Bullet text may still say 2011–2021 unless HAND edited — AUTO unchanged in substance |

**Story test:** Does rule D still beat rule C at cold t? (Should yes.)

---

### Act II — Why the hero panel exists (5–13)

| Slide | Topic | Δ? | What to check |
|------:|-------|----|----------------|
| 5 | Roster size before QC | **MED** | Team-season **N** drops (~18% fewer seasons); tail shape (BYU spike) should still appear if 2011–12 had worst junk |
| 6 | Games/team-season before QC | **MED** | One-game season share — 2011–12 may have contributed; median may move |
| 7 | Games/team-season after QC | **MED** | Same as 6 post-filter |
| 8 | Roster size after QC + min-20 | **MED** | Post-QC cluster near dress cap 15 — main message ≈ |
| 9 | ESPN coverage 2013→2014 | **● HIGH** | **Key slide for trim:** 2011–2012 bars **gone**; 2013→2014 step should remain the headline; x-axis is shorter |
| 10 | Drafted-player retention | **LOW–MED** | **Draft-safe floor** logic unchanged; lost-at-20 count may differ slightly (fewer player-seasons in pool) |
| 11 | Raw minutes distribution | **MED** | Pooled histogram/CDF — fewer rows; drafted vs all mix |
| 12 | PPM distribution | **MED** | Sub-20 tail counts scale down; **PPM > 1** outlier count may drop |
| 13 | PPM overlay full vs filtered | **MED** | Same overlay logic; numeric callouts in bullets |

**Story test:** Box QC + min-20 still justified? Draft-safe at min=0? (Should yes.)

---

### Act III — ρ calibration (14–16)

| Slide | Topic | Δ? | What to check |
|------:|-------|----|----------------|
| 14 | Hero ρ bracket (locked) | **● HIGH** | **Main scientific object:** longitudinal ρ*, mean H_sort, **9/9 vs 11/11** seasons at ρ*=0; bracket small multiples lose 2011–2012 columns |
| 15 | ppm0lt20 contrast bracket | **● HIGH** | Longitudinal ρ* was ~0.05 full panel — may move; **2014→2015 spike** still there (both seasons kept) |
| 16 | ppm0 ρ* timeseries | **● HIGH** | Two fewer points at left; spike at 2014→2015 is the drama — confirm it persists |

**Full-panel reference (Aug 18):**
- Slide 14 hero: ρ*=0 all seasons, H_sort ≈ 0.06
- Slide 15 ppm0: longitudinal ρ* ≈ 0.05, mid-decade spike 2014→2015

**Story test:** Hero still flat ρ*? ppm0 still “wrong estimand” with inflated ρ*? (Expect yes on both.)

---

### Act IV — Policy + overlap (17–21)

| Slide | Topic | Δ? | What to check |
|------:|-------|----|----------------|
| 17 | PPM-zero vs drop ability | **MED** | Distribution comparison — pooled N down |
| 18 | Bench-zero vs H_sort mechanism | **MED** | Per-season std vs ppm-zero fraction — **9 panels** not 11 |
| 19 | Panel policy compare | **● HIGH** | Side-by-side H_sort / ρ* from JSONs — numbers should match slides 14–15 |
| 20 | Overlap season **2012** | **MED** | **Geometry** for 2012 unchanged (single season); **ρ* footnote** now from **9-season** bracket (2012 not in bracket fit) |
| 21 | Overlap season **2013** | **LOW–MED** | 2013 still in window; overlap picture ≈; ρ* annotation may match new bracket |

**Story test:** Drop still beats PPM-zero at slide 19? Overlap still “looks sorted” at ρ*=0 (20–21)? (Expect yes.)

---

## Memo companion deck (~46 slides)

| Block | AUTO file | Δ? |
|-------|-----------|-----|
| Wavetops / Wang arc | `CHAR_PD20_22_takeaways_memo_13_21_AUTO.pptx` | **MED** — prose pulls JSON counts; season labels |
| Snag + Q1–Q3 | same | **LOW** — mostly fixed narrative |
| HAND companions 1–21 | same | **MED–HIGH** where tied to ρ, temp sweep, policy |
| Closing / MLE forward | same | ≈ — MLE is 2013+ anyway |

Diff tip: search memo deck for **“11 season”**, **“2011”**, **“2012”** — should become **9** / absent in pooled claims.

---

## Expected “nothing burger” vs “material shift”

### Should stay the same (if pipeline is correct)

- Gibbs SELECT gate cleared (PD20 Act I logic)
- Drop-at-20 **policy** choice (not ppm-zero)
- Draft-safe max floor ≈ 0 min (slide 10 qualitative)
- Box QC fixes roster tails (5–8 qualitative)
- ρ* ≈ 0 on **hero** panel (slide 14) — Alex said modest fit, not “random NCAA”
- ppm0 contrast **≠** production policy (slide 15 vs 14)
- Overlap geometry persists at ρ*=0 (slides 20–21)

### Might move (report to Alex if large)

- Longitudinal ρ* on ppm0 (slide 15) — was ~0.05
- Per-season ρ* for 2013–2015 on hero — fewer seasons in pool
- Inverted-U **fraction** at λ=1.5, 2.0 (slide 2) — denominator 9 not 11
- Any bullet quoting **team-season N** or **player-season N**
- Memo companions citing **11 seasons at ρ*=0**

### Should **not** block the paper if trim is OK

- Small H_sort drift (0.06 → 0.05x)
- ρ* staying at 0 with wider/narrower bracket error
- Loss of 2011–2012 from pooled charts only

---

## Quick file checklist (when run finishes)

```text
slides/auto/
  CHAR_PD20_HAND_13_21_AUTO.pptx
  CHAR_PD21_rho_hsort_calibrate_13_21_AUTO.pptx
  CHAR_PD21_rho_hsort_calibrate_ppm0lt20_13_21_AUTO.pptx
  CHAR_PD21_rho_hsort_timeseries_ppm0lt20_13_21_AUTO.pptx
  CHAR_PD22_*_13_21_AUTO.pptx          (one per PD22 figure slide)
  CHAR_PD20_22_takeaways_memo_13_21_AUTO.pptx

pd21_rho/
  PD21_rho_hsort_calibrate_2013_2021_fit_bracket.json      ← slide 14 numbers
  PD21_rho_hsort_calibrate_2013_2021_ppm0lt20_fit_bracket.json

pd20_temperature/
  GRANDCHILD_temperature_select_sweep_2013_2021.png          ← slide 2
```

---

## One-liner for Alex (if 2013–2021 matches full panel)

> “We dropped 2011–2012 for ESPN depth. On 2013–2021 the hero panel still gives ρ*≈0 and modest H_sort; ppm0 contrast still misbehaves; drop-at-20 policy unchanged; overlap slides still show stacking at ρ*=0. Primary window is now 2013–2021.”

---

*Generated for contrast run — fill in numeric deltas from JSON after `./scripts/regenerate_pd20_22_auto_13_21.sh` completes.*
