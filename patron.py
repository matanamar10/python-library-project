from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional
from datetime import datetime
import logging

"""
The Patron Class is an abstract class for teachers and students  - 
The library members 
"""


class Patron(BaseModel):
    name: str = Field(..., max_length=60)
    patron_id: str = Field(..., pattern=r'^\d{9}$')
    patron_items: Dict[str, Optional[datetime]] = {}

    def add_library_item_to_patron(self, library_item=None):
        try:
            self.patron_items[library_item.isbn] = library_item
        except ValidationError as e:
            logging.error(f"assign book to student has failed due to unexpected errors: {e}")

    def remove_library_item_from_patron(self, library_item=None):
        try:
            del self.patron_items[library_item.isbn]
        except ValueError as e:
            logging.error(f"Tried to remove the item from this student - action failed due to error: {e}")
