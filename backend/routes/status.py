"""
System health and status routes.

Checks connectivity to MongoDB, Gemini LLM, and the FAISS vector store.
"""

from fastapi import APIRouter
from database import client, db
from models.schemas import HealthStatus
from config import GEMINI_API_KEY, GEMINI_CHAT_MODEL
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """Run connectivity probes against every backend dependency."""
    checks: dict = {}

    # ── Backend ──────────────────────────────────────────────────
    checks["backend"] = {"status": "healthy", "message": "API server running"}

    # ── MongoDB ──────────────────────────────────────────────────
    try:
        await client.admin.command("ping")
        doc_count = await db.documents.count_documents({})
        checks["database"] = {
            "status": "connected",
            "message": f"MongoDB connected, {doc_count} documents stored",
        }
    except Exception as e:
        checks["database"] = {"status": "disconnected", "message": str(e)}

    # ── Gemini LLM ───────────────────────────────────────────────
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_CHAT_MODEL)
        await model.generate_content_async(
            "Reply with only the word 'ok'",
            request_options={"timeout": 10},
        )
        checks["llm"] = {
            "status": "connected",
            "message": f"{GEMINI_CHAT_MODEL} responding",
            "model": GEMINI_CHAT_MODEL,
        }
    except Exception as e:
        checks["llm"] = {"status": "disconnected", "message": str(e)}

    # ── FAISS Vector Store ───────────────────────────────────────
    try:
        from vectorstore.faiss_store import get_total_vectors

        total = get_total_vectors()
        checks["vectorstore"] = {
            "status": "healthy",
            "message": f"FAISS index with {total} vectors",
        }
    except Exception as e:
        checks["vectorstore"] = {"status": "error", "message": str(e)}

    return checks
