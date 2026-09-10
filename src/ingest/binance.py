"""
Ingest OHLCV kline data from Binance's public REST API and store it as
one Parquet file per symbol under data/ohlcv/symbol=<SYMBOL>/data.parquet.

Design:
- Incremental: on each run, only fetch candles newer than what's on disk.
- Idempotent: re-running never duplicates rows (dedup on date).
- No DB server needed: Parquet files ARE the storage layer; DuckDB
  queries them directly (see store/db.py).
"""

from __future__ import annotations

import os
import requests
import pandas as pd

BASE_URL = "https://data-api.binance.vision/api/v3/klines"
DATA_DIR = "data/ohlcv"

RAW_COLUMNS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "trades",
    "taker_buy_base", "taker_buy_quote", "ignore",
]

NUMERIC_COLS = ["open", "high", "low", "close", "volume"]


def fetch_klines(
    symbol: str,
    interval: str = "1d",
    limit: int = 1000,
    start_time: int | None = None,
) -> pd.DataFrame:
    """Fetch raw klines from Binance and return a clean OHLCV DataFrame."""
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    if start_time is not None:
        params["startTime"] = start_time

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    raw = response.json()

    if not raw:
        return pd.DataFrame(columns=["date", "symbol", *NUMERIC_COLS])

    df = pd.DataFrame(raw, columns=RAW_COLUMNS)
    df["date"] = pd.to_datetime(df["open_time"], unit="ms")
    df["symbol"] = symbol

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col])

    return df[["date", "symbol", *NUMERIC_COLS]]


def _parquet_path(symbol: str) -> str:
    folder = os.path.join(DATA_DIR, f"symbol={symbol}")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "data.parquet")


def load_existing(symbol: str) -> pd.DataFrame:
    path = _parquet_path(symbol)
    if os.path.exists(path):
        return pd.read_parquet(path)
    return pd.DataFrame(columns=["date", "symbol", *NUMERIC_COLS])


def save(df: pd.DataFrame, symbol: str) -> str:
    path = _parquet_path(symbol)
    df.to_parquet(path, index=False)
    return path


def ingest_symbol(symbol: str, interval: str = "1d", limit: int = 1000) -> pd.DataFrame:
    """Fetch only new candles for a symbol and merge with what's already stored."""
    existing = load_existing(symbol)

    start_time = None
    if not existing.empty:
        last_date = existing["date"].max()
        # +1ms so we don't re-fetch the last stored candle
        start_time = int(last_date.timestamp() * 1000) + 1

    new_data = fetch_klines(symbol, interval=interval, limit=limit, start_time=start_time)

    if new_data.empty and existing.empty:
        raise ValueError(f"No data returned for {symbol}")

    combined = pd.concat([existing, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset="date").sort_values("date").reset_index(drop=True)

    path = save(combined, symbol)
    added = len(combined) - len(existing)
    print(f"{symbol}: +{added} new rows -> {path} ({len(combined)} total)")

    return combined


def ingest_many(symbols: list[str], interval: str = "1d", limit: int = 1000) -> None:
    for symbol in symbols:
        try:
            ingest_symbol(symbol, interval=interval, limit=limit)
        except Exception as e:
            print(f"ERROR - {symbol}: {e}")



if __name__ == "__main__":
    from ingest.config import load_symbols
    symbols = load_symbols()["binance"]
    ingest_many(symbols, interval="1d", limit=1000)