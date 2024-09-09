from pydantic import BaseModel, Field
from src.models.entities.patrons.patron import Patron

"""
Represents a library_system patron.

Attributes:
    name (str): The patron's name.
    patron_id (str): The patron's ID.
    patron_items (Dict[str, Optional[datetime]]): Items borrowed by the patron.
"""


class PatronResponse(BaseModel):
    patron: Patron


class LibraryPatronStatusResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")
    patron_id: str = Field(..., pattern=r'^\d{9}$')


class NewPatronsResponse(BaseModel):
    message: str = Field(..., description="A message about the borrow or return status of library item")
