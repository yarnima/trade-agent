import requests
import pandas as pd
import plotly.graph_objects as go


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT"
]

INTERVAL = "1d"
LIMIT = 30

URL = "https://data-api.binance.vision/api/v3/klines"


for symbol in SYMBOLS:

    print()
    print("=" * 60)
    print(f"Downloading {symbol}...")
    print("=" * 60)

    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
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
            "ignore"
        ]
    )

    df["date"] = pd.to_datetime(
        df["open_time"],
        unit="ms"
    )

    for column in [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]:
        df[column] = pd.to_numeric(df[column])

    print(
        df[
            [
                "date",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        ].tail()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name=symbol
        )
    )

    fig.update_layout(
        title=f"{symbol} - Last {LIMIT} Days",
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )

    fig.show()