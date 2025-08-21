import requests
from typing import Dict, Any
from langchain_core.tools import tool

from src.config import config

@tool
def get_top_gainers_losers() -> Dict[str, Any]:
    """Get the top gainers, losers, and most actively traded stocks in the US market.
    
    This function uses the Alpha Vantage TOP_GAINERS_LOSERS endpoint to retrieve
    the top 20 gainers, losers, and most active stocks.
    
    Returns:
        Dict[str, Any]: Dictionary containing three lists:
            - 'top_gainers': List of top gaining stocks
            - 'top_losers': List of top losing stocks  
            - 'most_actively_traded': List of most actively traded stocks
            
            Each stock entry contains:
                - 'ticker': Stock symbol
                - 'price': Current price
                - 'change_amount': Price change amount
                - 'change_percentage': Price change percentage
                - 'volume': Trading volume
    
    Raises:
        ValueError: If the API returns an error.
        requests.RequestException: If the HTTP request fails.
    
    Example:
        >>> market_movers = get_top_gainers_losers()
        >>> for gainer in market_movers['top_gainers'][:5]:
        ...     print(f"{gainer['ticker']}: +{gainer['change_percentage']}")
    """
    params = {
        "function": "TOP_GAINERS_LOSERS", 
        "apikey":config["ALPHA_VANTAGE"]
    }
    
    response = requests.get("https://www.alphavantage.co/query", params=params)
    response.raise_for_status()
    data = response.json()
    
    # Check for API errors
    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")
    
    if "Note" in data:
        raise ValueError(f"API Rate Limit: {data['Note']}")
    
    return data
