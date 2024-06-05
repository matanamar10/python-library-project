from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional
from datetime import datetime
import logging

"""
The Patron Class is an abstract class for teachers and students  - 
The library members.
It contains 3 main attributes:
1. name - the patron name
2. patron_id - the patron id number
3. patron_items - the dictionary of books and disks which assigned to the patron. 
"""


class Patron(BaseModel):
    name: str = Field(..., max_length=60)
    patron_id: str = Field(..., pattern=r'^\d{9}$')
    patron_items: Dict[str, Optional[datetime]] = {}

    def add_library_item_to_patron(self, library_item=None):
        """
        The add_library_item_to_patron is assign a specific item to specific patron - used when patron borrow an item.
        """

        try:
            self.patron_items[library_item.isbn] = datetime.now()
        except ValidationError as e:
            logging.error(f"assign book to student has failed due to unexpected errors: {e}")

    """
    The remove_library_item_from_patron is unassign a specific item from specific patron
     - used when patron return an item.
    """

    def remove_library_item_from_patron(self, library_item=None):
        try:
            del self.patron_items[library_item.isbn]
        except ValueError as e:
            logging.error(f"Tried to remove the item from this student - action failed due to error: {e}")
