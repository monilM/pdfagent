from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class ChatRequest(BaseModel):
    question: str
    filters: Optional[Dict[str, Any]] = None  # e.g. {"doc_id": "guide1"}

class Citation(BaseModel):
    doc_id: str
    doc_title: str
    page: int
    chunk_id: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    confidence: float = 0.0
    refusal: bool = False
    reason: Optional[str] = None

class IngestResponse(BaseModel):
    doc_id: str
    title: str
    chunks_indexed: int