# app/services/contract_review/splitter_contract.py

import os
import json

CONTRACT_CHUNKS_PATH = "legal-data/contracts_chunks/"
os.makedirs(CONTRACT_CHUNKS_PATH, exist_ok=True)

def split_contract_local(input_file: str, output_file: str):
    """Split contract text into chunks based on paragraphs."""
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

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
                # Or create a default section
                sections.append({
                    "section_title": "Introduction",
                    "section_text": line
                })

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    return sections


if __name__ == "__main__":
    input_file = "legal-data/contracts_tmp/Contrat_de_travail.txt"
    output_file = os.path.join(CONTRACT_CHUNKS_PATH, "contract_sections.json")
    sections = split_contract_local(input_file, output_file)
    print(f" Contract split into {len(sections)} sections, saved to {output_file}")
    print("Sample:", sections[:3])  