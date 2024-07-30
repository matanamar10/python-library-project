import logging
from datetime import datetime
from controllers.management.finance import calculate_bill
from controllers.library import Library
from models.library_items.items import LibraryItem
from utils.custom_library_errors import *
from controllers.controllers_manager import ControllersManager


class BorrowingDepartment:
    def __init__(self):
        self.controller_manager = ControllersManager()

    def return_a_library_item(self, library: Library, library_item: LibraryItem, patron_id: str):
        """
        Handles the return process of a library item by a patron.

        This function updates the library system when a patron returns a borrowed item. It checks if the patron
         exists, verifies   if the item is in the library's inventory and currently borrowed, calculates any
        outstanding bills, and processes the return if all conditions are met.

        Parameters:
        - library (Library): The Library object representing the library system.
        - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being returned.
        - patron_id (str): The unique identifier for the patron returning the item.

        Raises:
        - ValueError: If the patron does not exist, the item is not in the library, the item is not borrowed,
                      or if the patron has outstanding bills.
        """
        patron = library.patrons.get(patron_id)
        if not patron:
            raise PatronNotFoundError(patron_id)
        if library_item.isbn not in library.library_items.keys():
            raise LibraryItemNotFoundError(library_item.isbn)
        if not library_item.is_borrowed:
            raise LibraryItemAlreadyBorrowedError(library_item.isbn)

        patron_calculated_bill = calculate_bill(patron=patron)
        library.bills[patron_id] = patron_calculated_bill

        if library.bills[patron_id] != 0:
            self.controller_manager.bill_repo.update_bill(patron_id, patron_calculated_bill)
            raise BillToPayError(patron_id)
        patron.remove_library_item_from_patron(library_item)
        library_item.is_borrowed = False  # The book is not borrowed anymore.
        self.controller_manager.patron_repo.return_item(patron_id, library_item.isbn)
        self.controller_manager.library_item_repo.update_item_status(library_item.isbn, False)

        logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")

    def borrow_library_item(self, library: Library, library_item: LibraryItem, patron_id: str):
        """
        Handles the borrowing process of a library item by a patron.

        This function updates the library system when a patron borrows an item. It checks if the patron exists,
        verifies if the item is in the library's inventory and not currently borrowed, and processes the borrowing
        if all conditions are met.

        Parameters:
        - library (Library): The Library object representing the library system.
        - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being borrowed.
        - patron_id (str): The unique identifier for the patron borrowing the item.

        Raises:
        - ValueError: If the patron does not exist, the item is not in the library, or if the item is already borrowed.
        """
        if patron_id not in library.patrons.keys():
            raise PatronNotFoundError(patron_id)
        if library_item.isbn not in library.library_items.keys():
            raise LibraryItemNotFoundError(library_item.isbn)
        if library_item.is_borrowed:
            raise LibraryItemAlreadyBorrowedError(library_item.isbn)

        patron = library.patrons[patron_id]
        patron.add_library_item_to_patron(library_item=library_item)
        library_item.is_borrowed = True
        borrow_date = datetime.now()
        self.controller_manager.patron_repo.borrow_item(patron_id, library_item.isbn, borrow_date)
        self.controller_manager.library_item_repo.update_item_status(library_item.isbn, True)

        logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")
