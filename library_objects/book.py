# book.py
from library_objects.items import LibraryItem
from pydantic import Field

"""
The Book class inherits from LibraryItem and represents books in the library.

Attributes:
    author (str): The author of the book.
"""


class Book(LibraryItem):
    author: str = Field(..., max_length=60)
