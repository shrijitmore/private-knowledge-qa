from fastapi import APIRouter, UploadFile, File, HTTPException
from services.document_service import process_upload, list_documents, delete_document
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    try:
        result = await process_upload(file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Upload processing failed")


@router.get("/")
async def get_documents():
    try:
        return await list_documents()
    except Exception as e:
        logger.error(f"List documents failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.delete("/{doc_id}")
async def remove_document(doc_id: str):
    try:
        return await delete_document(doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Delete failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete document")
