from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

from src.models.entities.patrons.patron import Patron

"""
Represents a library_system patron.

Attributes:
    name (str): The patron's name.
    patron_id (str): The patron's ID.
    patron_items (Dict[str, Optional[datetime]]): Items borrowed by the patron.
"""


class LibraryPatronRequest(BaseModel):
    name: str = Field(..., max_length=60)
    patron_id: str = Field(..., pattern=r'^\d{9}$')
    patron_items: Dict[str, Optional[datetime]] = {}

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "patron_id": "123456789",
                "patron_items": {
                    "9781234567890": "2024-09-01T00:00:00",
                    "9789876543210": None
                }
            }
        }


class AddPatronsRequest(BaseModel):
    patrons_to_add: List[Patron]


class PatronRequest(BaseModel):
    patron_id: str = Field(..., pattern=r'^\d{9}$')
