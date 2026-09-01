# Tenure sandbox — HERO + F-HERO (exploratory)

**Purpose:** Tenure-domain hero readouts on Mac, parallel to MBB [`../sports_sandbox/`](../sports_sandbox/).

**Campaign plan (print this):** [`TENURE_HERO_Campaign_Plan.md`](TENURE_HERO_Campaign_Plan.md)  
**Pipeline map (MBB mirror):** [`TENURE_hero_pipeline.md`](TENURE_hero_pipeline.md)  
**Living thread:** [`_DISPOSABLE_tenure_hero_thread.md`](_DISPOSABLE_tenure_hero_thread.md) — say **`anchor`** in chat for YOU ARE HERE.

**Data handoff:** [`../../20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md`](../../20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md)

---

## Layout

```text
tenure_sandbox/
  README.md                    ← this file
  TENURE_HERO_Campaign_Plan.md ← print stack #1
  TENURE_hero_pipeline.md
  _DISPOSABLE_tenure_hero_thread.md
  hero/                        ← Pass A HERO outputs
  fhero/                       ← F-HERO (later)
```

**Input (not in this folder):** `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl`  
**Script:** `tenure/scripts/tenure_pass_a_hero.py`

---

## v0 lock (summary)

| Item | Value |
|------|--------|
| Filter | HIGH/MEDIUM OpenAlex; non-null LOO on assistant rows |
| Grain | Person-level mean `poolq_loo_mean` |
| Bins | 16 quantile |
| Y | Tenure rate among **resolved** (tenure + attrition); censored excluded |
| ρ | Diagnostic in Act III — not parked unless data say so |

---

## Filename tokens (v0)

**Example:** `HERO_tenure_q16_infHM_resolved_v0.png`

| Token | Meaning |
|-------|---------|
| `tenure` | Domain |
| `q16` | 16 quantile LOO bins |
| `infHM` | Inference filter HIGH + MEDIUM |
| `resolved` | Rates use resolved denominator (Option A) |

Each PNG should have matching `*_binned.csv` and `*_provenance.json`.

---

## Run (after script lands)

```bash
# repo root
python tenure/scripts/tenure_pass_a_hero.py
python tenure/scripts/tenure_pass_a_hero.py --n-bins 12   # sensitivity
```

Outputs → `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/`
