from dataclasses import dataclass
from math import sqrt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import NoteChunk
from app.services.embeddings import generate_embeddings


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: NoteChunk
    score: float


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b, strict=True))
    magnitude_a = sqrt(sum(value**2 for value in vector_a))
    magnitude_b = sqrt(sum(value**2 for value in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Zero vectors do not have a cosine direction")

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_relevant_chunks(
    db: Session,
    user_id: int,
    question: str,
    top_k: int = 3,
) -> list[RetrievedChunk]:
    if not question.strip():
        raise ValueError("Question must not be blank")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    chunks = list(
        db.scalars(select(NoteChunk).where(NoteChunk.user_id == user_id)).all()
    )
    if not chunks:
        return []

    query_embedding = generate_embeddings([question])[0]

    return rank_chunks(query_embedding, chunks, top_k)


def rank_chunks(
    query_embedding: list[float],
    chunks: list[NoteChunk],
    top_k: int,
) -> list[RetrievedChunk]:
    scored_chunks: list[RetrievedChunk] = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk.embedding)
        scored_chunks.append(RetrievedChunk(chunk=chunk, score=score))
    scored_chunks.sort(key=lambda result: result.score, reverse=True)
    return scored_chunks[:top_k]
