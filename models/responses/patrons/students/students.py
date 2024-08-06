# students.py is a file which represents the students - type of actually patron.
from typing import ClassVar

from models.entities.patrons.patron import Patron
from pydantic import Field

from models.requests.patrons.patron import PatronRequest
from models.responses.patrons.patron import PatronResponse

"""
Represents a student patron with additional attributes.

Attributes:
    age (int): The age of the student.
    discount (float): The discount rate for the student.
"""


class StudentResponse(PatronResponse):
    age: int = Field(..., ge=14, le=99)
    discount: ClassVar[float] = 0.7

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "patron_id": "123456789",
                "patron_items": {
                    "9781234567890": "2024-09-01T00:00:00",
                    "9789876543210": None
                },
                "age": 17,
                "discount": 0.7
            }
        }
