/scaffold# DISPOSABLE — Legends (LoL) hero thread (2026-09-03)

**Purpose:** YOU ARE HERE for Charles + COMPASS **Legends / League of Legends** HERO work.  
**Data:** [`datasets/legends/lol_big_fish_player_split_panel.csv`](../../../../datasets/legends/lol_big_fish_player_split_panel.csv)  
**Column map:** [`datasets/legends/README.md`](../../../../datasets/legends/README.md)  
**LoL primer:** [`LEGENDS_LoL_primer_for_researchers.md`](LEGENDS_LoL_primer_for_researchers.md)  
**Cross-dataset context:** [`../_DISPOSABLE_big_fish_datasets_assessment.md`](../_DISPOSABLE_big_fish_datasets_assessment.md)  
**Say `anchor`** in chat to paste the table below.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | Big Fish assessment incl. Apache | ✓ — see parent disposable |
| **1** | **Sandbox scaffold** (this folder + README) | ✓ (2026-09-03) |
| **2** | **Cohort lock** — dev rows, censor flags, Y window | ✓ v0 locked (N=1,879 · Y2 37%) |
| **3** | Basic data plots (Â vs T̂_j analog, pond LOO hist\|ECDF) | ✓ (2026-09-04) |
| **4** | Reigning HERO porch — LOO bins × promotion rate | ✓ Q16 porch (2026-09-04) |
| **5** | Act II probes (CCT band, elite pond) — scaled gates | ✓ z∈[1,2] · top 20% (2026-09-04) |
| **6** | 3×3 data story mosaic (optional, Alex screening) | ✓ `LEGENDS_DATA_STORY_3x3.png` |

**Alex one-liner (Sep 2):** LoL panel from Oracle’s Elixir; **developmental → top-tier** promotion as Y; `teammate_mean_performance_excl_self` as pond LOO; more roster swapping than MBB.

---

## Cohort lock (v0 — used in data story 2026-09-04)

| Choice | Proposed v0 | Rationale |
|--------|-------------|-----------|
| **Rows** | `league_tier == "developmental"` AND `eligible_developmental_cohort == True` | ~16K dev stints; clean promotion ladder |
| **Â** | `own_performance_index` | Alex composite; require `performance_components_available` |
| **Peer LOO** | `teammate_mean_performance_excl_self` | 91.7% fill; primary pond context |
| **Y** | `top_tier_debut_within_2y` | More events than 1y (4,456 vs 3,052); still use censor |
| **Censor** | Require `full_2y_followup == True` before treating False as non-promotion | Avoid false negatives |
| **Exclude** | `prior_top_tier_before_period == True` | Already pro — not dev-to-pro story |

**Not yet locked:** split vs calendar year aggregation; position fixed effects; same-role LOO as sensitivity only (26.6% fill).

---

## HERO / pond frame

| Our term | Legends column |
|----------|----------------|
| Unit | `player_period_id` |
| Pond | team in dev split (`teamid`, `team_roster_players`) |
| Own Â | `own_performance_index` |
| Peer LOO | `teammate_mean_performance_excl_self` |
| Y (advancement) | `top_tier_debut_within_1y` / `_2y` |
| Environment ≠ advancement | `league_tier` separates pond tier from promotion outcome |

**Binding:** Score (performance index) ≠ select (PMC-style top-tier slot) — same separation as MBB draft / tenure.

---

## Folder layout (target)

```
legends_sandbox/
  _DISPOSABLE_legends_hero_thread.md   ← this file
  README.md
  basic_data_plots/                    ← LEGENDS_BDP_*.png
  pass_a/                              ← HERO porch outputs
  act2/                                ← CCT / elite pond probes
  data_story/                          ← 3×3 manifest + mosaic ✓
```

**Scripts (future):** `legends/scripts/legends_basic_plots.py`, `legends_pass_a_hero.py` — parallel to `tenure/scripts/`, `sports/scripts/`.

---

## Panel N sanity (why MBB knobs won’t copy verbatim)

| MBB habit | Legends reality |
|-----------|-----------------|
| Top 7% Â elite pond | Check dev-cohort top 7% N after filters |
| z ∈ [2, 3] CCT band | Likely too thin — plan scaled band (e.g. z ∈ [1, 2]) like tenure PD29 |
| Last-PS season window | Split-based stints; may need year+split rules |

Run counts in step 2 before locking Act II gates.

---

## Thread log

| Date | Entry |
|------|-------|
| 2026-09-03 | Thread opened; legends chosen as sole Big Fish focus; cohort lock drafted. |
| 2026-09-04 | Full 3×3 data story built (`LEGENDS_DATA_STORY_3x3.png`); cohort v0 locked N=1,879. |
