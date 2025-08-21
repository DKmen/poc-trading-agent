from langgraph.prebuilt import create_react_agent
from src.tools import (
    get_coin_price,
)
from src.config import llm, config
from .schema import OutputSchema

trade_analysis_agent = create_react_agent(
    name="trade_analysis_agent",
    model=llm,
    tools=[get_coin_price],
    prompt=config["TRADE_ANALYSIS_PROMPT"],
    # Use the Pydantic model directly as the response_format. Passing
    # typing constructs like List[OutputSchema] causes runtime errors when
    # libraries attempt to access attributes like __name__ on the object.
    response_format=OutputSchema,
)
