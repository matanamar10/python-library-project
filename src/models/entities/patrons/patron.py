from pydantic import BaseModel, Field, ValidationError, validator, field_validator
from typing import Dict, Optional
from datetime import datetime
import logging

"""
Represents a library_system patron.

Attributes:
    name (str): The patron's name.
    patron_id (str): The patron's ID.
    patron_items (Dict[str, Optional[datetime]]): Items borrowed by the patron.
"""


class Patron(BaseModel):
    name: str = Field(..., max_length=60)
    id: str = Field(..., pattern=r'^\d{9}$')
    items: Dict[str, Optional[datetime]] = {}

    def add_library_item_to_patron(self, library_item=None):
        """
        Assign a library_system item to the patron.

        Args:
            library_item (LibraryItem): The item to assign.
        """

        try:
            self.patron_items[library_item.isbn] = datetime.now()
        except ValidationError as e:
            logging.error(f"assign book to student has failed due to unexpected errors: {e}")

    def remove_library_item_from_patron(self, library_item=None):
        """
        Unassign a library_system item from the patron.

        Args:
            library_item (LibraryItem): The item to unassign.
        """

        try:
            del self.patron_items[library_item.isbn]
        except ValueError as e:
            logging.error(f"Tried to remove the item from this student - action failed due to error: {e}")
