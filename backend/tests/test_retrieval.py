import pytest

from app.models import NoteChunk
from app.services.retrieval import RetrievalCandidate, rank_chunks


def make_candidate(
    *,
    note_id: int,
    title: str,
    embedding: list[float],
) -> RetrievalCandidate:
    return RetrievalCandidate(
        chunk=NoteChunk(
            note_id=note_id,
            user_id=1,
            chunk_index=0,
            content=f"Content from {title}",
            embedding=embedding,
        ),
        note_title=title,
    )


def test_rank_chunks_returns_most_relevant_source() -> None:
    candidates = [
        make_candidate(note_id=101, title="FastAPI", embedding=[1.0, 0.0]),
        make_candidate(note_id=202, title="Vue", embedding=[0.0, 1.0]),
    ]

    results = rank_chunks(
        query_embedding=[1.0, 0.0],
        candidates=candidates,
        top_k=1,
        min_score=0.50,
    )

    assert len(results) == 1
    assert results[0].chunk.note_id == 101
    assert results[0].note_title == "FastAPI"
    assert results[0].score == pytest.approx(1.0)


def test_rank_chunks_rejects_irrelevant_source() -> None:
    candidates = [
        make_candidate(note_id=101, title="FastAPI", embedding=[1.0, 0.0]),
    ]

    results = rank_chunks(
        query_embedding=[-1.0, 0.0],
        candidates=candidates,
        top_k=3,
        min_score=0.50,
    )

    assert results == []
