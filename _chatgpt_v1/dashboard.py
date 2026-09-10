from dash import Dash, Input, Output, dcc, html

from src.dashboard.charts import create_candlestick_chart
from src.dashboard.queries import (
    get_price_history,
    get_symbols,
)


app = Dash(__name__)

symbols = get_symbols()

app.layout = html.Div(
    [
        html.H1(
            "Trade Agent",
            style={
                "textAlign": "center"
            },
        ),

        html.Div(
            [
                html.Label("Symbol"),

                dcc.Dropdown(
                    id="symbol-dropdown",
                    options=[
                        {
                            "label": symbol,
                            "value": symbol,
                        }
                        for symbol in symbols
                    ],
                    value=symbols[0] if symbols else None,
                    clearable=False,
                ),
            ],
            style={
                "width": "300px",
                "margin": "20px auto",
            },
        ),

        dcc.Graph(
            id="candlestick-chart"
        ),
    ],
    style={
        "padding": "20px"
    },
)


@app.callback(
    Output(
        "candlestick-chart",
        "figure",
    ),
    Input(
        "symbol-dropdown",
        "value",
    ),
)
def update_chart(symbol):

    if not symbol:
        return {}

    df = get_price_history(symbol)

    if df.empty:
        return {}

    return create_candlestick_chart(
        df=df,
        symbol=symbol,
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )