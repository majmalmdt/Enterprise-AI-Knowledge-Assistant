def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100
) -> list[str]:
    """
    Split text into overlapping chunks for RAG.
    """

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks
