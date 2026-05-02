# Development Plan: Multi-Agent Financial Assistant

This plan outlines the implementation of the Multi-Agent Financial Assistant as described in `finance_app_architecture.md`. The system uses a multi-agent architecture with LangGraph, FastAPI for the backend, Streamlit for the frontend, and FAISS/Redis for the data layer.

## 1. Project Initialization & Infrastructure Setup
- [x] Create the project directory structure as specified.
- [x] Initialize `requirements.txt` with necessary libraries:
    - `streamlit`, `fastapi`, `uvicorn`, `langgraph`, `langchain`, `langchain-openai`, `faiss-cpu`, `yfinance`, `redis`, `pandas`, `numpy`, `scikit-learn`, `python-dotenv`.
- [x] Set up a `.env` file for `OPENAI_API_KEY` and other configurations.
- [x] Ensure a local Redis instance is accessible (standard port 6379).

## 2. Data Layer Implementation
- [x] **YFinance Service (`data_layer/yfinance_service.py`):**
    - Implement functions to fetch historical stock prices, company info, and news.
- [x] **Redis Cache (`utils/helpers.py` or `data_layer/`):**
    - Implement caching logic for YFinance calls to minimize API hits and latency.
- [x] **FAISS Store (`data_layer/faiss_store.py`):**
    - Setup FAISS vector store for semantic search/retrieval of financial reports or news.

## 3. Core Agents Development (`agents/`)
- [x] **API Agent (`api_agent.py`):** Uses LangChain tools to fetch data via `yfinance_service.py`.
- [x] **Retriever Agent (`retriever_agent.py`):** Queries the FAISS vector store for relevant context.
- [x] **Analysis Agent (`analysis_agent.py`):** Processes fetched data to generate financial insights (ratios, trends).
- [x] **Prediction Agent (`prediction_agent.py` & `models/prediction_model.py`):**
    - Implement a simple polynomial regression model for short-term price trend prediction.
- [x] **Language Agent (`language_agent.py`):** Formats the final response for the user, ensuring a conversational and professional tone.

## 4. LangGraph Orchestrator (`orchestrator/workflow.py`)
- [x] Define the `State` object for the graph.
- [x] Create nodes for each agent.
- [x] Define the workflow graph:
    - Entry point -> API/Retriever Agents -> Analysis Agent -> Prediction Agent -> Language Agent.
    - Implement conditional edges if needed (e.g., if data is missing, retry or exit).

## 5. Backend Development (`api/routes.py`)
- [x] Create a FastAPI application.
- [x] Implement a POST endpoint `/chat` or `/analyze` that:
    - Accepts user queries.
    - Invokes the LangGraph orchestrator.
    - Returns the final agent response.

## 6. Frontend Development (`app.py`)
- [x] Build a Streamlit UI:
    - Chat interface for user queries.
    - Sidebar for configuration (e.g., ticker selection, date ranges).
    - Visualizations for stock prices and predicted trends using Plotly or Matplotlib.

## 7. Verification & Testing
- [ ] **Unit Tests:** Verify individual services (YFinance, Redis, FAISS).
- [ ] **Agent Tests:** Ensure agents correctly call tools and process data.
- [ ] **Integration Tests:** End-to-end test from Streamlit query to LLM response.
- [ ] **Performance:** Check Redis caching effectiveness and FAISS retrieval speed.

## Migration & Rollback
- Since this is a new project, migration isn't applicable. 
- Rollback strategy: Standard Git branching and versioning.
