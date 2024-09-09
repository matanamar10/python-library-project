from pydantic import Field

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class BookDocument(LibraryItemDocument):
    author: str = Field(..., max_length=60)
