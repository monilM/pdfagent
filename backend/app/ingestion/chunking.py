from typing import List, Dict
import re
import hashlib

def simple_chunk(text: str, max_chars=2200, overlap=250):
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk)
        start = max(0, end - overlap)
        if end == len(text):
            break
    return chunks

def chunk_pages(pages: List[Dict], doc_id: str, doc_title: str) -> List[Dict]:
    out = []
    idx = 0
    for p in pages:
        page_num = p["page"]
        text = p["text"] or ""
        for c in simple_chunk(text):
            idx += 1
            chunk_id = f"{doc_id}-p{page_num}-{idx}"
            content_hash = hashlib.md5(c.encode("utf-8")).hexdigest()
            out.append({
                "id": chunk_id,
                "text": c,
                "metadata": {
                    "doc_id": doc_id,
                    "doc_title": doc_title,
                    "page": page_num,
                    "chunk_id": chunk_id,
                    "content_hash": content_hash
                }
            })
    return out