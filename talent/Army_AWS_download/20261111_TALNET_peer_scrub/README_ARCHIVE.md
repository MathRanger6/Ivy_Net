# Vantage download archive — 2026-11-11 peer scrub

**Purpose:** Keep the DOD SAFE peer-scrub bundle for diff and recovery. **Not** ship-shape source of truth (see sync verdict below).

**Original drop:**  
`6-PDE_Work/4-PDE_VANTAGE/Downloaded_files/DOD SAFE-JJsa4kDiTVSHgt3P/`  
(Keep that tree; this folder is a **repo copy** so nothing is lost if the safe folder moves.)

**Also in repo:** `talent/Army_AWS_download/20261111_TALNET_peer_scrub.zip`

## Sync verdict (2026-11-12 file-by-file)

- **Ingested into git:** `functionsG.py` → `talent/talent_pipeline/functionsG.py`
- **Canonical for Vantage upload:** `talent/talent_pipeline/`, `talent/re_entry/`, `sports/scripts/`
- **This archive behind on:** `POOL_GROUPING_MODE='legacy'` in bundled `pipeline_config.py`, thinner `army_basic_plots.py`, 520 scratch/debug cells

## Worth keeping here only (not standard upload)

| Artifact | Why keep |
|----------|----------|
| `pipeline_config_27Apr_strata.py` | Strata experiment |
| `cox_plot_helpers_27Apr_strata.py` | Paired helper |
| `520_pipeline_cox_working_27Apr_strata.ipynb` | Strata notebook |
| `pipeline_config_new1.py` | Ad hoc config |
| `f506.py`, `f509_uic_tools.py` | Vantage naming variants |
| Full scrub `520_pipeline_cox_working.ipynb` | Rater-ID debug cells + outputs |

**Do not delete** when cleaning canonical paths — diff against this tree if Vantage behavior diverges.
