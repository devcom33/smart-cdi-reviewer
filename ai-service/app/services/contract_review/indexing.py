import os
import json
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import logging

from .parse_contract import parse_contract_pdf_to_txt, CONTRACT_TMP_PATH
from .splitter_contract import split_contract_local, CONTRACT_CHUNKS_PATH

router = APIRouter()
logger = logging.getLogger(__name__)

os.makedirs(CONTRACT_TMP_PATH, exist_ok=True)
os.makedirs(CONTRACT_CHUNKS_PATH, exist_ok=True)

def index_contract(txt):
    try:
        timestamp = int(time.time())
        filename = "contract_cdi_"
        json_filename = f"{Path(filename).stem}_{timestamp}.json"
        json_path = os.path.join(CONTRACT_CHUNKS_PATH, json_filename)
        sections = split_contract_local(txt, json_path)

        preview = txt[:1000] + ("..." if len(txt) > 1000 else "")
        return {
            "status": "ok",
            "json_path": json_path,
            "sections_count": len(sections),
            "preview": preview
        }
    except Exception as e:
        logger.exception("Failed indexing contract")
        raise HTTPException(status_code=500, detail=str(e))
