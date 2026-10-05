from openai import OpenAI

from app.config import settings

MAX_EMBEDDING_BATCH_SIZE = 10


def create_embedding_client() -> OpenAI:
    if settings.dashscope_api_key is None or settings.dashscope_base_url is None:
        raise RuntimeError(
            "DASHSCOPE_API_KEY and DASHSCOPE_BASE_URL must be configured"
        )

    return OpenAI(
        api_key=settings.dashscope_api_key.get_secret_value(),
        base_url=settings.dashscope_base_url,
    )


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    if any(not text.strip() for text in texts):
        raise ValueError("Embedding input must not contain blank text")

    client = create_embedding_client()
    embeddings: list[list[float]] = []

    for start in range(0, len(texts), MAX_EMBEDDING_BATCH_SIZE):
        batch = texts[start : start + MAX_EMBEDDING_BATCH_SIZE]
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=batch,
            dimensions=settings.embedding_dimensions,
            encoding_format="float",
        )
        ordered_items = sorted(response.data, key=lambda item: item.index)
        embeddings.extend(item.embedding for item in ordered_items)

    return embeddings
