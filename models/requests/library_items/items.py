# library_items.py

from pydantic import BaseModel, Field

from models.entities.library_items.items import LibraryItem

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
    library_item: LibraryItem
    patron_id: str = Field(Field(..., pattern=r'^\d{9}$'))
