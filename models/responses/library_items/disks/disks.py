# disks.py
from pydantic import Field
from models.requests.library_items.items import LibraryItemRequest
from models.responses.library_items.items import LibraryItemResponse

"""
The Disk class inherits from LibraryItem and represents disks in the library_system.

Attributes:
    disk_type (str): The type of the disk (e.g., DVD).
"""


class DiskResponse(LibraryItemResponse):
    disk_type: str = Field(..., max_length=60)

    class Config:
        schema_extra = {
            "example": {
                "is_borrowed": "False",
                "title": "MessiGoat",
                "isbn": "987654321",
                "disk_type": "CD"
            }
        }
