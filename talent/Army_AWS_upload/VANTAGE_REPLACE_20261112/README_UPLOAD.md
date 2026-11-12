# Vantage replace bundle — 2026-11-12

**Source:** Cursor canonical peer-context ship-shape (Nov 2026 file-by-file sync).

## Unpack

1. **520 workspace root** — same level as `big_dfs/`, `talent/`, `sports/`.
2. Back up existing notebook + root `.py` + `talent/re_entry/`.
3. Unzip on Mac, then copy **inner** folder to workspace root:

```bash
cd /path/to/520/workspace/root
unzip -o ~/Downloads/VANTAGE_PEER_CONTEXT_REPLACE_20261112.zip
cp -R VANTAGE_REPLACE_20261112/520_pipeline_cox_working.ipynb .
cp -R VANTAGE_REPLACE_20261112/*.py .
cp -R VANTAGE_REPLACE_20261112/talent/re_entry talent/
cp -R VANTAGE_REPLACE_20261112/sports/scripts sports/
cp VANTAGE_REPLACE_20261112/sports/541_grandchild_homophily_assign.py sports/
cp -R VANTAGE_REPLACE_20261112/docs ./docs
chmod +x talent/re_entry/*.py talent/re_entry/*.sh
```

**Layout after copy:** flat `.py` + notebook at **root**; `talent/re_entry/`; `sports/scripts/`; `sports/541_grandchild_homophily_assign.py`; **`docs/`** (agent background — start at `docs/INDEX_FOR_AGENTS.md`).

## Config

`pipeline_config.py`: `POOL_GROUPING_MODE = 'active_at_eval_thru'`.  
Restart kernel → Cell 0 → `reload_pipeline_config()`.

## Smoke

```bash
./talent/re_entry/army_basic_plots.py --all
./talent/re_entry/army_hero_slide_plot.py
```

See `talent/re_entry/AWS_UPLOAD_CHECKLIST.md` for full BDP.

**Not in zip:** feathers/data; `3-Master_Plan/`.
