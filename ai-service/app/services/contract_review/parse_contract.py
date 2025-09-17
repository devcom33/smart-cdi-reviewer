# app/services/contract_review/parse_contract.py

import os
import re
import pdfplumber

CONTRACT_TMP_PATH = "legal-data/contracts_tmp/"
os.makedirs(CONTRACT_TMP_PATH, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF, preserve paragraph/newline structure."""
    text_lines = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                # Split page text by lines, strip each line
                lines = [line.strip() for line in page_text.split("\n")]
                text_lines.extend(lines)
                text_lines.append("")  # add empty line between pages

    # Remove emoji and extra spaces
    clean_lines = [re.sub(r"⚠", "", line) for line in text_lines]
    
    # Join lines with newline, preserving paragraph breaks
    text = "\n".join([line for line in clean_lines if line.strip()])
    return text

def parse_contract_pdf_to_txt(file_path: str):
    """Save extracted text to a .txt file preserving paragraphs."""
    text = extract_text_from_pdf(file_path)
    txt_filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
    txt_path = os.path.join(CONTRACT_TMP_PATH, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return txt_path, text


if __name__ == "__main__":
    pdf_file = "legal-data/contracts_tmp/Contrat_de_travail.pdf"
    txt_path, parsed_text = parse_contract_pdf_to_txt(pdf_file)
    print(f"✅ Contract parsed and saved to {txt_path}")
    print(f"Preview:\n{parsed_text[:500]}...")  