from math import sqrt


QUERY_VECTOR = [1.0, 0.0]

CHUNKS = [
    {
        "id": 1,
        "text": "FastAPI 会自动读取 .env 吗？",
        "vector": [0.8, 0.2],
    },
    {
        "id": 2,
        "text": "Vue 的响应式状态如何更新页面？",
        "vector": [0.0, 1.0],
    },
    {
        "id": 3,
        "text": "RAG 如何找到相关笔记？",
        "vector": [0.6, 0.8],
    },
]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b, strict=True))
    magnitude_a = sqrt(sum(value**2 for value in vector_a))
    magnitude_b = sqrt(sum(value**2 for value in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Zero vectors do not have a cosine direction")

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_top_k(
    query_vector: list[float],
    chunks: list[dict],
    top_k: int,
    min_score: float,
) -> list[dict]:
    scored_chunks = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        if score >= min_score:
            scored_chunks.append({**chunk, "score": score})
    scored_chunks.sort(key=lambda chunk: chunk["score"], reverse=True)
    return scored_chunks[:top_k]


def main() -> None:
    results = retrieve_top_k(QUERY_VECTOR, CHUNKS, top_k=3, min_score=0.5)

    for rank, chunk in enumerate(results, start=1):
        print(f"{rank}. {chunk['text']} | score={chunk['score']:.3f}")


if __name__ == "__main__":
    main()
