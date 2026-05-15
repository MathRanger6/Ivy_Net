# Ivy_Net — Central documents (`docs/`)

Use this folder for guides that apply to **more than one** project area (**talent** / **sports** / **tenure**) or for “how the repo works” (Git, sync, tooling) when there is no natural home in a single domain.

## Where to look first

1. **Domain folder** — topic-specific notes and runbooks:
   - `sports/documents/`
   - `tenure/documents/`
   - `talent/documents/`

2. **`docs/` here** — if the topic is **shared**, or you **cannot** find it under the domain that matches your current work.

## What lives here now

| File | Purpose |
|------|---------|
| [`GIT_MULTIPLE_MACHINES_ELEMENTARY.md`](./GIT_MULTIPLE_MACHINES_ELEMENTARY.md) | Git/GitHub mental model: laptop, HPC, GitHub; first push/clone/pull. |
| [`GIT_FOR_DUMMIES.md`](./GIT_FOR_DUMMIES.md) | Practical Git recipes: stash, rebase, fix staging, recovery. |

## Adding new central docs

- Put the file in **`docs/`** and add one line to the table above.
- From a domain doc, link with a **relative** path, e.g. from `sports/documents/foo.md`: [`../../docs/README.md`](../../docs/README.md).
- Prefer **moving** a misplaced file into `docs/` over **duplicating** it; update links in the same commit.

## Related (not in `docs/`)

- Data sync policy: `scripts/DATA_SYNC.md`
- Root `.gitignore` — what not to commit
