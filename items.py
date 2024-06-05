# items.py

from pydantic import BaseModel, Field

"""
The library items class is represent all the items in the class - which is books and disks.
it contains 3 main attributes:
 1. is_borrowed - boolean attribute that check if the item is borrowed by customer or not
 2. title - the library item title
 3. isbn - the unique id of the item
 """


class LibraryItem(BaseModel):
    is_borrowed: bool = Field(default=False)
    title: str = Field(..., max_length=60)
    isbn: str = Field(Field(..., pattern=r'^\d{9}$'))
