"""
Schema definitions for stock trading analysis.

This module contains Pydantic models for validating and structuring
stock trading analysis data, following the same structure as the 
crypto trading schema for consistency.
"""

from pydantic import BaseModel
from typing import List, Literal


class TradingInfo(BaseModel):
    """Information about a stock trade."""
    trading_stock: str
    trading_amount: float
    trading_time: str


class TradingTechnicalIndicator(BaseModel):
    """Technical analysis indicator data."""
    indicator_name: str
    indicator_value: str
    interval: str
    start_time: str
    end_time: str


class Tranding(BaseModel):
    """Complete stock trading analysis result."""
    trading_info: TradingInfo
    trading_technical_analysis: str
    trading_technical_indicators: List[TradingTechnicalIndicator]
    trade_decision: Literal["Good", "Bad"]
    recommendations: str

class TradingAnalysisAgentOutput:
    """Agent for performing stock trading analysis."""
    output : list[Tranding]
