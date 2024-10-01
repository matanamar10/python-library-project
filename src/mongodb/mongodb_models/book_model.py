from pydantic import Field

from src.mongodb.mongodb_models.library_item_model import LibraryItem


class Book(LibraryItem):
    author: str
