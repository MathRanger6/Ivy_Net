# Pertinent Thoughts — Tenure Pipeline

Observations worth carrying into **dissertation prose**, **limitations**, or **methods** — not a substitute for **`TENURE_PIPELINE_OVERVIEW.md`** (implementation) or **`TENURE_DATA_GAMEPLAN.md`** (contract).

**Re-verify after each major scrape/parse:** Coverage counts, “red tier” schools, and rescue outcomes change when you re-run Cells 3A–4. Use current **`faculty_snapshots_plan.jsonl`**, **`pipeline_health_audit.csv`**, and **stage 4 viz** as ground truth, not the illustrative numbers below unless you have re-checked them. For **enrollment-colored** Stage 3 figures and **IPEDS** rebuild steps, see overview **§7.5–§7.6** (notebook **`541`** / `build_school_enrollment_from_ipeds.py`). **OpenAlex bulk** at UVA is **not** available yet — see overview **§4** and gameplan advisor direction.

---

## Internet Archive / URL limitations (school-level)

### Auburn — often no usable Wayback replay

CSSE URLs have repeatedly shown **no usable CDX/replay** (timeouts, 403-style behavior), consistent with **robots.txt / exclusion** from replay. Treat as a **coverage limitation**, not a parser bug. **Re-verify** against your latest plan and health audit before claiming Auburn is unique among the roster.

### NC State — redirect shells

Historically, many captures were **tiny `<meta refresh>` shells** pointing at `/directories/faculty.php` while Wayback did not always serve parseable content at the redirect target. **CELL 3E** in the notebook attempts rescue; success depends on Archive availability at re-run time. For prose: distinguish **shell on disk** vs **parseable faculty HTML**. Mechanics: **`TENURE_PIPELINE_OVERVIEW.md`** (Phase E).

### UW–Madison / UIUC — sub-page and era gaps

**CELL 3D** addresses the **JS hub → static sub-page** pattern. Residual **404s** or **missing nav links** in early years are **Archive gaps**, not necessarily code bugs. Panel coverage for these schools may **truncate** earlier or later than the global 2000–2024 window—report **empirical** year ranges from parsed output.

---

## UIUC — homepage vs faculty listing (method note)

Wayback sometimes captured the **department homepage** instead of the **All Faculty** listing for earlier eras, which **depresses** extracted counts before the site reorganisation. **Do not** interpret long-run faculty-count trends at UIUC without checking **page type** (title, link density, URL) for each interval. If the canonical faculty URL in **`r1_schools_data.py`** was updated, **re-CDX** and re-parse before locking conclusions.

---

## Parser — compound titles vs rank (`html_parser.py`)

The rank normaliser can match the **first** recognised rank token, so strings like **“adjunct assistant professor”** may map to **`assistant`** instead of **`adjunct`**. A **modifier-first** pass (adjunct / visiting / research / clinical) before base rank would better support tenure-track filtering later. Scale: order **~few %** of rows in large runs—worth a logged fix, not a silent assumption in the thesis.

---

## “Bad URL” schools (ongoing QA)

Some departments plot **low average faculty per snapshot** in **stage 4 diagnostics** (`plot_stage4_diag` in **`viz_pipeline.py`**) because CDX hit a **homepage or wrong path**, not because the department is tiny. **Examples** that have appeared in QA: **UCLA**, **Duke** — use as illustrations only; the current list is whatever the latest diagnostic shows. Fix path: **`url_update_worksheet.csv`** → **`apply_url_updates.py`** → **`r1_schools_data.py`** → Cell 2 → re-scrape.

---

*Last tightened: **2026-04-12** — cross-links to overview §7.5–§7.6 (IPEDS + viz) and §4 / gameplan (OpenAlex API vs bulk access pending).*
