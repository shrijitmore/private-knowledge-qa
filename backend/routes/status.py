from fastapi import APIRouter
from database import client, db
import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("/health")
async def health_check():
    checks = {}

    checks["backend"] = {"status": "healthy", "message": "API server running"}

    try:
        await client.admin.command('ping')
        doc_count = await db.documents.count_documents({})
        checks["database"] = {
            "status": "connected",
            "message": f"MongoDB connected, {doc_count} documents stored"
        }
    except Exception as e:
        checks["database"] = {"status": "disconnected", "message": str(e)}

    try:
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY', ''))
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = await model.generate_content_async(
            "Reply with only the word 'ok'",
            request_options={"timeout": 10}
        )
        checks["llm"] = {
            "status": "connected",
            "message": "Gemini 2.0 Flash responding",
            "model": "gemini-2.0-flash"
        }
    except Exception as e:
        checks["llm"] = {"status": "disconnected", "message": str(e)}

    try:
        from vectorstore.faiss_store import get_total_vectors
        total = get_total_vectors()
        checks["vectorstore"] = {
            "status": "healthy",
            "message": f"FAISS index with {total} vectors"
        }
    except Exception as e:
        checks["vectorstore"] = {"status": "error", "message": str(e)}

    return checks
