from beanie import Document
from typing import Literal
from src.env_utils import MongoDBSettings


class LibraryItem(Document):
    is_borrowed: bool
    title: str
    isbn: str
    type: Literal["Disk", "Book"]

    class Settings:
        collection = MongoDBSettings().mongo_items_collection
