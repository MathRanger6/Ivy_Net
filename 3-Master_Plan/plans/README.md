# Plan mirrors (Cursor Plan mode → git)

**Where Charles reads plans:** this folder — [`3-Master_Plan/plans/`](.) — **not** `~/.cursor/plans/` on your Mac.

Cursor Plan mode writes live files to `~/.cursor/plans/` (outside git). Important plans are **mirrored here** so they sync via Dropbox/git, work on Rivanna after `git pull`, and can be converted to PDF.

**Re-entering or lost?** Start at [`re_entry/00_READ_ME_FIRST.md`](../re_entry/00_READ_ME_FIRST.md) — not this folder.

## Quick reference (immersed mode)

| You want… | Open this |
|-----------|-----------|
| Read / print a plan | `3-Master_Plan/plans/*.plan.md` (below) |
| PDF | `./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/plans/20260721_hero_model_reset.plan.md` |
| See what’s mirrored | `./scripts/mirror_plan.sh --list` |
| Refresh after IDE edits | `./scripts/mirror_plan.sh hero_model_reset` |

## Current mirrors

| Repo file | Topic |
|-----------|--------|
| [`20260721_hero_model_reset.plan.md`](20260721_hero_model_reset.plan.md) | Three model layers, hero vs sim, smart restart |
| [`20260524_tier1_plan_map.plan.md`](20260524_tier1_plan_map.plan.md) | Doc ecosystem / tier1 map |
| [`20260615_pd12_compass_reassessment.plan.md`](20260615_pd12_compass_reassessment.plan.md) | PD12 COMPASS reassessment |
| [`20260617_primary_focus_now.plan.md`](20260617_primary_focus_now.plan.md) | Model work vs reading rabbit holes |

## Two-tier policy

| Location | Role |
|----------|------|
| **`~/.cursor/plans/*.plan.md`** | Live IDE workspace — Plan-mode UI, todos (Mac only) |
| **`3-Master_Plan/plans/*.plan.md`** | **Canonical mirror** — git, Rivanna, PDF source |

## Keep vs ephemeral (for agents)

**Mirror (keep)** — run `./scripts/mirror_plan.sh <slug>` after substantive edits:

- Scientific / sequencing plans (hero, tier1, PD12, COMPASS)
- Multi-section plans Charles should read
- Anything referenced from `3-Master_Plan/` handoffs
- User says the plan matters for Rivanna or git

**Skip mirror (ephemeral)** — leave in `~/.cursor/plans/` only:

- `fix_*`, `plans_git_*` (script skips unless `--force`)
- One-off git/UI/tooling fixes
- User says `skip mirror`

When a plan also has a **polished memo** in a domain folder, update the memo when the scientific content changes materially — but the **plan mirror** is always the minimum repo copy for agents and PDF.

## Naming

Repo mirrors: `YYYYMMDD_<short_slug>.plan.md` (no Cursor hash).  
Re-running `./scripts/mirror_plan.sh <slug>` updates the existing `*_<slug>.plan.md` file.

## Git commits

Include `3-Master_Plan/plans/*.md` with `.specstory/history/*.md` on agent sweeps. See [`AGENTS.md`](../../AGENTS.md).

## Relation to other docs

- **`.specstory/history/`** — chat archives (automatic; references plans but does not copy them)
- **`3-Master_Plan/plans/`** — plan mirrors (this folder; use `mirror_plan.sh`)
- **`3-Master_Plan/`** root — COMPASS guidance, agent reports
- **Domain memos** — optional human-polished layer for reading/advisor
