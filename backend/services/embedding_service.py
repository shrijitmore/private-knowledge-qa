import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

_configured = False


def _ensure_configured():
    global _configured
    if not _configured:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        _configured = True


async def generate_embeddings(texts: list) -> list:
    _ensure_configured()
    embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=batch,
            task_type="retrieval_document"
        )
        embeddings.extend(result['embedding'])
    return embeddings


async def generate_query_embedding(text: str) -> list:
    _ensure_configured()
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"
    )
    return result['embedding']
