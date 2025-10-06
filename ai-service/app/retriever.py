"""
Retrieve relevant sections from ChromaDB based on user queries
"""

from fastapi import APIRouter, Query
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "legal-data/chroma_db"

router = APIRouter()

# Load embeddings + Chroma vector store
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

@router.get("/search")
def search(query: str = Query(..., description="User question"),
           k: int = Query(3, description="Number of results to return")):
    """
    Search the ChromaDB for relevant sections
    """
    results = vectordb.similarity_search(query, k=k)

    response = [
        {
            "title": doc.metadata.get("title", "Unknown"),
            "text": doc.page_content
        }
        for doc in results
    ]

    return {"query": query, "results": response}
