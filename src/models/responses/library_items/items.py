from pydantic import BaseModel, Field
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


"""
Represents various responses related to library items in the system.
"""


class LibraryItemResponse(BaseModel):
    """
    Response model representing a library item.

    Attributes:
        item (LibraryItemDocument): The Beanie document representing the library item.
    """
    item: LibraryItemDocument


class LibraryItemStatusResponse(BaseModel):
    """
    Response model for indicating the status of a library item.

    Attributes:
        message (str): A descriptive message about the status of borrowing or returning the item.
        isbn (str): The ISBN of the item being referred to.
    """
    message: str = Field(..., description="A descriptive message about the status of borrowing or returning a specific library item, including the item's ISBN.")
    isbn: str = Field(..., pattern=r'^\d{9}$')


class NewItemsResponse(BaseModel):
    """
    Response model confirming the addition of new items to the library.

    Attributes:
        message (str): A confirmation message indicating successful addition of new items.
    """
    message: str = Field(..., description="A message confirming the successful addition of new items to the library collection.")
