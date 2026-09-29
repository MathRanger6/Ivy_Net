# ELS:2002 public-source files

The official NCES public-use ELS:2002 files downloaded on 2026-09-28 are stored under `source_public_nces_20260928/`.

That dated source directory is intentionally excluded from Git and included in the repository's `education` rsync scope. From the Mac repository root:

```bash
DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc education
./scripts/pull_big_data.sh to-hpc education
```

Official source: `https://nces.ed.gov/datalab/onlinecodebook/`, survey 11, 2002–12 PETS public-use release. The retained packages include the Stata student file, balanced-repeated-replication weight file, school and institution files, and codebook/record layouts.

The public student file contains prior achievement, application counts, postsecondary selectivity, transcript, and degree variables. Its common student-to-school identifier is suppressed. Do not use the public file to reconstruct high-school peer pools.
