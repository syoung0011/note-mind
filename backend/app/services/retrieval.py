from dataclasses import dataclass
from math import sqrt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Note, NoteChunk
from app.services.embeddings import generate_embeddings


@dataclass(frozen=True)
class RetrievalCandidate:
    chunk: NoteChunk
    note_title: str


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: NoteChunk
    note_title: str
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
    min_score: float = settings.retrieval_min_score,
) -> list[RetrievedChunk]:
    if not question.strip():
        raise ValueError("Question must not be blank")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")
    if not -1.0 <= min_score <= 1.0:
        raise ValueError("min_score must be between -1 and 1")

    rows = list(
        db.execute(
            select(NoteChunk, Note.title)
            .join(Note, Note.id == NoteChunk.note_id)
            .where(NoteChunk.user_id == user_id)
        ).all()
    )
    if not rows:
        return []

    candidates: list[RetrievalCandidate] = []
    for chunk, note_title in rows:
        candidates.append(RetrievalCandidate(chunk=chunk, note_title=note_title))

    query_embedding = generate_embeddings([question])[0]

    return rank_chunks(query_embedding, candidates, top_k, min_score)


def rank_chunks(
    query_embedding: list[float],
    candidates: list[RetrievalCandidate],
    top_k: int,
    min_score: float = 0.50,
) -> list[RetrievedChunk]:
    scored_chunks: list[RetrievedChunk] = []
    for candidate in candidates:
        score = cosine_similarity(query_embedding, candidate.chunk.embedding)
        if score >= min_score:
            scored_chunks.append(
                RetrievedChunk(
                    chunk=candidate.chunk,
                    note_title=candidate.note_title,
                    score=score,
                )
            )
    scored_chunks.sort(key=lambda result: result.score, reverse=True)
    return scored_chunks[:top_k]
