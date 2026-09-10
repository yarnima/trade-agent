"""
Ingest daily OHLCV data from TSETMC (Tehran Stock Exchange) and store it
using the same Parquet layout as every other collector.

Difference from binance.py: TSETMC's API has no "give me only new candles"
param — GetClosingPriceDailyList always returns the full history for an
instrument. So there's no incremental *fetch*, but the merge/save step is
still dedup-safe, so re-running this is still idempotent.
"""

from __future__ import annotations

from urllib.parse import quote

import requests
import pandas as pd

from src.ingest.storage import load_existing, merge_and_save

BASE_URL = "https://cdn.tsetmc.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}


def search_ins_code(symbol: str) -> str:
    """Resolve a TSE ticker (e.g. 'فملی') to its internal insCode."""
    url = f"{BASE_URL}/Instrument/GetInstrumentSearch/{quote(symbol)}"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    results = response.json().get("instrumentSearch", [])
    if not results:
        raise ValueError(f"Symbol not found: {symbol}")

    exact = next((r for r in results if r.get("lVal18AFC", "").strip() == symbol), None)
    item = exact or results[0]

    ins_code = item.get("insCode")
    if not ins_code:
        raise ValueError(f"insCode not found for {symbol}")

    return ins_code


def fetch_history(ins_code: str, symbol_label: str) -> pd.DataFrame:
    """Fetch full daily history for an instrument, normalized to the shared schema."""
    url = f"{BASE_URL}/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    raw = response.json().get("closingPriceDaily", [])
    if not raw:
        return pd.DataFrame(columns=["date", "symbol", "open", "high", "low", "close", "volume"])

    df = pd.DataFrame(raw)
    df["date"] = pd.to_datetime(df["dEven"].astype(str), format="%Y%m%d")
    df["symbol"] = symbol_label

    df = df.rename(columns={
        "priceFirst": "open",
        "priceMax": "high",
        "priceMin": "low",
        "pClosing": "close",
        "qTotTran5J": "volume",
    })

    return df[["date", "symbol", "open", "high", "low", "close", "volume"]].sort_values("date").reset_index(drop=True)


def ingest_symbol(symbol: str, symbol_label: str | None = None) -> pd.DataFrame:
    """
    symbol: the TSE ticker to search for, e.g. 'فملی'
    symbol_label: what to call it in storage/strategies, e.g. 'FEMLI'
                  (defaults to `symbol` if not given)
    """
    symbol_label = symbol_label or symbol

    ins_code = search_ins_code(symbol)
    print(f"{symbol} -> insCode {ins_code}")

    existing = load_existing(symbol_label)
    new_data = fetch_history(ins_code, symbol_label)

    if new_data.empty and existing.empty:
        raise ValueError(f"No data returned for {symbol}")

    combined = merge_and_save(existing, new_data, symbol_label)
    added = len(combined) - len(existing)
    print(f"{symbol_label}: +{added} new rows ({len(combined)} total)")

    return combined


def ingest_many(symbols: list[tuple[str, str]]) -> None:
    """symbols: list of (tse_ticker, storage_label) pairs."""
    for symbol, label in symbols:
        try:
            ingest_symbol(symbol, label)
        except Exception as e:
            print(f"ERROR - {symbol}: {e}")


if __name__ == "__main__":
    from ingest.config import load_symbols
    symbols = [(s["ticker"], s["label"]) for s in load_symbols()["tsetmc"]]
    ingest_many(symbols)