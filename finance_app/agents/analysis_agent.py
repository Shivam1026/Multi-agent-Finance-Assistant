import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
import json
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

class AnalysisAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(model=model_name, max_tokens=400)

    def run(self, state: dict):
        """
        Analyze numerical data from API results.
        Expects historical data to be in state.
        """
        # Historical data is usually stored as a dict/json in the state after API agent runs
        hist_data = state.get("hist_data")
        if not hist_data:
            return {"analysis": "No historical data provided for analysis."}
        
        df = pd.DataFrame.from_dict(hist_data)
        if df.empty:
            return {"analysis": "Historical data is empty."}
        
        # Perform simple calculations
        metrics = {
            "avg_close": df['Close'].mean(),
            "max_close": df['Close'].max(),
            "min_close": df['Close'].min(),
            "volatility": df['Close'].std(),
            "trend": "up" if df['Close'].iloc[-1] > df['Close'].iloc[0] else "down"
        }
        
        # Use LLM to provide a narrative analysis
        prompt = f"""
        Analyze the following stock metrics and provide a brief summary of the trend:
        {json.dumps(metrics, indent=2)}
        """
        response = self.llm.invoke([SystemMessage(content=prompt)])
        
        return {"analysis": response.content, "metrics": metrics}

if __name__ == "__main__":
    # Test
    agent = AnalysisAgent()
    state = {"hist_data": {"Close": {"0": 150, "1": 155, "2": 160}}}
    print(agent.run(state))
