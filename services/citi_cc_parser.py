import pdfplumber
from typing import Dict, List
from io import BytesIO
import logging

# Suppress noisy logs from pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def parse(file_bytes: bytes) -> Dict[str, str | List[str]]:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        statement_lines: List[str] = []

        for page in pdf.pages:
            raw_text = page.extract_text()
            if raw_text:
                raw_lines = raw_text.splitlines()
                cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
                statement_lines.extend(cleaned_lines)

        return {
            "source": "CITI_CC",
            "page_count": str(len(pdf.pages)),
            "statement_lines": statement_lines,
        }


def extract_account_summary(statement_lines: List[str]) -> Dict[str, str]:
    return {"Let me": "commit please"}
