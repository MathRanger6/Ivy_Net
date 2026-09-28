#!/usr/bin/env python3
"""Reconcile 2015 positive-point, zero-minute game rows to saved box scores."""

from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup


HERE = Path(__file__).resolve()
WORK = HERE.parents[1]
REPO = HERE.parents[5]
SOURCE_DIR = WORK / "data/source_recovery_2015"
AUDIT_ROWS = WORK / "data/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_zero_minutes_positive_points_stop.csv"
SCHEDULE = REPO / "datasets/mbb/mbb_df_sched.csv"
OUTPUT = SOURCE_DIR / "ASSORT_20260927_zero_minutes_recovery_overlay.csv"

# Explicit game-to-team mapping prevents a same-name/opponent-side match.
AFFECTED_TEAM_SLUG = {
    "400585679": "lafayette",
    "400585766": "texas-southern",
    "400586033": "idaho-state",
    "400586079": "montana",
    "400586746": "columbia",
    "400586813": "east-carolina",
    "400587876": "presbyterian",
    "400588686": "tennessee-tech",
    "400589084": "western-carolina",
    "400589295": "tennessee-martin",
    "400591121": "davidson",
    "400591738": "central-connecticut-state",
    "400595426": "michigan",
    "400597785": "illinois-chicago",
    "400597791": "wright-state",
    "400598621": "north-carolina-at",
    "400598635": "north-carolina-at",
    "400598804": "grambling",
    "400607369": "army",
    "400609279": "elon",
    "400785115": "delaware-state",
    "400786184": "georgia-state",
    "400787680": "louisville",
}


def normalize(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_text.casefold())


def source_for(game_id: str, schedule: dict) -> tuple[dict, str, str]:
    path = SOURCE_DIR / f"{game_id}_zero_source.html"
    content = path.read_bytes()
    soup = BeautifulSoup(content, "html.parser")
    canonical = soup.select_one('link[rel="canonical"]')
    if canonical is None:
        raise ValueError(f"Missing source URL in {path}")
    url = canonical["href"]
    date = schedule[game_id]["game_date"]
    if f"/{date}-" not in url:
        raise ValueError(f"Box-score date does not match schedule: {game_id} {url} {date}")
    tables = soup.select('table[id^="box-score-basic-"]')
    if len(tables) != 2:
        raise ValueError(f"Expected two team tables: {game_id}")
    points = sorted(int(t.select_one('tfoot [data-stat="pts"]').get_text(strip=True)) for t in tables)
    expected = sorted([int(schedule[game_id]["away_score"]), int(schedule[game_id]["home_score"])])
    if points != expected:
        raise ValueError(f"Team scores differ: {game_id} {points} {expected}")
    for table in tables:
        team_minutes = int(table.select_one('tfoot [data-stat="mp"]').get_text(strip=True))
        if team_minutes < 200 or team_minutes % 25 != 0:
            raise ValueError(f"Implausible game team-minute total: {game_id} {team_minutes}")
    table = soup.select_one("table#box-score-basic-" + AFFECTED_TEAM_SLUG[game_id])
    if table is None:
        raise ValueError(f"Affected team table missing: {game_id}")
    players = {}
    for row in table.select("tbody tr"):
        name_cell = row.select_one('[data-stat="player"]')
        minute_cell = row.select_one('[data-stat="mp"]')
        point_cell = row.select_one('[data-stat="pts"]')
        if not all((name_cell, minute_cell, point_cell)):
            continue
        name = name_cell.get_text(" ", strip=True)
        key = normalize(name)
        if key in players:
            raise ValueError(f"Duplicate source player name: {game_id} {name}")
        players[key] = (name, minute_cell.get_text(strip=True), point_cell.get_text(strip=True))
    return players, url, hashlib.sha256(content).hexdigest()


def main() -> None:
    with AUDIT_ROWS.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 37 or len({r["game_id"] for r in rows}) != 23:
        raise ValueError("Stopped-audit anomaly set differs from the observed 37 rows in 23 games")
    with SCHEDULE.open(newline="") as handle:
        schedule = {r["game_id"]: r for r in csv.DictReader(handle) if r["game_id"] in AFFECTED_TEAM_SLUG}
    if set(schedule) != set(AFFECTED_TEAM_SLUG):
        raise ValueError("A game is missing from the saved schedule")
    sources = {game: source_for(game, schedule) for game in AFFECTED_TEAM_SLUG}
    output = []
    for row in rows:
        players, url, digest = sources[row["game_id"]]
        found = players.get(normalize(row["athlete_display_name"]))
        status = "UNRESOLVED_NAME"
        source_name = source_points = source_minutes = recovered_minutes = ""
        if found:
            source_name, source_minutes, source_points = found
            status = "UNRESOLVED_POINTS"
            if source_points and float(source_points) == float(row["points"]):
                status = "UNRESOLVED_MINUTES"
                try:
                    minutes = float(source_minutes)
                    if minutes > 0:
                        recovered_minutes = str(minutes)
                        status = "RECOVERED"
                except ValueError:
                    pass
        output.append({
            **row,
            "recovery_status": status,
            "recovered_minutes": recovered_minutes,
            "source_player_name": source_name,
            "source_minutes": source_minutes,
            "source_points": source_points,
            "source_url": url,
            "source_sha256": digest,
        })
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, output[0].keys())
        writer.writeheader()
        writer.writerows(output)
    counts = {status: sum(r["recovery_status"] == status for r in output) for status in sorted({r["recovery_status"] for r in output})}
    print(counts)
    for row in output:
        if row["recovery_status"] != "RECOVERED":
            print(row["game_id"], row["athlete_display_name"], row["points"], row["recovery_status"], row["source_player_name"], row["source_minutes"], row["source_points"])


if __name__ == "__main__":
    main()
