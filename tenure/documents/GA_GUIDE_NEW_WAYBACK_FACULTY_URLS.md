# Graduate assistant guide — from Wayback URLs to scraped faculty HTML

**Audience:** Research assistants helping with the tenure / faculty-scrape pipeline  
**Last updated:** 2026-10-02  
**Example school:** University of Minnesota (Computer Science and Engineering)

You found **two promising faculty-directory pages** in the [Wayback Machine](https://web.archive.org/). This guide walks you from those URLs through download and parse — without running heavy OpenAlex or panel stages.

**Read first (short):** [`TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`](TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md) (daily wave section) and [`tenure/scripts/README.md`](../scripts/README.md) (command list).

---

## What you are doing (big picture)

1. Turn Wayback discoveries into **canonical live URLs** (the address the site used, not the `web.archive.org/web/…` wrapper).
2. Register them in the project **worksheet**, then **apply** so the pipeline knows Minnesota has new URLs to try.
3. Run **Cells 2 → 3A → 3B → 4** (CDX → download HTML → parse names) for Minnesota only.
4. Read the **post-wave report** and tell Charles whether the new URLs improved parse counts.

Nothing in this guide adds faculty to the dissertation panel by itself — it only **collects and parses archived HTML**.

---

## Before you start

| Requirement | Notes |
|-------------|--------|
| **Repo** | Clone or open the Cursor workspace that contains `tenure/540_tenure_pipeline.ipynb`. |
| **Python env** | Use **`tenure_net`** (Python **3.10+**). System `python3` may be too old for `html_parser.py`. |
| **Network** | CDX and Wayback downloads need internet. |
| **Do not run daily** | Leave Cells **5–9**, bulk OpenAlex, and `rebuild_plan.py --force` (full wipe) **off** unless Charles asks. |

**Minnesota identifiers you will see in files:**

- **University name (worksheet):** `University of Minnesota`
- **Slug (filters / folders):** `university_of_minnesota`
- **Department label:** `Computer Science and Engineering`

---

## Step 1 — Copy the right URL from Wayback

In the Wayback calendar, open a snapshot that looks like a **faculty or people directory** (names, titles, not just a news article).

Copy the **original URL**, not the archive URL.

| Wrong (archive wrapper) | Right (original site URL) |
|-------------------------|---------------------------|
| `https://web.archive.org/web/20190315120000/https://cse.umn.edu/cs/faculty` | `https://cse.umn.edu/cs/faculty` |

Use **`https://`** when the live site uses it. Trailing slashes are OK; the pipeline normalizes them.

**Example (illustrative — replace with your two discoveries):**

1. `https://cse.umn.edu/cs/faculty` (may already be in the worksheet; apply will skip duplicates)
2. `https://www.cs.umn.edu/directory/faculty.html` (older path — good Wayback candidate)

---

## Step 2 — Optional but recommended: probe each URL

From the **repository root** (folder that contains `tenure/` and `functionsG_working.py`):

```bash
conda activate tenure_net
python3 tenure/tenure_pipeline/probe_faculty_url.py --url 'https://YOUR_FIRST_URL_HERE/'
python3 tenure/tenure_pipeline/probe_faculty_url.py --url 'https://YOUR_SECOND_URL_HERE/'
```

**How to read the output:**

- **CDX HTML snaps** — how many archived HTML captures exist (more is usually better).
- **Parse records** — how many faculty rows our parser got from **one** test snapshot.
- **Verdict** — `OK` / `MARGINAL` / `FAIL` — use judgment; Charles may still want a URL with good CDX even if one snapshot parses poorly.

Send Charles a one-line note per URL: verdict + parse count + CDX count.

---

## Step 3 — Enter URLs in the worksheet

Open:

`tenure/tenure_pipeline/url_update_worksheet.csv`

(in Excel, LibreOffice, or VS Code — **keep CSV format**.)

**Important column:** `new_url` — paste each new URL here.

**Rules:**

- One **new** URL per row where you fill `new_url`.
- Match the school using the **`university`** column (`University of Minnesota`). You can use **two different rows** for the same university (one URL each in `new_url`).
- Do **not** delete or overwrite existing URLs in the `url` column; those are the audit trail.
- Leave `new_url` blank on rows you are not updating.

After apply (next step), the script refreshes stats columns; Charles may clear `new_url` after a successful wave.

---

## Step 4 — Apply worksheet → school list

From repo root:

```bash
./tenure/apply_url_updates.sh
```

or:

```bash
python3 tenure/tenure_pipeline/apply_url_updates.py
```

**Expect:**

- `changed` — URLs newly appended to `r1_schools_data.py`
- `already_there` — duplicate of a URL already on the list
- `already_tried` — URL was tried before and failed (Charles may override)

If nothing applies, fix typos in `university` or check you used `new_url`, not `url`.

---

## Step 5 — Configure the notebook for a Minnesota-only wave

Open `tenure/540_tenure_pipeline.ipynb`.

**Run Cell 0** and set flags as follows (all other `RUN_CELL*` should be **`False`** except those listed):

| Flag | Value |
|------|--------|
| `RUN_CELL2` | `True` (refresh school CSV) |
| `RUN_CELL3_CDX` | `True` |
| `RUN_CELL3_DOWNLOAD` | `True` |
| `RUN_CELL4` | `True` |
| `RUN_CELL1`, `RUN_CELL3_RETRY`, `RUN_CELL3C`–`E`, `RUN_CELL5`–`RUN_CELL9` | `False` |
| `WAYBACK_SLUGS` | `["university_of_minnesota"]` |
| `RUN_WAVE_REPORT_AFTER_PARSE` | `True` (default — prints table after Cell 4) |

Then run, in order:

1. **Cell 0** (already run if you edited flags)
2. **Cell 2**
3. **Cell 3A** (CDX — can take several minutes; be patient between schools)
4. **Cell 3B** (downloads HTML)

**If Cell 3B fails to write files on Dropbox** (missing HTML, “read-back verify failed”), from repo root:

```bash
python3 tenure/run_stage3b_cli.py
```

(use the same `WAYBACK_SLUGS` in Cell 0 first, then re-run Cell 0 before the CLI.)

5. **Cell 4** (parse). When parse finishes, you should see the **Wayback URL report** automatically if `RUN_WAVE_REPORT_AFTER_PARSE` is `True`.

**Manual report anytime** (after Cell 0):

```python
run_wayback_url_report()  # uses WAYBACK_SLUGS
```

Or from terminal:

```bash
python3 tenure/tenure_pipeline/wayback_wave_report.py --slugs university_of_minnesota
```

---

## Step 6 — CLI alternative (same code as the notebook)

Charles may prefer this for a single school:

```bash
conda activate tenure_net
python3 tenure/run_wayback_wave.py \
  --slugs university_of_minnesota \
  --steps apply,cell2,cdx,download,parse
```

This runs **apply** (worksheet), rebuilds Cell 2 CSV, then 3A / 3B / 4, then the **report** (unless `--no-post-report`).

---

## Step 7 — What to report back

Send Charles a short email or Slack message with:

1. The **two original URLs** you added (and probe verdicts if you ran probe).
2. Screenshot or paste of the **report table** rows for Minnesota — columns: **Plan** (planned snapshots), **HTML** (files on disk), **AvgRec** (mean parsed faculty per file from parse audit).
3. Any **errors** (403, 0-byte files, parse strategy `none`).
4. Whether old Minnesota URLs should stay or be retired (you do **not** remove URLs yourself unless Charles asks).

**Good outcome:** New URLs show **HTML > 0** and **AvgRec** meaningfully above empty or zero rows (often 10+ is “good”; context matters).

**Bad outcome:** Plan snaps but HTML stays 0 → mention 3B / Dropbox; CDX zero → URL may not be archived as HTML.

---

## Troubleshooting

| Symptom | What to try |
|---------|-------------|
| `No new_url entries` on apply | Fill `new_url` column; save CSV. |
| Minnesota runs every school | Set `WAYBACK_SLUGS = ["university_of_minnesota"]` and re-run Cell 0. |
| Same URL retried forever | Charles may use permanent-skip logic; don’t delete index files yourself. |
| Re-CDX one school from scratch | Charles only: `python3 tenure/tenure_pipeline/rebuild_plan.py --slug university_of_minnesota --dry-run` then `--force`. |
| Python `TypeError` on `\|` types | Wrong Python version — use **3.10+** / `tenure_net`. |

---

## Document history

| Date | Change |
|------|--------|
| 2026-10-02 | Initial GA walkthrough (Minnesota example; worksheet → 540 → report) |
