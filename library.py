import logging
from export_data_to_excel import export_library_items, export_library_patrons
from items import LibraryItem
from patron import Patron
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
The Library Class is represent all the necessary library attributes for managing library system.
The class got some attributes , like : 
1. items - Dictionary which contains all the items we have in our library - books and disks! 
2. patrons - Dictionary which contains all the members of the library - Teachers or Students
3. name - The name of the library 
4. bills - the dictionary which represent the bills of each student or teacher have to pay.  
"""


class Library(BaseModel):
    library_items: Dict[str, LibraryItem] = {}
    patrons: Dict[str, Patron] = {}
    bills: Dict[str, float] = {}  # Dictionary to keep track of all bills, keyed by patron ID
    name: str

    def add_new_library_items_to_the_library(self, new_library_items: List):
        """
        The add_new_library_items_to_the_library function is adding new items - books or disks to the library system
        the function get those arguments as parameters:
        1. new_library_items - list of items to add.
        """

        try:
            for new_library_item in new_library_items:
                if new_library_item.isbn in self.library_items.keys():
                    raise ValueError(f"The library item with isbn {new_library_item.isbn} is already exist in the "
                                     f"Library System")
                self.library_items[new_library_item.isbn] = new_library_item
                export_library_items(self.library_items)
                logging.info(
                    f"The library item {new_library_item.title} with isbn {new_library_item.isbn} is added to "
                    f"'{self.name}' library")
        except ValueError as e:
            logging.error(f"Add library item failed: {e}")

    def add_new_patron_to_the_library(self, patrons_to_add: List):
        """
        The add_new_patrons_to_the_library function is adding new patrons - students or teachers to the library system.
        the function get those arguments as parameters:
        1. patrons_to_add - list of patrons to add.
        """

        try:
            for patron in patrons_to_add:
                if patron.patron_id in self.patrons:
                    raise ValueError(f"The patron with id {patron.patron_id} is already in the library")
                self.patrons[patron.patron_id] = patron
                logging.info(f"The {patron} {patron.patron_id} is added successfully to the library")
                export_library_patrons(self.patrons)
        except ValidationError as e:
            logging.error(f"Add patron failed: {e}")

    def remove_patrons_from_the_library(self, patrons_to_remove: List):
        """
        The remove_patrons_from_the_library function is removing existing patrons -
        students or teachers from the library system.
        the function get those arguments as parameters:
        1. patrons_to_remove - list of patrons to remove.
        """

        try:
            for patron in patrons_to_remove:
                if patron.patron_id not in self.patrons:
                    raise ValueError(f"The patron isn't exists in the library system")
                del self.patrons[patron.patron_id]
                logging.info(f"The patron {patron.patron_id} is removed successfully from the library")
                export_library_patrons(self.library_items)
        except ValidationError as v:
            logging.error(f"Patron addition action failed due to errors: {v}")

    def search_library_items(self, library_item_title=None , library_item_isbn=None):
        """
        The search_library_items function is search for existing library items , filtered by items title/isbn.
        the function get those arguments as parameters:
        1. library_item_title - title to filter on him.
        2. library_item_isbn - isbn to filter on him.
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
        The remove_library_item_from_the_library function is removing existing items -
        disks or books from the library system.
        the function get those arguments as parameters:
        1.library_item_isbn  - item to remove.
        """

        try:
            # Check if the book isbn which provided by user is it exist in the books dictionary
            if library_item_isbn not in self.library_items.keys():
                raise ValueError(f"The library item with isbn {library_item_isbn} is already not in the library")
            if self.library_items[library_item_isbn].is_borrowed:
                raise ValueError(f"The library item with isbn {library_item_isbn} is borrowed and cant be removed")
            del self.library_items[library_item_isbn]
            logging.info(f"The item {library_item_isbn} is removed from the library")
            export_library_items(self.library_items)
        except ValueError as e:
            logging.error(f"The library item deletion failed due to this error: {e}")
