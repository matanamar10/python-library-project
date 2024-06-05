# students.py is a file which represents the students - type of actually patron.
import logging
from typing import ClassVar

from patron import Patron
from pydantic import BaseModel, Field, field_validator, ValidationError


class Student(Patron):
    age: int = Field(..., ge=14, le=99)
    discount: ClassVar[float] = 0.3

    """Assign book specific student - add the book to the list of books which user got"""
