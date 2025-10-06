import os
from typing import List, Dict, Any
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "legal-data/chroma_db"
TOP_K = 1
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def retrieve_sections_memory(clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Retrieve matching legal sections for contract clauses. Returns list in memory."""
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    matched_sections_set = set()
    matched_sections_list = []
    
    for clause in clauses:
        q_text = clause.get("text", "").strip()
        if not q_text:
            continue
        
        docs = vectorstore.similarity_search(q_text, k=TOP_K)
        if not docs:
            continue
        
        doc_text = docs[0].page_content if hasattr(docs[0], "page_content") else str(docs[0])
        
        if doc_text not in matched_sections_set:
            matched_sections_set.add(doc_text)
            matched_sections_list.append({
                "title": docs[0].metadata.get("title", "") if hasattr(docs[0], "metadata") else "",
                "text": doc_text
            })
    
    return matched_sections_list