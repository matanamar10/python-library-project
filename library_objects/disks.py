# disks.py
from pydantic import Field
from library_objects.items import LibraryItem

"""
The Disk class inherits from LibraryItem and represents disks in the library.

Attributes:
    disk_type (str): The type of the disk (e.g., DVD).
"""


class Disk(LibraryItem):
    disk_type: str = Field(..., max_length=60)
