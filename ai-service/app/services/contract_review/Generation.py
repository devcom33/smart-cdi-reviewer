#!/usr/bin/env python3
"""
generation.py — filter headings & personal-info, call Gemini per clause, produce minimal JSON output.

Behavior:
- Only process entries where section_title == "Clause".
- Skip personal-info-only clauses (Nom, CIN, Téléphone, Adresse, email, etc.).
- Use LangChain wrapper ChatGoogleGenerativeAI (gemini-1.5-flash) to detect issues.
- LLM must return JSON-only; issues and suggestions MUST be in French.
- Output: legal-data/generation_LLM/llm_issues.json
"""

import os
import json
import time
import re
import logging
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv, find_dotenv
from difflib import SequenceMatcher

# quiet noisy libs
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
logging.getLogger("absl").setLevel(logging.ERROR)

# load env
load_dotenv(find_dotenv())

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# --- CONFIG ---
CONTRACT_FILE = "legal-data/contracts_chunks/contract_sections.json"
RETRIEVAL_FILE = "legal-data/retrieval_output/retrieval_output.json"
OUTPUT_FILE = "legal-data/generation_LLM/llm_issues.json"
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMNAI_API_KEY")
SLEEP_BETWEEN_CALLS = float(os.getenv("SLEEP_BETWEEN_CALLS", "0.25"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "2"))
# -----------------

if not API_KEY:
    raise RuntimeError("GEMINI API key not found. Set GEMINI_API_KEY in your .env")

# initialize LLM wrapper
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=API_KEY)


# ----------------- Helpers & Filters -----------------
PERSONAL_PATTERNS = [
    r"\bNom\s*:", r"\bCIN\b", r"\bN[o°]?\s?:\s?[A-Z0-9-]+", r"\bAdresse\s*:",
    r"\bTéléphone\b", r"\bTél\b", r"\bMobile\b", r"\bFax\b", r"\bEmail\b", r"@\w+\.\w+",
    r"\b\d{2}[ .-]?\d{2}[ .-]?\d{2}[ .-]?\d{2}[ .-]?\d{2}\b",  # french-like phone 05 12 34 56 78
    r"\bCD\d{4,}\b"  # example CIN pattern like CD789012
]
PERSONAL_RE = re.compile("|".join(PERSONAL_PATTERNS), flags=re.IGNORECASE)


def is_personal_info_only(text: str) -> bool:
    """
    Return True if the text appears to be only identifying information (name/CIN/address/phone/email).
    Heuristic: if it matches personal info patterns and has few other tokens.
    """
    if not text:
        return False
    # if many personal tokens present -> treat as personal info
    found = PERSONAL_RE.findall(text)
    if not found:
        return False
    # if text length small or proportion of personal tokens high -> consider personal-only
    tokens = re.findall(r"\w{2,}", text)
    if not tokens:
        return True
    # proportion heuristic
    if len(found) / max(1, len(tokens)) >= 0.25:
        # also check that text doesn't contain contract words like "contrat", "heure", "salaire", "préavis"
        contract_words = ["contrat", "salaire", "préavis", "période", "horaire", "heures", "congé", "maternité", "non-concurrence"]
        lower = text.lower()
        for w in contract_words:
            if w in lower:
                return False
        return True
    return False


def is_trivial_clause_text(text: str) -> bool:
    """
    Skip trivial short uppercase headings that may have been mis-labelled as Clause.
    E.g. 'HORAIRES ET RÉMUNÉRATION' or 'EMPLOYEUR' as clause_text (should be a header).
    We already ensure section_title == 'Clause' to process only actual clauses, but this is extra safety.
    """
    if not text:
        return True
    # if the text is short (<=5 words) and is uppercase or matches known header patterns
    words = text.strip().split()
    if len(words) <= 6 and text.strip().isupper():
        # common header words that are not real clauses
        header_keywords = {"EMPLOYEUR", "EMPLOYER", "SALARIÉ", "SALARIE", "CONDITIONS", "HORAIRES", "RÉMUNÉRATION", "CONGÉS", "AVANTAGES", "CONDITIONS", "CONDITIONS PARTICULIÈRES"}
        for w in words:
            if w.upper() in header_keywords:
                return True
        # if no header keywords but still all caps and very short, skip
        return True
    return False


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Try to extract a JSON object from model text output (best-effort)."""
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
    """
    Minimal strict French prompt — ask for JSON-only.
    Output must be either {"compliant": true} OR {"issue": "...", "suggestion":"..."} (both in French).
    """
    esc = lambda s: s.replace('"', '\\"').replace("\n", " ").strip()
    return f"""
Vous êtes un classificateur légal strict (français). Vous comparerez la clause à la loi du travail marocaine en interne.
RENVOYEZ SEULEMENT UN OBJET JSON ET RIEN D'AUTRE.

CLAUSE (index {clause_index}):
\"\"\"{clause_text}\"\"\"

Tâche:
- Si la clause est conforme (aucun problème), renvoyez EXACTEMENT : {{"compliant": true}}
- Si la clause pose un problème, renvoyez EXACTEMENT un objet JSON avec ces clés:
  {{
    "issue": "description courte du problème en français (<=120 caractères)",
    "suggestion": "courte suggestion de correction en français (<=150 caractères) ou \"\" si non fournie"
  }}

Ne fournissez aucune explication, aucun texte hors du JSON, et n'incluez pas la section légale.
"""
# ----------------- End helpers -----------------


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


# ----------------- Main -----------------
def main():
    # load inputs
    if not os.path.exists(CONTRACT_FILE):
        print(f"Contract file not found: {CONTRACT_FILE}")
        return
    if not os.path.exists(RETRIEVAL_FILE):
        print(f"Retrieval file not found: {RETRIEVAL_FILE}")
        return

    clauses = []
    try:
        clauses = json.load(open(CONTRACT_FILE, "r", encoding="utf-8"))
    except Exception as e:
        print("Failed to load contract file:", e)
        return

    # retrieval file isn't strictly required for output; we keep it for internal matching if needed
    try:
        retrieval = json.load(open(RETRIEVAL_FILE, "r", encoding="utf-8"))
    except Exception:
        retrieval = []

    problematic: List[Dict[str, Any]] = []

    for idx, entry in enumerate(clauses):
        section_title = entry.get("section_title", "")
        section_text = entry.get("section_text", "") or entry.get("section_text", "")
        # process only entries that were parsed as actual clauses
        if section_title != "Clause":
            # skip headings / titles / "EMPLOYEUR" "SALARIÉ" etc.
            continue

        clause_text = (section_text or "").strip()
        clause_title = entry.get("section_title", "Clause")  # will be "Clause"

        # skip purely personal info (Nom, CIN, Adresse, Téléphone, Email)
        if is_personal_info_only(clause_text):
            # skip — not a contractual rule to check
            continue

        # skip trivial heading-like clause_text that are uppercase short strings
        if is_trivial_clause_text(clause_text):
            continue

        # build prompt and call LLM
        prompt = build_prompt_minimal_french(clause_text, idx)
        raw = call_llm(prompt)
        if raw is None:
            print(f"No LLM response for clause index {idx}")
            time.sleep(SLEEP_BETWEEN_CALLS)
            continue

        parsed = extract_json_from_text(raw)
        if parsed is None:
            print(f"Could not parse JSON from LLM for clause {idx}. Raw output:\n{raw}\n---")
            time.sleep(SLEEP_BETWEEN_CALLS)
            continue

        # if compliant true -> skip
        if isinstance(parsed, dict) and parsed.get("compliant") is True:
            continue

        # if parsed contains issue -> record minimal fields only
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

    save_path = OUTPUT_FILE
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(problematic, f, ensure_ascii=False, indent=2)

    print(f"Done. {len(problematic)} problematic clauses saved to: {save_path}")


if __name__ == "__main__":
    main()
