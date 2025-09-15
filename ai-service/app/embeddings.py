# app/services/embeddings.py
import json
import os
from fastapi import APIRouter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

SECTIONS_PATH = "legal-data/articles_cleaned/sections.json"
CHROMA_DIR = "legal-data/chroma_db"

router = APIRouter()

def load_sections(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_chroma_embeddings(sections):
    documents = [
        Document(page_content=section["text"], metadata={"title": section["title"]})
        for section in sections
    ]

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vectordb

@router.get("/create-chroma")
def create_chroma_db():
    sections = load_sections(SECTIONS_PATH)
    vectordb = create_chroma_embeddings(sections)
    return {"message": "Chroma DB created", "sections_count": len(sections)}

if __name__ == "__main__":
    result = create_chroma_db()
    print(result)
