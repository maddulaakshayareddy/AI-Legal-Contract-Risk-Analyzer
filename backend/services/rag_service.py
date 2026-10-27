from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# Load the embedding model once when the backend starts.
# It converts text into numerical vectors based on meaning.
MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)


def split_into_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[str]:
    """
    Split contract text into overlapping chunks.

    Example:
    Chunk 1 -> characters 0-1200
    Chunk 2 -> characters 1000-2200
    """

    if not text:
        return []

    text = text.strip()

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def create_embeddings(chunks: List[str]) -> np.ndarray:
    """
    Convert text chunks into embedding vectors.
    """

    if not chunks:
        return np.array([], dtype="float32")

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.astype("float32")


def build_faiss_index(
    chunks: List[str]
):
    """
    Create a FAISS similarity-search index from text chunks.
    """

    if not chunks:
        return None

    embeddings = create_embeddings(chunks)

    dimension = embeddings.shape[1]

    # Inner product works as cosine similarity
    # because embeddings are normalized.
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def retrieve_relevant_chunks(
    query: str,
    chunks: List[str],
    top_k: int = 5
) -> List[str]:
    """
    Retrieve the most semantically relevant contract chunks.
    """

    if not query or not chunks:
        return []

    index = build_faiss_index(chunks)

    if index is None:
        return []

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    k = min(top_k, len(chunks))

    scores, indices = index.search(query_embedding, k)

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position < 0:
            continue

        results.append(chunks[index_position])

    return results


def build_rag_context(
    query: str,
    contract_text: str,
    top_k: int = 5
) -> str:
    """
    Build a context string containing the most relevant
    contract sections for the user's question.
    """

    chunks = split_into_chunks(contract_text)

    relevant_chunks = retrieve_relevant_chunks(
        query,
        chunks,
        top_k=top_k
    )

    if not relevant_chunks:
        return "No relevant contract sections were found."

    context_parts = []

    for number, chunk in enumerate(relevant_chunks, start=1):
        context_parts.append(
            f"[Relevant Contract Section {number}]\n{chunk}"
        )

    return "\n\n".join(context_parts)