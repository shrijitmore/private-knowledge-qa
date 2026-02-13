"""
Embedding generation service using Google Gemini.

Wraps the ``google.generativeai`` embed_content API with lazy
configuration and batching support.
"""

import google.generativeai as genai
import logging
from config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL, EMBEDDING_BATCH_SIZE

logger = logging.getLogger(__name__)

_configured: bool = False


def _ensure_configured() -> None:
    """Configure the Gemini SDK once (idempotent)."""
    global _configured
    if not _configured:
        genai.configure(api_key=GEMINI_API_KEY)
        _configured = True


async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate document embeddings for a list of text chunks.

    Texts are batched in groups of ``EMBEDDING_BATCH_SIZE`` to stay within
    Gemini API limits.

    Args:
        texts: Raw text chunks to embed.

    Returns:
        A list of float vectors, one per input text, in the same order.
    """
    _ensure_configured()
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[i : i + EMBEDDING_BATCH_SIZE]
        result = genai.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            content=batch,
            task_type="retrieval_document",
        )
        embeddings.extend(result["embedding"])
    return embeddings


async def generate_query_embedding(text: str) -> list[float]:
    """Generate a single query embedding optimised for retrieval.

    Args:
        text: The user question to embed.

    Returns:
        A float vector of length ``GEMINI_EMBEDDING_DIM``.
    """
    _ensure_configured()
    result = genai.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_query",
    )
    return result["embedding"]
