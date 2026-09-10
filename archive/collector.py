import os
from urllib.parse import quote

import requests
import pandas as pd


BASE_URL = "https://cdn.tsetmc.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}


def search_symbol(symbol):

    url = (
        f"{BASE_URL}/Instrument/"
        f"GetInstrumentSearch/{quote(symbol)}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("instrumentSearch", [])

    if not results:
        raise ValueError(
            f"Symbol not found: {symbol}"
        )

    # اول دنبال تطابق دقیق نماد می‌گردیم
    exact = next(
        (
            item
            for item in results
            if item.get("lVal18AFC", "").strip() == symbol
        ),
        None
    )

    item = exact if exact else results[0]

    ins_code = item.get("insCode")
    found_symbol = item.get("lVal18AFC")

    if not ins_code:
        raise ValueError(
            f"InsCode not found for {symbol}"
        )

    print(
        f"Symbol: {found_symbol}"
    )

    print(
        f"InsCode: {ins_code}"
    )

    return ins_code


def get_history(ins_code):

    url = (
        f"{BASE_URL}/ClosingPrice/"
        f"GetClosingPriceDailyList/{ins_code}/0"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(
        data["closingPriceDaily"]
    )

    # فقط ستون‌های مورد نیاز
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
            "zTotTran"
        ]
    ].copy()

    # تاریخ
    df["date"] = pd.to_datetime(
        df["dEven"].astype(str),
        format="%Y%m%d"
    )

    # تغییر نام ستون‌ها
    df = df.rename(
        columns={
            "priceFirst": "open",
            "priceMax": "high",
            "priceMin": "low",
            "pClosing": "close",
            "pDrCotVal": "last",
            "qTotTran5J": "volume",
            "qTotCap": "value",
            "zTotTran": "trades"
        }
    )

    # مرتب‌سازی
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

    df = df.sort_values(
        "date"
    ).reset_index(drop=True)

    return df


def save_history(df, filename):

    os.makedirs(
        "data",
        exist_ok=True
    )

    path = f"data/{filename}.parquet"

    df.to_parquet(
        path,
        index=False
    )

    print(
        f"Saved: {path}"
    )

    print(
        f"Rows: {len(df)}"
    )


def get_and_save(symbol, filename):

    print()
    print("=" * 60)
    print(f"Downloading {symbol}")
    print("=" * 60)

    ins_code = search_symbol(symbol)

    df = get_history(
        ins_code
    )

    save_history(
        df,
        filename
    )

    print(
        df.tail()
    )


if __name__ == "__main__":

    stocks = [
        ("فملی", "femli"),
        ("شپنا", "shepna"),
        ("وخارزم", "vakharazm"),
    ]

    for symbol, filename in stocks:

        try:

            get_and_save(
                symbol,
                filename
            )

        except Exception as e:

            print(
                f"ERROR - {symbol}: {e}"
            )