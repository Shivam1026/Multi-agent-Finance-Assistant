from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.messages import HumanMessage
from finance_app.orchestrator.workflow import create_workflow

app = FastAPI(title="Finance AI Agent API")

class QueryRequest(BaseModel):
    query: str
    ticker: Optional[str] = "AAPL"

class AnalysisResponse(BaseModel):
    final_response: str
    analysis: str
    prediction: str
    predicted_prices: List[float]
    ticker_info: dict

workflow_app = create_workflow()

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: QueryRequest):
    try:
        input_state = {
            "messages": [HumanMessage(content=request.query)],
            "ticker": request.ticker
        }
        
        # Run the workflow
        result = workflow_app.invoke(input_state)
        
        return AnalysisResponse(
            final_response=result.get("final_response", ""),
            analysis=result.get("analysis", ""),
            prediction=result.get("prediction", ""),
            predicted_prices=result.get("predicted_prices", []),
            ticker_info=result.get("ticker_info", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "Finance AI Agent is running."}
