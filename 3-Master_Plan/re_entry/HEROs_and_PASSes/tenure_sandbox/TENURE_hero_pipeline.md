# Tenure hero pipeline — MBB mirror (use existing panel first)

**Last synced:** 2026-09-01

**Audience:** Charles + COMPASS (Mac analysis).

**Standalone:** Step-by-step map from rsync’d `faculty_panel_with_pools.jsonl` to tenure HERO plots, mirroring MBB post–re-entry work without re-scraping.

**MBB analogue doc:** [`../MBB_empirical_roster_select_replay.md`](../MBB_empirical_roster_select_replay.md)

---

## Side-by-side ladder

| Rung | MBB (done or in progress) | Tenure (this campaign) |
|------|----------------------------|-------------------------|
| **Data spine** | MBB panel CSV / exports | `faculty_panel_with_pools.jsonl` |
| **Pass A HERO** | `pass_a_empirical_bundle.py` → `sports_sandbox/hero/` | `tenure_pass_a_hero.py` → `tenure_sandbox/hero/` |
| **Pass A F-HERO** | `pass_a_congestion_conditional.py` → `fhero/` | **Act II** — T̂_j at fixed Â (pending lock) |
| **ρ / H_sort** | Reigning hero calibration; ρ* ≈ 0 → park for MBB | **Act III** — run diagnostic; park only if flat |
| **Generative replay** | `reigning_hero_sim_hero.py` | **Act IV** — after Alex lock |
| **Scrape / expand** | Box QC, min20, mg10 | **Parallel** — PEER on Rivanna when scheduled |

---

## Step 0 — Confirm Mac has panel (once per session)

```bash
./scripts/rsync_pull_recent_hpc.sh tenure   # if unsure
ls -lh tenure/tenure_pipeline/faculty_panel_with_pools.jsonl
```

See [`20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md`](../../20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md).

---

## Step 1 — Inference filter (strict v0)

From person–year rows, keep rows where:

- `match_confidence` ∈ **{HIGH, MEDIUM}**
- `poolq_loo_mean` is not null (on assistant rows used for LOO)
- `ever_assistant` is true

**Do not** hero-plot raw 106K without understanding OpenAlex NONE tier (62K person–years).

---

## Step 2 — Collapse to person-level (HERO grain)

Same logic as `tenure/tenure_pipeline/stage9_analysis.py`:

1. One record per `faculty_id`
2. **`loo_mean`** = mean of `poolq_loo_mean` over **assistant** years with non-null LOO
3. Drop persons with no computable LOO assistant years
4. Person flags: `tenure_event`, `attrition`, `censored`

---

## Step 3 — Outcomes (Option A — locked for v0)

**Resolved** = tenure OR attrition (known ending).

| Rate | Numerator | Denominator |
|------|-----------|-------------|
| Tenure rate | `tenure_event` | resolved in bin |
| Attrition rate | `attrition` | resolved in bin |

**Censored:** report `n_censored` per bin; **exclude** from rate denominator. Survival / Cox later.

---

## Step 4 — Bin and plot

| Knob | v0 |
|------|-----|
| X | Person-level `loo_mean` |
| Method | Quantile (equal **people** per bin) |
| Count | **16** |
| CI | Wilson on resolved counts |
| Outputs | PNG + CSV + provenance JSON → `tenure_sandbox/hero/` |

**Stage 9** (`stage9_inverted_u.png`, Apr 2026) used 18 bins on a **broader** population — useful sanity check, **not** the v0 deliverable.

---

## Step 5 — Act II+ (later)

| Act | Action |
|-----|--------|
| **II F-HERO** | Bin department mean pubs at fixed Â slice |
| **III ρ** | Department-level H_sort bracket (compare to MBB reigning hero ρ folder) |
| **IV Sim** | Frozen departments → fit score knobs → sim tenure flags → replay HERO |

**ρ policy:** Do **not** assume ρ ≈ 0 on tenure. Run Act III before parking ASSIGN like MBB.

---

## Code map

| File | Role |
|------|------|
| `tenure/tenure_pipeline/stage9_analysis.py` | Reference implementation (collapse + bin + plot) |
| `tenure/tenure_pipeline/build_faculty_panel_inference_v1.py` | Inference tier filter reference |
| `tenure/scripts/tenure_pass_a_hero.py` | v0 CLI → `tenure_sandbox/hero/` |
| `sports/scripts/pass_a_empirical_bundle.py` | MBB template for provenance + filenames |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | Initial pipeline map; v0 locks from Charles + Alex direction. |
