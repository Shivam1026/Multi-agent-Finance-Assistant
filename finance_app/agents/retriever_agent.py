import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from finance_app.data_layer.faiss_store import FAISSStore
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

class RetrieverAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOpenAI(model=model_name, max_tokens=400)
        self.store = FAISSStore()

    def run(self, state: dict):
        """
        Retriever node in LangGraph.
        Searches FAISS for relevant context and adds it to the state.
        """
        query = state.get("query", "")
        if not query and state.get("messages"):
            # If no explicit query, use the last human message
            query = state["messages"][-1].content
        
        relevant_docs = self.store.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Add context as a system message or metadata in state
        context_msg = SystemMessage(content=f"Context from Knowledge Base:\n{context}")
        
        # We don't want to bloat the main conversation history yet, maybe keep it in state
        return {"retrieved_context": context}

if __name__ == "__main__":
    agent = RetrieverAgent()
    state = {"query": "Tell me about electric cars"}
    result = agent.run(state)
    print(result)
