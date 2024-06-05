from typing import ClassVar

from patron import Patron

"""The Teacher class is inherit from the patron class and contains one extended attribute: 
1. discount - discount percentage on borrowing items"""


class Teacher(Patron):
    discount: ClassVar[float] = 0.6
