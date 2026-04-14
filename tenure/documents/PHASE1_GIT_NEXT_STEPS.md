# Phase 1 Git — what was done + what you do next

## Done in the workspace (automated)

1. **`.gitignore`** at repo root — ignores `**/faculty_snapshots/`, huge `dblp.xml`, `.env`, `__pycache__`, checkpoints, `obsolete_*`, `deleted_files/`, etc.
2. **`.env.example`** — template for `OPENALEX_API_KEY` (copy to `.env`; never commit `.env`).
3. **`openalex_resolver.py`** — API key is read from **`OPENALEX_API_KEY`** (no secret in source). Set your **new** key in the environment or in `.env` (load `.env` manually or via your shell / IDE).
4. **`git init`** + initial commit (if the assistant ran it — see `git log`).

## Your steps (once per machine)

### A. Put your OpenAlex key where Python sees it

Pick one:

- **Terminal / Jupyter:**  
  `export OPENALEX_API_KEY='your-new-key'`  
  (add to `~/.zshrc` or conda `env_vars` if you want it permanent for `tenure_net`.)

- **File:** Copy **`.env.example`** → **`.env`** in the repo root, set `OPENALEX_API_KEY=...`. Jupyter does **not** auto-load `.env` unless you use a loader or run notebooks from a shell that `source`s it — **export** is the most reliable for notebooks.

### B. Create the GitHub repo (browser)

1. GitHub → **New repository** → **Private**.
2. Name e.g. `pde-workspace` or `dissertation-pde`.
3. **Do not** add README / .gitignore / license (we already have files locally).

### C. Connect and push (terminal, repo root)

```bash
cd "/path/to/Cursor Workspace PDE"
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Use **HTTPS + personal access token** or **SSH** per GitHub’s docs.

### D. Rivanna later

Same: `git clone` your repo, set `OPENALEX_API_KEY` in the job environment or `~/.bashrc` on the cluster.

---

*See also `WORKSPACE_CLEANUP_ROADMAP.md` Phase 1.*
