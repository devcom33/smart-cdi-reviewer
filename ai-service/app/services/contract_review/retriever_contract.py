"""
Chroma Retrieval Top1 - Output only matched section content

This version returns for each clause only the section text from the Chroma DB, without extra metadata or scores, to match your desired output format.
"""

import os
import json
from typing import List, Dict, Any

CHROMA_DIR = "legal-data/chroma_db"
CONTRACT_FILE = "legal-data/contracts_chunks/contract_sections.json"
OUTPUT_FILE = "legal-data/retrieval_output/retrieval_output.json"
TOP_K = 1
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma


def load_contract_clauses(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    clauses = []
    for i, item in enumerate(data):
        text = item.get("section_text") or ""
        clauses.append({"index": i, "title": item.get("section_title", ""), "text": text})
    return clauses


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    clauses = load_contract_clauses(CONTRACT_FILE)

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    matched_sections_set = set()  # for deduplication by text
    matched_sections_list = []

    for clause in clauses:
        q_text = clause["text"].strip()
        if not q_text:
            continue

        docs = vectorstore.similarity_search(q_text, k=TOP_K)
        if not docs:
            continue

        doc_text = docs[0].page_content if hasattr(docs[0], "page_content") else str(docs[0])

        # Deduplicate by text content
        if doc_text not in matched_sections_set:
            matched_sections_set.add(doc_text)
            matched_sections_list.append({
                "title": docs[0].metadata.get("title", "") if hasattr(docs[0], "metadata") else "",
                "text": doc_text
            })

    # Save final list of unique matched sections
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(matched_sections_list, f, ensure_ascii=False, indent=2)

    print(f"Retrieved {len(matched_sections_list)} unique sections.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
