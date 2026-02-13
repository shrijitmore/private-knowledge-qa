"""
Retrieval-Augmented Generation (RAG) Q&A service.

Pipeline:
    1. Embed the user question.
    2. Retrieve the closest document chunks from FAISS.
    3. Build a grounded prompt with retrieved context.
    4. Call Gemini to generate an answer.
    5. Persist the Q&A entry in MongoDB for history.
"""

import google.generativeai as genai
import logging
from datetime import datetime, timezone
import uuid
from database import db
from config import (
    GEMINI_API_KEY,
    GEMINI_CHAT_MODEL,
    LLM_TIMEOUT_SECONDS,
    SIMILARITY_TOP_K,
    QA_HISTORY_LIMIT,
    SOURCE_PREVIEW_LENGTH,
)
from services.embedding_service import generate_query_embedding
from vectorstore.faiss_store import search

logger = logging.getLogger(__name__)

_model = None


def _get_model() -> genai.GenerativeModel:
    """Return a lazily-initialised Gemini chat model singleton."""
    global _model
    if _model is None:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(GEMINI_CHAT_MODEL)
    return _model


async def answer_question(question: str) -> dict:
    """Run the full RAG pipeline for a user question.

    Args:
        question: The natural-language question.

    Returns:
        A dict matching the ``AnswerResponse`` schema, including
        the answer text and a list of source references.
    """
    # 1. Embed the question
    query_embedding = await generate_query_embedding(question)

    # 2. Retrieve relevant chunks
    results = search(query_embedding, top_k=SIMILARITY_TOP_K)

    if not results:
        return {
            "question": question,
            "answer": (
                "No documents have been uploaded yet, or no relevant "
                "content was found. Please upload some text documents first."
            ),
            "sources": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # 3. Build grounded prompt
    context_parts = [
        f"[Source: {r['doc_name']}, Chunk {r['chunk_index']}]\n{r['chunk_text']}"
        for r in results
    ]
    context = "\n\n---\n\n".join(context_parts)

    prompt = (
        "You are a helpful assistant that answers questions based strictly "
        "on the provided context.\n"
        "If the answer cannot be found in the context, say so clearly.\n"
        "Always be concise and accurate.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    # 4. Generate answer via Gemini
    model = _get_model()
    response = await model.generate_content_async(
        prompt,
        request_options={"timeout": LLM_TIMEOUT_SECONDS},
    )
    answer_text: str = response.text

    # 5. Build source references with normalised similarity
    max_dist = max((r["distance"] for r in results), default=1.0)
    sources = []
    for r in results:
        similarity = 1.0 - (r["distance"] / (max_dist + 1e-6)) if max_dist > 0 else 1.0
        chunk_preview = r["chunk_text"]
        if len(chunk_preview) > SOURCE_PREVIEW_LENGTH:
            chunk_preview = chunk_preview[:SOURCE_PREVIEW_LENGTH] + "..."
        sources.append(
            {
                "document_name": r["doc_name"],
                "chunk_text": chunk_preview,
                "chunk_index": r["chunk_index"],
                "similarity_score": round(max(0, similarity), 3),
            }
        )

    # 6. Persist to history
    history_entry = {
        "id": str(uuid.uuid4()),
        "question": question,
        "answer": answer_text,
        "sources": sources,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    await db.qa_history.insert_one(history_entry)

    return {
        "question": question,
        "answer": answer_text,
        "sources": sources,
        "timestamp": history_entry["timestamp"],
    }


async def get_history() -> list[dict]:
    """Return the most recent Q&A entries (newest first).

    Limit is controlled by ``QA_HISTORY_LIMIT`` in config.
    """
    return (
        await db.qa_history.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(QA_HISTORY_LIMIT)
        .to_list(QA_HISTORY_LIMIT)
    )
