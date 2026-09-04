# DISPOSABLE — Big Fish datasets assessment (2026-09-03)

**Purpose:** COMPASS read on Alex’s Sep 2–3 “Big Fish” panels — fit for HERO / peer-context / cross-domain work.  
**Source:** Alex Gates emails in each `datasets/*/Re_ New dataset for Big Fish.eml`.  
**Active focus (Charles):** **Legends (LoL)** — see [`legends_sandbox/_DISPOSABLE_legends_hero_thread.md`](legends_sandbox/_DISPOSABLE_legends_hero_thread.md).

**Say `anchor`** in chat to paste the priority table below.

---

## YOU ARE HERE

| Priority | Dataset | Path | Usefulness | Next action |
|----------|---------|------|------------|-------------|
| **1 (now)** | **Legends (LoL)** | `datasets/legends/` | **High** | First BDP + dev-cohort HERO porch |
| 2 | Football | `datasets/football/` | **High** | Eligible-cohort BDP after legends |
| 3 | NELS88 | `datasets/nels88/` | **Med–high** | Light porch on `analytic_sample_min10` |
| 4 | HSB80 | `datasets/hsb80/` | **Medium** | Cohort-split porch (Soph vs Senior) |
| 5 | Apache | `datasets/Apache/` | **Med–high** | Activity-screened PMC promotion porch |

**Alex one-liner:** Same **Big Fish** skeleton everywhere — own performance (Â analog), leave-one-out peer context, pond/unit ID, downstream Y — so tooling can reuse MBB/tenure patterns where selection is clear.

---

## Naming map (Charles shorthand → repo)

| Charles said | Actual folder | Domain |
|--------------|---------------|--------|
| **league** | `datasets/legends/` | League of Legends esports |
| **nlb88** | `datasets/nels88/` | NELS:88 education |
| football | `datasets/football/` | FBS → NFL draft |
| hsb80 | `datasets/hsb80/` | HS&B:80 education |
| apache | `datasets/Apache/` | Apache OSS → PMC |

---

## Overall verdict

**All five could be useful**, but for different jobs:

| Dataset | Best role in dissertation |
|---------|---------------------------|
| **Legends** | Fourth empirical domain with a **real advancement gate** (dev → top tier) |
| **Football** | Second **sports/draft** replication of MBB |
| **Apache** | **Open-source governance** domain — promotion to PMC as Y |
| **NELS88** | Education “small pond” **complement** to tenure |
| **HSB80** | Larger education **robustness** check (cohort-split) |

None replace **MBB** or **tenure** as anchors. They extend cross-domain coverage and give Alex’s Big Fish framework more places to land.

---

## Binding frame (environment ≠ advancement)

| Domain | Environment (pond LOO) | Advancement Y | Selection clarity |
|--------|----------------------|---------------|-------------------|
| MBB (anchor) | team LOO | draft | Strong |
| Tenure (anchor) | dept LOO | tenure | Strong |
| **Legends** | dev-team LOO | top-tier promotion | **Strong** |
| **Football** | team LOO | NFL draft | **Strong** |
| **Apache** | project-year candidate pool LOO | PMC promotion | **Strong** (with roster censor caveat) |
| **NELS / HSB** | school LOO | degree attainment | **Weaker** (attainment ≠ top-K select) |

---

## 1. Legends (LoL) — **highest priority**

**Path:** `datasets/legends/lol_big_fish_player_split_panel.csv`  
**Docs:** [`datasets/legends/README.md`](../../../datasets/legends/README.md)

| Stat | Value |
|------|-------|
| Rows | 66,752 player×team×league×split×position stints |
| Columns | 84 |
| Years | 2015–2026 |
| Unique players | ~10,664 |

| HERO slot | Column | Fill / note |
|-----------|--------|-------------|
| Unit | `player_period_id` | 100% |
| Pond | `teamid` / dev league split | Explicit `league_tier` |
| **Â** | `own_performance_index` | 79.6% |
| **Peer LOO** | `teammate_mean_performance_excl_self` | 91.7% — primary LOO |
| Same-role LOO | `same_role_mean_performance_excl_self` | 26.6% — sparse |
| **Y** | `top_tier_debut_within_1y` / `_2y` | 3,052 / 4,456 True |
| Censor | `full_1y_followup`, `full_2y_followup` | Required before treating False as failure |
| Cohort filter | `eligible_developmental_cohort` | ~15,983 dev rows |

**Why useful:** Alex built this for the project. Dev-league → top-tier promotion is a clean advancement gate. Tier labels (`developmental` / `top` / `other`) support environment vs advancement separation. N is healthy for porch + elite-pond probes.

**Caveats:** Higher roster churn than MBB; esports may need one framing sentence for general readers; `same_role` LOO too sparse for primary spec.

**COMPASS read:** **Start here.** Full `legends_sandbox/` mirroring tenure/MBB BDP → HERO porch on dev cohort.

---

## 2. Football — strong MBB parallel

**Path:** `datasets/football/football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv`

| Stat | Value |
|------|-------|
| Rows | 168,165 player-seasons |
| Eligible cohort | 70,633 (`eligible_analysis_cohort == 1`) |
| Seasons | 2014–2024 |
| Unique players | ~65,030 |

| HERO slot | Column | Note |
|-----------|--------|------|
| **Â** | `own_performance_index` | 100% in eligible cohort; ~42% overall |
| **Peer LOO** | `teammate_mean_performance_excl_self` | 99.9% |
| Same-group LOO | `same_group_mean_performance_excl_self` | 72.2% |
| **Y** | `drafted_next_draft` | ~**2.7%** in eligible (~1,900 picks) |

**Why useful:** Draft-as-advancement, team-as-pond — structurally closest to MBB after LoL. Large eligible N; recruiting ranks as priors.

**Caveats:** Very sparse Y; OL / low-snap roles missing performance; only ~11 seasons; public data limits on opportunity for many positions.

**COMPASS read:** Worth `football_sandbox/` after legends — analyze by `position_group` (QB/WR/DB vs OL).

---

## 3. Apache — OSS governance, real promotion gate

**Path:** `datasets/Apache/apache_big_fish_panel.csv`  
**Alex blurb:** 10,537 contributors · 8 major projects · 2015–2024 · Git commits + activity → **PMC promotion**.

| Stat | Value |
|------|-------|
| Rows | 14,217 contributor×project×year |
| Unique persons | ~10,537 |
| Projects | 8 (airflow, beam, kafka, arrow, superset, nifi, cassandra, lucene) |
| **Y (next year)** | 174 promotions (~1.2% raw) |
| **Y (2y)** | 302 promotions |
| Activity screen (`meets_activity_screen_3plus`) | 4,518 rows → 155 next-y promos (~**3.4%**) |

| HERO slot | Column | Note |
|-----------|--------|------|
| Pond | `project` × `performance_year` | ~260 median `team_active_candidates` per project-year |
| **Â (own)** | `commits` (+ `within_team_percentile`, `own_top_decile`) | Annual commit volume |
| **Peer LOO** | `peer_mean_commits_loo` | 100% — LOO over active promotion candidates |
| Relative | `relative_to_peer_mean`, `peers_above` | Pre-built |
| Congestion proxy | `peer_top_decile_count_loo` | Count of top-decile peers in pond |
| **Y** | `promoted_to_pmc_next_year` / `promoted_to_pmc_within_2y` | Use `outcome_*_complete` flags |
| Screen | `meets_activity_screen_3plus` | Restrict to serious candidates (Alex intent) |

**Why useful:**

- **Novel domain** — neither sports nor academia; “advancement” = PMC seat (governance, not draft/tenure).
- **Pre-built Big Fish LOO** on the *promotion candidate pool* within project-year — closer to “who gets the scarce slot” than education panels.
- **Cross-domain talking point:** peer congestion among active contributors predicts who reaches the management committee.
- Eight projects give a small **multi-pond** structure (project fixed effects or pooled porch).

**Caveats (Alex flagged):**

- Apache publishes **current** rosters, not full historical PMC/committer lists → **some past promotions unobserved** (right-censor / misclassification risk on Y).
- Sparse Y even after activity screen (~155 events in 4.5K screened rows).
- **Â = raw commits** is volume-heavy; no Alex composite index like LoL/football — may need commit-rate or tenure-adjusted ability.
- Identity resolution noisy (`identity_match_method`: mostly email-only).
- Not “selection from a ranked score” in the NFL sense — PMC promotion is partly social/political; score≠select story needs careful wording.

**COMPASS read:** **Med–high** — worth a lightweight porch on activity-screened rows **after** legends + football. Best as a **fifth panel** or appendix “open source governance” vignette, not a chapter anchor. Flag roster censor limitation in any figure caption.

---

## 4. NELS88 — education small pond

**Path:** `datasets/nels88/nels88_big_fish_panel.csv`

| Stat | Value |
|------|-------|
| Rows | 10,545 students |
| Pond | 10th-grade high school (`F1SCH_ID`) |
| Analytic (min 10 peers) | ~7,238 |
| **Y** | `bachelors_or_higher_by_2000` ~**36%** (min-10) |

| HERO slot | Column |
|-----------|--------|
| **Â** | `own_performance_z` (baseline test) |
| **Peer LOO** | `peer_mean_loo`, `peer_mean_z_loo` (~97%) |
| Weights | `followup_weight_2000` |

**Why useful:** Education complement to tenure; fast school LOO porch; connects to classic small-pond literature.

**Caveats:** Sampled students ≠ full school cohort; attainment not competitive selection; single peer snapshot → long lag to Y.

**COMPASS read:** Supporting evidence, not headline domain.

---

## 5. HSB80 — larger education N, cohort split

**Path:** `datasets/hsb80/hsb80_big_fish_panel.csv`

| Stat | Value |
|------|-------|
| Rows | 22,889 (Sophomore 12,630 · Senior 10,259) |
| Analytic min-5 | ~22,058 |
| **Y** | `bachelors_or_higher_by_1986` ~**11%** (min-5; cohort still young) |

**Why useful:** ~2× NELS N; rich covariates (SES, GPA, school type).

**Caveats:** **Analyze Sophomore and Senior separately** (Alex); 1980s follow-up; same attainment-not-selection issue as NELS.

**COMPASS read:** Pair with NELS as mini **education bundle** for robustness.

---

## Suggested sequencing (bandwidth)

1. **Legends** — full sandbox (BDP + HERO porch + dev filter) ← **Charles focus now**
2. **Football** — eligible-cohort BDP / 3×3 where draft N allows
3. **Apache** — activity-screened PMC porch + censor note in caption
4. **NELS + HSB** — one porch each when education cross-domain is needed

---

## Thread log

| Date | Entry |
|------|-------|
| 2026-09-03 | Initial COMPASS assessment of football, legends, nels88, hsb80, apache; legends selected as active focus. |
