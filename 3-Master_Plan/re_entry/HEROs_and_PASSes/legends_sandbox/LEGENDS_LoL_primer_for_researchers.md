# League of Legends — primer for researchers

**Audience:** Charles (and advisors) with FPS / sim background (e.g. Apex, War Thunder), **no MOBA experience**.  
**Purpose:** Enough context to read Alex’s Big Fish panel, talk through a data story, and map LoL esports to the HERO frame (environment ≠ advancement).  
**Data:** [`datasets/legends/lol_big_fish_player_split_panel.csv`](../../../../datasets/legends/lol_big_fish_player_split_panel.csv) · column map in [`datasets/legends/README.md`](../../../../datasets/legends/README.md)

---

## 1. What League of Legends is

**League of Legends (LoL)** is a **5v5 team MOBA** (multiplayer online battle arena). It is **not** a battle royale or vehicle sim.

| If you know… | LoL analogue |
|--------------|--------------|
| Apex squad | Fixed **5-player team**, fixed **roles** for the whole match |
| Match → loot → circle | One **map**, one **objective** (destroy the enemy base) |
| War Thunder BR tiers | **Leagues/tiers** of pro competition (regional + “major” leagues) |
| Ranked ladder | **Pro circuit**: orgs, contracts, promotion between league levels |

Each match is roughly **25–45 minutes**. Deaths matter (respawn after a timer), but there is no “next ring” — the win condition is destroying the enemy **Nexus** (home base) after pushing through **lanes** and **towers**.

---

## 2. One match in plain English

1. **Two teams of five** spawn on opposite sides of **Summoner’s Rift** (the standard competitive map).
2. Three **lanes** (top, mid, bot) plus **jungle** (the space between lanes). **Minions** spawn and push lanes; players **farm** gold and XP from minions and fights.
3. Each player picks a **champion** (character with unique abilities) and a **role**:

   | Role (CSV code) | Typical job |
   |-----------------|-------------|
   | **top** | Bruisers, tanks — isolated side lane |
   | **jng** (jungle) | Roams the map, secures neutral objectives |
   | **mid** | Mages, assassins — map center |
   | **bot** | Ranged damage (“ADC”) |
   | **sup** (support) | Peel, heal, engage for bot lane |

4. Teams fight for **objectives** (towers, dragons, baron) to get stronger and open the map.
5. First team to destroy the enemy **Nexus** wins.

Compared to Apex: less about aim and zone pressure, more about **macro** (when to fight, push, rotate), **team composition**, and **role discipline** over one long round.

---

## 3. Esports structure (why the CSV has leagues and splits)

Pro LoL is **league-based**, like soccer divisions in different countries — not one global queue.

### Regions and top-tier leagues

Examples of **top-tier** regional leagues:

| Code | Region |
|------|--------|
| **LCK** | Korea (historically strongest) |
| **LPL** | China (large, deep talent pool) |
| **LEC** | Europe |
| **LCS** | North America |

Each region runs **splits** — sub-seasons within a calendar year (often Spring / Summer; names vary). Teams play a **regular season**, then **playoffs**, then sometimes **international** events (e.g. Worlds).

### Teams and rosters

- A **team** (org + brand, e.g. T1, Cloud9) fields a **roster** — typically **one starter per role**, sometimes substitutes.
- Players **transfer** between teams and regions. Alex noted **more roster swapping than college basketball**, which affects how stable a “pond” is across splits.

### Developmental (“academy”) leagues — **central to our Y**

Many orgs run two levels:

| Level | Example | Analogy |
|-------|---------|---------|
| **Top tier** | LCK, LPL, LEC, LCS | NBA, MLB |
| **Developmental** | LCK Challengers, LDL (China), NACL (NA), etc. | G-League, minors |

Same org brand; different competitive tier. **Advancement** in Alex’s panel = a developmental player **debuts in a top-tier league** within 1–2 years (`top_tier_debut_within_1y` / `_2y`). That is the LoL analog of **NBA draft** or **tenure**.

---

## 4. How this maps to the Big Fish / HERO frame

Each row in the panel is roughly: **one player stint** on a **team** in a **league × split**, at a **position** (`player_period_id`).

| Dissertation term | LoL / CSV |
|-------------------|-----------|
| **Unit** | Player stint in a split |
| **Pond** | That team’s roster in that split |
| **Own Â** | `own_performance_index` (composite from match stats) |
| **Peer LOO** | `teammate_mean_performance_excl_self` |
| **Environment** | `league_tier`: `developmental` \| `top` \| `other` |
| **Advancement (Y)** | `top_tier_debut_within_1y` or `_2y` |
| **Censoring** | `full_1y_followup`, `full_2y_followup` — require before treating False as failure |
| **Analysis cohort** | `eligible_developmental_cohort` — dev-to-pro story still live |

**Binding split (same as MBB / tenure):**

- **Environment** (how strong your teammates / pond are) ≠ **advancement** (whether you get promoted to top tier).
- Performance index **scores** talent; orgs **select** who moves up — score ≠ select.

### Cross-domain one-liner

| Domain | Pond | Advancement |
|--------|------|-------------|
| MBB | College team | NBA draft |
| Tenure | Department | Tenure |
| **LoL** | Dev/academy roster | Top-tier league debut |

---

## 5. Stats in the panel (why the columns look unfamiliar)

Source: **Oracle’s Elixir** — public match-level data aggregated to stint-level rates.

| Stat family | Meaning |
|-------------|---------|
| Damage / gold / CS per minute | Output and farming |
| KDA, kill participation | Fight impact |
| Vision score, wards | Map control (especially jng / sup) |
| Gold / XP / CS diff @10 / @15 | “Did you win lane early?” |
| Z-scored rates (`z_damage_per_min`, …) | Within-stint normalized versions |

**Roles differ:** a support with low damage can still be elite. The panel has team-wide LOO (`teammate_mean_performance_excl_self`) and sparser **same-role** LOO (`same_role_mean_performance_excl_self`).

---

## 6. Jargon cheat sheet (CSV-facing)

| Term | Meaning |
|------|---------|
| **Split** | Sub-season (e.g. Spring 2024) — see `year`, `split` |
| **League** | Competition code (LPL, LCK, LDL, …) — see `league` |
| **League tier** | Alex mapping: `developmental` / `top` / `other` |
| **Position** | `top` / `jng` / `mid` / `bot` / `sup` |
| **Promotion / debut** | First appearance in a top-tier league — see `first_top_tier_*` columns |

---

## 7. Limits to mention honestly

- **Roster churn** — ponds are less stable than a single MBB season.
- **Role heterogeneity** — same composite index across positions is convenient but imperfect.
- **Selection** — promotion is partly org politics and roster needs, not a pure merit sort.
- **Same-role LOO** — only ~27% populated; team LOO is the primary peer context.

---

## Related repo docs

| Doc | Path |
|-----|------|
| Column map | [`datasets/legends/README.md`](../../../../datasets/legends/README.md) |
| Active thread | [`_DISPOSABLE_legends_hero_thread.md`](_DISPOSABLE_legends_hero_thread.md) |
| All Big Fish datasets | [`../_DISPOSABLE_big_fish_datasets_assessment.md`](../_DISPOSABLE_big_fish_datasets_assessment.md) |

---

*2026-09-03 — COMPASS, for legends sandbox.*
