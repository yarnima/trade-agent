"""
Shared storage layer: one Parquet file per symbol under
data/ohlcv/symbol=<SYMBOL>/data.parquet.

Every collector (binance.py, tsetmc.py, ...) normalizes its output to the
same schema — date, symbol, open, high, low, close, volume — and uses
these two functions to read/write. This is what lets strategies and the
scanner treat crypto and stock symbols identically.
"""

from __future__ import annotations

import os
import pandas as pd

DATA_DIR = "data/ohlcv"
SCHEMA_COLS = ["date", "symbol", "open", "high", "low", "close", "volume"]


def _parquet_path(symbol: str) -> str:
    folder = os.path.join(DATA_DIR, f"symbol={symbol}")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "data.parquet")


def load_existing(symbol: str) -> pd.DataFrame:
    path = _parquet_path(symbol)
    if os.path.exists(path):
        return pd.read_parquet(path)
    return pd.DataFrame(columns=SCHEMA_COLS)


def save(df: pd.DataFrame, symbol: str) -> str:
    path = _parquet_path(symbol)
    df.to_parquet(path, index=False)
    return path


def merge_and_save(existing: pd.DataFrame, new_data: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Combine existing + freshly fetched rows, dedup on date, persist, return the full set."""
    combined = pd.concat([existing, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset="date").sort_values("date").reset_index(drop=True)
    save(combined, symbol)
    return combined
