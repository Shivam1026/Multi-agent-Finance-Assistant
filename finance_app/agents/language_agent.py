import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4.1-nano")

class LanguageAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(model=model_name, max_tokens=400)

    def run(self, state: dict):
        """
        Final synthesis node.
        Combines all outputs into a final professional answer.
        """
        user_query = state.get("messages", [HumanMessage(content="")])[-1].content
        context = state.get("retrieved_context", "None")
        analysis = state.get("analysis", "No analysis performed.")
        prediction = state.get("prediction", "No prediction performed.")
        ticker_info = state.get("ticker_info", "No ticker info.")

        prompt = f"""
        You are a sophisticated Financial Assistant. 
        User Query: {user_query}

        Provide a final, comprehensive response based on the following information:
        - Ticker Info: {json.dumps(ticker_info) if ticker_info else "N/A"}
        - Analysis: {analysis}
        - Knowledge Context: {context}
        - Future Prediction Trend: {prediction}

        Structure your response with clear sections: Executive Summary, Market Data, Trends & Analysis, and Outlook.
        Always include a disclaimer that this is not financial advice.
        """
        response = self.llm.invoke([SystemMessage(content=prompt)])
        
        return {"final_response": response.content}

if __name__ == "__main__":
    agent = LanguageAgent()
    state = {
        "messages": [HumanMessage(content="Should I buy AAPL?")],
        "analysis": "AAPL is showing strong growth.",
        "prediction": "The next 5 days show a positive trend.",
        "retrieved_context": "Apple recently announced new AI features."
    }
    print(agent.run(state))
