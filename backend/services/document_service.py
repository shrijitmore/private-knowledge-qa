"""
Document ingestion service.

Handles the full upload pipeline: read → validate → save to disk →
chunk → embed → store vectors in FAISS → persist metadata in MongoDB.
"""

import uuid
import logging
from datetime import datetime, timezone
from fastapi import UploadFile
from database import db
from config import UPLOAD_DIR
from utils.text import chunk_text, sanitize_filename
from services.embedding_service import generate_embeddings
from vectorstore.faiss_store import add_vectors, remove_by_doc_id

logger = logging.getLogger(__name__)


async def process_upload(file: UploadFile) -> dict:
    """Process an uploaded text file through the full ingestion pipeline.

    Steps:
        1. Sanitise filename and read raw bytes.
        2. Decode as UTF-8 (rejects non-text files).
        3. Save the file to ``UPLOAD_DIR``.
        4. Chunk the text into overlapping windows.
        5. Generate embeddings via Gemini.
        6. Store vectors + metadata in FAISS.
        7. Persist document metadata in MongoDB.

    Args:
        file: The ``UploadFile`` from the FastAPI request.

    Returns:
        A dict matching the ``DocumentMeta`` schema.

    Raises:
        ValueError: If the file is not valid UTF-8 or is empty.
    """
    doc_id = str(uuid.uuid4())
    filename = sanitize_filename(file.filename)

    content = await file.read()
    file_size = len(content)

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("File must be valid UTF-8 text")

    if not text.strip():
        raise ValueError("File is empty")

    # Persist raw file to disk
    file_path = UPLOAD_DIR / f"{doc_id}_{filename}"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Chunk → Embed → Store
    chunks = chunk_text(text)
    embeddings = await generate_embeddings(chunks)

    metadata_entries = [
        {
            "doc_id": doc_id,
            "doc_name": filename,
            "chunk_text": chunk,
            "chunk_index": i,
        }
        for i, chunk in enumerate(chunks)
    ]
    add_vectors(embeddings, metadata_entries)

    # MongoDB metadata
    doc_meta = {
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunk_count": len(chunks),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.documents.insert_one(doc_meta)

    return {
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunk_count": len(chunks),
        "uploaded_at": doc_meta["uploaded_at"],
    }


async def list_documents() -> list[dict]:
    """Return all document metadata records (``_id`` excluded)."""
    return await db.documents.find({}, {"_id": 0}).to_list(100)


async def delete_document(doc_id: str) -> dict:
    """Remove a document from MongoDB, FAISS, and disk.

    Args:
        doc_id: The UUID of the document to delete.

    Returns:
        A confirmation message dict.

    Raises:
        ValueError: If no document with *doc_id* exists.
    """
    result = await db.documents.delete_one({"id": doc_id})
    if result.deleted_count == 0:
        raise ValueError("Document not found")

    remove_by_doc_id(doc_id)

    for f in UPLOAD_DIR.glob(f"{doc_id}_*"):
        f.unlink()

    return {"message": "Document deleted"}
