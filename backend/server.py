"""
Knowledge Q&A — FastAPI application entry point.

Configures CORS, registers route modules, and manages the application
lifecycle (FAISS index load on startup, MongoDB client teardown on
shutdown).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load FAISS index.  Shutdown: close MongoDB client."""
    from vectorstore.faiss_store import load_store

    await load_store()
    logger.info("Application started successfully")
    yield
    from database import client

    client.close()
    logger.info("Application shutdown")


# ── App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="Knowledge Q&A API",
    description="Upload text documents and ask questions grounded in their content.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────
from config import CORS_ORIGINS  # noqa: E402 (after app creation to avoid circular)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────
from routes.documents import router as documents_router  # noqa: E402
from routes.qa import router as qa_router  # noqa: E402
from routes.status import router as status_router  # noqa: E402

app.include_router(documents_router)
app.include_router(qa_router)
app.include_router(status_router)


@app.get("/api")
async def root():
    """Root health-check — confirms the API is reachable."""
    return {"message": "Knowledge Q&A API", "version": "1.0.0"}
