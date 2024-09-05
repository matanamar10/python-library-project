from typing import Optional

from pydantic import Field

from src.models.entities.library_items.disks.disks import Disk


class DVD(Disk):
    director: str = Field(..., max_length=100, description="Director of the DVD")
    duration: Optional[int] = Field(None, description="Duration of the DVD in minutes")
