import logging
from exporter.export_data_to_excel import export_data, item_row_preparer, patron_row_preparer
from library_system.library_items.items import LibraryItem
from library_system.patrons.patron import Patron
from pydantic import BaseModel, ValidationError
from typing import Dict, List

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

    def add_new_library_items_to_the_library(self, new_library_items: List):
        """
        Add new library_items to the library_system.

        Args:
            new_library_items (List[LibraryItem]): List of library_items to add.
        """

        try:
            for new_library_item in new_library_items:
                if new_library_item.isbn in self.library_items.keys():
                    raise ValueError(
                        f"The library_system item with isbn {new_library_item.isbn} is already exist in the "
                        f"Library System")
                self.library_items[new_library_item.isbn] = new_library_item
                # export_data(self.library_items, '../data/library_items.csv', ["ISBN", "Type", "Title",
                # "Is Borrowed?"], item_row_preparer)
                logging.info(
                    f"The library_system item {new_library_item.title} with isbn {new_library_item.isbn} is added to "
                    f"'{self.name}' library_system")
        except ValueError as e:
            logging.error(f"Add library_system item failed: {e}")

    def add_new_patron_to_the_library(self, patrons_to_add: List):
        """
        Add new patrons to the library_system.

        Args:
            patrons_to_add (List[Patron]): List of patrons to add.
        """

        try:
            for patron in patrons_to_add:
                if patron.patron_id in self.patrons:
                    raise ValueError(f"The patron with id {patron.patron_id} is already in the library_system")
                self.patrons[patron.patron_id] = patron
                logging.info(f"The {patron} {patron.patron_id} is added successfully to the library_system")
        #                export_data(self.patrons, '../data/patrons.csv', ["ID", "Type", "Name", "Library-Items"],
        #                           patron_row_preparer)
        except ValidationError as e:
            logging.error(f"Add patron failed: {e}")

    def remove_patrons_from_the_library(self, patrons_to_remove: List):
        """
        Remove patrons from the library_system.

        Args:
            patrons_to_remove (List[Patron]): List of patrons to remove.
        """

        try:
            for patron in patrons_to_remove:
                if patron.patron_id not in self.patrons:
                    raise ValueError(f"The patron isn't exists in the library_system system")
                del self.patrons[patron.patron_id]
                logging.info(f"The patron {patron.patron_id} is removed successfully from the library_system")
        #                export_data(self.patrons, '../data/patrons.csv', ["ID", "Type", "Name", "Library-Items"],
        #                           patron_row_preparer)
        except ValidationError as v:
            logging.error(f"Patron addition action failed due to errors: {v}")

    def search_library_items(self, library_item_title=None, library_item_isbn=None):
        """
        Search for library_system library_items by title or ISBN.

        Args:
            library_item_title (str): Title to filter by.
            library_item_isbn (str): ISBN to filter by.

        Returns:
            List[str]: List of matching item titles.
        """

        # The results list is a list where all the filter results will be saved
        results = []
        for library_item in self.library_items.values():
            if (library_item_title is None or library_item.title in library_item_title) or \
                    (library_item_isbn is None or library_item.isbn == library_item_isbn):
                results.append(library_item.title)
        logging.info(f"Those are the filter matches: \n ")
        for result in results:
            logging.info(result)
        return results

    def remove_libray_item_from_the_library(self, library_item_isbn: str):
        """
        Remove an item from the library_system by ISBN.

        Args:
            library_item_isbn (str): ISBN of the item to remove.
        """

        try:
            # Check if the book isbn which provided by user is it exist in the books dictionary
            if library_item_isbn not in self.library_items.keys():
                raise ValueError(
                    f"The library_system item with isbn {library_item_isbn} is already not in the library_system")
            if self.library_items[library_item_isbn].is_borrowed:
                raise ValueError(
                    f"The library_system item with isbn {library_item_isbn} is borrowed and cant be removed")
            del self.library_items[library_item_isbn]
            logging.info(f"The item {library_item_isbn} is removed from the library_system")
        # export_data(self.library_items, '../data/library_items.csv', ["ID", "Type", "Name", "Library-Items"],
        # item_row_preparer)
        except ValueError as e:
            logging.error(f"The library_system item deletion failed due to this error: {e}")
