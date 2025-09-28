import os
import json
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

CONTRACT_CHUNKS_PATH = "legal-data/contracts_chunks/"
os.makedirs(CONTRACT_CHUNKS_PATH, exist_ok=True)


def split_contract_local(txt: str, output_file: str):
    """Split contract text into chunks based on paragraphs."""

    lines = [line.strip() for line in txt.splitlines() if line.strip()]

    sections = []
    for line in lines:
        # If line contains ":" or is all caps, treat it as a mini-title
        if ":" in line or line.isupper():
            title = line if len(line.split()) <= 10 else "Clause"
            sections.append({
                "section_title": title,
                "section_text": line
            })
        else:
            # Append text to previous section if exists
            if sections:
                sections[-1]["section_text"] += " " + line
            else:
                sections.append({
                    "section_title": "Introduction",
                    "section_text": line
                })

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    return sections