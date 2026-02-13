import os
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from fastapi import UploadFile
from database import db
from services.embedding_service import generate_embeddings
from vectorstore.faiss_store import add_vectors, remove_by_doc_id

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def chunk_text(text: str) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - CHUNK_OVERLAP
    return chunks


def sanitize_filename(filename: str) -> str:
    name = os.path.basename(filename)
    name = name.replace('..', '').replace('/', '').replace('\\', '')
    return name


async def process_upload(file: UploadFile) -> dict:
    doc_id = str(uuid.uuid4())
    filename = sanitize_filename(file.filename)

    content = await file.read()
    file_size = len(content)

    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("File must be valid UTF-8 text")

    if not text.strip():
        raise ValueError("File is empty")

    file_path = UPLOAD_DIR / f"{doc_id}_{filename}"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    chunks = chunk_text(text)
    embeddings = await generate_embeddings(chunks)

    metadata_entries = [
        {
            "doc_id": doc_id,
            "doc_name": filename,
            "chunk_text": chunk,
            "chunk_index": i
        }
        for i, chunk in enumerate(chunks)
    ]
    add_vectors(embeddings, metadata_entries)

    doc_meta = {
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunk_count": len(chunks),
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    }
    await db.documents.insert_one(doc_meta)

    return {
        "id": doc_id,
        "filename": filename,
        "file_size": file_size,
        "chunk_count": len(chunks),
        "uploaded_at": doc_meta["uploaded_at"]
    }


async def list_documents() -> list:
    docs = await db.documents.find({}, {"_id": 0}).to_list(100)
    return docs


async def delete_document(doc_id: str) -> dict:
    result = await db.documents.delete_one({"id": doc_id})
    if result.deleted_count == 0:
        raise ValueError("Document not found")

    remove_by_doc_id(doc_id)

    for f in UPLOAD_DIR.glob(f"{doc_id}_*"):
        f.unlink()

    return {"message": "Document deleted"}
