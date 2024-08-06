from typing import ClassVar

from models.entities.patrons.patron import Patron
from models.requests.patrons.patron import PatronRequest

"""
Represents a teacher patron with additional attributes.

Attributes:
    discount (float): The discount rate for the teacher.
"""


class TeacherRequest(PatronRequest):
    discount: ClassVar[float] = 0.6

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "patron_id": "123456789",
                "patron_items": {
                    "9781234567890": "2024-09-01T00:00:00",
                    "9789876543210": None
                },
                "discount": 0.6
            }
        }
