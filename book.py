# book.py
from items import LibraryItem
from pydantic import Field

"""
The Book class inherit from LibraryItem class and will represent the books in the library.
The only attribute which book got and default "library item" don't - is the author of the book.
"""


class Book(LibraryItem):
    author: str = Field(..., max_length=60)
