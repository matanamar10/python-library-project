# students.py is a file which represents the students - type of actually patron.
from typing import ClassVar

from patron import Patron
from pydantic import Field

"""The Student class is inherit from the patron class and contains two extended attributes: 
1. age - the student age - a number between 14 to 99
2. discount - discount percentage on borrowing items"""


class Student(Patron):
    age: int = Field(..., ge=14, le=99)
    discount: ClassVar[float] = 0.7
