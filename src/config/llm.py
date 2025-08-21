from langchain_openai import ChatOpenAI
from .constant import config

llm = ChatOpenAI(
    model=config.get("OPENAI_MODEL_ID"),
    temperature=0.6,
    api_key=config["OPENAI_API_KEY"],
    max_tokens=10000,
)
