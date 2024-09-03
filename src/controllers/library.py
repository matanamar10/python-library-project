import logging

from src.controllers.controllers_manager import ControllersManager
from src.models.entities.library_items.items import LibraryItem
from src.models.entities.patrons.patron import Patron
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument
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
    items: Dict[str, LibraryItem] = {}
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

    def add_new_items(self, new_library_items: List[LibraryItem]):
        """
        Add new library items to the library system.

        Args:
            new_library_items (List[LibraryItem]): List of library items to add.
        """
        for new_library_item in new_library_items:
            if LibraryItemDocument.objects(isbn=new_library_item.isbn).count() > 0:
                raise ItemAlreadyExistsError(new_library_item.isbn)
            new_library_item_document = item_pydantic_to_mongoengine(new_library_item)
            self.controllers_manager.library_item_repo.insert_document(new_library_item_document)
            logging.info(
                f"The library item {new_library_item.title} with ISBN {new_library_item.isbn} "
                f"was added to '{self.name}' library"
            )

    def add_new_patrons(self, patrons_to_add: List[Patron]):
        """
        Add new patrons to the library system.

        Args:
            patrons_to_add (List[Patron]): List of patrons to add.
        """
        for patron in patrons_to_add:
            if PatronDocument.objects(patron_id=patron.patron_id).count() > 0:
                raise PatronAlreadyExistsError(patron.patron_id)
            patron_document = patron_pydantic_to_mongoengine(patron)
            self.controllers_manager.patron_repo.insert_document(patron_document)
            logging.info(f"The patron {patron.name} with ID {patron.patron_id} was added to the library")

    def remove_patron(self, patron_id: str = Field(..., pattern=r'^\d{9}$')):
        """
        Remove patrons from the library system.

        Args:
            patrons_to_remove (List[Patron]): List of patrons to remove.
            :param patron_id:
        """

        if PatronDocument.objects(patron_id=patron_id).count() == 0:
            raise PatronNotFoundError(patron_id)
        self.controllers_manager.patron_repo.delete_document({'patron_id': patron_id})
        logging.info(f"The patron {patron_id} was removed from the library")

    def search_items(self, title=None, isbn=None):
        """
        Search for library items by title or ISBN.

        Args:
            title (str): Title to filter by.
            isbn (str): ISBN to filter by.

        Returns:
            List[str]: List of matching item titles.
        """
        query = {}
        if title:
            query['title'] = {'$regex': title, '$options': 'i'}
        if isbn:
            query['isbn'] = isbn

        items = list(collection.find(query))
        return items

    def remove_item(self, library_item_isbn: str = Field(..., pattern=r'^\d{9}$')):
        """
        Remove an item from the library system by ISBN.

        Args:
            library_item_isbn (str): ISBN of the item to remove.
        """
        if LibraryItemDocument.objects(isbn=library_item_isbn).count() == 0:
            raise LibraryItemNotFoundError(
                f"The library item with ISBN {library_item_isbn} does not exist in the library")
        if LibraryItemDocument.objects(isbn=library_item_isbn).first().is_borrowed:
            raise LibraryItemAlreadyBorrowedError(
                f"The library item with ISBN {library_item_isbn} is borrowed and cannot be removed")
        self.controllers_manager.library_item_repo.delete_document({'isbn': library_item_isbn})
        logging.info(f"The item {library_item_isbn} was removed from the library")
