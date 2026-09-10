from urllib.parse import quote

import pandas as pd
import requests

from src.providers.base import MarketDataProvider


class TSETMCProvider(MarketDataProvider):

    BASE_URL = "https://cdn.tsetmc.com/api"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/139 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
    }

    def search_symbol(self, symbol: str) -> dict:
        url = (
            f"{self.BASE_URL}/Instrument/"
            f"GetInstrumentSearch/{quote(symbol)}"
        )

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("instrumentSearch", [])

        if not results:
            raise ValueError(
                f"Symbol not found: {symbol}"
            )

        exact = next(
            (
                item
                for item in results
                if item.get("lVal18AFC", "").strip() == symbol
            ),
            None,
        )

        item = exact if exact else results[0]

        ins_code = item.get("insCode")
        found_symbol = item.get("lVal18AFC")

        if not ins_code:
            raise ValueError(
                f"InsCode not found for symbol: {symbol}"
            )

        return {
            "symbol": found_symbol,
            "ins_code": ins_code,
        }

    def resolve_symbol(self, symbol: str) -> str:
        result = self.search_symbol(symbol)
        return result["ins_code"]

    def get_history(
        self,
        provider_symbol: str,
        limit: int | None = None,
    ) -> pd.DataFrame:

        url = (
            f"{self.BASE_URL}/ClosingPrice/"
            f"GetClosingPriceDailyList/{provider_symbol}/0"
        )

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()
        rows = data.get("closingPriceDaily", [])

        if not rows:
            return pd.DataFrame(
                columns=[
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
            )

        df = pd.DataFrame(rows)

        df = df[
            [
                "dEven",
                "priceFirst",
                "priceMax",
                "priceMin",
                "pClosing",
                "pDrCotVal",
                "qTotTran5J",
                "qTotCap",
                "zTotTran",
            ]
        ].copy()

        df["date"] = pd.to_datetime(
            df["dEven"].astype(str),
            format="%Y%m%d",
        )

        df = df.rename(
            columns={
                "priceFirst": "open",
                "priceMax": "high",
                "priceMin": "low",
                "pClosing": "close",
                "pDrCotVal": "last",
                "qTotTran5J": "volume",
                "qTotCap": "value",
                "zTotTran": "trades",
            }
        )

        df = df[
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

        df = df.sort_values(
            "date"
        ).reset_index(drop=True)

        if limit:
            df = df.tail(limit)

        return df