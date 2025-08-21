import requests
import pandas as pd
from langchain_core.tools import tool

from src.config import config

@tool
def search_stocks(keywords: str) -> pd.DataFrame:
    """Search for stock symbols and company information using keywords.
    
    This function uses the Alpha Vantage SYMBOL_SEARCH endpoint to find
    stock symbols, company names, and market information based on search keywords.
    
    Args:
        keywords (str): Search keywords (e.g., company name, ticker symbol).
    
    Returns:
        pd.DataFrame: DataFrame containing search results with columns:
            - 'symbol': Stock symbol
            - 'name': Company name
            - 'type': Security type (e.g., Equity, ETF)
            - 'region': Trading region/country
            - 'market_open': Market open time
            - 'market_close': Market close time
            - 'timezone': Market timezone
            - 'currency': Trading currency
            - 'match_score': Relevance score (0-1)
    
    Raises:
        ValueError: If the API returns an error or no results are found.
        requests.RequestException: If the HTTP request fails.
    
    Example:
        >>> results = search_stocks('Apple')
        >>> print(results[['symbol', 'name', 'match_score']].head())
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
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
    
    # Extract search results
    if "bestMatches" not in data:
        raise ValueError(f"No search results found. Available keys: {list(data.keys())}")
    
    results = data["bestMatches"]
    if not results:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Normalize column names
    column_mapping = {
        "1. symbol": "symbol",
        "2. name": "name", 
        "3. type": "type",
        "4. region": "region",
        "5. marketOpen": "market_open",
        "6. marketClose": "market_close",
        "7. timezone": "timezone",
        "8. currency": "currency",
        "9. matchScore": "match_score"
    }
    
    df = df.rename(columns=column_mapping)
    
    # Convert match score to float
    if 'match_score' in df.columns:
        df['match_score'] = pd.to_numeric(df['match_score'], errors='coerce')
    
    return df
