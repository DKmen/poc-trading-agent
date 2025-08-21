import requests
from typing import Dict, Any
from langchain_core.tools import tool

from src.config import config

@tool 
def get_company_overview(stock_symbol: str) -> Dict[str, Any]:
    """Get comprehensive company information and financial metrics.
    
    This function uses the Alpha Vantage OVERVIEW endpoint to retrieve
    detailed company information, financial ratios, and key metrics.
    
    Args:
        stock_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    
    Returns:
        Dict[str, Any]: Dictionary containing company overview with keys including:
            - 'Symbol': Stock symbol
            - 'Name': Company name
            - 'Description': Company description
            - 'Exchange': Stock exchange
            - 'Country': Country of incorporation
            - 'Sector': Business sector
            - 'Industry': Industry classification
            - 'MarketCapitalization': Market cap
            - 'EBITDA': EBITDA
            - 'PERatio': Price-to-earnings ratio
            - 'PEGRatio': PEG ratio
            - 'BookValue': Book value per share
            - 'DividendPerShare': Annual dividend per share
            - 'DividendYield': Dividend yield
            - '52WeekHigh': 52-week high price
            - '52WeekLow': 52-week low price
            And many more financial metrics...
    
    Raises:
        ValueError: If the API returns an error or no data is found.
        requests.RequestException: If the HTTP request fails.
    
    Example:
        >>> overview = get_company_overview('AAPL')
        >>> print(f"Company: {overview['Name']}")
        >>> print(f"Sector: {overview['Sector']}")
        >>> print(f"Market Cap: ${overview['MarketCapitalization']}")
    """
    params = {
        "function": "OVERVIEW",
        "symbol": stock_symbol,
        "apikey": config["ALPHA_VANTAGE"]  # Use the API key from config
    }
    
    response = requests.get("https://www.alphavantage.co/query", params=params)
    response.raise_for_status()
    data = response.json()
    
    # Check for API errors
    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")
    
    if "Note" in data:
        raise ValueError(f"API Rate Limit: {data['Note']}")
    
    if not data or data.get('Symbol') is None:
        raise ValueError(f"No company data found for symbol: {stock_symbol}")
    
    return data
