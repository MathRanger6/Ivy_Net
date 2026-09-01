# Reigning hero — slide 12 lock (Aug 2026)

**Status:** Named from 09–21 permutation deck · HAND matrix slide **12**  
**Not** `FIXED_HERO` — discovery deck came first; this is the first **named** hero.

---

## Lock spec

| Field | Value |
|-------|--------|
| **Deck slide** | 12 |
| **output_tag** | `perm_loo_ever_lastps_ew16` |
| **Seasons** | **2009–2021** (`09_21`) |
| **panel-rows** | **last-ps** |
| **y-draft-mode** | **ever** |
| **roster-x** | **poolq_loo** |
| **Binning** | **equal_width · 16** (EW16) |
| **Population** | **ALLT** (no +DFT filter on panel) |
| **Filters** | min20 · mg10 · winsor 0.01–0.99 · PPM z |
| **HAND shape tags** | `robust tail drop` · `tail drop` |
| **LPM (09–21)** | β₂ ≈ +0.00172 (flat / not concave) |

**Canonical PNG (permutation run):**  
`../hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png`

---

## Population split (Charles confirmed Aug 27)

| Plot family | Row set | Same filter chain |
|-------------|---------|-------------------|
| **Â_i · LOO · (marginal T̂_j)** | **last-ps** cross-section | min20 · mg10 · winsor · ALLT · seasons |
| **Interval overlap · roster size** | **all-ps** (full panel) | same |

Overlap and roster size need full team-season rosters; HERO bins use one row per athlete (final season).

---

## `basic_data_plots/` — build list

| # | Artifact | HAND analog | Status |
|---|----------|-------------|--------|
| 1 | Interval overlap (09–21, hero filters) | PD20 ~slide 21 | **Built** — all-ps |
| 2 | Â_i \| T̂_j distributions | BDP slide 7 | **Built** — last-ps |
| 3 | Â_i \| LOO (poolq_loo) distributions | *(new, mirror #2)* | **Built** — last-ps |
| 3b | **T̂_j vs poolq_loo overlay** (density) | *(new)* | **Built** — last-ps |
| 3c | **Player poolq_LOO distribution** (hist + ECDF) | *(Alex Aug 2026)* | **Built** — last-ps |
| 3c′ | **Player poolq_LOO distribution (no winsor)** | *(mirror 3c)* | **Built** — last-ps |
| 3d | **P(Y=1) vs player poolq_LOO** (EW16) | HERO / Pass A | **Built** — last-ps |
| 3e | **P(Y=1) — LOO vs T̂_j side-by-side** | HERO vs team axis | **Built** — last-ps |
| 4 | APGMS + ARGMS draft-rate side-by-sides | Fixed_Ai 11–14 | **Built** — ALLT + orange +DFT |
| 5 | Team games per season | PD22 memo ~slide 27 | **Built** — after box QC |
| 5b | Player + team mean minutes | PD22 minutes (porch) | **Built** — all-ps |
| 6 | Team roster size distribution | BDP slide 18 | **Built** — all-ps |

**Parked:** min1 vs min20 minutes sensitivity (separate from porch minutes above).

---

## BDP convention (item 2 — Charles confirmed)

Where scripts support it: **primary = ALLT** (full panel histogram / bars); **orange overlay = +DFT** team-season subset (same pattern as `bdp_ai_tj_distributions.py` DFT overlay). Not a separate +DFT-only figure unless noted.

---

## `hero_star_sweeps/` — factorial grid

**Fixed:** LOO · ever · last-ps · ALLT · **equal_width** · min20 · mg10 · winsor 0.01–0.99.

| Axis | Values |
|------|--------|
| **n_bins** | 8 · 10 · 12 · 20 · 24 |
| **season window** | `09_21` · `11_21` · `13_21` · `09_19` (2009–2019) |

**20 runs** (5 × 4). Winsor held at 0.01–0.99 for v1.

**After star sweep:** neighborhood left/right, then F-HERO off this lock.

## `fhero/` — paired F-HERO (same population)

**Built** — ECDF + single-band knee + P2b overlay on reigning aperture.

```bash
python sports/scripts/reigning_hero_fhero.py
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_fhero.zsh
```

See [`fhero/README.md`](fhero/README.md) · manifest [`fhero/manifest.json`](fhero/manifest.json).

---

## `calibration/` — PD28 (ρ\*, γ\*, λ\*, temperature)

**Alex ask (Aug 28):** rerun homophily + MLE + Gibbs temperature on **09–21** reigning panel.

```bash
python sports/scripts/reigning_hero_calibration.py
```

See [`calibration/README.md`](calibration/README.md) · compare [`calibration/CAMPAIGN_COMPARE.md`](calibration/CAMPAIGN_COMPARE.md).

| Step | Status |
|------|--------|
| ρ\* (H_sort bracket) | **✓** ρ\* = **0.0** (longitudinal) |
| γ\*, λ\*, t\* (Bernoulli MLE) | **✓** γ\*≈**19.57** · λ\*≈**1.30** · t\*≈**1.07** |
| Temperature sweep | **✓** inverted-U survives at λ=1.5–2, cold/hot t |

Full compare: [`calibration/CAMPAIGN_COMPARE.md`](calibration/CAMPAIGN_COMPARE.md)

---

## `sim_hero/` — empirical roster SELECT → sim HERO (Aug 28)

Frozen NCAA rosters → $S_i = A_i - \lambda^* L^C$ → **Gibbs rule D** (v1 default) → compare sim HERO to empirical on reigning lock.

```bash
python sports/scripts/reigning_hero_sim_hero.py
python sports/scripts/reigning_hero_sim_hero.py --select all   # gibbs + topk + bernoulli
python sports/scripts/reigning_hero_sim_hero.py --gibbs-t-sweep   # overlay PNG + β₂ CSV
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_sim_hero.zsh
```

**Gibbs $t$ overlay:** `REIGNING_SIM_HERO_gibbs_t_sweep_*_last_ps.png` (+ `_beta2.csv`, `.json`).

### Score axis vs HERO axis (do not hide)

| Layer | Object | Reigning v1 |
|-------|--------|-------------|
| **SCORE / SELECT** | $S_i = A_i - \lambda^* L^C$ | `pool_c_smooth_team` (PD21 MLE) |
| **HERO readout** | draft rate vs bin | `poolq_loo` (EW16) |

Cold Gibbs $\approx$ top-$K$ on $S$ → can **over-draft low-LOO** big fish (left-spike on LOO porch). That is a **feature** of the mismatch, not a code bug.

**What to do (pick one for Alex, in order of pragmatism):**

1. **Document + $t_{\mathrm{Gibbs}}\approx 1$ (now)** — lock replay; cite axis mismatch in caption; cold/hot sweep arms show the dial.
2. **Sensitivity: LOO in SCORE** — rerun SELECT with `pool_c_smooth_loo` (or $L^C \propto -\mathrm{poolq\_loo}$) holding $\lambda^*$; same HERO axis. Tests whether alignment fixes cold left-spike without refitting MLE.
3. **Refit MLE on LOO $L^C$** — PD21 with `pool_c_smooth_loo` so fit and SELECT share the HERO congestion definition (bigger lift).
4. **Dual readout** — keep LOO HERO; add sim **F-HERO** on $\hat{T}_j$ (already built under `fhero/`) for team-axis comparison.

Do **not** silently swap axes — score $\neq$ hero is binding.

| SELECT | Role |
|--------|------|
| **gibbs** (default) | $K_s$ from NBA draft lookup · rule D · $t_{\mathrm{Gibbs}}=1$ |
| **topk** | Sensitivity — deterministic rule C |
| **bernoulli** | Sensitivity — MLE $p_i$ coin flips (variable $K$) |

**First Gibbs run (09–21):** sim ever-drafted **617** vs emp **615** on last-ps; LPM $\beta_2$ emp **+0.00172** vs sim **+0.00004** (both flat).

---

## Folders

```text
reigning_hero/
  README.md              ← this file
  basic_data_plots/      ← porch diagnostics (items 1–4, 6)
  calibration/           ← PD28 ρ / MLE / temperature (09–21 all-ps)
  sim_hero/              ← empirical roster Gibbs SELECT → sim HERO
  hero_star_sweeps/      ← 20-run EW bin × season grid
  fhero/                 ← paired F-HERO (T̂_j axis)
```

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-27 | Slide 12 named reigning hero from 09–21 perm deck + HAND matrix. Population split agreed. APGMS: ALLT + DFT overlay. Games/minutes porch plots parked. Star sweep 5×4 confirmed. |
| 2026-08-27 | **basic_data_plots/** built (5 plot families, 6 PNGs) via `reigning_hero_basic_plots.py`. |
| 2026-08-27 | **basic_data_plots/** auto deck — `REIGNING_BDP_slides_AUTO.pptx` via `build_reigning_hero_basic_plots_slides.py`. |
| 2026-08-27 | **hero_star_sweeps/** complete — 20 EW×season runs, manifest `complete=true`. |
| 2026-08-27 | **fhero/** — paired F-HERO on reigning population via `reigning_hero_fhero.py`. |
| 2026-08-28 | **PD28** — Alex: ρ\*, γ\*, λ\*, temperature on reigning panel; `calibration/` scaffold + `reigning_hero_calibration.py`. |
