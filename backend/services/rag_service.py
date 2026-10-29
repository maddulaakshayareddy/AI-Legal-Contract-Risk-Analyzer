
from typing import List
from functools import lru_cache

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(
        MODEL_NAME,
        device="cpu"
    )


def split_into_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[str]:
    """Split contract text into overlapping chunks."""

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
    """Convert text chunks into normalized embedding vectors."""

    if not chunks:
        return np.empty((0, 0), dtype="float32")

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=1,
        show_progress_bar=False
    )

    return np.asarray(embeddings, dtype="float32")


def build_faiss_index(chunks: List[str]):
    """Build a FAISS similarity-search index."""

    if not chunks:
        return None

    embeddings = create_embeddings(chunks)

    if embeddings.size == 0:
        return None

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def retrieve_relevant_chunks(
    query: str,
    chunks: List[str],
    top_k: int = 5
) -> List[str]:
    """Retrieve relevant contract chunks using semantic similarity."""

    if not query or not chunks:
        return []

    index = build_faiss_index(chunks)

    if index is None:
        return []

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=1,
        show_progress_bar=False
    ).astype("float32")

    k = min(top_k, len(chunks))
    scores, indices = index.search(query_embedding, k)

    results = []

    for score, position in zip(scores[0], indices[0]):
        if position >= 0:
            results.append(chunks[position])

    return results


def build_rag_context(
    query: str,
    contract_text: str,
    top_k: int = 5
) -> str:
    """Build context from the most relevant contract sections."""

    chunks = split_into_chunks(contract_text)

    relevant_chunks = retrieve_relevant_chunks(
        query,
        chunks,
        top_k=top_k
    )

    if not relevant_chunks:
        return "No relevant contract sections were found."

    return "\n\n".join(
        f"[Relevant Contract Section {number}]\n{chunk}"
        for number, chunk in enumerate(relevant_chunks, start=1)
    )
