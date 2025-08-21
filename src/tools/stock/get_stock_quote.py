import requests
from typing import Dict, Any
from langchain_core.tools import tool

from src.config import config

@tool
def get_stock_quote(stock_symbol: str) -> Dict[str, Any]:
    """Get the latest price and volume information for a stock ticker.
    
    This function uses the Alpha Vantage GLOBAL_QUOTE endpoint to retrieve
    real-time or end-of-day quote data for a given stock symbol.
    
    Args:
        stock_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
    
    Returns:
        Dict[str, Any]: A dictionary containing quote information with keys:
            - 'symbol': Stock symbol
            - 'open': Opening price
            - 'high': Day's high price
            - 'low': Day's low price
            - 'price': Current/latest price
            - 'volume': Trading volume
            - 'latest_trading_day': Latest trading day
            - 'previous_close': Previous day's closing price
            - 'change': Price change
            - 'change_percent': Percentage change
    
    Raises:
        ValueError: If the API returns an error or no data is found.
        requests.RequestException: If the HTTP request fails.
    
    Example:
        >>> quote = get_stock_quote('AAPL')
        >>> print(f"AAPL current price: ${quote['price']}")
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": stock_symbol,
        "apikey": config["ALPHA_VANTAGE"]
    }
    
    response = requests.get("https://www.alphavantage.co/query", params=params)
    response.raise_for_status()
    data = response.json()
    
    # Check for API errors
    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")
    
    if "Note" in data:
        raise ValueError(f"API Rate Limit: {data['Note']}")
    
    # Extract quote data
    quote_key = "Global Quote"
    if quote_key not in data:
        raise ValueError(f"No quote data found. Available keys: {list(data.keys())}")
    
    quote_data = data[quote_key]
    
    # Normalize the response
    normalized_quote = {
        'symbol': quote_data.get('01. symbol', ''),
        'open': float(quote_data.get('02. open', 0)),
        'high': float(quote_data.get('03. high', 0)),
        'low': float(quote_data.get('04. low', 0)),
        'price': float(quote_data.get('05. price', 0)),
        'volume': int(quote_data.get('06. volume', 0)),
        'latest_trading_day': quote_data.get('07. latest trading day', ''),
        'previous_close': float(quote_data.get('08. previous close', 0)),
        'change': float(quote_data.get('09. change', 0)),
        'change_percent': quote_data.get('10. change percent', '0%').replace('%', '')
    }
    
    return normalized_quote
