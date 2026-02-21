from app.services.embedder import Embedder
from app.services.reranker import Reranker
from app.services.qdrant_store import search
from app.config import settings

embedder = Embedder()
reranker = Reranker()

async def retrieve(question: str, filters: dict | None):
    qv = embedder.embed([question])[0]
    raw = search(qv, settings.top_k, filters)

    passages = []
    for r in raw:
        payload = r.payload or {}
        passages.append({
            "id": str(r.id),
            "text": payload.get("text", ""),
            "score": float(r.score),
            "doc_id": payload.get("doc_id", "unknown"),
            "doc_title": payload.get("doc_title", "unknown"),
            "page": int(payload.get("page", -1)),
            "chunk_id": payload.get("chunk_id", str(r.id)),
        })

    # Evidence gate at retrieval stage
    top_score = max([p["score"] for p in passages], default=0.0)
    if top_score < settings.min_top_score:
        return {"passages": [], "top_score": top_score, "reason": "Low retrieval score"}

    reranked = reranker.rerank(question, passages)
    reranked = reranked[:settings.rerank_top_n]

    # Evidence gate at rerank stage
    if reranked and reranked[0]["rerank_score"] < settings.min_rerank_score:
        return {"passages": [], "top_score": top_score, "reason": "Low rerank score"}

    return {"passages": reranked, "top_score": top_score, "reason": None}