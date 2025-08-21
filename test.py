import requests
import pandas as pd

from src import config

API_KEY = config["ALPHA_VANTAGE"]
symbol = "AAPL"
interval = "5min"

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
      f"&symbol={symbol}&interval={interval}&outputsize=full&apikey={API_KEY}"

response = requests.get(url)
data = response.json()


# Extract time series
time_series = data.get("Time Series (5min)", {})

# Convert to DataFrame
df = pd.DataFrame.from_dict(time_series, orient="index")
df = df.rename(columns={
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume"
})

# Convert index to datetime
df.index = pd.to_datetime(df.index)

# Sort ascending (oldest first)
df = df.sort_index()

print(df)