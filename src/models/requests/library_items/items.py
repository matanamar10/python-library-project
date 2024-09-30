# library_items.py
from typing import List, Optional

from pydantic import BaseModel, Field

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument

"""
Represents a generic library_system item.

Attributes:
    is_borrowed (bool): Indicates if the item is currently borrowed.
    title (str): The title of the item.
    isbn (str): The ISBN of the item.
"""


class LibraryItemRequest(BaseModel):
    is_borrowed: bool = Field(default=False)
    title: str = Field(..., max_length=60)
    isbn: str = Field(Field(..., pattern=r'^\d{9}$'))

    class Config:
        schema_extra = {
            "example": {
                "is_borrowed": "False",
                "title": "MessiGoat",
                "isbn": "987654321"
            }
        }


class BorrowRequest(BaseModel):
    library_item: LibraryItemDocument
    patron_id: str = Field(Field(..., pattern=r'^\d{9}$'))


class AddItemsRequest(BaseModel):
    library_items: List[LibraryItemDocument]

class ItemRequest(BaseModel):
    item_isbn: str = Field(Field(..., pattern=r'^\d{9}$'))
