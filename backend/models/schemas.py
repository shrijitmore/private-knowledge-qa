from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone
import uuid


class DocumentMeta(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_size: int
    chunk_count: int
    uploaded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SourceReference(BaseModel):
    document_name: str
    chunk_text: str
    chunk_index: int
    similarity_score: float


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceReference]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class QAHistoryItem(BaseModel):
    id: str
    question: str
    answer: str
    sources: List[SourceReference]
    timestamp: str
