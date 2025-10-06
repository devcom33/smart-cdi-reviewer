from typing import Dict, Any
from .splitter_contract import split_contract_memory
from .retriever_contract import retrieve_sections_memory
from .Generation import generate_issues_memory

def process_contract_workflow(contract_text: str) -> Dict[str, Any]:
    """
    Main workflow orchestrator. Processes contract through pipeline:
    text -> splitter -> retriever -> generation -> result
    
    Returns same structure as old project for frontend compatibility.
    """
    # Step 1: Split contract into sections
    sections = split_contract_memory(contract_text)
    
    # Step 2: Prepare clauses for retrieval
    clauses = []
    for i, item in enumerate(sections):
        text = item.get("section_text") or ""
        clauses.append({
            "index": i,
            "title": item.get("section_title", ""),
            "text": text
        })
    
    # Step 3: Retrieve matching legal sections
    retrieval_data = retrieve_sections_memory(clauses)
    
    # Step 4: Generate issues
    problematic = generate_issues_memory(sections, retrieval_data)
    
    # Step 5: Return result in same format as old project
    return {
        "status": "ok",
        "problematic_count": len(problematic),
        "output": problematic
    }