# mongo_repository.py

from typing import Dict, Any, Optional, Union
from datetime import datetime
from dal.dal import LibraryItemRepository, PatronRepository, BillRepository
from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument
from mongodb.mongodb_models.bills_model import Bill


class MongoLibraryItemRepository(LibraryItemRepository):
    def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Update the status of a library item identified by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.
            is_borrowed (bool): True if the item is borrowed, False if it is returned.

        """
        library_item = LibraryItemDocument.objects.get(isbn=isbn)
        library_item.is_borrowed = is_borrowed
        library_item.save()

        item = LibraryItemDocument.objects(isbn=isbn).first()
        if item:
            item.update(set__is_borrowed=is_borrowed)

    def insert_document(self, collection_name, document: Union[PatronDocument, LibraryItemDocument]):
        document.save()

    def delete_document(self, collection_name, query):
        LibraryItemDocument.objects(**query).delete()


class MongoPatronRepository(PatronRepository):
    def update_patron_items(self, patron_id: str, isbn: str, action: str,
                            borrow_date: Optional[datetime] = None) -> None:
        patron = PatronDocument.objects(patron_id=patron_id).first()
        if patron:
            if action == 'borrow':
                patron.patron_items[isbn] = borrow_date
            elif action == 'return':
                patron.patron_items.pop(isbn, None)
            patron.save()

    def insert_document(self, collection_name, document: Union[PatronDocument, LibraryItemDocument]):
        document.save()

    def delete_document(self, query: Dict[str, Any]):
        PatronDocument.objects(**query).delete()


class MongoBillRepository(BillRepository):
    def insert_bill(self, patron_id: str, amount: float):
        bill = Bill(patron_id=patron_id, amount=amount)
        bill.save()

    def update_bill(self, patron_id: str, amount: float):
        bill = Bill.objects(patron_id=patron_id).first()
        bill.update(set__amount=amount)

    def delete_bill(self, patron_id: str):
        Bill.objects(patron_id=patron_id).delete()
