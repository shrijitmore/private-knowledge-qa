"""
Text chunking and filename sanitisation utilities.

Used by the document ingestion pipeline to split raw text into
overlapping windows before embedding generation.
"""

import os
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split *text* into overlapping chunks of approximately *size* characters.

    Each chunk is stripped of leading/trailing whitespace.  Empty chunks
    (that would result from runs of whitespace) are silently dropped.

    Args:
        text: The full document text.
        size: Maximum character length per chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        A list of non-empty text chunks.
    """
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def sanitize_filename(filename: str) -> str:
    """Return a safe base filename with path-traversal characters removed.

    Args:
        filename: The raw filename from the upload (may contain slashes or ``..``).

    Returns:
        A sanitised filename safe for use in local storage paths.
    """
    name = os.path.basename(filename)
    return name.replace("..", "").replace("/", "").replace("\\", "")
