# disks.py
from pydantic import BaseModel, Field, field_validator, ValidationError
from items import LibraryItem

"""The Book class inherit from LibraryItem class and will represent the books in the library.
The only attribute which book got and default "library item" don't - is the type of the disk - dvd , etc."""


class Disk(LibraryItem):
    disk_type: str = Field(..., max_length=60)
