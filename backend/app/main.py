from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import ChatRequest, ChatResponse, IngestResponse, Citation

from app.services.retrieval import retrieve
from app.services.generator import generate
from app.services.validator import validate

from app.services.embedder import Embedder
from app.services.qdrant_store import ensure_collection, upsert_chunks
from app.ingestion.pdf_extract import extract_pdf_text_by_page
from app.ingestion.chunking import chunk_pages

import uuid

app = FastAPI(title="OSS PDF RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init collection
_embedder = Embedder()
ensure_collection(_embedder.dim)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    ctx = await retrieve(req.question, req.filters)
    passages = ctx["passages"]
    if not passages:
        return ChatResponse(
            answer="I don’t have enough information in the provided guides to answer that reliably.",
            citations=[],
            confidence=0.0,
            refusal=True,
            reason=ctx.get("reason", "No evidence"),
        )

    answer_text = await generate(req.question, passages)
    verdict = validate(answer_text, passages)

    if not verdict["ok"]:
        return ChatResponse(
            answer="I don’t have enough information in the provided guides to answer that reliably.",
            citations=[],
            confidence=verdict["confidence"],
            refusal=True,
            reason=verdict["reason"],
        )

    # Build structured citations (top passages)
    cits = []
    for p in passages:
        cits.append(Citation(
            doc_id=p["doc_id"], doc_title=p["doc_title"], page=p["page"],
            chunk_id=p["chunk_id"], score=p.get("rerank_score", p["score"])
        ))

    return ChatResponse(
        answer=answer_text,
        citations=cits,
        confidence=verdict["confidence"],
        refusal=verdict["refusal"]
    )

@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    doc_id = str(uuid.uuid4())
    title = file.filename

    pages = extract_pdf_text_by_page(content)
    chunks = chunk_pages(pages, doc_id=doc_id, doc_title=title)

    upsert_chunks(chunks, _embedder)
    return IngestResponse(doc_id=doc_id, title=title, chunks_indexed=len(chunks))