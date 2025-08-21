from langchain_core.messages import HumanMessage
import json

from src import stock_analysis_agent

# # invoke the trade analysis agent with user trade details
# user_trade_details = {
#     "trading_coin": "BTC",
#     "trading_amount": 0.6,
#     "trading_time": "20th December 2024, 13:25"
# }

# result = trade_analysis_agent.invoke({"messages": [HumanMessage(content=f"Analyze the trade details: {user_trade_details}")],})
# print(result["messages"][-1])

# invoke the stock analysis agent with user trade details
user_trade_details = {
    "trading_stock": "AAPL",
    "trading_amount": "500 $",
    "trading_time": "9th April 2025, 19:00",
    "trade_type": "buy"
}

result = stock_analysis_agent.invoke({"messages": [HumanMessage(content=f"Analyze the trade details: {user_trade_details}")],})

# Print the result properly
print("=" * 80)
print("STOCK TRADING ANALYSIS RESULT")
print("=" * 80)

if result and "messages" in result and result["messages"]:
    analysis_result = result["messages"][-1]
    
    # Print the content if it's a message object
    if hasattr(analysis_result, 'content'):
        content = analysis_result.content
        print("\n📊 ANALYSIS OUTPUT:")
        print("-" * 50)
        
        # Try to parse as JSON for better formatting
        try:
            parsed_content = json.loads(content)
            print(json.dumps(parsed_content, indent=2, ensure_ascii=False))
        except (json.JSONDecodeError, TypeError):
            # If not JSON, print as is
            print(content)
    else:
        print("\n📊 ANALYSIS OUTPUT:")
        print("-" * 50)
        print(analysis_result)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
else:
    print("❌ No analysis result found")
    print("Result structure:", type(result))
    if result:
        print("Available keys:", list(result.keys()) if isinstance(result, dict) else "Not a dictionary")
