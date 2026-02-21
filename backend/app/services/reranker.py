from sentence_transformers import CrossEncoder
from app.config import settings

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(settings.rerank_model)

    def rerank(self, query: str, passages: list[dict]) -> list[dict]:
        pairs = [[query, p["text"]] for p in passages]
        scores = self.model.predict(pairs)
        for p, s in zip(passages, scores):
            p["rerank_score"] = float(s)
        passages.sort(key=lambda x: x["rerank_score"], reverse=True)
        return passages