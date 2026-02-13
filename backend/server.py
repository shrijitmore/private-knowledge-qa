from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Knowledge Q&A API")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.documents import router as documents_router
from routes.qa import router as qa_router
from routes.status import router as status_router

app.include_router(documents_router)
app.include_router(qa_router)
app.include_router(status_router)


@app.get("/api")
async def root():
    return {"message": "Knowledge Q&A API", "version": "1.0.0"}


@app.on_event("startup")
async def startup():
    from vectorstore.faiss_store import load_store
    await load_store()
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown():
    from database import client
    client.close()
    logger.info("Application shutdown")
