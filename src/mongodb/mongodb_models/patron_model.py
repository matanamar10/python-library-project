from beanie import Document
from typing import Dict
from datetime import datetime
from src.env_utils import MongoDBSettings


class Patron(Document):
    name: str
    id: str
    items: Dict[str, datetime]

    class Settings:
        collection = MongoDBSettings().mongo_patrons_collection
