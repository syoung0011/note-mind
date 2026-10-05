from app.models import NoteChunk
from app.services.retrieval import RetrievalCandidate, rank_chunks


def make_candidate(chunk_id: int, embedding: list[float]) -> RetrievalCandidate:
    return RetrievalCandidate(
        chunk=NoteChunk(
            id=chunk_id,
            note_id=1,
            user_id=1,
            chunk_index=chunk_id - 1,
            content=f"chunk {chunk_id}",
            embedding=embedding,
        ),
        note_title=f"note {chunk_id}",
    )


def main() -> None:
    candidates = [
        make_candidate(1, [0.0, 1.0]),
        make_candidate(2, [0.8, 0.2]),
        make_candidate(3, [0.6, 0.8]),
    ]

    results = rank_chunks([1.0, 0.0], candidates, top_k=2)

    assert [result.chunk.id for result in results] == [2, 3]
    assert [result.note_title for result in results] == ["note 2", "note 3"]
    assert results[0].score > results[1].score
    top_one = rank_chunks([1.0, 0.0], candidates, top_k=1)
    assert [result.chunk.id for result in top_one] == [2]

    thresholded = rank_chunks(
        [1.0, 0.0],
        candidates,
        top_k=3,
        min_score=0.60,
    )
    assert [result.chunk.id for result in thresholded] == [2, 3]
    assert thresholded[1].score == 0.60
    print("Retrieval demo passed: top-k chunks are ordered by similarity.")


if __name__ == "__main__":
    main()
