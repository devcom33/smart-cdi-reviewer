"""
Step 2: Split Moroccan Labor Code text into major sections (clean version)
"""

import os
import re
import json
from fastapi import APIRouter

INPUT_PATH = "legal-data/articles_cleaned/labor_code_clean.txt"
OUTPUT_PATH = "legal-data/articles_cleaned/sections.json"

router = APIRouter()

def clean_body(text: str) -> str:
    """Remove newlines, emojis, and normalize spaces."""
    # remove emojis and special symbols like ⚠
    text = re.sub(r"[^\w\s.,;:!?()\-']", " ", text, flags=re.UNICODE)
    # replace multiple spaces/newlines with single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_by_sections(text: str):
    """Split text by numbered major sections (1., 2., 3. ...)."""
    pattern = r"(?m)^(\d+\.\s+[A-ZÉÈÀÙÂÊÎÔÛÄËÏÖÜÇ'\- ]+)"
    matches = list(re.finditer(pattern, text))

    sections = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        body = text[start:end].strip()
        body = clean_body(body)
        sections.append({"title": title, "text": body})

    return sections

@router.get("/split-sections")
def split_sections():
    """Split cleaned text into sections and save as JSON."""
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    sections = split_by_sections(raw_text)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    return {"message": "Sections extracted", "count": len(sections)}

if __name__ == "__main__":
    print(split_sections())
