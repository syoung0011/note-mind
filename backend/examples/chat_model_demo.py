from app.models import NoteChunk
from app.services.answering import generate_answer
from app.services.retrieval import RetrievedChunk


def main() -> None:
    chunk = NoteChunk(
        id=1,
        note_id=1,
        user_id=1,
        chunk_index=0,
        content="NoteMind 使用 FastAPI 构建后端 API。",
        embedding=[1.0, 0.0],
    )
    results = [
        RetrievedChunk(chunk=chunk, note_title="后端框架笔记", score=0.99)
    ]

    answer = generate_answer("NoteMind 使用什么框架构建后端？", results)

    if not answer:
        raise AssertionError("Chat model returned a blank answer")
    print(f"Chat model demo passed.\nAnswer: {answer}")


if __name__ == "__main__":
    main()
