from dataclasses import dataclass

from app.models import NoteChunk
from app.routers.chat import build_citations
from app.services.retrieval import RetrievalCandidate, rank_chunks


@dataclass(frozen=True)
class EvalCase:
    name: str
    query_embedding: list[float]
    candidates: list[RetrievalCandidate]
    expected_note_ids: list[int]


def make_candidate(
    chunk_id: int,
    note_id: int,
    title: str,
    content: str,
    embedding: list[float],
) -> RetrievalCandidate:
    return RetrievalCandidate(
        chunk=NoteChunk(
            id=chunk_id,
            note_id=note_id,
            user_id=1,
            chunk_index=0,
            content=content,
            embedding=embedding,
        ),
        note_title=title,
    )


def main() -> None:
    knowledge = [
        make_candidate(
            chunk_id=1,
            note_id=101,
            title="FastAPI 笔记",
            content="FastAPI 使用依赖注入获取当前用户。",
            embedding=[1.0, 0.0],
        ),
        make_candidate(
            chunk_id=2,
            note_id=202,
            title="Vue 笔记",
            content="Vue 使用响应式状态更新页面。",
            embedding=[0.0, 1.0],
        ),
    ]
    cases = [
        EvalCase(
            name="relevant question returns its source",
            query_embedding=[1.0, 0.0],
            candidates=knowledge,
            expected_note_ids=[101],
        ),
        EvalCase(
            name="irrelevant question is rejected",
            query_embedding=[-1.0, 0.0],
            candidates=knowledge,
            expected_note_ids=[],
        ),
        EvalCase(
            name="empty knowledge base is rejected",
            query_embedding=[1.0, 0.0],
            candidates=[],
            expected_note_ids=[],
        ),
        EvalCase(
            name="second relevant topic returns its source",
            query_embedding=[0.0, 1.0],
            candidates=knowledge,
            expected_note_ids=[202],
        ),
    ]

    for case in cases:
        results = rank_chunks(
            case.query_embedding,
            case.candidates,
            top_k=3,
            min_score=0.50,
        )
        citations = build_citations(results)
        actual_note_ids = [citation.note_id for citation in citations]
        assert actual_note_ids == case.expected_note_ids, (
            f"{case.name}: expected {case.expected_note_ids}, got {actual_note_ids}"
        )
        print(f"PASS: {case.name}")

    first_result = rank_chunks(
        [1.0, 0.0],
        knowledge,
        top_k=3,
        min_score=0.50,
    )[0]
    first_citation = build_citations([first_result])[0]
    assert first_citation.note_title == "FastAPI 笔记"
    assert first_citation.chunk_index == 0
    assert first_citation.content == "FastAPI 使用依赖注入获取当前用户。"
    assert first_citation.score == 1.0
    print("PASS: citation fields match the retrieved chunk")
    print("RAG quality eval passed: 5 checks completed.")


if __name__ == "__main__":
    main()
