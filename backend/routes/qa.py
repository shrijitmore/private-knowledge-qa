"""
Q&A routes — ask a question and retrieve run history.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import QuestionRequest, AnswerResponse, QAHistoryItem
from services.qa_service import answer_question, get_history
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/qa", tags=["qa"])


@router.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """Run the RAG pipeline: embed → search → generate → return answer with sources."""
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        return await answer_question(request.question.strip())
    except Exception as e:
        logger.error("QA failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")


@router.get("/history", response_model=List[QAHistoryItem])
async def qa_history():
    """Return the last N question-answer pairs (newest first)."""
    try:
        return await get_history()
    except Exception as e:
        logger.error("History fetch failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch history")
