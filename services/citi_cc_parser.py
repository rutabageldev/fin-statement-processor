import pdfplumber
from typing import Dict
from io import BytesIO


def parse(file_bytes: bytes) -> Dict[str, str]:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

        return {
            "source": "CITI_CC",
            "page_count": str(len(pdf.pages)),
            "raw_text_preview": text if text else "No text found",
        }
