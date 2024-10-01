from pydantic import BaseModel, Field
from src.mongodb.mongodb_models.patron_model import Patron

"""
Represents responses related to library patrons in the system.
"""


class PatronResponse(BaseModel):
    """
    Response model representing a library patron.

    Attributes:
        patron (PatronDocument): The Beanie document representing the library patron.
    """
    patron: Patron


class LibraryPatronStatusResponse(BaseModel):
    """
    Response model indicating the status of a library patron regarding a library item.

    Attributes:
        message (str): A message about the borrow or return status of a library item.
        patron_id (str): The ID of the patron.
    """
    message: str = Field(..., description="A message about the borrow or return status of a library item.")
    patron_id: str = Field(..., pattern=r'^\d{9}$')


class NewPatronsResponse(BaseModel):
    """
    Response model confirming the addition of new patrons to the library system.

    Attributes:
        message (str): A message confirming the successful addition of new patrons.
    """
    message: str = Field(..., description="A message confirming the successful addition of new patrons to the library.")
