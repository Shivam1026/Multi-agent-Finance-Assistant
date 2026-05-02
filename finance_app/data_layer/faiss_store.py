import os
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"

class FAISSStore:
    def __init__(self, index_path: str = FAISS_INDEX_PATH):
        self.embeddings = OpenAIEmbeddings()
        self.index_path = index_path
        self.vector_store: Optional[FAISS] = None
        self._load_or_create()

    def _load_or_create(self):
        if os.path.exists(self.index_path):
            self.vector_store = FAISS.load_local(
                self.index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True # Local index, trusted
            )
        else:
            # Initialize with a dummy document to create the store if it doesn't exist
            initial_doc = [Document(page_content="Initial document", metadata={"source": "system"})]
            self.vector_store = FAISS.from_documents(initial_doc, self.embeddings)
            self.save()

    def save(self):
        if self.vector_store:
            self.vector_store.save_local(self.index_path)

    def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        if self.vector_store:
            self.vector_store.add_texts(texts, metadatas=metadatas)
            self.save()

    def add_documents(self, documents: List[Document]):
        if self.vector_store:
            self.vector_store.add_documents(documents)
            self.save()

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if self.vector_store:
            return self.vector_store.similarity_search(query, k=k)
        return []

if __name__ == "__main__":
    # Test (Requires API Key)
    store = FAISSStore()
    store.add_texts(["Apple is a tech giant.", "Tesla makes electric cars."], metadatas=[{"source": "AAPL"}, {"source": "TSLA"}])
    results = store.similarity_search("Tell me about EV companies")
    for doc in results:
        print(f"Content: {doc.page_content} | Metadata: {doc.metadata}")
