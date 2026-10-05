def split_text(
    text: str,
    *,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    """Split text into ordered, overlapping character windows."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be at least 0 and less than chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break
        start = end - overlap

    return chunks
