import logging
from datetime import datetime
from src.controllers.management.finance import calculate_bill
from src.models.entities.library_items.items import LibraryItem
from src.mongodb.mongodb_models.bills_model import BillDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument
from utils.custom_library_errors import *
from src.controllers.controllers_manager import ControllersManager
from utils.utils import patron_mongoengine_to_pydantic


class BorrowingDepartment:
    def __init__(self):
        self.controller_manager = ControllersManager()

    async def return_item(self, library_item: LibraryItem, patron_id: str):
        """
        Handles the asynchronous return process of a library item by a patron.
        """
        if not await self.controller_manager.patron_repo.patron_exists(patron_id):
            raise PatronNotFoundError(patron_id)

        if not await self.controller_manager.library_item_repo.item_exists(library_item.isbn):
            raise LibraryItemNotFoundError(library_item.isbn)

        if not await self.controller_manager.library_item_repo.is_item_borrowed(library_item.isbn):
            raise BorrowedLibraryItemNotFound(library_item.isbn)

        patron_document = await PatronDocument.find_one(PatronDocument.id == patron_id)
        patron = patron_mongoengine_to_pydantic(patron_document)

        patron_calculated_bill = calculate_bill(patron=patron)
        bill_document = await BillDocument.find_one(BillDocument.patron_id == patron_id)

        bill_document.patron_bill_sum = patron_calculated_bill
        await bill_document.save()

        if bill_document.patron_bill_sum != 0:
            await self.controller_manager.bill_repo.update_bill(patron_id, patron_calculated_bill)
            raise BillToPayError(patron_id)

        patron.remove_library_item_from_patron(library_item)
        library_item.is_borrowed = False

        await self.controller_manager.patron_repo.return_item(patron_id, library_item.isbn)
        await self.controller_manager.library_item_repo.update_item_status(library_item.isbn, False)

        logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")

    async def borrow_item(self, library_item: LibraryItem, patron_id: str):
        """
        Handles the asynchronous borrowing process of a library item by a patron.
        """
        if await self.controller_manager.patron_repo.patron_exists(patron_id):
            raise PatronNotFoundError(patron_id)

        if not await self.controller_manager.library_item_repo.item_exists(library_item.isbn):
            raise LibraryItemNotFoundError(library_item.isbn)

        if await self.controller_manager.library_item_repo.is_item_borrowed(library_item.isbn):
            raise LibraryItemAlreadyBorrowedError(library_item.isbn)

        patron_document = await PatronDocument.find_one(PatronDocument.patron_id == patron_id)
        patron = patron_mongoengine_to_pydantic(patron_document)

        patron.add_library_item_to_patron(library_item=library_item)
        library_item.is_borrowed = True
        borrow_date = datetime.now()

        await self.controller_manager.patron_repo.borrow_item(patron_id, library_item.isbn, borrow_date)
        await self.controller_manager.library_item_repo.update_item_status(library_item.isbn, True)

        logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")
