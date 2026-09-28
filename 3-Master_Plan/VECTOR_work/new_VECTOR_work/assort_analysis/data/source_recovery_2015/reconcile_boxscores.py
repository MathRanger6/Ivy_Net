"""Match six archived 2014-15 box scores to frozen rows with missing minutes.

This writes an isolated overlay; it never changes the source game file.
Only exact normalized player names, expected team, and identical points qualify.
"""

import csv
import hashlib
import re
import unicodedata
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup


HERE = Path(__file__).resolve().parent
AUDIT_DATA = HERE.parent / "ASSORT_20260925_v1_partial_stat_rows.csv"
OUTPUT = HERE / "minutes_recovery_overlay.csv"
GAMES = {
    "400588733": ("2015-01-14-northern-kentucky", {"Kennesaw St": "kennesaw-state", "N Kentucky": "northern-kentucky"}),
    "400587124": ("2014-12-31-holy-cross", {"Boston Univ": "boston-university", "Holy Cross": "holy-cross"}),
    "400595623": ("2014-12-30-new-orleans", {"New Orleans": "new-orleans"}),
    "400586911": ("2014-12-07-cleveland-state", {"W Illinois": "western-illinois", "Cleveland St": "cleveland-state"}),
    "400595585": ("2014-11-30-southeastern-louisiana", {"SE Louisiana": "southeastern-louisiana"}),
    "400586692": ("2014-11-25-southern-methodist", {"Arkansas": "arkansas", "SMU": "southern-methodist"}),
}
# Two source-name differences checked individually against team, game, and points.
SOURCE_NAME_ALIASES = {
    ("400586911", "W Illinois", "mohammedconde"): "mohamedconde",
    ("400586692", "SMU", "benemeloguii"): "benemelogu",
}


def norm(value):
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_text.casefold())


def read_source(game_id):
    stem, _ = GAMES[game_id]
    path = HERE / (stem + ".html")
    content = path.read_bytes()
    soup = BeautifulSoup(content, "html.parser")
    source = {}
    for team, slug in GAMES[game_id][1].items():
        table = soup.select_one("table#box-score-basic-" + slug)
        if table is None:
            raise ValueError(f"Missing expected table: {game_id} {team}")
        players = {}
        for tr in table.select("tbody tr"):
            name_cell = tr.select_one('[data-stat="player"]')
            minutes_cell = tr.select_one('[data-stat="mp"]')
            points_cell = tr.select_one('[data-stat="pts"]')
            if not all((name_cell, minutes_cell, points_cell)):
                continue
            name = name_cell.get_text(" ", strip=True)
            key = norm(name)
            if key in players:
                raise ValueError(f"Duplicate name in source: {game_id} {team} {name}")
            players[key] = (name, minutes_cell.get_text(strip=True), points_cell.get_text(strip=True))
        source[team] = players
    return source, hashlib.sha256(content).hexdigest(), f"https://www.sports-reference.com/cbb/boxscores/{stem}.html"


def main():
    sources = {game: read_source(game) for game in GAMES}
    out = []
    counts = Counter()
    with AUDIT_DATA.open(newline="") as handle:
        for row in csv.DictReader(handle):
            game = row["game_id"]
            team = row["team_short_display_name"]
            players, digest, url = sources[game]
            original_key = norm(row["athlete_display_name"])
            key = SOURCE_NAME_ALIASES.get((game, team, original_key), original_key)
            found = players[team].get(key)
            status = "UNRESOLVED_NAME"
            recovered = ""
            source_name = source_points = ""
            if found:
                source_name, source_minutes, source_points = found
                status = "UNRESOLVED_POINTS"
                if source_points and float(source_points) == float(row["points"]):
                    status = "UNRESOLVED_MINUTES"
                    if source_minutes and source_minutes not in {"--", "-"}:
                        try:
                            recovered = str(float(source_minutes))
                            status = "RECOVERED"
                        except ValueError:
                            pass
            counts[status] += 1
            out.append({
                **row,
                "recovery_status": status,
                "recovered_minutes": recovered,
                "source_player_name": source_name,
                "source_points": source_points,
                "source_url": url,
                "source_sha256": digest,
            })
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, out[0].keys())
        writer.writeheader()
        writer.writerows(out)
    print(dict(counts))
    for row in out:
        if row["recovery_status"] != "RECOVERED":
            print(row["game_id"], row["team_short_display_name"], row["athlete_display_name"], row["points"], row["recovery_status"], row["source_player_name"], row["source_points"])


if __name__ == "__main__":
    main()
