# Tenure PDE — Streamlining, Conda vs Git, and Research Priorities (Printable Digest)

**Purpose:** One place to read (and print) how your **projects**, **conda environments**, and **Git** fit together, plus **where the science goes next** after Rivanna connectivity.  
**Last updated:** Session notes consolidated for PDF / paper markup.

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

## Part 3 — After connectivity: research priorities (are we barking up the right tree?)

Once SSH / Git / Rivanna paths are working, the **first scientific priority** is **rough, honest counts** — not perfect models — to see if the agenda is viable.

### Question A — Certainty about role, place, and time

**Goal:** Count how many individuals you have **high certainty** for as:

- **Assistant professor**
- At a **specific school**
- At a **specific time** (year / season / snapshot, per your panel design)

This is the core “do we have enough signal?” question before investing in heavy OpenAlex econometrics.

### Question B — Outcomes: promotion vs “got out”

**Goal:** Among those assistant-professor–identified people, quantify:

- How many **promoted to Associate** (or equivalent), **within your data window and rules**, and  
- How many **left** the assistant rank without promotion in the sense you define (“got out” — move to industry, leave academia, move institutions, etc., depending on definition).

Exact operational definitions (titles, years, censoring) will be tightened in analysis — this digest only captures **intent**.

### Question C — Who gets OpenAlex first

**Goal:** Restrict the **first** OpenAlex author disambiguation pass to faculty you already classify as **high confidence** in your pipeline **and** **assistant professor** (per your parsed HTML / panel rules). **Quantify** that set (N = ?).

Those names are the **first** candidates for OA matching (you already have API-based resolution in the pipeline; bulk OA on HPC comes next for scale).

### Question D — Performance metrics on Rivanna

**Goal:** Use **downloaded OpenAlex data** on the HPC (not the public API for bulk everything) to attach **works** and **citations** (and derived metrics) as **performance** measures for those disambiguated authors.

**Order of operations (high level):**

1. **Panel / parse certainty** → assistant + school + time counts.  
2. **High-confidence assistant subset** → count + list for OA work.  
3. **OA disambiguation** (existing pipeline + HPC bulk as needed).  
4. **Works / citations** → outcome and performance analysis layers.

---

## Part 4 — What to print (PDF checklist)

**Recommended core packet (start here):**

| File | What it is |
|------|------------|
| **`TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md`** | **This file** — conda vs Git, clutter, research priorities. |
| **`GIT_MULTIPLE_MACHINES_ELEMENTARY.md`** | Git remote, push/pull, first repo on GitHub, two machines. |
| **`RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md`** | Remote SSH, workspaces, agents (CODA/PEER/SPORT), `cdh` / `Chas_Working`, OpenAlex not in Git. |

**Optional add-ons (longer / more technical):**

| File | When to print |
|------|----------------|
| **`TENURE_PIPELINE_OVERVIEW.md`** | When you want the full pipeline narrative on paper (long). |
| **`TENURE_DATA_GAMEPLAN.md`** | If it still matches your data strategy; skim for overlap with Part 3 above first. |
| **`Pertinent_Thoughts_Tenure.md`** | If you use it as a running notebook of ideas. |

**Tip:** Print the **three core** files first; add overviews only if you want a **thick** binder.

---

## Part 5 — Clarifications still open (fill in by hand on printout if you like)

- Exact **definition** of “got out” vs “promoted” for your study (titles, years, censoring).
- Whether **talent** and **sports** repos will mirror the same Git pattern as **tenure** (three repos vs one monorepo — your call).

---

## Part 6 — File locations (all under the dissertation workspace)

These guides live in:

`…/Cursor Workspace PDE/current_documents/tenure_documents/`

Same folder as `TENURE_PIPELINE_OVERVIEW.md` and related tenure docs.

---

*Consolidated for printing and margin notes. Update Part 3 when operational definitions are fixed.*
