from fastapi import APIRouter, HTTPException
from models.schemas import QuestionRequest
from services.qa_service import answer_question, get_history
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/qa", tags=["qa"])


@router.post("/ask")
async def ask(request: QuestionRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        return await answer_question(request.question.strip())
    except Exception as e:
        logger.error(f"QA failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")


@router.get("/history")
async def qa_history():
    try:
        return await get_history()
    except Exception as e:
        logger.error(f"History fetch failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")
