from app.models import NoteChunk
from app.services.answering import build_context
from app.services.retrieval import RetrievedChunk


def make_result(chunk_id: int, content: str, score: float) -> RetrievedChunk:
    chunk = NoteChunk(
        id=chunk_id,
        note_id=1,
        user_id=1,
        chunk_index=chunk_id - 1,
        content=content,
        embedding=[1.0, 0.0],
    )
    return RetrievedChunk(chunk=chunk, note_title="FastAPI 学习笔记", score=score)


def main() -> None:
    results = [
        make_result(1, "FastAPI 使用依赖注入获取当前用户。", 0.95),
        make_result(2, "查询笔记时需要按 user_id 过滤。", 0.88),
    ]

    context = build_context(results)

    assert context == (
        "[片段 1]\nFastAPI 使用依赖注入获取当前用户。\n\n"
        "[片段 2]\n查询笔记时需要按 user_id 过滤。"
    )
    print("Answering demo passed: context keeps rank, content, and boundaries.")


if __name__ == "__main__":
    main()
