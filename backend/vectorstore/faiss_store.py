"""
FAISS vector store for semantic search over document chunks.

Maintains an in-memory ``IndexFlatL2`` index that is persisted to disk
after every mutation so that data survives server restarts.  A parallel
JSON metadata file maps each vector index position to the originating
document and chunk text.
"""

import faiss
import numpy as np
import json
import logging
from pathlib import Path
from config import FAISS_DATA_DIR, FAISS_INDEX_PATH, FAISS_META_PATH, GEMINI_EMBEDDING_DIM

logger = logging.getLogger(__name__)

_index: faiss.IndexFlatL2 | None = None
_metadata: list[dict] = []


def _ensure_dir() -> None:
    """Create the data directory if it does not exist."""
    FAISS_DATA_DIR.mkdir(parents=True, exist_ok=True)


async def load_store() -> None:
    """Load the FAISS index + metadata from disk, or create a new empty index.

    Called once during application startup.
    """
    global _index, _metadata
    _ensure_dir()
    if FAISS_INDEX_PATH.exists() and FAISS_META_PATH.exists():
        _index = faiss.read_index(str(FAISS_INDEX_PATH))
        with open(FAISS_META_PATH, "r") as f:
            _metadata = json.load(f)
        logger.info("Loaded FAISS index with %d vectors", _index.ntotal)
    else:
        _index = faiss.IndexFlatL2(GEMINI_EMBEDDING_DIM)
        _metadata = []
        logger.info("Created new FAISS index (dim=%d)", GEMINI_EMBEDDING_DIM)


def _save() -> None:
    """Persist the current index and metadata to disk."""
    _ensure_dir()
    faiss.write_index(_index, str(FAISS_INDEX_PATH))
    with open(FAISS_META_PATH, "w") as f:
        json.dump(_metadata, f)


def add_vectors(embeddings: list[list[float]], metadata_entries: list[dict]) -> None:
    """Append *embeddings* and their corresponding *metadata_entries* to the store.

    Args:
        embeddings: List of float vectors (one per chunk).
        metadata_entries: List of dicts with keys ``doc_id``, ``doc_name``,
            ``chunk_text``, ``chunk_index``.
    """
    global _index, _metadata
    if not embeddings:
        return
    vectors = np.array(embeddings, dtype=np.float32)
    _index.add(vectors)
    _metadata.extend(metadata_entries)
    _save()


def search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """Return the *top_k* closest chunks to *query_embedding*.

    Each result dict includes all metadata keys plus a ``distance`` field
    (L2 distance — lower is more similar).
    """
    global _index, _metadata
    if _index is None or _index.ntotal == 0:
        return []
    query = np.array([query_embedding], dtype=np.float32)
    k = min(top_k, _index.ntotal)
    distances, indices = _index.search(query, k)
    results: list[dict] = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(_metadata):
            entry = _metadata[idx].copy()
            entry["distance"] = float(distances[0][i])
            results.append(entry)
    return results


def remove_by_doc_id(doc_id: str) -> None:
    """Remove all vectors belonging to *doc_id* and rebuild the index.

    This reconstructs every kept vector and creates a fresh index, which
    is acceptable at the current data scale.
    """
    global _index, _metadata
    keep_indices = [i for i, m in enumerate(_metadata) if m["doc_id"] != doc_id]
    if not keep_indices:
        _index = faiss.IndexFlatL2(GEMINI_EMBEDDING_DIM)
        _metadata = []
        _save()
        return
    kept_vectors = [_index.reconstruct(i) for i in keep_indices]
    new_index = faiss.IndexFlatL2(GEMINI_EMBEDDING_DIM)
    new_index.add(np.array(kept_vectors, dtype=np.float32))
    _metadata = [_metadata[i] for i in keep_indices]
    _index = new_index
    _save()


def get_total_vectors() -> int:
    """Return the number of vectors currently stored in the index."""
    return _index.ntotal if _index else 0
