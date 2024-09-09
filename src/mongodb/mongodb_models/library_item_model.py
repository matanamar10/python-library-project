from beanie import Document
from pydantic import Field
from typing import Literal
from src.env_utils import MongoDBSettings


class LibraryItemDocument(Document):
    is_borrowed: bool = Field(default=False)
    title: str = Field(..., max_length=60)
    isbn: str = Field(..., regex=r'^\d{9}$', unique=True)
    type: Literal["Disk", "Book"]

    class Settings:
        collection = MongoDBSettings().mongo_items_collection  # Ensure this matches your collection name
