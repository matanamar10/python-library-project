# book.py
from items import LibraryItem
from pydantic import Field


class Book(LibraryItem):
    author: str = Field(..., max_length=60)
