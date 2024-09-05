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
    message: str = Field(...,
                         description="A descriptive message about the status of borrowing or returning a specific library item, including the item's ISBN.")
    isbn: str = Field(..., pattern=r'^\d{9}$')


class NewItemsResponse(BaseModel):
    message: str = Field(...,
                         description="A message confirming the successful addition of new items to the library collection")