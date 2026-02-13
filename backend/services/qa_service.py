import google.generativeai as genai
import os
import logging
from datetime import datetime, timezone
import uuid
from database import db
from services.embedding_service import generate_query_embedding
from vectorstore.faiss_store import search

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        _model = genai.GenerativeModel('gemini-2.0-flash')
    return _model


async def answer_question(question: str) -> dict:
    query_embedding = await generate_query_embedding(question)
    results = search(query_embedding, top_k=5)

    if not results:
        return {
            "question": question,
            "answer": "No documents have been uploaded yet, or no relevant content was found. Please upload some text documents first.",
            "sources": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    context_parts = []
    for r in results:
        context_parts.append(f"[Source: {r['doc_name']}, Chunk {r['chunk_index']}]\n{r['chunk_text']}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a helpful assistant that answers questions based strictly on the provided context.
If the answer cannot be found in the context, say so clearly.
Always be concise and accurate.

Context:
{context}

Question: {question}

Answer:"""

    model = _get_model()
    response = await model.generate_content_async(
        prompt,
        request_options={"timeout": 30}
    )

    answer_text = response.text

    sources = []
    max_dist = max((r['distance'] for r in results), default=1.0)
    for r in results:
        similarity = 1.0 - (r['distance'] / (max_dist + 1e-6)) if max_dist > 0 else 1.0
        sources.append({
            "document_name": r['doc_name'],
            "chunk_text": r['chunk_text'][:200] + "..." if len(r['chunk_text']) > 200 else r['chunk_text'],
            "chunk_index": r['chunk_index'],
            "similarity_score": round(max(0, similarity), 3)
        })

    history_entry = {
        "id": str(uuid.uuid4()),
        "question": question,
        "answer": answer_text,
        "sources": sources,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.qa_history.insert_one(history_entry)

    return {
        "question": question,
        "answer": answer_text,
        "sources": sources,
        "timestamp": history_entry["timestamp"]
    }


async def get_history() -> list:
    history = await db.qa_history.find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).limit(5).to_list(5)
    return history
