from app.models import NoteChunk
from app.services.retrieval import rank_chunks


def make_chunk(chunk_id: int, embedding: list[float]) -> NoteChunk:
    return NoteChunk(
        id=chunk_id,
        note_id=1,
        user_id=1,
        chunk_index=chunk_id - 1,
        content=f"chunk {chunk_id}",
        embedding=embedding,
    )


def main() -> None:
    chunks = [
        make_chunk(1, [0.0, 1.0]),
        make_chunk(2, [0.8, 0.2]),
        make_chunk(3, [0.6, 0.8]),
    ]

    results = rank_chunks([1.0, 0.0], chunks, top_k=2)

    assert [result.chunk.id for result in results] == [2, 3]
    assert results[0].score > results[1].score
    top_one = rank_chunks([1.0, 0.0], chunks, top_k=1)
    assert [result.chunk.id for result in top_one] == [2]
    print("Retrieval demo passed: top-k chunks are ordered by similarity.")


if __name__ == "__main__":
    main()
