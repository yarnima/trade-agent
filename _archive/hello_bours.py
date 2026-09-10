import os
import requests
import pandas as pd

BASE_URL = "https://cdn.tsetmc.com/api"


def get_history(ins_code):
    url = f"{BASE_URL}/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["closingPriceDaily"])

    df["date"] = pd.to_datetime(
        df["dEven"].astype(str),
        format="%Y%m%d"
    )

    df = df.rename(columns={
        "priceFirst": "open",
        "priceMax": "high",
        "priceMin": "low",
        "pClosing": "close",
        "pDrCotVal": "last",
        "qTotTran5J": "volume",
        "qTotCap": "value",
        "zTotTran": "trades"
    })

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
            "trades"
        ]
    ]

    return df.sort_values("date").reset_index(drop=True)


def save_history(df, symbol):
    os.makedirs("data", exist_ok=True)

    path = f"data/{symbol}.parquet"

    df.to_parquet(path, index=False)

    print(f"Saved: {path}")
