from pydantic import BaseModel
from typing import List, Literal

class TradingInfo(BaseModel):
    trading_coin: str
    trading_amount: float
    trading_time: str

class TradingTechnicalIndicator(BaseModel):
    indicator_name: str
    indicator_value: str
    interval: str
    start_time: str
    end_time: str

class OutputSchema(BaseModel):
    trading_info: TradingInfo
    trading_technical_analysis: str
    trading_technical_indicators: List[TradingTechnicalIndicator]
    trade_decision: Literal["Good", "Bad"]
    recommendations: str
    