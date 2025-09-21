import os
import json
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import logging

# Import the parsing and splitting functions
from .parse_contract import parse_contract_pdf_to_txt, CONTRACT_TMP_PATH
from .splitter_contract import split_contract_local, CONTRACT_CHUNKS_PATH

router = APIRouter()
logger = logging.getLogger(__name__)

os.makedirs(CONTRACT_TMP_PATH, exist_ok=True)
os.makedirs(CONTRACT_CHUNKS_PATH, exist_ok=True)


@router.post("/index", summary="Upload PDF, parse text and split into JSON sections")
async def index_contract(file: UploadFile = File(...)):
    """
    Upload a contract PDF. Automatically extracts text and splits it into JSON sections.
    Returns paths and section count.
    """
    try:
        # --- Step 1: Save PDF ---
        pdf_path = os.path.join(CONTRACT_TMP_PATH, file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # --- Step 2: Parse PDF to TXT ---
        txt_path, text = parse_contract_pdf_to_txt(pdf_path)

        # --- Step 3: Split TXT to JSON ---
        # Generate unique JSON filename to avoid overwriting
        timestamp = int(time.time())
        json_filename = f"{Path(file.filename).stem}_{timestamp}.json"
        json_path = os.path.join(CONTRACT_CHUNKS_PATH, json_filename)
        sections = split_contract_local(txt_path, json_path)

        # --- Step 4: Return response ---
        preview = text[:1000] + ("..." if len(text) > 1000 else "")
        return {
            "status": "ok",
            "pdf_path": pdf_path,
            "txt_path": txt_path,
            "json_path": json_path,
            "sections_count": len(sections),
            "preview": preview
        }

    except Exception as e:
        logger.exception("Failed indexing contract")
        raise HTTPException(status_code=500, detail=str(e))


# --- Optional: local test ---
if __name__ == "__main__":
    import asyncio

    class DummyFile:
        filename = "Contrat_de_travail.pdf"
        async def read(self):
            with open(f"legal-data/contracts_tmp/{self.filename}", "rb") as f:
                return f.read()

    asyncio.run(index_contract(DummyFile()))
