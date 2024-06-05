from typing import ClassVar

from patron import Patron


class Teacher(Patron):
    discount: ClassVar[float] = 0.5
