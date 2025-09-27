"""
Step 1: Extract and clean Moroccan Labor Code PDF into plain text
"""

import os
import re
import pdfplumber
from fastapi import APIRouter

RAW_PATH = "legal-data/articles_raw/code_du_travail.pdf"
OUTPUT_PATH = "legal-data/articles_cleaned/labor_code_clean.txt"

router = APIRouter()

def extract_text(pdf_path: str) -> str:
    """Extract text from PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([p.extract_text() or "" for p in pdf.pages])
    return text

def clean_text(text: str) -> str:
    """Remove page numbers, hyphenation, keep section structure."""
    text = re.sub(r"Page\s+\d+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"-\n\s*", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

@router.get("/parse-pdf")
def parse_pdf():
    """Extract & clean PDF, save as plain text."""
    raw_text = extract_text(RAW_PATH)
    cleaned = clean_text(raw_text)
    print(cleaned)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(cleaned)

    return {"message": "PDF extracted & cleaned", "chars": len(cleaned)}

if __name__ == "__main__":
    print(parse_pdf())
