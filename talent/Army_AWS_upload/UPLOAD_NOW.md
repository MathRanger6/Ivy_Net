# Upload tonight (OneDrive → Up to PDE)

**One file for PDE / virtual desktop:**

| File | Size (approx) | Put in OneDrive |
|------|---------------|-----------------|
| **`VANTAGE_UPTOPDE_20261112_b13_FULL.zip`** | ~4.8 MB | **Up to PDE** folder |

After unzip on VDI you get **`README.md`**, **`README_TRANSFER.md`**, **`ship_shape/`**, **`archive_peer_scrub/`**, **`provisional_next/`** (no extra wrapper folder).

## You do not upload

- `VANTAGE_UPTOPDE_20261112.zip` — old bundle (superseded)
- `VANTAGE_UPTOPDE_20261112_b13.zip` — ship_shape only, incomplete
- Loose `VANTAGE_REPLACE_20261112/` — already inside `ship_shape` in the zip
- Repo-only folders under `Army_AWS_upload/` that are not the zip above

## Smoke on VDI (after copy)

1. Deploy **`ship_shape/`** → 520 workspace root (`README_TRANSFER.md`).
2. Cell 0: `pipeline_config_div_name`
3. Cells 0–11, then `python talent/re_entry/army_hero_grid_runner.py --quick`

**Mac:** keep working in Cursor; pull Vantage results back after smoke.
