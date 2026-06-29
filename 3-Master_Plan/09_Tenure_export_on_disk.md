# PEER → COMPASS: faculty_panel_inference_v1 exported

**Canonical name:** `09_Tenure_export_on_disk.md`  
**Original archive:** [`obsolete/original_filenames/20260624_PEER_inference_export_complete.md`](obsolete/original_filenames/20260624_PEER_inference_export_complete.md)

**Date:** 2026-06-24  
**From:** PEER  
**To:** COMPASS, Charles, VECTOR  
**Trigger:** Charles C1–C2 locks

---

## Deliverables

| File | Description |
|------|-------------|
| [`tenure_pipeline/faculty_panel_inference_v1.csv`](../tenure_pipeline/faculty_panel_inference_v1.csv) | Inference sample (HIGH + MEDIUM; poolq required) |
| [`tenure_pipeline/faculty_panel_inference_v1_manifest.json`](../tenure_pipeline/faculty_panel_inference_v1_manifest.json) | Filter rules + N counts |
| [`tenure_pipeline/build_faculty_panel_inference_v1.py`](../tenure_pipeline/build_faculty_panel_inference_v1.py) | Rebuild script |

## Inference sample (manifest)

- **796 persons**, **52 departments**, **2396 person-years** (assistant rows with LOO pool quality)
- **Filter:** `match_confidence ∈ {HIGH, MEDIUM}`; exclude MULTI from primary
- **Full roster:** 168 R1 CS departments in data construction (report both N's in prose per C3)

## VECTOR use

Setting 3 Methods/Results: lead with inference-ready N; label stage 9 figure **preliminary**; Layer B Cox pre-submission.

---

*PEER standing by. Route Layer B with `R1` when pre-submission window opens.*
