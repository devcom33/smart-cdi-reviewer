from typing import List, Dict, Any

def split_contract_memory(txt: str) -> List[Dict[str, Any]]:
    """Split contract text into chunks based on paragraphs. Returns list in memory."""
    lines = [line.strip() for line in txt.splitlines() if line.strip()]
    sections = []
    
    for line in lines:
        if ":" in line or line.isupper():
            title = line if len(line.split()) <= 10 else "Clause"
            sections.append({
                "section_title": title,
                "section_text": line
            })
        else:
            if sections:
                sections[-1]["section_text"] += " " + line
            else:
                sections.append({
                    "section_title": "Introduction",
                    "section_text": line
                })
    
    return sections