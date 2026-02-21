import fitz  # PyMuPDF
from typing import List, Dict

def extract_pdf_text_by_page(pdf_bytes: bytes) -> List[Dict]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append({"page": i, "text": text})
    return pages