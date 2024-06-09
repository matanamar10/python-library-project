from typing import ClassVar

from library_objects.patron import Patron

"""
Represents a teacher patron with additional attributes.

Attributes:
    discount (float): The discount rate for the teacher.
"""


class Teacher(Patron):
    discount: ClassVar[float] = 0.6
