# Tenure data gameplan (mutually agreed plan)

**What this file is:** The **forward-looking contract** for what we **will** accomplish in the **PEER** empirical setting (CS faculty tenure at R1 institutions) and **how** it connects to the inverted‑U thesis (Army CODA, basketball SCOUT, academia). It is **strategic**: outcomes, stages, durable artifacts, and advisor alignment. **Algorithmic detail**—how each notebook cell reads and writes specific `.csv` / `.jsonl` / `.py` files—is in **`TENURE_PIPELINE_OVERVIEW.md`** (the “pipeline map”). **`540_tenure_pipeline.ipynb`** is the **conductor** at the workspace root; heavy logic lives in **`tenure_pipeline/`** modules where possible.

**Lineage:** Narrative builds on **`Pertinent_Thoughts_Tenure.md`**, prior PEER design notes, and the live pipeline described in **`TENURE_PIPELINE_OVERVIEW.md`**. The sports parallel is **`../sports_documents/SPORTS_DATA_GAMEPLAN.md`**: same split—**gameplan = intent and stage contract**, **overview + notebook = implementation wiring**.

---

## Working agreement (process)

1. **Gameplan vs overview:** **`TENURE_DATA_GAMEPLAN.md`** (this file) stays **stable and readable**—goals, stage boundaries, durable files, open questions. **`TENURE_PIPELINE_OVERVIEW.md`** carries **cell-level** behavior, flags, checkpoints, and file schemas as the implementation reference. For **stable handles** to each `##` section here (**§G1–§G14** + front matter), see **`TENURE_PIPELINE_OVERVIEW.md` §0**.
2. **Document first for big design changes:** If a stage’s *meaning* changes (e.g. tenure vs attrition definition), update **this gameplan** (or an advisor memo), then align code/notebook.
3. **Snapshots:** The repo and `tenure_pipeline/` hold truth; obsolete or one-off experiments should live under clearly named archive folders, not mixed into canonical outputs.
4. **Panel time semantics & collisions (implementation detail):** Use **exact Wayback timestamps** (derive e.g. `snpsht_dt`) as the **analysis clock** for ordering and `merge_asof`; treat **`year` / `season`** as **CDX culling strata**, not substitutes for observation time. For **duplicate or ambiguous names**, allow **multiplicity**, **blending**, and **conflict flags** for later QA—`faculty_linker` is a **baseline** path, not the only defensible representation. See **`TENURE_PIPELINE_OVERVIEW.md` §5** (subsections *Temporal keys* and *Collisions*).
5. **Fix plumbing early:** Structural mistakes in scrape/plan/panel **do not get clearer with age**. Prefer correcting **identity, retention, and join logic** close to when we touch that stage—then re-run—rather than “someday” after results exist.

---

## Snapshot identity, retention, and season labels

**Primary key for a Wayback observation** is the **Archive capture timestamp** (and the corresponding `wayback_url` / derived `snpsht_dt`). **`year` + `season` (spring/fall)** are **useful derived labels**—e.g. for heatmaps, stratification, and CDX query bands—but they are **not** a substitute for a continuous timeline.

**Retention:** Through ingest and parse, **do not discard** captures merely because another capture exists in the same nominal season. Prefer **many dated observations**; **algorithmic consolidation** (median week, dedupe rules, event logic) is a **downstream** step with logged assumptions—not an early filter.

**CDX / plan (Cells 3A–3B):** The pipeline requests **up to `CDX_SNAPS_PER_SEASON` distinct captures per (calendar year, season band)** (default **12** in CELL 0; see overview). When more CDX rows exist than that cap, the closest **`CDX_SPACING_POOL_MULT` × cap** to the season anchor are pooled, sorted in time, then **evenly subsampled** so captures are spread across the year. Each selected capture has a **unique on-disk name** including the Wayback **`timestamp`**. **More snapshots is better** until a later phase explicitly summarizes; overnight runs are acceptable.

**What counts as “tried” for CDX:** CELL 3A builds **`tried_urls` only from `faculty_snapshots_plan.jsonl`** (plus `tried_primary_url` / `tried_urls` fields on prior rows). Deleting or archiving that file (and, for a full Wayback reset, **`cdx_retry_queue.jsonl`**, **`faculty_snapshots_index.jsonl`**, **`faculty_snapshots/`**, and downstream parse/panel JSONL) makes URLs **untried** again for the next run. Removing HTML alone does not reset the plan.

**3A → 3A-RETRY spacing:** The notebook includes an optional **bridge cell** after 3A-VIZ: displays a short **hourglass** message and sleeps **`CDX_SLEEP_BEFORE_RETRY_SEC`** (default 30 minutes) before you run **CELL 3A-RETRY**, so the Archive gets a breather between pass 1 and the slow retry pass.

**Option B on disk (naming):** `faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html` (legacy two-part `year_season.html` filenames may still appear until rebuilt).

---

## Target architecture: **540** as pipeline conductor

**Intent:** **`540_tenure_pipeline.ipynb`** is the **single entry point** you run for the scrape → parse → (future) match → panel chain. Cells are gated by **`RUN_CELL*`** flags in Cell 0 (see overview).

| Role | Responsibility |
|------|----------------|
| **`tenure_pipeline/*.py`** | Parsers (`html_parser.py`), URL helpers (`apply_url_updates.py`), utilities; importable, testable units. |
| **`540` notebook** | Orchestration: load constants, run stages in order, checkpoint/resume, thin cells that call into `.py` where factored. |
| **Human loops** | URL research → `url_update_worksheet.csv` → `apply_url_updates.py` → `r1_schools_data.py`; optional QA CSVs for match overrides when entity resolution lands. |

**Why this fits:** Matches **document-first** staging, **append-only** plan/index JSONL, and your preference for **one conductor** instead of scattered one-off notebooks.

---

## Outcomes we want

- **Empirical:** A defensible longitudinal panel of CS faculty at R1 departments with **rank / presence** from Wayback snapshots and **publication-based performance** from bibliographic data (OpenAlex and/or DBLP—see stages below).
- **Thesis-facing:** Measures that support an **inverted‑U** test: tenure or promotion success vs **leave–self‑out peer pool quality** (and related peer-group definitions), analogous to Army and basketball designs.
- **Operational:** Reproducible **HTML archive** per planned snapshot, **parsed** roster records, then **matched** people to author IDs, then **panel** rows with explicit **sample-loss accounting** at each filter (advisor: “track how many people you throw away at every point”).
- **Coverage:** **Full R1 CS roster in the plan** is a **publication-time** goal; **near-term** priority (advisor, Apr 2026) is **quality and end-to-end statistics on the current corpus**, not maximizing scrape breadth every week.

---

## Durable team / URL equity (files on disk)

**Intent:** Treat these as **durable inputs**, not disposable cache—extend when QA shows gaps.

| File (location) | Role |
|-----------------|------|
| **`tenure_pipeline/r1_schools_data.py`** | **Source of truth** for `PILOT_SCHOOLS` and per-school `urls[]`. |
| **`tenure_pipeline/r1_cs_departments.csv`** | CSV emitted by Cell 2 from the Python list—downstream convenience. |
| **`tenure_pipeline/url_update_worksheet.csv`** | Human-edited queue for new/changed URLs; drives `apply_url_updates.py`. |
| **`tenure_pipeline/faculty_snapshots_plan.jsonl`** | Append-only CDX plan + sentinels (`n_snaps`, bookmarks, reasons)—see overview for semantics; **sole driver of “tried” URLs** for 3A skip logic. |
| **`tenure_pipeline/cdx_retry_queue.jsonl`** | URLs that timed out in 3A pass 1; consumed by **CELL 3A-RETRY** (clear when doing a full clean slate). |
| **`tenure_pipeline/faculty_snapshots_index.jsonl`** | Per-download audit (HTTP status, bytes, paths). |
| **`tenure_pipeline/faculty_snapshots_parsed.jsonl`** | Parsed faculty rows (Cell 4). |
| **`tenure_pipeline/faculty_panel.jsonl`** | Longitudinal within-school panel + Wayback timestamps (Cell 5); see overview §5. |
| **`tenure_pipeline/faculty_panel_collisions.jsonl`** | Name-key collision QA (Cell 5). |
| **`tenure_pipeline/dblp_parsed/*.jsonl`** | Per-year DBLP extracts (Cell 1). |
| **`tenure_pipeline/school_enrollment_annual.csv`** | IPEDS fall headcount by school × year (for viz; rebuild `541` / `build_school_enrollment_from_ipeds.py`). |
| **`tenure_pipeline/openalex_*.json` / `*.jsonl`** | Cells 6A–6B outputs when run (institution map, author IDs, works-by-year, low-confidence queue). |
| **`tenure_pipeline/faculty_panel_enriched.jsonl`** | Cell 7: pubs + tenure/attrition/censoring flags. |
| **`tenure_pipeline/faculty_panel_with_pools.jsonl`** | Cell 8: LOO peer pool metrics (`poolq_loo_mean`, etc.). |
| **`tenure_pipeline/stage9_inverted_u.png`** / **`stage9_binned_table.csv`** | Cell 9: preliminary inverted-U artifacts. |
| **`tenure_pipeline/faculty_panel_advisor.csv`** / **`R1_tenure_data.csv`** | Cell 543: flat CSV for advisors / committee (`PANEL_CSV_GLOSSARY.md`). |

**Option B on disk:** `faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html` (multi-capture) or legacy `<year>_<season>.html`; `source_id = faculty_source_id(url)`—see overview.

---

## Stage map (high level)

| Stage | Notebook region | Intent | Key outputs | Detail |
|-------|-------------------|--------|-------------|--------|
| **0** | Cell 0 | Flags, paths, imports | — | Overview §2 |
| **1** | Cell 1 | DBLP XML → yearly JSONL | `tenure_pipeline/dblp_parsed/` | Overview §3 |
| **2** | Cell 2 | Schools list → CSV | `r1_cs_departments.csv` | Overview §3 |
| **3A–3E** | Cells 3A–3E (+ optional bridge before 3A-RETRY) | CDX plan, Wayback download, optional rescues | `faculty_snapshots_plan.jsonl`, HTML tree, `cdx_retry_queue.jsonl`, indexes | Overview §3–4 |
| **4** | Cell 4 | Parse HTML → names/ranks | `faculty_snapshots_parsed.jsonl` | Overview §4 |
| **5** | Cell 5 | Within-school longitudinal panel + Wayback plan join (`snpsht_dt`, etc.) | `faculty_panel.jsonl`, `faculty_panel_collisions.jsonl` | Overview §4 |
| **6A–6B** | Cells 6A–6B | OpenAlex institution + author resolution + works-by-year (API) | `openalex_*.json` / `*.jsonl` | Overview §4 |
| **7** | Cell 7 | Enriched panel (pubs + tenure/attrition events) | `faculty_panel_enriched.jsonl` | Overview §2 |
| **8** | Cell 8 | LOO peer pool metrics | `faculty_panel_with_pools.jsonl` | Overview §2 |
| **9** | Cell 9 | Binned inverted-U check | `stage9_inverted_u.png`, `stage9_binned_table.csv` | Overview §2; §G12 |
| **10+** | Cells 10, 10.5, 12 (+ 543 ✅) | Layer B Cox survival (**planned**) + advisor CSV package (**done**) | `faculty_panel_advisor.csv`; Cox artifacts TBD | Overview §4 |

Full **sentinel rules**, **CDX timeouts**, **3B ghost retries**, and **parser strategies** are **not** duplicated here—see **`TENURE_PIPELINE_OVERVIEW.md`**.

---

## Advisor direction — 2026-04-09 conversation (Alex Gates)

*Source: `2-Way_Ahead/20260410_Paper_directions_4_otter_ai.pdf` (Otter transcript). Summarized for implementation alignment.*

1. **Priority shift (next ~week):** The scrape/plan machinery is in good shape. **Do not** treat “add more schools / URLs” as the main task **right now**. Shift time toward **quality and measurement on existing data**: how many **assistant → associate** transitions you can see, how much **attrition** (assistant disappears without associate), and rough **peer-group** definitions you can actually populate.
2. **You do not need the full 187-school scrape today**—you need enough structure to estimate effects and see whether the **inverted‑U** is plausible; **defend the sample** at publication time.
3. **Core ingredients to plan explicitly:** (a) **success metric**—tenure / promotion to associate; (b) **peer group(s)**—nested definitions (immediate peers vs broader assistant cohorts—flexible, characterize alternatives); (c) **performance metric**—publications/citations via **OpenAlex** (and ORCID for disambiguation); expect to **try several** specifications.
4. **Faculty-per-snapshot distribution:** Treat as **department pool size**; very large counts may include non–tenure-track listings—**filter later**, but start measuring.
5. **Name matching (v0):** Basic **within-school / within-department** consistency before exotic global merges.
6. **OpenAlex at scale:** Prefer **bulk** OpenAlex (UVA **Connected Data Hub** / HPC: **`.csv.gz`** table shards) over hand-fixing author IDs for subsets; **do not** manually merge three OpenAlex IDs unless the same rule could apply **everywhere** (otherwise bias). **Status (June 2026):** **`build_openalex_cache.py`** + **`openalex_snapshot_cache.jsonl`** implement bulk works-by-year on Rivanna when CDH mount is available; Mac uses **rsync’d cache** (see **`HPC_SETUP_CHECKLIST.md`**, overview **§4**). Cell **6A** author resolution may still use API when not on HPC.
7. **Sanity check literature:** Use **Dakota**-style tenure/productivity work (and any shared **tenure rates**) only to compare **orders of magnitude**—not as the main theoretical anchor.
8. **Field:** **CS** aligns with DBLP; if linkage rates collapse, **other hard sciences** are acceptable—decide on evidence.
9. **Working style:** Drive toward a **first end-to-end curve** (even with messy data); **log sample loss** at each filter; **re-run the pipeline** after a day of cleaning rather than cleaning for a week without integrated results. (Rough time split discussed: **most** time on getting the model through; **small** slice on new URLs / edge HTML.)

---

## Stage 1 — DBLP parse (Cell 1)

**We will** keep per-year JSONL under `tenure_pipeline/dblp_parsed/` as the canonical bibliographic spine for author names/years to match against later stages. Analysis window for publications may be a subset of years on disk.

---

## Stage 2 — R1 school list (Cell 2)

**We will** maintain **`r1_schools_data.py`** as the authoritative list of departments and `urls[]`, rebuild **`r1_cs_departments.csv`** from Cell 2 after edits, and use **`apply_url_updates.py`** + the worksheet for controlled URL changes.

---

## Stage 3 — Wayback scrape (Cells 3A–3E)

**We will** discover snapshots via CDX (3A), download HTML (3B), and use **optional** rescue cells (3C–3E) where archived pages are shells—documented in the overview. **Goal:** durable HTML + plan/index lines suitable for Cell 4.

---

## Stage 4 — HTML parse (Cell 4)

**We will** parse all `*.html` under each school directory (Option B + `legacy/`) into **`faculty_snapshots_parsed.jsonl`**, with strategy audit. **Capture broad titles**; narrow to tenure-track populations at analysis time.

---

## Stages 6–9 — Match, enriched panel, pools, analysis (implemented May–June 2026)

**Delivered** (see **`PEER_Status_Update_for_VECTOR_2026-06-03.md`** and overview §2):

| Piece | Intent |
|--------|--------|
| **Entity resolution** | Faculty names ↔ **OpenAlex** (Cells 6A–6B in `540`; `openalex_resolver.py`) with **scalable** rules; DBLP JSONL for cross-checks; optional QA CSV for overrides. **Bulk** OpenAlex at UVA when access exists. |
| **Panel** | `(person × year)` (or equivalent) with rank transitions, attrition flags, and publication metrics. |
| **Peer quality** | Leave–self–out (or pre-specified) pool metrics on agreed performance measure. |
| **Inference / EDA (Layer A)** | Binned tenure rates vs pool quality — **stage 9 complete** (non-monotone pattern, 18 bins). |

Cell numbers and artifacts are documented in **`TENURE_PIPELINE_OVERVIEW.md`** §2–§4.

---

## Layer B — Cox survival (Cells 10 / 10.5 / 12) — 📋 Planned

**Intent:** Time-to-tenure Cox with pool-quality linear + quadratic terms — adapt Army **`520`** workflow to tenure covariates (`poolq_loo_mean`, `pubs_year`, etc.).

**Status (corrected 2026-06-11):** **`540_tenure_pipeline.ipynb` ends at Cell 9.** Layer B is **not wired** yet. **543** advisor CSV export is complete separately.

| Piece | Status |
|--------|--------|
| **Cox / survival (Layer B)** | 📋 **Planned** — build Cells 10 / 10.5 / 12 in `540`; template: `talent/520_pipeline_cox_working.ipynb` |
| **Formal HR output** | Not yet — blocked on Layer B build |

---

## Fast path — first inverted-U checkpoint (dirty OK)

**Purpose:** See whether **tenure (or promotion) rate** vs **peer pool quality** shows a **nonlinear** pattern early, before perfecting every linkage.

**Rule:** Do not delete canonical under **`tenure_pipeline/`** while experimenting; write scratch outputs with dated suffixes if needed.

**Checklist (adapted from sports gameplan logic) — ✅ ALL COMPLETE as of May 2026**

- [x] **Inputs:** `faculty_panel_with_pools.jsonl` (72 MB) — panel with rank, year, `pubs_year`, `pubs_cumulative`, outcome flags.
- [x] **Define v0 outcomes:** `tenure_event` / `attrition` / `censored` flags; `gap_tolerance=2` years; implemented in `panel_builder.py`.
- [x] **Define v0 peer pool:** `poolq_loo_mean` — LOO mean pubs among OpenAlex-matched assistants in same dept-year; implemented in `pool_metrics.py`.
- [x] **Bins:** 18 equal-width bins of `poolq_loo_mean`; tenure rates with Wilson 95% CI per bin.
- [x] **Save artifacts:** `stage9_inverted_u.png` + `stage9_binned_table.csv` (18 bins × 17 columns).
- [x] **Optional — LPM:** Not yet estimated (Layer B Cox is the **planned** main spec — not yet in `540`).

**Result:** Non-monotone pattern consistent with inverted-U. Peak tenure rates at bins 16–17 (LOO median ~8–9 pubs/yr), with a drop at the very top bin 18 (LOO median ~12.7 pubs/yr). See `PEER_Status_Update_for_VECTOR_2026-06-03.md` for full binned results and caveats.

---

## Open points — Updated June 2026

**Resolved since April 2026:**
- ✅ Panel grain and tenure-clock window: `(faculty_id × year)`, `gap_tolerance=2` years; implemented in `panel_builder.py`.
- ✅ Peer-group v0: LOO mean pubs among OA-matched assistants in same dept-year; `pool_metrics.py`.
- ✅ OpenAlex as primary pub source (DBLP retained as cross-check spine only).
- ✅ First inverted-U check (stage 9 / Layer A): signal present; binned artifacts saved.
- ✅ Advisor-facing CSV + glossary produced (`faculty_panel_advisor.csv`, `PANEL_CSV_GLOSSARY.md`).
- ✅ External briefing prepared: `advancement_under_constrained_distinction_dakota_feedback_v03.rtf` (June 2026, Dakota / academic-careers committee member).

**Still open:**
- Exact **peer-group robustness** set — alternative definitions (broader cohort, field-weighted, citation-based).
- **LPM / logit** sign check (`tenure_event ~ poolq_loo + poolq_loo² + covariates`).
- **Layer B — Cox survival**: build Cells 10 / 10.5 / 12 in `540` (adapt `520` pattern); report HR estimates and inverted-U test on quadratic pool-quality term.
- **Attrition vs lateral move**: snapshots cannot distinguish “left academia” from “moved institution” — competing-risk framing hedges this; note as limitation.
- **Coverage expansion**: current ~60 usable schools; 168 in `PILOT_SCHOOLS`; publication-time goal is defensible breadth. Prioritize analysis lock-in over URL chasing for now.
- **OA bulk access upgrade**: UVA CDH bulk snapshot for author resolution (would improve HIGH confidence rate beyond current ~32%).
- **Heterogeneity**: subfield (ML vs systems vs theory), cohort-year, and dept prestige tier effects.
- **Prestige covariate**: merge NRC rankings or USNews CS tier into panel for controls.

---

## Document history

- **2026-06-11:** **Layer B correction** — Cox (Cells 10 / 10.5 / 12) reframed as **planned** (`540` ends at Cell 9); split § "Stages 6–9" from Layer B; removed "Cox wired" from resolved open points.
- **2026-06-08:** Stage map rows **7–10+** updated (Cells 7–9 complete). §G11 heading reframed from “planned” to implemented for Cells 6–9. Open points + fast-path checklist marked complete.
- **2026-06-08:** **`PEER_report_to_COMPASS.md`** created in `3-Master_Plan/`. **`TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md`** Part 3 rewritten with current panel stats + stage 9 status. **`Pertinent_Thoughts_Tenure.md`** § Stage 9 inverted-U added. Durable files table extended (enriched panel, pools, stage 9, advisor CSV). **`PEER_Status_Update_for_VECTOR_2026-06-03.md`** coverage corrected (168 schools vs quality filter). fast-path checklist marked complete; resolved items noted; still-open items updated. Stage 9 inverted-U result documented. Cox model (Cells 10/10.5), 543 package notebook, `faculty_panel_advisor.csv`, `PANEL_CSV_GLOSSARY.md`, `PEER_Status_Update_for_VECTOR_2026-06-03.md`, and Dakota briefing (`advancement_under_constrained_distinction_dakota_feedback_v03.rtf`) added to resolved items.
- **2026-04-03 — 2026-04-08:** Earlier iterations of **`TENURE_DATA_GAMEPLAN.md`** (roster size, sentinels, URL workflow, Cell 3A-RETRY)—superseded in structure by this file; technical detail preserved in **`TENURE_PIPELINE_OVERVIEW.md`**.
- **2026-04-10:** **Restructured to mirror `SPORTS_DATA_GAMEPLAN.md`**: split **gameplan** vs **overview**; added **Advisor direction (2026-04-09)** from Otter transcript; condensed duplicate cell-by-cell specs in favor of cross-links to **`TENURE_PIPELINE_OVERVIEW.md`**.
- **2026-04-10 (later):** Working agreement item 1 points to **`TENURE_PIPELINE_OVERVIEW.md` §0** for **§G1–§G14** stable anchors to each `##` heading here.
- **2026-04 (later):** Working agreement item **4** summarizes **§5** in the overview (*Temporal keys*, *Collisions*) so the gameplan stays the strategic hook without duplicating that text.
- **2026-04 (later):** Stage map row **5** = Cell 5 panel outputs; durable-files table adds **`faculty_panel.jsonl`** / **`faculty_panel_collisions.jsonl`**.
- **2026-04-10:** **Snapshot identity & retention** + **fix plumbing early** (working agreement **5**); Option B filename pattern allows **timestamp** suffix; CDX multi-capture per season band—see overview **§3** / **§5**.
- **2026-04-11:** CDX cap **12** per band + **temporal spacing** when many candidates; **`tried_urls`** / clean-slate semantics; **`cdx_retry_queue.jsonl`** in durable files; **3A→3A-RETRY bridge** (`CDX_SLEEP_BEFORE_RETRY_SEC`, hourglass cell)—see overview **§2–§3**.
- **2026-04-11 (later):** **`Pertinent_Thoughts_Tenure.md`** shortened: dissertation-facing notes only; stale operational counts and duplicate pipeline detail removed; **NC State** status in overview de-“pending” in favour of re-run guidance.
- **2026-04-12:** OpenAlex **bulk snapshot at UVA** — access **pending**; Stage **6A–6B** documented as **API** path; durable-files table adds **`school_enrollment_annual.csv`** + **`openalex_*`**; advisor bullet 6 links to overview **§4** + Otter transcript; stage map rows **6A–6B** / **7+**; **Stages 6–9** table names OpenAlex + bulk.
