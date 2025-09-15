# app/services/splitter.py
"""
Step 2: Split Moroccan Labor Code text by sections for retrieval.
"""

import os
import re
import json
from fastapi import APIRouter

RAW_TEXT_PATH = "legal-data/articles_cleaned/labor_code_clean.txt"
OUTPUT_PATH = "legal-data/articles_cleaned/sections.json"

router = APIRouter()

def load_text(file_path: str) -> str:
    """Load cleaned text from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def split_by_sections(text: str):
    """
    Split text by sections using pattern like:
    1. DÉFINITION ET NATURE DU CDI
    2. CONDITIONS DE FORMATION DU CONTRAT
    """
    # Regex pattern: number + dot + space + uppercase section title
    pattern = r"(\d+\.\s+[A-ZÉÈÀÇ]+\s+[^0-9]+)"
    parts = re.split(pattern, text)
    
    # Skip any text before the first section
    parts = parts[1:] if len(parts) > 1 else parts
    
    # Combine title + content
    sections = []
    for i in range(0, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        sections.append({
            "title": title,
            "text": content
        })
    return sections

@router.get("/split-sections")
def split_sections():
    """API endpoint to split cleaned labor code text into sections and save as JSON."""
    text = load_text(RAW_TEXT_PATH)
    sections = split_by_sections(text)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)
    
    return {"message": "Text split into sections", "sections_count": len(sections)}

if __name__ == "__main__":
    result = split_sections()
    print(result)
