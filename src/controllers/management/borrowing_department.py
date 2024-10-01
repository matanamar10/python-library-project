import logging
from datetime import datetime
from src.controllers.management.finance import calculate_bill
from src.mongodb.mongodb_models.bills_model import Bill
from src.mongodb.mongodb_models.patron_model import Patron
from utils.custom_library_errors import *
from src.controllers.controllers_manager import ControllersManager


class BorrowingDepartment:
    """
    A class to handle borrowing and returning of library items.
    """

    def __init__(self):
        self.controller_manager = ControllersManager()

    async def return_item(self, library_item_isbn: str, patron_id: str):
        """
        Handles the return process of a library item by a patron.

        This function updates the library system when a patron returns a borrowed item.

        Args:
            library_item_isbn (str): The ISBN of the library item being returned.
            patron_id (str): The unique identifier for the patron returning the item.

        Raises:
            PatronNotFoundError: If the patron does not exist.
            LibraryItemNotFoundError: If the library item does not exist.
            BorrowedLibraryItemNotFound: If the library item is not borrowed.
            BillToPayError: If the patron has outstanding bills.
        """
        if not await self.controller_manager.patron_repo.patron_exists(patron_id):
            raise PatronNotFoundError(patron_id)

        if not await self.controller_manager.library_item_repo.item_exists(library_item_isbn):
            raise LibraryItemNotFoundError(library_item_isbn)

        if not await self.controller_manager.library_item_repo.is_item_borrowed(library_item_isbn):
            raise BorrowedLibraryItemNotFound(library_item_isbn)

        patron_document = await Patron.find_one(Patron.id == patron_id)

        patron_calculated_bill = calculate_bill(patron=patron_document)
        bill_document = await Bill.find_one(Bill.patron_id == patron_id)
        bill_document.patron_bill_sum = patron_calculated_bill
        await bill_document.save()

        if bill_document.patron_bill_sum != 0:
            raise BillToPayError(patron_id)

        await self.controller_manager.patron_repo.return_item(patron_id, library_item_isbn)
        await self.controller_manager.library_item_repo.update_item_status(library_item_isbn, False)

        logging.info(f"Library item {library_item_isbn} has been returned by patron {patron_id}")

    async def borrow_item(self, library_item_isbn: str, patron_id: str):
        """
        Handles the borrowing process of a library item by a patron.

        Args:
            library_item_isbn (str): The ISBN of the library item being borrowed.
            patron_id (str): The unique identifier for the patron borrowing the item.

        Raises:
            PatronNotFoundError: If the patron does not exist.
            LibraryItemNotFoundError: If the library item does not exist.
            LibraryItemAlreadyBorrowedError: If the library item is already borrowed.
        """
        if not await self.controller_manager.patron_repo.patron_exists(patron_id):
            raise PatronNotFoundError(patron_id)

        if not await self.controller_manager.library_item_repo.item_exists(library_item_isbn):
            raise LibraryItemNotFoundError(library_item_isbn)

        if await self.controller_manager.library_item_repo.is_item_borrowed(library_item_isbn):
            raise LibraryItemAlreadyBorrowedError(library_item_isbn)

        borrow_date = datetime.now()
        await self.controller_manager.patron_repo.borrow_item(patron_id, library_item_isbn, borrow_date)
        await self.controller_manager.library_item_repo.update_item_status(library_item_isbn, True)

        logging.info(f"Library item {library_item_isbn} has been borrowed by patron {patron_id}")
