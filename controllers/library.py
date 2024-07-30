import logging

from controllers.controllers_manager import ControllersManager
from models.library_items.items import LibraryItem
from models.patrons.patron import Patron
from pydantic import BaseModel
from typing import Dict, List, Optional
from utils.utils import patron_pydantic_to_mongoengine, item_pydantic_to_mongoengine
from utils.custom_library_errors import *

"""
Represents a library system with various attributes for managing its system.

Attributes:
    library_items (Dict[str, LibraryItem]): Dictionary of library items.
    patrons (Dict[str, Patron]): Dictionary of library patrons.
    bills (Dict[str, float]): Dictionary of patron bills.
    name (str): The name of the library.
 """


class Library(BaseModel):
    library_items: Dict[str, LibraryItem] = {}
    patrons: Dict[str, Patron] = {}
    bills: Dict[str, float] = {}
    name: str
    controllers_manager: Optional[ControllersManager] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.controllers_manager:
            self.controllers_manager = ControllersManager()

    def add_new_library_items_to_the_library(self, new_library_items: List[LibraryItem]):
        """
        Add new library items to the library system.

        Args:
            new_library_items (List[LibraryItem]): List of library items to add.
        """
        for new_library_item in new_library_items:
            if new_library_item.isbn in self.library_items.keys():
                raise ItemAlreadyExistsError(new_library_item.isbn)
            self.library_items[new_library_item.isbn] = new_library_item
            new_library_item_document = item_pydantic_to_mongoengine(new_library_item)
            self.controllers_manager.library_item_repo.insert_document(new_library_item_document)
            logging.info(
                f"The library item {new_library_item.title} with ISBN {new_library_item.isbn} "
                f"was added to '{self.name}' library"
            )

    def add_new_patron_to_the_library(self, patrons_to_add: List[Patron]):
        """
        Add new patrons to the library system.

        Args:
            patrons_to_add (List[Patron]): List of patrons to add.
        """
        for patron in patrons_to_add:
            if patron.patron_id in self.patrons.keys():
                raise PatronAlreadyExistsError(patron.patron_id)
            self.patrons[patron.patron_id] = patron
            patron_document = patron_pydantic_to_mongoengine(patron)
            self.controllers_manager.patron_repo.insert_document(patron_document)
            logging.info(f"The patron {patron.name} with ID {patron.patron_id} was added to the library")

    def remove_patrons_from_the_library(self, patrons_to_remove: List[Patron]):
        """
        Remove patrons from the library system.

        Args:
            patrons_to_remove (List[Patron]): List of patrons to remove.
        """

        for patron in patrons_to_remove:
            if patron.patron_id not in self.patrons:
                raise PatronNotFoundError(patron.patron_id)
            del self.patrons[patron.patron_id]
            self.controllers_manager.patron_repo.delete_document({'patron_id': patron.patron_id})
            logging.info(f"The patron {patron.patron_id} was removed from the library")

    def search_library_items(self, library_item_title=None, library_item_isbn=None):
        """
        Search for library items by title or ISBN.

        Args:
            library_item_title (str): Title to filter by.
            library_item_isbn (str): ISBN to filter by.

        Returns:
            List[str]: List of matching item titles.
        """
        results = []
        for library_item in self.library_items.values():
            if (library_item_title is None or library_item_title in library_item.title) or \
                    (library_item_isbn is None or library_item_isbn == library_item.isbn):
                results.append(library_item.title)
        logging.info(f"Filter matches: {results}")
        return results

    def remove_library_item_from_the_library(self, library_item_isbn: str):
        """
        Remove an item from the library system by ISBN.

        Args:
            library_item_isbn (str): ISBN of the item to remove.
        """
        if library_item_isbn not in self.library_items.keys():
            raise LibraryItemNotFoundError(
                f"The library item with ISBN {library_item_isbn} does not exist in the library")
        if self.library_items[library_item_isbn].is_borrowed:
            raise ValueError(f"The library item with ISBN {library_item_isbn} is borrowed and cannot be removed")
        del self.library_items[library_item_isbn]
        self.controllers_manager.library_item_repo.delete_document({'isbn': library_item_isbn})
        logging.info(f"The item {library_item_isbn} was removed from the library")
