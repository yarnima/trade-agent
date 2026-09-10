import requests
import pandas as pd
import plotly.graph_objects as go


API_KEY = "demo"


# -------------------------
# Get Silver Data
# -------------------------

url = (
    "https://www.alphavantage.co/query"
    "?function=GOLD_SILVER_HISTORY"
    "&symbol=SILVER"
    "&interval=daily"
    f"&apikey={API_KEY}"
)


print("Downloading Silver data...")

response = requests.get(
    url,
    timeout=60
)

response.raise_for_status()

data = response.json()


# -------------------------
# Check API Response
# -------------------------

if "Error Message" in data:
    raise Exception(
        data["Error Message"]
    )

if "Note" in data:
    raise Exception(
        data["Note"]
    )


series = data.get("data")

if not series:
    raise Exception(
        f"No data returned:\n{data}"
    )


# -------------------------
# DataFrame
# -------------------------

df = pd.DataFrame(series)

print("\nColumns:")
print(df.columns.tolist())


# API returns:
# date
# price

df["date"] = pd.to_datetime(
    df["date"]
)

df["price"] = pd.to_numeric(
    df["price"]
)


# -------------------------
# Sort
# -------------------------

df = df.sort_values(
    "date"
).reset_index(drop=True)


# -------------------------
# Last 7 Days
# -------------------------

df = df.tail(7)


print("\n==============================")
print("Silver - Last 7 Days")
print("==============================")

print(
    df.to_string(index=False)
)


# -------------------------
# Chart
# -------------------------

fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["price"],
        mode="lines+markers",
        name="Silver XAG/USD"
    )
)


fig.update_layout(
    title="Silver XAG/USD - Last 7 Days",
    xaxis_title="Date",
    yaxis_title="USD / Troy Ounce",
    xaxis_rangeslider_visible=False,
    template="plotly_white"
)


fig.show()