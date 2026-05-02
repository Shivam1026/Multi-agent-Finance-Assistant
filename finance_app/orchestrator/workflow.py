from typing import TypedDict, List, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END

from finance_app.agents.api_agent import APIAgent
from finance_app.agents.retriever_agent import RetrieverAgent
from finance_app.agents.analysis_agent import AnalysisAgent
from finance_app.agents.prediction_agent import PredictionAgent
from finance_app.agents.language_agent import LanguageAgent
from finance_app.data_layer.yfinance_service import get_stock_history, get_ticker_info

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    retrieved_context: str
    hist_data: dict
    ticker_info: dict
    analysis: str
    prediction: str
    predicted_prices: list
    final_response: str
    ticker: str

# Initialize Agents
api_agent = APIAgent()
retriever_agent = RetrieverAgent()
analysis_agent = AnalysisAgent()
prediction_agent = PredictionAgent()
language_agent = LanguageAgent()

def api_node(state: AgentState):
    # For simplicity in this workflow, we'll extract the ticker first or assume it's provided
    # A more robust version would use the APIAgent's tool-calling capability
    ticker = state.get("ticker", "AAPL") # Default for now, should be extracted from query
    
    hist = get_stock_history(ticker, period="1mo")
    info = get_ticker_info(ticker)
    
    return {
        "hist_data": hist.to_dict(),
        "ticker_info": info,
        "ticker": ticker
    }

def retriever_node(state: AgentState):
    return retriever_agent.run(state)

def analysis_node(state: AgentState):
    return analysis_agent.run(state)

def prediction_node(state: AgentState):
    return prediction_agent.run(state)

def language_node(state: AgentState):
    return language_agent.run(state)

def create_workflow():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("data_fetcher", api_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("analyzer", analysis_node)
    workflow.add_node("predictor", prediction_node)
    workflow.add_node("synthesizer", language_node)

    # Define Edges
    workflow.set_entry_point("data_fetcher")
    
    workflow.add_edge("data_fetcher", "retriever")
    workflow.add_edge("retriever", "analyzer")
    workflow.add_edge("analyzer", "predictor")
    workflow.add_edge("predictor", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()

if __name__ == "__main__":
    app = create_workflow()
    input_state = {
        "messages": [HumanMessage(content="Analyze AAPL for me")],
        "ticker": "AAPL"
    }
    config = {"configurable": {"thread_id": "1"}}
    for output in app.stream(input_state, config):
        print(output)
