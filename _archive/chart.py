import pandas as pd
import plotly.graph_objects as go


def load_data(symbol):

    path = f"data/{symbol}.parquet"

    df = pd.read_parquet(path)

    df = df.sort_values("date")
    df = df.reset_index(drop=True)

    return df


def plot_pattern(symbol, pattern):

    df = load_data(symbol)

    start = pattern["rise_start_idx"]
    correction_end = pattern["correction_end_idx"]

    # فقط محدوده‌ای که برای Pattern لازم داریم
    df_plot = df.iloc[
        start:correction_end + 1
    ].copy()

    fig = go.Figure()

    # --------------------------------------------------
    # Candlestick
    # --------------------------------------------------

    fig.add_trace(
        go.Candlestick(
            x=df_plot["date"],

            open=df_plot["open"],
            high=df_plot["high"],
            low=df_plot["low"],
            close=df_plot["close"],

            name=symbol
        )
    )

    # --------------------------------------------------
    # 50% level
    # --------------------------------------------------

    fifty = pattern["fifty_percent"]

    fig.add_hline(
        y=fifty,
        line_dash="dash",
        annotation_text="50% Retracement",
        annotation_position="top left"
    )

    # --------------------------------------------------
    # Rise start
    # --------------------------------------------------

    rise_start_date = df.loc[
        start, "date"
    ]

    rise_low = pattern["rise_low"]

    fig.add_annotation(
        x=rise_start_date,
        y=rise_low,
        text="Rise Start",
        showarrow=True,
        arrowhead=2
    )

    # --------------------------------------------------
    # Rise high
    # --------------------------------------------------

    high_date = df.loc[
        pattern["rise_high_idx"],
        "date"
    ]

    high_price = pattern["rise_high"]

    fig.add_annotation(
        x=high_date,
        y=high_price,
        text="Rise High",
        showarrow=True,
        arrowhead=2
    )

    # --------------------------------------------------
    # Correction low
    # --------------------------------------------------

    correction_date = df.loc[
        correction_end,
        "date"
    ]

    correction_low = pattern[
        "correction_low"
    ]

    fig.add_annotation(
        x=correction_date,
        y=correction_low,
        text="Correction",
        showarrow=True,
        arrowhead=2
    )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    rise_percent = pattern["rise_percent"]
    correction_percent = pattern["correction_percent"]

    fig.update_layout(
        title=(
            f"{symbol} | "
            f"Rise: {rise_percent:.1f}% | "
            f"Correction: {correction_percent:.1f}%"
        ),

        xaxis_title="Date",
        yaxis_title="Price",

        xaxis_rangeslider_visible=False,

        template="plotly_white"
    )

    fig.show()