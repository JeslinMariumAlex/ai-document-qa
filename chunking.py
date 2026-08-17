def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []

    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # If we haven't reached the end,
        # try to find a sentence boundary.
        if end < len(text):
            sentence_end = text.rfind(".", start, end)

            if sentence_end > start:
                end = sentence_end + 1

        chunk = text[start:end]
        chunks.append(chunk)

        # Always move forward.
        next_start = end - overlap

        if next_start <= start:
            next_start = end
        else:
            # Move to the next word boundary
            while next_start < len(text) and text[next_start] != " ":
                next_start += 1

            next_start += 1

        start = next_start

    return chunks



if __name__ == "__main__":
    text = (
        "FastAPI is a modern Python web framework. "
        "It is used to build APIs quickly. "
        "It supports automatic validation. "
        "PostgreSQL is used for storing application data."
    )

    chunks = chunk_text(text, chunk_size=80, overlap=20)

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)