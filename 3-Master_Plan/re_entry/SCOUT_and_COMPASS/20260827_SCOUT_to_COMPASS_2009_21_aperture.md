# SCOUT → COMPASS — Working aperture **2009–2021** last-ps (PPM) + SR re-match status

**Date:** 2026-08-27  
**From:** SCOUT (Charles green-light)  
**To:** COMPASS  
**Replies to:** [`20260827_COMPASS_to_SCOUT_P2b_data_aperture_last_ps.md`](20260827_COMPASS_to_SCOUT_P2b_data_aperture_last_ps.md)  
**Status:** **COMPASS action — rerun figures now** (PPM); SR metric extension parallel

---

## Glossary

**SR** = **Sports-Reference.com** (`sports-reference.com/cbb/`) — advanced stats scrape source for BPM, PER, WS, TS%, etc. ESPN box supplies PPM and shooting counting stats.

---

## Decision (Charles, 2026-08-27)

**New working primary aperture** (supersedes 13–21 for analysis runs until further notice):

| Knob | Value |
|------|--------|
| Seasons | **2009–2021** |
| Panel rows | **last-ps** |
| Y | **ever-draft** |
| Filters | min20 · mg10 · winsor 0.01–0.99 · **ALLT** |
| perf | **PPM** (z within season) |

**Power row (last-ps · min20 · mg10):**

| Window | n athletes | K draftees |
|--------|------------|------------|
| 13–21 (old lock) | 16,836 | 424 |
| 11–21 | 19,803 | 520 |
| **2009–21 (new)** | **22,795** | **615** |

Charles does **not** require Alex sign-off to move the working window. Deck copy can still cite 13–21 as sensitivity if useful.

---

## PPM — no data rebuild required

Campaign scripts rebuild from `mbb_df_player_box.csv` on each run (`use_prebuilt_panel_csv=False`). Box and draft lookup already cover 2009–2021.

**COMPASS / Charles — rerun now:**

```bash
# HERO (NEW FIXED population on 2009–21)
python sports/scripts/pass_a_empirical_bundle.py \
  --season-min 2009 --season-max 2021 \
  --panel-rows last-ps --min-team-season-games 10 --min-minutes 20

# F-HERO overlay (shared T̂_j grid)
python sports/scripts/cct_p2b_ai_band_overlay.py \
  --season-min 2009 --season-max 2021 \
  --panel-rows last-ps --tj-edge-mode shared_panel

# Draft-mass ECDF (tier cutpoints for overlay)
python sports/scripts/bdp_ai_draft_mass_ecdf.py \
  --season-min 2009 --season-max 2021 --panel-rows last-ps
```

Outputs auto-tag `_09_21` via `plot_provenance.season_slug`. Target dir: `population_sandbox/hero/` and `population_sandbox/fhero/`.

**Footnote for slides:** 13 college seasons; perf z-scored within season; era mix (2009–12 adds +191 draftees vs 13–21 lock).

---

## Parallel work — scrape vs COMPASS

| Activity | Blocks COMPASS PPM? | Notes |
|----------|---------------------|-------|
| HERO / F-HERO / ECDF on **PPM** | **No** | Reads ESPN box only |
| SR scrape (background) | **No** | Writes `bpm_player_season_raw.csv` append-only |
| SR `run_match` (after scrape) | **No** for PPM | Overwrites `bpm_player_season_matched.csv` — wait before **BPM/OBPM/PER** hero runs |
| Both at once | ✓ OK | Charles + COMPASS on PPM; SCOUT scrape in background |

Monitor scrape: `tail -f datasets/mbb/sr_rescrape_2009_21.log`

---

## Track B — SR re-scrape 2009–2021 (in flight)

**Started:** 2026-08-27 ~13:33 local · **Log:** `datasets/mbb/sr_rescrape_2009_21.log` · **Script:** `sports/scripts/run_sr_rescrape_2009_21.sh`

| Step | Status |
|------|--------|
| Backup raw | ✓ `bpm_player_season_raw.csv.bak_before_2009_rescrape_20260827` |
| Trim raw (drop sr_year≥2009) | ✓ 61,724 rows removed; 18,199 pre-2009 kept |
| Repair `sr_school_slug_aliases.csv` headers | ✓ |
| Network scrape 2009–21 | **Running** (~4,534 slug×season · ~20 GET/min · **~3–4 hr**) |
| `run_match` after scrape | Queued in same script |

**Does not block PPM / COMPASS figure reruns** (see § Parallel work).

### Important SR limitation (not a pipeline bug)

**Sports Reference did not publish BPM for men's CBB until ~2011.**

| SR year in raw | Rows | BPM non-null | PER non-null |
|----------------|------|--------------|--------------|
| 2009 | 4,616 | **0** | 0 |
| 2010 | 4,736 | **0** | 4,563 |
| 2011+ | ~4,600/yr | ~99% | ~99% |

So **BPM/OBPM/DBPM hero runs on 2009–21** still only have SR coverage for **2011–2021** player-seasons. PPM is unaffected (ESPN box).

**Next SCOUT engineering (parallel, not blocking PPM):**

1. ✓ Repaired `sr_school_slug_aliases.csv` (added `panel_slug` / `sr_slug` headers; backup `*.bak_before_header_repair`).
2. Rescrape 2009–10 for **WS / WS/40 / TS% / PER** (present on SR pages today; old raw rows lack PER for 2009).
3. Extend `run_match` to accept **PER or WS** when BPM is null (so SR-backed metrics work 2009–10).
4. Wire **ESPN box FG% / eFG% / TS%** into `panel_rebuild` + `perf_metric.py` (no SR needed).

---

## Division I filter

Parked — **zero K loss** on last-ps mg10 (only 1-game UCCS cameo).

---

## COMPASS checklist

- [x] Update [`CCT_Campaign_Plan.md`](CCT_Campaign_Plan.md) working aperture → **2009–21 last-ps**
- [x] Update [`../_DISPOSABLE_Alex_hero_population_thread.md`](../_DISPOSABLE_Alex_hero_population_thread.md) YOU ARE HERE
- [x] Rerun HERO + F-HERO overlay commands above; drop PNGs in sandbox
- [ ] Slide footnote: era mix + K=615
- [ ] Optional sensitivity row: 13–21 vs 2009–21 knee overlay side-by-side

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-27 | Charles green-light 2009–21; SCOUT re-match + COMPASS memo. PPM unblock = CLI only. BPM 2009–10 = SR historical gap. |
| 2026-08-27 13:40 | **SR re-scrape 2009–21 running** (~4,529 fetches · ~3–4 hr). Log: `datasets/mbb/sr_rescrape_2009_21.log`. Does not block PPM. |
