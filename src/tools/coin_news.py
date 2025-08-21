"""Utilities for fetching cryptocurrency news.

This module provides helpers to obtain news articles for a given coin and
date range. The actual implementation should call a news API (e.g. NewsAPI,
CoinDesk, CryptoPanic) and normalize the results into a list of dictionaries.
"""

from typing import List, Dict, Optional
from langchain_core.tools import tool

@tool
def get_coin_news(coin: str, start_date: str, end_date: str) -> List[Dict[str, Optional[str]]]:
    """Fetch news articles for a cryptocurrency between two dates.
    Parameters
    ----------
    coin : str
        Symbol or name of the cryptocurrency (e.g. "bitcoin" or "BTC").
    start_date : str
        Inclusive start date in ISO date format (YYYY-MM-DD).
    end_date : str
        Inclusive end date in ISO date format (YYYY-MM-DD).

    Returns
    -------
    List[Dict[str, Optional[str]]]
        A list of article objects. Each article dict should contain at least:
        - "title" (str): Article title
        - "source" (str): Source name
        - "published_at" (str): ISO 8601 timestamp
        - "url" (str): Link to the article
        - "summary" (Optional[str]): Short summary if available

    Raises
    ------
    ValueError
        If the provided dates are malformed or start_date > end_date.
    requests.RequestException
        If a network request to the news provider fails.

    Notes
    -----
    This function is currently a stub (no network calls). Implementations
    should validate dates, call the chosen news API, and map provider fields
    to the shape described above.

    Example
    -------
    >>> get_coin_news("bitcoin", "2025-01-01", "2025-01-07")
    [{"title": "BTC rallies...", "source": "CoinDesk", "published_at": "2025-01-02T12:34:00Z", "url": "https://...", "summary": "..."}]
    """
    pass
