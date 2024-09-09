from beanie import Document
from typing import Dict
from datetime import datetime
from pydantic import Field
from src.env_utils import MongoDBSettings


class PatronDocument(Document):
    name: str = Field(..., max_length=60)
    id: str = Field(..., regex=r'^\d{9}$', unique=True)
    items: Dict[str, datetime] = Field(...)  # Stores borrowed items and their due dates

    class Settings:
        collection = MongoDBSettings().mongo_patrons_collection
