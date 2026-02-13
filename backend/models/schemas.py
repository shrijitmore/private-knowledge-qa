"""
Pydantic models used for request validation and response serialisation.

Every model that appears in an API response is referenced via
``response_model`` on the corresponding route so that FastAPI
auto-generates accurate OpenAPI docs.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone
import uuid


# ── Documents ────────────────────────────────────────────────────────

class DocumentMeta(BaseModel):
    """Metadata for a single uploaded document."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique document identifier")
    filename: str = Field(..., description="Original filename of the uploaded document")
    file_size: int = Field(..., description="File size in bytes")
    chunk_count: int = Field(..., description="Number of text chunks created from the document")
    uploaded_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 upload timestamp",
    )


# ── Q&A ──────────────────────────────────────────────────────────────

class SourceReference(BaseModel):
    """A single source chunk returned alongside an answer."""

    document_name: str = Field(..., description="Filename the chunk originates from")
    chunk_text: str = Field(..., description="Extracted text snippet used as context")
    chunk_index: int = Field(..., description="Zero-based index of the chunk within its document")
    similarity_score: float = Field(..., ge=0, le=1, description="Normalised similarity score (0–1)")


class QuestionRequest(BaseModel):
    """Incoming question payload."""

    question: str = Field(..., min_length=1, description="The natural-language question to answer")


class AnswerResponse(BaseModel):
    """Full answer with grounding sources."""

    question: str
    answer: str
    sources: List[SourceReference]
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 timestamp of when the answer was generated",
    )


class QAHistoryItem(BaseModel):
    """A single entry in the Q&A run history."""

    id: str
    question: str
    answer: str
    sources: List[SourceReference]
    timestamp: str


# ── Status / Health ──────────────────────────────────────────────────

class ServiceStatus(BaseModel):
    """Health status of a single service component."""

    status: str = Field(..., description="One of: healthy, connected, disconnected, error")
    message: str = Field(..., description="Human-readable status detail")
    model: str | None = Field(default=None, description="Model identifier (LLM only)")


class HealthStatus(BaseModel):
    """Aggregated health check response."""

    backend: ServiceStatus
    database: ServiceStatus
    llm: ServiceStatus
    vectorstore: ServiceStatus


# ── Generic ──────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    """Simple message wrapper for delete / action confirmations."""

    message: str
