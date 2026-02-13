"""
Document management routes — upload, list, and delete.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from models.schemas import DocumentMeta, MessageResponse
from services.document_service import process_upload, list_documents, delete_document
from config import MAX_FILE_SIZE
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentMeta)
async def upload_document(file: UploadFile = File(...)):
    """Upload a ``.txt`` file, chunk it, generate embeddings, and index it."""
    if not file.filename or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    try:
        result = await process_upload(file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Upload failed: %s", e)
        raise HTTPException(status_code=500, detail="Upload processing failed")


@router.get("/", response_model=List[DocumentMeta])
async def get_documents():
    """Return metadata for every uploaded document."""
    try:
        return await list_documents()
    except Exception as e:
        logger.error("List documents failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.delete("/{doc_id}", response_model=MessageResponse)
async def remove_document(doc_id: str):
    """Delete a document by its UUID from MongoDB, FAISS, and disk."""
    try:
        return await delete_document(doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Delete failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to delete document")
