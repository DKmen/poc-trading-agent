from langchain_core.messages import HumanMessage
import json

from src import stock_analysis_agent

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
    messages = result["messages"]
    
    print(f"\n📊 FOUND {len(messages)} MESSAGES:")
    print("=" * 50)
    
    for i, message in enumerate(messages, 1):
        print(f"\n📝 MESSAGE {i}:")
        print("-" * 30)
        print(f"Type: {type(message).__name__}")
        
        # Print message content
        if hasattr(message, 'content'):
            content = message.content
            print("Content:")
            
            # Try to parse as JSON for better formatting
            try:
                parsed_content = json.loads(content)
                print(json.dumps(parsed_content, indent=2, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError):
                # If not JSON, print as is
                print(content)
        else:
            print("Raw message:")
            print(message)
        
        # Print other attributes if available
        if hasattr(message, 'role'):
            print(f"Role: {message.role}")
        if hasattr(message, 'name'):
            print(f"Name: {message.name}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
else:
    print("❌ No analysis result found")
    print("Result structure:", type(result))
    if result:
        print("Available keys:", list(result.keys()) if isinstance(result, dict) else "Not a dictionary")
