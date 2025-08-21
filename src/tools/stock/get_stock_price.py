import requests
import pandas as pd
from typing import Optional
from langchain_core.tools import tool

from src.config import config

@tool
def get_stock_price(
    stock_symbol: str, 
    start_date: str, 
    end_date: str, 
    function_type: str = "TIME_SERIES_DAILY", 
    interval: str = "5min",
    outputsize: str = "full",
    adjusted: bool = True,
    extended_hours: bool = True,
    month: Optional[str] = None
) -> pd.DataFrame:
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
            - 'TIME_SERIES_DAILY': Daily data (raw, as-traded)
            - 'TIME_SERIES_DAILY_ADJUSTED': Daily data with adjustments
            - 'TIME_SERIES_WEEKLY': Weekly data (raw)
            - 'TIME_SERIES_WEEKLY_ADJUSTED': Weekly data with adjustments
            - 'TIME_SERIES_MONTHLY': Monthly data (raw)
            - 'TIME_SERIES_MONTHLY_ADJUSTED': Monthly data with adjustments
            Defaults to 'TIME_SERIES_DAILY'.
        interval (str, optional): Time interval for intraday data only. 
            Valid when function_type='TIME_SERIES_INTRADAY':
            '1min', '5min', '15min', '30min', '60min'. 
            Ignored for daily/weekly/monthly data. Defaults to '5min'.
        outputsize (str, optional): 'compact' returns latest 100 data points,
            'full' returns complete historical data. Defaults to 'full'.
        adjusted (bool, optional): For intraday data, whether to return adjusted prices.
            Defaults to True.
        extended_hours (bool, optional): For intraday data, whether to include 
            pre-market and post-market hours. Defaults to True.
        month (str, optional): For intraday data, specify month in YYYY-MM format
            to get historical intraday data for that month.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing price data with columns:
            - 'Open': Opening price (float)
            - 'High': Highest price during period (float)
            - 'Low': Lowest price during period (float)
            - 'Close': Closing price (float)
            - 'Volume': Trading volume (float)
            - 'Adjusted_Close': Adjusted closing price (float, if applicable)
            - 'Dividend_Amount': Dividend amount (float, if applicable)
            - 'Split_Coefficient': Split coefficient (float, if applicable)
            
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
        >>> # Get weekly adjusted data
        >>> weekly_data = get_stock_price('AAPL', '2025-01-01', '2025-08-20', 'TIME_SERIES_WEEKLY_ADJUSTED')
        >>>
        >>> # Get historical intraday data for specific month
        >>> historical_intraday = get_stock_price('AAPL', '2024-01-01', '2024-01-31', 
        ...                                       'TIME_SERIES_INTRADAY', '1min', month='2024-01')
    
    Note:
        - Alpha Vantage has rate limits - avoid excessive requests
        - For intraday data, the interval parameter determines granularity
        - For daily/weekly/monthly data, the interval parameter is ignored
        - Intraday data is typically available for the last 30 days unless month is specified
        - Adjusted data includes split and dividend adjustments
        - Extended hours include pre-market (4:00am) and post-market (8:00pm) trading
    """
    # Build URL with appropriate parameters based on function type
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": function_type,
        "symbol": stock_symbol,
        "outputsize": outputsize,
        "apikey": config["ALPHA_VANTAGE"]  # Use the API key from config
    }
    
    # Add interval parameter only for intraday data
    if function_type == "TIME_SERIES_INTRADAY":
        params["interval"] = interval
        params["adjusted"] = "true" if adjusted else "false"
        params["extended_hours"] = "true" if extended_hours else "false"
        if month:
            params["month"] = month
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    stock_trade_data = response.json()
    
    # Check for API errors
    if "Error Message" in stock_trade_data:
        raise ValueError(f"API Error: {stock_trade_data['Error Message']}")
    
    if "Note" in stock_trade_data:
        raise ValueError(f"API Rate Limit: {stock_trade_data['Note']}")
    
    # Step 2: Parse into DataFrame
    # Get the time series key (it varies by function type)
    time_series_keys = [key for key in stock_trade_data.keys() if "Time Series" in key]
    if not time_series_keys:
        raise ValueError(f"No time series data found in API response. Available keys: {list(stock_trade_data.keys())}")
    
    time_series = stock_trade_data.get(time_series_keys[0], {})
    if not time_series:
        raise ValueError("No time series data available for the given parameters")
    
    # Parse time series data into DataFrame
    time_series_df = pd.DataFrame.from_dict(time_series, orient="index")
    
    # Handle different column naming conventions based on function type
    if "ADJUSTED" in function_type:
        # Adjusted data has additional columns
        column_mapping = {
            "1. open": "Open",
            "2. high": "High", 
            "3. low": "Low",
            "4. close": "Close",
            "5. adjusted close": "Adjusted_Close",
            "6. volume": "Volume",
            "7. dividend amount": "Dividend_Amount",
            "8. split coefficient": "Split_Coefficient"
        }
    else:
        # Standard OHLCV data
        column_mapping = {
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low", 
            "4. close": "Close",
            "5. volume": "Volume"
        }
    
    # Rename columns based on what's actually present in the data
    available_columns = {k: v for k, v in column_mapping.items() if k in time_series_df.columns}
    time_series_df = time_series_df.rename(columns=available_columns)
    
    # Convert to numeric types for all relevant columns
    numeric_columns = ["Open", "High", "Low", "Close", "Volume", "Adjusted_Close", "Dividend_Amount", "Split_Coefficient"]
    for col in numeric_columns:
        if col in time_series_df.columns:
            time_series_df[col] = pd.to_numeric(time_series_df[col], errors='coerce')
    
    time_series_df.index = pd.to_datetime(time_series_df.index)
    time_series_df = time_series_df.sort_index()
    
    # Step 3: Filter by date range
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)

    mask = (time_series_df.index >= start_datetime) & (time_series_df.index <= end_datetime)
    filtered_df = time_series_df.loc[mask]

    return filtered_df
