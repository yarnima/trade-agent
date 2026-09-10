import plotly.graph_objects as go


def create_candlestick_chart(
    df,
    symbol: str,
):
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name=symbol,
        )
    )

    fig.update_layout(
        title=f"{symbol} - Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=700,
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40,
        ),
    )

    return fig