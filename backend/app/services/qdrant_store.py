from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from .embedder import Embedder
from app.config import settings

client = QdrantClient(url=settings.qdrant_url)

def ensure_collection(vector_size: int):
    collections = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection not in collections:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_chunks(chunks: list[dict], embedder: Embedder):
    # chunks items include: id, text, metadata
    vectors = embedder.embed([c["text"] for c in chunks])
    points = []
    for c, v in zip(chunks, vectors):
        points.append(PointStruct(
            id=c["id"],
            vector=v,
            payload={
                "text": c["text"],
                **c["metadata"]
            }
        ))
    client.upsert(collection_name=settings.qdrant_collection, points=points)

def search(query_vector: list[float], top_k: int, filters: dict | None = None):
    qfilter = None
    if filters:
        # Basic exact match filters on payload fields
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue
        must = []
        for k, v in filters.items():
            must.append(FieldCondition(key=k, match=MatchValue(value=v)))
        qfilter = Filter(must=must)

    return client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        score_threshold=None,
        query_filter=qfilter
    )