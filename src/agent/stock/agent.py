from langgraph.prebuilt import create_react_agent
from src.tools import (
    get_stock_price,
    get_stock_quote,
    search_stocks,
)
from src.config import llm, config
from .schema import TradingAnalysisAgentOutput

stock_analysis_agent = create_react_agent(
    name="stock_analysis_agent",
    model=llm,
    tools=[get_stock_price, get_stock_quote, search_stocks],
    prompt=config["STOCK_PROMPTS"]["STOCK_TECHNICAL_ANALYSIS"],
    response_format=TradingAnalysisAgentOutput,
)
