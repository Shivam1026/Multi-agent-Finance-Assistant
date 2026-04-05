import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from finance_app.models.prediction_model import PolynomialPricePredictor
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

class PredictionAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(model=model_name, max_tokens=400)
        self.predictor = PolynomialPricePredictor(degree=2)

    def run(self, state: dict):
        """
        Prediction node in LangGraph.
        """
        hist_data = state.get("hist_data")
        if not hist_data:
            return {"prediction": "No historical data to predict from."}
        
        df = pd.DataFrame.from_dict(hist_data)
        if df.empty or 'Close' not in df.columns:
            return {"prediction": "Incomplete historical data for prediction."}
        
        # Close prices as list
        prices = df['Close'].tolist()
        
        # Simple polynomial prediction for next 5 days
        future_prices = self.predictor.predict(prices, days_ahead=5)
        
        # Use LLM to describe the prediction
        prompt = f"""
        Based on historical prices, a polynomial regression model predicted the next 5 days' prices:
        {future_prices}
        
        Provide a cautious summary of this prediction, emphasizing it's only a mathematical trend and not financial advice.
        """
        response = self.llm.invoke([SystemMessage(content=prompt)])
        
        return {"prediction": response.content, "predicted_prices": future_prices}

if __name__ == "__main__":
    agent = PredictionAgent()
    state = {"hist_data": {"Close": {"0": 100, "1": 102, "2": 105, "3": 108, "4": 112}}}
    print(agent.run(state))
