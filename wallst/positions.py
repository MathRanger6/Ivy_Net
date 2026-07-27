#!/usr/bin/env python3
"""Portfolio snapshot: fetch prices, print P/L by lot, persist holdings + history.

Holdings live in ``holdings.json`` (ticker → list of purchase lots). Each run
appends one row per lot to ``history.csv``.

Plain quote run (works from any directory; shell returns you afterward):

    wallst

Record new purchase lot(s):

    wallst buy '[("NVDA", 10, 214.05)]'
    wallst buy '[("NVDA", 10, 214.05, "2026-05-11")]'

Each buy tuple is (ticker, shares, price) or (ticker, shares, price, date).
Unknown tickers must be added to holdings.json first.
"""

from __future__ import annotations

import ast
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

HERE = Path(__file__).resolve().parent
HOLDINGS_PATH = HERE / "holdings.json"
HISTORY_PATH = HERE / "history.csv"

HISTORY_COLUMNS = [
    "quote_datetime",
    "ticker",
    "purchase_date",
    "shares",
    "cost",
    "current_price",
    "net_gain_loss",
    "ticker_net_total",
    "run_net_total",
]

Lot = dict[str, Any]
Holdings = dict[str, dict[str, list[Lot]]]


def load_holdings() -> Holdings:
    if not HOLDINGS_PATH.exists():
        raise SystemExit(f"Missing {HOLDINGS_PATH.name}")
    data = json.loads(HOLDINGS_PATH.read_text(encoding="utf-8"))
    holdings: Holdings = {}
    for ticker, payload in data.items():
        sym = str(ticker).upper()
        if "lots" in payload:
            lots = [_normalize_lot(lot) for lot in payload["lots"]]
        else:
            lots = [_normalize_lot({"shares": payload["holding"], "price": payload["cost"]})]
        holdings[sym] = {"lots": lots}
    return holdings


def _normalize_lot(raw: dict[str, Any]) -> Lot:
    lot: Lot = {"shares": float(raw["shares"]), "price": float(raw["price"])}
    if raw.get("date"):
        lot["date"] = str(raw["date"])
    return lot


def save_holdings(holdings: Holdings) -> None:
    out: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for ticker in sorted(holdings):
        lots: list[dict[str, Any]] = []
        for lot in holdings[ticker]["lots"]:
            row: dict[str, Any] = {"shares": lot["shares"], "price": lot["price"]}
            if lot.get("date"):
                row["date"] = lot["date"]
            lots.append(row)
        out[ticker] = {"lots": lots}
    HOLDINGS_PATH.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ticker_totals(lots: list[Lot]) -> tuple[float, float, float]:
    shares = sum(lot["shares"] for lot in lots)
    cost_basis = sum(lot["shares"] * lot["price"] for lot in lots)
    avg_cost = cost_basis / shares if shares else 0.0
    return shares, avg_cost, cost_basis


def parse_buy_updates(argv: list[str]) -> list[tuple[str, float, float, str | None]]:
    if not argv:
        return []
    raw = " ".join(argv).strip()
    if not raw:
        return []
    try:
        parsed = ast.literal_eval(raw)
    except (SyntaxError, ValueError) as exc:
        raise SystemExit(
            f"Could not parse buy updates: {raw!r}\n"
            'Use: wallst buy \'[("NVDA", 10, 214.05)]\'\n'
            'Or:  wallst buy \'[("NVDA", 10, 214.05, "2026-05-11")]\''
        ) from exc
    if not isinstance(parsed, (list, tuple)):
        raise SystemExit("Buy updates must be a list of (ticker, shares, price[, date]) tuples.")
    out: list[tuple[str, float, float, str | None]] = []
    for item in parsed:
        if not isinstance(item, (list, tuple)) or len(item) not in (3, 4):
            raise SystemExit(
                f"Each buy must be (ticker, shares, price) or with date; got {item!r}"
            )
        ticker, shares, price = item[0], float(item[1]), float(item[2])
        date = str(item[3]) if len(item) == 4 else None
        out.append((str(ticker).upper(), shares, price, date))
    return out


def apply_buy_updates(
    holdings: Holdings, updates: list[tuple[str, float, float, str | None]]
) -> None:
    for ticker, shares, price, date in updates:
        if ticker not in holdings:
            raise SystemExit(
                f"Unknown ticker {ticker!r} — add a lots entry to {HOLDINGS_PATH.name} first."
            )
        lot: Lot = {"shares": shares, "price": price}
        if date:
            lot["date"] = date
        holdings[ticker]["lots"].append(lot)
        date_note = f" on {date}" if date else ""
        print(f"Added {ticker} lot: {shares:g} @ ${price:g}{date_note}")


def quote_datetime_now() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def fetch_current_price(ticker: str) -> float:
    info = yf.Ticker(ticker).info
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    if price is None:
        raise SystemExit(f"No price returned for {ticker}")
    return float(price)


def lot_label(lot: Lot) -> str:
    date = lot.get("date")
    if date:
        return f"{date}: {lot['shares']:g} @ ${lot['price']:g}"
    return f"{lot['shares']:g} @ ${lot['price']:g}"


def append_history(rows: list[dict]) -> pd.DataFrame:
    new_df = pd.DataFrame(rows, columns=HISTORY_COLUMNS)
    if HISTORY_PATH.exists():
        hist = pd.read_csv(HISTORY_PATH)
        hist = pd.concat([hist, new_df], ignore_index=True)
    else:
        hist = new_df
    hist = hist.reindex(columns=HISTORY_COLUMNS)
    hist.to_csv(HISTORY_PATH, index=False)
    return hist


def run_quotes(holdings: Holdings) -> None:
    quote_datetime = quote_datetime_now()
    run_net_total = 0.0
    history_rows: list[dict] = []
    prices: dict[str, float] = {}

    for ticker in sorted(holdings):
        prices[ticker] = fetch_current_price(ticker)

    for ticker in sorted(holdings):
        lots = holdings[ticker]["lots"]
        current_price = prices[ticker]
        total_shares, avg_cost, _ = ticker_totals(lots)
        ticker_net = sum((current_price - lot["price"]) * lot["shares"] for lot in lots)
        run_net_total += ticker_net

        print(
            f"{ticker}: ${current_price:g} (avg cost ${avg_cost:.4f}, {total_shares:g} shares)"
        )

        for lot in lots:
            lot_pnl = (current_price - lot["price"]) * lot["shares"]
            lot_side = "gain" if lot_pnl >= 0 else "loss"
            print(f"       {lot_label(lot)} → ${lot_pnl:,.2f} {lot_side}")

            history_rows.append(
                {
                    "quote_datetime": quote_datetime,
                    "ticker": ticker,
                    "purchase_date": lot.get("date", ""),
                    "shares": lot["shares"],
                    "cost": lot["price"],
                    "current_price": current_price,
                    "net_gain_loss": lot_pnl,
                    "ticker_net_total": ticker_net,
                    "run_net_total": run_net_total,
                }
            )

        ticker_side = "gain" if ticker_net >= 0 else "loss"
        print(f"       Total {ticker}: ${ticker_net:,.2f} {ticker_side}\n")

    total_side = "gain" if run_net_total >= 0 else "loss"
    print(f"Portfolio net {total_side}: ${run_net_total:,.2f}\n")

    for row in history_rows:
        row["run_net_total"] = run_net_total

    append_history(history_rows)
    print(
        f"Saved {len(history_rows)} lot row(s) → {HISTORY_PATH.name} "
        f"(quote_datetime={quote_datetime})"
    )


def main() -> None:
    holdings = load_holdings()

    if len(sys.argv) >= 2 and sys.argv[1] == "buy":
        updates = parse_buy_updates(sys.argv[2:])
        if not updates:
            raise SystemExit(
                'Usage: wallst buy \'[("NVDA", 10, 214.05)]\'\n'
                '   or: wallst buy \'[("NVDA", 10, 214.05, "2026-05-11")]\''
            )
        apply_buy_updates(holdings, updates)
        save_holdings(holdings)

    run_quotes(holdings)


if __name__ == "__main__":
    main()
