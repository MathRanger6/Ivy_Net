# =============================================================================
# CELL 5: Build player–season–team panel from game-level (or sub-season) box rows
# =============================================================================
# Input: mbb_df_player_box.csv — typically one row per game appearance (or similar grain).
# Output: agg — one row per (athlete_id, season, team_id) with season totals and ppm.
#
# Rationale for groupby keys: a player could theoretically appear on two teams in one
# season (transfer); we keep team_id in the key so those are separate panel rows.

# Restrict CSV read to columns this pipeline needs (faster IO on large files).
usecols = [
    "athlete_id",
    "season",
    "team_id",
    "team_short_display_name",
    "athlete_display_name",
    "minutes",
    "points",
]
print("Loading player box (may take 1–2 min)...")
df_g = pd.read_csv(PLAYER_BOX_PATH, usecols=usecols, low_memory=False)

# Coerce IDs and numerics; bad strings → NaN then dropped.
for c in ["athlete_id", "season", "team_id", "minutes", "points"]:
    df_g[c] = pd.to_numeric(df_g[c], errors="coerce")
df_g = df_g.dropna(subset=["athlete_id", "season", "team_id"])
df_g["season"] = df_g["season"].astype(int)

# Apply configured season window (aligns with draft lookup and memo sample).
df_g = df_g[(df_g["season"] >= MIN_SEASON) & (df_g["season"] <= MAX_SEASON)]

# Aggregate to one row per player–season–team.
# - minutes/points: season sums across all games in the file for that key.
# - *_display_name: "last" = arbitrary tie-break if multiple strings appear (usually constant).
# - games: count of rows contributing (here = count of minute records).
agg = (
    df_g.groupby(["athlete_id", "season", "team_id"], as_index=False)
    .agg(
        minutes=("minutes", "sum"),
        points=("points", "sum"),
        team_short_display_name=("team_short_display_name", "last"),
        athlete_display_name=("athlete_display_name", "last"),
        games=("minutes", "count"),
    )
)

# Points per minute; guard divide-by-zero for all-zero-minute rows (should be rare after filter).
agg["ppm"] = np.where(agg["minutes"] > 0, agg["points"] / agg["minutes"], np.nan)

# Drop low-minute seasons (see MIN_MINUTES_SEASON in config cell).
agg = agg[agg["minutes"] >= MIN_MINUTES_SEASON].copy()
print("Player-season rows:", len(agg))
agg.head()