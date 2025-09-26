from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os, json, glob
from typing import List, Dict, Any
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma


router = APIRouter()

CHROMA_DIR = "legal-data/chroma_db"
CONTRACT_DIR = "legal-data/contracts_chunks/"
OUTPUT_FILE = "legal-data/retrieval_output/retrieval_output.json"
TOP_K = 1
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_latest_contract_file() -> str:
    files = glob.glob(os.path.join(CONTRACT_DIR, "*.json"))
    
    if not files:
        raise FileNotFound("No Contract JSON found in contracts_chunks")
    
    return max(files, key=os.path.getmtime)


def load_contract_clauses(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    clauses = []
    for i, item in enumerate(data):
        text = item.get("section_text") or ""
        clauses.append({"index": i, "title": item.get("section_title", ""), "text": text})
    return clauses


@router.post("/retrieve_sections")
def retrieve_sections():
    CONTRACT_FILE = get_latest_contract_file()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    clauses = load_contract_clauses(CONTRACT_FILE)

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    matched_sections_set = set()
    matched_sections_list = []

    for clause in clauses:
        q_text = clause["text"].strip()
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


    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(matched_sections_list, f, ensure_ascii=False, indent=2)

    return JSONResponse({
        "status": "ok",
        "retrieved_count": len(matched_sections_list),
        "output_file": OUTPUT_FILE
    })
