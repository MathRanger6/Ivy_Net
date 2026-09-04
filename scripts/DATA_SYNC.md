# Ivy_Net data sync: Git vs rsync (HPC ↔ Mac)

This document is the **single place** to answer: *What lives in Git? What is gitignored? What do I `rsync`? How do I get Slurm logs and sweep results onto my Mac for Cursor?*

**Cross-domain guides (Git, filing):** [`docs/README.md`](../docs/README.md)

**Related scripts**

| Script | Purpose |
|--------|---------|
| [`pull_big_data.sh`](./pull_big_data.sh) | **Big Fish unzipped CSVs** + **`datasets/mbb/`** — unzip from git zips (Mac) or rsync HPC ↔ Mac. |
| [`rsync_pull_from_hpc.sh`](./rsync_pull_from_hpc.sh) | Pull one subtree (or `all` default targets, or `sweep`). |
| [`rsync_push_to_hpc.sh`](./rsync_push_to_hpc.sh) | Push code/small files to Rivanna; avoids clobbering HPC-generated blobs. |
| [`rsync_pull_recent_hpc.sh`](./rsync_pull_recent_hpc.sh) | **One command** to refresh logs + sweep + (optionally) tenure outputs — see below. |
| [`rsync_hpc_include.sh`](./rsync_hpc_include.sh) | Shared rsync excludes and helpers (sourced by the above). |
| [`clear_slurm.sh`](./clear_slurm.sh) | Delete local `slurm_out/` and legacy root `slurm-*.{out,err}` logs. |

Configuration overrides (all rsync scripts): **`HPC_USER`**, **`HPC_HOST`**, **`HPC_REPO`** (defaults: `dzk3ja`, `login.hpc.virginia.edu`, `~/Ivy_Net`). Dry run: **`DRY_RUN=1`**.

---

## 1. Strategy in one picture

- **Git (push / pull):** Source code, notebooks, `.slurm`, docs, small config. Anything you want **versioned**, **diffed**, and **shared via GitHub**.
- **rsync:** Large or generated artifacts, Slurm logs, sweep outputs, panels, OpenAlex JSONLs — **gitignored** (or not tracked) but **needed on both machines**.
- **HPC-only / manual:** Things too big or unnecessary on a laptop (e.g. full HTML snapshot trees, full DBLP parsed JSONL).

There is intentional overlap in *rules*: `.gitignore` tells Git “don’t commit this,” and `rsync_hpc_include.sh` tells rsync “don’t push stale Mac copies over HPC” or “don’t pull multi-GB trees.” When you add a **new generated path**, update **both** `.gitignore` (if it must never be committed) and the rsync excludes (if push/pull behavior should change). This file’s tables below help avoid forgetting one side.

---

## 2. Quick reference: where does this file live?

| Kind of data | Typical path | In Git? | Pull to Mac (rsync) | Push Mac → HPC |
|--------------|--------------|---------|---------------------|----------------|
| Pipeline code, Cell 0, `.py` in `tenure_pipeline` | `tenure/tenure_pipeline/*.py` | Yes | Optional (Git usually enough) | Yes (`rsync_push` or Git) |
| Generated JSONL/CSV panels, OA files, PNGs | `tenure/tenure_pipeline/*.jsonl`, etc. | **No** (`.gitignore`) | Yes — `rsync_pull … tenure/tenure_pipeline` | **Guarded** — push excludes skip large HPC outputs |
| HTML Wayback captures | `**/faculty_snapshots/` | **No** | **No** (excluded; HPC-first) | **No** |
| DBLP parsed yearly JSONL | `tenure/tenure_pipeline/dblp_parsed/` | Ignored / huge | **No** (excluded) | N/A |
| Slurm `.out` / `.err` | `slurm_out/slurm-*.{out,err}` (and legacy repo root) | **No** | Yes — `logs` or `quick` / `all` | Rarely needed |
| Papermill output notebook | `slurm-*-output.ipynb` (often repo root) | **No** | Use same pull as parent dir or copy manually | Optional |
| Faithful 537 sweep tree | `sports/outputs/simulation_sweeps/rivanna_faithful_537/`, CSVs, plots | **No** | Yes — `sweep` or `quick` | Sweep **code** yes; **results** pull-only via excludes |
| Faithful 538 sweep tree | `rivanna_faithful_538/`, `faithful_538_*` CSVs/plots | **No** | Yes — `sweep` or `quick` | Sweep **code** via `sweep` or Git; `empirical_perf_fit.json` is **Git-tracked** at `datasets/mbb/` (see `README_TRACKED_ARTIFACTS.md`) |
| DBLP XML | `python_packages/dblp-parser/dblp.xml`, `datasets/` | **No** | Manual / intentional only | Manual |
| Big Fish unzipped CSVs (football ~178MB, LoL ~72MB) | `datasets/football/.../football_big_fish_player_season_panel.csv`, `datasets/legends/lol_big_fish_player_split_panel.csv` | **No** (`.gitignore`; **`.zip` in Git**) | **`./scripts/pull_big_data.sh unzip`** (Mac) or **`from-hpc`** | **`to-hpc`** after unzip on Mac |
| Bulk MBB CSV/SQLite | `datasets/mbb/**` | **No** (except small JSON) | **`./scripts/pull_big_data.sh from-hpc mbb`** | **`to-hpc mbb`** |

---

## 3. “I submitted from my phone” → work in local Cursor

**Typical flow**

1. On Rivanna (Terminus or later on a laptop): `cd ~/Ivy_Net` and `sbatch sim_job.slurm` (or `pipe_job.slurm`, etc.). Note **job IDs** if you want.
2. When jobs have produced output (or failed), on your **Mac** in the Ivy_Net clone:

   ```bash
   # See what would transfer (optional):
   DRY_RUN=1 ./scripts/rsync_pull_recent_hpc.sh quick

   # Pull Slurm logs + 537 sweep artifacts (no full tenure tree):
   ./scripts/rsync_pull_recent_hpc.sh quick
   ```

3. If you also need refreshed **tenure pipeline** panels, OA files, PNGs under `tenure/tenure_pipeline/`:

   ```bash
   ./scripts/rsync_pull_recent_hpc.sh all
   ```

4. Open **Cursor** on the Mac repo; the agent can read **`slurm_out/`**, **`rivanna_faithful_537/`** / **`rivanna_faithful_538/`**, and pulled JSONLs/CSVs.

**Git** does *not* replace this step for logs or sweep results — those paths are gitignored by design.

---

## 4b. Big data: `pull_big_data.sh`

Git tracks **`.zip` archives only** for Big Fish panels (GitHub 100MB cap). Unzipped CSVs and bulk MBB live on disk and sync via this script.

| Command | When | What |
|---------|------|------|
| `./scripts/pull_big_data.sh` | **Mac, after `git pull`** | Unzip football + LoL CSVs from zips in repo (no SSH) |
| `./scripts/pull_big_data.sh from-hpc` | Mac needs HPC copy | Pull Big Fish CSVs + `datasets/mbb/` |
| `./scripts/pull_big_data.sh from-hpc big-fish` | Legends/football only | Big Fish CSVs only |
| `./scripts/pull_big_data.sh to-hpc` | Mac → Rivanna | Big Fish + **education** + `datasets/mbb/` |
| `./scripts/pull_big_data.sh to-hpc big-fish` | Mac → Rivanna | LoL + football unzipped CSVs only |
| `./scripts/pull_big_data.sh to-hpc education` | Mac → Rivanna | `datasets/nels88/` + `datasets/hsb80/` |
| `./scripts/pull_big_data.sh from-hpc education` | Rivanna → Mac | NELS88 + HS&B80 |
| `DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc big-fish` | Preview | No writes |

**Run on Mac, not Rivanna.** `to-hpc` pushes **from this Mac** to `~/Ivy_Net` on Rivanna over SSH. Running it on Rivanna tries to SSH back into Rivanna from Rivanna — wrong direction and repeated password prompts.

**Typical Mac workflow:** `git pull` → `./scripts/pull_big_data.sh unzip` → work in Cursor.

**Typical Rivanna workflow (two steps, two machines):**

1. **Mac:** `git push` (scripts + small tracked files) and `./scripts/pull_big_data.sh to-hpc big-fish` (large gitignored CSVs).
2. **Rivanna:** `git pull` only — **do not** run `pull_big_data.sh to-hpc` on Rivanna.

NELS88 / HS&B80 CSVs are **already in Git** (~4–10 MB); `git pull` on Rivanna gets them. `to-hpc education` is optional belt-and-suspenders if you want rsync to mirror those folders too.

Football zip note: archive is a **flat** `.csv`; `unzip` moves it into `football_big_fish_player_season_panel/`.

### SSH: password once vs key (no password)

Rsync talks to Rivanna over **SSH**. UVA can ask for your **password** (and sometimes **2FA/Duo**) on each new SSH connection.

**What we fixed in the script:** one rsync transfer + **connection reuse** → at most **one** password prompt per script run (not one per file).

**Optional — use an SSH key so rsync never asks:**

1. You have a **key pair**: private key (secret, stays on Mac) + public key (registered on Rivanna). The repo’s `ivy_net_keys` / `ivy_net_keys.pub` may be yours if you set that up — private key is gitignored.
2. **`ssh-add`** tells macOS: “remember this private key for this session.” After that, SSH (and rsync) present the key automatically instead of prompting for a password.

```bash
# Once per Mac login session (adjust path to your private key):
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
# or, if you use the repo key:
# ssh-add --apple-use-keychain "/path/to/Ivy_Net/ivy_net_keys"

# Test — should print nothing and exit 0 (no password prompt):
ssh -o BatchMode=yes dzk3ja@login.hpc.virginia.edu true
```

If the test **fails**, rsync will keep asking for passwords — fix key setup on Rivanna first (public key in `~/.ssh/authorized_keys`), or just type your password once per `pull_big_data.sh` run.

---

## 5. `rsync_pull_recent_hpc.sh` (one-shot refresh)

Run from **Mac**, repo root or any directory (script resolves paths).

| Command | What it pulls (HPC → Mac) |
|---------|---------------------------|
| `./scripts/rsync_pull_recent_hpc.sh` | Same as **`all`** |
| `./scripts/rsync_pull_recent_hpc.sh all` | `slurm_out/` + faithful 537 **`sweep`** include rules + **`tenure/tenure_pipeline`** |
| `./scripts/rsync_pull_recent_hpc.sh quick` | `slurm_out/` + **`sweep`** only — good after **`sim_job.slurm`** / 537 |
| `./scripts/rsync_pull_recent_hpc.sh logs` | **`slurm_out/`** only |
| `./scripts/rsync_pull_recent_hpc.sh sweep` | Sweep results only (same as `rsync_pull_from_hpc.sh sweep`) |
| `./scripts/rsync_pull_recent_hpc.sh tenure` | **`tenure/tenure_pipeline`** only |

Dry run: `DRY_RUN=1 ./scripts/rsync_pull_recent_hpc.sh quick`

Help: `./scripts/rsync_pull_recent_hpc.sh --help`

---

## 6. Lower-level: `rsync_pull_from_hpc.sh` / `rsync_push_to_hpc.sh`

**Pull** any subtree the helper supports:

```bash
./scripts/rsync_pull_from_hpc.sh                           # default: tenure/tenure_pipeline
./scripts/rsync_pull_from_hpc.sh tenure/tenure_pipeline
./scripts/rsync_pull_from_hpc.sh slurm_out                 # Slurm logs → local slurm_out/
./scripts/rsync_pull_from_hpc.sh sweep                     # 537 sweep artifacts only
./scripts/rsync_pull_from_hpc.sh all                       # each default target in IVY_RSYNC_DEFAULT_TARGETS
```

**Push** (code up; large generated files excluded so HPC data is not overwritten from an empty/stale Mac):

```bash
./scripts/rsync_push_to_hpc.sh                            # default tenure/tenure_pipeline (code side)
./scripts/rsync_push_to_hpc.sh sports/outputs/simulation_sweeps   # sweep *sources* (see excludes)
./scripts/rsync_push_to_hpc.sh all
```

Always read the **excludes** in [`rsync_hpc_include.sh`](./rsync_hpc_include.sh) before assuming a path round-trips.

---

## 7. `clear_slurm.sh` (local cleanup only)

Runs in your **local** clone (or anywhere you point the script); **does not** touch Rivanna.

- Deletes **`$REPO_ROOT/slurm_out/slurm-*.*`**
- Deletes legacy **`$REPO_ROOT/slurm-*.*`** in the repo root

It does **not** remove **`slurm-*-output.ipynb`** papermill outputs (different filename pattern). Remove those by hand if needed.

---

## 8. Git: `.gitignore` philosophy

- **Secrets and env:** `.env`, keys — never commit.
- **Slurm:** `slurm-*.out`, `slurm-*.err`, `slurm-*-output.ipynb` anywhere under the repo (unqualified patterns match in subdirectories, so **`slurm_out/`** is covered).
- **Tenure pipeline outputs:** large JSONL/CSV/cache paths under `tenure/tenure_pipeline/` — see `.gitignore` for the full list.
- **Sports 537:** sweep streams, `rivanna_faithful_537/`, plots — sync via rsync.
- **HTML / DBLP dump / faculty_snapshots:** excluded from normal sync and Git.

Your **VA weekend checklist** habit — *check `git status` before commit* — is the right safeguard against accidentally staging a generated file if someone removes a `.gitignore` rule.

---

## 9. What rsync intentionally does **not** do

- **`faculty_snapshots/`** — huge HTML archive; stays HPC-centric; excluded from pull/push in the shared config.
- **`dblp_parsed/`** — hundreds of MB JSONL; pull excluded; regenerate or copy intentionally if you really need it on Mac.
- **DBLP `dblp.xml`** — multi-GB; excluded; copy manually when needed.

If you need a *small* subset of snapshots on Mac, use a **manual** `rsync` with tight includes, or export derived tables only (JSONL panels).

---

## 10. Keeping Git and rsync aligned (checklist)

When you introduce a **new** generated artifact:

1. Should it **ever** be on GitHub? If **no**, add to **`.gitignore`**.
2. Should **Mac → HPC** push skip it (HPC is source of truth)? If yes, add **`_IVY_RSYNC_PUSH_EXCLUDES`** in `rsync_hpc_include.sh`.
3. Should **HPC → Mac** pull include it? If it lives under an excluded directory, add an **`--include`** pattern (similar to `ivy_rsync_pull_sweep`) or pull a new subtree.
4. Add a **row or footnote** in the table in **§2** of this file so future you remembers.

---

## 11. Troubleshooting

| Problem | Things to check |
|---------|------------------|
| Empty **`slurm_out/`** on Mac after pull | No jobs yet with new `#SBATCH` paths; or wrong `HPC_REPO`; or pull never run — run `quick` or `logs`. |
| Sweep folder missing locally | Run `./scripts/rsync_pull_from_hpc.sh sweep` or `quick`; confirm paths on HPC under `sports/outputs/simulation_sweeps/`. |
| Mac overwrote HPC data after push | Push excludes should prevent large JSONL push; verify `rsync_hpc_include.sh` lists your file. |
| `git status` shows huge unwanted files | Add `.gitignore` rules; `git rm --cached` if already staged once. |
| rsync slow | Normal for first full `tenure/tenure_pipeline` pull; use **`quick`** when you only need logs + sweep. |
| rsync asks password **every file** | Old script pushed one file per SSH session — fixed in `rsync_hpc_include.sh` (single rsync + `ControlMaster`). Update scripts; run **`to-hpc big-fish`** if you only need LoL/football (~250 MB), not full `datasets/mbb/`. Load SSH key with **`ssh-add`**. |

---

## 12. See also

- [`../tenure/HPC_SLURM_PIPELINE_GUIDE.md`](../tenure/HPC_SLURM_PIPELINE_GUIDE.md) — Slurm, `slurm_out/`, `track_slurm.sh`
- [`../tenure/documents/VA_WEEKEND_CHECKLIST.md`](../tenure/documents/VA_WEEKEND_CHECKLIST.md) — commit discipline, typical `sbatch` commands
- [`../sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md`](../sports/documents/Rivanna_Faithful_537_Sweep_For_Dummies.md) — 537 workflow and rsync **`sweep`**
