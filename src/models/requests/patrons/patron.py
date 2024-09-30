from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

from src.mongodb.mongodb_models.patron_model import PatronDocument

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



class AddPatronsRequest(BaseModel):
    patrons_to_add: List[PatronDocument]


class PatronRequest(BaseModel):
    patron_id: str = Field(..., pattern=r'^\d{9}$')
