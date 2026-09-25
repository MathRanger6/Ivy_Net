# MBB assortativity — empirical sorting, pools, and PPM (SCOUT)

**Prepared:** September 25, 2026  
**For:** Charles / VECTOR  
**Lane:** SCOUT — saved artifacts, repo paths, execution gaps.  
**Status:** Read-only. No runs in this note.

**Use with (same folder, separate memos):** [VECTOR](20260925_MBB_Assort_issue_thoughts_VECTOR.md) (interpretation, math, bounded audit); [COMPASS](20260925_MBB_Assort_issue_thoughts_COMPASS.md) (framing, hypotheses, campaign).  
**Hygiene / PPM construction:** [SCOUT data-hygiene response](../source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md) §3.6.

---

## Evidence tags

| Tag | Meaning |
|-----|---------|
| **[Direct repo]** | Code, config, or file in repository today |
| **[Saved result]** | Named artifact; not re-run here |
| **[Meeting record]** | Charles–Alex conversation Sep 25, 2026 (summary only) |
| **[Gap]** | Not in repo or blocked |

---

## 1. Charles’s question (pointer)

[Meeting record] Pool composition, PPM, five-on-court scarcity, Squid vs Jackals, and “why measured assortativity ≈ 0?” — recorded in VECTOR and COMPASS memos. SCOUT below is **artifact and pipeline facts** only.

---

## 2. Estimand map (repo objects)

[Direct repo] [`BINDING_Selection_is_its_own_step.md`](../../../../BINDING_Selection_is_its_own_step.md); [`GRANDCHILD_D_and_H_sort_interpretation.md`](../../../../../re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md); [`pd21_rho_hsort_calibrate.py`](../../../../../../sports/scripts/pd21_rho_hsort_calibrate.py); [`panel_rebuild.py`](../../../../../../sports/sports_pipeline/panel_rebuild.py); [`panel_build.py`](../../../../../../sports/sports_pipeline/panel_build.py).

| Object | Code / artifact |
|--------|-----------------|
| **$H_{\mathrm{sort}}$** | `realized_sorting_index_H_sort` / PD21 `empirical_h_sort` |
| **$\rho^\*$ bracket** | `PD21_rho_hsort_calibrate_*_fit_bracket.json` |
| **`poolq_loo`** | `recompute_teammate_loo_pool_quality` after `assign_perf_from_metric("ppm")` |
| **Assort sim (paused)** | [`ASSORT_20260925_initial_execution_stop.md`](../source_review/ASSORT_20260925_initial_execution_stop.md) |

---

## 3. Saved $H_{\mathrm{sort}}$ and panel provenance

[Saved result] PD21 brackets, PPM → within-season z, **min20 drop**:

| Artifact | Generated | 2015 empirical $H_{\mathrm{sort}}$ | Provenance note |
|----------|-----------|--------------------------------------|-----------------|
| [`PD21_rho_hsort_calibrate_2015_fit_bracket.json`](../../../../../re_entry/HEROs_and_PASSes/pd21_rho/PD21_rho_hsort_calibrate_2015_fit_bracket.json) | **2026-08-14** | **≈ 0.114** | **Before** mg10 lock (Aug 17) — not current QC panel |
| [`PD21_rho_hsort_calibrate_2013_2021_fit_bracket.json`](../../../../../re_entry/HEROs_and_PASSes/pd21_rho/PD21_rho_hsort_calibrate_2013_2021_fit_bracket.json) | **2026-08-19** | **≈ 0.061** (2015 row) | Post–QC era trace; **$\rho=0$** sim mean **≈ 0.081** same row |
| Same 2013–2021 file | — | **≈ 0.056–0.071** other seasons | Per-season trace in JSON |

[Direct repo] mg10: [`BOX_QC_panel_build_policy.md`](../../../../../re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md) §3b; `config.min_team_season_games = 10`.

[Saved result] Grandchild ρ → $D$ (2015, $C=15$): [`GRANDCHILD_D_and_H_sort_interpretation.md`](../../../../../re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md).

**How to read magnitudes** (z-score vs $H_{\mathrm{sort}}$, random-allocation null, LOO vs partition): **VECTOR memo** — not duplicated here.

---

## 4. Panel counts and PPM facts (Sep 25 rebuild)

[Saved result] `build_from_box`, mg10 + dash + **min20**, all seasons in box:

| Quantity | Value |
|----------|--------|
| Player-season rows | 88,399 (2005–2025) |
| Team-seasons | 7,325 |
| Mean eligible roster size | **≈ 12.1** |
| **2015** team-seasons | 351 |
| **2015** mean roster size | **≈ 12.2** |

Zero PPM after min20 (PPM = 0 ⟺ 0 points, ≥20 season minutes):

| Scope | Mean per team-season | Share of teams with ≥1 |
|-------|----------------------|-------------------------|
| All seasons | **≈ 0.05** | **≈ 4.6%** |
| 2015 | **≈ 0.08** | **≈ 7.7%** |

[Direct repo] PPM not in game CSV; computed at aggregation — [hygiene §3.6](../source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md).

---

## 5. Hero / QC artifacts (tail, not $H_{\mathrm{sort}}$)

[Saved result] Post–QC Pass A pair and CPR tables: [hygiene response](../source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md) §§2, 7; [`reigning_hero/README.md`](../../../../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md) (different spec: last-PS, EW16, 09–21).

[Saved result] Sep 2026 perf-metric LOO batch — PPM retained for hero shape gate: `sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/LOO_SHAPE_REPORT.md` (path per campaign docs).

---

## 6. Checklist → evidence location (SCOUT column only)

| Charles question | Repo fact |
|------------------|-----------|
| Metric | PPM z; PD21 JSON §3; hygiene §3.6 |
| Min20 | `panel_rebuild` after aggregation; production lock in hygiene §3 |
| Mg10 | `panel_rebuild._apply_box_qc`; Pass A sensitivity README |
| D-I only | **[Gap]** no season-specific membership crosswalk in panel builder |
| Draft-ever teams | `restrict_teams_by_draftees` in config — hero path; not assort main spec |
| Assort experiment | **Stopped** — [execution stop](../source_review/ASSORT_20260925_initial_execution_stop.md) |

---

## 7. Gaps and blocked work (SCOUT)

1. **2015 assort population** — canonical-team + partial points/minutes rows unresolved ([execution stop](../source_review/ASSORT_20260925_initial_execution_stop.md)).  
2. **Per-game rotation audit** — not run; proposed in VECTOR memo.  
3. **Permutation $H_{\mathrm{sort}}$ null** on frozen population — not in repo.  
4. **Transfer rows** at `(athlete_id, season, team_id)` — **[Gap]** no saved 2015 audit vs last-team-only rule.  
5. **Assort 100× repetitions** — not started.

**Next steps / hypotheses / audit design:** VECTOR and COMPASS memos.

---

## Thread log

- **2026-09-25** — Initial SCOUT artifact note.  
- **2026-09-25 (pm)** — Trimmed to SCOUT-only facts; interpretation lives in VECTOR + COMPASS.

---

*SCOUT — evidence and gaps. Read all three memos in `docs/scientific_questions/`.*
