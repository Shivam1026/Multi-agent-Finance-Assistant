import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from finance_app.data_layer.yfinance_service import get_stock_history, get_ticker_info, get_stock_news
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4.1-nano")

@tool
def fetch_stock_history(ticker: str, period: str = "1mo", interval: str = "1d"):
    """
    Fetch historical stock price data for a given ticker symbol.
    """
    hist = get_stock_history(ticker, period, interval)
    # Convert to string/json for the LLM to consume
    return hist.to_json()

@tool
def fetch_ticker_info(ticker: str):
    """
    Fetch detailed information about a company (sector, industry, market cap, etc.) using its ticker symbol.
    """
    return get_ticker_info(ticker)

@tool
def fetch_stock_news(ticker: str):
    """
    Fetch the latest news articles for a given stock ticker.
    """
    return get_stock_news(ticker)

class APIAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(model=model_name, max_tokens=400)
        self.tools = [fetch_stock_history, fetch_ticker_info, fetch_stock_news]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def run(self, state: dict):
        """
        Agent logic to decide which tools to call based on the user query.
        In the LangGraph context, this will be a node.
        """
        messages = state.get("messages", [])
        # Simple invocation for now; will be integrated into LangGraph workflow
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

if __name__ == "__main__":
    # Quick test
    from langchain_core.messages import HumanMessage
    agent = APIAgent()
    state = {"messages": [HumanMessage(content="Get me the latest news and info for AAPL")]}
    result = agent.run(state)
    print(result)
