# FOUNDY handoff — Chapter 3 (Data & empirics)

**Superseded as the front door on 13 November 2026.** NVECTOR should start at `20261113_FOUNDY_to_NVECTOR_Ch3_handoff.md`. This file is still useful for Army background. Its locks on survival ("footnote only") and on file locations under `VECTOR_work/` are out of date.

**Audience:** FOUNDY (thesis drafting for Charles / NVector).  
**Status:** Charles to **approve before** treating as binding for Word work.  
**Prepared:** 2026-11-09 (COMPASS + Charles thread).  
**Companion agent:** CODA = repo/code truth; FOUNDY = prose in Word. This file is the **single front door** for Ch.3 writing.

**Say `anchor` in chat with Charles** → he pastes the live **YOU ARE HERE** from [`3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md`](../../re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md).

---

## 1 · What Chapter 3 is (Alex, PD52 / 2026-11-04 transcript)

Chapter 3 is **not** the model chapter. It has **two movements**, in order:

1. **Systems** — What makes a setting measurable for the dissertation question; then **four systems** (Army, Romanian education, college basketball / NBA draft, tenure): provenance, cleaning, **which column is which concept**. Alex: this layer *is* the science; in a journal it becomes supplementary data.
2. **Results** — Only after (1). **No assignment model** here (that is Chapter 5). **No development / “too much talent” claim** in this chapter.

**First deliverable Charles wants:** ~**2-page executive summary** of the chapter (readable without column names), same pattern as the introduction chapter — draft early, **revise after** the detailed sections exist.

**One-sentence criteria line (Alex):** A system works when individual performance is observable, groups are structured (not a random draw), selection is global with a **finite slot count**, and outsiders do not constantly enter (Army: no lateral refill).

**Transcript:** `Introduction_Agent_Handoff_20261027/transcripts/20261104_Paper_Directions_52_otter_ai_transcript.docx`

---

## 2 · Locked decisions (do not reopen without Charles + Alex)

| Topic | Decision |
|-------|----------|
| **Chapter scope** | Data description + empirical **descriptive** results (band histograms / data stories). **No** LG, no score≠select mechanics beyond a footnote if needed. |
| **Army promotion outcome** | **Any promotion to major** when `dor_maj` is observed (`event = 1`). Below-zone / BZ timing = motivation & possible future work — **not** the coded outcome on current figures. |
| **Army figure pair** | Two **final-incidence** bars per performance band: **promotion** and **attrition** (Cell 11 CIF bars / HERO). Curves → mention only; **not** a survival-methods chapter. |
| **BZ / Cox history** | Alex (2026-11-09): **one footnote (A)** or **omit (D)** — not a sidebar paragraph. Default **A** so readers know why attrition sits beside promotion. |
| **Out of scope for now** | Sex, prestige, MOS splits, **YG-faceted exploratory CR panels** (not the global YG **filter**), Kaplan–Meier demos (`First_good_plots.pdf` = archive). |
| **YG + snapshot window** | **In scope and essential.** Charles restricts **year groups** and the **snapshot / study window** so each cohort is followed through realistic CPT→MAJ promotion possibility; drops tail YGs still mid-window at extract end → **less unresolved (`event = 0`)** in bar denominators. Chapter must say this in Army methods—not a footnote. |
| **Data system name in print** | **PDE (AAG-RFL)** / Talent Net DUAs. **Vantage** = same DUAs, ops path — footnote only until rerun is run of record. |
| **OER / evaluation fields** | Charles confirmed **approved** for methods prose (2026-11-09); no microdata release. |
| **Counts in prose** | Embed **March 2026 AWS export** numbers where known; footnote **Vantage TBD** until bars match. |

**Binding elsewhere in repo:** [`AGENTS.md`](../../../AGENTS.md) — score ≠ select; environment ≠ advancement.

---

## 3 · Read these in order (FOUNDY)

| # | Document | Use |
|---|----------|-----|
| 1 | [`_DISPOSABLE_Ch3_data_empirics_thread.md`](../../re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md) | Live status, Army **prose seed** (§ Army — draft of the data section), placeholder figures, thread log. |
| 2 | **This file** | Decisions + navigation. |
| 3 | [`20261109_CODA_Response_Ch3_raw_to_dataframes.md`](20261109_CODA_Response_Ch3_raw_to_dataframes.md) | Pipeline 501→520, filters, events 0/1/2, IRB table, flow-count placeholder. **Technical backbone** for Army subsection. |
| 4 | [`20261018_CODA_Response_NVector_Army_LOO_Questions.md`](20261018_CODA_Response_NVector_Army_LOO_Questions.md) | LOO vs minus-mean, peer definitions — **do not contradict**; Ch.3 Army run of record uses **minus-mean** on March figures. |
| 5 | [`ARMY_PLOT_PROVENANCE_AUDIT.md`](../../re_entry/ARMY_PLOT_PROVENANCE_AUDIT.md) | Which PNGs are real, filters from filenames, what is **not** in git. |

**Optional prose (Army institutions):** `Introduction_Agent_Handoff_20261027/drafts/07_army_DRAFT.md` — introduction only; Ch.3 goes **deeper on data**, not policy essay.

**Questions file (historical):** [`20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md`](20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md)

---

## 4 · Army — what FOUNDY should write first

Charles already has a **plain-language Army data section draft** in the disposable (starts at “Why it matches”). FOUNDY jobs:

1. **Executive summary** (~2 pp.) — four systems + criteria; no column names required.
2. **Expand Army** using CODA §1–7 — start at **raw snapshots + OER**, not at `tb_ratio_fwd_snr`.
3. **One cleaning paragraph** — pool defined on snapshot day × SNR **inflates** pools vs rating window (median ~23 vs ~12); say it in mapping, not as apology.
4. **Cohort window (YG + snapshots)** — Charles’s design choice: **`filter_ygs`** (when enabled) plus extract coverage so the **youngest included YG** has had time to face major promotion before censoring; tie to `dor_cpt` / board timing in prose. Placeholder figures: **YG 2002–2011** on March export run of record; Vantage may retune list but **logic stays**.
5. **Outcome + figures** — embed placeholders below; paste caption block from disposable § Army placeholder kit.

### Terminology (get this right)

| Concept | Column / name | Common mistake |
|---------|----------------|----------------|
| Own performance | `tb_ratio_fwd_snr` | Do not call it “portable talent.” |
| Group | SNR pool at snapshot (legacy) | Not yet “rating window only” in March run. |
| Peer / group quality (March HERO) | `pool_minus_mean_snr_fwd` | **Not** “LOO mean of others only” in prose — code: own TB minus **pool mean** (`tb_ratio_fwd_snr − pool_tb_ratio_mean_snr_fwd`). Straight LOO pond = future / other runs (`pool_tb_ratio_mean_snr_fwd`). |
| Promotion | `dor_maj` → `event = 1` | Not BZ-only. |
| Attrition | Last snapshot before study end, no major | `event = 2`. |
| Open at end | Still in file at study end | `event = 0`; stays in bar **denominators**. |

### Placeholder figures (until Vantage)

| Figure | Path (repo) |
|--------|-------------|
| **Main** | `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png` |
| **Companion** | `…/ARMY_own_tb_ratio_fwd_cif_b8.png` |
| Optional time shape | `…/ARMY_G1_pool_minus_mean_fwd_CR_curves.png` |

**Caption template** — full text in disposable § **Army placeholder kit**. Short form:

> March 2026 AWS export, Run 1 · `pipeline_config_17_1` (`TALENT_NET_export_20260320-1000`). Last snapshot; promotion = any to major; 8 equal-width bins on z-scored **pool minus mean (forward SNR)**; no OER; YG 2002–2011 in export base config; N = 31,692. Vantage rerun (filters TBD) may replace figure.

**Bar definition (for one sentence in methods):** Promotion bar = promoted in band ÷ all in band; attrition bar analogous; officers still open count as not promoted (see `talent/documents/CR_Red_Line_Flow_Explanation.md`).

---

## 5 · Other three systems (stubs — Charles / CODA to extend)

Same **two-part** pattern as Army when materials arrive:

| System | Performance measure (Alex) | FOUNDY status |
|--------|---------------------------|---------------|
| Romanian education | (existing dissertation thread) | Not started in this handoff |
| College basketball → NBA draft | Points per minute | Not started |
| Tenure | (Charles 11-04: include) | Not started |

Do **not** invent counts or paths; leave `TK` until Charles points at repo notebooks.

---

## 6 · What FOUNDY should **not** do

- Open the **introduction** literature thread (`_DISPOSABLE_FOUNDY_Introduction_thread.md`) except for cross-cites already in Zotero.
- Present **assortativity / LG / ρ** as Chapter 3 content.
- Use **sex / prestige / MOS** Army panels or `First_good_plots.pdf`.
- Claim **Vantage** as a separate IRB data system.
- Define pool quality as LOO-only without checking §4 table above.
- Ship CODA response to NVector as final until Charles approves (footer on CODA file).

---

## 7 · Working style with Charles

- **Word + Zotero** (same as introduction): tracked changes; Charles’s name on insertions when editing live Word.
- **Durable memory:** update disposable **thread log** after substantive turns; FOUNDY can ask Charles to paste `anchor`.
- **PDFs:** Charles runs `./scripts/convert_single_md_to_pdf.sh` locally if he wants a print copy of this handoff or CODA — agent does not auto-convert.

---

## 8 · Open items (TK for Charles / CODA)

| Item | Owner |
|------|--------|
| Flow table counts (502 → Cell 9 → Cell 11) | Charles + Vantage log |
| Footnote draft for BZ / survival history | FOUNDY draft → Alex |
| Pick one Way_Ahead mosaic slide vs flipbook-only | Charles (optional illustration only) |
| Romanian / MBB / tenure data paths for FOUNDY | Charles next |

---

## 9 · Thread log (handoff doc)

| Date | Note |
|------|------|
| 2026-11-09 | Created so FOUNDY has one Ch.3 entry point; consolidates CODA response, disposable, figure kit, Alex decisions. |
