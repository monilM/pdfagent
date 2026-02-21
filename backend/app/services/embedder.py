from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import settings

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.embed_model)
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str]) -> list[list[float]]:
        emb = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        if isinstance(emb, np.ndarray):
            return emb.tolist()
        return [e.tolist() for e in emb]