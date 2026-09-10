import pandas as pd
import requests

from src.providers.base import MarketDataProvider


class BinanceProvider(MarketDataProvider):

    BASE_URL = (
        "https://data-api.binance.vision"
        "/api/v3/klines"
    )

    def get_history(
        self,
        provider_symbol: str,
        limit: int | None = None,
    ) -> pd.DataFrame:

        params = {
            "symbol": provider_symbol,
            "interval": "1d",
            "limit": limit or 1000,
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )

        df["date"] = pd.to_datetime(
            df["open_time"],
            unit="ms",
        ).dt.date

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(
                df[column]
            )

        df["trades"] = pd.to_numeric(
            df["trades"]
        )

        df["last"] = None
        df["value"] = None

        return df[
            [
                "date",
                "open",
                "high",
                "low",
                "close",
                "last",
                "volume",
                "value",
                "trades",
            ]
        ]