# students.py is a file which represents the students - type of actually patron.
from typing import ClassVar

from library_objects.patron import Patron
from pydantic import Field

"""
Represents a student patron with additional attributes.

Attributes:
    age (int): The age of the student.
    discount (float): The discount rate for the student.
"""


class Student(Patron):
    age: int = Field(..., ge=14, le=99)
    discount: ClassVar[float] = 0.7
