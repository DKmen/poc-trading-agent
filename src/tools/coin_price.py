"""Minimal crypto OHLCV fetcher tool.

Retrieves compact OHLCV series from Binance klines. Output is bounded and
downsampled to keep LLM context small.
"""

from typing import List, Dict, Optional, Any
from langchain_core.tools import tool
import datetime
import requests
from math import ceil

@tool
def get_coin_price(coin: str, start_date: str, end_date: str, interval: str = "1d") -> List[Dict[str, Optional[Any]]]:
    """Return compact OHLCV for a coin between two dates at an interval.

    Inputs: coin (e.g., BTC or BTCUSDT), start_date, end_date (YYYY-MM-DD),
    interval in {1m,5m,1h,1d}. Output is downsampled to <=250 points.
    """
    # Validate inputs
    try:
        start_dt = datetime.datetime.fromisoformat(start_date)
        end_dt = datetime.datetime.fromisoformat(end_date)
    except Exception as ex:
        raise ValueError(f"Invalid date(s): {ex}")
    if start_dt > end_dt:
        raise ValueError("start_date cannot be after end_date")

    # Normalize symbol (default to USDT if no quote)
    symbol = coin.upper()
    if len(symbol) <= 5 and not symbol.endswith(("USDT", "USD", "USDC", "BUSD")):
        symbol = f"{symbol}USDT"

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": int(start_dt.timestamp() * 1000),
        "endTime": int(end_dt.timestamp() * 1000),
        "limit": 750,  # cap results
    }

    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    klines = resp.json()

    series: List[Dict[str, Optional[Any]]] = [
        {
            "timestamp": datetime.datetime.fromtimestamp(k[0] / 1000).isoformat(),
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
        }
        for k in klines
    ]

    # Downsample to reduce token usage
    MAX_POINTS = 500
    n = len(series)
    if n > MAX_POINTS:
        stride = ceil(n / MAX_POINTS)
        series = series[::stride]
        # ensure last point included
        if klines:
            last = klines[-1]
            last_ts = datetime.datetime.fromtimestamp(last[0] / 1000).isoformat()
            if series[-1]["timestamp"] != last_ts:
                series[-1] = {
                    "timestamp": last_ts,
                    "open": float(last[1]),
                    "high": float(last[2]),
                    "low": float(last[3]),
                    "close": float(last[4]),
                    "volume": float(last[5]),
                }

    return series
