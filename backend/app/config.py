import os
from pydantic import BaseModel

class Settings(BaseModel):
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "pdf_chunks")

    embed_model: str = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
    rerank_model: str = os.getenv("RERANK_MODEL", "BAAI/bge-reranker-large")

    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:8000/v1")
    llm_model: str = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    llm_api_key: str = os.getenv("LLM_API_KEY", "local-key")

    top_k: int = int(os.getenv("TOP_K", "30"))
    rerank_top_n: int = int(os.getenv("RERANK_TOP_N", "8"))
    min_top_score: float = float(os.getenv("MIN_TOP_SCORE", "0.25"))
    min_rerank_score: float = float(os.getenv("MIN_RERANK_SCORE", "0.10"))
    min_citations: int = int(os.getenv("MIN_CITATIONS", "2"))

    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

settings = Settings()