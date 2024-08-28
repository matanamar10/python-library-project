# library_items.py
from pydantic import BaseModel, Field

from src.models.entities.library_items.items import LibraryItem

"""
Represents a generic library_system item.

Attributes:
    is_borrowed (bool): Indicates if the item is currently borrowed.
    title (str): The title of the item.
    isbn (str): The ISBN of the item.
"""


class LibraryItemResponse(BaseModel):
    item: LibraryItem


class LibraryItemStatusResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")
    isbn: str = Field(..., pattern=r'^\d{9}$')


class NewItemsResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")


class NewPatronsResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")
