# MBB — first season at school for **sorting only** (design lock)

**Status:** Charles decisions **2026-10-04** — document before code.  
**Audience:** Charles, Alex-facing prose, agents (COMPASS / SCOUT / implementation).  
**Binding cross-ref:** [`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../3-Master_Plan/BINDING_Selection_is_its_own_step.md) — environment (`poolq_loo`) ≠ score (`A_i`) ≠ select (top K).

---

## One-sentence estimand

When the **first-season-at-school sort** mode is on, **ranking / ability ventiles / sim `A_i`** use **raw PPM from the player’s first NCAA season at the current `team_id`**, with a **minutes floor**; **leave-one-out teammate pool quality (`poolq_loo`) stays exactly the reigning same-season definition** and is **not** rebuilt from freshman PPM.

This is **not** pre-NCAA recruiting latent ability. It is the earliest **observed** production **after** joining that program, still confounded by role and minutes.

---

## Locked decisions (Charles, 2026-10-04)

| # | Decision | Choice | Rationale (short) |
|---|----------|--------|-------------------|
| D1 | **Which “first season”?** | **First season at current school** = minimum `season` among panel rows with the same `(athlete_id, team_id)`. | Matches “incoming to this program” better than global career-first season (transfers). |
| D2 | **Ability measure for sort** | **Raw PPM** = `points / minutes` on that first-at-school player-season row (panel column `ppm` if present, else recompute from `points`, `minutes`). **No** within-season z-score on this sort column unless a **separate** sensitivity flag is added later. | Charles asked for raw PPM, not z-scored hero `perf`. |
| D3 | **Minutes gate (sort only)** | Apply a **minutes floor on the first-at-school row only** before accepting that PPM as sort ability. Numeric floor: **TBD — see open questions** (default candidate = reigning `min_minutes = 20`). | Avoid zero-minute / noise freshman rows; gate applies to **sort**, not necessarily identical to analysis row filters. |
| D4 | **LOO / `poolq_loo`** | **No change.** LOO is computed from **same-season** ability used today (typically season `ppm` → `perf`, optional within-season z per existing hero spec). | Congestion / peer context remains **contemporaneous** for the `(team_id, season)` of each row — “selection year or not” does not switch LOO to freshman PPM. |
| D5 | **Score vs select** | This mode only replaces **`A_i` / sort input** (and derived **ability ventiles**). **Selection** (top K, lex tie-break) and **hero right panel** (`poolq_loo` bins) follow existing rules. | BINDING: score ≠ select; hero outcome panel ≠ score arm. |
| D6 | **Documentation** | Any run with this mode must stamp **provenance** (plot footer, JSON, export slug) with an explicit tag, e.g. `sort=first_ps_at_school_raw_ppm`. | Prevents accidental comparison to reigning last-ps z-PPM curves. |

---

## Definitions (implementation must match prose)

### First season at current school

For each row with keys `(athlete_id, team_id, season, …)`:

1. Restrict to the athlete’s rows at **that** `team_id` (ignore seasons at other schools).
2. Let `season_first(team) = min(season)` over those rows **after** the same panel hygiene used for the run (dash names, team-season game count, etc.) — **document whether min is pre- or post- `min_team_season_games`** in code comments and provenance; default recommendation: **post team-season game filter** so fragmentary one-game schools do not define “first season.”
3. The **sort PPM** for that `(athlete_id, team_id)` pair is the PPM on the row with `season == season_first(team)`.

**Transfers:** A player who moves from School A to School B gets **separate** first-at-school PPM for A and for B. Cross-school hero rows use the sort value for the **team on that row**.

**Redshirt / sit-out:** If the panel has no row until year 2, “first season at school” is the **first season appearing in data**, not calendar eligibility.

### Raw PPM

\[
\text{PPM}_{i,\text{first@school}} = \frac{\text{points}_{i,\text{first@school}}}{\text{minutes}_{i,\text{first@school}}}
\]

Use finite minutes only; if minutes `<` floor or non-finite → sort ability **missing** for that `(athlete_id, team_id)` (see open questions for fallback).

### Same-season LOO (unchanged)

For each player-season row `(athlete_id, team_id, season)`:

\[
\text{poolq\_loo}_{i,t} = \frac{1}{|T_{t\setminus i}|} \sum_{j \in T_{t\setminus i}} \text{perf}_{j,t}
\]

where `perf_{j,t}` is the **existing** season-level measure (e.g. z-scored `ppm` in reigning Pass A), **not** freshman-at-school PPM.

---

## Required two-column architecture (do not overwrite `perf` in place)

Today `apply_perf_metric_for_analysis` sets **`perf`** then recomputes **`poolq_loo` from `perf`**. If freshman PPM were copied into **`perf`**, LOO would silently become “mean teammate freshman PPM,” violating **D4**.

**Required pattern when sort mode is on:**

| Column | Role |
|--------|------|
| `perf` (or `perf_loo`) | Same as reigning — drives **`poolq_loo` / `poolq_sq` only** |
| `sort_ability` (name TBD) | First-at-school raw PPM (post minutes floor) — drives **ability ventiles**, **`A_i` in sim/replay**, any **left-panel** Pass A binning |

Plots and JSON must label which column each panel uses.

---

## Scope (what this mode is for)

| In scope | Out of scope (unless new Charles order) |
|----------|----------------------------------------|
| Pass A **left** panel (ability bins) | Recruiting / HS composites |
| Empirical selection replay **`A_i`** | Changing **`Y_draft`** or draft timing |
| Generative / ASSORT **`ability`** column in prepared CSVs | Replacing **`poolq_loo`** with HS or freshman peer pools |
| Sensitivity vs reigning sort | Claiming true pre-NCAA latent talent |

---

## Comparison to reigning hero (default off)

| | Reigning (default) | First-at-school sort mode |
|--|-------------------|---------------------------|
| Sort / ability | Season `perf` (often **within-season z** of `ppm`) | **Raw PPM**, first season **at that `team_id`** |
| LOO | Same-season `perf` | **Unchanged** (same-season `perf`) |
| Estimand | Contemporaneous production + peer context | **Early-at-program** production for rank; **contemporaneous** peers for congestion |

---

## Open questions (Charles — need answers before merge)

1. **Minutes floor value:** Use reigning **`20`** minutes on the first-at-school row, or a **different** floor (e.g. 50 for freshman only)?
2. **Missing sort ability:** If first-at-school row fails the floor, is the player **dropped from sort/ventiles**, **NaN excluded from top-K**, or **fallback** to same-season PPM (would violate “raw first season only” unless labeled)?
3. **`season_first` timing:** Confirm **post-`min_team_season_games`** (recommended) vs raw box min season.
4. **Panel grain:** For **last-ps** hero, attach one `sort_ability` per athlete on the last row — confirm. For **all-ps** replay, attach constant `sort_ability` on every row for `(athlete_id, team_id)` — confirm.
5. **ASSORT prepared panels:** Regenerate `ability` from this column for mechanism runs, while **`peer` / congestion** fields stay on same-season logic — confirm separate prep script vs inline flag.
6. **Provenance slug:** OK with `sort=first_ps_at_school_raw_ppm` + `loo=same_season_perf` in filenames?

---

## Implementation checklist (when authorized)

- [ ] `PipelineConfig` (+ CLI): `sort_first_season_at_school: bool = False`, `sort_min_minutes: float`, document in `config.py` docstring → **this file**.
- [ ] `panel_build.assign_first_season_at_school_sort_ability(...)` — returns `sort_ability`; does **not** alter LOO path.
- [ ] `apply_perf_metric_for_analysis` **or** parallel `apply_perf_and_sort_for_analysis` — LOO first from season metric, then attach sort column.
- [ ] Pass A / provenance stamps per **D6**.
- [ ] Unit test: synthetic transfer (two schools) → two sort values; LOO unchanged when sort flag toggled.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-10-04 | Initial lock from Charles: (1) first season **at current school**, (2) **raw PPM + minutes floor**, (3) **no LOO change** — contemporaneous season only. |
