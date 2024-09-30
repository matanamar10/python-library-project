from pydantic import Field

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class Book(LibraryItemDocument):
    author: str
