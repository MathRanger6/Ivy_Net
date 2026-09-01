# Archive — HERO permutation sweep (64-cell deck)

**Status:** Developmental — tells the LOO vs poolq / ever vs season / all-ps vs last-ps story.  
**Not** the Alex lock population.

## What this is

Full factorial sweep of HERO `pass_a_empirical_bundle.py` knobs (Aug 2026). Outputs were written flat into `hero/` before housekeeping moved them here.

## Recreate

```bash
# Full sweep (~64 runs)
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero_permutation_sweep.zsh

# Slide manifest (commands per cell)
# See hero_permutation_slides/manifest.json in this folder
python sports/scripts/build_hero_permutation_slides.py  # if rebuilding PDF deck
```

## Key single runs

| Run | Command gist |
|-----|----------------|
| OLD FIXED (11–21 all-ps) | `--output-tag FIXED_HERO` |
| NEW FIXED (13–21 last-ps) | `--season-min 2013 --season-max 2021 --panel-rows last-ps` |
| mg=0 sensitivity | `--min-team-season-games 0` |

Canonical NEW FIXED should live in [`../hero/`](../hero/) after rerun — not in this archive.

## Related

- [`../hero_permutation_slides/manifest.json`](hero_permutation_slides/manifest.json) — per-cell CLI strings
- Disposable: [`../../_DISPOSABLE_Alex_hero_population_thread.md`](../../_DISPOSABLE_Alex_hero_population_thread.md)
