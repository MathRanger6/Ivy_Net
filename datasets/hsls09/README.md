# HSLS:09 public-source files

The official NCES public-use HSLS:09 files downloaded on 2026-09-28 are stored under `source_public_nces_20260928/`.

That dated source directory is intentionally excluded from Git and included in the repository's `education` rsync scope. From the Mac repository root:

```bash
DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc education
./scripts/pull_big_data.sh to-hpc education
```

Official source: `https://nces.ed.gov/datalab/onlinecodebook/`, survey 37, HSLS 2009–16 PETS/PEAR public-use release with 2021 administrative outcomes. The retained packages include the Stata student and school files and codebook/record layouts.

The public student file contains ninth-grade mathematics achievement, application counts, postsecondary selectivity, and outcomes through 2021. Its common student-to-school identifier is suppressed. Do not use the public file to reconstruct high-school peer pools.
