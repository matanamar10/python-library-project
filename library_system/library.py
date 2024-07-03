import logging
from library_system.library_items.items import LibraryItem
from library_system.patrons.patron import Patron
from pydantic import BaseModel, ValidationError
from typing import Dict, List
from mongodb.mongo_handler import insert_document, delete_document, update_item_status, update_patron_items

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
Represents a library_system with various attributes for managing its system.

Attributes:
    library_items (Dict[str, LibraryItem]): Dictionary of library_system library_items.
    patrons (Dict[str, Patron]): Dictionary of library_system patrons.
    bills (Dict[str, float]): Dictionary of patron bills.
    name (str): The name of the library_system.
"""


class Library(BaseModel):
    library_items: Dict[str, LibraryItem] = {}
    patrons: Dict[str, Patron] = {}
    bills: Dict[str, float] = {}  # Dictionary to keep track of all bills, keyed by patron ID
    name: str

    def add_new_library_items_to_the_library(self, new_library_items: List[LibraryItem]):
        """
        Add new library_items to the library_system.

        Args:
            new_library_items (List[LibraryItem]): List of library_items to add.
        """
        try:
            for new_library_item in new_library_items:
                if new_library_item.isbn in self.library_items:
                    raise ValueError(
                        f"The library item with isbn {new_library_item.isbn} already exists in the library"
                    )
                self.library_items[new_library_item.isbn] = new_library_item
                insert_document('library-items', new_library_item.dict())
                logging.info(
                    f"The library item {new_library_item.title} with isbn {new_library_item.isbn} was added to '{self.name}' library"
                )
        except ValueError as e:
            logging.error(f"Add library item failed: {e}")

    def add_new_patron_to_the_library(self, patrons_to_add: List[Patron]):
        """
        Add new patrons to the library_system.

        Args:
            patrons_to_add (List[Patron]): List of patrons to add.
        """
        try:
            for patron in patrons_to_add:
                if patron.patron_id in self.patrons:
                    raise ValueError(f"The patron with id {patron.patron_id} already exists in the library")
                self.patrons[patron.patron_id] = patron
                insert_document('library-patrons', patron.dict())
                logging.info(f"The patron {patron.name} with id {patron.patron_id} was added to the library")
        except ValidationError as e:
            logging.error(f"Add patron failed: {e}")

    def remove_patrons_from_the_library(self, patrons_to_remove: List[Patron]):
        """
        Remove patrons from the library_system.

        Args:
            patrons_to_remove (List[Patron]): List of patrons to remove.
        """
        try:
            for patron in patrons_to_remove:
                if patron.patron_id not in self.patrons:
                    raise ValueError(f"The patron with id {patron.patron_id} does not exist in the library")
                del self.patrons[patron.patron_id]
                delete_document('library-patrons', {'patron_id': patron.patron_id})
                logging.info(f"The patron {patron.patron_id} was removed from the library")
        except ValidationError as v:
            logging.error(f"Remove patron failed: {v}")

    def search_library_items(self, library_item_title=None, library_item_isbn=None):
        """
        Search for library_system library_items by title or ISBN.

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
        Remove an item from the library_system by ISBN.

        Args:
            library_item_isbn (str): ISBN of the item to remove.
        """
        try:
            if library_item_isbn not in self.library_items:
                raise ValueError(f"The library item with isbn {library_item_isbn} does not exist in the library")
            if self.library_items[library_item_isbn].is_borrowed:
                raise ValueError(f"The library item with isbn {library_item_isbn} is borrowed and cannot be removed")
            del self.library_items[library_item_isbn]
            delete_document('library-items', {'isbn': library_item_isbn})
            logging.info(f"The item {library_item_isbn} was removed from the library")
        except ValueError as e:
            logging.error(f"Remove library item failed: {e}")

    def borrow_library_item(self, library_item: LibraryItem, patron_id: str):
        """
        Borrow a library item.

        Args:
            library_item (LibraryItem): The library item to be borrowed.
            patron_id (str): The ID of the patron borrowing the item.
        """
        try:
            patron = self.patrons.get(patron_id)
            if not patron:
                raise ValueError(f"Patron with ID {patron_id} not found in the library")
            if library_item.isbn not in self.library_items:
                raise ValueError(f"Library item with ISBN {library_item.isbn} not found in the library")
            if library_item.is_borrowed:
                raise ValueError(f"Library item with ISBN {library_item.isbn} is already borrowed")

            patron.add_library_item_to_patron(library_item=library_item)
            library_item.is_borrowed = True

            update_item_status(library_item.isbn, True)
            update_patron_items(patron_id, library_item.isbn, "borrow")

            logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")
        except ValueError as e:
            logging.error(f"Failed to borrow library item: {e}")

    def return_library_item(self, library_item: LibraryItem, patron_id: str):
        """
        Return a borrowed library item.

        Args:
            library_item (LibraryItem): The library item to be returned.
            patron_id (str): The ID of the patron returning the item.
        """
        try:
            patron = self.patrons.get(patron_id)
            if not patron:
                raise ValueError(f"Patron with ID {patron_id} not found in the library")
            if library_item.isbn not in self.library_items:
                raise ValueError(f"Library item with ISBN {library_item.isbn} not found in the library")
            if not library_item.is_borrowed:
                raise ValueError(f"Library item with ISBN {library_item.isbn} is not borrowed")

            patron.remove_library_item_from_patron(library_item)
            library_item.is_borrowed = False

            update_item_status(library_item.isbn, False)
            update_patron_items(patron_id, library_item.isbn, "return")

            logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")
        except ValueError as e:
            logging.error(f"Failed to return library item: {e}")
