from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os, json, time, re, logging
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .retriever_contract import get_latest_contract_file


router = APIRouter()

CONTRACT_FILE = get_latest_contract_file()
RETRIEVAL_FILE = "legal-data/retrieval_output/retrieval_output.json"
OUTPUT_FILE = "legal-data/generation_LLM/llm_issues.json"


load_dotenv(find_dotenv())
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMNAI_API_KEY")
SLEEP_BETWEEN_CALLS = float(os.getenv("SLEEP_BETWEEN_CALLS", "0.25"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "2"))

if not API_KEY:
    raise RuntimeError("GEMINI API key not found. Set GEMINI_API_KEY in your .env")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=API_KEY)

PERSONAL_PATTERNS = [
    r"\bNom\s*:", r"\bCIN\b", r"\bN[o°]?\s?:\s?[A-Z0-9-]+", r"\bAdresse\s*:",
    r"\bTéléphone\b", r"\bTél\b", r"\bMobile\b", r"\bFax\b", r"\bEmail\b", r"@\w+\.\w+",
    r"\b\d{2}[ .-]?\d{2}[ .-]?\d{2}[ .-]?\d{2}[ .-]?\d{2}\b",
    r"\bCD\d{4,}\b"
]
PERSONAL_RE = re.compile("|".join(PERSONAL_PATTERNS), flags=re.IGNORECASE)

def is_personal_info_only(text: str) -> bool:
    if not text:
        return False
    found = PERSONAL_RE.findall(text)
    if not found:
        return False
    tokens = re.findall(r"\w{2,}", text)
    if not tokens:
        return True
    if len(found) / max(1, len(tokens)) >= 0.25:
        contract_words = ["contrat", "salaire", "préavis", "période", "horaire", "heures", "congé", "maternité", "non-concurrence"]
        lower = text.lower()
        for w in contract_words:
            if w in lower:
                return False
        return True
    return False

def is_trivial_clause_text(text: str) -> bool:
    if not text:
        return True
    words = text.strip().split()
    if len(words) <= 6 and text.strip().isupper():
        header_keywords = {"EMPLOYEUR", "EMPLOYER", "SALARIÉ", "SALARIE", "CONDITIONS", "HORAIRES",
                           "RÉMUNÉRATION", "CONGÉS", "AVANTAGES", "CONDITIONS PARTICULIÈRES"}
        for w in words:
            if w.upper() in header_keywords:
                return True
        return True
    return False

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:
        pass
    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1 or last <= first:
        return None
    candidate = text[first:last+1]
    try:
        return json.loads(candidate)
    except Exception:
        for m in re.finditer(r"\{(?:.|\n)*?\}", text):
            try:
                return json.loads(m.group(0))
            except Exception:
                continue
    return None

def build_prompt_minimal_french(clause_text: str, clause_index: int) -> str:
    return f"""
Vous êtes un classificateur légal strict (français). Vous comparerez la clause à la loi du travail marocaine en interne.
RENVOYEZ SEULEMENT UN OBJET JSON ET RIEN D'AUTRE.

CLAUSE (index {clause_index}):
\"\"\"{clause_text}\"\"\"

Tâche:
- Si la clause est conforme (aucun problème), renvoyez EXACTEMENT : {{"compliant": true}}
- Si la clause pose un problème, renvoyez EXACTEMENT un objet JSON avec ces clés:
  {{"issue": "description courte du problème en français (<=120 caractères)",
    "suggestion": "courte suggestion de correction en français (<=150 caractères) ou \"\" si non fournie"}}

Ne fournissez aucune explication, aucun texte hors du JSON, et n'incluez pas la section légale.
"""

def call_llm(prompt: str) -> Optional[str]:
    last_err = None
    for attempt in range(RETRY_ATTEMPTS + 1):
        try:
            resp = llm.invoke([HumanMessage(content=prompt)])
            text = getattr(resp, "content", None) or str(resp)
            return text
        except Exception as e:
            last_err = e
            time.sleep(0.5 * (attempt + 1))
    print(f"LLM invocation failed after retries: {last_err}")
    return None

def generate_issues():
    if not os.path.exists(CONTRACT_FILE):
        return JSONResponse({"status": "error", "message": f"{CONTRACT_FILE} not found"}, status_code=404)
    if not os.path.exists(RETRIEVAL_FILE):
        return JSONResponse({"status": "error", "message": f"{RETRIEVAL_FILE} not found"}, status_code=404)
    
    clauses = json.load(open(CONTRACT_FILE, "r", encoding="utf-8"))
    try:
        retrieval = json.load(open(RETRIEVAL_FILE, "r", encoding="utf-8"))
    except Exception:
        retrieval = []

    problematic: List[Dict[str, Any]] = []

    for idx, entry in enumerate(clauses):
        section_title = entry.get("section_title", "")
        section_text = entry.get("section_text", "") or entry.get("section_text", "")
        if section_title != "Clause":
            continue

        clause_text = (section_text or "").strip()
        if is_personal_info_only(clause_text):
            continue
        if is_trivial_clause_text(clause_text):
            continue

        prompt = build_prompt_minimal_french(clause_text, idx)
        raw = call_llm(prompt)
        if raw is None:
            continue
        parsed = extract_json_from_text(raw)
        if parsed is None:
            continue
        if isinstance(parsed, dict) and parsed.get("compliant") is True:
            continue

        issue = parsed.get("issue") if isinstance(parsed, dict) else None
        suggestion = parsed.get("suggestion") if isinstance(parsed, dict) else None
        if issue:
            problematic.append({
                "clause_index": idx,
                "clause_title": "Clause",
                "clause_text": clause_text,
                "issue": issue,
                "suggestion": suggestion or ""
            })
        time.sleep(SLEEP_BETWEEN_CALLS)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(problematic, f, ensure_ascii=False, indent=2)

    return JSONResponse({
        "status": "ok",
        "problematic_count": len(problematic),
        "output": problematic,
        "output_file": OUTPUT_FILE
    })