"""
MongoDB async client initialisation.

Exports ``client`` (the raw Motor client, used for admin commands like
ping) and ``db`` (the application database handle used by all services).
Environment variables ``MONGO_URL`` and ``DB_NAME`` are loaded from
``/app/backend/.env`` at import time.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

client: AsyncIOMotorClient = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client[os.environ["DB_NAME"]]
