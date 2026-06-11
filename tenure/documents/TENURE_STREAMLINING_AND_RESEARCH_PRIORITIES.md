# Tenure PDE — Streamlining, Conda vs Git, and Research Priorities (Printable Digest)

**Purpose:** One place to read (and print) how your **projects**, **conda environments**, and **Git** fit together, plus **where the science goes next** after Rivanna connectivity.  
**Last updated:** 2026-06-08 (PEER tenure lane — see **`3-Master_Plan/PEER_report_to_COMPASS.md`** for COMPASS handoff).

---

## Part 1 — Projects vs conda environments (talent_net, sports_net, tenure_net)

You clarified something important: these are **both** names for **projects** **and** names for **conda environments**.

| Name | Typical meaning |
|------|------------------|
| **talent_net** | Conda env + “talent” pipeline / project work |
| **sports_net** | Conda env + sports / replication project work |
| **tenure_net** | Conda env + tenure / dissertation pipeline work |

**Conda** = which **Python packages** are installed in an isolated environment (`conda activate tenure_net`, etc.).  
**Folders** = where **code and data** live (`tenure_pipeline/`, `tenure_documents/`, notebooks, etc.).

They are related but **not the same thing**:

- **`conda env list`** shows **environments** on that machine.
- **`ls` in Dropbox** shows **folders** — your layout (`tenure_pipeline`, `tenure_documents`, …).

**Git does not replace conda.** Git tracks **source files** in a **repository**. Conda builds **runtimes**. On Rivanna you will usually:

1. **`git clone`** the repo (code).
2. **`conda env create -f environment.yml`** (or equivalent) to recreate **tenure_net**-like dependencies **on the cluster**.

So: **Git streamlines “one true copy of the code” across machines.** It does **not** automatically untangle every folder on your Mac — you still choose a **clear repo layout** (what lives inside the dissertation repo vs separate repos for talent vs sports).

---

## Part 2 — Why things feel “jumbled” and how Git helps (and what it cannot do)

**Feels jumbled because:**

- Multiple **projects** (talent, sports, tenure) each have code, docs, and envs.
- You **reorganized** around `tenure_pipeline/`, `tenure_documents/`, etc. — good direction, but old habits and Dropbox paths linger.
- **Conda env names** (`*_net`) are easy to confuse with **folder** names if they are not documented in one place.

**Git helps by:**

- Giving **one authoritative history** for whatever you put **in the repo** (commits, branches, “what changed when”).
- Letting Mac and Rivanna share **the same code** via **clone / pull / push**.
- Reducing “which copy did I edit?” when you adopt a simple rule: **commit + push** when you finish a chunk.

**Git does not magically:**

- Merge unrelated folders without you **choosing** what belongs in the repo.
- Replace **conda** — you still maintain **environment.yml** (or similar) **inside** or **beside** the repo.
- Organize your **entire** Dropbox — only what you **add** to Git.

**Practical streamlining recommendation:** Pick **one Git repo** for the **tenure dissertation codebase** first. Keep `current_documents/tenure_documents/` and `tenure_pipeline/` **inside** that repo if they belong to the same dissertation (adjust `.gitignore` for huge outputs). Talent and sports can stay **separate repos** later if that matches how you think about them.

---

## Part 3 — Research priorities (updated June 2026)

**Status:** Charles’s April 2026 “rough counts first” agenda (Questions A–D below) has been **substantially executed**. The pipeline now runs **Cells 0–9 complete**, with **Cells 10 / 10.5 wired** (Cox not yet formally reported) and **543** advisor CSV export. See **`PEER_Status_Update_for_VECTOR_2026-06-03.md`** and **`3-Master_Plan/PEER_report_to_COMPASS.md`** for numbers.

### Current panel snapshot (`faculty_panel_with_pools.jsonl`, May 2026 run)

| Metric | Value |
|--------|-------|
| Person–year rows | ~106,600 |
| Unique faculty (`faculty_id`) | ~29,300 |
| Universities (`uni_slug`) in panel | **168** (full `PILOT_SCHOOLS` roster represented) |
| Calendar years | 2000–2024 |
| Persons ever observed as assistant | ~2,330 |
| Person-level outcomes (ever-assistant) | tenure ~422; attrition ~570; censored ~1,340 |
| OpenAlex `match_confidence` (row-level) | HIGH ~17%; MEDIUM ~10%; MULTI ~13%; LOW ~2%; NONE ~58% |

**Interpretation:** Roster **breadth** (168 schools) is better than early “~60 usable departments” language implied — but **depth** (parse quality, OA linkage, resolved tenure outcomes) varies sharply by school. Treat “usable for inference” as a **filter**, not the raw school count.

### Question A — Certainty about role, place, and time — **partially answered**

We can count assistant-professor observations with school + year. **`rank=assistant`** person–years (~6,600) and **`ever_assistant`** persons (~2,330) are documented in the panel. **`n_snapshots`** and strategy audit support per-school QA. Remaining work: tighten tenure-track filtering (compound titles, adjunct misclassification — see **`Pertinent_Thoughts_Tenure.md`**).

### Question B — Outcomes: promotion vs “got out” — **implemented**

`tenure_event`, `attrition`, `censored`, `year_of_tenure` are in the panel (`panel_builder.py`, `gap_tolerance=2`). Competing-risk framing aligns with Army (CODA) and manuscript **`advancement_under_constrained_distinction_dakota_feedback_v03.rtf`**. Lateral moves vs true exit remain **unobserved** (limitation).

### Question C — Who gets OpenAlex first — **superseded by full 6A–6B pass**

The pipeline ran OpenAlex resolution on the full panel, not only a high-confidence assistant subset. **`match_confidence`** tiers (HIGH / MEDIUM / MULTI / LOW / NONE) document quality. Publication analyses should filter to HIGH (+ optionally MEDIUM); see **`PANEL_CSV_GLOSSARY.md`**.

### Question D — Performance metrics on Rivanna — **implemented**

CDH bulk snapshot + **`openalex_snapshot_cache.jsonl`** + **`build_openalex_cache.py`** / Slurm job documented in **`TENURE_PIPELINE_OVERVIEW.md` §4**. Mac workflow: rsync cache, run Stages 7–9 offline.

### Question E — Inverted-U (added June 2026) — **preliminary yes**

**Stage 9:** 18 bins of `poolq_loo_mean` → tenure rate plot shows **non-monotone** pattern with **drop at top bin** (`stage9_inverted_u.png`, `stage9_binned_table.csv`). **Not** final Cox evidence — run Cells 10 / 10.5 → 12 next.

**Order of operations going forward:**

1. **Formal Cox / competing risks** on assistant spell (Cells 10–12).  
2. **Robustness:** peer-group definitions, OA confidence filters, prestige controls.  
3. **Coverage polish** (URL worksheet, bad schools) — secondary to analysis lock-in per advisor Apr 2026 direction.

---

## Part 4 — What to print (PDF checklist)

**Recommended core packet (start here):**

| File | What it is |
|------|------------|
| **`TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md`** | **This file** — conda vs Git, clutter, research priorities. |
| **[`GIT_MULTIPLE_MACHINES_ELEMENTARY.md`](../docs/GIT_MULTIPLE_MACHINES_ELEMENTARY.md)** | Git remote, push/pull, first repo on GitHub, two machines. |
| **[`GIT_FOR_DUMMIES.md`](../docs/GIT_FOR_DUMMIES.md)** *(optional)* | Stash, rebase, fix staging — cheat sheet after you know the basics. |
| **`RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md`** | Remote SSH, workspaces, agents (CODA/PEER/SPORT), `cdh` / `Chas_Working`, OpenAlex not in Git. |

**Optional add-ons (longer / more technical):**

| File | When to print |
|------|----------------|
| **`TENURE_PIPELINE_OVERVIEW.md`** | When you want the full pipeline narrative on paper (long). |
| **`TENURE_DATA_GAMEPLAN.md`** | If it still matches your data strategy; skim for overlap with Part 3 above first. |
| **`Pertinent_Thoughts_Tenure.md`** | If you use it as a running notebook of ideas. |

**Tip:** Print the **core** files first (**this file**, **elementary Git**, **Rivanna/Cursor SSH**); add **[`GIT_FOR_DUMMIES`](../docs/GIT_FOR_DUMMIES.md)** if you want the cheat sheet on paper; add overviews only if you want a **thick** binder.

---

## Part 5 — Clarifications still open (fill in by hand on printout if you like)

- Exact **definition** of “got out” vs “promoted” for your study (titles, years, censoring).
- Whether **talent** and **sports** repos will mirror the same Git pattern as **tenure** (three repos vs one monorepo — your call).

---

## Part 6 — File locations

**Central (cross-domain) docs:** `docs/` — start at **[`docs/README.md`](../docs/README.md)**.

**This tenure stream:** `tenure/documents/` (this file, Rivanna/Cursor SSH guide, pipeline overviews, etc.).

**Other domains:** `sports/documents/`, `talent/documents/`.

---

*Consolidated for printing and margin notes. Update Part 3 when operational definitions are fixed.*
