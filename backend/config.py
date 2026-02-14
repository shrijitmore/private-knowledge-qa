"""
Centralized application configuration.

All tunables, paths, and environment-derived settings live here so that
service modules never read os.environ directly (except database.py which
bootstraps first).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# ── MongoDB ──────────────────────────────────────────────────────────
MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/knowledge_qa")
# Extract database name from URI, removing any query parameters
DB_NAME: str = MONGODB_URI.split("/")[-1].split("?")[0] if "/" in MONGODB_URI else "knowledge_qa"

# ── Gemini LLM ──────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]
GEMINI_CHAT_MODEL: str = "gemini-2.0-flash"
GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"
GEMINI_EMBEDDING_DIM: int = 3072
LLM_TIMEOUT_SECONDS: int = 30

# ── Document Processing ─────────────────────────────────────────────
CHUNK_SIZE: int = 500           # characters per chunk
CHUNK_OVERLAP: int = 100        # overlap between consecutive chunks
EMBEDDING_BATCH_SIZE: int = 100 # texts per Gemini embed_content call
MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB

# ── Storage Paths ────────────────────────────────────────────────────
UPLOAD_DIR: Path = ROOT_DIR / "uploads"
FAISS_DATA_DIR: Path = ROOT_DIR / "data"
FAISS_INDEX_PATH: Path = FAISS_DATA_DIR / "faiss_index.bin"
FAISS_META_PATH: Path = FAISS_DATA_DIR / "metadata.json"

# ── QA ───────────────────────────────────────────────────────────────
SIMILARITY_TOP_K: int = 5
QA_HISTORY_LIMIT: int = 5
SOURCE_PREVIEW_LENGTH: int = 200  # max chars shown per source chunk

# ── CORS ─────────────────────────────────────────────────────────────
CORS_ORIGINS: list[str] = os.environ.get("CORS_ORIGINS", "*").split(",")

# Ensure writable directories exist at import time
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FAISS_DATA_DIR.mkdir(parents=True, exist_ok=True)
