import faiss
import numpy as np
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STORE_DIR = Path(__file__).parent.parent / "data"
INDEX_PATH = STORE_DIR / "faiss_index.bin"
META_PATH = STORE_DIR / "metadata.json"
EMBEDDING_DIM = 3072

_index = None
_metadata = []


def _ensure_dir():
    STORE_DIR.mkdir(parents=True, exist_ok=True)


async def load_store():
    global _index, _metadata
    _ensure_dir()
    if INDEX_PATH.exists() and META_PATH.exists():
        _index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, 'r') as f:
            _metadata = json.load(f)
        logger.info(f"Loaded FAISS index with {_index.ntotal} vectors")
    else:
        _index = faiss.IndexFlatL2(EMBEDDING_DIM)
        _metadata = []
        logger.info("Created new FAISS index")


def _save():
    _ensure_dir()
    faiss.write_index(_index, str(INDEX_PATH))
    with open(META_PATH, 'w') as f:
        json.dump(_metadata, f)


def add_vectors(embeddings: list, metadata_entries: list):
    global _index, _metadata
    if not embeddings:
        return
    vectors = np.array(embeddings, dtype=np.float32)
    _index.add(vectors)
    _metadata.extend(metadata_entries)
    _save()


def search(query_embedding: list, top_k: int = 5):
    global _index, _metadata
    if _index is None or _index.ntotal == 0:
        return []
    query = np.array([query_embedding], dtype=np.float32)
    k = min(top_k, _index.ntotal)
    distances, indices = _index.search(query, k)
    results = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(_metadata):
            entry = _metadata[idx].copy()
            entry['distance'] = float(distances[0][i])
            results.append(entry)
    return results


def remove_by_doc_id(doc_id: str):
    global _index, _metadata
    keep_indices = [i for i, m in enumerate(_metadata) if m['doc_id'] != doc_id]
    if not keep_indices:
        _index = faiss.IndexFlatL2(EMBEDDING_DIM)
        _metadata = []
        _save()
        return
    kept_vectors = []
    for i in keep_indices:
        vec = _index.reconstruct(i)
        kept_vectors.append(vec)
    new_index = faiss.IndexFlatL2(EMBEDDING_DIM)
    new_index.add(np.array(kept_vectors, dtype=np.float32))
    _metadata = [_metadata[i] for i in keep_indices]
    _index = new_index
    _save()


def get_total_vectors():
    return _index.ntotal if _index else 0
