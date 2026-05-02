# Multi-Agent Financial Assistant (Streamlit + Langgraph + FAISS + YFinance + Redis)

## Overview
Multi-agent financial system using Langgraph architecture:
- YFinance data fetching
- FAISS for retrieval (RAG)
- Redis (local) for caching
- LLM-based insights(OpenAI models)


## Architecture
Frontend(Streamlit) → FastAPI → Orchestrator → Agents → FAISS 

## 🏗️ Final Architecture (Simplified)

```
Frontend (Streamlit / API)
        │
        ▼
FastAPI Backend
        │
        ▼
Orchestrator (LangGraph)
        │
        ▼
Multi-Agent System
        │
        ├── API Agent (YFinance)
        ├── Retriever Agent (FAISS)
        ├── Analysis Agent
        ├── Prediction Agent(Polynomial regression)
        └── Language Agent
        │
        ▼
FAISS Vector Store (Primary Storage) 



## Agents
- API Agent (YFinance)
- Retriever Agent (FAISS)
- Analysis Agent
- Prediction Agent
- Language Agent

## Data Layer
- FAISS → semantic storage
- Redis → caching (TTL based)



## Project Structure
finance_app/
│
├── app.py
├── requirements.txt
│
├── api/
│   └── routes.py
│
├── agents/
│   ├── api_agent.py
│   ├── retriever_agent.py
│   ├── analysis_agent.py
│   ├── prediction_agent.py
│   └── language_agent.py
│
├── orchestrator/
│   └── workflow.py
│
├── data_layer/
│   ├── yfinance_service.py
│   └── faiss_store.py
│
├── models/
│   └── prediction_model.py
│
└── utils/
    └── helpers.py

