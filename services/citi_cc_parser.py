import pdfplumber
from typing import Dict


def parse(file_bytes: bytes) -> Dict[str, str]:
    with pdfplumber.open(file_bytes) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        return {
            "source": "CITI_CC",
            "page_count": str(len(pdf.pages)),
            "raw_text_preview": text[:500] if text else "No text found",
        }
