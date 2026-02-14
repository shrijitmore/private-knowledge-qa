"""
MongoDB async client initialisation.

Exports ``client`` (the raw Motor client, used for admin commands like
ping) and ``db`` (the application database handle used by all services).
Environment variables ``MONGO_URL`` and ``DB_NAME`` are loaded from
``/app/backend/.env`` at import time.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI, DB_NAME

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
