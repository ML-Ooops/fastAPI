from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.news_database
