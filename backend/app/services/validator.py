import re
from app.config import settings

CITATION_RE = re.compile(r"\[[^:\]]+:p\d+#.+?\]")

def extract_citations(text: str):
    return list(set(CITATION_RE.findall(text)))

def validate(answer_text: str, passages: list[dict]):
    citations = extract_citations(answer_text)
    ok = True
    reason = None

    if "I don't know based on the provided guides." in answer_text.strip():
        return {"ok": True, "refusal": True, "confidence": 0.0, "citations": []}

    if len(citations) < settings.min_citations:
        ok = False
        reason = "Insufficient citations"

    # Ensure citations refer to retrieved chunks
    allowed = set([f'[{p["doc_id"]}:p{p["page"]}#{p["chunk_id"]}]' for p in passages])
    bad = [c for c in citations if c not in allowed]
    if bad:
        ok = False
        reason = "Citations not in retrieved sources"

    confidence = 0.85 if ok else 0.2
    return {"ok": ok, "refusal": False, "confidence": confidence, "citations": citations, "reason": reason}