# SCOUT review — CCT Campaign Plan

**Date:** 2026-08-21  
**Reviewer:** SCOUT  
**Document:** [`CCT_Campaign_Plan.md`](CCT_Campaign_Plan.md)  
**Context:** Charles briefed Alex on **fix Â_i** — Alex excited. Campaign plan is operational go-forward doc.

---

## Verdict

**Approved — ready for Charles green-light on Priority 1 spec.** Plan matches porch reading (SCOUT-approved), BINDING rules, BDP Act I closure, and existing script paths. **Four engineering patches** applied directly in `CCT_Campaign_Plan.md` (§4 CLI, winsor, QC note, status log). **No scientific forks** with COMPASS.

---

## Endorsements (scrubbed)

| Section | SCOUT read |
|---------|------------|
| §0–1 Campaign arc / win condition | ✓ Correct — conditional not marginal; bin-16 dip explicitly not win condition |
| §2 Guardrails | ✓ Matches BINDING + porch + BDP QC rules |
| §3 Plot menu priorities 1–5 | ✓ Same as porch §10; build order sensible |
| §4 Engineering | ✓ **Patched** — see below |
| §5–6 Checklist / ownership | ✓ Charles-only checkboxes; SCOUT deliverable clear |
| §7–8 Captions / Alex paragraph | ✓ Binding-safe; consistent with porch §12 |
| §9 Do-not-do | ✓ |
| §11 Open decisions | ✓ Defaults reasonable; **await Charles lock** before build |

---

## Patches applied in campaign plan (SCOUT)

1. **CLI `--min-games 11` → `--min-team-season-games 10`** — Repo convention: `mg10` = config value **10** (drop team-seasons with **≤10** games; keep **11+**). Not a literal CLI value of 11.

2. **Added locked hero winsor** — Priority 1 / CLI: `poolq_winsor_quantiles=(0.01, 0.99)` to match POST-QC hero and `pass_a_empirical_bundle` defaults. BDP Â/T̂ plots intentionally omit winsor; **CCT draft-rate plots should not**.

3. **QC baseline explicit** — `drop_dash_placeholder_names=True` always on (Charles BDP rule); separate from mg10.

4. **Fixed incremental-writes link** — `../../../.cursor/rules/incremental-writes.mdc` (repo root from this folder).

5. **Status log** — Alex briefed; SCOUT review complete.

---

## Spot-checks (numbers referenced in plan)

| Item | Verified |
|------|----------|
| Panel n ≈ 46,306 PS, ~1,133 drafts at mg10 min20 PPM | ✓ BDP JSON |
| Draft rate ~2–2.5% | ✓ 2.45% |
| MLE λ̂ ≈ 2.6, t̂ ≈ 1.1 | ✓ pd21_mle JSON |
| Reuse paths: `pd20_22_campaign_window`, `hero_gallery_paths`, `pass_a_empirical_bundle` | ✓ modules exist |
| Output dir `basic_data_plots/` | ✓ BDP convention |
| Do not clobber `pass_a/` canonical PNGs | ✓ |

---

## SCOUT build notes (for §4 when green-lit)

**Priority 1 implementation sketch:**

1. Build panel via same path as `pass_a_empirical_bundle` (`PipelineConfig`: mg=10, min20, dash QC, winsor 0.01–0.99).
2. Filter to Â_i ∈ [lo, hi] **after** z-scoring within season (PPM default).
3. Bin **poolq_loo** into ventiles **within the filtered subset** (document n per bin in JSON).
4. Compute draft rate + Wilson or binomial CI; flag bins with n < 30 (plan says warn at 30, no claims at n < 10).
5. Optional secondary panel: same Â band, **T̂_j** ventiles (not LOO — label clearly in caption).

**Risk SCOUT flags upfront:** Â band [1.5, 2.0] may yield **thin bins** (~few hundred PS total, ~10–20 drafts). JSON cell counts mandatory; Charles may need top-decile or wider band (§11). Heatmap (P2) may be more stable than bar chart if P1 bins are sparse.

**Alex briefed:** No code until Charles checks Phase 0 box **Priority 1 spec locked** — even with Alex excited, spec lock prevents wrong-axis rebuild.

---

## Open questions for Charles (not blockers)

| # | Question | Default if silent |
|---|----------|-------------------|
| 1 | Â band [1.5, 2.0] OK? | Use default |
| 2 | Primary axis poolq_loo only, or dual panel with T̂_j? | poolq_loo only first |
| 3 | 16 ventiles vs 10 for draft-rate bins? | 16 (hero match) |
| 4 | 2011–2021 vs 2013–2021 sensitivity later? | 11_21 locked panel |

---

## Phase 0 checklist (SCOUT update)

| Item | Status |
|------|--------|
| SCOUT reviewed campaign plan | ✓ **This file** |
| Charles green-light on build | ⏳ Awaiting Charles |

---

**Bottom line:** COMPASS plan is execution-ready. Charles: lock §11 defaults (or override in one line), check Phase 0 **go**, SCOUT ships Priority 1 PNG + JSON + `basic_data_plots/CCT_README.md`.

— **SCOUT**
