# Wayback Stage 3B — operations & troubleshooting

**Audience:** Charles (and GAs) when Cell 3B behaves oddly or every URL run feels slow.  
**Last synced:** 2026-10-16  

**Related:** daily workflow [`TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`](TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md) · architecture [`TENURE_ARCHITECTURE_AUDIT_20261002.md`](TENURE_ARCHITECTURE_AUDIT_20261002.md) · code **`tenure/tenure_pipeline/stage3b_download.py`**

---

## Two knobs that prevent “why is MSU running again?”

| Knob | Where | What it does |
|------|--------|----------------|
| **`WAYBACK_SLUGS`** | Cell 0 | Limits **3A, 3B, 4** to listed `uni_slug` values. **`None` = entire plan backlog** (~hundreds of missing files across all schools). |
| **Permanent skip** | `stage3b_download.py` | If the **last** index row for a path is a **permanent** failure and the file is still missing, **do not** re-hit Wayback. |

**After `apply_url_updates.py`:** the script prints a suggested `WAYBACK_SLUGS = [...]`. Paste into Cell 0, **re-run Cell 0**, then 2 → 3A → 3B → 4.

**CLI equivalent:**  
`python3 tenure/run_wayback_wave.py --slugs university_of_minnesota --steps apply,cell2,cdx,download,parse`

---

## How 3B builds the download queue

1. Read **`faculty_snapshots_plan.jsonl`** (all planned snapshots).
2. **Skip** if HTML already on disk (≥ 500 B) under any root from `faculty_snapshot_search_roots()` in Cell 0.
3. **Skip** (permanent) if index last row says archive-dead and file still missing — see markers below.
4. **Skip** (slug filter) if `WAYBACK_SLUGS` is set and this row’s `uni_slug` is not in the list.
5. Everything else → **To download** (sorted by school name in the log — Michigan State before Arizona State alphabetically).

So adding one URL **does not** automatically limit 3B to that school unless **`WAYBACK_SLUGS`** (or the wave CLI `--slugs`) is set.

---

## Error messages (what they mean)

### `read-back verify failed (expected … B; read -1 B; stat -1 B)`

| Piece | Meaning |
|-------|---------|
| **expected … B** | Wayback download succeeded in memory. |
| **read / stat -1** | After write, Python cannot read or `stat` the file (treated as **missing**). |
| **Typical cause** | **Dropbox / CloudStorage** path, or **Jupyter kernel sandbox** — write does not persist where 3B expects. |
| **Not** | Bad faculty URL or empty Wayback capture (those are `too small` or HTTP codes). |
| **Retry policy** | **Retried every run** until a file lands (not permanent-skip). |
| **Fix** | Run **`./tenure/run_stage3b.sh`** from Terminal. As of 2026-10-16, 3B **stops before downloading** if a test save into the faculty folder fails, so a notebook run cannot add more schools to this pile. |

### `too small (0B)` (or &lt; 500 B)

Wayback returned an empty or useless body for that capture timestamp. Often **permanent** for that URL+timestamp.

**Fix:** Different URL in worksheet, or re-CDX (3A) to pick another timestamp — not “run 3B again forever.”

### `HTTP 403` / `404` / `410`

Archive or server blocked that replay. Treated as **permanent skip** when last index row matches.

### Ghost warning: “index row(s) claim success but HTML is missing…”

Index says **200 OK** and size OK, but **no usable file on disk** (Dropbox placeholder, moved tree, etc.). Those paths stay in the retry set until a real file exists or you clean index/plan (advanced — ask before deleting JSONL).

---

## Permanent skip vs retry (index semantics)

**Permanent** (skip re-download if file still missing) — substring in last index `error`:

- `too small`
- `HTTP 403`, `HTTP 404`, `HTTP 410`

**Retry** (every run until disk OK):

- `read-back verify failed`
- `write failed`
- transient network errors

3B header lines to watch:

- **`Permanent skip`** — count of plan rows skipped this way.
- **`Slug filter skip`** — rows outside `WAYBACK_SLUGS`.
- **`To download`** — what will actually hit Wayback this run.

---

## Where the code lives (Oct 2026)

| Piece | Location |
|-------|----------|
| Download logic | `tenure/tenure_pipeline/stage3b_download.py` |
| Notebook Cell 3B | Thin wrapper: `from stage3b_download import run_stage3b_from_globals` |
| Terminal 3B | `tenure/run_stage3b_cli.py` — exec Cell 0 + module (not inline notebook body) |
| Slug hint after apply | `apply_url_updates.py` prints suggested `WAYBACK_SLUGS` |

**Do not edit** `tenure/alex_tenure_handoff/` — see `STALE_DO_NOT_EDIT.md`.

---

## Fix changelog (ops)

| Date | Issue | Fix | Doc / code |
|------|--------|-----|------------|
| 2026-10-02 | ASU ~440 KB downloads OK but file vanishes on Dropbox | `$TMPDIR` staging + `cp` in `stage3b_download.py`; CLI runner | `stage3b_download.py`, `run_stage3b_cli.py` |
| 2026-10-02 | MSU/BU/Hawaii retried forever (0 B, 403) | Permanent skip from last index row | `PERMANENT_DOWNLOAD_ERROR_MARKERS` in `stage3b_download.py` |
| 2026-10-02 | Phase 2 tooling | probe, wave report, `rebuild_plan --slug`, discover → shared CDX | [`TENURE_ARCHITECTURE_AUDIT_20261002.md`](TENURE_ARCHITECTURE_AUDIT_20261002.md) |
| 2026-10-16 | Every `apply_url` run walked global backlog (MSU, BU, …) | **`WAYBACK_SLUGS` required habit**; apply script prints slugs; Cell 0 comment | `apply_url_updates.py`, Cell 0, SCRAPE dummies |
| 2026-10-16 | Notebook Cell 3B duplicate of module (no permanent skip in notebook) | **Cell 3B → thin wrapper** calling `run_stage3b_from_globals` | `540_tenure_pipeline.ipynb` cell 3B |
| 2026-10-16 | CLI exec’d 691-line inline 3B | CLI: Cell 0 + module only | `run_stage3b_cli.py` |
| 2026-10-16 | macOS `python3` = 3.9 broke probe/apply | `tenure/lib/tenure_python.sh` + `./apply_url_updates.sh`, `./probe_faculty_url.sh`, etc.; `.vscode/settings.json` → tenure_net | repo root |
| 2026-10-16 | Notebook re-queued ASU read-back failures, then would do the same to every other missing school | Write probe at start of 3B; abort with no new index rows if the save fails | `stage3b_download.py` |
| 2026-10-16 | Terminal run still lost ASU HTML on Dropbox (`stat -1`) after a successful test save | If the Dropbox save does not stick, write the same file under `~/Desktop/faculty_snapshots` (already on the search list) | `stage3b_download.py` |
| 2026-10-16 | Same `stat -1` on Desktop. Microsoft Defender quarantines the page as `Trojan:JS/Nemucod` ~1–3s after save | If the file disappears, save it again with `<script>` blocks removed (faculty text kept) | `stage3b_download.py` |

*Append new rows here when we change 3B behavior — one line per fix is enough.*

---

## Document history

| Date | Change |
|------|--------|
| 2026-10-16 | Created — slug filter, permanent skip, read-back verify, fix changelog |
