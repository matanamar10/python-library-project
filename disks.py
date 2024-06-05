# disks.py
from pydantic import BaseModel, Field, field_validator, ValidationError
from items import LibraryItem


class Disk(LibraryItem):
    disk_type: str = Field(..., max_length=60)
