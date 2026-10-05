from app.config import settings
from app.services import generate_embeddings


def main() -> None:
    texts = [
        "FastAPI 可以用依赖注入获得数据库会话。",
        "Vue Router 可以保护需要登录的页面。",
    ]
    embeddings = generate_embeddings(texts)

    assert len(embeddings) == len(texts)
    assert all(len(vector) == settings.embedding_dimensions for vector in embeddings)
    print(
        f"Embedding demo passed: {len(embeddings)} vectors, "
        f"{settings.embedding_dimensions} dimensions each."
    )


if __name__ == "__main__":
    main()
