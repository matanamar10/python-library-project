# library_items.py

from pydantic import BaseModel, Field

"""
Represents a generic library_system item.

Attributes:
    is_borrowed (bool): Indicates if the item is currently borrowed.
    title (str): The title of the item.
    isbn (str): The ISBN of the item.
"""


class LibraryItemResponse(BaseModel):
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


class LibraryItemStatusResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")
    item: LibraryItemResponse

    class Config:
        schema_extra = {
            "example": {
                "message": "Item The Great Gatsby borrowed successfully by patron 123456789",
                "item": {
                    "title": "The Great Gatsby",
                    "isbn": "123456789",
                    "is_borrowed": True
                }
            }
        }
