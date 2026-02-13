"""FAISS-based vector store for document chunk embeddings."""

from vectorstore.faiss_store import (
    load_store,
    add_vectors,
    search,
    remove_by_doc_id,
    get_total_vectors,
)
