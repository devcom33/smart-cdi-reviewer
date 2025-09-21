# app/services/contract_review/parse_contract.py

import os
import re
import pdfplumber
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

CONTRACT_TMP_PATH = "legal-data/contracts_tmp/"
os.makedirs(CONTRACT_TMP_PATH, exist_ok=True)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF, preserve paragraph/newline structure."""
    text_lines = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                lines = [line.strip() for line in page_text.split("\n")]
                text_lines.extend(lines)
                text_lines.append("")  # add empty line between pages

    clean_lines = [re.sub(r"⚠", "", line) for line in text_lines]
    text = "\n".join([line for line in clean_lines if line.strip()])
    return text


def parse_contract_pdf_to_txt(file_path: str):
    """Save extracted text to a .txt file preserving paragraphs."""
    text = extract_text_from_pdf(file_path)
    txt_filename = Path(file_path).stem + ".txt"
    txt_path = os.path.join(CONTRACT_TMP_PATH, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return txt_path, text


# --- FastAPI endpoints (minimal wrappers) -----------------
@router.post("/parse", summary="Upload PDF and extract text to txt file")
async def upload_and_parse_pdf(file: UploadFile = File(...)):
    """
    Upload a contract PDF. Saves file to legal-data/contracts_tmp,
    extracts text and saves a .txt file, returns paths and preview.
    """
    try:
        os.makedirs(CONTRACT_TMP_PATH, exist_ok=True)
        saved_path = os.path.join(CONTRACT_TMP_PATH, file.filename)

        # save bytes
        with open(saved_path, "wb") as out:
            content = await file.read()
            out.write(content)

        txt_path, text = parse_contract_pdf_to_txt(saved_path)
        preview = text[:1000] + ("..." if len(text) > 1000 else "")
        return {"status": "ok", "pdf_path": saved_path, "txt_path": txt_path, "preview": preview}
    except Exception as e:
        logger.exception("Failed to parse uploaded PDF")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/extract_txt", summary="Extract text from an existing PDF under legal-data/contracts_tmp")
def extract_txt_from_existing(pdf_filename: str):
    pdf_path = os.path.join(CONTRACT_TMP_PATH, pdf_filename)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    try:
        txt_path, text = parse_contract_pdf_to_txt(pdf_path)
        return {"status": "ok", "txt_path": txt_path, "length": len(text)}
    except Exception as e:
        logger.exception("Error extracting text")
        raise HTTPException(status_code=500, detail=str(e))


# keep a __main__ convenience if you want to test locally (optional)
if __name__ == "__main__":
    pdf_file = os.path.join(CONTRACT_TMP_PATH, "Contrat_de_travail.pdf")
    if os.path.exists(pdf_file):
        txt_path, parsed_text = parse_contract_pdf_to_txt(pdf_file)
        print(f" Contract parsed and saved to {txt_path}")
        print(f"Preview:\n{parsed_text[:500]}...")
    else:
        print("No sample PDF found in", CONTRACT_TMP_PATH)
