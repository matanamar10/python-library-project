# book.py
from models.entities.library_items.items import LibraryItem
from pydantic import Field

from models.requests.library_items.items import LibraryItemRequest

"""
The Book class inherits from LibraryItem and represents books in the library_system.

Attributes:
    author (str): The author of the book.
"""


class BookRequest(LibraryItemRequest):
    author: str = Field(..., max_length=60)

    class Config:
        schema_extra = {
            "example": {
                "is_borrowed": "False",
                "title": "MessiGoat",
                "isbn": "987654321",
                "author": "Jon Snow"
            }
        }
