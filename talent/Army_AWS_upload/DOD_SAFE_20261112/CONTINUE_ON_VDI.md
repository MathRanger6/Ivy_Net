# Continue working tonight (after smoke)

**Smoke:** deploy **`ship_shape/`** only (see `README_TRANSFER.md`).

**Do not lose tonight’s work** — keep this staging folder on the VDI (e.g. `~/VANTAGE_B13_staging/`) and edit here; paste winners into the live 520 root when ready.

## Folders

| Folder | Use tonight |
|--------|-------------|
| **`ship_shape/`** | Production copy → 520 workspace root |
| **`provisional_next/`** | Diff/paste targets after smoke (configs, 520, helpers) |
| **`continue_tonight/`** | **Working docs** — edit `Peer_Context_prep_for_battle.md` here; copy into workspace `docs/` when done |
| **`ship_shape/docs/`** | Same docs at deploy path — refresh from `continue_tonight/` after edits |
| **`ship_shape/talent_pipeline_mirror/`** | Extra `.py` from Mac git **not** at flat ship root — copy to root only if a cell needs them |
| **`archive_peer_scrub/`** | Reference only |

## Mac ↔ VDI tonight

- **VDI → Mac:** zip edited files from staging; Dropbox/OneDrive back to Mac; drop into `talent/talent_pipeline/` or `3-Master_Plan/re_entry/`.
- **Mac → VDI:** you will not get another bundle until tomorrow — everything for tonight must be **in this zip**.

## HERO smoke commands

```bash
python talent/re_entry/army_hero_grid_runner.py --quick
```
