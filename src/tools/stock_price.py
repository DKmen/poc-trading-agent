import requests
import pandas as pd
from langchain_core.tools import tool

from src.config import config

@tool
def get_stock_price(stock_symbol: str, start_date: str, end_date: str, function_type: str = "TIME_SERIES_DAILY", interval: str = "5min") -> pd.DataFrame:
    """Retrieve stock price data from Alpha Vantage API with flexible time frames.
    
    Fetches OHLCV (Open, High, Low, Close, Volume) time series data for a given
    stock symbol within the specified date range. Supports multiple time frames
    from intraday to monthly data based on the function_type parameter.
    
    Args:
        stock_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
        start_date (str): Start date in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format.
        end_date (str): End date in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format.
        function_type (str, optional): Alpha Vantage API function type. Options:
            - 'TIME_SERIES_INTRADAY': Intraday data (requires interval parameter)
            - 'TIME_SERIES_DAILY': Daily data (interval ignored)
            - 'TIME_SERIES_WEEKLY': Weekly data (interval ignored)
            - 'TIME_SERIES_MONTHLY': Monthly data (interval ignored)
            Defaults to 'TIME_SERIES_DAILY'.
        interval (str, optional): Time interval for intraday data only. 
            Valid when function_type='TIME_SERIES_INTRADAY':
            '1min', '5min', '15min', '30min', '60min'. 
            Ignored for daily/weekly/monthly data. Defaults to '5min'.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing price data with columns:
            - 'Open': Opening price (float)
            - 'High': Highest price during period (float)
            - 'Low': Lowest price during period (float)
            - 'Close': Closing price (float)
            - 'Volume': Trading volume (float)
            
            Index is datetime, sorted chronologically from oldest to newest.
            Data is filtered to the specified date range.
    
    Raises:
        ValueError: If the API key is missing, symbol is invalid, or API returns an error.
        requests.RequestException: If the HTTP request to Alpha Vantage fails.
    
    Examples:
        >>> # Get daily data
        >>> daily_data = get_stock_price('AAPL', '2025-08-01', '2025-08-20', 'TIME_SERIES_DAILY')
        >>> 
        >>> # Get 5-minute intraday data
        >>> intraday_data = get_stock_price('AAPL', '2025-08-19', '2025-08-20', 'TIME_SERIES_INTRADAY', '5min')
        >>> 
        >>> # Get weekly data
        >>> weekly_data = get_stock_price('AAPL', '2025-01-01', '2025-08-20', 'TIME_SERIES_WEEKLY')
    
    Note:
        - Requires a valid ALPHA_VANTAGE API key in the configuration
        - Alpha Vantage has rate limits - avoid excessive requests
        - For intraday data, the interval parameter determines granularity
        - For daily/weekly/monthly data, the interval parameter is ignored
        - Intraday data is typically available for the last 30 days only
    """
    stock_url = f"https://www.alphavantage.co/query?function={function_type}" \
      f"&symbol={stock_symbol}&interval={interval}&outputsize=full&apikey={config['ALPHA_VANTAGE']}"
    pass

    response = requests.get(stock_url)
    stock_trade_data = response.json()
    
    # Step 2: Parse into DataFrame
    time_series = stock_trade_data.get(list(stock_trade_data.keys())[1], {})
    time_series_df = pd.DataFrame.from_dict(time_series, orient="index")
    time_series_df = time_series_df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    time_series_df.index = pd.to_datetime(time_series_df.index)
    time_series_df = time_series_df.sort_index()

    # Step 3: Filter by date range
    mask = (time_series_df.index >= start_date) & (time_series_df.index <= end_date)
    filtered_df = time_series_df.loc[mask]

    return filtered_df
